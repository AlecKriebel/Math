#!/usr/bin/env python3
"""Finite custody seal only; no mathematical execution or outside writes."""
from pathlib import Path
import datetime, hashlib, json
N = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23443301/reviews/adversarial-sol')
S = N.parent.parent/'sources'

def meta(p):
    if p.is_symlink() or not p.is_file():
        raise ValueError('ordinary file required')
    b=p.read_bytes()
    return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def write(name,obj):
    with (N/name).open('x') as f:
        json.dump(obj,f,indent=2); f.write('\n')

stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
for name in ('OWNED_MANIFEST.json','FINAL.json'):
    if (N/name).exists():
        raise ValueError('terminal already exists; no resealing')
initial=json.loads((N/'INITIAL_SEAL.json').read_text())
for field in ('source_PDF','controlling_TeX'):
    row=initial[field]
    if meta(N/row['path'])!={k:row[k] for k in ('bytes','SHA256')}:
        raise ValueError('initial source changed')
for field in ('INITIAL','actual_hand_controls'):
    row=initial[field]
    if meta(N/row['path'])!={k:row[k] for k in ('bytes','SHA256')}:
        raise ValueError('frozen initial result changed')
if (N/'native-run/exit.txt').read_text()!='0\n' or (N/'native-run/stderr.txt').read_bytes()!=b'':
    raise ValueError('actual native execution qualification changed')
with (N/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+stamp+' — Finite family sealed. Completion estimate:100%. Full original claim/independent proof, seven hand controls, one unchanged native ordinary run and selected primary interfaces recorded. Findings withheld pending root comparison; no other family findings read. No further execution/writes planned.\n')
paths=sorted(p for p in N.rglob('*') if p.is_file())
dirs=sorted(p.relative_to(N).as_posix() for p in N.rglob('*') if p.is_dir())
if len(paths)!=42 or dirs!=['native-run','primary','reading'] or any(p.is_symlink() for p in N.rglob('*')):
    raise ValueError('unexpected finite namespace')
write('OWNED_MANIFEST.json',{'schema':'polynomial-compatibility-adversarial-manifest-v1','UTC':stamp,'root':str(N),'files':[{'path':p.relative_to(N).as_posix(),**meta(p),'mode':oct(p.stat().st_mode&0o777)} for p in paths],'exact_terminal_files':['OWNED_MANIFEST.json','FINAL.json'],'total_files':44,'child_directories':dirs,'no_future_or_subtree_exclusions':True})
script=S/'published-source/container-001/tree/draft_pr_actual_claims_1100_1200_20261017/audits/pr1141_30006210/reviews/covariance_01/exact_controls.py'
proof=script.parent.parent.parent/'inputs/PROOF.md'
write('FINAL.json',{'schema':'polynomial-compatibility-adversarial-final-v1','UTC':stamp,'record_id':23443301,'sheet_row':159,'status':'FAMILY_COMPLETE_FINDINGS_WITHHELD_PENDING_ROOT_COMPARISON','REPORT':{'path':'REPORT.md',**meta(N/'REPORT.md')},'MANIFEST':{'path':'OWNED_MANIFEST.json',**meta(N/'OWNED_MANIFEST.json')},'INITIAL_SEAL':{'path':'INITIAL_SEAL.json',**meta(N/'INITIAL_SEAL.json')},'source_first_full_PDF_pages':4,'source_first_full_TeX_lines':288,'fresh_own_native_pages_viewed':4,'prior_source_manuscript_priority_and_archived_checks_assertions_exposed':True,'peer_root_archived_opinion_or_stored_result_bodies_read':False,'actual_written_independent_universal_derivation_and_seven_hand_controls_frozen_before_support':True,'native_ordinary_runs':1,'native_exit_history':[0],'native_script':{'path':str(script),**meta(script)},'opaque_hash_only_PROOF_input':{'path':str(proof),**meta(proof)},'native_result':{'path':'native-run/result.json',**meta(N/'native-run/result.json')},'primary_bodies':[{'path':'primary/'+name,**meta(N/'primary'/name)} for name in ('osss.body','llll.body','owr-pdf.body')],'web_OWR_reader_500_then_ordinary_official_GET_200_disclosed':True,'finite_native_checks_not_universal_proof':True,'novelty_priority_or_human_peer_review_certification':False,'source_W_Git_Sheet_old_packet_mutations_or_outreach':False,'native_version':'1.0.0','printed_version_label_present':False,'declared_date':'2026-10-17','created':'2026-10-17T23:12:45.847488+00:00','native_file_order':['polynomial-compatibility-source-and-verification.zip','polynomial-compatibility.pdf'],'native_authored_rights':'CC BY4.0; third-party rights retained; no MIT inferred','owned_files':44,'owned_child_directories':dirs,'AA':None,'follow_up':None,'publication_authority':False,'completion_percent_family':100})
print(json.dumps({'FINAL':meta(N/'FINAL.json'),'MANIFEST':meta(N/'OWNED_MANIFEST.json'),'REPORT':meta(N/'REPORT.md'),'files':44,'child_directories':dirs}))
