# app.py - 寰宇维基本地服务器主程序
# 运行方式: python app.py 或 在VS中按F5
# 访问地址: http://localhost:5000

import json
import os
import markdown
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = 'huan-yu-wiki-secret-key-2026-change-in-production'

# 数据文件路径
DATA_FILE = 'wiki_data.json'

# ==================== 数据管理函数 ====================

def init_data():
    """初始化数据文件（如果不存在）"""
    if not os.path.exists(DATA_FILE):
        default_data = {
            "users": {
                "admin": {"password": "admin123", "role": "admin", "avatar": "A", "join_date": "2026-01-01"},
                "寰宇行者": {"password": "wiki2026", "role": "editor", "avatar": "🌌", "join_date": "2026-01-15"},
                "蕉学家": {"password": "banana", "role": "contributor", "avatar": "🍌", "join_date": "2026-02-10"}
            },
            "pages": {
                "首页": {
                    "title": "🌍 寰宇维基",
                    "content": """# 欢迎来到寰宇维基

**寰宇维基**是一个运行在你本地的知识库系统，所有数据都存储在您的电脑上，完全离线可用。

## ✨ 特色功能
- 📖 **完整的Wiki系统**：创建、编辑、浏览任意词条
- 🔍 **全文搜索**：快速找到你需要的内容
- 👥 **用户系统**：登录后即可参与编辑
- 🎨 **Fandom风格界面**：现代化深色主题，侧边栏导航

## 🚀 快速开始
1. 点击右上角**登录**（账号：admin / admin123）
2. 点击导航栏的**创建页面**添加新词条
3. 浏览已有页面，点击**编辑**参与贡献

## 📚 示例词条
- [香蕉](/page/香蕉) - 神奇的浆果
- [Python编程](/page/Python编程) - 入门指南
- [赛博朋克](/page/赛博朋克) - 文化解读

> 💡 提示：本Wiki支持Markdown语法！你可以使用标题、列表、代码块等丰富内容。""",
                    "author": "system",
                    "last_edit": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "views": 0,
                    "tags": ["首页", "欢迎"]
                },
                "香蕉": {
                    "title": "🍌 香蕉",
                    "content": """# 🍌 香蕉

**香蕉**（学名：*Musa*）是一种巨型草本植物结出的浆果，是全球贸易量最大的水果之一。

---

## 📖 植物学特征

香蕉植株其实不是树，而是**巨型草本植物**。它的“树干”由叶鞘层层包裹形成假茎，最高可达**9米**！

> 💡 趣味事实：香蕉在植物学上被归类为**浆果**，而草莓反而不是真正的浆果！

---

## 🥗 营养价值

| 营养素 | 含量(每100g) | 功效 |
|--------|--------------|------|
| 钾 | 358mg | 帮助肌肉放松 |
| 维生素B6 | 0.4mg | 提升情绪 |
| 膳食纤维 | 2.6g | 肠道健康 |

---

## 🌍 文化影响

- **音乐**：地下丝绒乐队的香蕉专辑封面
- **电影**：《神偷奶爸》小黄人最爱
- **网络迷因**：香蕉皮滑倒、胶带香蕉艺术品

---

## 🔗 相关词条
- [水果](/page/水果)
- [植物](/page/植物)""",
                    "author": "蕉学家",
                    "last_edit": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "views": 42,
                    "tags": ["水果", "食物", "植物"]
                },
                "Python编程": {
                    "title": "🐍 Python编程",
                    "content": """# Python编程入门

Python是一种简单易学、功能强大的编程语言。

## 为什么选择Python？

- 语法简洁清晰
- 拥有丰富的第三方库
- 适合人工智能、数据分析、Web开发

## 基础示例

```python
# Hello World
print("Hello, Wiki!")

# 列表推导式
squares = [x**2 for x in range(10)]
```

## 学习资源
1. Python官方文档
2. 廖雪峰Python教程
3. Real Python

## 相关词条
- [编程语言](/page/编程语言)
- [人工智能](/page/人工智能)""",
                    "author": "寰宇行者",
                    "last_edit": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "views": 28,
                    "tags": ["编程", "技术", "Python"]
                },
                "赛博朋克": {
                    "title": "🎮 赛博朋克",
                    "content": """# 赛博朋克文化解读

**赛博朋克**（Cyberpunk）是科幻文学的一个子流派，特点是**高科技，低生活**。

## 核心元素

- 🤖 **人工智能**与意识上传
- 💊 **生物改造**与赛博义体
- 💻 **黑客**与数字空间
- 🏙️ **霓虹都市**与贫民窟

## 代表作品

- 电影：《银翼杀手》、《攻壳机动队》
- 游戏：《赛博朋克2077》、《杀出重围》
- 小说：威廉·吉布森《神经漫游者》

> "街头找到了自己的用途。" —— 威廉·吉布森

## 相关词条
- [科幻](/page/科幻)
- [反乌托邦](/page/反乌托邦)""",
                    "author": "admin",
                    "last_edit": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "views": 35,
                    "tags": ["文化", "科幻", "游戏"]
                }
            },
            "recent_activity": []
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)

