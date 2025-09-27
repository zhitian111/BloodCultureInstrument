import os
import torch
import pyarrow
from torch.utils.data import Dataset, DataLoader
import pyarrow.feather as feather


class BCI_Dataset(Dataset):
    def __init__(self, path = os.path.join("..", "..", "dataset", "processed_data",)):
        self.data = feather.read_feather(os.path.join(path, "data.arrow"))

    def __len__(self):
        return self.data.__len__()

    def __getitem__(self, item):
        return self.data.take([item])

test = BCI_Dataset()
print(test.__getitem__(9))