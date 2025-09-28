import torch
from torch.utils.data import Dataset
import pyarrow.feather as feather
from sklearn.model_selection import train_test_split
from global_config import PATH_CONFIG


class BCIDataset(Dataset):
    def __init__(self, test_size=0.2, shuffle=True, random_state=42):
        """
        血液培养数据集，支持训练/测试状态切换

        参数:
            test_size: 测试集占比
            shuffle: 是否打乱数据
            random_state: 随机种子，保证划分可复现
        """
        # 1. 加载数据（添加异常处理）
        self.datas = self._load_data(PATH_CONFIG['PROCESSED_DATA_FILE'], 'data.arrow')
        self.labels_df = self._load_data(PATH_CONFIG['PROCESSED_LABEL_FILE'], 'label.arrow')

        # 2. 筛选标签（仅保留SPE_Result为2或3的样本）
        self.labels_df = self.labels_df[
            self.labels_df["SPE_Result"].isin([2, 3])
        ].reset_index(drop=True)  # 重置索引，避免后续索引混乱

        # 3. 提取关键列（增加长度校验，确保数据一致性）
        self._validate_data_length()
        self.labels = self.labels_df["SPE_Result"]
        self.counts = self.labels_df["Count"]
        self.begins = self.labels_df["Begin"]
        self.ends = self.labels_df["End"] + 1  # 调整结束索引

        # 4. 划分训练/测试索引（分层采样，保证类别分布一致）
        self.indices = range(len(self.labels))
        self.train_indices, self.test_indices = train_test_split(
            self.indices,
            test_size=test_size,
            shuffle=shuffle,
            stratify=self.labels,
            random_state=random_state  # 固定随机种子，便于复现
        )

        # 5. 初始状态为训练模式
        self.status = True  # True: 训练模式, False: 测试模式

    @staticmethod
    def _load_data(file_path, data_name):
        """加载feather数据并处理异常"""
        try:
            return feather.read_feather(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"{data_name}不存在，请检查路径: {file_path}")
        except Exception as e:
            raise RuntimeError(f"加载{data_name}失败: {str(e)}")

    def _validate_data_length(self):
        """验证关键列长度一致性，避免索引不匹配"""
        if len(self.labels_df) == 0:
            raise ValueError("筛选后标签为空，请检查SPE_Result筛选条件")

        # 检查counts、begins、ends与labels长度是否一致
        cols = ["Count", "Begin", "End"]
        for col in cols:
            if len(self.labels_df[col]) != len(self.labels_df):
                raise ValueError(f"列 {col} 长度与标签不一致，请检查数据")

    def __len__(self):
        """根据当前状态返回训练/测试集长度"""
        return len(self.train_indices) if self.status else len(self.test_indices)

    def __getitem__(self, item):
        """根据当前状态返回对应样本（增加边界检查）"""
        # 获取当前状态的索引
        if self.status:
            idx = self.train_indices[item]
        else:
            idx = self.test_indices[item]

        # 提取样本信息（增加索引有效性校验）
        self._check_index_valid(idx)
        label = self.labels.iloc[idx]
        count = self.counts.iloc[idx]
        begin = self.begins.iloc[idx]
        end = self.ends.iloc[idx]
        data_slice = self.datas.iloc[begin:end].values

        # 转换为张量并返回
        return {
            'label': torch.tensor(label, dtype=torch.short),
            'count': torch.tensor(count, dtype=torch.int16),
            'data': torch.tensor(data_slice, dtype=torch.float32)
        }

    def _check_index_valid(self, idx):
        """检查索引是否在有效范围内"""
        if idx < 0 or idx >= len(self.labels):
            raise IndexError(f"索引 {idx} 超出有效范围 [0, {len(self.labels) - 1}]")

    def _clip_boundary(self, begin, end):
        """将begin和end限制在datas的有效范围内"""
        max_len = len(self.datas)
        begin = max(0, min(begin, max_len - 1))  # 确保begin >=0 且 < max_len
        end = max(begin + 1, min(end, max_len))  # 确保end > begin 且 <= max_len
        return begin, end

    def train(self):
        """切换到训练模式"""
        self.status = True

    def test(self):
        """切换到测试模式"""
        self.status = False

    def __repr__(self):
        """打印数据集信息，便于调试"""
        return (f"BCIDataset(train_size={len(self.train_indices)}, "
                f"test_size={len(self.test_indices)}, "
                f"current_mode={'train' if self.status else 'test'})")


# 测试代码
if __name__ == "__main__":
    # 初始化数据集
    dataset = BCIDataset(test_size=0.2, random_state=42)
    print(dataset)  # 打印数据集信息

    # 测试训练模式
    dataset.train()
    print(f"训练集长度: {len(dataset)}")
    sample = dataset[0]
    print(f"训练样本 - 标签: {sample['label']}, 数据形状: {sample['data'].shape}")

    # 测试测试模式
    dataset.test()
    print(f"测试集长度: {len(dataset)}")
    sample = dataset[0]
    print(f"测试样本 - 标签: {sample['label']}, 数据形状: {sample['data'].shape}")
