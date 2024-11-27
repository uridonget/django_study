// content.js
import { renderHomePage } from './pages/home.js';
import { renderLobbyPage } from './pages/lobby.js';

export function loadContent(path) {
    console.log(`Loading content for ${path}`);

    if (path === '/') {
        renderHomePage();
    } else if (path === '/lobby') {
        renderLobbyPage();
    } else {
        renderNotFoundPage();
    }
}

// 404 페이지 렌더링
function renderNotFoundPage() {
    const app = document.getElementById('app');
    app.innerHTML = '<h1>404 - 페이지를 찾을 수 없습니다.</h1>';
}
