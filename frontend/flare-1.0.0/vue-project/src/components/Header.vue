<template>
  <header class="px-6 py-4 border-b">
    <nav class="flex items-center justify-between max-w-7xl mx-auto">
      <div class="text-sm font-medium space-x-4">
        <!-- Home 버튼 -->
        <router-link to="/main" class="text-gray-600 hover:text-black">Home</router-link>
        <!-- My Diary 버튼 -->
        <router-link to="/mydiary" class="text-gray-600 hover:text-black">My Diary</router-link>
      </div>
      <div class="flex items-center space-x-4">
        <template v-if="store.isLoggedIn">
          <!-- 로그인 상태 -->
          <span class="text-sm font-medium text-gray-600">
            {{ store.user?.fullName }}님
          </span>
          <button
            @click="navigateToProfile"
            class="px-4 py-2 text-sm font-medium text-black bg-gray-200 rounded-full hover:bg-gray-300"
          >
            My Profile
          </button>
          <button
            @click="logout"
            class="px-4 py-2 text-sm font-medium text-black bg-gray-200 rounded-full hover:bg-gray-300"
          >
            Logout
          </button>
        </template>
        <template v-else>
          <!-- 비로그인 상태 -->
          <button
            @click="navigateToLogin"
            class="px-4 py-2 text-sm font-medium text-black bg-gray-200 rounded-full hover:bg-gray-300"
          >
            Login
          </button>
          <button
            @click="navigateToSignup"
            class="px-4 py-2 text-sm font-medium text-white bg-black rounded-full hover:bg-gray-800"
          >
            Sign Up
          </button>
        </template>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

// Pinia 상태 가져오기
const store = useCounterStore()
const router = useRouter()

// 네비게이션 함수
const navigateToLogin = () => {
  router.push({ name: 'Login' })
}

const navigateToSignup = () => {
  router.push({ name: 'Signup' })
}

const navigateToProfile = () => {
  router.push({ name: 'Profile' })
}

// 로그아웃 함수
const logout = async () => {
  const result = await store.logout()
  if (result.success) {
    alert(result.message)
    router.push('/main')
  } else {
    alert(result.message)
  }
}
</script>
