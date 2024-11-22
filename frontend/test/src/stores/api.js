import axios from "axios";
import router from "../router";

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: "http://localhost:8000", // API 기본 URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Refresh Token을 사용해 Access Token 갱신
export const refreshAccessToken = async () => {
  try {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
      throw new Error("No refresh token found");
    }

    const response = await axios.post("/dj-rest-auth/token/refresh/", {
      refresh: refreshToken,
    });

    const newAccessToken = response.data.access;
    localStorage.setItem("access_token", newAccessToken);

    // Axios 기본 헤더 업데이트
    apiClient.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${newAccessToken}`;

    return newAccessToken;
  } catch (error) {
    console.error("Failed to refresh token:", error.response?.data || error.message);
    throw error;
  }
};

// Axios 인터셉터 추가
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const newAccessToken = await refreshAccessToken();

        // 원래 요청에 새 토큰 설정
        originalRequest.headers[
          "Authorization"
        ] = `Bearer ${newAccessToken}`;
        return apiClient(originalRequest); // 원래 요청 재시도
      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
        router.push("/login"); // 로그인 페이지로 리다이렉트
      }
    }

    return Promise.reject(error);
  }
);

// API 요청 메서드
export const login = async (credentials) => {
  const response = await apiClient.post("/dj-rest-auth/login/", credentials);
  return response.data;
};

export const signUp = async (userData) => {
  const response = await apiClient.post("/dj-rest-auth/registration/", userData);
  return response.data;
};

export default apiClient;
