// Entry for make.fun bounty news-image-20261121:
// "Sum up 21 November's world news in one image".
//
// The artwork is entry.png beside this file (1024x1024, drawn offline by
// make_image.py from the day's headlines). This program checks the file
// against the bounty gate (PNG, at most 1 MiB, at most 1024x1024) and copies
// its bytes unchanged to the grader's output directory. Node standard
// library only, no network, deterministic: every run writes the same bytes.
//
// Local test (outside the grader container):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024;
const MAX_DIMENSION = 1024;
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);

if (bytes.length === 0 || bytes.length > MAX_BYTES) {
  throw new Error(`entry.png must be 1..${MAX_BYTES} bytes, got ${bytes.length}`);
}
for (let i = 0; i < PNG_SIGNATURE.length; i += 1) {
  if (bytes[i] !== PNG_SIGNATURE[i]) {
    throw new Error('entry.png does not start with the PNG signature');
  }
}
// IHDR width/height: big-endian uint32 at offsets 16 and 20.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
  throw new Error(`entry.png is ${width}x${height}, over the ${MAX_DIMENSION}px cap`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
console.log(`entry.png ${width}x${height}, ${bytes.length} bytes -> ${join(outDir, 'entry.png')}`);
