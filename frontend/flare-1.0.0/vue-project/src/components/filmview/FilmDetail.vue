<template>
  <div v-if="film" class="bg-white min-h-screen">
    <div class="max-w-5xl mx-auto px-6 py-8">
      <!-- Header Section -->
      <div class="flex items-center mb-8">
        <button @click="$emit('close')" class="text-gray-800 hover:text-gray-600 flex items-center">
          <ChevronLeftIcon class="w-5 h-5 mr-2" />
          다이어리로 돌아가기
        </button>
      </div>

      <!-- Title and Actions Section -->
      <div class="flex justify-between items-start mb-6">
        <h1 class="text-4xl font-bold">{{ film.title }}</h1>
        <div class="flex items-center space-x-3">
          <button 
            @click="handleFollow" 
            class="px-4 py-2 rounded-full border border-gray-300 hover:bg-gray-50 flex items-center"
          >
            <UserPlusIcon class="w-4 h-4 mr-2" />
            {{ isFollowing ? '팔로잉' : '팔로우' }}
          </button>
          <button 
            @click="handleLike" 
            class="p-2 rounded-full hover:bg-gray-50"
            :class="{ 'text-red-500': isLiked }"
          >
            <HeartIcon class="w-6 h-6" />
          </button>
        </div>
      </div>

      <!-- Metadata Section -->
      <div class="text-sm text-gray-500 mb-6">
        시청 날짜: {{ formatDate(film.watchedDate) }} | 작성 날짜: {{ formatDate(film.createdDate) }} | 수정 날짜: {{ formatDate(film.modifiedDate) }}
      </div>

      <!-- Stats Section -->
      <div class="flex items-center space-x-6 mb-8">
        <div class="flex items-center">
          <StarIcon class="w-6 h-6 text-yellow-500 mr-2" />
          <span class="text-xl font-semibold">{{ film.rating }}</span>
        </div>
        <div class="flex items-center">
          <HeartIcon class="w-6 h-6 text-red-500 mr-2" />
          <span class="text-xl font-semibold">{{ film.likes }}</span>
        </div>
        <div class="flex items-center">
          <MessageCircleIcon class="w-6 h-6 text-blue-500 mr-2" />
          <span class="text-xl font-semibold">{{ film.comments.length }}</span>
        </div>
      </div>

      <!-- Content Section -->
      <div class="flex space-x-8">
        <div class="w-1/3">
          <img
            :src="film.image"
            :alt="film.title"
            class="w-full rounded-lg shadow-lg"
          />
        </div>
        <div class="w-2/3">
          <div class="h-64 overflow-y-auto pr-4 mb-8">
            <p class="text-gray-800 leading-relaxed whitespace-pre-line">{{ film.content }}</p>
          </div>
          
          <!-- Edit/Delete Actions -->
          <div class="flex justify-end space-x-4">
            <button 
              @click="$emit('edit-film', film)" 
              class="px-4 py-2 text-sm border rounded-md text-gray-600 hover:bg-gray-50"
            >
              수정
            </button>
            <button 
              @click="$emit('delete-film', film.id)" 
              class="px-4 py-2 text-sm border rounded-md text-red-600 hover:bg-red-50"
            >
              삭제
            </button>
          </div>
        </div>
      </div>

      <!-- AI Recommendations Section -->
      <button @click="$emit('get-recommendations')" class="mt-4 flex items-center space-x-2 text-blue-600 hover:text-blue-800 font-semibold">
          <AtomIcon class="w-6 h-6" />
          <span class="text-lg">AI가 추천해주는 다른 영화</span>
      </button>

      <!-- Comments Section -->
      <section class="mt-8">
        <h2 class="text-2xl font-bold mb-4">댓글</h2>
        <div class="bg-gray-100 p-4 rounded-lg">
          <div class="space-y-4">
            <div v-for="comment in film.comments" :key="comment.id" class="flex items-start space-x-4">
              <img :src="placeholderImage" alt="Profile" class="w-10 h-10 rounded-full" />
              <div>
                <p class="font-medium text-gray-800">{{ comment.author }}</p>
                <p class="text-gray-600 mt-1">{{ comment.content }}</p>
              </div>
            </div>
          </div>
          <div class="mt-6 flex items-center">
            <input v-model="newComment" placeholder="댓글 작성..." class="flex-1 mb-2 px-4 py-2 border rounded-md bg-white" />
            <button @click="addComment" class="ml-2 bg-gray-300 text-gray-800 p-2 rounded-full hover:bg-gray-400">
              <MessageCircleIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </section>
    </div>

    <!-- RecommendationsModal -->
    <RecommendationsModal
      v-if="showRecommendationsModal"
      :recommendedMovies="selectedRecommendation"
      @close="closeRecommendationModal"
    />
  </div>

  <!-- Loading State -->
  <div v-else class="flex items-center justify-center min-h-screen text-gray-500">
    <Loader2Icon class="w-6 h-6 animate-spin mr-2" />
    로딩 중...
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import {
  StarIcon,
  HeartIcon,
  MessageCircleIcon,
  ChevronLeftIcon,
  AtomIcon,
  UserPlusIcon,
  CalendarIcon,
  Loader2Icon,
} from 'lucide-vue-next';
import RecommendationsModal from './RecommendationsModal.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const journal_pk = route.params.journal_pk; // 라우트에서 가져옴

const props = defineProps({
  film: { type: Object, required: true },
});

const emit = defineEmits(['close', 'edit-film', 'delete-film', 'add-comment', 'get-recommendations']);

const newComment = ref('');
const isLiked = ref(false);
const isFollowing = ref(false);
const showRecommendationsModal = ref(false);
const selectedRecommendation = ref([]);

const placeholderImage = computed(() => {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40">
      <rect width="100%" height="100%" fill="#e0e0e0"/>
      <text x="50%" y="50%" font-family="Arial" font-size="12" fill="#666" dominant-baseline="middle" text-anchor="middle">
        User
      </text>
    </svg>
  `;
  return `data:image/svg+xml;base64,${btoa(svg)}`;
});

const handleLike = () => {
  isLiked.value = !isLiked.value;
};

const handleFollow = () => {
  isFollowing.value = !isFollowing.value;
};

const addComment = async() => {
  if (!newComment.trim()) {
    alert('댓글 내용을 입력해주세요.');
    return;
  }

  try {
    // API 호출로 새 댓글 추가
    const newCommentData = await addComment(journal_pk, newComment);

    // 댓글 배열에 새 댓글 추가
    film.comments.push({
      id: newCommentData.id,
      author: newCommentData.author,
      content: newCommentData.content,
    });

    // 입력 필드 초기화
    newComment = '';
    console.log('새로 추가된 댓글:', newCommentData);
  } catch (error) {
    console.error('댓글 추가 실패:', error);
    alert('댓글 추가에 실패했습니다. 다시 시도해주세요.');
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? '' : date.toISOString().split('T')[0];
};

const openRecommendationModal = (recommendation) => {
  selectedRecommendation.value = props.film.recommended.map((rec) => ({
    title: rec.movie.title,
    poster: rec.movie.poster_path,
    releaseDate: rec.movie.release_date,
    rating: parseFloat(rec.movie.vote_average),
    plot: rec.movie.description || '설명이 없습니다.',
    reason: rec.reason,
  }));
  showRecommendationsModal.value = true;
};

const closeRecommendationModal = () => {
  showRecommendationsModal.value = false;
};
</script>