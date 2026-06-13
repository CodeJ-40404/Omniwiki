// static/script.js - 前端交互
// 搜索自动补全
// ==================== 搜索功能 ====================
const searchInput = document.getElementById('globalSearchInput');
const searchButton = document.getElementById('searchButton');
const searchSuggestions = document.getElementById('searchSuggestions');

// HTML 转义函数
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

if (searchInput) {
    let debounceTimer;

    // 搜索建议（自动补全）
    searchInput.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        if (query.length < 1) {
            if (searchSuggestions) searchSuggestions.style.display = 'none';
            return;
        }

        debounceTimer = setTimeout(async () => {
            try {
                console.log('搜索:', query); // 调试用
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                console.log('搜索结果:', data); // 调试用

                if (searchSuggestions) {
                    if (data.length > 0) {
                        searchSuggestions.innerHTML = data.map(item => `
                            <div class="suggestion-item" data-page="${escapeHtml(item.name)}">
                                <div class="suggestion-title">${escapeHtml(item.title)}</div>
                                <div class="suggestion-name">${escapeHtml(item.name)}</div>
                            </div>
                        `).join('');
                        searchSuggestions.style.display = 'block';

                        // 绑定点击事件
                        document.querySelectorAll('.suggestion-item').forEach(el => {
                            el.addEventListener('click', () => {
                                window.location.href = `/page/${encodeURIComponent(el.dataset.page)}`;
                            });
                        });
                    } else {
                        // 显示"创建新页面"建议
                        searchSuggestions.innerHTML = `
                            <div class="suggestion-item" data-query="${escapeHtml(query)}">
                                <div class="suggestion-title">
                                    <i class="fas fa-plus-circle"></i> 创建页面 "${escapeHtml(query)}"
                                </div>
                                <div class="suggestion-name">未找到相关页面，点击创建</div>
                            </div>
                        `;
                        searchSuggestions.style.display = 'block';

                        document.querySelector('.suggestion-item')?.addEventListener('click', () => {
                            window.location.href = `/create?prefill_name=${encodeURIComponent(query)}`;
                        });
                    }
                }
            } catch (error) {
                console.error('搜索建议失败:', error);
            }
        }, 300);
    });

    // 点击其他地方关闭建议框
    document.addEventListener('click', function (e) {
        if (searchSuggestions && !searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
            searchSuggestions.style.display = 'none';
        }
    });

    // 回车搜索
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
                window.location.href = `/search?q=${encodeURIComponent(query)}`;
            }
        }
    });
}

// 搜索按钮点击
if (searchButton) {
    searchButton.addEventListener('click', () => {
        const query = searchInput ? searchInput.value.trim() : '';
        if (query) {
            window.location.href = `/search?q=${encodeURIComponent(query)}`;
        }
    });
}

// 用户下拉菜单（如果存在）
const userMenuBtn = document.getElementById('userMenuBtn');
const userDropdown = document.getElementById('userDropdown');
if (userMenuBtn && userDropdown) {
    userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('show');
    });
    document.addEventListener('click', () => {
        userDropdown.classList.remove('show');
    });
}

console.log('script.js 已加载'); // 调试用