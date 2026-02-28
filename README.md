# 知习云 — BUAA 共享练习平台

> 一个基于 Python/Django 构建的题目共享与自测平台，支持用户注册登录、题目上传（OCR识别）、题组管理、小组协作、错题推荐及学习统计可视化等功能。

## 功能特性

- **用户管理**：注册、登录、个人资料管理（头像、简介等）
- **题目管理**：创建、编辑、删除题目，支持文本和图片两种格式
- **OCR 识别**：通过上传图片自动识别文本，快速录入题目内容
- **题组管理**：将题目整理为题单，支持分科目分类
- **题组共享**：将题单分享给指定小组或公开发布
- **用户小组**：创建和加入学习小组，成员可共享题单
- **题目搜索**：搜索公开或小组内共享的题目和题单
- **错题回顾**：根据错误频率和科目智能推荐复习题目
- **学习统计**：可视化展示每日做题量、正确率及科目分布
- **敏感词过滤**：基于 DFA 算法自动过滤题目中的敏感词
- **管理后台**：自定义 Django 管理界面

## 技术栈

- **后端**：Python 3.8+、Django 4.2
- **前端**：Tailwind CSS、原生 JavaScript
- **数据库**：SQLite（开发）/ MySQL（生产可选）
- **OCR**：Tesseract + pytesseract + Pillow
- **机器学习**：scikit-learn、scipy、numpy（用于错题推荐算法）
- **其他**：django-markdownx（Markdown 支持）、django-widget-tweaks

## 环境要求

- Python 3.8 或更高版本
- pip（Python 包管理器）
- Tesseract OCR 引擎（用于图片文字识别）
- （可选）Conda 环境管理器

## 安装步骤

### 1. 克隆仓库到本地

```bash
git clone https://github.com/plhlalala/BUAA_python_summer_project.git
cd BUAA_python_summer_project
```

### 2. 创建并激活虚拟环境

**使用 pip + venv：**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**或使用 Conda：**

```bash
conda create --name se python=3.8
conda activate se
```

### 3. 安装依赖

**使用 pip（推荐）：**

```bash
pip install -r requirements-pip.txt
```

**使用 Conda + pip（Windows 平台）：**

```bash
conda install --file requirements-conda.txt
pip install django-markdownx==4.0.7 django-widget-tweaks==1.4.5
```

### 4. 安装 Tesseract OCR

OCR 功能依赖 Tesseract 引擎，请根据操作系统安装：

- **Ubuntu/Debian**：
  ```bash
  sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
  ```
- **macOS**：
  ```bash
  brew install tesseract tesseract-lang
  ```
- **Windows**：从 [Tesseract 官方页面](https://github.com/UB-Mannheim/tesseract/wiki) 下载安装包，并将安装路径添加到系统 PATH，或在 `questions/views.py` 中 `ocr_image` 函数里指定实际安装路径（常见路径示例）：
  ```python
  # 64 位系统（常见）
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  # 32 位系统
  # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
  ```

### 5. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级管理员（可选）

```bash
python manage.py createsuperuser
```

### 7. 运行开发服务器

```bash
python manage.py runserver
```

在浏览器中访问 `http://127.0.0.1:8000/` 即可使用平台。

管理员后台地址：`http://127.0.0.1:8000/admin/`

## 项目结构

```
BUAA_python_summer_project/
├── core/                   # 首页视图和学习能力模型
├── groups/                 # 用户小组管理
├── questions/              # 题目、题组、答题记录管理
├── user/                   # 用户注册、登录、个人资料
├── shareplatform/          # Django 项目配置（settings、urls等）
├── templates/              # 全局 HTML 模板
├── static/                 # 静态文件（CSS、JS、图片）
├── media/                  # 用户上传的媒体文件
├── sensitive_word_filter.py  # 基于 DFA 的敏感词过滤器
├── sensitive_words_lines.txt # 敏感词列表
├── requirements-pip.txt    # pip 依赖列表
├── requirements-conda.txt  # Conda 依赖列表
└── manage.py
```

## 使用说明

1. **注册/登录**：访问 `/user/register/` 注册账号，然后登录。
2. **创建题目**：登录后进入题目管理页面，可手动输入或通过上传图片 OCR 识别录入题目。
3. **整理题单**：将题目添加到题单中，便于分类管理和练习。
4. **加入小组**：在小组页面搜索并加入感兴趣的学习小组，或创建自己的小组。
5. **共享题单**：将题单分享给小组成员或设置为公开，供他人练习。
6. **练习题目**：在题单详情页开始练习，系统会记录答题情况。
7. **查看统计**：在统计页面查看答题数据和学习曲线。
8. **错题复习**：在错题页面根据科目和数量获取智能推荐复习题目。

## 配置说明

- **密钥安全**：生产环境部署前，请将 `shareplatform/settings.py` 中的 `SECRET_KEY` 替换为随机生成的密钥，并将 `DEBUG` 设置为 `False`。
- **允许的主机**：在 `settings.py` 的 `ALLOWED_HOSTS` 中添加您的服务器域名或 IP 地址。
- **数据库**：默认使用 SQLite，如需使用 MySQL，请修改 `settings.py` 中的 `DATABASES` 配置，并确保已安装 PyMySQL。
- **OCR 路径**：Linux/macOS 下 Tesseract 通常安装在 `/usr/bin/tesseract`，Windows 下请参照第 4 步配置路径。