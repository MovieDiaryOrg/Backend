<template>
  <Suspense>
    <template #default>
      <div class="min-h-screen bg-white">
        <Header :isLoggedIn="isLoggedIn" @login="login" @logout="logout" />

        <main class="max-w-7xl mx-auto px-6 py-12">
          <h1 class="text-[120px] font-black leading-tight tracking-tight mb-12">
            MY FILM MEMORY
          </h1>

          <ScrollingText />

          <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
            <FeaturedFilm :film="featuredFilm" />

            <section>
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold">감상평 모아보기</h2>
                <select v-model="sortBy" class="px-4 py-2 border rounded-md">
                  <option value="latest">최신순</option>
                  <option value="likes">좋아요 많은 순</option>
                  <option value="rating">별점 높은 순</option>
                </select>
              </div>
              <div class="bg-gray-100 p-6 rounded-2xl h-[600px] overflow-y-auto">
                <div class="grid grid-cols-2 gap-4">
                  <ReviewCard 
                    v-for="review in sortedReviews" 
                    :key="review.id" 
                    :image="review.image"
                    :title="review.title"
                    :author="review.author"
                    :rating="review.rating"
                    :likes="review.likes"
                  />
                </div>
              </div>
            </section>
          </div>
        </main>
      </div>
    </template>
    <template #fallback>
      <div>Loading...</div>
    </template>
  </Suspense>  
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Header from '@/components/Header.vue'
import ScrollingText from '@/components/ScrollingText.vue'
import FeaturedFilm from '@/components/FeaturedFilm.vue'
import ReviewCard from '@/components/ReviewCard.vue'
import MainPage from '@/services/main'

const featuredFilm = ref({
  tmdb_id: 0,
  title: '',
  image: '', // 기본값 제공
  release_date: '',
  description: '',
  genre: []
});
const reviews = ref([]);

const isLoggedIn = ref(false)
const sortBy = ref('latest')

const login = () => isLoggedIn.value = true
const logout = () => isLoggedIn.value = false

onMounted(async() => {
  try{
    const mainPageData = await MainPage();

    // 인기 영화 데이터 설정
    const popularMovie = mainPageData.popular_movie || {};
    featuredFilm.value = {
      tmdb_id: popularMovie.tmdb_id || 0,
      title: popularMovie.title || '',
      image: popularMovie.image || '/placeholder.svg',
      release_date: popularMovie.release_date || '',
      description: popularMovie.description || '',
      genre: (popularMovie.genre || []).join(', ') // 장르를 쉼표로 구분된 문자열로 변환
    };

    // 리뷰 데이터 설정
    const movieJournals = mainPageData.movie_journals || [];

    reviews.value = movieJournals.map((journal) => ({
      id: journal.movie_journal.id,
      // title: journal.movie_journal.title.split(' ')[1] || 'No Title', // 임시 제목 추출
      title: journal.title|| 'No Title', // 임시 제목 추출
      author: journal.movie_journal.user.username,
      image: journal.movie_journal.ai_img 
      ? `http://localhost:8000${journal.movie_journal.ai_img}`
      : '/placeholder.svg',
      rating: parseFloat(journal.movie_journal.evaluation) || 0,
      likes: journal.movie_journal.likes_count || 0
    }));

    console.log('Reviews:', reviews.value);
  } catch (err) {
    console.error('Error loading main page data:', err);
  }
});

const sortedReviews = computed(() => {
  return [...reviews.value].sort((a, b) => {
    if (sortBy.value === 'latest') return b.id - a.id
    if (sortBy.value === 'likes') return b.likes - a.likes
    if (sortBy.value === 'rating') return b.rating - a.rating
    return 0
  })
})
</script>

<style scoped>
</style>