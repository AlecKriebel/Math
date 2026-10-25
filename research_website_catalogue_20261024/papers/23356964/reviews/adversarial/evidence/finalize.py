#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,datetime
P=Path(__file__).resolve().parents[1];B=P.parents[1];S=B/'sources';C=S/'published-source/generic-wreath-hyperfiniteness-verification'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
c=json.loads((P/'evidence/custody.json').read_text());seal=json.loads((P/'evidence/pre-helper-seal.json').read_text())
for f in c['public_assets']:assert sha(S/f['name'])==f['sha256']
for f in c['members']:assert sha(S/f['source_path'])==f['sha256']
for f in seal['files']:assert sha(P/f['path'])==f['sha256']
objective=Path('/Users/alec/.codex/attachments/97d02095-52a0-400f-a038-cbc727c7c885/goal-objective.md')
scopes={
'cjmst-v13.pdf':('Sections2/3 definitions and finite-move criterion; Section5 through Cor5.5 with proof; Theorem7.3 with proof and Cor7.5','Load-bearing: finite Borel dimension for fixed-rank abelian actions without freeness; compatible union with varying dimensions; hyperfiniteness for all local-polynomial-growth actions'),
'owr-2025-02.pdf':('Complete Iyer/Shinko contribution printed114–115, including Question3','Exact original question and distinction from measured hyperfiniteness'),
'iyer-shinko-v1.pdf':('Introduction, action-space/dimension definitions, Theorems18–19 and proofs','Baseline hypothesis and attribution, not the main black-box input'),
'agw-v1.pdf':('Lifting setup, Theorem3.3 and equation3.7 with proof','Attribution predecessor; authenticated2006 author preprint only, publisher2008 body not acquired'),
'doucha-v3.pdf':('Proposition2.12 including part3 and partition/subshift perturbation proof','Attribution predecessor; current direct lifting proof independently checked'),
'dmt-v1.pdf':('Boolean action coding, Prop3.2, DefA.3/A.5 and PropA.7 with proof','Generic finite-extension framework and attribution'),
'dmt-v2.pdf':('Boolean action coding, Prop3.2, DefA.3/A.5 and PropA.7 with proof','Revision-bound check of same attribution interface')}
ledger=[]
for p in c['primary_sources']:
 scope,role=scopes[p['name']]
 ledger.append(p|{'read_scope':scope,'role':role,'complete_work_read':False})
