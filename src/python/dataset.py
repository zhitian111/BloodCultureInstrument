import os
import torch
import pyarrow.feather as feather
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split

# 1. 数据加载与预处理（一次性完成）
path = os.path.join("..", "..", "dataset", "processed_data")
# 读取原始数据
datas = feather.read_feather(os.path.join(path, "data.arrow"))
labels_all = feather.read_feather(os.path.join(path, "label.arrow"))

# 筛选SPE_Result为2或3的样本（保留标签和对应的元数据）
filtered_labels = labels_all[(labels_all["SPE_Result"] == 2) | (labels_all["SPE_Result"] == 3)]
# 提取所需列（避免重复索引，提高访问效率）
labels = filtered_labels["SPE_Result"]
counts = filtered_labels["Count"]
begins = filtered_labels["Begin"]
ends = filtered_labels["End"] + 1  # 需要+1调整结束位置

# 2. 划分训练集和测试集索引
all_indices = range(len(labels))
train_indices, test_indices = train_test_split(
    all_indices,
    test_size=0.2,  # 显式指定测试集比例
    train_size=0.8,
    shuffle=True,
    stratify=labels
)


# 3. 定义数据集类
class BCIDataset(Dataset):
    def __init__(self, used_indices, used_datas, used_labels, used_counts, used_begins, used_ends):
        """
        初始化数据集

        参数:
            used_indices: 用于当前数据集的索引（训练/测试索引）
            used_datas: 原始数据（data.arrow内容）
            used_labels: 标签列（SPE_Result）
            used_counts: Count列
            used_begins: Begin列
            used_ends: End列（已+1调整）
        """
        self.indices = used_indices
        # 将依赖数据传入实例变量（避免全局变量）
        self.datas = used_datas
        self.labels = used_labels
        self.counts = used_counts
        self.begins = used_begins
        self.ends = used_ends

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, item):
        # 获取当前样本在筛选后数据中的索引
        idx = self.indices[item]

        # 基于索引提取数据（使用实例变量而非全局变量）
        label = self.labels.iloc[idx]
        count = self.counts.iloc[idx]
        begin = self.begins.iloc[idx]
        end = self.ends.iloc[idx]

        # 截取数据片段（确保begin和end在有效范围内）
        # 增加边界检查，避免索引越界
        if begin < 0:
            begin = 0
        if end > len(self.datas):
            end = len(self.datas)
        data = self.datas.iloc[begin:end].values

        # 转换为张量并返回
        return {
            'label': torch.tensor(label, dtype=torch.short),
            'count': torch.tensor(count, dtype=torch.int16),
            'data': torch.tensor(data, dtype=torch.float32)
        }


# 4. 创建训练集和测试集实例
train_dataset = BCIDataset(
    used_indices=train_indices,
    used_datas=datas,
    used_labels=labels,
    used_counts=counts,
    used_begins=begins,
    used_ends=ends
)
test_dataset = BCIDataset(
    used_indices=test_indices,
    used_datas=datas,
    used_labels=labels,
    used_counts=counts,
    used_begins=begins,
    used_ends=ends
)

# 测试代码
if __name__ == "__main__":

    for i in range(0, 100):
        sample = train_dataset.__getitem__(i)
        print("训练集样本：")
        print(f"标签: {sample['label']}")
        print(f"计数: {sample['count']}")
        print(f"数据形状: {sample['data'].shape}")
