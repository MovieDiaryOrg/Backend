import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const addComment = async (journal_pk, content) => {
  const token = localStorage.getItem('access_token');
  if (!token) throw new Error('로그인이 필요합니다.');

  const response = await axios.post(
    `${API_BASE_URL}/movieDiary/${journal_pk}/comment/`, // journal_pk를 URL에 포함
    { content }, // 요청 본문에 content 추가
    {
      headers: {
        Authorization: `Bearer ${token}`, // 인증 토큰 헤더에 포함
      },
    }
  );

  return response.data; // 추가된 댓글 데이터를 반환
};