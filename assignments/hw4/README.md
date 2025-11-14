# 实验4: 运行Diffusion Models
本次实验将指导你如何在本地环境中运行扩散模型（Diffusion Models）。请按照以下步骤进行操作：
先克隆仓库：
https://github.com/byrkbrk/conditional-ddpm.git

然后按照以下步骤进行：
你需要：
- 正确运行推理脚本，生成样本图像
- 正确运行训练脚本，在 MNIST 或 FashionMNIST 上训练模型
- 理解代码结构与主要实现细节
## 环境安装

如果你已经安装了 Conda，在仓库根目录（包含本 `README.md` 的目录）运行下面一行即可创建并激活环境（适用于 Linux/Windows/macOS）：

```powershell
cd conditional-ddpm
conda env create -f diffusion-env_linux_or_windows.yaml && conda activate diffusion-env
```

## 文件与代码导览（快速教学）

- `train.py` — 训练脚本。负责数据加载、模型构建、训练循环与检查点保存。
- `sample.py` — 推理（采样）脚本：从预训练检查点恢复模型并生成样本图像。
- `diffusion_model.py` / `models.py` — 模型定义与去噪网络结构。
- `sampling_functions.py` — 包含逆扩散（sampling）相关的实用函数。
- `utils.py` — 辅助函数（日志、保存、可视化等）。
- `checkpoints/` — 提供了若干预训练权重（例如 `pretrained_mnist_checkpoint_49.pth`）。
- `datasets/` — sprite 数据文件（如适用）。

建议先打开并阅读 `sample.py` 与 `sampling_functions.py`，然后运行推理命令观察结果；随后再阅读 `train.py` 以理解训练流程。

## 一键推理（Inference）—— 快速生成图片并查看推理实现

下面的命令会使用仓库中提供的预训练模型生成样本：

（示例：使用 MNIST 预训练检查点）

```powershell
python sample.py checkpoints/pretrained_mnist_checkpoint_49.pth --n-samples 400 --n-images-per-row 20
```

运行后，生成的图像和动画会被保存到 `generated-images/`（或脚本中指定的输出目录）。

阅读建议：在运行上面的命令之前，请先打开并浏览 `sample.py`，关注以下步骤：

- 如何加载模型权重（checkpoint）
- 如何构造初始噪声并调用采样函数
- `sampling_functions.py` 中的逆扩散循环与噪声调度

这能帮助你把命令行看到的图像与代码实现直接对应起来。

## 一键训练（Training）—— 启动训练并查看训练代码

如果你想从头训练（例如在 MNIST 或 FashionMNIST 上），使用：

```powershell
python train.py --dataset-name mnist
```

可替换 `--dataset-name` 为 `fashion_mnist` 或 `sprite`。训练过程中模型检查点会保存到 `checkpoints/`，生成的日志与中间图片会保存在脚本指定的目录。

阅读建议：打开 `train.py` 并关注：

- 数据增强与 DataLoader 的构造
- 训练循环（loss 计算、反向传播、优化器步骤）
- 如何定期保存检查点与生成样本用于可视化

## 运行小贴士

- GPU：如果有 GPU，确保在激活的 conda 环境中安装了与 CUDA 兼容的 PyTorch，并从 `train.py` / `sample.py` 的输出确认设备为 `cuda`。若无 GPU，脚本会回退到 CPU（会慢很多）。
- 快速调试：把 `--n-samples` 或训练 epoch 设置得小一点以便快速跑通流程。
- 可视化：查看 `generated-images/` 目录中的 JPEG/GIF，通常每个类会按行或分组排列，便于比对。
