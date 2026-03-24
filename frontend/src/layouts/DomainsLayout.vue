<script setup>
import { useRoute } from "vue-router";

import { Button } from "@/components/ui/button";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";

const route = useRoute();
</script>

<template>
  <section>
    <div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <Breadcrumb>
        <BreadcrumbItem>
          <BreadcrumbLink to="/accounts">平台</BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator />
        <BreadcrumbItem>
          <BreadcrumbPage>域名管理</BreadcrumbPage>
        </BreadcrumbItem>
      </Breadcrumb>

      <div class="mt-4 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Domain Management</p>
          <h2 class="mt-2 text-3xl font-semibold text-slate-900">域名与 DNS</h2>
          <p class="mt-2 text-sm text-slate-500">域名页做成二级目录，避免多个域名和记录入口混在一级导航。</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <RouterLink to="/domains/zones">
            <Button :variant="route.path === '/domains/zones' ? 'default' : 'outline'">域名列表</Button>
          </RouterLink>
          <RouterLink to="/domains/records">
            <Button :variant="route.path === '/domains/records' ? 'default' : 'outline'">DNS 记录</Button>
          </RouterLink>
        </div>
      </div>
    </div>

    <div class="mt-6">
      <router-view />
    </div>
  </section>
</template>
