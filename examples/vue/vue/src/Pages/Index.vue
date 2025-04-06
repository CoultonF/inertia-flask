<script setup>
import HelloWorld from '@/components/HelloWorld.vue'
import vueLogo from '@/assets/vue.svg'
import { Link } from '@inertiajs/vue3'

const props = defineProps({
  data: Number
})
</script>

<template>
  <div>
    <a href="https://vite.dev" target="_blank">
      <img src ="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img :src="vueLogo" class="logo vue" alt="Vue logo" />
    </a>
    <a href="https://inertiajs.com" target="_blank">
      <img src="/inertia.png" class="logo inertia" alt="Inertia logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue + Inertia" :initialCount="data" />
  
  <div class="spa-test">
    <h2>SPA Navigation Test</h2>
    <Link href="/about" class="nav-link">Go to About Page</Link>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
.logo.inertia:hover {
  filter: drop-shadow(0 0 2em #9747e8aa);
}

.spa-test {
  margin-top: 2rem;
  padding: 1.5rem;
  border-radius: 8px;
  background-color: #f9f9f9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.nav-link {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
</style>
