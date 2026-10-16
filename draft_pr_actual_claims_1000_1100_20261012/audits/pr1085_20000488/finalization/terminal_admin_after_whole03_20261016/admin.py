"""Bounded dated terminal administration after adopted whole03; no services."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys
F=Path(__file__).resolve().parent; A=F.parents[1]; K=A/'preprint_v1_0'
ALLOWED=['README.md','verify_package.py','PAYLOAD_MEMBERS.txt','SUPPORT_MANIFEST.json','pr1085_support_v1_0.zip','UPLOAD_BINDINGS.json']
CURRENT='CURRENT_TERMINAL_ACCOUNTING_20261016.json'
CMAP='CURRENT_TERMINAL_COPY_MAP_20261016.json'
PREFIX='evidence/terminal_after_whole03/'
REVIEW_FILES=['REPORT.md','VERDICT.json','SEAL.json','OUTPUT_PINS.json','INPUT_FREEZE.json','DERIVATION_FREEZE.json','INDEPENDENT_DERIVATION.md','SOURCE_READ_LEDGER.json','check_independent.py','NEW_MATH_RECEIPTS.json','FINAL_CONSERVATION.json']
SOURCES=['ROOT_CASE_ALIAS_REPAIR_REVIEW_01.json','ROOT_WHOLE_PACKAGE_REVIEW_03.json']+['reviews/package_03/'+n for n in REVIEW_FILES]+['preprint_v1_0/'+n for n in ALLOWED if not n.endswith('.zip')]
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def pin(p,base):return {'path':str(p.relative_to(base)),**ident(p)}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def dump(p,o):
 p.parent.mkdir(parents=True,exist_ok=True);write(p,(json.dumps(o,indent=2)+'\n').encode())
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.after_whole03_tmp');need(not t.exists(),'own atomic temporary exists');t.write_bytes(b);os.replace(t,p)
def load(p):return json.loads(p.read_text())
def initialize():
 need(not (F/'BASELINE_INPUT_PINS.json').exists(),'already initialized')
 rows=[pin(p,A) for p in sorted(A.rglob('*')) if p.is_file() and F not in p.parents]
 need(not any(p.is_symlink() for p in A.rglob('*') if F not in p.parents),'unexpected audit symlink')
 need(len([p for p in K.rglob('*') if p.is_file()])==179,'unexpected candidate boundary')
 need(ident(K/'paper.pdf')=={'bytes':97501,'sha256':'464de043ac6b723f3bd5c03dddb6efd1c0bfeb05b5209bb532006580b7aedc2d'},'paper boundary')
 need(ident(K/'pr1085_support_v1_0.zip')=={'bytes':513981,'sha256':'e550ae4098acc41ea9ebf11d2f452de64acfceb375b63a4197853607b8c9c591'},'archive boundary')
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 dump(F/'BASELINE_INPUT_PINS.json',{'utc':now,'scope':'Every preexisting regular audit file before new post-whole03 terminal administration; this new effort excluded. Hash-only.','files':rows})
 for n in ALLOWED:
  p=F/'before/preprint_v1_0'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(K/n,p)
 dump(F/'AUTHORIZED_EXISTING_CHANGES.json',{'utc':now,'files':['preprint_v1_0/'+n for n in ALLOWED],'scope':'Current dated terminal prose/verifier only, with dependent allowlist/manifest/CLOSED ZIP/binding. All prior status, seals, math, PDF, path guards and native bibliography exact.'})
 (F/'RESEARCH_LOG.md').write_text('# Terminal administration after whole03\n\n'+now+f' — Froze all {len(rows)} prior regular audit inputs and exact before bytes of six allowed existing edits. Only own scratch is ignored. Administrative completion estimate 10%; root final integrity remains required.\n')
 print(json.dumps({'frozen_inputs':len(rows),'saved_before':len(ALLOWED)}))
def mutate():
 need(not (K/CURRENT).exists(),'already mutated')
 baseline={r['path']:r for r in load(F/'BASELINE_INPUT_PINS.json')['files']}
 selected=[]
 for src in SOURCES:
  source=F/'before'/src if src.startswith('preprint_v1_0/') else A/src
  row=baseline[src];need(ident(source)=={k:row[k] for k in ['bytes','sha256']},'copy source boundary '+src)
  target=PREFIX+src;write(K/target,source.read_bytes())
  item={'source_relative_audit':src,'copy':target,**ident(source)}
  if src.startswith('preprint_v1_0/'):item['source_snapshot_relative_audit']=str(source.relative_to(A))
  selected.append(item)
 dump(K/CMAP,{'schema':1,'scope':'Minimal authored whole03/root interfaces and five exact before-interface copies only. Original preparation/terminal partitions and six repair copies are unchanged. Source locators refer to exact local audit custody, not distribution promises; omitted bodies and historical executable environments are not replay claims.','files':selected})
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 current={'schema':1,'utc':now,'pr':1085,'problem_id':20000488,'audited_head':'5e23f0c801d23976830657d2eef2b32bdc7da05a','status':'WHOLE03_ROOT_ADOPTED_TERMINAL_ADMIN_PENDING_EXTERNAL_ROOT_INTEGRITY','whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_complete_whole_review':3,'latest_actionable_P0_P1_P2_P3':0,'case_alias_repair_root_adopted':True,'latest_complete_whole_review_root_adopted':True,'new_complete_whole03_required':False,'new_complete_whole03_completed':True,'further_complete_whole_review_currently_required':False,'root_terminal_integrity_adoption_required':True,'root_terminal_integrity_adopted':False,'publication_ready':False,'all_actionable_issues_resolved':False,'issues_resolved':False,'published':False,'human_peer_review':False,'formal_proof_certificate':False,'services_hold':'preceding PR1032 priority cursor','historical_STATUS_TERMINAL_ACCOUNTING_CASE_REPAIR_preserved':True,'priority':'UNKNOWN_EXACT_REMAINING_GEOMETRIC_FORMULATIONS','novelty':'UNKNOWN','worldwide_open_status':'UNKNOWN','independent_discovery':'UNKNOWN','paper_pdf_sha256':'464de043ac6b723f3bd5c03dddb6efd1c0bfeb05b5209bb532006580b7aedc2d','paper_tex_sha256':'c18a6ed12250dcee413e85f9a6297c525015396f151cdab8d89a6eb76938046d','latest_review_prefix':PREFIX+'reviews/package_03/','latest_root_adoption':PREFIX+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','repair_root_adoption':PREFIX+'ROOT_CASE_ALIAS_REPAIR_REVIEW_01.json','meaning':'Three NEW complete whole-package reviews have completed (minimum two). Whole01/02 zero findings predate CASE-1085. Root adopted the repair and the NEW complete whole03 ZERO-actionable result on the repaired candidate. No further complete review is currently required. This bounded terminal administration is not a new whole review or release grant. External ROOT terminal integrity adoption is required and unadopted; readiness/issue-clearance/publication remain false and services remain held after PR1032. Historical pending records retain their exact captured-stage meaning.'}
 dump(F/'CURRENT_TERMINAL_ACCOUNTING.json',current);dump(K/CURRENT,current)
 readme=(F/'before/preprint_v1_0/README.md').read_text()
 old='Those captured zero-finding verdicts predate the later case-alias finding. CASE_ALIAS_REPAIR_ACCOUNTING.json now requires external root repair adoption and a NEW complete whole03 review; current readiness and all-issues-clearance remain false.'
 new='Those captured zero-finding verdicts predate the later case-alias finding. The unchanged dated CASE_ALIAS_REPAIR_ACCOUNTING.json records the subsequent pending-repair stage. CURRENT_TERMINAL_ACCOUNTING_20261016.json records the current three-review state: root adopted the repair and the NEW complete whole03 ZERO-actionable review. No further complete review is currently required; external root terminal integrity adoption is required and unadopted, so current readiness and all-issues-clearance remain false.'
 need(old in readme,'README current-stage anchor');readme=readme.replace(old,new)
 old='The new review is pending; readiness, all-issues-clearance and publication remain false, and services remain held after PR1032.'
 new='That dated pending stage is preserved exactly. The later current record below supplies the adopted whole03 completion; readiness, all-issues-clearance and publication remain false, and services remain held after PR1032.'
 need(old in readme,'README historical anchor');readme=readme.replace(old,new)
 readme+='\n## Current terminal state after adopted whole03 (2026-10-16)\n\nCURRENT_TERMINAL_ACCOUNTING_20261016.json is byte-identical to the new outer administrative current record. Three NEW complete whole-package reviews are complete (minimum two); latest whole03 has ZERO actionable P0–P3 findings and root adoption, following root adoption of CASE-1085. No further complete review is currently required. External ROOT terminal integrity adoption remains REQUIRED and unadopted. Publication readiness, all-issues-clearance and publication remain false; services remain held after PR1032. Older status/accounting/review/seal records retain their exact captured-stage meanings.\n\nCURRENT_TERMINAL_COPY_MAP_20261016.json adds only selected authored whole03 report/verdict, frozen derivation, finite checker/results, source-read/custody identities, review pins/seal, root adoptions and five exact before interfaces. Every copied selected whole03 output is bound to its original review output manifest; the root adoption and seal bind that same manifest. Omitted source bodies, images, runtimes, raw operational streams and old ZIPs remain outside this new selection. The old ZIP is retained only in local before custody. Historical pin locators are not redirected to successor bytes.\n\nThe verifier validates the older captured stages and then this separate current state and its evidence bindings. This administration leaves the paper, mathematics, source credits, all four writer/path guards and native bibliographic metadata exact. It performs no compilation, rendering, new mathematical review, service action, human refereeing or priority clearance. The unchanged paper was actually compiled in both modes and all seven pages viewed during complete whole03. Priority, novelty, independent discovery and worldwide openness remain UNKNOWN.\n'
 write(K/'README.md',readme.encode())
 verifier=(F/'before/preprint_v1_0/verify_package.py').read_text();anchor='    require(regular(ROOT / "paper.pdf").read_bytes().startswith(b"%PDF-"), "paper PDF signature")\n'
 gate=(F/'current_gate.txt').read_text();need(anchor in verifier,'verifier current gate anchor');verifier=verifier.replace(anchor,gate+anchor)
 verifier=verifier.replace('"publication_ready": False, "new_whole_reviews": 2,','"publication_ready": False, "new_whole_reviews": 3,\n            "latest_complete_whole_review": 3, "latest_actionable_P0_P1_P2_P3": 0,\n            "root_terminal_integrity_adoption_required": True, "root_terminal_integrity_adopted": False,\n            "further_complete_whole_review_currently_required": False,\n            "current_terminal_exact_copies": len(current_copies),')
 verifier=verifier.replace('"new_complete_whole03_required": True, "new_complete_whole03_completed": False,','"new_complete_whole03_required": False, "new_complete_whole03_completed": True,')
 verifier=verifier.replace('two historical complete whole reviews are recorded; the later case-alias repair requires external root adoption and NEW complete whole03, and services are held after PR1032.','three complete whole reviews are recorded; root adopted the case-alias repair and latest ZERO-actionable whole03. No further complete review is currently required; external root terminal integrity adoption remains required and unadopted, and services are held after PR1032.')
 write(K/'verify_package.py',verifier.encode())
 old=(F/'before/preprint_v1_0/PAYLOAD_MEMBERS.txt').read_text().splitlines();names=sorted(set(old+[r['copy'] for r in selected]+[CURRENT,CMAP]));write(K/'PAYLOAD_MEMBERS.txt',('\n'.join(names)+'\n').encode())
 manifest=load(F/'before/preprint_v1_0/SUPPORT_MANIFEST.json');manifest['files']=[pin(K/n,K) for n in names];dump(K/'SUPPORT_MANIFEST.json',manifest)
 out=F/'rebuilt.zip';proc=subprocess.run([sys.executable,'-B',str(K/'build_archive.py'),'--output',str(out)],capture_output=True,text=True)
 dump(F/'BUILD_RECEIPT.json',{'utc':now,'argv':[sys.executable,'-B',str(K/'build_archive.py'),'--output',str(out)],'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr});need(proc.returncode==0,'actual builder failed '+proc.stderr)
 body=out.read_bytes();write(K/'pr1085_support_v1_0.zip',body);out.unlink()
 binding=load(F/'before/preprint_v1_0/UPLOAD_BINDINGS.json');binding['files'][1].update(ident(K/'pr1085_support_v1_0.zip'));dump(K/'UPLOAD_BINDINGS.json',binding)
 dump(F/'BUILD_SUMMARY.json',{'utc':now,'baseline_inputs':len(baseline),'new_selected_copies':len(selected),'archive_members':len(names)+1,'archive_bytes':len(body),'archive_sha256':sha(body),'all_historical_stages_preserved':True})
 with (F/'RESEARCH_LOG.md').open('a') as log:log.write('\n'+now+' — Added separate identical outer/kit three-review current record, minimal exact evidence selection and operative current semantics. Six allowed existing interfaces updated atomically; no guard/math/native bibliography change. Administrative completion estimate 50%; final-byte controls and root integrity remain.\n')
 print(json.dumps(load(F/'BUILD_SUMMARY.json'),indent=2))
if __name__=='__main__':
 if sys.argv[1:]==['initialize']:initialize()
 elif sys.argv[1:]==['mutate']:mutate()
 else:raise ValueError('use initialize or mutate')
