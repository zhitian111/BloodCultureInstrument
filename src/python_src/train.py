import torch
from torch.utils.data import DataLoader
from lib.python_lib.dataset import DictDataset  # 导入自定义数据集
from lib.python_lib.model import SimpleNN       # 导入模型
import torch.nn as nn
import torch.optim as optim

# ===================== 超参数设置 =====================
BATCH_SIZE = 32    # 批量大小
EPOCHS = 5         # 训练轮数
LEARNING_RATE = 0.001  # 学习率

# ===================== 数据加载 =====================
# 初始化训练集
train_dataset = DictDataset(test_size=0.2, random_state=42)
train_dataset.train()
train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True  # 训练时打乱数据
)

# 初始化测试集
test_dataset = DictDataset(test_size=0.2, random_state=42)
test_dataset.test()
test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE
)

# ===================== 模型、损失、优化器初始化 =====================
model = SimpleNN(input_dim=1024, output_dim=1)  # 900维输入→1维输出
criterion = nn.BCEWithLogitsLoss()  # 二分类损失（配合sigmoid）
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# ===================== 训练循环 =====================
for epoch in range(EPOCHS):
    model.train()  # 开启训练模式（如Dropout、BatchNorm生效）
    running_loss = 0.0

    for batch_idx, batch in enumerate(train_loader):
        # 提取数据和标签
        data = batch['data']
        labels = batch['label']  # Dataset中已将标签转为0/1（2→0，3→1）

        # 前向传播
        outputs = model(data).squeeze()  # 输出形状: [batch_size]
        loss = criterion(outputs, labels)

        # 反向传播与优化
        optimizer.zero_grad()  # 清空梯度
        loss.backward()        # 反向传播
        optimizer.step()       # 更新参数

        running_loss += loss.item()

        # 打印批次日志
        if (batch_idx + 1) % 50 == 0:
            print(f"Epoch [{epoch+1}/{EPOCHS}], "
                  f"Batch [{batch_idx+1}/{len(train_loader)}], "
                  f"Loss: {loss.item():.4f}")

    # 打印 epoch 平均损失
    avg_loss = running_loss / len(train_loader)
    print(f"Epoch {epoch+1}/{EPOCHS}, Average Loss: {avg_loss:.4f}")

# ===================== 测试评估 =====================
model.eval()  # 开启评估模式（如Dropout、BatchNorm关闭）
correct = 0
total = 0

with torch.no_grad():  # 测试时关闭梯度计算
    for batch in test_loader:
        data = batch['data']
        labels = batch['label']
        outputs = model(data).squeeze()
        predictions = (outputs > 0.5).float()  # sigmoid阈值0.5，转为0/1
        total += labels.size(0)
        correct += (predictions == labels).sum().item()

accuracy = 100 * correct / total
print(f"Test Accuracy: {accuracy:.2f}%")

# ===================== 模型保存（可选） =====================
torch.save(model.state_dict(), "simple_nn_model.pth")
print("Model saved to 'simple_nn_model.pth'.")