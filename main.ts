// news-image-20261125 entry — Node 22, standard library only.
//
// The entry is the image file entry.png sitting next to this script: a dense
// newspaper front page summing up Wednesday 25 November 2026's world news,
// drawn from scratch in code by compose.py.
//
// This program copies that image to $MAKEFUN_OUTPUT_DIR/entry.png (default
// /output), which is where the grader looks for the entry.
//
// Local check (outside the grader's container, /output stands in for it):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

copyFileSync(source, join(outputDir, 'entry.png'));
