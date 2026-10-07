#!/usr/bin/env python3
"""Fetch only six hash-checked external proof sections, outside the deposit payload."""
import hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PIN='adc7f1241b42e322a6451854ab7e4b4c146bf78a'
PART='preprints/Exponential-PSD-rank-of-positively-shifted-matching-matrices-October-5-2026/build/source/sections'
expected=json.loads((ROOT/'agent_notes/upstream_adversary_checks.json').read_text())['source_sha256']
out=ROOT/'sources/family126/build/source/sections';out.mkdir(parents=True,exist_ok=True)
for name,sha in expected.items():
    path=out/name
    if path.exists():data=path.read_bytes()
    else:
        req=urllib.request.Request(f'https://raw.githubusercontent.com/openai/math/{PIN}/{PART}/{name}',headers={'User-Agent':'TSP-Research-Reproduction/1.0'})
        with urllib.request.urlopen(req,timeout=60) as r:data=r.read()
    assert hashlib.sha256(data).hexdigest()==sha,f'Source hash mismatch: {name}'
    path.write_bytes(data)
print('Six pinned proof sections verified. Original author: OpenAI; upstream Apache-2.0 license. No upstream files are included in the authored deposit archives.')
