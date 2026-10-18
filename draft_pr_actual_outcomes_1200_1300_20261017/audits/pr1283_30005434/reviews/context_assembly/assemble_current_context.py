#!/usr/bin/env python3
"""Assemble explicitly curated PR1283 inputs; never infer source membership."""
from pathlib import Path
import argparse, hashlib, json, runpy, subprocess
HERE=Path(__file__).resolve()
if HERE.parent.name=='_local':A=HERE.parents[1]
elif HERE.parent.name=='context_assembly' and HERE.parent.parent.name=='reviews':A=HERE.parents[2]
else:raise RuntimeError('Explicit own context-assembler location required')
P=A/'publication'
REG=[
 ('reviews/blind_source_reconstruction/MANIFEST.json','files','relative_path','bytes','math'),
 ('reviews/candidate_adversary/MANIFEST.json','files','relative_path','bytes','math'),
 ('reviews/blind_reconstruction_adversary/MANIFEST.json','files','relative_path','bytes','math'),
 ('reviews/portable_quotient_diagnostics/MANIFEST.json','files','relative_path','bytes','math'),
 ('priority/direct_lineage/OUTPUT_MANIFEST.json','files','relative_path','bytes','priority'),
 ('priority/structural_reductions/OUTPUT_MANIFEST.json','files','relative_path','bytes','priority'),
 ('priority/direct_lineage_cross_challenge/OUTPUT_MANIFEST.json','files','relative_path','bytes','priority'),
 ('priority/structural_cross_challenge/OUTPUT_MANIFEST.json','files','relative_path','bytes','priority'),
 ('reviews/note_author/MANIFEST.json','members','relative_path','bytes','documentary'),
 ('reviews/note_scope_revision1/MANIFEST.json','files','relative_path','bytes','documentary'),
 ('reviews/context_assembly/MANIFEST.json','files','relative_path','bytes','documentary'),
 ('reviews/workflow_tooling/MANIFEST.json','authored_files','path','bytes','workflow')]
ROOTFILES=[
 'ELIGIBILITY_REVALIDATION.json','LIVE_PR_PREFLIGHT.json',
 'ROOT_MATHEMATICAL_REVIEW.md','ROOT_PRIMARY_SOURCE_INSPECTION.json',
 'ROOT_INITIAL_MATH_AUTHENTICATION.json','ROOT_BLIND_ADVERSARY_AUTHENTICATION.json',
 'root_intersection_family_check.py','ROOT_INTERSECTION_FAMILY_RESULTS.json',
 'ROOT_INTERSECTION_FAMILY_REPLAY.json','ROOT_BLIND_DETERMINISTIC_STDOUT.txt',
 'ROOT_CURRENT_EDITION_AUTHENTICATION.json','CURRENT_EDITION_CHANGE_MAP.json',
 'ROOT_INITIAL_PRIORITY_AUTHENTICATION.json','ROOT_FINAL_PRIORITY_AUTHENTICATION.json',
 'ROOT_PRIORITY_REVIEW.md','ROOT_PRIORITY_QUERY_LEDGER.json',
 'ROOT_NOTE_AUTHOR_AUTHENTICATION.json','ROOT_WORKFLOW_AUTHENTICATION.json',
 'ROOT_CURRENT_METADATA_WORKFLOW_REPLAY.json','PACKAGE_GUIDE.md']
SEALS=[
 'reviews/blind_source_reconstruction/INITIAL_SEAL.json',
 'reviews/candidate_adversary/SEAL.json',
 'reviews/blind_reconstruction_adversary/FINAL_SEAL.json',
 'reviews/note_author/SEAL.json',
 'priority/direct_lineage/INITIAL_SEAL.json',
 'priority/structural_reductions/INITIAL_SEAL.json',
 'priority/direct_lineage_cross_challenge/CROSS_CHALLENGE_SEAL.json',
 'priority/structural_cross_challenge/CROSS_CHALLENGE_SEAL.json',
 'reviews/workflow_tooling/SEAL.json']