def load_data():
    """加载所有数据"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """保存数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_activity(action, user, page_name=None):
    """记录用户活动"""
    data = load_data()
    if "recent_activity" not in data:
        data["recent_activity"] = []
    data["recent_activity"].insert(0, {
        "action": action,
        "user": user,
        "page": page_name,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    # 只保留最近50条
    data["recent_activity"] = data["recent_activity"][:50]
    save_data(data)

# ==================== 登录装饰器 ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return "权限不足，需要管理员权限", 403
        return f(*args, **kwargs)
    return decorated_function

# ==================== 路由：页面浏览 ====================

@app.route('/')
def index():
    """首页 - 展示热门页面和最近活动"""
    data = load_data()
    pages = data['pages']
    
    # 获取热门页面（按浏览量排序）
    hot_pages = sorted(pages.items(), key=lambda x: x[1].get('views', 0), reverse=True)[:6]
    
    # 获取最近更新的页面
    recent_pages = sorted(pages.items(), key=lambda x: x[1].get('last_edit', ''), reverse=True)[:6]
    
    # 获取最近活动
    recent_activity = data.get('recent_activity', [])[:10]
    
    # 统计信息
    stats = {
        'total_pages': len(pages),
        'total_users': len(data.get('users', {})),
        'total_views': sum(p.get('views', 0) for p in pages.values())
    }
    
    return render_template('index.html', 
                         hot_pages=hot_pages,
                         recent_pages=recent_pages,
                         recent_activity=recent_activity,
                         stats=stats,
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))

@app.route('/page/<page_name>')
def view_page(page_name):
    """查看单个页面"""
    data = load_data()
    
    if page_name not in data['pages']:
        # 尝试模糊匹配
        suggestions = [p for p in data['pages'].keys() if page_name.lower() in p.lower()]
        return render_template('404.html', page_name=page_name, suggestions=suggestions, username=session.get('username')), 404
    
    page = data['pages'][page_name]
    # 增加浏览量
    page['views'] = page.get('views', 0) + 1
    save_data(data)
    
    # 将Markdown转换为HTML
    content_html = markdown.markdown(page['content'], extensions=['extra', 'codehilite'])
    
    # 获取所有页面列表用于侧边栏
    all_pages = list(data['pages'].keys())
    
    # 获取相关页面（相同标签）
    related_pages = []
    if 'tags' in page:
        for p_name, p_data in data['pages'].items():
            if p_name != page_name and page['tags'] and set(page['tags']) & set(p_data.get('tags', [])):
                related_pages.append(p_name)
    
    return render_template('wiki_page.html',
                         page=page,
                         page_name=page_name,
                         content_html=content_html,
                         all_pages=all_pages,
                         related_pages=related_pages[:5],
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))

# ==================== 路由：编辑与创建 ====================

@app.route('/edit/<page_name>', methods=['GET', 'POST'])
@login_required
def edit_page(page_name):
    """编辑页面"""
    data = load_data()
    
    if page_name not in data['pages']:
        return redirect(url_for('create_page', prefill_name=page_name))
    
    if request.method == 'POST':
        content = request.form['content']
        title = request.form['title']
        tags = request.form.get('tags', '').split(',')
        tags = [t.strip() for t in tags if t.strip()]
        
        data['pages'][page_name] = {
            'title': title,
            'content': content,
            'author': session['username'],
            'last_edit': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'views': data['pages'][page_name].get('views', 0),
            'tags': tags
        }
        save_data(data)
        add_activity(f"编辑了页面「{page_name}」", session['username'], page_name)
        return redirect(url_for('view_page', page_name=page_name))
    
    page = data['pages'][page_name]
    tags_str = ', '.join(page.get('tags', []))
    return render_template('edit.html',
                         page=page,
                         page_name=page_name,
                         tags_str=tags_str,
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))


@app.route('/delete/<page_name>')
@login_required
def delete_page(page_name):
    """删除页面（需要登录）"""
    data = load_data()
    if page_name in data['pages']:
        del data['pages'][page_name]
        save_data(data)
        add_activity(f"删除了页面「{page_name}」", session['username'], page_name)
    return redirect(url_for('index'))

# ==================== 路由：搜索 ====================

@app.route('/api/search')
def api_search():
    """搜索API（用于前端自动补全）"""
    query = request.args.get('q', '').strip().lower()
    
    print(f"API搜索请求: {query}")  # 调试用
    
    if not query:
        return jsonify([])
    
    data = load_data()
    results = []
    
    for name, page in data['pages'].items():
        if query in name.lower() or query in page.get('title', '').lower():
            results.append({
                'name': name,
                'title': page.get('title', name)
            })
    
    print(f"API搜索结果: {len(results)} 条")  # 调试用
    return jsonify(results[:10])

@app.route('/search')
def search_page():
    """搜索页面"""
    query = request.args.get('q', '').strip()
    
    print(f"搜索页面请求: {query}")  # 调试用
    
    if not query:
        return redirect(url_for('index'))
    
    data = load_data()
    results = []
    
    for name, page in data['pages'].items():
        score = 0
        if query.lower() in name.lower():
            score += 10
        if query.lower() in page.get('title', '').lower():
            score += 8
        for tag in page.get('tags', []):
            if query.lower() in tag.lower():
                score += 5
        if query.lower() in page.get('content', '').lower():
            score += 1
        
        if score > 0:
            content = page.get('content', '')
            excerpt = content[:300].replace('\n', ' ')
            import re
            pattern = re.compile(f'({re.escape(query)})', re.IGNORECASE)
            excerpt = pattern.sub(r'<mark>\1</mark>', excerpt)
            
            results.append({
                'name': name,
                'title': page.get('title', name),
                'author': page.get('author', '未知'),
                'last_edit': page.get('last_edit', ''),
                'views': page.get('views', 0),
                'tags': page.get('tags', []),
                'excerpt': excerpt,
                'score': score
            })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return render_template('search.html', 
                         query=query, 
                         results=results,
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))
# ==================== 路由：用户系统 ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = load_data()
        users = data.get('users', {})
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            session['avatar'] = users[username].get('avatar', username[0].upper())
            add_activity(f"登录了系统", username)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='用户名或密码错误')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        email = request.form.get('email', '')
        
        data = load_data()
        
        if username in data.get('users', {}):
            return render_template('register.html', error='用户名已存在')
        
        if len(username) < 2:
            return render_template('register.html', error='用户名至少2个字符')
        
        if len(password) < 3:
            return render_template('register.html', error='密码至少3个字符')
        
        if 'users' not in data:
            data['users'] = {}
        
        data['users'][username] = {
            'password': password,
            'role': 'contributor',
            'avatar': username[0].upper(),
            'join_date': datetime.now().strftime("%Y-%m-%d"),
            'email': email
        }
        save_data(data)
        
        session['username'] = username
        session['role'] = 'contributor'
        session['avatar'] = username[0].upper()
        add_activity(f"注册了新账号", username)
        
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """用户登出"""
    username = session.get('username')
    if username:
        add_activity(f"登出系统", username)
    session.clear()
    return redirect(url_for('index'))



