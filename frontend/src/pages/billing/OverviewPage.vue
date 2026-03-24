<script setup>
import { onMounted, ref } from "vue";

import client from "../../api/client";

const overview = ref({ line_item_count: 0, months: [], totals_by_currency: [], provider_breakdown: [] });
const logs = ref([]);
const lineItems = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

async function fetchData() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const [overviewRes, logsRes, itemsRes] = await Promise.all([
      client.get("/billing/overview"),
      client.get("/billing/collect-logs"),
      client.get("/billing/line-items", { params: { ordering: "-discounted_cost" } }),
    ]);
    overview.value = overviewRes.data.data || overview.value;
    logs.value = logsRes.data.data || [];
    lineItems.value = itemsRes.data.results || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "账单总览加载失败。";
  } finally {
    loading.value = false;
  }
}

async function collectBilling() {
  await client.post("/billing/collect", {});
  successMessage.value = "已触发模拟账单采集";
  await fetchData();
}

async function recollectBilling() {
  await client.post("/billing/recollect", {});
  successMessage.value = "已重跑模拟账单采集";
  await fetchData();
}

onMounted(fetchData);
</script>

<template>
  <section>
    <div v-if="errorMessage" class="rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">{{ errorMessage }}</div>
    <div v-if="successMessage" class="mb-4 rounded-3xl bg-emerald-50 px-6 py-4 text-sm text-emerald-700">{{ successMessage }}</div>
    <div class="mb-4 grid gap-4 md:grid-cols-4">
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">阿里云总费用</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">
          ¥ {{ Number(overview.totals_by_currency?.find((item) => item.currency === 'CNY')?.total_cost || 0).toFixed(2) }}
        </p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">AWS 总费用</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">
          $ {{ Number(overview.totals_by_currency?.find((item) => item.currency === 'USD')?.total_cost || 0).toFixed(2) }}
        </p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">账单明细</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ overview.line_item_count || 0 }}</p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">账单月份</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ overview.months?.[0] || "-" }}</p>
      </div>
    </div>

    <div class="mb-4 flex flex-col gap-3 rounded-3xl bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between">
      <div class="text-sm text-slate-500">账单采集日志与高成本明细</div>
      <div class="flex gap-3">
        <button class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm" @click="collectBilling">采集账单</button>
        <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white" @click="recollectBilling">重跑采集</button>
      </div>
    </div>

    <div class="mb-4 grid gap-4 lg:grid-cols-2">
      <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
        <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">云厂商费用分布</div>
        <table class="min-w-full text-left">
          <thead class="bg-slate-50 text-sm text-slate-500">
            <tr>
              <th class="px-6 py-4">Provider</th>
              <th class="px-6 py-4">币种</th>
              <th class="px-6 py-4">费用</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="3">加载中...</td></tr>
            <tr v-for="item in overview.provider_breakdown" :key="item.provider" class="border-t border-slate-100">
              <td class="px-6 py-4 font-medium uppercase">{{ item.provider }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.currency }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.currency === "USD" ? "$" : "¥" }} {{ Number(item.total_cost).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
        <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">采集日志</div>
        <table class="min-w-full text-left">
          <thead class="bg-slate-50 text-sm text-slate-500">
            <tr>
              <th class="px-6 py-4">任务</th>
              <th class="px-6 py-4">状态</th>
              <th class="px-6 py-4">结果</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="3">加载中...</td></tr>
            <tr v-for="item in logs" :key="item.id" class="border-t border-slate-100">
              <td class="px-6 py-4 font-medium">{{ item.name }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.status }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.result?.line_items || 0 }} 条</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
      <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">高成本明细</div>
      <table class="min-w-full text-left">
        <thead class="bg-slate-50 text-sm text-slate-500">
          <tr>
            <th class="px-6 py-4">资源</th>
            <th class="px-6 py-4">产品</th>
            <th class="px-6 py-4">环境</th>
            <th class="px-6 py-4">归一化产品</th>
            <th class="px-6 py-4">币种</th>
            <th class="px-6 py-4">费用</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="6">加载中...</td></tr>
          <tr v-for="item in lineItems" :key="item.id" class="border-t border-slate-100">
            <td class="px-6 py-4 font-medium">{{ item.resource_name || item.resource_id }}</td>
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
