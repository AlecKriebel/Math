#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import subprocess,sys,json,time,hashlib,os,shutil
ROOT=Path('/mnt/data/k2p_identifiability_program')
commands=[
 ('source extraction',[sys.executable,str(ROOT/'code/extract_sources.py')]),
 ('dependency crosswalk',[sys.executable,str(ROOT/'code/build_dependency_crosswalk.py')]),
 ('K2P domain verifier',[sys.executable,str(ROOT/'code/verify_k2p_domain.py')]),
 ('K2P bridge fibre verifier',[sys.executable,str(ROOT/'code/verify_k2p_bridge_fibre.py')]),
 ('clean-room compiler tests',[sys.executable,str(ROOT/'code/run_cleanroom_tests.py')]),
 ('mutation tests',[sys.executable,str(ROOT/'code/run_mutation_tests.py')]),
 ('candidate graph discovery',[sys.executable,str(ROOT/'code/discover_collision_graphs.py')]),
 ('membership evidence extract',[sys.executable,str(ROOT/'code/extract_membership_evidence.py')]),
 ('collision certificate scan',[sys.executable,str(ROOT/'code/scan_collision_certificates.py')]),
]
results=[]
for name,cmd in commands:
 t=time.time()
 try:
  cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=600)
  status='PASS' if cp.returncode==0 else 'FAIL'
  rc=cp.returncode;stdout=cp.stdout;stderr=cp.stderr
 except subprocess.TimeoutExpired as e:
  status='TIMEOUT';rc=None;stdout=e.stdout or '';stderr=e.stderr or ''
 except Exception as e:
  status='ERROR';rc=None;stdout='';stderr=repr(e)
 safe=name.replace(' ','_').replace('/','_')
 (ROOT/f'logs/checkpoint_{safe}.stdout.txt').write_text(stdout if isinstance(stdout,str) else str(stdout))
 (ROOT/f'logs/checkpoint_{safe}.stderr.txt').write_text(stderr if isinstance(stderr,str) else str(stderr))
 results.append({'name':name,'status':status,'returncode':rc,'seconds':round(time.time()-t,3),
                 'stdout':f'logs/checkpoint_{safe}.stdout.txt','stderr':f'logs/checkpoint_{safe}.stderr.txt'})
# supplied replay is kept separate because failures may reflect missing optional environment.
sup=[]
p=ROOT/'certificates/supplied_k2p_replay.json'
if p.exists():
 try:sup=json.loads(p.read_text())
 except Exception:pass
graphs=[]
p=ROOT/'certificates/discovered_collision_graphs.json'
if p.exists():
 try:graphs=json.loads(p.read_text())
 except Exception:pass
lit={}
p=ROOT/'certificates/literature_search_raw.json'
if p.exists():
 try:
  x=json.loads(p.read_text());lit={'searched_at_utc':x.get('searched_at_utc'),'errors':x.get('errors',[]),'queries':x.get('queries',[])}
 except Exception:pass
status={'generated_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'scope':'partial theorem-hardening checkpoint, not full classification',
        'internal_checks':results,'supplied_replay':sup,'candidate_graph_count':len(graphs),'literature':lit,
        'closed_gates':['exact K2P edge cone','composition','strict stochastic subdivision','strict continuous-time cone','admissible-rooting physical divisibility','two K2P character sectors','directed submersion consequence of certified collision','abstract contextualization lemma'],
        'open_gates':['collision graph-to-witness binding','one-sided bridge recovery','ordinary triangle K2P image relation','physical component bridge fibre','bounded directed K2P atlas','marginal open-image theorem','restoration/coherent probes','Omega/Theta K2P deformation','independent collision replay','global continuous-time gluing']}
(ROOT/'CHECKPOINT_STATUS.json').write_text(json.dumps(status,indent=2))
# README reflects actual check status.
md=['# K2P full-identifiability program — theorem-hardening checkpoint','',
'**This archive is partial.  It does not claim Outcome K2P-FULL, K2P-MODIFIED, or K2P-COUNTERCLASSIFICATION.**','',
'It closes the exact K2P edge-domain/rooting gate, derives the correct two-sector bridge gauge, proves the proper directed-germ consequence of a supplied strict full-rank tree–theta collision, and proves a general contextualization lemma.  The exhaustive bounded atlas and global necessity theorem remain open.','',
'## Internal checks','']
for r in results:md.append(f"- **{r['status']}** — {r['name']} ({r['seconds']} s; `{r['stdout']}` / `{r['stderr']}`)")
md += ['','## Main reports','',
'- `reports/JC_TO_K2P_DEPENDENCY_CROSSWALK.md`','- `reports/K2P_MODEL_DOMAIN_AND_ROOTING_AUDIT.md`','- `reports/K2P_TREE_THETA_CONTAINMENT_AUDIT.md`','- `reports/K2P_LOCAL_MOVE_CLASSIFICATION.md`','- `reports/K2P_GLOBAL_THEOREM_REPORT.md`','- `reports/K2P_SHARPNESS_REPORT.md`','- `reports/ADVERSARIAL_FAILURE_LOG.md`','- `reports/PRIORITY_AND_LITERATURE_AUDIT.md`','',
'## Exact new code','',
'- `code/verify_k2p_domain.py` — inverse Fourier cone, composition, strict factorization, CT check.','- `code/verify_k2p_bridge_fibre.py` — exact character-orbit and gauge check.','- `code/k2p_cleanroom/` — independent graph-to-switching-to-descendant-mask-to-Fourier compiler.','- `tests/` — clean-room unit and mutation tests.','',
'## Supplied-source replay','']
if sup:
 for r in sup:md.append(f"- **{r.get('status')}** — `{r.get('path')}`")
else:md.append('- No executable supplied K2P verifier was automatically bound and replayed.  Inspect `reports/SUPPLIED_K2P_VERIFIER_REPLAY.md`.')
md += ['','## Open theorem gates','']+[f'- {x}' for x in status['open_gates']]
md += ['','## Reproduce','',"Run `bash run_all.sh`.  The script writes fresh logs and rebuilds `CHECKPOINT_STATUS.json`.  SHA-256 manifests are generated by `code/make_manifest.py`."]
(ROOT/'README.md').write_text('\n'.join(md)+'\n')
print(json.dumps(status,indent=2))
