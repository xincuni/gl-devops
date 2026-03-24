<script setup>
import { computed, onMounted, ref } from "vue";

import client from "../../api/client";

const logs = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const statusFilter = ref("");

const successCount = computed(() => logs.value.filter((item) => item.status === "success").length);

async function fetchLogs() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const params = {};
    if (statusFilter.value) params.status = statusFilter.value;
    const { data } = await client.get("/jumpserver/sync-logs", { params });
    logs.value = data.results || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "JumpServer 同步记录加载失败。";
  } finally {
    loading.value = false;
  }
}

async function triggerSync() {
  await client.post("/jumpserver/sync", {});
  successMessage.value = "已触发模拟 JumpServer 同步";
  await fetchLogs();
}

onMounted(fetchLogs);
</script>

<template>
  <section>
    <div v-if="errorMessage" class="rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">{{ errorMessage }}</div>
    <div v-if="successMessage" class="mb-4 rounded-3xl bg-emerald-50 px-6 py-4 text-sm text-emerald-700">{{ successMessage }}</div>
    <div class="mb-4 grid gap-4 md:grid-cols-3">
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">同步记录</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ logs.length }}</p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">成功数量</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ successCount }}</p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">失败数量</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ logs.length - successCount }}</p>
      </div>
    </div>
    <div class="mb-4 flex flex-col gap-3 rounded-3xl bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between">
      <div class="flex flex-wrap gap-3">
        <select v-model="statusFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部状态</option>
          <option value="success">success</option>
          <option value="failed">failed</option>
        </select>
        <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white" @click="fetchLogs">筛选</button>
      </div>
      <button class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm" @click="triggerSync">同步到 JumpServer</button>
    </div>
    <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
      <table class="min-w-full text-left">
        <thead class="bg-slate-50 text-sm text-slate-500">
          <tr>
            <th class="px-6 py-4">主机</th>
            <th class="px-6 py-4">规则</th>
            <th class="px-6 py-4">JumpServer 资产 ID</th>
            <th class="px-6 py-4">状态</th>
            <th class="px-6 py-4">时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="5">加载中...</td></tr>
          <tr v-else-if="logs.length === 0" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="5">当前没有同步记录。</td></tr>
          <tr v-for="item in logs" :key="item.id" class="border-t border-slate-100 transition hover:bg-slate-50/70">
            <td class="px-6 py-4 font-medium">{{ item.instance_name }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.rule_name || "-" }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.jumpserver_asset_id || "-" }}</td>
            <td class="px-6 py-4">
              <span class="rounded-full px-3 py-1 text-sm" :class="item.status === 'success' ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'">{{ item.status }}</span>
            </td>
            <td class="px-6 py-4 text-slate-600">{{ new Date(item.synced_at).toLocaleString("zh-CN") }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
