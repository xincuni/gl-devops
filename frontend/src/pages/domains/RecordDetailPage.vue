<script setup>
import { onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";

import client from "../../api/client";

const route = useRoute();
const loading = ref(false);
const errorMessage = ref("");
const record = ref(null);

async function fetchDetail() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const { data } = await client.get(`/domains/records/${route.params.id}`);
    record.value = data;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "记录详情加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchDetail);
</script>

<template>
  <section>
    <div v-if="errorMessage" class="rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">
      {{ errorMessage }}
    </div>

    <div v-else-if="loading" class="rounded-3xl bg-white p-6 shadow-sm text-slate-500">加载中...</div>

    <div v-else-if="record" class="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
      <article class="rounded-3xl bg-white p-6 shadow-sm">
        <div class="mb-4">
          <RouterLink class="text-sm font-medium text-slate-500 underline-offset-4 hover:underline" :to="`/domains/records?zone=${record.zone}&zone_name=${encodeURIComponent(record.zone_name)}`">
            返回记录列表
          </RouterLink>
        </div>
        <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Record Detail</p>
        <h3 class="mt-2 text-2xl font-semibold">{{ record.name }}.{{ record.zone_name }}</h3>
        <div class="mt-6 grid gap-4 md:grid-cols-2">
          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-400">类型</p>
            <p class="mt-2 font-medium text-slate-900">{{ record.type }}</p>
          </div>
          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-400">值</p>
            <p class="mt-2 font-medium text-slate-900 break-all">{{ record.value }}</p>
          </div>
          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-400">TTL</p>
            <p class="mt-2 font-medium text-slate-900">{{ record.ttl }}</p>
          </div>
          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-400">状态</p>
            <p class="mt-2 font-medium text-slate-900">{{ record.status }}</p>
          </div>
        </div>
      </article>

      <article class="rounded-3xl bg-white p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Recent Audits</p>
        <div class="mt-4 space-y-3">
          <div v-if="!record.audits?.length" class="text-sm text-slate-500">暂无审计记录。</div>
          <div v-for="item in record.audits" :key="item.id" class="rounded-2xl border border-slate-100 p-4">
            <p class="font-medium text-slate-900">{{ item.action }}</p>
            <p class="mt-1 text-xs text-slate-500">
              操作人：{{ item.operator || "system" }} · {{ item.created_at }}
            </p>
            <pre class="mt-3 overflow-auto rounded-xl bg-slate-50 p-3 text-xs text-slate-600">{{ JSON.stringify(item.detail || {}, null, 2) }}</pre>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>
