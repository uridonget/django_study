// home.js
import { navigateTo } from '../navigation.js';

export function renderHomePage() {
    console.log("Rendering Home Page...");

    const app = document.getElementById('app');

    // 기존 콘텐츠 삭제
    app.innerHTML = '';

    // 헤더 생성
    const header = document.createElement('header');

    // 네비게이션 생성
    const nav = document.createElement('nav');

    // 네비게이션 링크 정의
    const navLinks = [
        { href: '/', text: 'Home' },
        { href: '/about', text: 'About' },
        { href: '/lobby', text: 'Lobby' },
    ];

    // 네비게이션 링크 동적 생성
    navLinks.forEach((link, index) => {
        const a = document.createElement('a');
        a.href = link.href;
        a.textContent = link.text;
        a.setAttribute('data-link', ''); // SPA 라우팅을 위한 속성

        nav.appendChild(a);

        // 링크 사이에 구분자 추가 (마지막 링크 제외)
        if (index < navLinks.length - 1) {
            nav.appendChild(document.createTextNode(' | '));
        }
    });

    header.appendChild(nav);

    // 메인 제목 생성
    const title = document.createElement('h1');
    title.textContent = 'SPA 실습';

    // 요소들을 app에 추가
    app.appendChild(header);
    app.appendChild(title);

    // 스타일 추가 (선택 사항)
    addStyles();
}

// 스타일 추가 함수
function addStyles() {
    const style = document.createElement('style');
    style.textContent = `
        header {
            background-color: #f0f0f0;
            padding: 10px;
        }
        nav a {
            text-decoration: none;
            color: blue;
            margin-right: 5px;
        }
        nav a:hover {
            text-decoration: underline;
        }
        h1 {
            margin-top: 20px;
        }
    `;
    document.head.appendChild(style);
}
