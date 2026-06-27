# 🌍 寰宇维基 / OmniWiki

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)  

![Flask Version](https://img.shields.io/badge/Flask-2.0+-green.svg)  

![License](https://img.shields.io/badge/License-MIT-yellow.svg)  

![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)  


**一个功能完整的本地Wiki系统，支持页面编辑、讨论区、用户系统等完整功能**  

**A fully-featured local Wiki system with page editing, discussion forums, user system and more**  


[快速开始](#-快速开始--quick-start) • [功能介绍](#-功能介绍--features) • [安装指南](#-安装指南--installation) • [截图](#-截图--screenshots)  


---

## 📖 目录 / Table of Contents

- [项目简介 / Introduction](#-项目简介--introduction)  
- [功能介绍 / Features](#-功能介绍--features)  
- [技术栈 / Tech Stack](#-技术栈--tech-stack)  
- [快速开始 / Quick Start](#-快速开始--quick-start)  
- [详细安装 / Detailed Installation](#-详细安装--detailed-installation)  
- [项目结构 / Project Structure](#-项目结构--project-structure)
- [API 文档 / API Documentation](#-api-文档--api-documentation)
- [配置说明 / Configuration](#-配置说明--configuration)
- [截图 / Screenshots](#-截图--screenshots)
- [常见问题 / FAQ](#-常见问题--faq)
- [贡献指南 / Contributing](#-贡献指南--contributing)
- [许可证 / License](#-许可证--license)

---

## 📋 项目简介 / Introduction

### 中文

**寰宇维基 (OmniWiki)** 是一个功能完整的本地Wiki系统，专为个人知识管理和团队协作设计。所有数据存储在本地，无需联网，完全保护您的隐私。系统采用现代化的Fandom风格界面，提供流畅的编辑体验和强大的讨论功能。

### English

**OmniWiki** is a fully-featured local Wiki system designed for personal knowledge management and team collaboration. All data is stored locally, requiring no internet connection and ensuring complete privacy. The system features a modern Fandom-style interface, providing a smooth editing experience and powerful discussion capabilities.
**Notice!** there's only chinese version available now, eng version is still designing
---

## ✨ 功能介绍 / Features

### 核心功能 / Core Features

| 功能 / Feature | 描述 / Description |
|---------------|-------------------|
| 📝 **页面系统 / Page System** | 创建、编辑、浏览、删除Wiki页面，支持Markdown语法 |
| 👤 **用户系统 / User System** | 注册、登录、个人主页、角色权限管理 |
| 🔍 **搜索功能 / Search** | 实时搜索建议、全文检索、搜索结果高亮 |
| 🏷️ **标签系统 / Tags** | 标签云、按标签筛选页面 |
| 💬 **评论系统 / Comments** | 发表评论、回复、点赞、删除，支持Markdown |
| 🗣️ **讨论区 / Discussions** | 发起话题、回复、置顶、关闭、热度排序 |
| 📸 **图片上传 / Image Upload** | 上传图片并自动插入编辑器 |
| 📜 **版本历史 / Version History** | 查看编辑历史、恢复到任意版本 |
| 🎨 **视觉特效 / Visual Effects** | 点击烟花特效、鼠标几何图形跟随 |

### 界面特性 / UI Features

| 特性 / Feature | 描述 / Description |
|---------------|-------------------|
| 🌙 **深色主题 / Dark Theme** | 舒适的深色界面，保护眼睛 |
| 📱 **响应式设计 / Responsive** | 适配桌面、平板、手机 |
| 🎯 **Fandom风格 / Fandom Style** | 三栏布局，侧边栏导航 |
| ⚡ **实时预览 / Live Preview** | 编辑时右侧实时渲染Markdown |
| 🛠️ **富文本工具栏 / Rich Toolbar** | 快捷按钮支持Markdown语法 |

---

## 🛠️ 技术栈 / Tech Stack

| 技术 / Technology | 用途 / Purpose |
|------------------|----------------|
| **Python 3.8+** | 后端语言 |
| **Flask 2.0+** | Web框架 |
| **Markdown** | 内容渲染 |
| **Marked.js** | 前端Markdown解析 |
| **Highlight.js** | 代码语法高亮 |
| **Font Awesome 6** | 图标库 |
| **JSON** | 数据存储 |

---

## 🚀 快速开始 / Quick Start

### 中文

```bash
# 1. 克隆项目
git clone https://github.com/CodeJ-40404/Omniwiki.git
cd omniwiki

# 2. 安装依赖
pip install flask markdown

# 3. 运行服务器
python Omniwiki.py

# 4. 打开浏览器访问
# http://localhost:5000

# 5. 登录测试账号
# 用户名: admin / 密码: admin123
```

### English

```bash
# 1. Clone the repository
git clone https://github.com/CodeJ-40404/Omniwiki.git
cd omniwiki

# 2. Install dependencies
pip install flask markdown

# 3. Run the server
python Omniwiki.py

# 4. Open your browser and visit
# http://localhost:5000

# 5. Login with test account
# Username: admin / Password: admin123
```

---

## 📦 详细安装 / Detailed Installation

### 中文

#### 系统要求
- Python 3.8 或更高版本
- pip 包管理器
- 现代浏览器（Chrome, Firefox, Edge 等）

#### 安装步骤

1. **下载项目**
   ```bash
   git clone https://github.com/CodeJ-40404/Omniwiki.git
   cd Omniwiki
   ```

2. **创建虚拟环境（推荐）**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install flask markdown
   ```

4. **初始化数据**
   ```bash
   # 运行后会自动创建数据文件
   python Omniwiki.py
   ```

5. **访问系统**
   - 打开浏览器访问 `http://localhost:5000`
   - 使用测试账号登录：`admin / admin123`

### English

#### Requirements
- Python 3.8 or higher
- pip package manager
- Modern browser (Chrome, Firefox, Edge, etc.)

#### Installation Steps

1. **Download the project**
   ```bash
   git clone https://github.com/CodeJ-40404/Omniwiki.git
   cd omniwiki
   ```

2. **Create virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask markdown
   ```

4. **Initialize data**
   ```bash
   # Data files will be created automatically when running
   python Omniwiki.py
   ```

5. **Access the system**
   - Open your browser and visit `http://localhost:5000`
   - Login with test account: `admin / admin123`

---

## 📁 项目结构 / Project Structure
~~some are still designing~~
```
omniwiki/
│
├── Omniwiki.py                          # 主服务器程序
├── wiki_data.json                  # Wiki数据文件（自动生成）
├── discussions_data.json           # 讨论数据文件（自动生成）
├── comments_data.json              # 评论数据文件（自动生成）
├── uploads/                        # 上传的图片文件夹
│
├── templates/                      # 模板文件夹
│   ├── base.html                   # 基础模板
│   ├── index.html                  # 首页
│   ├── wiki_page.html              # 页面浏览
│   ├── edit.html                   # 编辑页面
│   ├── create.html                 # 创建页面
│   ├── discussions.html            # 讨论区
│   ├── recent_discussions.html     # 最新讨论
│   ├── hot_discussions.html        # 热门讨论
│   ├── my_discussions.html         # 我的讨论
│   ├── search.html                 # 搜索结果
│   ├── login.html                  # 登录页
│   ├── register.html               # 注册页
│   ├── all_pages.html              # 所有页面
│   ├── tags.html                   # 标签云
│   ├── history.html                # 版本历史
│   └── 404.html                    # 404页面
│
└── static/                         # 静态文件
    ├── style.css                   # 主样式表
    └── script.js                   # 前端脚本
```

---

## 🔌 API 文档 / API Documentation

### 中文

| 端点 / Endpoint | 方法 / Method | 描述 / Description |
|----------------|---------------|-------------------|
| `/api/search?q={query}` | GET | 搜索建议API |
| `/api/comments/{page}` | GET | 获取页面评论 |
| `/api/comments/{page}` | POST | 添加评论 |
| `/api/comments/{page}/{id}/like` | POST | 点赞评论 |
| `/api/discussions/{page}` | GET | 获取讨论列表 |
| `/api/discussions/{page}/topic` | POST | 创建话题 |
| `/api/discussions/{page}/topic/{id}/reply` | POST | 回复话题 |
| `/api/hot-discussions-full` | GET | 获取热门讨论 |
| `/api/my-discussions-full` | GET | 获取我的讨论 |

### English

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/search?q={query}` | GET | Search suggestions API |
| `/api/comments/{page}` | GET | Get page comments |
| `/api/comments/{page}` | POST | Add comment |
| `/api/comments/{page}/{id}/like` | POST | Like comment |
| `/api/discussions/{page}` | GET | Get discussion list |
| `/api/discussions/{page}/topic` | POST | Create topic |
| `/api/discussions/{page}/topic/{id}/reply` | POST | Reply to topic |
| `/api/hot-discussions-full` | GET | Get hot discussions |
| `/api/my-discussions-full` | GET | Get my discussions |

---

## ⚙️ 配置说明 / Configuration

### 中文

#### 环境变量

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `SECRET_KEY` | Flask会话密钥 | `huan-yu-wiki-secret-key-2026` |
| `PORT` | 服务器端口 | `5000` |
| `DEBUG` | 调试模式 | `True` |

#### 修改端口

```python
# 在 Omniwiki.py 中修改
app.run(debug=True, host='127.0.0.1', port=8080)
```

### English

#### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session secret key | `huan-yu-wiki-secret-key-2026` |
| `PORT` | Server port | `5000` |
| `DEBUG` | Debug mode | `True` |

#### Change Port

```python
# Modify in Omniwiki.py
app.run(debug=True, host='127.0.0.1', port=8080)
```

---

## 📸 截图 / Screenshots

### 中文

> 由于项目是本地运行，请自行启动后体验。界面风格类似于 Fandom Wiki，采用深色主题和三栏布局。

### English

> Since the project runs locally, please start it yourself to experience. The UI style is similar to Fandom Wiki, featuring a dark theme and three-column layout.

---

## ❓ 常见问题 / FAQ

### 中文

**Q: 保存页面后没有变化？**
A: 检查 `Omniwiki.py` 中 `/edit/<page_name>` 的 POST 处理逻辑是否正确。

**Q: 图片上传失败？**
A: 确保 `uploads/` 文件夹存在且有写入权限。

**Q: 评论功能不工作？**
A: 检查 `comments_data.json` 文件是否已创建。

**Q: 如何备份数据？**
A: 备份以下文件：`wiki_data.json`、`discussions_data.json`、`comments_data.json` 和 `uploads/` 文件夹。

### English

**Q: The page doesn't change after saving?**
A: Check if the POST handling logic in `/edit/<page_name>` of `Omniwiki.py` is correct.

**Q: Image upload fails?**
A: Make sure the `uploads/` folder exists and has write permissions.

**Q: Comment feature doesn't work?**
A: Check if the `comments_data.json` file has been created.

**Q: How to backup data?**
A: Backup the following files: `wiki_data.json`, `discussions_data.json`, `comments_data.json` and the `uploads/` folder.

---

## 👥 贡献指南 / Contributing

### 中文

欢迎贡献代码、报告问题或提出新功能建议！

1. Fork 本项目
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### English

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 许可证 / License

### 中文

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

### English

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 致谢 / Acknowledgements

### 中文

- [Flask](https://flask.palletsprojects.com/) - 轻量级Web框架
- [Marked.js](https://marked.js.org/) - Markdown解析器
- [Highlight.js](https://highlightjs.org/) - 代码高亮
- [Font Awesome](https://fontawesome.com/) - 图标库

### English

- [Flask](https://flask.palletsprojects.com/) - Lightweight web framework
- [Marked.js](https://marked.js.org/) - Markdown parser
- [Highlight.js](https://highlightjs.org/) - Code syntax highlighting
- [Font Awesome](https://fontawesome.com/) - Icon library

---

**Made with 🍌 by OmniWiki Contributors**  

*codej-40404*

[⬆ 返回顶部 / Back to Top](#)

