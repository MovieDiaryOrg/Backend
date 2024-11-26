import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// 영화 등록 API 호출
export const addMovieDiary = async (movieData) => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) throw new Error('토큰이 없습니다. 로그인 상태를 확인하세요.');

    console.log('Authorization 헤더:', `Bearer ${token}`);

    const response = await axios.post(`${API_BASE_URL}/movieDiary/`, movieData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    console.log('등록된 영화:', response.data);
    return response.data; // 등록된 영화 데이터 반환
  } catch (error) {
    console.error('영화 등록 중 오류 발생:', error);
    throw error;
  }
};

// 등록된 영화 상세 조회
export const fetchMovieDetail = async (id) => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) throw new Error('토큰이 없습니다. 로그인 상태를 확인하세요.');

    const response = await axios.get(`${API_BASE_URL}/movieDiary/${id}/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    console.log('영화 상세 조회:', response.data);
    return response.data;
  } catch (error) {
    console.error('영화 상세 조회 중 오류 발생:', error);
    throw error;
  }
};

// 사용자 다이어리 영화 리스트 조회
export const fetchUserMovies = async (user_pk = null) => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) throw new Error('토큰이 없습니다. 로그인 상태를 확인하세요.');

    // user_pk가 존재하면 해당 유저의 다이어리 URL로, 없으면 본인의 다이어리 URL로 요청
    const url = user_pk 
      ? `${API_BASE_URL}/movieDiary/${user_pk}/list/`
      : `${API_BASE_URL}/movieDiary/list/`;

    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    console.log('사용자 영화 리스트:', response.data);
    return response.data;
  } catch (error) {
    console.error('영화 리스트 조회 중 오류 발생:', error);
    throw error;
  }
};
