import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
// A relative MAKEFUN_OUTPUT_DIR is resolved against the caller's cwd,
// an absolute one is used as-is; default is the server's /output.
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const src = join(here, "assets", "poster.png");
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error(`poster asset missing: ${src} (run tools/render.py first)`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
console.log(`wrote ${dst}`);
