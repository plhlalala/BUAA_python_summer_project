# BUAA_python_summer_project 使用指南

欢迎使用 BUAA_python_summer_project，本项目是一个基于 Python 和 Django 的 Web 应用。以下是如何在本地运行项目的步骤。

## 环境要求

- Python 3.8 或更高版本
- pip (Python 包管理器)
- Conda 环境管理器

## 安装步骤

### 克隆仓库到本地

打开终端（命令提示符、Powershell 或 Bash），并运行以下命令：

```bash
git clone https://github.com/您的GitHub用户名/BUAA_python_summer_project.git
cd BUAA_python_summer_project
```

### 创建并激活 Conda 环境

使用 `environment.yml` 文件创建 Conda 环境，并激活该环境：

```bash
conda env create -f environment.yml
conda activate se
```

### 安装依赖

在激活的 Conda 环境中，安装通过 pip 管理的依赖：

```bash
pip install -r requirements.txt
```

### 数据库迁移

执行以下命令，以应用数据库迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 运行开发服务器

使用以下命令启动 Django 开发服务器：

```bash
python manage.py runserver
```

在浏览器中访问 `http://127.0.0.1:8000/` 来查看应用。

## 使用说明

- OCR 功能需要将相关路径配置为本地路径。请根据您的环境修改 `settings.py` 中的相关配置。