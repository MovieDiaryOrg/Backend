import { createRouter, createWebHistory } from 'vue-router'
import UserView from '@/views/UserView.vue'
import SignUpView from '@/views/SignUpView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: HomeView,
    // },
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import('../views/AboutView.vue'),
    // },
    {
      path: '/user/',
      name: 'user',
      component: UserView,
      children: [
        {
          path: '/signup/',
          name: 'signup',
          component: SignUpView
        }
        
      ]
    },
  ],
})

export default router
