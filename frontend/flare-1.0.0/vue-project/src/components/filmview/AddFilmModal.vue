<script setup>
import { ref, watch } from 'vue';
import { addMovieDiary, fetchMovieDetail } from '@/services/diary.js';

// props 정의
const props = defineProps({
  mode: { type: String, default: 'add' }, // 'add' 또는 'edit'
  initialFilm: { type: Object, default: () => ({}) } // 수정 모드의 초기 데이터
});

// emit 정의
const emit = defineEmits(['close', 'show-detail']); // 상세 페이지 렌더링 이벤트 추가

// 영화 데이터 상태
const film = ref({
  title: '',
  rating: 0,
  description: '',
  watched_date: new Date().toISOString().substr(0, 10)
});

// props를 watch하여 초기 데이터를 설정
watch(
  () => props.initialFilm,
  (newFilm) => {
    if (props.mode === 'edit' && newFilm) {
      film.value = { ...newFilm };
    } else if (props.mode === 'add') {
      // 새로운 데이터를 초기화
      film.value = {
        title: '',
        rating: 0,
        description: '',
        watched_date: new Date().toISOString().substr(0, 10)
      };
    }
  },
  { immediate: true }
);

// 등록 버튼 로직
const handleSubmit = async () => {
  if (!film.value.title || !film.value.rating) {
    alert('제목과 평점을 모두 입력해주세요.');
    return;
  }

  const movieData = {
    content: film.value.description,
    watched_date: film.value.watched_date,
    movie: film.value.title,
    evaluation: film.value.rating
  };

  try {
    // 영화 등록 API 호출
    const registeredFilm = await addMovieDiary(movieData);

    // 등록된 영화 ID로 상세 정보 조회
    const filmDetail = await fetchMovieDetail(registeredFilm.movie_journal.id);

    // 부모 컴포넌트로 상세 페이지 렌더링 이벤트 전달
    emit('show-detail', filmDetail.movie_journal);

    // 모달 닫기 이벤트 발생
    emit('close');
  } catch (error) {
    alert('영화 등록 중 오류가 발생했습니다. 다시 시도해주세요.');
    console.error(error);
  }
};
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white rounded-lg p-8 w-full max-w-3xl">
      <h2 class="text-3xl font-bold mb-6">
        {{ mode === 'add' ? '새 영화 추가' : '영화 수정' }}
      </h2>
      <div class="space-y-6">
        <!-- 제목 입력 -->
        <div class="space-y-1">
          <label for="movie-title" class="block text-sm font-medium text-gray-700">영화 제목</label>
          <input
            id="movie-title"
            v-model="film.title"
            placeholder="영화 제목을 입력하세요"
            class="w-full px-4 py-3 border rounded-md bg-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
          />
        </div>

        <!-- 감상문 입력 -->
        <div class="space-y-1">
          <label for="movie-review" class="block text-sm font-medium text-gray-700">감상문</label>
          <textarea
            id="movie-review"
            v-model="film.description"
            placeholder="감상문을 적어보세요"
            class="w-full h-48 p-4 border rounded-md resize-none bg-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
          ></textarea>
        </div>

        <!-- 시청 날짜 -->
        <div class="flex space-x-6">
          <div class="space-y-1 flex-1">
            <label for="watch-date" class="block text-sm font-medium text-gray-700">시청 날짜</label>
            <input
              id="watch-date"
              v-model="film.watched_date"
              type="date"
              class="w-full px-4 py-3 border rounded-md bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
            />
          </div>

          <!-- 평점 -->
          <div class="space-y-1 flex-1">
            <label class="block text-sm font-medium text-gray-700">평가</label>
            <div class="flex items-center">
              <div
                v-for="i in 5"
                :key="i"
                @click="film.rating = i"
                :class="[
                  'w-10 h-10 cursor-pointer transition-colors',
                  i <= film.rating ? 'text-yellow-500' : 'text-gray-300'
                ]"
              >★</div>
              <span class="ml-2 text-xl">{{ film.rating || 0 }}점</span>
            </div>
          </div>
        </div>

        <!-- 버튼 -->
        <div class="flex justify-end space-x-4">
          <button
            @click="$emit('close')"
            class="px-6 py-3 border rounded-md text-gray-800 hover:bg-gray-200 transition duration-300 text-lg"
          >
            취소
          </button>
          <button
            @click="handleSubmit"
            class="px-8 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition duration-300 transform hover:scale-105 text-lg"
          >
            {{ mode === 'add' ? '등록하기' : '수정 완료' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
