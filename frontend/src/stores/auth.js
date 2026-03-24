import { defineStore } from "pinia";

import client from "../api/client";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    initialized: false,
  }),
  getters: {
    isAuthenticated: () => Boolean(localStorage.getItem("access_token")),
  },
  actions: {
    async login(payload) {
      const { data } = await client.post("/auth/login", payload);
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      await this.fetchMe();
    },
    async fetchMe() {
      const { data } = await client.get("/auth/me");
      this.user = data.data;
      this.initialized = true;
      return this.user;
    },
    async logout() {
      const refresh = localStorage.getItem("refresh_token");
      try {
        if (refresh) {
          await client.post("/auth/logout", { refresh });
        }
      } finally {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        this.user = null;
        this.initialized = true;
      }
    },
    async ensureAuth() {
      if (!localStorage.getItem("access_token")) {
        this.initialized = true;
        return false;
      }
      if (this.user) {
        this.initialized = true;
        return true;
      }
      try {
        await this.fetchMe();
        return true;
      } catch {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        this.user = null;
        this.initialized = true;
        return false;
      }
    },
  },
});
