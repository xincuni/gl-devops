<script setup>
import { onMounted, ref } from "vue";

import client from "../../api/client";

const tasks = ref([]);
const loading = ref(false);
const errorMessage = ref("");

async function fetchTasks() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const { data } = await client.get("/tasks");
    tasks.value = data.results || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "任务加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchTasks);
</script>

<template>
  <section>
    <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Tasks</p>
    <h2 class="mt-2 text-3xl font-semibold">任务中心</h2>

    <div v-if="errorMessage" class="mt-8 rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">
      {{ errorMessage }}
    </div>

    <div class="mt-8 grid gap-4">
      <article v-if="loading" class="rounded-3xl bg-white p-6 shadow-sm text-slate-500">
        加载中...
      </article>
      <article v-else-if="tasks.length === 0" class="rounded-3xl bg-white p-6 shadow-sm text-slate-500">
        当前还没有任务记录。
      </article>
      <article v-for="task in tasks" :key="task.id" class="rounded-3xl bg-white p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs uppercase tracking-[0.25em] text-slate-400">Task #{{ task.id }}</p>
            <h3 class="mt-2 text-lg font-semibold">{{ task.name }}</h3>
          </div>
          <span class="rounded-full px-3 py-1 text-sm" :class="task.status === 'success' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'">
            {{ task.status }}
          </span>
        </div>
      </article>
    </div>
  </section>
</template>
