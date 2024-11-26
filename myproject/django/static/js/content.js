// content.js
import { getHomeContent } from './pages/home.js';
import { getAboutContent } from './pages/about.js';
import { getContactContent } from './pages/contact.js';

export function loadContent(path) {
    console.log(`Loading content for ${path}`);

    const content = document.querySelector('main') || createMainContent();
    content.innerHTML = ''; // 기존 콘텐츠 초기화

    // URL에 따른 동적 콘텐츠 로드
    if (path === '/about') {
        content.innerHTML = getAboutContent();
    } else if (path === '/contact') {
        content.innerHTML = getContactContent();
    } else {
        content.innerHTML = getHomeContent();
    }
}

function createMainContent() {
    const main = document.createElement('main');
    document.body.appendChild(main);
    return main;
}
