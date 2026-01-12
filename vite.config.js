import { defineConfig } from "vite";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  root: path.resolve(__dirname, "frontend"),
  build: {
    outDir: path.resolve(__dirname, "static", "dist"),
    emptyOutDir: true,
    rollupOptions: {
      input: path.resolve(__dirname, "frontend", "main.js"),
      output: {
        entryFileNames: "assets/[name].js",
        chunkFileNames: "assets/[name].js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith(".css")) {
            return "assets/[name].css";
          }
          return "assets/[name][extname]";
        },
      },
    },
  },
});
