<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../../stores/auth";

const form = reactive({
  username: "admin",
  password: "",
});

const authStore = useAuthStore();
const router = useRouter();
const loading = ref(false);
const errorMessage = ref("");

async function handleLogin() {
  loading.value = true;
  errorMessage.value = "";
  try {
    await authStore.login(form);
    router.push("/accounts");
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "登录失败，请检查用户名和密码。";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top,_#d1fae5,_#f8fafc_45%,_#e5e7eb)] p-6">
    <div class="w-full max-w-md rounded-3xl bg-white p-8 shadow-xl shadow-slate-200/70">
      <p class="text-sm uppercase tracking-[0.3em] text-slate-500">GL DevOps</p>
      <h1 class="mt-3 text-3xl font-semibold text-slate-900">登录</h1>
      <p class="mt-2 text-sm text-slate-500">迭代 1 先交付认证、云账号、任务中心基础能力。</p>
      <form class="mt-8 space-y-4" @submit.prevent="handleLogin">
        <input v-model="form.username" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none transition focus:border-signal" placeholder="用户名" />
        <input v-model="form.password" type="password" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none transition focus:border-signal" placeholder="密码" />
        <p v-if="errorMessage" class="rounded-2xl bg-red-50 px-4 py-3 text-sm text-red-600">
          {{ errorMessage }}
        </p>
        <button :disabled="loading" type="submit" class="w-full rounded-2xl bg-ink px-4 py-3 font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60">
          {{ loading ? "登录中..." : "登录" }}
        </button>
      </form>
    </div>
  </div>
</template>
