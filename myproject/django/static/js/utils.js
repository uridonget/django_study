// utils.js
export function logMessage(message) {
    console.log(`[Utils] ${message}`);
}

export function createHeader() {
    const header = document.createElement('header');
    const nav = document.createElement('nav');

    const navLinks = [
        { href: '/', text: 'Home' },
        { href: '/lobby', text: 'Lobby' },
    ];

    navLinks.forEach((link, index) => {
        const a = document.createElement('a');
        a.href = link.href;
        a.textContent = link.text;
        a.setAttribute('data-link', '');
        nav.appendChild(a);

        if (index < navLinks.length - 1) {
            nav.appendChild(document.createTextNode(' | '));
        }
    });

    header.appendChild(nav);
    return header;
}

export function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.type = 'module'; // ES6 모듈 지원 시 사용
        script.onload = () => resolve(`Script ${src} loaded.`);
        script.onerror = () => reject(new Error(`Failed to load script ${src}`));
        document.head.appendChild(script);
    });
}
