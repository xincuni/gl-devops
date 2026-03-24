<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import client from "../../api/client";

const zones = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const syncingZoneId = ref(null);
const sortKey = ref("zone_name");
const sortOrder = ref("asc");

async function fetchZones() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const { data } = await client.get("/domains/zones");
    zones.value = data.results || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "域名加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchZones);

const sortedZones = computed(() => {
  const items = [...zones.value];
  items.sort((left, right) => {
    const leftValue = left[sortKey.value] ?? "";
    const rightValue = right[sortKey.value] ?? "";
    if (leftValue === rightValue) return 0;
    const compare = leftValue > rightValue ? 1 : -1;
    return sortOrder.value === "asc" ? compare : -compare;
  });
  return items;
});

async function syncZone(zoneId) {
  syncingZoneId.value = zoneId;
  errorMessage.value = "";
  try {
    await client.post(`/domains/zones/${zoneId}/sync`);
    await fetchZones();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "域名同步失败。";
  } finally {
    syncingZoneId.value = null;
  }
}

function toggleSort(key) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
    return;
  }
  sortKey.value = key;
  sortOrder.value = "asc";
}
</script>

<template>
  <section>
    <div v-if="errorMessage" class="mt-8 rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">
      {{ errorMessage }}
    </div>

    <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
      <table class="min-w-full text-left">
        <thead class="bg-slate-50 text-sm text-slate-500">
          <tr>
            <th class="px-6 py-4">
              <button class="font-medium" @click="toggleSort('zone_name')">域名</button>
            </th>
            <th class="px-6 py-4">
              <button class="font-medium" @click="toggleSort('provider')">Provider</button>
            </th>
            <th class="px-6 py-4">
              <button class="font-medium" @click="toggleSort('account_name')">账号</button>
            </th>
            <th class="px-6 py-4">
              <button class="font-medium" @click="toggleSort('record_count')">记录数</button>
            </th>
            <th class="px-6 py-4">
              <button class="font-medium" @click="toggleSort('status')">状态</button>
            </th>
            <th class="px-6 py-4 text-right">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100">
            <td class="px-6 py-6 text-slate-500" colspan="5">加载中...</td>
          </tr>
          <tr v-else-if="zones.length === 0" class="border-t border-slate-100">
            <td class="px-6 py-6 text-slate-500" colspan="5">当前还没有域名数据。</td>
          </tr>
          <tr v-for="item in sortedZones" :key="item.id" class="border-t border-slate-100 transition hover:bg-slate-50/70">
            <td class="px-6 py-4 font-medium">{{ item.zone_name }}</td>
            <td class="px-6 py-4 uppercase text-slate-600">{{ item.provider }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.account_name }}</td>
            <td class="px-6 py-4">
              <span class="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">{{ item.record_count }}</span>
            </td>
            <td class="px-6 py-4">
              <span
                class="rounded-full px-3 py-1 text-sm"
                :class="item.status === 'active' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'"
              >
                {{ item.status }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex justify-end gap-2">
                <button
                  class="inline-flex rounded-full bg-white px-3 py-1 text-sm text-slate-700 shadow-sm ring-1 ring-slate-200 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
                  :disabled="syncingZoneId === item.id"
                  @click="syncZone(item.id)"
                >
                  {{ syncingZoneId === item.id ? "同步中..." : "同步" }}
                </button>
                <RouterLink
                  class="inline-flex rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700 transition hover:bg-slate-200"
                  :to="`/domains/records?zone=${item.id}&zone_name=${encodeURIComponent(item.zone_name)}`"
                >
                  查看记录
                </RouterLink>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
