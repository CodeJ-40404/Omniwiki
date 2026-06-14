/* ========== static/script.js - 寰宇维基完整脚本 ========== */

// ============================================================
// 1. 主题切换系统
// ============================================================
(function () {
    const savedTheme = localStorage.getItem('wiki-theme') || 'dark';
    const html = document.documentElement;

    function applyTheme(theme) {
        if (theme === 'light') {
            html.setAttribute('data-theme', 'light');
            localStorage.setItem('wiki-theme', 'light');
        } else {
            html.removeAttribute('data-theme');
            localStorage.setItem('wiki-theme', 'dark');
        }
        updateToggleButton(theme);
        // 触发主题变化事件
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: theme } }));
    }

    function updateToggleButton(theme) {
        const btn = document.getElementById('themeToggle');
        if (!btn) return;
        const isLight = theme === 'light' || html.getAttribute('data-theme') === 'light';
        if (isLight) {
            btn.innerHTML = '<i class="fas fa-sun sun-icon"></i>';
        } else {
            btn.innerHTML = '<i class="fas fa-moon moon-icon"></i>';
        }
    }

    window.toggleTheme = function () {
        const current = html.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        const btn = document.getElementById('themeToggle');
        if (btn) {
            btn.classList.add('animating');
            setTimeout(() => btn.classList.remove('animating'), 500);
        }
        applyTheme(next);
    };

    window.getCurrentTheme = function () {
        return html.getAttribute('data-theme') || 'dark';
    };

    // 初始化
    applyTheme(savedTheme);

    document.addEventListener('DOMContentLoaded', function () {
        const btn = document.getElementById('themeToggle');
        if (btn) {
            btn.addEventListener('click', window.toggleTheme);
        }
    });
})();

// ============================================================
// 2. 搜索系统
// ============================================================
(function () {
    const searchInput = document.getElementById('globalSearchInput');
    const searchButton = document.getElementById('searchButton');
    const searchSuggestions = document.getElementById('searchSuggestions');

    if (!searchInput) return;

    let debounceTimer;

    searchInput.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        if (query.length < 1) {
            if (searchSuggestions) searchSuggestions.style.display = 'none';
            return;
        }

        debounceTimer = setTimeout(function () {
            fetch('/api/search?q=' + encodeURIComponent(query))
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (!searchSuggestions) return;
                    if (data.length > 0) {
                        searchSuggestions.innerHTML = data.map(function (item) {
                            return '<div class="suggestion-item" data-page="' + item.name + '">' +
                                '<div class="suggestion-title">' + escapeHtml(item.title) + '</div>' +
                                '<div class="suggestion-name">' + escapeHtml(item.name) + '</div>' +
                                '</div>';
                        }).join('');
                        searchSuggestions.style.display = 'block';

                        document.querySelectorAll('.suggestion-item').forEach(function (el) {
                            el.addEventListener('click', function () {
                                window.location.href = '/page/' + encodeURIComponent(el.dataset.page);
                            });
                        });
                    } else {
                        searchSuggestions.innerHTML = '';
                        searchSuggestions.style.display = 'none';
                    }
                })
                .catch(function () {
                    if (searchSuggestions) searchSuggestions.style.display = 'none';
                });
        }, 300);
    });

    document.addEventListener('click', function (e) {
        if (searchSuggestions && !searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
            searchSuggestions.style.display = 'none';
        }
    });

    searchInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch();
        }
    });

    if (searchButton) {
        searchButton.addEventListener('click', performSearch);
    }

    function performSearch() {
        const query = searchInput.value.trim();
        if (query) {
            window.location.href = '/search?q=' + encodeURIComponent(query);
        }
    }

    function escapeHtml(text) {
        if (!text) return '';
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
})();

// ============================================================
// 3. 用户下拉菜单
// ============================================================
(function () {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');

    if (userMenuBtn) {
        userMenuBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            if (userDropdown) userDropdown.classList.toggle('show');
        });
        document.addEventListener('click', function () {
            if (userDropdown) userDropdown.classList.remove('show');
        });
    }
})();

// ============================================================
// 4. 搜索自动补全（供其它页面使用）
// ============================================================
window.performSearch = function (query) {
    if (query) {
        window.location.href = '/search?q=' + encodeURIComponent(query);
    }
};

window.escapeHtml = function (text) {
    if (!text) return '';
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
};

// ============================================================
// 5. Toast 提示（全局）
// ============================================================
window.showToast = function (message, type) {
    type = type || 'success';
    var toast = document.createElement('div');
    toast.className = 'toast' + (type === 'error' ? ' error' : '');
    toast.innerHTML = '<i class="fas ' + (type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle') + '"></i> ' + message;
    document.body.appendChild(toast);
    setTimeout(function () { toast.remove(); }, 3000);
};

// ============================================================
// 6. 主题切换事件监听（供组件响应）
// ============================================================
document.addEventListener('themeChanged', function (e) {
    // 重新高亮代码块
    document.querySelectorAll('.code-content pre code, .markdown-body pre code').forEach(function (block) {
        if (typeof hljs !== 'undefined' && block) {
            try { hljs.highlightElement(block); } catch (err) { }
        }
    });

    // 重新渲染 KaTeX
    if (typeof renderMathInElement !== 'undefined') {
        var content = document.getElementById('markdownContent') || document.getElementById('previewContent');
        if (content) {
            try {
                renderMathInElement(content, {
                    delimiters: [
                        { left: '$$', right: '$$', display: true },
                        { left: '$', right: '$', display: false },
                        { left: '\\(', right: '\\)', display: false },
                        { left: '\\[', right: '\\]', display: true }
                    ],
                    throwOnError: false
                });
            } catch (err) { }
        }
    }
});

// ============================================================
// 7. 页面加载后初始化
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    // 如果有页面内容，触发一次主题事件确保样式正确
    setTimeout(function () {
        document.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { theme: document.documentElement.getAttribute('data-theme') || 'dark' }
        }));
    }, 100);
});

// ============================================================
// 8. 返回顶部按钮（由各页面独立控制）
// ============================================================
// 返回顶部按钮逻辑在 wiki_page.html 中独立实现

// ============================================================
// 9. 评论系统工具（供评论区使用）
// ============================================================
window.renderMarkdownForComment = function (text) {
    if (!text) return '';
    var html = window.escapeHtml(text);
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');
    html = html.replace(/\n/g, '<br>');
    return html;
};



