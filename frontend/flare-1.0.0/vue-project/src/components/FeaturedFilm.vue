<!-- components/FeaturedFilm.vue -->


<template>
  <section>
    <h2 class="text-2xl font-bold mb-6">오늘의 영화</h2>
    <div class="bg-gray-100 p-6 rounded-2xl">
      <img 
        :src="film.image" 
        :alt="film.title"
        class="w-full h-[500px] object-cover rounded-lg mb-4"
      />
      <h3 class="text-xl font-bold mb-2">{{ film.title }}</h3>
      <p class="text-gray-600 mb-2">장르: {{ film.genre }}</p>
      <p class="text-gray-600">{{ film.description }}</p>
    </div>
  </section>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  film: {
    type: Object,
    required: true
  }
})
</script>