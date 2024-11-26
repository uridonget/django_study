// app.js
import { navigateTo } from './navigation.js';
import { loadContent } from './content.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log("App initialized!");

    // 네비게이션 이벤트
    document.body.addEventListener('click', (event) => {
        if (event.target.matches('[data-link]')) {
            event.preventDefault();
            const path = event.target.getAttribute('href');
            navigateTo(path); // URL 변경
            loadContent(path); // 현재 브라우저의 URL에 따라 적합한 콘텐츠를 동적으로 로드.
        }
    });

    // 초기 콘텐츠 로드
    loadContent(window.location.pathname);
});
