<script setup>
import { onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";

import client from "../../api/client";

const route = useRoute();
const asset = ref(null);
const loading = ref(false);
const errorMessage = ref("");

async function fetchDetail() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const { data } = await client.get(`/cmdb/assets/${route.params.id}`);
    asset.value = data;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "CMDB 详情加载失败。";
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
    <div v-else-if="asset" class="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
      <article class="rounded-3xl bg-white p-6 shadow-sm">
        <div class="mb-4"><RouterLink class="text-sm font-medium text-slate-500 underline-offset-4 hover:underline" to="/cmdb/assets">返回 CMDB 列表</RouterLink></div>
        <p class="text-sm uppercase tracking-[0.3em] text-slate-500">CMDB Asset</p>
        <h3 class="mt-2 text-2xl font-semibold">{{ asset.name }}</h3>
        <div class="mt-6 grid gap-4 md:grid-cols-2">
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">类型</p><p class="mt-2 font-medium text-slate-900">{{ asset.asset_type }}</p></div>
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">来源</p><p class="mt-2 font-medium text-slate-900">{{ asset.source }}</p></div>
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">状态</p><p class="mt-2 font-medium text-slate-900">{{ asset.status }}</p></div>
          <div class="rounded-2xl bg-slate-50 p-4"><p class="text-xs uppercase tracking-[0.2em] text-slate-400">来源引用</p><p class="mt-2 font-medium text-slate-900">{{ asset.source_ref }}</p></div>
        </div>
      </article>
      <article class="rounded-3xl bg-white p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Metadata</p>
        <pre class="mt-4 overflow-auto rounded-xl bg-slate-50 p-4 text-xs text-slate-600">{{ JSON.stringify(asset.metadata || {}, null, 2) }}</pre>
        <p class="mt-6 text-sm uppercase tracking-[0.3em] text-slate-500">Labels</p>
        <pre class="mt-4 overflow-auto rounded-xl bg-slate-50 p-4 text-xs text-slate-600">{{ JSON.stringify(asset.labels || {}, null, 2) }}</pre>
      </article>
    </div>
  </section>
</template>
