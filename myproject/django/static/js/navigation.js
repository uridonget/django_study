// navigation.js

// window.history.pushState를 사용하여 페이지 새로고침 없이 URL을 변경.

export function navigateTo(path) {
    console.log(`Navigating to ${path}`);
    window.history.pushState(null, null, path);
}
