#!/usr/bin/env python3
"""Seal reviewer-owned artifacts, reading public sources without modification."""
from pathlib import Path
import hashlib,json,datetime,zipfile
HERE=Path(__file__).resolve().parent
PAPER=HERE.parent.parent
PROGRAMME=PAPER.parent.parent
SRC=PAPER/'sources'
PKG=SRC/'published-source/satoh_filtration_verification'
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha(p): return sha_bytes(p.read_bytes())
def binding(p):
 return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt=json.loads((SRC/'receipt.json').read_text())
assert receipt['complete'] and receipt['queue_matched']
assets=[]
for row in receipt['files']:
 p=SRC/row['name']; b=p.read_bytes()
 assert len(b)==row['bytes']
 assert hashlib.md5(b).hexdigest()==row['md5']
 assert sha_bytes(b)==row['sha256']
 assets.append({**binding(p),'url':row['url'],'md5':hashlib.md5(b).hexdigest(),'receipt_match':True})
assert sha(SRC/'record.json')==receipt['record_sha256']
assert (SRC/'satoh_filtration_counterexamples.pdf').read_bytes()==(PKG/'satoh_filtration_counterexamples.pdf').read_bytes()
replay=json.loads((HERE/'replay-results.json').read_text())
current={str(p.relative_to(PKG)):sha(p) for p in sorted(PKG.rglob('*')) if p.is_file()}
assert len(current)==107 and current==replay['source_sha256']
assert replay['all_sources_unchanged'] and not replay['full_package_replay_claimed']
manifest=json.loads((PKG/'PACKAGE_MANIFEST.json').read_text())
assert len(manifest['files'])==manifest['file_count']==106
for row in manifest['files']:
 p=PKG/row['path']
 assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
assert set(current)=={r['path'] for r in manifest['files']}|{'PACKAGE_MANIFEST.json'}
with zipfile.ZipFile(SRC/'satoh_filtration_verification.zip') as z:
 members=[i for i in z.infolist() if not i.is_dir()]
 assert len(members)==107 and {i.filename for i in members}==set(current)
 for i in members: assert sha_bytes(z.read(i))==current[i.filename]
custody={
 'record_id':'23387442','checked_utc':now,'receipt':binding(SRC/'receipt.json'),
 'record':binding(SRC/'record.json'),'assets':assets,
 'embedded_pdf_identical':True,'zip_regular_members':107,'archive_matches_every_extracted_file':True,
 'package_manifest':binding(PKG/'PACKAGE_MANIFEST.json'),'manifest_payload_entries_checked':106,
 'all_107_sources_unchanged_since_replay_snapshot':True,'source_sha256':current,
 'mathematical_source_bindings':[binding(PKG/'satoh_filtration_counterexamples.tex'),binding(PKG/'native/unsolved_math_prioritization/attempts/30003703/release/PROOF.md')],
 'scope':'Integrity checks read bytes; they do not constitute reading or accepting historical assessment bodies. No source file modified.'}
write(HERE/'SOURCE_CUSTODY.json',custody)
primaryreceipt=PAPER/'reviews/scope/primary-source-receipts.json'
primarycache=primaryreceipt.parent/'cache/primary-sources'
coverage={
 'owr2018-02.pdf':'Entire Satoh contribution, printed pp.87–90; definitions and literal all-k conjecture pp.88–89. Original problem source.',
 'satoh-v2.pdf':'Section 3 matrix-entry algebra/action/finite-generation interfaces, section 4.2 full J/J^(k+1) definition, Theorem 6.3 low-degree comparison. Author v2, not final journal body.',
 'burde-v2.pdf':'Identity (4), Theorem 4.14 and surrounding historical attribution; classical identity matches up to sign/variables. Current proof is self-contained.'}
rows=[]
for row in json.loads(primaryreceipt.read_text()):
 p=primarycache/row['name']
 assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
 r={**binding(p),'url':row['url'],'version':row['version'],'receipt_match':True,'read_coverage':coverage[row['name']]}
 txt=p.with_suffix('.txt')
 if txt.exists(): r['extracted_text']=binding(txt)
 rows.append(r)
write(HERE/'PRIMARY_SOURCE_LEDGER.json',{'checked_utc':now,'receipt':binding(primaryreceipt),'sources':rows,'limitations':['Pinned author-preprint versions are not substituted for final journal editions.','No exhaustive priority or post-2018 continuously-open-status certification.','No sibling scope conclusion read.']})
fresh=json.loads((HERE/'fresh-control-results.json').read_text())
assert fresh['assertions']==4502 and fresh['script_sha256']==sha(HERE/'fresh_controls.py')
assert len(replay['runs'])==3
assert all(r['exit_code']==0 and r['json_exact_match'] for r in replay['runs'])
for r in replay['runs']:
 assert sha(PKG/r['script'])==r['script_sha256']
 assert sha(PKG/r['expected_output'])==r['expected_output_sha256']
