// static/script.js - 前端交互
// 搜索自动补全
const searchInput = document.getElementById('globalSearchInput');
const searchSuggestions = document.getElementById('searchSuggestions');

if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const query = this.value.trim();
        if (query.length < 2) {
            searchSuggestions.style.display = 'none';
            return;
        }
        debounceTimer = setTimeout(() => {
            fetch(`/api/search?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    if (data.length > 0) {
                        searchSuggestions.innerHTML = data.map(item =>
                            `<div class="suggestion-item" data-page="${item.name}">🔍 ${item.name} - ${item.title}</div>`
                        ).join('');
                        searchSuggestions.style.display = 'block';
                        document.querySelectorAll('.suggestion-item').forEach(el => {
                            el.addEventListener('click', () => {
                                window.location.href = `/page/${el.dataset.page}`;
                            });
                        });
                    } else {
                        searchSuggestions.style.display = 'none';
                    }
                });
        }, 300);
    });

    document.addEventListener('click', function (e) {
        if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
            searchSuggestions.style.display = 'none';
        }
    });
}

// 搜索按钮
const searchBtn = document.getElementById('searchButton');
if (searchBtn) {
    searchBtn.addEventListener('click', () => {
        const query = searchInput.value.trim();
        if (query) {
            window.location.href = `/search?q=${encodeURIComponent(query)}`;
        }
    });
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });
}

// 用户下拉菜单
const userMenuBtn = document.getElementById('userMenuBtn');
const userDropdown = document.getElementById('userDropdown');
if (userMenuBtn) {
    userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('show');
    });
    document.addEventListener('click', () => {
        userDropdown.classList.remove('show');
    });
}

// 热门页面加载（右侧边栏）
function loadHotPages() {
    fetch('/api/search?q=')
        .then(res => res.json())
        .catch(() => []);
}

// 统计信息加载（可通过API扩展）
// 页面渲染完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    // 可以在这里添加额外的初始化逻辑
});