// navigation.js

export function navigateTo(path) {
    console.log(`Navigating to ${path}`);
    window.history.pushState(null, null, path);
}
