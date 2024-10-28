// login_success.js

const urlParams = new URLSearchParams(window.location.search);
const accessToken = urlParams.get('access');
const refreshToken = urlParams.get('refresh');

if (accessToken && refreshToken) {
    sessionStorage.setItem('access_token', accessToken);
    sessionStorage.setItem('refresh_token', refreshToken);
    window.location.href = "/lobby/";
} else {
    window.location.href = "/";
}