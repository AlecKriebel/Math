#!/usr/bin/env python3
"""Prepare an exact pinned OAI proof closure without changing the source clone."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PIN = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
MATHLIB_PIN = 'd13f23b723b8a846827a245b89c10fc7d3f11612'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-clone', type=Path, default=Path('/Users/alec/Desktop/math'))
    ap.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'formal_build')
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    def blob(rel):
        return subprocess.check_output(['git', '-C', str(args.source_clone), 'show', f'{PIN}:lean/{rel}'])
    seen, active, order = set(), set(), []
    def visit(module):
        if module in active:
            raise RuntimeError(f'import cycle: {module}')
        if module in seen:
            return
        active.add(module)
        data = blob(module.replace('.', '/')+'.lean')
        for line in data.decode().splitlines():
            if line.startswith('import '):
                for child in line.split()[1:]:
                    if child.startswith('OAI.'):
                        visit(child)
        active.remove(module)
        seen.add(module)
        order.append((module, data))
    visit('OAI.Analysis.HenonEmden.Main')
    rows = []
    for module, data in order:
        rel = module.replace('.', '/')+'.lean'
        target = args.output/rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        rows.append({'module':module,'source_relative':f'lean/{rel}',
                     'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    for rel in ['lean-toolchain','LICENSE','ComparatorChallenges/HenonEmden.lean',
                'ComparatorChallenges/HenonEmden.json','docs/370.md']:
        target = args.output/rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob(rel))
    (args.output/'lakefile.lean').write_text(f'''import Lake
open Lake DSL
package OAI where
  version := v!"0.1.0"
  fixedToolchain := true
  leanOptions := #[⟨`autoImplicit, false⟩]
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "{MATHLIB_PIN}"
@[default_target] lean_lib OAI where
  roots := #[`OAI.Analysis.HenonEmden.Main]
lean_lib ComparatorChallenges where
  roots := #[`ComparatorChallenges.HenonEmden]
''')
    preserved_lock = Path(__file__).resolve().parent/'formal_lean_dependency_lock.json'
    (args.output/'lake-manifest.json').write_bytes(preserved_lock.read_bytes())
    audit = Path(__file__).resolve().parent/'formal_AxiomAudit.lean'
    (args.output/'AxiomAudit.lean').write_bytes(audit.read_bytes())
    (args.output/'source_hashes_prepared.json').write_text(json.dumps(
        {'upstream_commit':PIN, 'mathlib_commit':MATHLIB_PIN,'modules':rows},indent=2)+'\n')
    (args.output/'import_order.txt').write_text('\n'.join(module for module,_ in order)+'\n')
    print(f'Prepared {len(order)} exact OAI modules at {args.output}; build not run.')

if __name__ == '__main__':
    main()