# ==================== 路由：所有页面 ====================

@app.route('/all-pages')
def all_pages():
    """所有页面列表（按字母排序）"""
    data = load_data()
    pages = sorted([(name, data['pages'][name]) for name in data['pages'].keys()], key=lambda x: x[0])
    return render_template('all_pages.html', pages=pages, username=session.get('username'), user_avatar=session.get('avatar'))

@app.route('/random')
def random_page():
    """随机跳转一个页面"""
    import random
    data = load_data()
    pages = list(data['pages'].keys())
    if pages:
        return redirect(url_for('view_page', page_name=random.choice(pages)))
    return redirect(url_for('index'))

@app.route('/preview', methods=['POST'])
@login_required
def preview():
    """实时预览Markdown内容"""
    content = request.json.get('content', '')
    html = markdown.markdown(content, extensions=['extra', 'codehilite', 'toc', 'tables'])
    return jsonify({'html': html})

# ==================== 新增：页面版本历史 ====================

@app.route('/history/<page_name>')
@login_required
def page_history(page_name):
    """查看页面编辑历史"""
    data = load_data()
    if page_name not in data['pages']:
        return redirect(url_for('index'))
    
    history = data['pages'][page_name].get('history', [])
    return render_template('history.html',
                         page_name=page_name,
                         page=data['pages'][page_name],
                         history=history,
                         username=session.get('username'))

@app.route('/restore/<page_name>/<int:version>')
@login_required
def restore_version(page_name, version):
    """恢复到指定版本"""
    data = load_data()
    if page_name not in data['pages']:
        return redirect(url_for('index'))
    
    history = data['pages'][page_name].get('history', [])
    if 0 <= version < len(history):
        old_version = history[version]
        data['pages'][page_name]['content'] = old_version['content']
        data['pages'][page_name]['title'] = old_version['title']
        data['pages'][page_name]['last_edit'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        data['pages'][page_name]['author'] = session['username']
        
        # 记录恢复操作
        add_activity(f"将页面「{page_name}」恢复到版本 {version+1}", session['username'], page_name)
        save_data(data)
    
    return redirect(url_for('edit_page', page_name=page_name))

# ==================== 新增：导出页面 ====================

@app.route('/export/<page_name>')
def export_page(page_name):
    """导出页面为Markdown或HTML"""
    data = load_data()
    if page_name not in data['pages']:
        return "页面不存在", 404
    
    page = data['pages'][page_name]
    export_type = request.args.get('type', 'md')
    
    if export_type == 'md':
        content = f"# {page['title']}\n\n{page['content']}"
        return Response(content, mimetype='text/markdown',
                       headers={'Content-Disposition': f'attachment; filename={page_name}.md'})
    else:
        html = markdown.markdown(page['content'], extensions=['extra', 'codehilite'])
        full_html = f"""<!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>{page['title']}</title>
        <style>body{{max-width:800px;margin:0 auto;padding:2rem;font-family:system-ui;}}</style>
        </head><body>{html}</body></html>"""
        return Response(full_html, mimetype='text/html',
                       headers={'Content-Disposition': f'attachment; filename={page_name}.html'})

# ==================== 新增：图片上传（需要创建uploads文件夹）====================

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    """上传图片到本地"""
    if 'image' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    # 生成唯一文件名
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
        return jsonify({'error': '不支持的图片格式'}), 400
    
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}.{ext}"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    # 返回图片URL
    return jsonify({'url': f'/uploads/{filename}'})

# 静态文件服务（用于访问上传的图片）
from flask import send_from_directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ==================== 标签系统 ====================

@app.route('/tags')
def tags_page():
    """标签云页面"""
    data = load_data()
    
    # 统计所有标签
    tag_counts = {}
    for page_name, page in data['pages'].items():
        for tag in page.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    if not tag_counts:
        return render_template('tags.html', 
                             tags=[],
                             hot_tags=[],
                             total_tags=0,
                             total_used=0,
                             total_pages_with_tags=0,
                             most_used_tag_count=0,
                             username=session.get('username'))
    
    # 计算字体大小（最小14px，最大36px）
    max_count = max(tag_counts.values())
    min_count = min(tag_counts.values())
    
    tags_list = []
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[0].lower()):
        # 字体大小：14 + (count - min) / (max - min) * 22
        if max_count > min_count:
            font_size = 14 + (count - min_count) / (max_count - min_count) * 22
        else:
            font_size = 20
        opacity = 0.6 + (count / max_count) * 0.4 if max_count > 0 else 0.8
        
        tags_list.append({
            'name': tag,
            'count': count,
            'font_size': round(font_size),
            'opacity': round(opacity, 2)
        })
    
    # 热门标签（按使用次数排序，取前12个）
    hot_tags = sorted([{'name': k, 'count': v} for k, v in tag_counts.items()], 
                     key=lambda x: x['count'], reverse=True)[:12]
    
    # 统计信息
    total_pages_with_tags = sum(1 for p in data['pages'].values() if p.get('tags'))
    most_used_tag_count = max(tag_counts.values()) if tag_counts else 0
    
    return render_template('tags.html',
                         tags=tags_list,
                         hot_tags=hot_tags,
                         total_tags=len(tag_counts),
                         total_used=len([t for t in tag_counts.values() if t > 0]),
                         total_pages_with_tags=total_pages_with_tags,
                         most_used_tag_count=most_used_tag_count,
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))

