import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCounterStore = defineStore('counter', () => {
  const error = ref(null)
  const isLoading = ref(false)

  const login = async function(loginData){
    try {
      isLoading.value = true
      error.value = null
      
      const response = await axios.post('http://127.0.0.1:8000/accounts/login/', {
        username: loginData.username,
        password: loginData.password,
      })
  
      if (response.status === 200) {
        // JWT 토큰이 있다면 localStorage에 저장
        if (response.data.access) {   // access token
          localStorage.setItem('access_token', response.data.access)
        }
        if (response.data.refresh) {  // refresh token
          localStorage.setItem('refresh_token', response.data.refresh)
        }

        // axios 기본 헤더에 토큰 설정
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`

        return {
          success: true,
          message: '로그인이 완료되었습니다.'
        }
      }
    } catch (err) {
      console.log('Error response: ', err.response)       // 에러 확인용 출력
      error.value = err.response?.data?.message || '로그인 중 오류가 발생했습니다.'
      return {
        success: false,
        message: error.value
      }
    } finally {
      isLoading.value = false
    }
  }

  const signUp = async function(signUpData) {
    // try {
    //   // 비밀번호 일치 여부 확인
    //   if (signUpData.password1 !== signUpData.password2) {
    //     throw new Error('비밀번호가 일치하지 않습니다.')
    //   }

    //   isLoading.value = true
    //   error.value = null
      
    //   const response = await axios.post('http://127.0.0.1:8000/accounts/registration/', {
    //     username: signUpData.username,
    //     password: signUpData.password1,  // password1을 사용
    //     password: signUpData.password2,  // password2을 사용 -> dj_rest_auth는 password confirmation을 요구하므로
    //   })

    //   if (response.status === 201 || response.status === 200) {
    //     // 회원가입 후 자동으로 받은 토큰이 있다면 저장
    //     if (response.data.access){
    //       localStorage.setItem('access_token', response.data.access)
    //       axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
    //     }
    //     if (response.data.refresh){
    //       localStorage.setItem('refresh_token', response.data.refresh)
    //     }

    //     return {
    //       success: true,
    //       message: '회원가입이 완료되었습니다.'
    //     }
    //   }
    // } catch (err) {
    //   console.log('Error response:', err.response)    // 에러 확인용 출력
    //   if (err.message === '비밀번호가 일치하지 않습니다.') {
    //     error.value = err.message
    //   } else {
    //     error.value = err.response?.data?.message || '회원가입 중 오류가 발생했습니다.'
    //   }
    //   return {
    //     success: false,
    //     message: error.value
    //   }
    // } finally {
    //   isLoading.value = false
    // }

    const username = signUpData.username
    const password1 = signUpData.password1
    const password2 = signUpData.password2

    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/accounts/registration/`,
      data: {
        username, password1, password2
      }
    })
    .then(res => {
      console.log('회원가입이 완료되었습니다.')
    })
    .catch(err => console.log(err))
  }

  return {  
    signUp,
    login, 
    error,
    isLoading
  }
})