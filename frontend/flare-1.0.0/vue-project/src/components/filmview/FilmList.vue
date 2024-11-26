<!-- components/filmview/FilmList.vue -->


<template>
  <div>
    <div class="flex justify-between items-center mb-8">
      <div class="relative w-64">
        <input
          :value="searchQuery"
          @input="$emit('update:searchQuery', $event.target.value)"
          type="text"
          placeholder="영화 검색..."
          class="pl-10 pr-4 py-2 w-full border rounded-full bg-gray-100"
        />
        <SearchIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
      </div>
      <select
        :value="filterOption"
        @change="$emit('update:filterOption', $event.target.value)"
        class="px-4 py-2 rounded-full border bg-gray-100"
      >
        <option value="all">모든 영화</option>
        <option value="highRated">높은 평점순</option>
        <option value="mostLiked">좋아요 많은 순</option>
      </select>
    </div>
    <TransitionGroup name="book-list" tag="div" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
      <div
        v-for="film in films"
        :key="film.id"
        @click="$emit('select-film', film.id)"
        class="book-container cursor-pointer transform transition-all duration-300 hover:scale-105"
      >
        <div class="book">
          <div class="book-cover">
            <img :src="film.image" :alt="film.title" class="w-full h-full object-cover" />
            <div class="book-title-overlay">
              <h3 class="font-bold text-lg text-white text-center">{{ film.title }}</h3>
            </div>
          </div>
          <div class="book-spine">
            <h3 class="font-bold text-sm text-gray-800 writing-mode-vertical">{{ film.title }}</h3>
          </div>
        </div>
        <div class="mt-2 text-center">
          <div class="flex justify-center items-center">
            <StarIcon class="w-5 h-5 text-yellow-500 mr-1" />
            <span class="text-base">{{ film.rating.toFixed(1) }}</span>
          </div>
          <div class="flex justify-center items-center space-x-3 mt-1">
            <span class="flex items-center">
              <HeartIcon class="w-4 h-4 text-red-500 mr-1" />
              <span class="text-sm">{{ film.likes }}</span>
            </span>
            <span class="flex items-center">
              <MessageCircleIcon class="w-4 h-4 text-blue-500 mr-1" />
              <span class="text-sm">{{ film.comments }}</span>
            </span>
          </div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { StarIcon, HeartIcon, MessageCircleIcon, SearchIcon } from 'lucide-vue-next'

defineProps({
  films: Array,
  searchQuery: String,
  filterOption: String
})

defineEmits(['update:searchQuery', 'update:filterOption', 'select-film'])
</script>

<style scoped>
.book-container {
  perspective: 1000px;
}

.book {
  transform-style: preserve-3d;
  transform: rotateY(-30deg);
  transition: transform 0.5s;
}

.book:hover {
  transform: rotateY(0deg);
}

.book-cover {
  width: 225px;
  height: 300px;
  background-color: #f3d5b5;
  border: 1px solid #7c4a03;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  position: relative;
}

.book-title-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.book:hover .book-title-overlay {
  opacity: 1;
}

.book-spine {
  position: absolute;
  left: -15px;
  top: 0;
  width: 30px;
  height: 300px;
  background-color: #d4a373;
  border: 1px solid #7c4a03;
  transform: rotateY(-90deg);
  transform-origin: right;
}

.writing-mode-vertical {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  padding: 10px 2px;
}

.book-list-enter-active,
.book-list-leave-active {
  transition: all 0.5s ease;
}

.book-list-enter-from,
.book-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>