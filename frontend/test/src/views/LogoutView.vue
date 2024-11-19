<template>
  <h1>Logout View</h1>
  <div>
    <form @submit.prevent="handleLogout">
      <input type="submit" value="Logout" :disabled="store.isLoading">
    </form>
    <p v-if="store.error" class="error">{{ store.error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()

const handleLogout = async () => {
  const result = await store.logout()
  
  if (result.success) {
    localStorage.removeItem('access_token')      // localStorage에서 토큰 제거
    localStorage.removeItem('refresh_token')      // localStorage에서 토큰 제거
    alert(result.message)
    // 로그인 성공 시 이동할 페이지 설정
    router.push('/') // 또는 다른 페이지로 이동
  } else {
    alert(result.message)
  }
}
</script>

<style scoped>
.error {
  color: red;
  font-size: 0.9em;
  margin-top: 10px;
}
</style>