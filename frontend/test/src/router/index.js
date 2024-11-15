import { createRouter, createWebHistory } from 'vue-router'
import UserView from '@/views/UserView.vue'
import SignUpView from '@/views/SignUpView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/user',
      name: 'user',
      component: UserView
    },    
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    }
  ]
})

export default router
