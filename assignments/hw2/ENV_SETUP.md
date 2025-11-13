# 📦 完整环境配置教程（macOS 版）

本教程将指导你从零开始配置完整的开发环境，包括 Git 密钥配置、仓库克隆、Conda 环境创建和依赖安装。

> **Windows 用户注意**：本教程以 macOS 为例，Windows 的特殊情况会在相应步骤中标注说明。

---

## 第一步：配置 Git 密钥（用于 Clone 仓库）

### 使用 SSH 密钥

1. **检查是否已有 SSH 密钥**
   ```bash
   ls -al ~/.ssh
   ```
   如果看到 `id_rsa` 和 `id_rsa.pub` 或 `id_ed25519` 和 `id_ed25519.pub`，说明已有密钥，可跳过步骤2。

2. **生成新的 SSH 密钥**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   或使用 RSA：
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```
   按提示操作（可直接回车使用默认路径，设置密码可选）。

3. **复制公钥内容**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # 或
   cat ~/.ssh/id_rsa.pub
   ```
   复制输出的整个内容。

4. **添加到 GitHub/GitLab**
   - GitHub: Settings → SSH and GPG keys → New SSH key → 粘贴公钥
   - GitLab: Preferences → SSH Keys → 粘贴公钥

---

## 第二步：Clone 仓库

```bash
# 使用 SSH（推荐）
git clone git@github.com:username/Deep-Learning.git

# 进入项目目录
cd Deep-Learning
```

---

## 第三步：配置 Conda 和 Pip 清华源（加速下载）

### 配置 Conda 清华源

```bash
# 添加清华源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/

# 设置搜索时显示通道地址
conda config --set show_channel_urls yes

# 验证配置
conda config --show channels
```

### 配置 Pip 清华源

```bash
# 创建配置文件
code ~/.pip/pip.conf
```

> **Windows 用户**：
> ```powershell
> # 在用户目录下创建 pip 文件夹
> mkdir $env:APPDATA\pip
> 
> # 创建配置文件 pip.ini
> notepad $env:APPDATA\pip\pip.ini
> ```

在打开的文件中输入：
``` ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
```

---

## 第五步：创建 Conda 环境并安装依赖

```bash
# 进入项目根目录
cd Deep-Learning

# 创建 conda 环境（Python 3.12）
conda create -n dl python=3.12 -y

# 激活环境
conda activate dl

# 安装依赖
pip install -r requirements.txt

# 安装 Jupyter 内核（用于在 Jupyter 中使用此环境）
pip install ipykernel
```

---

## 第六步：配置 VSCode 和 Jupyter

1. **安装 VSCode Jupyter 插件**
   - 打开 VSCode
   - 点击左侧扩展图标
   - 搜索 "Jupyter" 并安装

2. **选择内核**
   - 打开 `assignments/hw2/mnist.ipynb`
   - 点击右上角的 "Select Kernel"
   - 选择 "Python (dl)" 或 "dl"

3. **如果提示安装 ipykernel**
   ```bash
   conda activate dl
   pip install ipykernel
   ```

---

## 第七步：配置 API 密钥（可选）

如果需要使用 WandB 或 SwanLab 的在线日志功能：

1. **获取 WandB API Key**
   - 访问 https://wandb.ai/
   - 注册/登录账号
   - Settings → API keys → 复制 API key

2. **获取 SwanLab API Key**
   - 访问 https://swanlab.cn/
   - 注册/登录账号
   - 在个人设置中获取 API key

3. **配置密钥**
   - 编辑 `assignments/hw2/config.py`
   - 将对应的 API key 填入：
   ```python
   wandb_api_key = "your_wandb_api_key_here"
   swanlab_api_key = "your_swanlab_api_key_here"
   ```

如果不使用在线日志功能，可以跳过此步骤。

---

## 🚀 快速开始（已配置好环境后）

```bash
# 激活环境
conda activate dl

# 进入实验目录
cd assignments/hw2

# 在 VSCode 中打开 mnist.ipynb 并运行
```