@app.route('/tag/<tag_name>')
def tag_pages(tag_name):
    """查看标签下的所有页面"""
    data = load_data()
    
    # 查找包含该标签的页面
    pages_with_tag = []
    total_views = 0
    last_updated = ''
    
    for name, page in data['pages'].items():
        if tag_name in page.get('tags', []):
            pages_with_tag.append({
                'name': name,
                'page': page
            })
            total_views += page.get('views', 0)
            if page.get('last_edit', '') > last_updated:
                last_updated = page.get('last_edit', '')
    
    # 按最后编辑时间排序
    pages_with_tag.sort(key=lambda x: x['page'].get('last_edit', ''), reverse=True)
    
    # 查找相关标签（共同出现在同一页面中的其他标签）
    related_tags = {}
    for name, page in data['pages'].items():
        if tag_name in page.get('tags', []):
            for tag in page.get('tags', []):
                if tag != tag_name:
                    related_tags[tag] = related_tags.get(tag, 0) + 1
    
    related_tags_list = sorted([{'name': k, 'count': v} for k, v in related_tags.items()],
                              key=lambda x: x['count'], reverse=True)[:10]
    
    return render_template('tag_pages.html',
                         tag=tag_name,
                         pages=pages_with_tag,
                         total_views=total_views,
                         last_updated=last_updated[:10] if last_updated else '暂无',
                         related_tags=related_tags_list,
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))

@app.route('/api/tags')
def api_tags():
    """标签API（用于自动补全）"""
    data = load_data()
    tag_counts = {}
    for page in data['pages'].values():
        for tag in page.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    return jsonify([{'name': k, 'count': v} for k, v in sorted(tag_counts.items())])

@app.route('/api/tags/related')
def api_related_tags():
    """获取相关标签"""
    tag = request.args.get('tag', '')
    if not tag:
        return jsonify([])
    
    data = load_data()
    related = {}
    for page in data['pages'].values():
        if tag in page.get('tags', []):
            for t in page.get('tags', []):
                if t != tag:
                    related[t] = related.get(t, 0) + 1
    
    return jsonify([{'name': k, 'count': v} for k, v in sorted(related.items(), key=lambda x: x[1], reverse=True)[:10]])



# ==================== 评论系统 ====================

# 评论数据文件
COMMENTS_FILE = 'comments_data.json'

def init_comments_file():
    """初始化评论数据文件"""
    if not os.path.exists(COMMENTS_FILE):
        default_comments = {}
        with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_comments, f, ensure_ascii=False, indent=2)

def load_comments():
    """加载所有评论"""
    with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_comments(comments):
    """保存评论"""
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

@app.route('/api/comments/<page_name>', methods=['GET'])
def get_comments(page_name):
    """获取页面的评论列表"""
    comments_data = load_comments()
    page_comments = comments_data.get(page_name, [])
    # 按时间倒序（最新的在前）
    page_comments.sort(key=lambda x: x.get('time', ''), reverse=True)
    return jsonify(page_comments)

@app.route('/api/comments/<page_name>', methods=['POST'])
@login_required
def add_comment(page_name):
    """添加评论"""
    data = request.json
    content = data.get('content', '').strip()
    parent_id = data.get('parent_id', None)
    
    if not content:
        return jsonify({'error': '评论内容不能为空'}), 400
    
    if len(content) > 5000:
        return jsonify({'error': '评论内容不能超过5000字'}), 400
    
    comments_data = load_comments()
    
    if page_name not in comments_data:
        comments_data[page_name] = []
    
    # 生成唯一ID
    comment_id = int(datetime.now().timestamp() * 1000)
    
    new_comment = {
        'id': comment_id,
        'content': content,
        'author': session['username'],
        'avatar': session.get('avatar', session['username'][0].upper()),
        'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'timestamp': datetime.now().timestamp(),
        'likes': 0,
        'parent_id': parent_id,
        'replies': []
    }
    
    if parent_id:
        # 查找父评论并添加回复
        for comment in comments_data[page_name]:
            if comment['id'] == parent_id:
                comment['replies'].append(new_comment)
                break
    else:
        comments_data[page_name].append(new_comment)
    
    save_comments(comments_data)
    
    # 记录活动
    add_activity(f"在页面「{page_name}」发表了评论", session['username'], page_name)
    
    return jsonify(new_comment), 201

@app.route('/api/comments/<page_name>/<int:comment_id>/like', methods=['POST'])
@login_required
def like_comment(page_name, comment_id):
    """点赞评论"""
    comments_data = load_comments()
    
    def find_and_like(comments):
        for comment in comments:
            if comment['id'] == comment_id:
                comment['likes'] = comment.get('likes', 0) + 1
                return True
            if comment.get('replies'):
                if find_and_like(comment['replies']):
                    return True
        return False
    
    if page_name in comments_data:
        find_and_like(comments_data[page_name])
        save_comments(comments_data)
        return jsonify({'success': True})
    
    return jsonify({'error': '评论不存在'}), 404

