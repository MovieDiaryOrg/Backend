<template>
  <div class="bg-white p-4 rounded-lg shadow-md">
    <img 
      :src="image || '/placeholder.svg?height=200&width=200'" 
      :alt="title"
      class="w-full aspect-square object-cover rounded-lg mb-3"
    />
    <h3 class="font-bold mb-1">{{ title }}</h3>
    <p class="text-sm text-gray-600 mb-2">작성자: {{ author }}</p>
    <div class="flex justify-between items-center">
      <span class="flex items-center">
        <HeartIcon class="w-4 h-4 mr-1 text-red-500" />
        {{ likes }}
      </span>
      <span class="flex items-center">
        <template v-for="i in 5" :key="i">
          <StarIcon v-if="i <= Math.floor(safeRating)" class="w-4 h-4 text-yellow-400" />
          <StarHalfIcon v-else-if="i - 0.5 <= safeRating" class="w-4 h-4 text-yellow-400" />
          <StarIcon v-else class="w-4 h-4 text-gray-300" />
        </template>
        <span class="ml-1 text-sm">{{ displayRating }}</span>
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { HeartIcon, StarIcon, StarHalfIcon } from 'lucide-vue-next'

const props = defineProps({
  image: {
    type: String,
    default: '/placeholder.svg?height=200&width=200'
  },
  title: {
    type: String,
    required: true
  },
  author: {
    type: String,
    required: true
  },
  rating: {
    type: Number,
    default: 0
  },
  likes: {
    type: Number,
    default: 0
  }
})

const safeRating = computed(() => {
  const rating = Number(props.rating)
  return isNaN(rating) ? 0 : Math.max(0, Math.min(5, rating))
})

const displayRating = computed(() => {
  return safeRating.value.toFixed(1)
})
</script>