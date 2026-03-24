<script setup>
import { computed, onMounted, watch, ref } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";

import client from "../../api/client";

const route = useRoute();
const router = useRouter();
const records = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const selectedIds = ref([]);
const typeFilter = ref("");
const statusFilter = ref("");
const keyword = ref("");
const ttl = ref("600");
const currentPage = ref(1);
const totalCount = ref(0);
const pageSize = ref(20);
const currentZoneId = computed(() => route.query.zone || "");
const currentZoneName = computed(() => route.query.zone_name || "");
const successMessage = ref("");
const sortKey = ref("name");
const sortOrder = ref("asc");

async function fetchRecords() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const params = {};
    if (currentZoneId.value) {
      params.zone = currentZoneId.value;
    }
    if (typeFilter.value) {
      params.type = typeFilter.value;
    }
    if (statusFilter.value) {
      params.status = statusFilter.value;
    }
    if (keyword.value) {
      params.search = keyword.value;
    }
    params.page = currentPage.value;
    const { data } = await client.get("/domains/records", { params });
    records.value = data.results || [];
    totalCount.value = data.count || 0;
    selectedIds.value = [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "DNS 记录加载失败。";
  } finally {
    loading.value = false;
  }
}

function syncFiltersFromRoute() {
  typeFilter.value = route.query.type || "";
  statusFilter.value = route.query.status || "";
  keyword.value = route.query.search || "";
  currentPage.value = Number(route.query.page || 1);
}

onMounted(() => {
  syncFiltersFromRoute();
  fetchRecords();
});

watch(
  () => route.query,
  () => {
    syncFiltersFromRoute();
    fetchRecords();
  },
);

async function batchSetStatus(target) {
  if (!selectedIds.value.length) return;
  const endpoint = target === "active" ? "/domains/records/batch-enable" : "/domains/records/batch-disable";
  await client.post(endpoint, { record_ids: selectedIds.value });
  successMessage.value = `已批量${target === "active" ? "启用" : "停用"} ${selectedIds.value.length} 条记录`;
  await fetchRecords();
}

async function batchUpdateTTL() {
  if (!selectedIds.value.length) return;
  await client.post("/domains/records/batch-update-ttl", {
    record_ids: selectedIds.value,
    ttl: Number(ttl.value),
  });
  successMessage.value = `已将 ${selectedIds.value.length} 条记录的 TTL 更新为 ${ttl.value}`;
  await fetchRecords();
}

function clearFilter() {
  router.push("/domains/records");
}

function applyFilters() {
  router.push({
    path: "/domains/records",
    query: {
      ...(currentZoneId.value ? { zone: currentZoneId.value, zone_name: currentZoneName.value } : {}),
      ...(typeFilter.value ? { type: typeFilter.value } : {}),
      ...(statusFilter.value ? { status: statusFilter.value } : {}),
      ...(keyword.value ? { search: keyword.value } : {}),
      page: 1,
    },
  });
}

function toggleAll(event) {
  if (event.target.checked) {
    selectedIds.value = records.value.map((item) => item.id);
  } else {
    selectedIds.value = [];
  }
}

function changePage(nextPage) {
  if (nextPage < 1) return;
  const maxPage = Math.max(1, Math.ceil(totalCount.value / pageSize.value));
  if (nextPage > maxPage) return;
  router.push({
    path: "/domains/records",
    query: {
      ...(currentZoneId.value ? { zone: currentZoneId.value, zone_name: currentZoneName.value } : {}),
      ...(typeFilter.value ? { type: typeFilter.value } : {}),
      ...(statusFilter.value ? { status: statusFilter.value } : {}),
      ...(keyword.value ? { search: keyword.value } : {}),
      page: nextPage,
    },
  });
}

const sortedRecords = computed(() => {
  const items = [...records.value];
  items.sort((left, right) => {
    const leftValue = left[sortKey.value] ?? "";
    const rightValue = right[sortKey.value] ?? "";
    if (leftValue === rightValue) return 0;
    const compare = leftValue > rightValue ? 1 : -1;
    return sortOrder.value === "asc" ? compare : -compare;
  });
  return items;
});

