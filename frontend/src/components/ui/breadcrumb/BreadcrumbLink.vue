<script setup>
import { RouterLink } from "vue-router";

defineProps({
  to: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <RouterLink v-if="to" :to="to" class="transition hover:text-slate-900">
    <slot />
  </RouterLink>
  <span v-else>
    <slot />
  </span>
</template>
