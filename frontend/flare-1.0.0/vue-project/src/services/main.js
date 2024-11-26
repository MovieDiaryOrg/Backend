import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// 메인 페이지 호출
const MainPage = async () => {
    try{
        const response = await axios.get(`${API_BASE_URL}/`);
        const data = response?.data ?? { featuredFilm: null, reviews: [] }; // 적절한 기본값 설정
        console.log('data = ', data)
        return data;
    } catch (err){
        console.error("메인 페이지 로딩 중 오류 발생: ", err)
        throw err;
    }
};

export default MainPage;