@app.route('/api/comments/<page_name>/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(page_name, comment_id):
    """删除评论（仅作者或管理员可删）"""
    comments_data = load_comments()
    username = session['username']
    role = session.get('role', 'user')
    
    def find_and_delete(comments):
        for i, comment in enumerate(comments):
            if comment['id'] == comment_id:
                if comment['author'] == username or role == 'admin':
                    del comments[i]
                    return True
                else:
                    return False
            if comment.get('replies'):
                if find_and_delete(comment['replies']):
                    return True
        return False
    
    if page_name in comments_data:
        if find_and_delete(comments_data[page_name]):
            save_comments(comments_data)
            return jsonify({'success': True})
        return jsonify({'error': '无权删除或评论不存在'}), 403
    
    return jsonify({'error': '评论不存在'}), 404

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_page():
    """创建新页面"""
    if request.method == 'POST':
        page_name = request.form.get('page_name', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        tags = request.form.get('tags', '').split(',')
        tags = [t.strip() for t in tags if t.strip()]
        
        if not page_name:
            return "页面名称不能为空", 400
        
        # 清理页面名称（只保留字母、数字、中文、连字符）
        import re
        page_name = re.sub(r'[^\w\u4e00-\u9fa5-]', '', page_name)
        
        if not page_name:
            return "页面名称无效", 400
        
        data = load_data()
        
        if page_name in data['pages']:
            return render_template('create.html', 
                                 error="页面已存在！请使用不同的页面标识符", 
                                 username=session.get('username'),
                                 user_avatar=session.get('avatar'))
        
        data['pages'][page_name] = {
            'title': title,
            'content': content,
            'author': session['username'],
            'last_edit': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'views': 0,
            'tags': tags
        }
        save_data(data)
        add_activity(f"创建了新页面「{page_name}」", session['username'], page_name)
        return redirect(url_for('view_page', page_name=page_name))
    
    # GET 请求：显示创建页面表单
    prefill_name = request.args.get('prefill_name', '')
    return render_template('create.html', 
                         prefill_name=prefill_name, 
                         username=session.get('username'), 
                         user_avatar=session.get('avatar'))



# ==================== 讨论区系统 ====================

DISCUSSIONS_FILE = 'discussions_data.json'

def init_discussions_file():
    """初始化讨论数据文件"""
    if not os.path.exists(DISCUSSIONS_FILE):
        default_data = {}
        with open(DISCUSSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)

def load_discussions():
    """加载所有讨论"""
    with open(DISCUSSIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_discussions(discussions):
    """保存讨论"""
    with open(DISCUSSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(discussions, f, ensure_ascii=False, indent=2)

@app.route('/discussions/<page_name>')
def view_discussions(page_name):
    """查看页面的讨论区"""
    data = load_data()
    if page_name not in data['pages']:
        return redirect(url_for('index'))
    
    discussions_data = load_discussions()
    page_discussions = discussions_data.get(page_name, [])
    # 按时间倒序
    page_discussions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    # 统计讨论数量
    topic_count = len(page_discussions)
    reply_count = sum(len(t.get('replies', [])) for t in page_discussions)
    
    return render_template('discussions.html',
                         page_name=page_name,
                         page=data['pages'][page_name],
                         discussions=page_discussions,
                         topic_count=topic_count,
                         reply_count=reply_count,
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))

@app.route('/api/discussions/<page_name>', methods=['GET'])
def get_discussions(page_name):
    """获取页面的讨论列表API"""
    discussions_data = load_discussions()
    page_discussions = discussions_data.get(page_name, [])
    page_discussions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return jsonify(page_discussions)

@app.route('/api/discussions/<page_name>/topic', methods=['POST'])
@login_required
def create_topic(page_name):
    """创建新话题"""
    data = request.json
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    
    if not title:
        return jsonify({'error': '标题不能为空'}), 400
    if not content:
        return jsonify({'error': '内容不能为空'}), 400
    if len(title) > 200:
        return jsonify({'error': '标题不能超过200字'}), 400
    if len(content) > 5000:
        return jsonify({'error': '内容不能超过5000字'}), 400
    
    discussions_data = load_discussions()
    if page_name not in discussions_data:
        discussions_data[page_name] = []
    
    topic_id = int(datetime.now().timestamp() * 1000)
    
    new_topic = {
        'id': topic_id,
        'title': title,
        'content': content,
        'author': session['username'],
        'avatar': session.get('avatar', session['username'][0].upper()),
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'timestamp': datetime.now().timestamp(),
        'views': 0,
        'likes': 0,
        'reply_count': 0,
        'is_pinned': False,
        'is_closed': False,
        'replies': []
    }
    
    discussions_data[page_name].append(new_topic)
    save_discussions(discussions_data)
    
    # 记录活动
    add_activity(f"在「{page_name}」的讨论区发起了新话题「{title}」", session['username'], page_name)
    
    return jsonify(new_topic), 201

@app.route('/api/discussions/<page_name>/topic/<int:topic_id>/reply', methods=['POST'])
@login_required
def add_reply(page_name, topic_id):
    """回复话题"""
    data = request.json
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'error': '回复内容不能为空'}), 400
    if len(content) > 3000:
        return jsonify({'error': '回复内容不能超过3000字'}), 400
    
    discussions_data = load_discussions()
    
    if page_name not in discussions_data:
        return jsonify({'error': '讨论不存在'}), 404
    
    for topic in discussions_data[page_name]:
        if topic['id'] == topic_id:
            if topic.get('is_closed', False):
                return jsonify({'error': '该话题已关闭，无法回复'}), 403
            
            reply_id = int(datetime.now().timestamp() * 1000)
            new_reply = {
                'id': reply_id,
                'content': content,
                'author': session['username'],
                'avatar': session.get('avatar', session['username'][0].upper()),
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'timestamp': datetime.now().timestamp(),
                'likes': 0,
                'reply_to': None
            }
            topic['replies'].append(new_reply)
            topic['reply_count'] = topic.get('reply_count', 0) + 1
            save_discussions(discussions_data)
            
            add_activity(f"在「{page_name}」的讨论区回复了话题「{topic['title']}」", session['username'], page_name)
            
            return jsonify(new_reply), 201
    
    return jsonify({'error': '话题不存在'}), 404

@app.route('/api/discussions/<page_name>/topic/<int:topic_id>/like', methods=['POST'])
@login_required
def like_topic(page_name, topic_id):
    """点赞话题"""
    discussions_data = load_discussions()
    
    if page_name not in discussions_data:
        return jsonify({'error': '讨论不存在'}), 404
    
    for topic in discussions_data[page_name]:
        if topic['id'] == topic_id:
            topic['likes'] = topic.get('likes', 0) + 1
            save_discussions(discussions_data)
            return jsonify({'likes': topic['likes']})
    
    return jsonify({'error': '话题不存在'}), 404

@app.route('/api/discussions/<page_name>/topic/<int:topic_id>/reply/<int:reply_id>/like', methods=['POST'])
@login_required
def like_reply(page_name, topic_id, reply_id):
    """点赞回复"""
    discussions_data = load_discussions()
    
    if page_name not in discussions_data:
        return jsonify({'error': '讨论不存在'}), 404
    
    for topic in discussions_data[page_name]:
        if topic['id'] == topic_id:
            for reply in topic.get('replies', []):
                if reply['id'] == reply_id:
                    reply['likes'] = reply.get('likes', 0) + 1
                    save_discussions(discussions_data)
                    return jsonify({'likes': reply['likes']})
    
    return jsonify({'error': '回复不存在'}), 404

@app.route('/api/discussions/<page_name>/topic/<int:topic_id>/close', methods=['POST'])
@login_required
def close_topic(page_name, topic_id):
    """关闭/开启话题（仅管理员或作者）"""
    discussions_data = load_discussions()
    username = session['username']
    role = session.get('role', 'user')
    
    if page_name not in discussions_data:
        return jsonify({'error': '讨论不存在'}), 404
    
    for topic in discussions_data[page_name]:
        if topic['id'] == topic_id:
            if topic['author'] == username or role == 'admin':
                topic['is_closed'] = not topic.get('is_closed', False)
                save_discussions(discussions_data)
                return jsonify({'is_closed': topic['is_closed']})
            return jsonify({'error': '无权操作'}), 403
    
    return jsonify({'error': '话题不存在'}), 404

@app.route('/api/discussions/<page_name>/topic/<int:topic_id>/pin', methods=['POST'])
@login_required
def pin_topic(page_name, topic_id):
    """置顶话题（仅管理员）"""
    if session.get('role') != 'admin':
        return jsonify({'error': '需要管理员权限'}), 403
    
    discussions_data = load_discussions()
    
    if page_name not in discussions_data:
        return jsonify({'error': '讨论不存在'}), 404
    
    for topic in discussions_data[page_name]:
        if topic['id'] == topic_id:
            topic['is_pinned'] = not topic.get('is_pinned', False)
            save_discussions(discussions_data)
            return jsonify({'is_pinned': topic['is_pinned']})
    
    return jsonify({'error': '话题不存在'}), 404

@app.route('/api/discussions/<page_name>/topic/<int:topic_id>', methods=['DELETE'])
@login_required
def delete_topic(page_name, topic_id):
    """删除话题（仅管理员或作者）"""
    discussions_data = load_discussions()
    username = session['username']
    role = session.get('role', 'user')
    
    if page_name not in discussions_data:
        return jsonify({'error': '讨论不存在'}), 404
    
    for i, topic in enumerate(discussions_data[page_name]):
        if topic['id'] == topic_id:
            if topic['author'] == username or role == 'admin':
                del discussions_data[page_name][i]
                save_discussions(discussions_data)
                add_activity(f"删除了「{page_name}」讨论区的话题「{topic['title']}」", username, page_name)
                return jsonify({'success': True})
            return jsonify({'error': '无权删除'}), 403
    
    return jsonify({'error': '话题不存在'}), 404


@app.route('/recent-discussions')
def recent_discussions():
    """最新讨论 - 全局讨论区首页"""
    discussions_data = load_discussions()
    
    # 收集所有话题
    all_topics = []
    for page_name, topics in discussions_data.items():
        for topic in topics:
            topic['page_name'] = page_name
            # 获取页面标题
            data = load_data()
            page_title = data['pages'].get(page_name, {}).get('title', page_name)
            topic['page_title'] = page_title
            all_topics.append(topic)
    
    # 按时间倒序排序
    all_topics.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return render_template('recent_discussions.html',
                         topics=all_topics[:50],  # 只显示最近50条
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))

