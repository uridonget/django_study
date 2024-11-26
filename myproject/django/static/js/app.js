// app.js
import { renderHomePage } from './pages/home.js';
import { navigateTo } from './navigation.js';
import { loadContent } from './content.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log("App initialized!");

    // Home 페이지 렌더링
    renderHomePage();

    // 이벤트 위임을 통한 네비게이션 이벤트 처리
    document.body.addEventListener('click', (event) => {
        if (event.target.matches('a[data-link]')) {
            event.preventDefault();
            const path = event.target.getAttribute('href');
            navigateTo(path);
            loadContent(path);
        }
    });

    // 브라우저 뒤로가기/앞으로가기 버튼 처리
    window.addEventListener('popstate', () => {
        loadContent(window.location.pathname);
    });

    // 초기 콘텐츠 로드
    loadContent(window.location.pathname);
});
