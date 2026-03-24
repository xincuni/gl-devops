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
        <BreadcrumbItem><BreadcrumbPage>账单分析</BreadcrumbPage></BreadcrumbItem>
      </Breadcrumb>
      <div class="mt-4 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Billing & Cost</p>
          <h2 class="mt-2 text-3xl font-semibold text-slate-900">账单采集与费用分析</h2>
        </div>
        <div class="flex flex-wrap gap-2">
          <RouterLink to="/billing/overview">
            <Button :variant="route.path === '/billing/overview' ? 'default' : 'outline'">账单总览</Button>
          </RouterLink>
          <RouterLink to="/billing/analysis">
            <Button :variant="route.path === '/billing/analysis' ? 'default' : 'outline'">费用分析</Button>
          </RouterLink>
        </div>
      </div>
    </div>
    <div class="mt-6">
      <router-view />
    </div>
  </section>
</template>
