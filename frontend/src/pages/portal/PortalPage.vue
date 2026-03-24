<script setup>
import { onMounted, ref } from "vue";

import client from "../../api/client";

const summary = ref(null);
const recentTasks = ref([]);
const alerts = ref([]);
const loading = ref(false);
const errorMessage = ref("");

async function fetchPortal() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const [summaryRes, tasksRes, alertsRes] = await Promise.all([
      client.get("/portal/summary"),
      client.get("/portal/recent-tasks"),
      client.get("/portal/alerts"),
    ]);
    summary.value = summaryRes.data.data;
    recentTasks.value = tasksRes.data.data || [];
    alerts.value = alertsRes.data.data || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "首页数据加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchPortal);
</script>

<template>
  <section>
    <div class="mb-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Portal</p>
      <h2 class="mt-2 text-3xl font-semibold text-slate-900">运维总览</h2>
      <p class="mt-3 text-sm text-slate-500">账号、DNS、主机、JumpServer、账单和任务的统一看板。</p>
    </div>

    <div v-if="errorMessage" class="mb-4 rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">{{ errorMessage }}</div>

    <div class="mb-4 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">云账号</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ summary?.accounts?.total || 0 }}</p>
        <p class="mt-2 text-sm text-slate-500">活跃 {{ summary?.accounts?.active || 0 }}</p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">DNS</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ summary?.domains?.zones || 0 }}</p>
        <p class="mt-2 text-sm text-slate-500">记录 {{ summary?.domains?.records || 0 }}</p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">云主机</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ summary?.instances?.total || 0 }}</p>
        <p class="mt-2 text-sm text-slate-500">运行 {{ summary?.instances?.running || 0 }} / 已纳管 {{ summary?.instances?.jumpserver_synced || 0 }}</p>
      </div>
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">任务</p>
        <p class="mt-2 text-3xl font-semibold text-slate-900">{{ summary?.tasks?.total || 0 }}</p>
        <p class="mt-2 text-sm text-slate-500">失败 {{ summary?.tasks?.failed || 0 }} / 等待 {{ summary?.tasks?.pending || 0 }}</p>
      </div>
    </div>

    <div class="mb-4 grid gap-4 lg:grid-cols-2">
      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">费用概览</p>
        <div class="mt-4 grid gap-4 md:grid-cols-2">
          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-sm text-slate-500">阿里云</p>
            <p class="mt-2 text-2xl font-semibold text-slate-900">
              ¥ {{ Number(summary?.billing?.totals_by_currency?.find((item) => item.currency === "CNY")?.total_cost || 0).toFixed(2) }}
            </p>
          </div>
          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-sm text-slate-500">AWS</p>
            <p class="mt-2 text-2xl font-semibold text-slate-900">
              $ {{ Number(summary?.billing?.totals_by_currency?.find((item) => item.currency === "USD")?.total_cost || 0).toFixed(2) }}
            </p>
          </div>
        </div>
        <p class="mt-4 text-sm text-slate-500">账单明细 {{ summary?.billing?.line_item_count || 0 }} 条，月份 {{ summary?.billing?.months?.[0] || "-" }}</p>
      </div>

      <div class="rounded-3xl bg-white p-5 shadow-sm">
        <p class="text-sm text-slate-500">告警与提示</p>
        <div class="mt-4 space-y-3">
          <div v-if="loading" class="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-500">加载中...</div>
          <div v-for="item in alerts" :key="item.title" class="rounded-2xl px-4 py-3 text-sm"
            :class="item.level === 'high' ? 'bg-red-50 text-red-700' : item.level === 'medium' ? 'bg-amber-50 text-amber-700' : 'bg-slate-50 text-slate-600'">
            <div class="font-medium">{{ item.title }}</div>
            <div class="mt-1 break-all">{{ Array.isArray(item.value) ? JSON.stringify(item.value) : item.value }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid gap-4 lg:grid-cols-2">
      <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
        <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">最近任务</div>
        <table class="min-w-full text-left">
          <thead class="bg-slate-50 text-sm text-slate-500">
            <tr>
              <th class="px-6 py-4">任务</th>
              <th class="px-6 py-4">类型</th>
              <th class="px-6 py-4">状态</th>
              <th class="px-6 py-4">操作人</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="4">加载中...</td></tr>
            <tr v-for="item in recentTasks" :key="item.id" class="border-t border-slate-100">
              <td class="px-6 py-4 font-medium">{{ item.name }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.task_type }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.status }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.created_by__username || "-" }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
        <div class="border-b border-slate-100 px-6 py-4 text-sm font-medium text-slate-900">厂商费用分布</div>
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
            <tr v-for="item in summary?.billing?.provider_breakdown || []" :key="`${item.provider}-${item.currency}`" class="border-t border-slate-100">
              <td class="px-6 py-4 font-medium uppercase">{{ item.provider }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.currency }}</td>
              <td class="px-6 py-4 text-slate-600">{{ item.currency === "USD" ? "$" : "¥" }} {{ Number(item.total_cost).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>
