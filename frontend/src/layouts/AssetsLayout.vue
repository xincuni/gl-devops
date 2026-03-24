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
        <BreadcrumbItem><BreadcrumbLink to="/accounts">平台</BreadcrumbLink></BreadcrumbItem>
        <BreadcrumbSeparator />
        <BreadcrumbItem><BreadcrumbPage>资产管理</BreadcrumbPage></BreadcrumbItem>
      </Breadcrumb>
      <div class="mt-4 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Asset Management</p>
          <h2 class="mt-2 text-3xl font-semibold text-slate-900">云主机与 CMDB</h2>
        </div>
        <div class="flex flex-wrap gap-2">
          <RouterLink to="/assets/instances">
            <Button :variant="route.path === '/assets/instances' ? 'default' : 'outline'">主机列表</Button>
          </RouterLink>
          <RouterLink to="/cmdb/assets">
            <Button :variant="route.path.startsWith('/cmdb/assets') ? 'default' : 'outline'">CMDB</Button>
          </RouterLink>
          <RouterLink to="/jumpserver/rules">
            <Button :variant="route.path.startsWith('/jumpserver') ? 'default' : 'outline'">JumpServer</Button>
          </RouterLink>
        </div>
      </div>
    </div>
    <div class="mt-6">
      <router-view />
    </div>
  </section>
</template>
