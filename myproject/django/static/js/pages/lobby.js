// lobby.js

export function renderLobbyPage() {
    console.log("Rendering Lobby Page...");

    const app = document.getElementById('app');

    // 기존 콘텐츠 삭제
    app.innerHTML = '';

    // 헤더와 네비게이션 생성 (home.js와 동일)
    const header = document.createElement('header');
    const nav = document.createElement('nav');
    nav.innerHTML = `
        <a href="/" data-link>Home</a> |
        <a href="/about" data-link>About</a> |
        <a href="/lobby" data-link>Lobby</a>
    `;
    header.appendChild(nav);

    // 제목 및 콘텐츠 생성
    const title = document.createElement('h1');
    title.textContent = 'Lobby Page';

    const content = document.createElement('p');
    content.textContent = '이것은 SPA의 Lobby 페이지입니다.';

    // 요소 추가
    app.appendChild(header);
    app.appendChild(title);
    app.appendChild(content);
}