const allSelected = computed(
  () => records.value.length > 0 && selectedIds.value.length === records.value.length,
);

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
    <div v-if="currentZoneId" class="mb-4 flex items-center justify-between rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
      <div>
        <p class="text-xs uppercase tracking-[0.2em] text-slate-400">当前域名</p>
        <p class="mt-1 text-sm font-medium text-slate-800">{{ currentZoneName || `Zone #${currentZoneId}` }}</p>
      </div>
      <button class="rounded-full bg-white px-3 py-1 text-sm text-slate-700 shadow-sm" @click="clearFilter">
        查看全部
      </button>
    </div>

    <div v-if="errorMessage" class="mt-8 rounded-3xl bg-red-50 px-6 py-4 text-sm text-red-600">
      {{ errorMessage }}
    </div>

    <div v-if="successMessage" class="mt-8 rounded-3xl bg-emerald-50 px-6 py-4 text-sm text-emerald-700">
      {{ successMessage }}
    </div>

    <div v-if="selectedIds.length" class="mt-4 rounded-3xl border border-signal/20 bg-teal-50 px-6 py-4 text-sm text-teal-800">
      已选中 {{ selectedIds.length }} 条记录，可以直接执行批量启用、停用或修改 TTL。
    </div>

    <div class="mb-4 flex flex-col gap-3 rounded-3xl bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between">
      <div class="flex flex-wrap gap-3">
        <input v-model="keyword" class="rounded-xl border border-slate-200 px-3 py-2 text-sm" placeholder="搜索主机记录或值" />
        <select v-model="typeFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部类型</option>
          <option value="A">A</option>
          <option value="CNAME">CNAME</option>
        </select>
        <select v-model="statusFilter" class="rounded-xl border border-slate-200 px-3 py-2 text-sm">
          <option value="">全部状态</option>
          <option value="active">active</option>
          <option value="disabled">disabled</option>
        </select>
        <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white" @click="applyFilters">筛选</button>
      </div>
      <div class="flex flex-wrap gap-2">
        <button class="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50" :disabled="!selectedIds.length" @click="batchSetStatus('active')">批量启用</button>
        <button class="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50" :disabled="!selectedIds.length" @click="batchSetStatus('disabled')">批量停用</button>
        <input v-model="ttl" class="w-24 rounded-xl border border-slate-200 px-3 py-2 text-sm" />
        <button class="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50" :disabled="!selectedIds.length" @click="batchUpdateTTL">批量改 TTL</button>
      </div>
    </div>

    <div class="overflow-hidden rounded-3xl bg-white shadow-sm">
      <table class="min-w-full text-left">
        <thead class="bg-slate-50 text-sm text-slate-500">
          <tr>
            <th class="px-6 py-4">
              <input :checked="allSelected" type="checkbox" @change="toggleAll" />
            </th>
            <th class="px-6 py-4"><button class="font-medium" @click="toggleSort('zone_name')">域名</button></th>
            <th class="px-6 py-4"><button class="font-medium" @click="toggleSort('name')">主机记录</button></th>
            <th class="px-6 py-4"><button class="font-medium" @click="toggleSort('type')">类型</button></th>
            <th class="px-6 py-4"><button class="font-medium" @click="toggleSort('value')">值</button></th>
            <th class="px-6 py-4"><button class="font-medium" @click="toggleSort('ttl')">TTL</button></th>
            <th class="px-6 py-4 text-right">详情</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-t border-slate-100">
            <td class="px-6 py-6 text-slate-500" colspan="7">加载中...</td>
          </tr>
          <tr v-else-if="records.length === 0" class="border-t border-slate-100">
            <td class="px-6 py-6 text-slate-500" colspan="7">当前还没有 DNS 记录。</td>
          </tr>
          <tr v-for="item in sortedRecords" :key="item.id" class="border-t border-slate-100 transition hover:bg-slate-50/70">
            <td class="px-6 py-4">
              <input v-model="selectedIds" :value="item.id" type="checkbox" />
            </td>
            <td class="px-6 py-4 font-medium">{{ item.zone_name }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.name }}</td>
            <td class="px-6 py-4 uppercase">
              <span class="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">{{ item.type }}</span>
            </td>
            <td class="px-6 py-4 text-slate-600">{{ item.value }}</td>
            <td class="px-6 py-4 text-slate-600">{{ item.ttl }}</td>
            <td class="px-6 py-4 text-right">
              <RouterLink class="text-sm font-medium text-slate-700 underline-offset-4 hover:underline" :to="`/domains/records/${item.id}`">
                查看详情
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-4 flex items-center justify-between rounded-2xl bg-white px-4 py-3 shadow-sm">
      <p class="text-sm text-slate-500">共 {{ totalCount }} 条记录</p>
      <div class="flex items-center gap-2">
        <button class="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm" @click="changePage(currentPage - 1)">上一页</button>
        <span class="text-sm text-slate-500">第 {{ currentPage }} 页</span>
        <button class="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm" @click="changePage(currentPage + 1)">下一页</button>
      </div>
    </div>
  </section>
</template>
