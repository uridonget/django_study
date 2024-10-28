// validateToken.js

const accessToken = sessionStorage.getItem('access_token');
const refreshToken = sessionStorage.getItem('refresh_token');

// 토큰이 세션 스토리지에 존재하는 경우에만 검증 요청을 보냄
if (accessToken && refreshToken) {
    console.log("there is accessToken and refreshToken in session storage");
    
    // JWT 검증 API로 요청 보내기
    fetch('/api/validate-token/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`, // Authorization 헤더에 Bearer 토큰 포함
            'Content-Type': 'application/json'
        },
        // body: JSON.stringify({ token: accessToken })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server response was not OK.');
        }
        return response.json();
    })
    .then(data => {
        if (data.valid) {
            fetch('/lobby/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`, // Authorization 헤더에 Bearer 토큰 포함
                    'Content-Type': 'application/json'
                }
            })
            // window.location.href = "/lobby/";
            // 로비창으로 이동을 하면서 request를 들고가고싶다.
        } else {
            sessionStorage.removeItem('access_token');
            sessionStorage.removeItem('refresh_token');
        }
    })
    .catch(error => {
        console.error('Error during token validation:', error);
        sessionStorage.removeItem('access_token');
        sessionStorage.removeItem('refresh_token');
    });
} else {
    console.log('No tokens found in session storage.');
}