@app.route('/hot-discussions')
def hot_discussions():
    """热门讨论 - 按回复数和点赞数排序"""
    discussions_data = load_discussions()
    
    # 收集所有话题
    all_topics = []
    for page_name, topics in discussions_data.items():
        for topic in topics:
            topic['page_name'] = page_name
            data = load_data()
            page_title = data['pages'].get(page_name, {}).get('title', page_name)
            topic['page_title'] = page_title
            # 计算热度 = 点赞数 + 回复数 * 2 + 浏览量 * 0.5
            topic['hot_score'] = (topic.get('likes', 0) + 
                                  topic.get('reply_count', 0) * 2 + 
                                  topic.get('views', 0) * 0.5)
            all_topics.append(topic)
    
    # 按热度排序
    all_topics.sort(key=lambda x: x.get('hot_score', 0), reverse=True)
    
    return render_template('hot_discussions.html',
                         topics=all_topics[:50],
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))

@app.route('/my-discussions')
@login_required
def my_discussions():
    """我的讨论 - 用户参与的话题"""
    discussions_data = load_discussions()
    username = session['username']
    
    my_topics = []
    for page_name, topics in discussions_data.items():
        for topic in topics:
            # 我发起的话题
            if topic['author'] == username:
                topic['page_name'] = page_name
                data = load_data()
                page_title = data['pages'].get(page_name, {}).get('title', page_name)
                topic['page_title'] = page_title
                topic['my_role'] = 'author'
                my_topics.append(topic)
            # 我回复过的话题
            for reply in topic.get('replies', []):
                if reply['author'] == username:
                    # 避免重复添加
                    if not any(t.get('id') == topic['id'] for t in my_topics):
                        topic_copy = topic.copy()
                        topic_copy['page_name'] = page_name
                        data = load_data()
                        page_title = data['pages'].get(page_name, {}).get('title', page_name)
                        topic_copy['page_title'] = page_title
                        topic_copy['my_role'] = 'replied'
                        my_topics.append(topic_copy)
                    break
    
    my_topics.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return render_template('my_discussions.html',
                         topics=my_topics,
                         username=username,
                         user_avatar=session.get('avatar'))