REPLAYS=[
 ('root_intersection_family_check.py','ROOT_INTERSECTION_FAMILY_RESULTS.json','Intersection-closed subset families and boundary controls; finite diagnostics only.'),
 ('reviews/blind_source_reconstruction/checks.py','ROOT_BLIND_DETERMINISTIC_STDOUT.txt','Independent relation enumeration; original three-mode wrapped log is history, bare stdout reference is explicit.'),
 ('reviews/candidate_adversary/verify_algebra.py','reviews/candidate_adversary/CHECK_RESULTS.json','Independent labelled meet/operation-table enumeration and fault controls; no private input checker.'),
 ('reviews/portable_quotient_diagnostics/checks.py','reviews/portable_quotient_diagnostics/CHECK_RESULTS.txt','Detached free-three-generator congruence quotients, table enumeration and boundaries; mathematical functions preserved.'),
 ('priority/structural_cross_challenge/durable_structural_checks.py','priority/structural_cross_challenge/DURABLE_DIAGNOSTIC_RESULTS.json','Durable checks separating old classes from the exact old operation; no historical priority inference.')]

def need(c,m):
 if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def checker():return runpy.run_path(str(P/'verification/verify.py'))

def curated(v):
 registry=[];files={}
 def add(raw,role='authored_evidence'):
  path=v['member'](A,raw);need(path.is_file(),'Missing explicit artifact '+raw)
  item={'path':raw,**binding(path),'role':role}
  need(raw not in files or files[raw]==item,'Conflicting explicit inventory '+raw);files[raw]=item
 for raw,ek,pk,sk,role in REG:
  p=v['member'](A,raw);base=p.parent.relative_to(A).as_posix()
  reg={'path':raw,'base':base,'entries_key':ek,'path_key':pk,'size_key':sk,'sha256':sha(p),'role':role}
  v['registry_schema'](reg);registry.append(reg);add(raw)
  obj=json.loads(p.read_text());need(isinstance(obj.get(ek),list) and bool(obj[ek]),'Empty explicit manifest '+raw)
  for entry in obj[ek]:
   name=v['manifest_member_name'](reg,entry,obj);v['check_binding'](v['member'](A,base+'/'+name),entry,sk);add(base+'/'+name)
 for raw in ROOTFILES:
  add(raw,'source_receipt' if raw in {'ROOT_PRIMARY_SOURCE_INSPECTION.json','ROOT_PRIORITY_QUERY_LEDGER.json'} else 'authored_evidence')
 for raw in SEALS:add(raw)
 v['authenticate_nested_manifests'](A,registry)
 return registry,[files[k] for k in sorted(files)]

