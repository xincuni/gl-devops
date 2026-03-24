<script setup>
import { computed, onMounted, ref } from "vue";

import client from "../../api/client";

const rules = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const statusFilter = ref("");
const providerFilter = ref("");

const activeCount = computed(() => rules.value.filter((item) => item.status === "active").length);

async function fetchRules() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const params = {};
    if (statusFilter.value) params.status = statusFilter.value;
    if (providerFilter.value) params.provider = providerFilter.value;
    const { data } = await client.get("/jumpserver/rules", { params });
    rules.value = data.results || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "JumpServer 规则加载失败。";
  } finally {
    loading.value = false;
  }
}

async function ensureRule() {
  await client.post("/jumpserver/rules", {
    name: `规则 ${Date.now()}`,
    provider: providerFilter.value || "",
    region: "",
    env: "",
    node_path: "/Default/Cloud",
    platform: "linux",
    status: "active",
    priority: 100,
    extra_config: { created_from: "frontend_demo" },
  });
  successMessage.value = "已创建一条模拟规则";
  await fetchRules();
}

onMounted(fetchRules);
</script>

<template>
  <section>
    <div v-if="errorMessage" class="rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">{{ errorMessage }}</div>
    <div v-if="successMessage" class="mb-4 rounded-3xl bg-emerald-50 px-6 py-4 text-sm text-emerald-700">{{ successMessage }}</div>
    <div class="mb-4 grid gap-4 md:grid-cols-3">
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">规则总数</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ rules.length }}</p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">生效规则</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ activeCount }}</p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">默认节点</p>
        <p class="mt-2 text-lg font-semibold text-slate-900">/Default/Cloud</p>
      </div>
    </div>
    <div class="mb-4 flex flex-col gap-3 rounded-3xl bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between">
      <div class="flex flex-wrap gap-3">
        <select v-model="statusFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部状态</option>
          <option value="active">active</option>
          <option value="disabled">disabled</option>
        </select>
        <select v-model="providerFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部 Provider</option>
          <option value="aliyun">aliyun</option>
          <option value="aws">aws</option>
        </select>
        <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white" @click="fetchRules">筛选</button>
      </div>
      <button class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm" @click="ensureRule">新增模拟规则</button>
    </div>
    <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
      <table class="min-w-full text-left">
        <thead class="bg-slate-50 text-sm text-slate-500">
          <tr>
            <th class="px-6 py-4">规则名称</th>
            <th class="px-6 py-4">Provider</th>
            <th class="px-6 py-4">环境</th>
            <th class="px-6 py-4">节点路径</th>
            <th class="px-6 py-4">优先级</th>
            <th class="px-6 py-4">状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="6">加载中...</td></tr>
          <tr v-else-if="rules.length === 0" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="6">当前没有 JumpServer 规则。</td></tr>
          <tr v-for="item in rules" :key="item.id" class="border-t border-slate-100 transition hover:bg-slate-50/70">
            <td class="px-6 py-4 font-medium">{{ item.name }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.provider || "-" }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.env || "-" }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.node_path }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.priority }}</td>
            <td class="px-6 py-4">
              <span class="rounded-full px-3 py-1 text-sm" :class="item.status === 'active' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'">{{ item.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
