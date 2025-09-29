import torch
import torch.nn as nn
from .global_config import PATH_CONFIG


class SimpleNN(nn.Module):
    def __init__(self, input_dim=1024, output_dim=1):
        """900维输入到1维输出的简单神经网络，含ReLU激活"""
        super(SimpleNN, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 256),   # 第一层：1024→256
            nn.ReLU(inplace=True),       # ReLU激活（节省内存）
            nn.Linear(256, 128),         # 第二层：256→128
            nn.ReLU(inplace=True),
            nn.Linear(128, 64),          # 第三层：128→64
            nn.ReLU(inplace=True),
            nn.Linear(64, output_dim)    # 输出层：64→1（二分类用sigmoid）
        )

    def forward(self, x):
        """前向传播：自动展平三维输入（如[batch, 900, 1]→[batch, 900]）"""
        if x.dim() == 3:
            x = x.view(x.size(0), -1)  # 展平为二维张量
        return self.layers(x)
