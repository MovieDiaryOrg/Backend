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
    <main class="max-w-7xl mx-auto px-6 py-12">
      <div class="flex items-start justify-between mb-12">
        <div class="flex items-start space-x-8">
          <div class="w-32 h-32 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
            <img 
              v-if="user.profileImage"
              :src="user.profileImage" 
              alt="Profile Picture"
              class="w-full h-full object-cover"
            />
            <UserIcon v-else class="w-16 h-16 text-gray-400" />
          </div>
          <div>
            <div class="flex items-center space-x-4">
              <h1 class="text-4xl font-bold">My profile</h1>
              <router-link 
                to="/profile/edit"
                class="text-sm text-gray-600 hover:text-gray-900"
              >
                내 정보 수정
              </router-link>
            </div>
            <div class="mt-6 space-y-2">
              <p class="text-lg">name : {{ user.name }}</p>
              <p class="text-lg">phone : {{ user.phone }}</p>
              <p class="text-lg">email : {{ user.email }}</p>
            </div>
            <div class="mt-6 flex items-center space-x-8">
              <div class="flex items-center space-x-2">
                <UsersIcon class="w-5 h-5 text-gray-500" />
                <span class="font-medium">{{ user.followers.length }} 팔로워</span>
              </div>
              <div class="flex items-center space-x-2">
                <UserPlusIcon class="w-5 h-5 text-gray-500" />
                <span class="font-medium">{{ user.following.length }} 팔로잉</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Liked Posts Section -->
        <section class="bg-gray-50 rounded-2xl p-6">
          <h2 class="text-xl font-semibold mb-4 flex items-center">
            <HeartIcon class="w-5 h-5 mr-2" />
            내가 좋아하는 게시글
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <ReviewCard 
              v-for="post in likedPosts" 
              :key="post.id"
              :image="post.image"
              :title="post.title"
              :author="post.author"
              :rating="post.rating"
            />
          </div>
        </section>

        <!-- My Comments Section -->
        <section class="bg-gray-50 rounded-2xl p-6">
          <h2 class="text-xl font-semibold mb-4 flex items-center">
            <MessageCircleIcon class="w-5 h-5 mr-2" />
            내가 작성한 댓글
          </h2>
          <div class="space-y-4 h-[400px] overflow-y-auto pr-2">
            <div v-for="comment in myComments" :key="comment.id" class="bg-white rounded-lg p-4 shadow-sm">
              <div class="flex justify-between items-start mb-2">
                <p class="font-medium">게시글 : {{ comment.postTitle }}</p>
                <p class="text-sm text-gray-500">작성자 : {{ comment.author }}</p>
              </div>
              <p class="text-gray-600">{{ comment.content }}</p>
            </div>
          </div>
        </section>
      </div>

      <!-- Followers and Following Section -->
      <div class="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8">
        <section class="bg-gray-50 rounded-2xl p-6">
          <h2 class="text-xl font-semibold mb-4 flex items-center">
            <UsersIcon class="w-5 h-5 mr-2" />
            팔로워
          </h2>
          <div class="space-y-4 h-[300px] overflow-y-auto pr-2">
            <div v-for="follower in user.followers" :key="follower.id" class="flex items-center space-x-4 bg-white rounded-lg p-4 shadow-sm">
              <div class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
                <img 
                  v-if="follower.profileImage"
                  :src="follower.profileImage" 
                  alt="Follower Profile Picture"
                  class="w-full h-full object-cover"
                />
                <UserIcon v-else class="w-6 h-6 text-gray-400" />
              </div>
              <div>
                <p class="font-medium">{{ follower.name }}</p>
                <p class="text-sm text-gray-500">{{ follower.email }}</p>
              </div>
            </div>
          </div>
        </section>

        <section class="bg-gray-50 rounded-2xl p-6">
          <h2 class="text-xl font-semibold mb-4 flex items-center">
            <UserPlusIcon class="w-5 h-5 mr-2" />
            팔로잉
          </h2>
          <div class="space-y-4 h-[300px] overflow-y-auto pr-2">
            <div v-for="following in user.following" :key="following.id" class="flex items-center space-x-4 bg-white rounded-lg p-4 shadow-sm">
              <div class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
                <img 
                  v-if="following.profileImage"
                  :src="following.profileImage" 
                  alt="Following Profile Picture"
                  class="w-full h-full object-cover"
                />
                <UserIcon v-else class="w-6 h-6 text-gray-400" />
              </div>
              <div>
                <p class="font-medium">{{ following.name }}</p>
                <p class="text-sm text-gray-500">{{ following.email }}</p>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- New Account Management Section -->
      <div class="mt-12">
        <section class="bg-gray-50 rounded-2xl p-6">
          <h2 class="text-xl font-semibold mb-4 flex items-center">
            <SettingsIcon class="w-5 h-5 mr-2" />
            계정 관리
          </h2>
          <div class="space-y-4">
            <button
              @click="showDeleteConfirmation = true"
              class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition duration-300"
            >
              회원 탈퇴
            </button>
          </div>
        </section>
      </div>
    </main>

    <!-- Delete Account Confirmation Modal -->
    <div v-if="showDeleteConfirmation" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-8 max-w-md w-full">
        <h3 class="text-2xl font-bold mb-4">회원 탈퇴 확인</h3>
        <p class="mb-6">정말로 회원 탈퇴를 진행하시겠습니까? 이 작업은 되돌릴 수 없습니다.</p>
        <div class="flex justify-end space-x-4">
          <button
            @click="showDeleteConfirmation = false"
            class="px-4 py-2 bg-gray-300 rounded-md hover:bg-gray-400 transition duration-300"
          >
            취소
          </button>
          <button
            @click="handleDeleteAccount"
            class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition duration-300"
          >
            탈퇴 확인
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { getProfile, deleteAccountAPI } from '@/services/account'
import { HeartIcon, MessageCircleIcon, UserIcon, UsersIcon, UserPlusIcon, SettingsIcon } from 'lucide-vue-next'
import ReviewCard from '@/components/ReviewCard.vue'

