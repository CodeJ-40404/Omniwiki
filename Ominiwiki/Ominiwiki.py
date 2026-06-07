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

@app.route('/search')
def search_page():
    """搜索页面"""
    query = request.args.get('q', '').strip()
    data = load_data()
    
    if not query:
        return redirect(url_for('index'))
    
    results = []
    for name, page in data['pages'].items():
        score = 0
        if query.lower() in name.lower():
            score += 10
        if query.lower() in page['title'].lower():
            score += 5
        if query.lower() in page['content'].lower():
            score += 1
        if score > 0:
            results.append({
                'name': name,
                'title': page['title'],
                'excerpt': page['content'][:200].replace('\n', ' '),
                'score': score
            })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return render_template('search.html',
                         query=query,
                         results=results,
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))

@app.route('/api/search')
def api_search():
    """搜索API（用于前端自动补全）"""
    query = request.args.get('q', '').lower()
    data = load_data()
    results = [{'name': p, 'title': data['pages'][p]['title']} 
               for p in data['pages'].keys() if query in p.lower()]
    return jsonify(results[:10])

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

@app.route('/profile')
@login_required
def profile():
    """用户个人页面"""
    data = load_data()
    user_data = data['users'].get(session['username'], {})
    
    # 获取用户贡献的页面
    user_pages = []
    for name, page in data['pages'].items():
        if page.get('author') == session['username']:
            user_pages.append({'name': name, 'title': page['title'], 'last_edit': page.get('last_edit')})
    
    return render_template('profile.html',
                         user_data=user_data,
                         user_pages=user_pages,
                         username=session.get('username'),
                         user_avatar=session.get('avatar'))

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

# ==================== 新增：页面分类和标签云 ====================

@app.route('/tags')
def tags_page():
    """标签云页面"""
    data = load_data()
    tag_counts = {}
    for page in data['pages'].values():
        for tag in page.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    tags_sorted = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    return render_template('tags.html', tags=tags_sorted, username=session.get('username'))

@app.route('/tag/<tag_name>')
def tag_pages(tag_name):
    """按标签查看页面"""
    data = load_data()
    pages_with_tag = []
    for name, page in data['pages'].items():
        if tag_name in page.get('tags', []):
            pages_with_tag.append({'name': name, 'page': page})
    
    return render_template('tag_pages.html', tag=tag_name, pages=pages_with_tag, username=session.get('username'))


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

# ==================== 启动服务器 ====================

if __name__ == '__main__':
    init_data()
    print("=" * 50)
    print("🍌 寰宇维基 本地服务器已启动!")
    print("📖 访问地址: http://localhost:5000")
    print("👤 测试账号: admin / admin123")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)
