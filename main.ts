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
// PNG IHDR: width and height are big-endian uint32 at offsets 16 and 20.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width === 0 || height === 0 || width > MAX_DIMENSION || height > MAX_DIMENSION) {
  throw new Error(`entry.png must be within ${MAX_DIMENSION}x${MAX_DIMENSION}, got ${width}x${height}`);
}

// The gate takes a whole PNG: every chunk with its checksum and the image
// data its header describes. Walk the chunk list to IEND, checking each
// chunk's CRC, so a truncated or corrupt file fails here, not at the gate.
const CRC_TABLE = (() => {
  const table = new Int32Array(256);
  for (let n = 0; n < 256; n += 1) {
    let c = n;
    for (let k = 0; k < 8; k += 1) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c;
  }
  return table;
})();

function crc32(buf: Buffer, start: number, end: number): number {
  let c = 0xffffffff;
  for (let i = start; i < end; i += 1) {
    c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  }
  return (c ^ 0xffffffff) >>> 0;
}

let offset = PNG_SIGNATURE.length;
let sawIhdr = false;
let sawIdat = false;
let sawIend = false;
while (offset + 8 <= bytes.length) {
  const length = bytes.readUInt32BE(offset);
  const type = bytes.toString('ascii', offset + 4, offset + 8);
  const dataEnd = offset + 8 + length;
  if (dataEnd + 4 > bytes.length) {
    throw new Error(`entry.png chunk ${type} overruns the file`);
  }
  if (crc32(bytes, offset + 4, dataEnd) !== bytes.readUInt32BE(dataEnd)) {
    throw new Error(`entry.png chunk ${type} has a bad checksum`);
  }
  if (type === 'IHDR') sawIhdr = true;
  if (type === 'IDAT') sawIdat = true;
  if (type === 'IEND') {
    sawIend = true;
    offset = dataEnd + 4;
    break;
  }
  offset = dataEnd + 4;
}
if (!sawIhdr || !sawIdat || !sawIend || offset !== bytes.length) {
  throw new Error('entry.png is not a whole PNG (missing IHDR/IDAT/IEND or trailing bytes)');
}

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });
copyFileSync(source, join(outputDir, 'entry.png'));
