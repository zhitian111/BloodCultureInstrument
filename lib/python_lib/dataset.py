import torch
import random
from torch.utils.data import Dataset
import pyarrow.feather as feather
from sklearn.model_selection import train_test_split
from .global_config import PATH_CONFIG


class DictDataset(Dataset):
    def __init__(self, test_size=0.2, shuffle=True, random_state=42, drop_rate=0.1):
        """简化版血液培养数据集，假设数据格式规范，省略冗余校验"""
        # 加载数据（简化异常处理）
        self.datas = feather.read_feather(PATH_CONFIG['PROCESSED_DATA_FILE'])
        self.labels_df = feather.read_feather(PATH_CONFIG['PROCESSED_LABEL_FILE'])

        # 筛选标签（仅保留2/3类）
        self.labels_df = self.labels_df[
            self.labels_df["SPE_Result"].isin([2, 3])
        ].reset_index(drop=True)

        # 提取关键列（省略长度一致性校验）
        self.labels = self.labels_df["SPE_Result"]
        self.counts = self.labels_df["Count"]
        self.begins = self.labels_df["Begin"]
        self.ends = self.labels_df["End"] + 1  # 调整结束索引

        self.seed = random_state
        self.drop_rate = drop_rate

        # 划分训练/测试索引
        self.indices = range(len(self.labels))
        self.train_indices, self.test_indices = train_test_split(
            self.indices,
            test_size=test_size,
            shuffle=shuffle,
            stratify=self.labels,
            random_state=random_state
        )

        # 初始化模式
        self.status = True  # True:训练, False:测试
        self.if_drop = True  # 是否启用长度调整

    def __len__(self):
        """返回当前模式下的样本量"""
        return len(self.train_indices) if self.status else len(self.test_indices)

    def __getitem__(self, item):
        # 1. 获取当前模式的索引（确保索引有效）
        try:
            idx = self.train_indices[item] if self.status else self.test_indices[item]
        except IndexError:
            # 极端情况：索引越界，返回默认样本
            return {
                'label': torch.tensor(0.0, dtype=torch.float32),
                'count': torch.tensor(0, dtype=torch.int16),
                'data': torch.zeros(1024, 1, dtype=torch.float32)
            }

        # 2. 提取样本信息（确保数值有效，避免异常）
        try:
            original_label = self.labels.iloc[idx]
            begin = int(self.begins.iloc[idx])
            end = int(self.ends.iloc[idx])
        except (ValueError, IndexError):
            # 数值转换/提取失败，用默认值
            original_label = 2  # 默认标签（2类）
            count = 100  # 默认长度
            begin = 0  # 默认起始索引
            end = begin + count  # 默认结束索引

        # 3. 确保 begin < end（避免截取空数据）
        begin = max(0, begin)  # 起始索引不小于0
        end = max(begin + 1, end)  # 结束索引至少比起始大1（保证截取到数据）
        count = end - begin  # 重新计算count，确保与实际截取长度一致

        # 4. 调整数据长度（核心逻辑，确保count合法）
        if self.if_drop and original_label == 3 and count > 120:
            random.seed(self.seed + idx)
            count = random.randint(10, count)
            end = begin + count  # 重新计算end，确保与新count匹配

        # 5. 截取数据并处理（确保生成合法张量）
        try:
            # 截取数据（限制end不超过总数据长度，避免越界）
            max_data_len = len(self.datas)
            end = min(end, max_data_len)
            data_slice = self.datas.iloc[begin:end].values
            data_tensor = torch.tensor(data_slice, dtype=torch.float32)
        except Exception:
            # 数据截取/张量创建失败，用零张量替代
            data_tensor = torch.zeros(count, 1, dtype=torch.float32)

        # 6. 补零/截断到目标长度（1024行），确保形状合法
        target_length = 1024
        current_length = data_tensor.shape[0]
        if current_length > target_length:
            data_padded = data_tensor[:target_length, :]
        else:
            pad_length = target_length - current_length
            zero_pad = torch.zeros(pad_length, 1, dtype=torch.float32)
            data_padded = torch.cat([data_tensor, zero_pad], dim=0)

        # 7. 处理标签（确保是0.0/1.0的float类型）
        label = 0.0 if original_label == 2 else 1.0  # 二分类标签
        label_tensor = torch.tensor(label, dtype=torch.float32)

        # 8. 返回完整的合法数据（无None）
        return {
            'label': label_tensor,  # float32类型
            'count': torch.tensor(count, dtype=torch.int32),  # int32类型
            'data': data_padded  # 1024×1的float32张量
        }

    # 模式切换方法
    def train(self):
        self.status = True

    def test(self):
        self.status = False

    # 长度调整开关
    def drop(self):
        self.if_drop = True

    def un_drop(self):
        self.if_drop = False

    def __repr__(self):
        return (f"DictDataset(train_size={len(self.train_indices)}, "
                f"test_size={len(self.test_indices)}, "
                f"current_mode={'train' if self.status else 'test'})")


# 测试代码
if __name__ == "__main__":
    dataset = DictDataset(test_size=0.2, random_state=42)
    print(dataset)

    dataset.train()
    print(f"训练集长度: {len(dataset)}")
    sample = dataset[0]
    print(f"训练样本 - 标签: {sample['label']}, 数据形状: {sample['data'].shape}, 数据: {sample['data']}")

    dataset.test()
    print(f"测试集长度: {len(dataset)}")
    sample = dataset[0]
    print(f"测试样本 - 标签: {sample['label']}, 数据形状: {sample['data'].shape}")
