// app.js
import { navigateTo } from './navigation.js';
import { isLoggedIn } from './auth/checkAuth.js';
import { loadScript } from './utils.js';
import { renderHomePage } from './pages/home.js';
import { renderLobbyPage } from './pages/lobby.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log("App initialized!");

    // 초기 콘텐츠 로드
    initializeApp();

    // 이벤트 위임을 통한 네비게이션 이벤트 처리
    document.body.addEventListener('click', (event) => {
        if (event.target.matches('a[data-link]')) {
            event.preventDefault();
            const path = event.target.getAttribute('href');
            navigateTo(path);
            loadPageScript(path);
        }
    });

    // 브라우저 뒤로가기/앞으로가기 버튼 처리
    window.addEventListener('popstate', () => {
        loadPageScript(window.location.pathname);
    });
});

// 초기화 함수
async function initializeApp() {
    const path = window.location.pathname;

    // 인증 상태 확인
    if (!isLoggedIn()) {
        console.log("User not logged in. Redirecting to /lobby...");
        navigateTo('/');
        await loadPageScript('/home'); // Lobby 페이지 동적 로드
    } else {
        console.log("User logged in. Loading content...");
        navigateTo('/lobby')
        await loadPageScript('/lobby'); // 현재 경로에 맞는 페이지 동적 로드
    }
}

// 페이지 스크립트 동적 로드
async function loadPageScript(path) {
    try {
        if (path === '/lobby') {
            await loadScript('/static/js/pages/lobby.js');
            // 여기에 await loadScript 함수를 통해서 js 파일을 미리 로드할 수 있다.
            renderLobbyPage(); // lobby.js에 정의된 함수
        } else {
            await loadScript('/static/js/pages/home.js');
            renderHomePage(); // home.js에 정의된 함수
        }
    } catch (error) {
        console.error(`Failed to load script for path: ${path}`, error);
    }
}
