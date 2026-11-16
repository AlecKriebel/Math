#!/usr/bin/env python3
"""Finite metadata seal; no mathematical execution or writes outside this review."""
from pathlib import Path
import datetime, hashlib, json
N=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23393139/reviews/adversarial-sol')
S=N.parent.parent/'sources'

def meta(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError('ordinary file required')
    b=path.read_bytes()
    return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def write(name,value):
    with (N/name).open('x') as f:
        json.dump(value,f,indent=2); f.write('\n')

for name in ('OWNED_MANIFEST.json','FINAL.json'):
    if (N/name).exists():
        raise ValueError('terminal exists; no resealing')
initial=json.loads((N/'INITIAL_SEAL.json').read_text())
for field in ('source_PDF','controlling_TeX','INITIAL','actual_hand_controls'):
    row=initial[field]
    if meta(N/row['path'])!={k:row[k] for k in ('bytes','SHA256')}:
        raise ValueError('frozen source/initial result changed')
code=S/'published-source/container-001/tree/ode_wellposedness_audit_01/check_auxiliary.py'
if meta(code)!={'bytes':5372,'SHA256':'a5e1a35caad1d75be7407696197ce9637213d96f235cfad4a17662cdc62ace9f'}:
    raise ValueError('inspected code changed')
if meta(N/'primary/ferudun.body')['bytes']!=212882 or hashlib.md5((N/'primary/ferudun.body').read_bytes()).hexdigest()!='112d9feb590219716908b2cf1c54e7d7':
    raise ValueError('foreign native file identity changed')
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (N/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+stamp+' — Finite family seal complete. Completion estimate:100%. INITIAL/hand controls unchanged; targeted primary interfaces recorded; native scientific execution0 with hardcoded-source-output reason. Findings withheld pending root comparison. All owned writes quiescent after seal.\n')
paths=sorted(p for p in N.rglob('*') if p.is_file())
dirs=sorted(p.relative_to(N).as_posix() for p in N.rglob('*') if p.is_dir())
if len(paths)!=39 or dirs!=['primary','reading'] or any(p.is_symlink() for p in N.rglob('*')):
    raise ValueError('unexpected finite review namespace')
write('OWNED_MANIFEST.json',{'schema':'fixed-city-adversarial-manifest-v1','UTC':stamp,'root':str(N),'files':[{'path':p.relative_to(N).as_posix(),**meta(p),'mode':oct(p.stat().st_mode&0o777)} for p in paths],'exact_terminal_files':['OWNED_MANIFEST.json','FINAL.json'],'total_files':41,'child_directories':dirs,'no_future_or_subtree_exclusions':True})
record=json.loads((S/'record.response.body').read_text())
write('FINAL.json',{'schema':'fixed-city-adversarial-family-final-v1','UTC':stamp,'record_id':23393139,'sheet_row':160,'status':'FAMILY_COMPLETE_FINDINGS_WITHHELD_PENDING_ROOT_COMPARISON','REPORT':{'path':'REPORT.md',**meta(N/'REPORT.md')},'MANIFEST':{'path':'OWNED_MANIFEST.json',**meta(N/'OWNED_MANIFEST.json')},'INITIAL_SEAL':{'path':'INITIAL_SEAL.json',**meta(N/'INITIAL_SEAL.json')},'source_first_PDF_pages_personally_read':5,'source_first_controlling_TeX_lines':192,'fresh_own_native_rasters_personally_viewed':5,'actual_universal_derivation_and_seven_hand_controls_before_support':True,'current_peer_root_science_or_archived_opinion_result_bodies_read':False,'source_manuscript_own_priority_overlap_and_review_assertions_disclosed':True,'checkpoint_pause_observed':'INITIAL boundary until root CHECKPOINT_DONE65256bfa','native_scientific_execution_count':0,'native_execution_decision':{'path':'NATIVE_EXECUTION_DECISION.md',**meta(N/'NATIVE_EXECUTION_DECISION.md')},'inspected_unchanged_126line_native_code':{'path':str(code),**meta(code)},'native_nonexecution_reason':'Normal code hardcodes HERE/AUXILIARY_RESULTS.json in immutable source; no output option. No patch/relocation/alternate campaign.','primary_bodies':[{'path':'primary/'+name,**meta(N/'primary'/name)} for name in ('aldous.body','aldous-huang.body','ferudun.body')],'all_three_ordinary_primary_PDF_GET_HTTP_status':200,'late_raw_path_only_coordination_matched_bodies_no_more_GETs':True,'native_metadata':{'version':record['metadata']['version'],'publication_date':record['metadata']['publication_date'],'created':record['created'],'license':record['metadata']['license'],'files_in_original_order':record['files']},'printed_date':'15 October2026','printed_version':'1.0.0','separate_code_license_not_inferred':True,'source_W_Git_Sheet_other_review_old_packet_mutations_or_outreach':False,'convergence_empirical_firstness_formal_or_human_review_certification':False,'owned_files':41,'owned_child_directories':dirs,'AA':None,'follow_up':None,'publication_authority':False,'completion_percent_family':100})
print(json.dumps({'FINAL':meta(N/'FINAL.json'),'MANIFEST':meta(N/'OWNED_MANIFEST.json'),'REPORT':meta(N/'REPORT.md'),'files':41,'child_directories':dirs}))
