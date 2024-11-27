// checkAuth.js

export function isLoggedIn() {
    const token = sessionStorage.getItem('access_token'); // Access Token 가져오기
    if (token) {
        // console.log('User is logged in.');
        alert('User is logged in.');
        return true;
    } else {
        // console.log('User is not logged in.');
        alert('User is not logged in.');
        return false;
    }
}

export function redirectToLogin() {
    // OAuth 로그인 페이지로 리다이렉트
    const loginUrl = '/api/auth/login'; // Django에서 OAuth 엔드포인트 설정
    window.location.href = loginUrl;
}
