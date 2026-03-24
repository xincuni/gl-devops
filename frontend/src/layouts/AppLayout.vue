<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

const router = useRouter();
const authStore = useAuthStore();
const username = computed(() => authStore.user?.username || "admin");

async function handleLogout() {
  await authStore.logout();
  router.push("/login");
}
</script>

<template>
  <div class="min-h-screen bg-mist text-ink">
    <div class="grid min-h-screen md:grid-cols-[220px_1fr]">
      <aside class="bg-ink px-6 py-8 text-white">
        <div class="mb-8">
          <p class="text-xs uppercase tracking-[0.3em] text-teal-200">GL DevOps</p>
          <h1 class="mt-2 text-2xl font-semibold">Iteration 1</h1>
        </div>
        <nav class="space-y-2">
          <RouterLink class="block rounded px-3 py-2 hover:bg-white/10" to="/accounts">云账号</RouterLink>
          <RouterLink class="block rounded px-3 py-2 hover:bg-white/10" to="/tasks">任务中心</RouterLink>
        </nav>
      </aside>
      <main class="p-6 md:p-10">
        <div class="mb-6 flex items-center justify-end">
          <div class="flex items-center gap-3 rounded-full bg-white px-4 py-2 shadow-sm">
            <span class="text-sm text-slate-500">{{ username }}</span>
            <button class="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700" @click="handleLogout">退出</button>
          </div>
        </div>
        <router-view />
      </main>
    </div>
  </div>
</template>
