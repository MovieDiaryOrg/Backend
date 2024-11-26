import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '@/views/MainPage.vue';
import IntroPage from '@/views/IntroPage.vue'; // IntroPage 컴포넌트
import Login from '@/views/Login.vue';
import Signup from '@/views/Signup.vue';
import Profile from '@/views/Profile.vue';
import ProfileEdit from '@/views/ProfileEdit.vue';
import FilmMyMemoryView from '@/views/FilmMyMemoryView.vue';
import FilmMemoryView from '@/views/FilmMemoryView.vue';
import { useCounterStore } from '@/stores/counter';

const routes = [
  { path: '/', component: IntroPage }, // IntroPage 경로
  { path: '/main', component: MainPage }, // MainPage 경로
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } }, // 인증 필요
  { path: '/profile/edit', name: 'ProfileEdit', component: ProfileEdit, meta: { requiresAuth: true } }, // 인증 필요
  { path: '/mydiary', name: 'FilmMyMemoryView', component: FilmMyMemoryView, meta: { requiresAuth: true } }, // 인증 필요
  { path: '/:user_pk/diary/', name: 'FilmMemoryView', component: FilmMemoryView, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const store = useCounterStore();

  if (to.meta.requiresAuth && !store.isLoggedIn) {
    // 인증이 필요한 경로인데 로그인되지 않은 경우
    alert('로그인 후 이용할 수 있습니다.');
    next({ name: 'Login' }); // 로그인 페이지로 리다이렉트
  } else {
    next(); // 정상적으로 진행
  }
});

export default router;