const router = useRouter()
const showDeleteConfirmation = ref(false)

const user = ref({
  name: '사용자1',
  phone: '010-1234-5678',
  email: 'admin1@ssafy.com',
  profileImage: null,
  followers: [
    { id: 1, name: '팔로워1', email: 'follower1@example.com', profileImage: null },
    { id: 2, name: '팔로워2', email: 'follower2@example.com', profileImage: null },
    { id: 3, name: '팔로워3', email: 'follower3@example.com', profileImage: null },
  ],
  following: [
    { id: 1, name: '팔로잉1', email: 'following1@example.com', profileImage: null },
    { id: 2, name: '팔로잉2', email: 'following2@example.com', profileImage: null },
    { id: 3, name: '팔로잉3', email: 'following3@example.com', profileImage: null },
    { id: 4, name: '팔로잉4', email: 'following4@example.com', profileImage: null },
  ]
})

const likedPosts = ref([
  { id: 1, title: '오펜하이머', author: '크리스토퍼 놀란', image: '/placeholder.svg?height=200&width=200', rating: 4.5 },
  { id: 2, title: '다크나이트', author: '크리스토퍼 놀란', image: '/placeholder.svg?height=200&width=200', rating: 5 },
  { id: 3, title: '인셉션', author: '크리스토퍼 놀란', image: '/placeholder.svg?height=200&width=200', rating: 4.8 },
])

const myComments = ref([
  {
    id: 1,
    postTitle: '오펜하이머',
    author: '사용자2',
    content: '영화를 보면서 느낀 감정을 이렇게 세심하게 표현해주셔서 다시 그 장면들이 떠오르네요, 정말 공감합니다.'
  },
  {
    id: 2,
    postTitle: '7번방의 선물',
    author: '사용자10',
    content: '감상문을 읽으니 영화의 따뜻함과 슬픔, 그리고 슬픔까지 모두 함께 느껴지는 것 같아요, 너무 잘 표현하셨어요!'
  },
  {
    id: 3,
    postTitle: '인사이드아웃',
    author: '사용자3',
    content: '그렇게 너무 귀엽네요. 잘 봤습니다. 좋아요 누르고 갑니다!'
  }
])

const handleDeleteAccount = async () => {
  try {
    await deleteAccountAPI(); // 회원 탈퇴 API 호출
    alert('회원 탈퇴가 완료되었습니다.');
    localStorage.removeItem('access_token'); // 로컬 스토리지에서 토큰 삭제
    router.push('/login'); // 로그인 페이지로 이동
  } catch (error) {
    console.error('회원 탈퇴 실패:', error.response?.data || error);
    alert('회원 탈퇴에 실패했습니다. 다시 시도해주세요.');
  }
};
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>