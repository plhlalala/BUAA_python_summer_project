# TODOLIST

* 借助django自带的后台管理系统，实现用户和管理员的信息管理。
* 对上传题目是否含有敏感词进行检测，若有则删除。
* 在题目详情页添加评论功能。
* 待补充


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

- OCR 功能需要将相关路径配置为本地路径。请根据您的环境修改 `questions/views.py` 中 `ocr_image`中`pytesseract.pytesseract.tesseract_cmd` 中的相关配置。


## 附：
<h1 style="text-align: center;">Shared Exercise Platform</h1>
 
设计一个平台，学生可以在上面上传和分享问题，并且可以进行自测。

* 基本要求
  1. 使用GUI库如Tkinter、PyQt5，或其他Python支持的前端和后端框架。
  2. 问题应包括多种格式，如选择题和填空题。问题需自行获取。
  3. 界面应美观但不过于花哨，以免影响解题。可以添加其他功能，但应用户友好且易于使用。

* 必须完成的任务
  1. 基本要求：用户和管理员注册、登录及个人信息管理。
  2. 用户组：用户可以选择创建和加入组，用户可以自行搜索并加入组。
  3. 上传：自动识别PDF或图片中的文本。识别后，提取的文本结果可以编辑以完成问题输入。（提示：使用OCR）
  4. 问题分组：设计自己的或利用现有的数据结构，将问题按章节或其他标准分类。解题时，用户可以选择特定的题组。解题界面应根据个人喜好设计，无需过多要求。
  5. 问题分享：用户可以选择将题组分享给特定组或公开分享。共享的接收者可以访问共享的题组。
  6. 搜索组：搜索应具有可定制的参数，但搜索范围应包括共享的题组和用户上传的问题，不应搜索未共享的题组。
  7. 错题日志：根据用户的错误回答、错误频率以及用户指定的科目和题量，参考相关推荐算法生成一组用户应优先重新解决的问题集，使用科学有效的算法。

* 可选任务
  1. 系统具有筛选敏感词并删除题库中敏感词的功能。找到实现该功能的方法。
  2. 可视化学生能力。根据错误答案的类型和时间，参考相关资料定义学生错误问题信息到学生能力信息的转换标准。绘制显示学生能力随时间变化的图表。
  3. 实现额外功能，根据实用性和工作量给予加分。