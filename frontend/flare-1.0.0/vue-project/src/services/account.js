import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/accounts'

// 로그인
export const login = async (username, password) => {
  const response = await axios.post(`${API_BASE_URL}/dj-rest-auth/login/`, {
    username,
    password,
  })
  return {
    access: response.data.access,
    user: response.data.user,
  }
}

// 로그아웃
export const logout = async () => {
  const response = await axios.post(`${API_BASE_URL}/dj-rest-auth/logout/`)
  return response.data
}

// 회원가입
export const signup = async (formData) => {
  const response = await axios.post(`${API_BASE_URL}/dj-rest-auth/registration/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

// 회원정보 수정
export const updateProfile = async (formData) => {
  const token = localStorage.getItem('access_token') // 토큰 가져오기
  if (!token) throw new Error('로그인이 필요합니다.')

  const response = await axios.patch(`${API_BASE_URL}/dj-rest-auth/user/`, formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data', // 파일 업로드를 위해 Content-Type 설정
    },
  })

  return response.data
}

// 현재 로그인한 사용자 정보 가져오기
export const getProfile = async () => {
  const token = localStorage.getItem('access_token') // 토큰 가져오기
  if (!token) throw new Error('로그인이 필요합니다.')

  const response = await axios.get(`${API_BASE_URL}/dj-rest-auth/user/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return response.data
}

// 사용자 정보 Fetch
export const fetchUserInfo = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) throw new Error('로그인이 필요합니다.');

  try {
    const response = await axios.get(`${API_BASE_URL}/user/info/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data; // 사용자 정보를 반환
  } catch (error) {
    console.error('사용자 정보 가져오기 실패:', error);
    throw error;
  }
};



// 회원 탈퇴
export const deleteAccountAPI = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('로그인이 필요합니다.');
  }

  await axios.delete(`${API_BASE_URL}/user/delete/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};