log=HERE/'RESEARCH_LOG.md'
with log.open('a') as f:
 f.write(f'- {now} — 100%: Adversarial review complete, exact-claim PASS. No substantive defect or unresolved proof gap identified. Rechecked receipt size/MD5/SHA, record hash, all 107 ZIP/extracted files, 106 manifest payload entries, embedded main PDF equality and unchanged-source replay snapshot. Bound report, primary ledger, controls and selected replay evidence; no source repair or publication mutation. Limits: unrefereed AI review, selected mathematical replay, no priority certificate.\n')
artifactnames=['REVIEW.md','RESEARCH_LOG.md','SOURCE_CUSTODY.json','PRIMARY_SOURCE_LEDGER.json','fresh_controls.py','fresh-control-results.json','fresh-controls.stdout.txt','fresh-controls.stderr.txt','replay_selected.py','replay-results.json','replay-driver.stdout.txt','replay-driver.stderr.txt','replay-native.stdout.txt','replay-native.stderr.txt','replay-freegroup.stdout.txt','replay-freegroup.stderr.txt','replay-matrix_ideal.stdout.txt','replay-matrix_ideal.stderr.txt','paper.txt','seal_review.py']
evidence={
 'record_id':'23387442','sealed_utc':now,'completion_percent':100,
 'objective':binding(PROGRAMME/'GOAL.md'),'artifacts':[binding(HERE/n) for n in artifactnames],
 'fresh_exact_assertions':4502,'selected_unmodified_replays':3,'all_selected_replays_pass':True,
 'source_files_unchanged':107,'mathematical_defects':[],
 'independence':'Fresh proof reconstruction and controls preceded submitted-helper reading. No sibling or historical assessment bodies read; incidental status names in wrapper/manuscript disclosed in REVIEW.md.'}
write(HERE/'evidence.json',evidence)
verdict={
 'record_id':'23387442','title':"Counterexamples to Satoh's SL(2) representation-filtration conjecture",'version':'1.0','publication_date':'2026-10-15',
 'review_type':'independent adversarial mathematical review','status':'PASS','verdict':'PASS','completed_utc':now,'completion_percent':100,
 'pdf_sha256':sha(SRC/'satoh_filtration_counterexamples.pdf'),'source_zip_sha256':sha(SRC/'satoh_filtration_verification.zip'),
 'source_receipt':binding(SRC/'receipt.json'),'report':binding(HERE/'REVIEW.md'),'evidence':binding(HERE/'evidence.json'),'source_custody':binding(HERE/'SOURCE_CUSTODY.json'),
 'exact_checked_claims':[
  'For every integer n>=4, fixing all generators except x4 -> x4 w, w=[[[x1,x2],[x1,x3]],x1], defines an automorphism in D_n(5)\\A_n(5).',
  'For every integer n>=3, fixing all generators except x3 -> x3 v, v=[[[x1,x2],[x1,[x1,x2]]],x1], defines an automorphism in D_n(6)\\A_n(6).',
  'A_n(k) uses the integral lower central subgroup Gamma_(k+1). D_n(k) is the action kernel on the full J/J^(k+1) in the rational SL(2,C) matrix-entry algebra.',
  'The actual universal matrix ideal containments are M(w)-I in Mat2(J^6) and M(v)-I in Mat2(J^7).',
  'Integral Magnus coefficients and independent unitriangular evaluations prove w not in Gamma_6 and v not in Gamma_7.',
  'These constructions contradict the all-degree equality literally formulated in the inspected 2018 Satoh report for every rank n>=3.'
 ],
 'assumptions':['Free group with the stated ordered generators and spare-generator rank bounds.','Rational algebra of complex SL(2) matrix-entry functions, not trace or character algebra.','Full ideal quotient J/J^(k+1), integral lower central series, stated commutator convention.'],
 'strongest_verified_result':'The two exact rank/degree families in Theorem 1, with universal ideal-power and integral nonmembership proofs.',
 'exact_remaining_mathematical_gap':None,'gaps':[],'defects':[],
 'controls':{'fresh_assertions':4502,'submitted_mathematical_helpers_replayed':3,'replay_outputs_exact_match':True,'all_107_source_files_unchanged':True},
 'limits':['AI review does not constitute human peer review or formal proof verification.','No firstness or exhaustive novelty certification; primary author versions are distinguished from unavailable final journal bodies.','No degree-five conclusion at rank three, every-degree failure, larger-matrix extension, character-algebra conclusion, or other Andreadakis conjecture.','Only three selected mathematical helpers replayed, not historical status/priority wrapper.'],
 'source_repair_performed':False,'external_communication_performed':False,'publication_mutation_performed':False}
write(HERE/'verdict.json',verdict)
# Independently reread the artifact bindings after serialization.
for row in json.loads((HERE/'evidence.json').read_text())['artifacts']:
 p=Path(row['path']); assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
for k in ['report','evidence','source_custody','source_receipt']:
 row=verdict[k]; assert sha(Path(row['path']))==row['sha256']
print(json.dumps({'status':'PASS','completed_utc':now,'files':{n:sha(HERE/n) for n in ['REVIEW.md','verdict.json','evidence.json','SOURCE_CUSTODY.json','PRIMARY_SOURCE_LEDGER.json']},'source_files_unchanged':107},indent=2))
