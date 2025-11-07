## 实验2 — 超参数影响观察（教学版）

目标：通过运行 `mnist.ipynb` 中的实验，观察不同超参数（learning rate、batch size、optimizer、epoch 等）对训练速度与最终性能的影响，并学会如何调参进行基本诊断。

一键环境安装（推荐使用 Conda）：在仓库根目录运行：

```powershell
conda create -n dl python=3.10 -y && conda activate dl && pip install -r requirements.txt && pip install jupyter
```

快速一键运行（在激活环境后）：

1) 在浏览器中启动 Jupyter Notebook：

```powershell
jupyter notebook
```

然后在打开的页面中点击并运行 `assignments/hw2/mnist.ipynb`。

2) 或者直接在命令行中自动执行整个 notebook（将会在控制台打印输出并生成执行后的 notebook）：

```powershell
jupyter nbconvert --to notebook --execute assignments/hw2/mnist.ipynb --ExecutePreprocessor.timeout=600
```

关于 `config.py`：
- 如果你要使用 WandB 或 SwanLab 的在线日志功能，请在 `assignments/hw2/config.py` 中填入相应的 API Key（`wandb_api_key`, `swanlab_api_key`）。如果不使用在线日志，则可以保留默认并跳过相关代码段。

实验建议：
- 先把 `batch size` 设置为小值（例如 16）跑几轮，观察训练曲线的抖动；再加大到 128，比较稳定性与速度；
- 调整学习率（例如 1e-4、1e-3、1e-2）观察收敛情况；
- 尝试不同优化器（SGD / Adam）并比较训练曲线。