def assemble(bootstrap=False):
 v=checker();snapshot=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text())
 v['authenticate_snapshot'](A/'submitted',snapshot)
 source={'submitted_snapshot_sha256':sha(A/'SUBMITTED_SNAPSHOT.json'),'current_edition_correction_sha256':sha(A/'CURRENT_EDITION_CORRECTION.json'),'current_edition':{name:binding(A/'current_edition'/name) for name in sorted(v['NAMES'])}}
 v['authenticate_source_bindings'](A,A,{'edition_mode':'documented_correction','source_bindings':source})
 for filename in ['MATH_GATE.json','PRIORITY_ADJUDICATION.json']:
  g=json.loads((A/filename).read_text());need(g.get('pr')==1283 and g.get('problem_id')==30005434 and g.get('original_head')==snapshot['head'] and g.get('status')=='PASS','Actual gate required '+filename)
 priority=json.loads((A/'PRIORITY_ADJUDICATION.json').read_text())
 need(priority['mathematical_gate_sha256']==sha(A/'MATH_GATE.json') and priority['current_edition_correction_sha256']==source['current_edition_correction_sha256'],'Gate bindings differ')
 registry,files=curated(v)
 metadata=json.loads((A/'reviews/context_assembly/METADATA_PROPOSAL.json').read_text());v['metadata_contract'](metadata)
 need(json.loads((P/'zenodo-deposit.json').read_text())['metadata']==metadata,'Actual metadata drift')
 need((P/'manuscript/main.tex').read_bytes()==(A/'reviews/note_scope_revision1/main.tex').read_bytes(),'Current source revision drift')
 context={'edition_mode':'documented_correction','schema':'math-pr1283-current-context-v1','pr':1283,'problem_id':30005434,'original_head':snapshot['head'],'original_branch':snapshot['branch'],'original_body_sha256':snapshot['body_sha256'],'title':metadata['title'],'expected_pdf_pages':4,'source_date_epoch':'1792195200','edition_text':{},'structured_records':{},'disclosures':{'firstness_claim':False,'current_openness_claim':False,'ai_assisted':True,'unrefereed':True},'metadata':metadata,'publication_text':json.loads((A/'reviews/context_assembly/PUBLICATION_TEXT_PROPOSAL.json').read_text()),'tracker':{'original_problem':'30005434 (OWR-12697693-005): Dietzel, OWR9/2023 p545 Problem3, semilattice realizations by meet-semibraces; https://doi.org/10.4171/OWR/2023/9 ; https://github.com/AlecKriebel/Math/pull/1283','notes':'Full printed-axiom existence answer, using the exact operation recorded by Castiglioni-San Martin2016 Example3.5(4), with Rump framework credit and separate older meet-monoid convention. Attributed verification; no new solution, operation, firstness or current-openness claim. AI-assisted, unrefereed preprint and scoped verification package.'},'authored_freezes':registry,'portable_files':files,'diagnostic_replays':[{'program':p,'mode':'normal_O_OO','result':r,'output_mode':'stdout','scope':s,'layout':'isolated','arguments':[],'comparison':'bytes_exact'} for p,r,s in REPLAYS],'gate_bindings':{k:sha(A/n) for k,n in [('math_gate_sha256','MATH_GATE.json'),('priority_adjudication_sha256','PRIORITY_ADJUDICATION.json'),('submitted_snapshot_sha256','SUBMITTED_SNAPSHOT.json')]},'source_bindings':source}
 if not bootstrap:
  context['document_bindings']={k:sha(P/n) for k,n in [('source_sha256','manuscript/main.tex'),('pdf_sha256','output/pdf/main.pdf'),('compile_receipt_sha256','COMPILE_RECEIPT.json'),('layout_receipt_sha256','LAYOUT_VERIFICATION.json')]}
  pages=[int(line.split(':',1)[1]) for line in subprocess.check_output(['pdfinfo',str(P/'output/pdf/main.pdf')],text=True).splitlines() if line.startswith('Pages:')]
  need(pages==[4],'Actual PDF pages differ; explicitly revise expected pages after visual inspection')
 return context

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--bootstrap',action='store_true');parser.add_argument('--finalize',action='store_true');parser.add_argument('--replay-diagnostics',action='store_true');args=parser.parse_args()
 need(not(args.bootstrap and args.finalize),'Choose one phase')
 context=assemble(args.bootstrap)
 path=A/'CURRENT_PR1283_CONTEXT.json'
 if args.bootstrap or args.finalize:
  need(not any((P/n).exists() for n in ['STAGE_INTENT.json','PUBLISH_INTENT.json','PUBLICATION_RECEIPT.json','FINAL_REVIEW_GATE.json']),'No assembly after final review/service state')
  previous=path.read_bytes() if path.exists() else None;save(path,context)
  try:
   if args.finalize:checker()['load_context'](A,P)
  except BaseException:
   if previous is None:path.unlink()
   else:path.write_bytes(previous)
   raise
 replay=checker()['replay_diagnostics'](A,context) if args.replay_diagnostics else []
 print(json.dumps({'status':'PASS','phase':'bootstrap' if args.bootstrap else 'final' if args.finalize else 'read_only','context_sha256':sha(path) if path.exists() else None,'families':len(context['authored_freezes']),'portable_files':len(context['portable_files']),'diagnostic_runs':replay},indent=2))
if __name__=='__main__':main()
