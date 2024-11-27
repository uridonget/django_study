import { createHeader } from '../utils.js';

export function renderHomePage() {
    console.log("Rendering Home Page...");

    const app = document.getElementById('app');
    app.innerHTML = '';

    // const header = createHeader();
    // app.appendChild(header);

    const title = document.createElement('h1');
    title.textContent = 'Home Page';

    const content = document.createElement('p');
    content.textContent = '토큰이 유효하지 않으면 이 페이지에 오게 됩니다.';

    app.appendChild(title);
    app.appendChild(content);
}
