#!/usr/bin/env python3
"""Validate old dated stage pins using only byte-identical preserved records."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;PACKAGE=AUDIT/'preprint_v1_0';REPAIR01=AUDIT/'repairs/package01'
def require(c,m):
 if not c:raise ValueError(m)
def match(p,r):return p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
def resolve_package(r):
 for p in [HERE/'before/preprint_v1_0'/r['path'],REPAIR01/'before/preprint_v1_0'/r['path'],PACKAGE/r['path']]:
  if match(p,r):return p
 raise ValueError('No exact preserved stage bytes: '+r['path'])
def main():
 groups=[('original_preparation103',json.loads((PACKAGE/'OUTPUT_PINS.json').read_text())['entries'],103),('repair01_current124',json.loads((PACKAGE/'CURRENT_OUTPUT_PINS.json').read_text())['entries'],124),('repair01_all125',json.loads((REPAIR01/'FINAL_CURRENT_PINS.json').read_text())['records'],125)]
 result=[]
 for stage,records,count in groups:
  require(len(records)==count,'old stage count changed')
  result.append({'stage':stage,'count':len(records),'records':[dict(r,resolved_path=resolve_package(r).relative_to(AUDIT).as_posix()) for r in records]})
 oldrepair=json.loads((REPAIR01/'OUTPUT_PINS.json').read_text())['entries'];require(len(oldrepair)==37,'repair01 output count changed')
 for r in oldrepair:require(match(REPAIR01/r['path'],r),'repair01 terminal bytes changed')
 initial01=json.loads((REPAIR01/'INPUT_PINS.json').read_text())['records'];require(len(initial01)==294,'repair01 original custody count changed')
 for r in initial01:
  if r['path'].startswith('preprint_v1_0/'):
   resolve_package(dict(r,path=r['path'][len('preprint_v1_0/'):]))
  else:require(match(AUDIT/r['path'],r),'repair01 old outside-package input changed')
 for folder,count in [('package_01',17),('package_02',28)]:
  records=json.loads((AUDIT/'reviews'/folder/'OUTPUT_PINS.json').read_text())['entries'];require(len(records)==count,'old review count changed')
  for r in records:require(match(AUDIT/'reviews'/folder/r['path'],r),'old review output changed')
 print(json.dumps({'pass':True,'scope':'Exact dated stage validation only; no old seal is rebound to new bytes.','stages':result,'repair01_terminal_outputs_unchanged':37,'repair01_initial_inputs_resolved':294,'whole01_outputs_unchanged':17,'whole02_outputs_unchanged':28},indent=2))
if __name__=='__main__':main()