@app.route('/api/all-discussions')
def api_all_discussions():
    """获取所有讨论（用于最新讨论页面）"""
    discussions_data = load_discussions()
    data = load_data()
    
    all_topics = []
    for page_name, topics in discussions_data.items():
        page_title = data['pages'].get(page_name, {}).get('title', page_name)
        for topic in topics:
            topic['page_name'] = page_name
            topic['page_title'] = page_title
            all_topics.append(topic)
    
    all_topics.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return jsonify(all_topics)

@app.route('/api/hot-discussions-full')
def api_hot_discussions_full():
    """获取热门讨论完整数据"""
    discussions_data = load_discussions()
    data = load_data()
    
    all_topics = []
    for page_name, topics in discussions_data.items():
        page_title = data['pages'].get(page_name, {}).get('title', page_name)
        for topic in topics:
            topic['page_name'] = page_name
            topic['page_title'] = page_title
            # 热度计算：点赞 + 回复数*3 + 浏览量*0.3
            topic['hot_score'] = (topic.get('likes', 0) + 
                                  topic.get('reply_count', 0) * 3 + 
                                  topic.get('views', 0) * 0.3)
            all_topics.append(topic)
    
    all_topics.sort(key=lambda x: x.get('hot_score', 0), reverse=True)
    return jsonify(all_topics[:50])

@app.route('/api/discussions-stats')
def api_discussions_stats():
    """获取讨论区统计数据"""
    discussions_data = load_discussions()
    data = load_data()
    
    total_topics = 0
    total_replies = 0
    participants = set()
    today_active = 0
    today = datetime.now().strftime("%Y-%m-%d")
    
    for page_name, topics in discussions_data.items():
        for topic in topics:
            total_topics += 1
            total_replies += topic.get('reply_count', 0)
            participants.add(topic['author'])
            for reply in topic.get('replies', []):
                participants.add(reply['author'])
                if reply.get('created_at', '').startswith(today):
                    today_active += 1
            if topic.get('created_at', '').startswith(today):
                today_active += 1
    
    return jsonify({
        'total_topics': total_topics,
        'total_replies': total_replies,
        'total_participants': len(participants),
        'today_active': today_active
    })

@app.route('/api/my-discussions')
@login_required
def api_my_discussions():
    """获取当前用户的讨论"""
    discussions_data = load_discussions()
    data = load_data()
    username = session['username']
    
    my_topics = []
    for page_name, topics in discussions_data.items():
        page_title = data['pages'].get(page_name, {}).get('title', page_name)
        for topic in topics:
            if topic['author'] == username:
                topic_copy = topic.copy()
                topic_copy['page_name'] = page_name
                topic_copy['page_title'] = page_title
                topic_copy['my_role'] = 'author'
                my_topics.append(topic_copy)
            else:
                for reply in topic.get('replies', []):
                    if reply['author'] == username:
                        topic_copy = topic.copy()
                        topic_copy['page_name'] = page_name
                        topic_copy['page_title'] = page_title
                        topic_copy['my_role'] = 'replied'
                        my_topics.append(topic_copy)
                        break
    
    # 去重（如果既是作者又是回复者，只显示为作者）
    seen_ids = set()
    unique_topics = []
    for topic in my_topics:
        if topic['id'] not in seen_ids:
            seen_ids.add(topic['id'])
            unique_topics.append(topic)
    
    unique_topics.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    stats = {
        'total': len([t for t in unique_topics if t['my_role'] == 'author']),
        'replies': len([t for t in unique_topics if t['my_role'] == 'replied'])
    }
    
    return jsonify({'topics': unique_topics, 'stats': stats})

@app.route('/api/my-discussions-full')
@login_required
def api_my_discussions_full():
    """获取当前用户的完整讨论数据"""
    discussions_data = load_discussions()
    data = load_data()
    username = session['username']
    
    # 收集所有参与的话题
    topic_map = {}
    
    for page_name, topics in discussions_data.items():
        page_title = data['pages'].get(page_name, {}).get('title', page_name)
        for topic in topics:
            # 我发起的话题
            if topic['author'] == username:
                topic_copy = topic.copy()
                topic_copy['page_name'] = page_name
                topic_copy['page_title'] = page_title
                topic_copy['my_role'] = 'author'
                topic_map[topic['id']] = topic_copy
            
            # 我回复过的话题
            for reply in topic.get('replies', []):
                if reply['author'] == username:
                    if topic['id'] not in topic_map:
                        topic_copy = topic.copy()
                        topic_copy['page_name'] = page_name
                        topic_copy['page_title'] = page_title
                        topic_copy['my_role'] = 'replied'
                        topic_copy['my_reply'] = reply
                        topic_map[topic['id']] = topic_copy
    
    # 转换为列表并排序
    my_topics = list(topic_map.values())
    my_topics.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    # 统计信息
    stats = {
        'authored': len([t for t in my_topics if t['my_role'] == 'author']),
        'replied': len([t for t in my_topics if t['my_role'] == 'replied']),
        'totalLikes': sum(t.get('likes', 0) for t in my_topics),
        'rank': 0  # 可以后续实现排名计算
    }
    
    return jsonify({'topics': my_topics, 'stats': stats})


