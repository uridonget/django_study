import { createHeader } from '../utils.js';

export function renderLobbyPage() {
    console.log("Rendering Lobby Page...");

    const app = document.getElementById('app');
    app.innerHTML = '';

    // const header = createHeader();
    // app.appendChild(header);

    const title = document.createElement('h1');
    title.textContent = 'Lobby Page';

    const content = document.createElement('p');
    content.textContent = '유효한 토큰을 가지고 있으면 이 페이지에 오게 됩니다.';

    app.appendChild(title);
    app.appendChild(content);
}
