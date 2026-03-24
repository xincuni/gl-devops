<script setup>
import { onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";

import client from "../../api/client";

const route = useRoute();
const instance = ref(null);
const loading = ref(false);
const errorMessage = ref("");

async function fetchDetail() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const { data } = await client.get(`/assets/instances/${route.params.id}`);
    instance.value = data;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "主机详情加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchDetail);
</script>

<template>
  <section>
    <div v-if="errorMessage" class="rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">{{ errorMessage }}</div>
    <div v-else-if="loading" class="rounded-3xl bg-white p-6 shadow-sm text-slate-500">加载中...</div>
    <div v-else-if="instance" class="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
      <article class="rounded-3xl bg-white p-6 shadow-sm">
        <div class="mb-4">
          <RouterLink class="text-sm font-medium text-slate-500 underline-offset-4 hover:underline" to="/assets/instances">返回主机列表</RouterLink>
        </div>
        <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Instance Detail</p>
        <h3 class="mt-2 text-2xl font-semibold">{{ instance.instance_name }}</h3>
        <div class="mt-6 grid gap-4 md:grid-cols-2">
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">实例 ID</p><p class="mt-2 font-medium text-slate-900">{{ instance.instance_id }}</p></div>
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">Provider</p><p class="mt-2 font-medium text-slate-900">{{ instance.provider }}</p></div>
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">区域</p><p class="mt-2 font-medium text-slate-900">{{ instance.region }}</p></div>
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">状态</p><p class="mt-2 font-medium text-slate-900">{{ instance.status }}</p></div>
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">私网 IP</p><p class="mt-2 font-medium text-slate-900">{{ instance.private_ip }}</p></div>
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">公网 IP</p><p class="mt-2 font-medium text-slate-900">{{ instance.public_ip || "-" }}</p></div>
        </div>
      </article>
      <article class="rounded-3xl bg-white p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Tags</p>
        <pre class="mt-4 overflow-auto rounded-xl bg-slate-50 p-4 text-xs text-slate-600">{{ JSON.stringify(instance.tags_json || {}, null, 2) }}</pre>
      </article>
    </div>
  </section>
</template>
