<script setup>
import { computed } from "vue";

import { cn } from "@/lib/utils";

const props = defineProps({
  variant: {
    type: String,
    default: "default",
  },
  size: {
    type: String,
    default: "default",
  },
  class: {
    type: String,
    default: "",
  },
  as: {
    type: String,
    default: "button",
  },
});

const classes = computed(() =>
  cn(
    "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400 disabled:pointer-events-none disabled:opacity-50",
    props.variant === "default" && "bg-slate-900 text-white hover:bg-slate-800",
    props.variant === "outline" && "border border-slate-200 bg-white hover:bg-slate-50",
    props.variant === "ghost" && "hover:bg-slate-100",
    props.size === "default" && "h-10 px-4 py-2",
    props.size === "sm" && "h-8 rounded-md px-3 text-xs",
    props.class,
  ),
);
</script>

<template>
  <component :is="as" :class="classes">
    <slot />
  </component>
</template>
