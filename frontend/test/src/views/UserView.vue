<template>
  <h1>Login View</h1>
  <div>
    <form @submit.prevent="handleLogin">
      <label for="username">username: </label>
      <input type="text" id="username" v-model.trim="username"><br>

      <label for="password">password: </label>
      <input type="password" id="password" v-model.trim="password"><br>

      <input type="submit" value="Login" :disabled="store.isLoading">
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

const username = ref('')
const password = ref('')

const handleLogin = async () => {
  const result = await store.login({
    username: username.value,
    password: password.value
  })
  
  if (result.success) {
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