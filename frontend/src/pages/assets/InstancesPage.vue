<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import client from "../../api/client";

const instances = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const providerFilter = ref("");
const statusFilter = ref("");
const jumpserverStatusFilter = ref("");
const keyword = ref("");
const sortKey = ref("instance_name");
const sortOrder = ref("asc");

async function fetchInstances() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const params = {};
    if (providerFilter.value) params.provider = providerFilter.value;
    if (statusFilter.value) params.status = statusFilter.value;
    if (jumpserverStatusFilter.value) params.jumpserver_sync_status = jumpserverStatusFilter.value;
    if (keyword.value) params.search = keyword.value;
    const { data } = await client.get("/assets/instances", { params });
    instances.value = data.results || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "主机加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchInstances);

const sortedInstances = computed(() => {
  const items = [...instances.value];
  items.sort((a, b) => {
    const left = a[sortKey.value] ?? "";
    const right = b[sortKey.value] ?? "";
    if (left === right) return 0;
    const compare = left > right ? 1 : -1;
    return sortOrder.value === "asc" ? compare : -compare;
  });
  return items;
});

function toggleSort(key) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
    return;
  }
  sortKey.value = key;
  sortOrder.value = "asc";
}

async function syncInstances() {
  await client.post("/assets/instances/sync", {});
  successMessage.value = "已触发模拟主机同步";
  await fetchInstances();
}

async function syncToJumpServer(instanceId) {
  await client.post(`/assets/instances/${instanceId}/sync-to-jumpserver`, {});
  successMessage.value = "已触发单台主机同步到 JumpServer";
  await fetchInstances();
}
</script>

<template>
  <section>
    <div v-if="errorMessage" class="rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">{{ errorMessage }}</div>
    <div v-if="successMessage" class="mb-4 rounded-3xl bg-emerald-50 px-6 py-4 text-sm text-emerald-700">{{ successMessage }}</div>

    <div class="mb-4 flex flex-col gap-3 rounded-3xl bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between">
      <div class="flex flex-wrap gap-3">
        <input v-model="keyword" class="rounded-xl border border-slate-200 px-3 py-2 text-sm" placeholder="搜索主机名 / IP" />
        <select v-model="providerFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部 Provider</option>
          <option value="aliyun">aliyun</option>
          <option value="aws">aws</option>
        </select>
        <select v-model="statusFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部状态</option>
          <option value="running">running</option>
          <option value="stopped">stopped</option>
        </select>
        <select v-model="jumpserverStatusFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部 JumpServer 状态</option>
          <option value="pending">pending</option>
          <option value="synced">synced</option>
          <option value="failed">failed</option>
        </select>
        <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white" @click="fetchInstances">筛选</button>
      </div>
      <button class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm" @click="syncInstances">同步主机</button>
    </div>

    <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
      <table class="min-w-full text-left">
        <thead class="bg-slate-50 text-sm text-slate-500">
          <tr>
            <th class="px-6 py-4"><button class="font-medium" @click="toggleSort('instance_name')">主机名</button></th>
            <th class="px-6 py-4"><button class="font-medium" @click="toggleSort('provider')">Provider</button></th>
            <th class="px-6 py-4"><button class="font-medium" @click="toggleSort('region')">区域</button></th>
            <th class="px-6 py-4">IP</th>
            <th class="px-6 py-4"><button class="font-medium" @click="toggleSort('status')">状态</button></th>
            <th class="px-6 py-4">JumpServer</th>
            <th class="px-6 py-4 text-right">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="7">加载中...</td></tr>
          <tr v-else-if="sortedInstances.length === 0" class="border-t border-slate-100"><td class="px-6 py-6 text-slate-500" colspan="7">当前没有主机资产。</td></tr>
          <tr v-for="item in sortedInstances" :key="item.id" class="border-t border-slate-100 transition hover:bg-slate-50/70">
            <td class="px-6 py-4 font-medium">{{ item.instance_name }}</td>
            <td class="px-6 py-4 uppercase text-slate-600">{{ item.provider }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.region }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.private_ip }} <span v-if="item.public_ip">/ {{ item.public_ip }}</span></td>
            <td class="px-6 py-4">
              <span class="rounded-full px-3 py-1 text-sm" :class="item.status === 'running' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'">
                {{ item.status }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex flex-col gap-2">
                <span class="inline-flex w-fit rounded-full px-3 py-1 text-sm" :class="item.jumpserver_sync_status === 'synced' ? 'bg-emerald-50 text-emerald-700' : item.jumpserver_sync_status === 'failed' ? 'bg-red-50 text-red-700' : 'bg-slate-100 text-slate-600'">
                  {{ item.jumpserver_sync_status }}
                </span>
                <span v-if="item.jumpserver_asset_id" class="text-xs text-slate-500">{{ item.jumpserver_asset_id }}</span>
              </div>
            </td>
            <td class="px-6 py-4 text-right">
              <div class="flex items-center justify-end gap-3">
                <button class="text-sm font-medium text-slate-500 underline-offset-4 hover:underline" @click="syncToJumpServer(item.id)">同步到 JumpServer</button>
                <RouterLink class="text-sm font-medium text-slate-700 underline-offset-4 hover:underline" :to="`/assets/instances/${item.id}`">查看详情</RouterLink>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
