<template>
  <h1>SignUp View</h1>
  <div>
    <form @submit.prevent="handleSignUp">
      <label for="username">username: </label>
      <input type="text" id="username" v-model.trim="username" required><br>

      <label for="password1">password1: </label>
      <input type="password" id="password1" v-model.trim="password1" required><br>
      
      <label for="password2">password2: </label>
      <input type="password" id="password2" v-model.trim="password2" required><br>

      <label for="first_name">First name: </label>
      <input type="text" id="first_name" v-model.trim="first_name" required><br>
      
      <label for="last_name">Last name: </label>
      <input type="text" id="last_name" v-model.trim="last_name" required><br>

      <label for="email">Email: </label>
      <input type="email" id="email" v-model.trim="email" required><br>

      <label for="phone">Phone: </label>
      <input type="text" id="phone" v-model.trim="phone" required><br>

      <label for="image">Profile Image: </label>
      <input type="file" id="image" @change="onImageChange"><br>

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
  const first_name = ref('')
  const last_name = ref('')
  const email = ref('')
  const phone = ref('')
  const profile_image = ref(null)

  const onImageChange = (e) => {
    const file = e.target.files[0]
    
    if (file) {
      profile_image.value = file
    }
  }

  const handleSignUp = async () => {
    const result = await store.signUp({
      username: username.value,
      password1: password1.value,
      password2: password2.value,
      first_name: first_name.value,
      last_name: last_name.value,
      email: email.value,
      phone: phone.value,
      profile_image: profile_image.value || null
    })

    console.log(`result = ${result}`)
    // const result = await store.signUp({
    //   username : username.value,
    //   password1: password1.value,
    //   password2: password2.value
    // })
    router.push('/accounts/')

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