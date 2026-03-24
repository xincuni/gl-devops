<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import client from "../../api/client";

const assets = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const typeFilter = ref("");
const sourceFilter = ref("");
const keyword = ref("");
const ordering = ref("asset_type");

async function fetchAssets() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const params = {};
    if (typeFilter.value) params.asset_type = typeFilter.value;
    if (sourceFilter.value) params.source = sourceFilter.value;
    if (keyword.value) params.search = keyword.value;
    if (ordering.value) params.ordering = ordering.value;
    const { data } = await client.get("/cmdb/assets", { params });
    assets.value = data.results || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "CMDB 资产加载失败。";
  } finally {
    loading.value = false;
  }
}

async function syncCMDB() {
  await client.post("/cmdb/sync", {});
  successMessage.value = "已触发 CMDB 资产同步";
  await fetchAssets();
}

onMounted(fetchAssets);

const groupedCount = computed(() => assets.value.length);
const groupedAssets = computed(() => {
  return assets.value.reduce((accumulator, item) => {
    const key = item.asset_type;
    accumulator[key] = accumulator[key] || 0;
    accumulator[key] += 1;
    return accumulator;
  }, {});
});
</script>

<template>
  <section>
    <div v-if="errorMessage" class="rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">{{ errorMessage }}</div>
    <div v-if="successMessage" class="mb-4 rounded-3xl bg-emerald-50 px-6 py-4 text-sm text-emerald-700">{{ successMessage }}</div>
    <div class="mb-4 grid gap-4 md:grid-cols-4">
      <div v-for="(count, type) in groupedAssets" :key="type" class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm uppercase tracking-[0.2em] text-slate-500">{{ type }}</p>
        <p class="mt-2 text-2xl font-semibold text-slate-900">{{ count }}</p>
      </div>
    </div>
    <div class="mb-4 flex flex-col gap-3 rounded-3xl bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between">
      <div class="flex items-center gap-3">
        <input v-model="keyword" class="rounded-xl border border-slate-200 px-3 py-2 text-sm" placeholder="搜索名称 / 来源引用" />
        <select v-model="typeFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部资产类型</option>
          <option value="cloud_account">cloud_account</option>
          <option value="cloud_instance">cloud_instance</option>
          <option value="dns_zone">dns_zone</option>
          <option value="dns_record">dns_record</option>
        </select>
        <select v-model="sourceFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部来源</option>
          <option value="aliyun">aliyun</option>
          <option value="aws">aws</option>
          <option value="cloudflare">cloudflare</option>
        </select>
        <select v-model="ordering" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="asset_type">按类型排序</option>
          <option value="name">按名称排序</option>
          <option value="-last_synced_at">按同步时间排序</option>
        </select>
        <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white" @click="fetchAssets">筛选</button>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-sm text-slate-500">共 {{ groupedCount }} 条资产</span>
        <button class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm" @click="syncCMDB">同步 CMDB</button>
      </div>
    </div>
    <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
      <table class="min-w-full text-left">
        <thead class="bg-slate-50 text-sm text-slate-500">
          <tr>
            <th class="px-6 py-4">名称</th>
            <th class="px-6 py-4">类型</th>
            <th class="px-6 py-4">来源</th>
            <th class="px-6 py-4">状态</th>
            <th class="px-6 py-4 text-right">详情</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="5">加载中...</td></tr>
          <tr v-else-if="assets.length === 0" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="5">当前没有 CMDB 资产。</td></tr>
          <tr v-for="item in assets" :key="item.id" class="border-t border-slate-100 transition hover:bg-slate-50/70">
            <td class="px-6 py-4 font-medium">{{ item.name }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.asset_type }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.source }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.status }}</td>
            <td class="px-6 py-4 text-right"><RouterLink class="text-sm font-medium text-slate-700 underline-offset-4 hover:underline" :to="`/cmdb/assets/${item.id}`">查看详情</RouterLink></td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
