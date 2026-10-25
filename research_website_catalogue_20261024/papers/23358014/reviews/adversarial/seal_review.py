#!/usr/bin/env python3
"""Read-only public-source verification and reviewer-owned final evidence seal."""
from pathlib import Path
import hashlib,json,datetime,zipfile,subprocess
HERE=Path(__file__).resolve().parent; PAPER=HERE.parent.parent; PROGRAMME=PAPER.parent.parent
SRC=PAPER/'sources'; PKG=SRC/'published-source/critical_wave_verification'
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha(p):return sha_bytes(p.read_bytes())
def bind(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt=json.loads((SRC/'receipt.json').read_text());assets=[]
for r in receipt['assets']:
 p=SRC/r['name'];b=p.read_bytes()
 assert len(b)==r['bytes'] and hashlib.md5(b).hexdigest()==r['md5'] and sha_bytes(b)==r['sha256']
 assets.append({**bind(p),'md5':r['md5'],'url':r['url'],'receipt_match':True})
assert sha(SRC/'record.json')==receipt['record_sha256']
assert sha(SRC/'critical_wave_growth.pdf')=='a68d8d47dcf625f9ab8818924071200bff2b2280d67665e1e67dd7b83effe988'
assert sha(SRC/'critical_wave_verification.zip')=='1da933750640177045808de748dd7f5732c33277377285b688a411f9f89771a0'
initial=json.loads((HERE/'initial-source-hashes.json').read_text())
current={str(p.relative_to(PKG)):sha(p) for p in sorted(PKG.rglob('*')) if p.is_file()}
assert len(current)==113 and current==initial
replay=json.loads((HERE/'replay-results.json').read_text())
assert replay['source_sha256']==current and replay['all_113_sources_unchanged']
manifest=json.loads((PKG/'FILE_MANIFEST.json').read_text())
assert len(manifest['files'])==112
for r in manifest['files']:
 p=PKG/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
assert set(current)=={r['path'] for r in manifest['files']}|{'FILE_MANIFEST.json'}
with zipfile.ZipFile(SRC/'critical_wave_verification.zip') as z:
 rows=[i for i in z.infolist() if not i.is_dir()]
 assert len(rows)==113 and {r.filename for r in rows}==set(current)
 for r in rows:assert sha_bytes(z.read(r))==current[r.filename]
 assert not any(r.filename.lower().endswith(('.pdf','.zip','.tar','.gz','.7z')) for r in rows)
pdfinfo=subprocess.run(['pdfinfo',str(SRC/'critical_wave_growth.pdf')],capture_output=True,text=True,check=True).stdout
pages=int(next(line.split(':',1)[1].strip() for line in pdfinfo.splitlines() if line.startswith('Pages:')))
assert pages==6
write(HERE/'SOURCE_CUSTODY.json',{'record_id':'23358014','checked_utc':now,'record':bind(SRC/'record.json'),'receipt':bind(SRC/'receipt.json'),'assets':assets,'published_pdf_pages':pages,'archive_regular_members':113,'all_zip_members_match_extracted_bytes':True,'all_113_sources_unchanged':True,'extra_reader_pdf_count':0,'nested_archives':0,'manifest':bind(PKG/'FILE_MANIFEST.json'),'manifest_payload_entries_checked':112,'source_sha256':current,'mathematical_source_bindings':[bind(PKG/'manuscript/critical_wave_growth.tex'),bind(PKG/'original_submission/COUNTEREXAMPLE.md')],'scope':'Hashing opaque historical files authenticates custody; their assessment bodies were not read. No public source was modified.'})
coverage={
 'km-v1.pdf':'Model and spaces; Lemma 2.9/Duhamel; local existence/uniqueness interfaces and global Theorem 3.7 statement; control convention r=1 for beta2=0; Proposition 4.4, Lemma 4.6; tangent/ordinary-critical cone and substitute j-second-variation definitions; Theorem 4.17 L-infinity localization. Pinned author v1, not final journal body.',
 'owr-2021-09.pdf':'Full Meinlschmidt contribution printed pp438–440: model, optional velocity cost, constraint, strict second-order condition, L2 neighborhood and precise beta2=0 open-question context.',
 'bss-2009.pdf':'Theorem 1.1 and Corollary 1.2, surrounding finite-time compact-boundary applicability and proof setup. Exact admissible (p,q,gamma)=(4,12,1) checked. Not a reproof of the entire microlocal theorem.',
 'ct-2015.pdf':'Example 4.16, its calculation and following Definition 4.17/extended-cone discussion. Attribution to Dunn via this inspected source; not Dunn original or the separate CT2012 body.',
 'cw-v1.pdf':'Theorem 4.4 with NDC and surrounding role of generalized Legendre condition. Background comparison, not a load-bearing theorem for the example.',
 'bw-v1.pdf':'Theorem 2.6 NDC and Lemma 2.7, supporting exact smooth-plus-nonsmooth normalized expression. Pinned author v1; background interface.',
 'ww-v1.pdf':'Title/abstract and introduction describing nonuniformly convex integrands, measure-space conditions and L1 quadratic growth. Background credit only, no wholesale transfer of hypotheses to the wave example.',
 'hsw-2012.pdf':'Directional/group sparsity setup and mixed-norm subgradient/optimality discussion. Background credit; current sparse subgradient is computed directly and matches KM Proposition 4.4.',
 'chw-2017.pdf':'Extended cone definition (5.1), Theorem 5.1 and surrounding regularized/extended-cone comparison. Parabolic model context, no transplant of its theorem to the wave model.'}
preceipt=PAPER/'reviews/scope/primary-source-receipts.json';cache=preceipt.parent/'cache/primary-sources'
primaries=[]
for r in json.loads(preceipt.read_text()):
 p=cache/r['name'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
 row={**bind(p),'url':r['url'],'version':r['version'],'receipt_match':True,'read_coverage':coverage[r['name']]}
 if p.with_suffix('.txt').exists():row['extracted_text']=bind(p.with_suffix('.txt'))
 primaries.append(row)
assert len(primaries)==9
write(HERE/'PRIMARY_SOURCE_LEDGER.json',{'checked_utc':now,'receipt':bind(preceipt),'sources':primaries,'web_metadata_crosschecks':['https://arxiv.org/abs/1907.02744v1','https://www.numdam.org/articles/10.1016/j.anihpc.2008.12.004/','https://publications.mfo.de/handle/mfo/3850'],'limitations':['No exhaustive priority audit or full final-edition verification claimed.','Each source read only to the coverage explicitly recorded.','No sibling scope findings read.']})
fresh=json.loads((HERE/'fresh-control-results.json').read_text()); assert fresh['script_sha256']==sha(HERE/'fresh_controls.py')
numeric=sum(v for k,v in fresh['counts'].items() if k.startswith('high_precision_') or k in ['negative_shifted_pulse_restores_first_order','negative_beta2_restores_growth'])
exact=fresh['assertions']-numeric
assert (exact,numeric)==(13201,428)
assert len(replay['runs'])==5 and replay['total_submitted_assertions']==5575
for r in replay['runs']:
 assert r['exit_code']==0 and r['all_mathematical_fields_exact_match']
 assert sha(PKG/r['script'])==r['script_sha256'] and sha(PKG/r['expected'])==r['expected_sha256']
with (HERE/'RESEARCH_LOG.md').open('a') as f:
 f.write('- '+now+' — 100%: Independent adversarial review complete and sealed, exact-claim PASS. No substantive defect or unresolved proof gap identified. Receipt size/MD5/SHA and record hash, six-page PDF, all 113 ZIP/source files, 112 manifest payload hashes and unchanged initial/replay snapshots verified. Bound full report, primary interfaces, 13,201 exact fresh assertions, 428 numerical diagnostics and five unmodified selected replays. No PDE simulation/numerical PDE constant/priority certification or publication mutation.\n')
names=['REVIEW.md','RESEARCH_LOG.md','SOURCE_CUSTODY.json','PRIMARY_SOURCE_LEDGER.json','initial-source-hashes.json','fresh_controls.py','fresh-control-results.json','fresh-controls.stdout.txt','fresh-controls.stderr.txt','replay_selected.py','replay-results.json','replay-driver.stdout.txt','replay-driver.stderr.txt','paper.txt','seal_review.py']
for r in replay['runs']:names.extend([f"replay-{r['name']}.stdout.txt",f"replay-{r['name']}.stderr.txt"])
write(HERE/'evidence.json',{'record_id':'23358014','sealed_utc':now,'completion_percent':100,'objective':bind(PROGRAMME/'GOAL.md'),'artifacts':[bind(HERE/n) for n in names],'fresh_exact_assertions':exact,'fresh_high_precision_diagnostics':numeric,'submitted_assertions':5575,'selected_unmodified_replays':5,'source_files_unchanged':113,'defects':[],'independence':'Independent proof reconstruction and fresh controls completed before submitted checker reading. No current sibling/scope or dedicated historical opinion bodies read; necessary incidental status wording is disclosed in the report.'})
verdict={'record_id':'23358014','title':'Failure of strong quadratic growth in unregularized sparse control of a critical wave equation','version':'1.0','publication_date':'2026-10-14','review_type':'independent adversarial mathematical review','status':'PASS','verdict':'PASS','completed_utc':now,'completion_percent':100,'pdf_sha256':sha(SRC/'critical_wave_growth.pdf'),'source_zip_sha256':sha(SRC/'critical_wave_verification.zip'),'source_receipt':bind(SRC/'receipt.json'),'report':bind(HERE/'REVIEW.md'),'evidence':bind(HERE/'evidence.json'),'source_custody':bind(HERE/'SOURCE_CUSTODY.json'),
 'exact_checked_claims':[
  'On the 3D unit ball with T=1, zero Dirichlet/initial data, real defocusing quintic wave, gamma=beta1=1 and beta2=0, for every fixed sufficiently small positive timewise spatial-L2 cap rho and every finite nu>=0, target pi*e has zero as unique global optimizer, with gap at least ||u||_L1(H)^3/(12*rho^2).',
  'The ordinary critical cone at zero is exactly {0}, so the source substitute strict second-variation condition on nonzero critical directions is vacuous.',
  'Centered pulses h*e on |t-1/2|<h have L2(H)^2 norm 2*h^3 and actual nonlinear cost gap (pi^2/3+2/pi^2)*h^4+O(h^6), proving no positive L2-squared growth in either L2 or L-infinity neighborhoods.',
  'Global optimizers exist for every target d in H and finite nu>=0 in this capped small-input model; every optimizer at target (pi+epsilon)*e has L2(H) norm divided by epsilon tending to infinity.',
  'Local L1(H)-squared growth holds with coefficient 1/(4*pi^2). Arbitrary small target changes give every optimizer L1(H)=O(epsilon), L2(H)=O(sqrt(epsilon)), uniformly in nu.',
  'Along positive radial target changes, every optimizer has L1(H)=Theta(epsilon) and c*epsilon^(3/4)<=L2(H)<=C*epsilon^(1/2), with radial lower-bound neighborhood allowed to depend on fixed nu.'
 ],
 'assumptions':['Spatial unit ball in R3, time interval [0,1], homogeneous Dirichlet boundary and zero energy initial data.','Real defocusing y^5 nonlinearity, compatible energy/Strichartz mild state.','Positive fixed sufficiently small cap on ||u(t)||_L2(B), not pointwise spatial amplitude. Bochner L1(H)/L2(H) norms.','Sparse/state penalty coefficients one, quadratic control coefficient zero, optional velocity penalty finite and nonnegative.','Positive radial epsilon limit with rho and nu held fixed; stated uniformity distinctions preserved.'],
 'strongest_verified_result':'The full Theorem 1 and Corollary 3 for the actual nonlinear small-cap model, including every-global-optimizer perturbation quantifiers and surviving local L1 growth.',
 'exact_remaining_mathematical_gap':None,'gaps':[],'defects':[],
 'controls':{'fresh_exact_assertions':exact,'fresh_high_precision_diagnostics':numeric,'selected_unmodified_helpers':5,'submitted_assertions':5575,'all_mathematical_replay_fields_match':True,'only_ignored_fields':'Dynamically emitted utc in source17 and addendum21.','all_113_source_files_unchanged':True},
 'limits':['AI review is not human peer review or formal proof verification.','No numerical PDE constant, nonlinear PDE simulation, sharp exponent bracket or exhaustive priority certification.','No perturbed optimizer uniqueness, pairwise Lipschitz selection or L-infinity convergence of perturbed optimizers.','No universal failure of unregularized growth or resolution of every beta2=0 sufficient-condition theory.','Selected mathematical replays only; no historical opinion/priority/status wrapper executed.'],
 'source_repair_performed':False,'publication_mutation_performed':False,'external_communication_performed':False}
write(HERE/'verdict.json',verdict)
for r in json.loads((HERE/'evidence.json').read_text())['artifacts']:
 p=Path(r['path']);assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
for key in ['report','evidence','source_custody','source_receipt']:
 r=verdict[key];assert sha(Path(r['path']))==r['sha256']
print(json.dumps({'status':'PASS','completed_utc':now,'source_files_unchanged':113,'hashes':{name:sha(HERE/name) for name in ['REVIEW.md','verdict.json','evidence.json','SOURCE_CUSTODY.json','PRIMARY_SOURCE_LEDGER.json']}},indent=2))
