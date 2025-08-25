import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset
from torch import nn

# --- GPU 설정 ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

seq_len = 10
features = ['c_pct','h_pct','l_pct','high_vol']
data = pd.read_csv('preprocess.csv').dropna()

# 시퀀스 생성
def create_seq(df, seq_len):
    X, y = [], []
    for i in range(len(df) - seq_len):
        X.append(df[features].iloc[i:i+seq_len].values)
        y.append(int(df['label'].iloc[i+seq_len]))  # 정수형 보장

    X = np.array(X, dtype=np.float32)  # 리스트 → ndarray
    y = np.array(y, dtype=np.int64)
    return torch.tensor(X), torch.tensor(y)

X, y = create_seq(data, seq_len)
X, y = X.to(device), y.to(device)

# --- DataLoader 생성 ---
dataset = TensorDataset(X, y)
train_size = int(len(dataset) * 0.8)
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, len(dataset)-train_size])
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# --- LSTM 모델 ---
class LSTMClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    def forward(self, x):
        _, (h, _) = self.lstm(x)
        return self.fc(h[-1])

model = LSTMClassifier(input_size=len(features), hidden_size=32, output_size=3).to(device)

# --- 손실함수와 옵티마이저 ---
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# --- 학습 루프 ---
epochs = 20
for epoch in range(epochs):
    model.train()
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        pred = model(xb)
        loss = criterion(pred, yb)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

# --- 평가 ---
model.eval()
correct, total = 0, 0
with torch.no_grad():
    for xb, yb in test_loader:
        xb, yb = xb.to(device), yb.to(device)
        pred = model(xb).argmax(dim=1)
        correct += (pred == yb).sum().item()
        total += yb.size(0)
print(f"Test Accuracy: {correct/total:.4f}")