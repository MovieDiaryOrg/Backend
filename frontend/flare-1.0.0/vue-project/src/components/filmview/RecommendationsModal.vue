<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg w-[600px] max-h-[80vh] overflow-y-auto relative shadow-xl">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6 border-b pb-4">
          <div class="flex items-center">
            <CircuitBoardIcon class="w-6 h-6 text-blue-500 mr-2" />
            <h2 class="text-xl font-bold">AI 추천 영화</h2>
          </div>
          <button 
            @click="$emit('close')" 
            class="text-gray-500 hover:text-gray-700 transition-colors"
            aria-label="Close"
          >
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        
        <div class="space-y-6">
          <div 
            v-for="movie in recommendedMovies" 
            :key="movie.title" 
            class="flex gap-4 p-4 bg-gray-50 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-300"
          >
            <img 
              :src="movie.poster || '/placeholder.svg?height=120&width=80'" 
              :alt="movie.title"
              class="w-20 h-30 object-cover rounded shadow"
            />
            <div class="flex-1 min-w-0">
              <h3 class="font-bold text-lg mb-1 flex items-center">
                <FilmIcon class="w-4 h-4 text-purple-500 mr-2" />
                {{ movie.title }}
              </h3>
              <p class="text-sm text-gray-600 mb-1 flex items-center">
                <CalendarIcon class="w-4 h-4 text-gray-400 mr-1" />
                개봉일: {{ formatDate(movie.releaseDate) }}
              </p>
              <div class="flex items-center mb-2">
                <StarIcon class="w-4 h-4 text-yellow-500 mr-1" />
                <span class="text-sm font-medium">
                  {{ movie.rating ? movie.rating.toFixed(1) : 'N/A' }}
                </span>
              </div>
              <div class="relative">
                <p class="text-sm text-gray-700 mb-2 line-clamp-2">
                  {{ movie.plot || '줄거리 정보가 없습니다.' }}
                </p>
                <button 
                  @click="togglePlot(movie)" 
                  class="text-xs text-blue-500 hover:underline focus:outline-none"
                >
                  {{ movie.showFullPlot ? '줄이기' : '더 보기' }}
                </button>
                <div v-if="movie.showFullPlot" class="absolute z-10 bg-white border border-gray-200 rounded-md p-2 shadow-lg mt-1">
                  <p class="text-sm text-gray-700">{{ movie.plot }}</p>
                </div>
              </div>
              <p class="text-sm text-gray-600 mt-2 flex items-start">
                <LightbulbIcon class="w-4 h-4 text-yellow-400 mr-1 mt-0.5 flex-shrink-0" />
                <span><strong>추천 이유:</strong> {{ movie.reason || '추천 이유가 제공되지 않았습니다.' }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { StarIcon, XIcon, FilmIcon, CalendarIcon, LightbulbIcon, CircuitBoardIcon } from 'lucide-vue-next'

const props = defineProps({
  recommendedMovies: {
    type: Array,
    default: () => []
  }
})

defineEmits(['close'])

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return isNaN(date.getTime()) ? 'N/A' : date.toISOString().split('T')[0]
}

const togglePlot = (movie) => {
  if (!movie.showFullPlot) {
    movie.showFullPlot = true
  } else {
    movie.showFullPlot = false
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>