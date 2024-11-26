// stores/counter.js
import { defineStore } from 'pinia'
import { login, logout } from '@/services/account'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    isLoggedIn: !!localStorage.getItem('access_token'),
    user: null, // 사용자 정보 저장
    error: null,
    isLoading: false,
  }),
  actions: {
    async login(username, password) {
      try {
        this.isLoading = true
        this.error = null
        const result = await login(username, password)

        // 토큰 저장
        localStorage.setItem('access_token', result.access)
        if (result.refresh) {
          localStorage.setItem('refresh_token', result.refresh)
        }

        this.isLoggedIn = true
        // 사용자 정보 저장
        this.user = {
          username: result.user.username,
          email: result.user.email,
          phone: result.user.phone,
          fullName: `${result.user.last_name}${result.user.first_name}`, // 전체 이름 생성
          profileImage: result.user.profile_image, // 프로필 이미지
        }

        return { success: true, message: '로그인 성공' }
      } catch (error) {
        this.error = error.response?.data?.message || '로그인 실패'
        return { success: false, message: this.error }
      } finally {
        this.isLoading = false
      }
    },
    async logout() {
      try {
        this.isLoading = true

        // 로그아웃 API 호출
        await logout()

        // 토큰 및 상태 초기화
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        this.isLoggedIn = false
        this.user = null

        return { success: true, message: '로그아웃 성공' }
      } catch (error) {
        this.error = error.response?.data?.message || '로그아웃 실패'
        return { success: false, message: this.error }
      } finally {
        this.isLoading = false
      }
    },
    async fetchUser(new_user){
      try {
        this.isLoading = true;
        
        this.user = {
          username: new_user.username,
          email: new_user.email,
          phone: new_user.phone,
          firstName: new_user.first_name,
          secondName: new_user.last_name,
          profileImage: new_user.profile_image, // 프로필 이미지
          fullName : new_user.last_name + new_user.first_name 
        };
        console.log('사용자 정보 갱신 성공:', this.user);
      } catch (error) {
        console.error('오류:', error);
      } finally {
        this.isLoading = false;
      }
    }
  },
})
