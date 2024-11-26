<template>
  <div class="min-h-screen bg-white">
    <!-- Header -->
    <header class="px-6 py-4 border-b">
      <nav class="flex items-center justify-between max-w-7xl mx-auto">
        <div class="flex items-center space-x-6">
          <router-link to="/main" class="text-sm hover:text-gray-600">Home</router-link>
          <router-link to="/mydiary" class="text-sm hover:text-gray-600">My Diary</router-link>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="max-w-2xl mx-auto px-6 py-12">
      <h1 class="text-4xl font-bold mb-12">프로필 수정</h1>
      
      <form @submit.prevent="handleSubmit" class="space-y-8">
        <div class="flex justify-center">
          <div class="relative w-32 h-32">
            <div class="w-full h-full rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
              <img 
                v-if="profileImage"
                :src="profileImage"
                alt="Profile Picture"
                class="w-full h-full object-cover"
              />
              <UserIcon v-else class="w-full h-full p-4 text-gray-400" />
            </div>
            <label for="profileImage" class="absolute bottom-0 right-0 bg-black text-white p-2 rounded-full cursor-pointer">
              <CameraIcon class="w-5 h-5" />
            </label>
            <input 
              id="profileImage" 
              type="file" 
              accept="image/*" 
              @change="handleImageUpload" 
              class="hidden"
            />
          </div>
        </div>

        <div class="space-y-1">
          <label for="firstName" class="block text-sm font-medium">이름</label>
          <input 
            id="firstName" 
            v-model="formData.firstName" 
            type="text" 
            required
            class="w-full px-3 py-2 border-b border-gray-200 focus:border-gray-900 focus:outline-none transition-colors bg-transparent"
          />
        </div>

        <div class="space-y-1">
          <label for="lastName" class="block text-sm font-medium">성</label>
          <input 
            id="lastName" 
            v-model="formData.lastName" 
            type="text" 
            required
            class="w-full px-3 py-2 border-b border-gray-200 focus:border-gray-900 focus:outline-none transition-colors bg-transparent"
          />
        </div>

        <div class="space-y-1">
          <label for="email" class="block text-sm font-medium">이메일</label>
          <input 
            id="email" 
            v-model="formData.email" 
            type="email" 
            required
            class="w-full px-3 py-2 border-b border-gray-200 focus:border-gray-900 focus:outline-none transition-colors bg-transparent"
          />
        </div>

        <div class="space-y-1">
          <label for="phone" class="block text-sm font-medium">전화번호</label>
          <input 
            id="phone" 
            v-model="formData.phone" 
            type="tel" 
            required
            class="w-full px-3 py-2 border-b border-gray-200 focus:border-gray-900 focus:outline-none transition-colors bg-transparent"
          />
        </div>
        <div class="space-y-1">
          <label for="currentPassword" class="block text-sm font-medium">현재 비밀번호</label>
          <input 
            id="currentPassword" 
            v-model="formData.currentPassword" 
            type="password" 
            class="w-full px-3 py-2 border-b border-gray-200 focus:border-gray-900 focus:outline-none transition-colors bg-transparent"
          />
        </div>
        <div class="space-y-1">
          <label for="password" class="block text-sm font-medium">새 비밀번호</label>
          <input 
            id="password" 
            v-model="formData.password" 
            type="password"
            class="w-full px-3 py-2 border-b border-gray-200 focus:border-gray-900 focus:outline-none transition-colors bg-transparent"
          />
        </div>

        <div class="space-y-1">
          <label for="confirmPassword" class="block text-sm font-medium">새 비밀번호 확인</label>
          <input 
            id="confirmPassword" 
            v-model="formData.confirmPassword" 
            type="password"
            class="w-full px-3 py-2 border-b border-gray-200 focus:border-gray-900 focus:outline-none transition-colors bg-transparent"
          />
        </div>

        <div class="flex space-x-4 pt-4">
          <button 
            type="submit"
            class="flex-1 bg-black text-white py-3 rounded-full hover:bg-gray-800 transition-colors"
          >
            저장하기
          </button>
          <button 
            type="button"
            @click="$router.push('/profile')"
            class="flex-1 bg-gray-200 text-gray-800 py-3 rounded-full hover:bg-gray-300 transition-colors"
          >
            취소
          </button>
        </div>
      </form>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProfile, updateProfile } from '@/services/account'
import { useCounterStore } from '@/stores/counter'
import { CameraIcon, UserIcon } from 'lucide-vue-next'

const router = useRouter()
const profileImage = ref(null)
const profileImageFile = ref(null) // 실제 파일 데이터 저장
const store = useCounterStore()


// Form 데이터 초기화
const formData = ref({
  firstName: '',
  lastName: '',
  phone: '',
  email: '',
  password: '',
  confirmPassword: '',
  currentPassword: '', 
})

// 사용자 정보 가져오기
const fetchUserProfile = async () => {
  try {
    const profile = await getProfile()
    formData.value.firstName = profile.first_name || ''
    formData.value.lastName = profile.last_name || ''
    formData.value.phone = profile.phone || ''
    formData.value.email = profile.email || ''
    profileImage.value = profile.profile_image || null // 프로필 이미지 URL 설정
  } catch (error) {
    console.error('사용자 정보 가져오기 실패:', error.response?.data || error)
    alert('사용자 정보를 불러오지 못했습니다. 다시 시도해주세요.')
    router.push('/login')
  }
}

// 컴포넌트 마운트 시 사용자 정보 가져오기
onMounted(() => {
  fetchUserProfile()
})

// 프로필 이미지 업로드
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    profileImage.value = URL.createObjectURL(file) // 미리보기용 URL 생성
    profileImageFile.value = file // 실제 파일 저장
    console.log('File selected:', file.name)
  }
}

const handleSubmit = async () => {
  if (formData.value.password && formData.value.password !== formData.value.confirmPassword) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }

  try {
    const formDataToSend = new FormData()
    formDataToSend.append('first_name', formData.value.firstName)
    formDataToSend.append('last_name', formData.value.lastName)
    formDataToSend.append('phone', formData.value.phone)
    formDataToSend.append('email', formData.value.email)

    // 새 비밀번호와 현재 비밀번호 추가
    if (formData.value.password) {
      formDataToSend.append('new_password1', formData.value.password)
      formDataToSend.append('new_password2', formData.value.confirmPassword)
      formDataToSend.append('current_password', formData.value.currentPassword) // 현재 비밀번호 추가
    }

    // 프로필 이미지가 있을 경우 추가
    if (profileImageFile.value) {
      formDataToSend.append('profile_image', profileImageFile.value)
    }

    // API 호출
    const response = await updateProfile(formDataToSend)
    await store.fetchUser(response);

    alert('회원정보가 성공적으로 수정되었습니다.')
    router.push('/profile')
  } catch (error) {
    console.error('회원정보 수정 실패:', error.response?.data || error)
    alert('회원정보 수정에 실패했습니다. 다시 시도해주세요.')
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