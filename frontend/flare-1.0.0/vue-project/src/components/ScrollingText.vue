<template>
  <div class="overflow-hidden whitespace-nowrap mb-16 border-y py-4">
    <div class="animate-scroll-text inline-block">
      <!-- <span class="text-lg">— Film of the Day — {{ currentDate }} — Film of the Day — {{ currentDate }} —&nbsp;</span> -->
      <!-- <span class="text-lg">ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ영화를 감상한 순간들을 기록하며 나만의 기억 조각을 완성하세요.&nbsp;</span> -->
      <span class="text-lg" style="font-style:italic; color: gray;">ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ- Record your movie moments to create your own personalized memory sculpture -&nbsp;</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const currentDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
})
</script>

<style scoped>
.animate-scroll-text {
  animation: scroll 20s linear infinite;
}

@keyframes scroll {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}
</style>