@app.route('/profile')
@login_required
def profile():
    """个人中心主页"""
    username = session['username']
    data = load_data()
    discussions_data = load_discussions()
    
    # 用户资料
    user_data = data['users'].get(username, {})
    
    # 统计用户创建的页面
    user_pages = []
    for name, page in data['pages'].items():
        if page.get('author') == username:
            user_pages.append({
                'name': name,
                'title': page.get('title', name),
                'views': page.get('views', 0),
                'last_edit': page.get('last_edit', '')
            })
    
    # 统计用户发起的话题和回复
    topics_count = 0
    replies_count = 0
    total_likes = 0
    
    for page_name, topics in discussions_data.items():
        for topic in topics:
            if topic.get('author') == username:
                topics_count += 1
                total_likes += topic.get('likes', 0)
            for reply in topic.get('replies', []):
                if reply.get('author') == username:
                    replies_count += 1
                    total_likes += reply.get('likes', 0)
    
    # 用户常用标签
    tag_counts = {}
    for page in user_pages:
        page_data = data['pages'].get(page['name'], {})
        for tag in page_data.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    favorite_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # 贡献日历数据
    contributions = {}
    for page in user_pages:
        date = page.get('last_edit', '')[:10]
        if date:
            contributions[date] = contributions.get(date, 0) + 1
    
    # 最近活动（结合页面编辑和讨论）
    recent_activities = []
    
    # 添加页面编辑活动
    for page in sorted(user_pages, key=lambda x: x.get('last_edit', ''), reverse=True)[:5]:
        recent_activities.append({
            'icon': 'fa-file-alt',
            'page_name': page['title'],
            'page_url': f"/page/{page['name']}",
            'description': f'编辑了页面「{page["title"]}」',
            'time_ago': format_time_ago(page.get('last_edit', ''))
        })
    
    # 添加讨论活动
    for page_name, topics in discussions_data.items():
        page_title = data['pages'].get(page_name, {}).get('title', page_name)
        for topic in topics:
            if topic.get('author') == username:
                recent_activities.append({
                    'icon': 'fa-comments',
                    'page_name': topic['title'],
                    'page_url': f"/discussions/{page_name}#topic-{topic['id']}",
                    'description': f'发起了话题「{topic["title"]}」',
                    'time_ago': format_time_ago(topic.get('created_at', ''))
                })
            for reply in topic.get('replies', []):
                if reply.get('author') == username:
                    recent_activities.append({
                        'icon': 'fa-reply',
                        'page_name': topic['title'],
                        'page_url': f"/discussions/{page_name}#topic-{topic['id']}",
                        'description': f'回复了话题「{topic["title"]}」',
                        'time_ago': format_time_ago(reply.get('created_at', ''))
                    })
    
    # 排序并去重
    recent_activities.sort(key=lambda x: x.get('time_ago', ''), reverse=False)
    recent_activities = recent_activities[:10]
    
    # 计算贡献等级
    total_contributions = len(user_pages) + topics_count + replies_count
    level = min(10, max(1, total_contributions // 10 + 1))
    
    stats = {
        'pages_created': len(user_pages),
        'topics_count': topics_count,
        'replies_count': replies_count,
        'total_likes': total_likes,
        'last_active': format_time_ago(datetime.now().strftime("%Y-%m-%d %H:%M")),
        'level': level,
        'achievement_points': total_contributions,
        'contributions_total': total_contributions
    }
    
    return render_template('profile.html',
                         username=username,
                         user_avatar=session.get('avatar', username[0].upper()),
                         profile_data={
                             'real_name': user_data.get('real_name', ''),
                             'bio': user_data.get('bio', ''),
                             'location': user_data.get('location', ''),
                             'website': user_data.get('website', ''),
                             'join_date': user_data.get('join_date', datetime.now().strftime("%Y-%m-%d"))
                         },
                         email=user_data.get('email', ''),
                         stats=stats,
                         favorite_tags=[{'name': k, 'count': v} for k, v in favorite_tags],
                         contributions_data=contributions,
                         recent_activities=recent_activities,
                         created_pages=user_pages,
                         is_own_profile=True)

def format_time_ago(date_str):
    """格式化时间为相对时间"""
    if not date_str:
        return '刚刚'
    try:
        date = datetime.strptime(date_str[:10], "%Y-%m-%d")
        now = datetime.now()
        diff = (now - date).days
        if diff == 0:
            return '今天'
        elif diff == 1:
            return '昨天'
        elif diff < 7:
            return f'{diff}天前'
        elif diff < 30:
            return f'{diff // 7}周前'
        else:
            return f'{diff // 30}个月前'
    except:
        return date_str

@app.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    """编辑个人资料"""
    username = session['username']
    data = load_data()
    
    if 'users' not in data:
        data['users'] = {}
    if username not in data['users']:
        data['users'][username] = {}
    
    data['users'][username]['real_name'] = request.form.get('real_name', '')
    data['users'][username]['bio'] = request.form.get('bio', '')
    data['users'][username]['location'] = request.form.get('location', '')
    data['users'][username]['website'] = request.form.get('website', '')
    
    if request.form.get('email'):
        data['users'][username]['email'] = request.form.get('email')
    
    save_data(data)
    return redirect(url_for('profile'))


@app.errorhandler(404)
def page_not_found(e):
    """自定义404页面"""
    # 获取请求的路径
    path = request.path
    page_name = path.split('/')[-1] if '/page/' in path else path
    
    # 获取可能的建议（模糊匹配）
    data = load_data()
    suggestions = []
    if page_name and page_name != '/':
        for name in data['pages'].keys():
            if page_name.lower() in name.lower() or name.lower() in page_name.lower():
                suggestions.append(name)
    
    return render_template('404.html', 
                         page_name=page_name,
                         suggestions=suggestions[:5],
                         username=session.get('username'),
                         user_avatar=session.get('avatar')), 404

# ==================== 启动服务器 ====================

if __name__ == '__main__':
    init_data()
    print("=" * 50)
    print("🍌 寰宇维基 本地服务器已启动!")
    print("📖 访问地址: http://localhost:5000")
    print("👤 测试账号: admin / admin123")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)
