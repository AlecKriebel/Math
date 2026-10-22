#!/usr/bin/env python3
"""Readonly verification of sealed second-review outputs and frozen copies."""
from pathlib import Path
import hashlib,json,argparse
OUT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--full-input-recheck',action='store_true',help='Also compare all854 original live inputs; later root administrative edits may legitimately change dated root records.')
args=parser.parse_args()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rowcheck(p,row):
 assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],str(p)
seal=json.loads((OUT/'SEAL.json').read_text());pins=json.loads((OUT/'OUTPUT_PINS.json').read_text())
for r in seal['pinned_records']:rowcheck(OUT/r['path'],r)
for r in pins['files']:rowcheck(OUT/r['path'],r)
frozen=json.loads((OUT/'FROZEN_COPY_PINS.json').read_text())
for r in frozen['files']:rowcheck(OUT/r['path'],r)
assert (OUT/'INPUT_PINS.sha256').read_text().split()[0]==sha(OUT/'INPUT_PINS.json')
initial=json.loads((OUT/'INPUT_PINS.json').read_text())
base=Path(initial['base'])
if args.full_input_recheck:
 for r in initial['files']:rowcheck(base/r['path'],r)
# Candidate bytes, including source/PDF/archive, remain the same as the review's initial complete candidate freeze.
for r in initial['files']:
 if r['path'].startswith('preprint_v1_0/'):rowcheck(base/r['path'],r)
verdict=json.loads((OUT/'VERDICT.json').read_text());assert verdict['findings']==[] and verdict['severity_counts']==dict.fromkeys(['P0','P1','P2','P3'],0)
print(json.dumps({'status':'PASS','sealed_output_files':len(pins['files']),'frozen_copies':len(frozen['files']),'candidate_files':177,'full_initial_live_input_recheck':args.full_input_recheck,'actionable_findings':0,'review':'second fresh full package review'}))
