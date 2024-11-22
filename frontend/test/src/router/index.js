import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogoutView from '@/views/LogoutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },    
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: "/",
      redirect: "/login", // 기본 경로를 로그인 페이지로 리디렉션
    },
  ]
})

export default router
