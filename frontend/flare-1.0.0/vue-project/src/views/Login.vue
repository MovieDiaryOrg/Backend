<template>
  <div class="min-h-screen bg-white">
    <!-- Header -->
    <header class="px-6 py-4">
      <nav class="flex items-center justify-between max-w-7xl mx-auto">
        <div class="flex items-center space-x-6">
          <router-link to="/main" class="text-sm hover:text-gray-600">Home</router-link>
          <router-link to="/mydiary" class="text-sm hover:text-gray-600">My Diary</router-link>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="max-w-md mx-auto px-6 pt-20">
      <h1 class="text-4xl font-black text-center mb-12">LOGIN</h1>
      
      <div class="space-y-8">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-1">
            <label for="username" class="block text-sm font-medium">
              아이디
            </label>
            <input 
              id="username" 
              v-model="username" 
              type="text" 
              required
              class="w-full px-3 py-2 border-b border-gray-200 focus:border-gray-900 focus:outline-none transition-colors bg-transparent"
            />
          </div>

          <div class="space-y-1">
            <label for="password" class="block text-sm font-medium">
              비밀번호
            </label>
            <input 
              id="password" 
              v-model="password" 
              type="password" 
              required
              class="w-full px-3 py-2 border-b border-gray-200 focus:border-gray-900 focus:outline-none transition-colors bg-transparent"
            />
          </div>

          <div class="pt-4">
            <button 
              type="submit"
              class="w-full bg-black text-white py-3 rounded-full hover:bg-gray-800 transition-colors"
            >
              로그인
            </button>
          </div>
        </form>

        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 bg-white text-gray-500">또는</span>
          </div>
        </div>

        <div class="text-center">
          <p class="text-sm text-gray-600">
            계정이 없으신가요?
            <router-link to="/signup" class="text-black hover:underline ml-1">
              회원가입
            </router-link>
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const router = useRouter()
const store = useCounterStore()

const username = ref('')
const password = ref('')

const handleLogin = async () => {
  const result = await store.login(username.value, password.value)

  if (result.success) {
    alert(result.message)
    router.push('/main') // 로그인 성공 후 /main으로 이동
  } else {
    alert(result.message)
  }
}
</script>

<style scoped>
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
  -webkit-box-shadow: 0 0 0px 1000px white inset;
  transition: background-color 5000s ease-in-out 0s;
}
</style>