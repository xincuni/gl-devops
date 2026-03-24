<script setup>
import { onMounted, ref } from "vue";

import client from "../../api/client";

const accounts = ref([]);
const loading = ref(false);
const errorMessage = ref("");

async function fetchAccounts() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const { data } = await client.get("/accounts");
    accounts.value = data.results || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "云账号加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchAccounts);
</script>

<template>
  <section>
    <div class="flex items-end justify-between">
      <div>
        <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Accounts</p>
        <h2 class="mt-2 text-3xl font-semibold">云账号管理</h2>
      </div>
      <button class="rounded-2xl bg-signal px-4 py-3 font-medium text-white">新增账号</button>
    </div>

    <div v-if="errorMessage" class="mt-8 rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">
      {{ errorMessage }}
    </div>

    <div class="mt-8 overflow-hidden rounded-3xl bg-white shadow-sm">
      <table class="min-w-full text-left">
        <thead class="bg-slate-50 text-sm text-slate-500">
          <tr>
            <th class="px-6 py-4">名称</th>
            <th class="px-6 py-4">Provider</th>
            <th class="px-6 py-4">状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100">
            <td class="px-6 py-6 text-slate-500" colspan="3">加载中...</td>
          </tr>
          <tr v-else-if="accounts.length === 0" class="border-t border-slate-100">
            <td class="px-6 py-6 text-slate-500" colspan="3">当前还没有云账号。</td>
          </tr>
          <tr v-for="item in accounts" :key="item.id" class="border-t border-slate-100">
            <td class="px-6 py-4 font-medium">{{ item.name }}</td>
            <td class="px-6 py-4 uppercase text-slate-600">{{ item.provider }}</td>
            <td class="px-6 py-4">
              <span class="rounded-full bg-emerald-50 px-3 py-1 text-sm text-emerald-700">{{ item.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
