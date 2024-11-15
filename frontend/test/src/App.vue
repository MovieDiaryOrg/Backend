<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink :to="{name: 'user'}">Login</RouterLink>
        <RouterLink :to="{name: 'signup'}">Sign Up</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
  
</template>

<style scoped>
</style>