(P/'evidence/primary-interface-ledger.json').write_text(json.dumps({'utc':now,'sources':ledger,'unavailable':[{'name':'AGW2008 publisher PDF','url':'https://www.ams.org/journals/tran/2008-360-07/S0002-9947-08-04450-4/S0002-9947-08-04450-4.pdf','result':'web fetch403 Forbidden','effect':'Pinned2006 author preprint contains cited passage. Current manuscript supplies direct lifting proof; no unresolved load-bearing mathematical gap.'}],'load_bearing_source_gaps':[]},indent=2)+'\n')
v={'schema_version':1,'record_id':'23356964','role':'independent_adversarial','status':'PASS','verdict':'PASS','completion_percent':100,'completed_utc':now,
'mandatory_objective':{'path':str(objective),'sha256':sha(objective)},
'source_binding':{'receipt_path':str(S/'receipt.json'),'receipt_sha256':c['receipt_sha256'],'record_path':str(S/'record.json'),'record_sha256':c['record_sha256'],'metadata':c['metadata'],'record_created_utc':c['record_created'],'public_assets':c['public_assets'],'main_pdf_pages':5,'main_tex_sha256':sha(C/'note.tex'),'mathematical_support_sha256':sha(C/'source/author/PROOF.md'),'outer_regular_members':121,'nested_regular_members':51,'nested_archives':3,'embedded_pdf_identical_to_main':True,'all_source_bytes_unchanged_at_completion':True},
'exact_claim':'A dense G_delta subset of the full Polish action space Act(Z wr Z, Cantor) has hyperfinite orbit equivalence relation on the entire Cantor space. Restricted countable discrete wreath product, not an unrestricted product.',
'strongest_verified_claim':'The generic full-space theorem and the auxiliary theorem: every Borel W-action on a standard Borel X admitting a Borel equivariant p:X->Zhat for the shift character has hyperfinite whole-space orbit relation; stabilizers allowed and p need not be onto.',
'exact_remaining_gap':None,'substantive_defects':[],
'independence':{'pre_helper_seal_utc':seal['utc'],'pre_helper_seal_sha256':sha(P/'evidence/pre-helper-seal.json'),'fresh_controls_before_helper_inspection_or_execution':True,'sibling_or_dedicated_historical_assessment_bodies_read':False,'incidental_exposure':'Current manuscript and necessary mathematical PROOF include historical status/priority/approach/failure-mode language; not adopted as verdicts. Raw-primary receipts supply provenance only. Root warned of historical ACCEPTANCE wrapper; that path was not executed.','strict_source_blindness_claimed':False,'interruption_handling':'Completed controls and screenshots preserved; no live23356964 process or unresolved execution handle observed on resumption; no completed check restarted solely because of interruption.'},
'evidence':{'fresh_code':'evidence/fresh_controls.py','fresh_results':'evidence/fresh-controls.json','fresh_prefix_signed_checks':10108,'finite_quotient_models':4,'slab_width_cases':18,'proof_review':'REVIEW.md','custody':'evidence/custody.json','primary_interfaces':'evidence/primary-interface-ledger.json','selective_replay_receipt':'evidence/selective-replay-receipt.json','unchanged_mathematical_programs_replayed':['source/author/checks.py','source/independent_review_2/independent_diagnostics.py','audits/slab/boundary_diagnostics.py'],'outer_integrity_verified':True,'full_publication_wrapper_run':False},
'limitations':['AI-assisted review only, not independent human peer review or a formal proof certificate.','Does not assert hyperfiniteness of every Borel W-action without the height factor.','Does not assert a single comeager conjugacy class, a G_delta characterization of all hyperfinite actions, or a uniform Borel choice of factors/exhaustions across the action space.','Finite quotient/prefix controls and program replays do not prove Baire category or infinite Borel hyperfiniteness; those steps are audited analytically using the exact primary imports.','Finite equivalence-relation exhaustions are Borel, not asserted clopen or continuous.','AGW2008 publisher body inaccessible; pinned2006 preprint checked and current direct proof removes dependency.','No first-priority, continued-openness or journal-suitability certification.','Historical acceptance/priority bodies and full historical publication wrapper not read or replayed.'],
'follow_up':None,'promotion_authorized':False,'public_or_external_mutations':False,'report_sha256':sha(P/'REVIEW.md')}
(P/'verdict.json').write_text(json.dumps(v,indent=2)+'\n')
with (P/'LOG.md').open('a') as f:f.write('\n'+now+' — 100%: Independent adversarial review complete: PASS for exact generic full-action-space and height-conditioned Borel theorems. Complete proof audit, original primary interfaces, pre-helper fresh controls, selective unchanged math replay,172-member custody and all limitations sealed. No substantive gap found, no source repair or public mutation; no inherited historical acceptance used. Source and pre-helper hashes revalidated at completion.\n')
files=[]
for f in sorted(P.rglob('*')):
 if not f.is_file() or 'replay-work' in f.parts or '__pycache__' in f.parts or f.name=='evidence-manifest.json':continue
 files.append({'path':f.relative_to(P).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)})
m={'schema_version':1,'record_id':'23356964','role':'adversarial','completed_utc':now,'completion_percent':100,'artifact_count':len(files),'files':files,'excluded_scratch':'replay-work/; all substantive evidence and exact replay commands retained outside scratch.'}
(P/'evidence-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'verdict':'PASS','completed_utc':now,'artifact_count':len(files),'report_sha256':sha(P/'REVIEW.md'),'verdict_sha256':sha(P/'verdict.json'),'manifest_sha256':sha(P/'evidence-manifest.json')},indent=2))
