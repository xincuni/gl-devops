<script setup>
import { onMounted, ref } from "vue";

import client from "../../api/client";

const items = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const providerFilter = ref("");
const currencyFilter = ref("");
const envFilter = ref("");
const productFilter = ref("");
const keyword = ref("");
const ordering = ref("-discounted_cost");

function buildParams() {
  const params = { ordering: ordering.value };
  if (providerFilter.value) params.provider = providerFilter.value;
  if (currencyFilter.value) params.currency = currencyFilter.value;
  if (envFilter.value) params.normalized_env = envFilter.value;
  if (productFilter.value) params.normalized_product = productFilter.value;
  if (keyword.value) params.search = keyword.value;
  return params;
}

async function fetchItems() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const { data } = await client.get("/billing/line-items", { params: buildParams() });
    items.value = data.results || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "账单明细加载失败。";
  } finally {
    loading.value = false;
  }
}

async function exportItems() {
  const response = await client.get("/billing/line-items/export", {
    params: buildParams(),
    responseType: "blob",
  });
  const blob = new Blob([response.data], { type: "text/csv;charset=utf-8;" });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "billing-line-items.csv";
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

onMounted(fetchItems);
</script>

<template>
  <section>
    <div v-if="errorMessage" class="mb-4 rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">{{ errorMessage }}</div>
    <div class="mb-4 flex flex-col gap-3 rounded-3xl bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between">
      <div class="flex flex-wrap gap-3">
        <input v-model="keyword" class="rounded-xl border border-slate-200 px-3 py-2 text-sm" placeholder="搜索资源 / 产品" />
        <select v-model="providerFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部 Provider</option>
          <option value="aliyun">aliyun</option>
          <option value="aws">aws</option>
        </select>
        <select v-model="currencyFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部币种</option>
          <option value="CNY">CNY</option>
          <option value="USD">USD</option>
        </select>
        <select v-model="envFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部 Env</option>
          <option value="prod">prod</option>
          <option value="staging">staging</option>
          <option value="shared">shared</option>
        </select>
        <select v-model="productFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部归一化产品</option>
          <option value="portal">portal</option>
          <option value="ops">ops</option>
          <option value="infra">infra</option>
        </select>
        <select v-model="ordering" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="-discounted_cost">费用从高到低</option>
          <option value="discounted_cost">费用从低到高</option>
          <option value="-billing_date">日期从新到旧</option>
          <option value="billing_date">日期从旧到新</option>
        </select>
        <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white" @click="fetchItems">筛选</button>
      </div>
      <button class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm" @click="exportItems">导出 CSV</button>
    </div>

    <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
      <table class="min-w-full text-left">
        <thead class="bg-slate-50 text-sm text-slate-500">
          <tr>
            <th class="px-6 py-4">日期</th>
            <th class="px-6 py-4">Provider</th>
            <th class="px-6 py-4">资源</th>
            <th class="px-6 py-4">产品</th>
            <th class="px-6 py-4">Env</th>
            <th class="px-6 py-4">归一化产品</th>
            <th class="px-6 py-4">币种</th>
            <th class="px-6 py-4">费用</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="8">加载中...</td></tr>
          <tr v-else-if="items.length === 0" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="8">当前没有账单明细。</td></tr>
          <tr v-for="item in items" :key="item.id" class="border-t border-slate-100 transition hover:bg-slate-50/70">
            <td class="px-6 py-4 text-slate-600">{{ item.billing_date }}</td>
            <td class="px-6 py-4 font-medium uppercase">{{ item.provider }}</td>
            <td class="px-6 py-4">
              <div class="font-medium">{{ item.resource_name || item.resource_id }}</div>
              <div class="text-xs text-slate-400">{{ item.resource_id }}</div>
            </td>
            <td class="px-6 py-4 text-slate-600">{{ item.product }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.normalized_env }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.normalized_product }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.currency }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.currency === "USD" ? "$" : "¥" }} {{ Number(item.discounted_cost).toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
