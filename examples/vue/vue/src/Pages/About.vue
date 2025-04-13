<script setup>
import { Link } from '@inertiajs/vue3'

// Props received from the server
defineProps({
  version: String
})
</script>

<template>
  <div class="about-page">
    <h1>About Page</h1>
    
    <div class="card">
      <h2>App Version</h2>
      <p>{{ version }}</p>
    </div>
    
    <div class="navigation">
      <Link href="/" class="link">Back to Home</Link>
    </div>
  </div>
</template>

<style scoped>
.about-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.card {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.navigation {
  margin-top: 2rem;
}

.link {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
</style>
