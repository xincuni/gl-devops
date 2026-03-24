<script setup>
import { onMounted, ref } from "vue";

import client from "../../api/client";

const byEnv = ref([]);
const byProduct = ref([]);
const byAccount = ref([]);
const byResource = ref([]);
const trend = ref([]);
const loading = ref(false);
const errorMessage = ref("");

async function fetchAnalysis() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const [envRes, productRes, accountRes, resourceRes, trendRes] = await Promise.all([
      client.get("/billing/analysis/by-env"),
      client.get("/billing/analysis/by-product"),
      client.get("/billing/analysis/by-account"),
      client.get("/billing/analysis/by-resource"),
      client.get("/billing/analysis/trend"),
    ]);
    byEnv.value = envRes.data.data || [];
    byProduct.value = productRes.data.data || [];
    byAccount.value = accountRes.data.data || [];
    byResource.value = resourceRes.data.data || [];
    trend.value = trendRes.data.data || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "费用分析加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchAnalysis);
</script>

<template>
  <section>
    <div v-if="errorMessage" class="rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">{{ errorMessage }}</div>
    <div class="mb-4 grid gap-4 lg:grid-cols-2">
      <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
        <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">按 Env 分析</div>
        <table class="min-w-full text-left">
          <thead class="bg-slate-50 text-sm text-slate-500"><tr><th class="px-6 py-4">Env</th><th class="px-6 py-4">费用</th></tr></thead>
          <tbody>
            <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="2">加载中...</td></tr>
            <tr v-for="item in byEnv" :key="`${item.currency}-${item.env}`" class="border-t border-slate-100"><td class="px-6 py-4 font-medium">{{ item.env }} <span class="ml-2 text-xs text-slate-400">({{ item.currency }})</span></td><td class="px-6 py-4 text-slate-600">{{ item.currency === "USD" ? "$" : "¥" }} {{ Number(item.total_cost).toFixed(2) }}</td></tr>
          </tbody>
        </table>
      </div>
      <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
        <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">按 Product 分析</div>
        <table class="min-w-full text-left">
          <thead class="bg-slate-50 text-sm text-slate-500"><tr><th class="px-6 py-4">Product</th><th class="px-6 py-4">费用</th></tr></thead>
          <tbody>
            <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="2">加载中...</td></tr>
            <tr v-for="item in byProduct" :key="`${item.currency}-${item.product}`" class="border-t border-slate-100"><td class="px-6 py-4 font-medium">{{ item.product }} <span class="ml-2 text-xs text-slate-400">({{ item.currency }})</span></td><td class="px-6 py-4 text-slate-600">{{ item.currency === "USD" ? "$" : "¥" }} {{ Number(item.total_cost).toFixed(2) }}</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="mb-4 grid gap-4 lg:grid-cols-2">
      <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
        <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">按账号分析</div>
        <table class="min-w-full text-left">
          <thead class="bg-slate-50 text-sm text-slate-500"><tr><th class="px-6 py-4">账号</th><th class="px-6 py-4">Provider</th><th class="px-6 py-4">币种</th><th class="px-6 py-4">费用</th></tr></thead>
          <tbody>
            <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="4">加载中...</td></tr>
            <tr v-for="item in byAccount" :key="`${item.currency}-${item.provider}-${item.account_name}`" class="border-t border-slate-100">
              <td class="px-6 py-4 font-medium">{{ item.account_name }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.provider }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.currency }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.currency === "USD" ? "$" : "¥" }} {{ Number(item.total_cost).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
        <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">按日期趋势</div>
        <table class="min-w-full text-left">
          <thead class="bg-slate-50 text-sm text-slate-500"><tr><th class="px-6 py-4">日期</th><th class="px-6 py-4">费用</th></tr></thead>
          <tbody>
            <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="2">加载中...</td></tr>
            <tr v-for="item in trend" :key="`${item.date}-${item.currency}`" class="border-t border-slate-100"><td class="px-6 py-4 font-medium">{{ item.date }} <span class="ml-2 text-xs text-slate-400">({{ item.currency }})</span></td><td class="px-6 py-4 text-slate-600">{{ item.currency === "USD" ? "$" : "¥" }} {{ Number(item.total_cost).toFixed(2) }}</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
      <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">高成本资源</div>
      <table class="min-w-full text-left">
          <thead class="bg-slate-50 text-sm text-slate-500"><tr><th class="px-6 py-4">资源</th><th class="px-6 py-4">产品</th><th class="px-6 py-4">币种</th><th class="px-6 py-4">费用</th></tr></thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="4">加载中...</td></tr>
          <tr v-for="item in byResource" :key="item.resource_id" class="border-t border-slate-100">
            <td class="px-6 py-4 font-medium">{{ item.resource_name || item.resource_id }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.product }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.currency }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.currency === "USD" ? "$" : "¥" }} {{ Number(item.total_cost).toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
