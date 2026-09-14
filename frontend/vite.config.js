import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In dev, forward API/health calls to the FastAPI server on :8000.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
      "/health": "http://localhost:8000",
      "/healthz": "http://localhost:8000",
    },
  },
  build: { outDir: "dist", emptyOutDir: true },
});
