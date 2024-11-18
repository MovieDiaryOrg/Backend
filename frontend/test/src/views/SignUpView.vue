<template>
  <h1>SignUp View</h1>
  <div>
    <form @submit.prevent="handleSignUp">
      <label for="username">username: </label>
      <input type="text" id="username" v-model.trim="username"><br>

      <label for="password1">password1: </label>
      <input type="password" id="password1" v-model.trim="password1"><br>
      
      <label for="password2">password2: </label>
      <input type="password" id="password2" v-model.trim="password2"><br>

      <button :disabled="store.isLoading">{{ store.isLoading?'처리중..':'회원가입' }}</button>
      <p v-if="store.error" class="error">{{store.error}}</p>
    </form>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  import { useRouter } from 'vue-router'

  const store = useCounterStore()
  const router = useRouter()

  const username = ref('')
  const password1 = ref('')
  const password2 = ref('')

  const handleSignUp = async () => {
    const result = await store.signUp({
      username : username.value,
      password1: password1.value,
      password2: password2.value
    })
    router.push('/accounts/')

    console.log(`result = ${result}`)

    // 에러 처리 로직 강화
    if (result.success){
      alert(result.message)
      router.push('/accounts/')    // 로그인 페이지로 이동
    } else {
      alert(result.message)
    }
  }
</script>

<style scoped>
</style>