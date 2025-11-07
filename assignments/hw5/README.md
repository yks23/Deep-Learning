# 实验5 — 用 RNN 学习对 K 个整数排序

目标：实现并训练一个小型 RNN（序列到序列），学习把长度为 K 的整数序列按升序排序。这个作业旨在让同学动手实现数据生成、模型训练与推理流程，理解序列建模与自回归解码的基本思路。

目录结构（本作业相关）：

- `train.py` — 训练脚本。生成训练数据、训练模型并保存检查点。
- `infer.py` — 推理脚本。加载检查点，展示模型在若干样例上的排序结果。
- `model.py` — 模型实现（Encoder-Decoder RNN）。

快速一键训练：

```powershell
python assignments/hw5/train.py --epochs 10 --seq-len 6 --vocab-size 10 --batch-size 256
```

训练结束后，模型会保存到 `checkpoints/sort_rnn.pth`（默认），你可以用下面的命令进行推理查看效果：

```powershell
python assignments/hw5/infer.py --checkpoint checkpoints/sort_rnn.pth --n-samples 8 --seq-len 6 --vocab-size 10
```

阅读建议（教学导览）：

- 先打开 `assignments/hw5/model.py`，理解 Encoder-Decoder 的简要实现：
  - Encoder 使用 embedding + GRU 读取源序列；
  - Decoder 使用 GRUCell 自回归生成每个排序后的位置（训练时使用 teacher forcing）；
- 再阅读 `train.py`：数据如何在线生成、训练循环、loss 计算与检查点保存；
- 最后运行 `infer.py` 看模型在随机样本上的表现，观察输入 / 目标 / 预测三者差异。

拓展作业：

- 修改任务为降序排序或不允许重复元素；
- 评估在不同 `vocab-size` 与 `seq-len` 下的泛化能力。
- 用 Attention 或 Pointer Network 改进模型；
