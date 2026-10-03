"""Publish only owned PR365 math checkpoint and PR366 publication receipts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr365_2303002';B=P/'audits/pr366_2303016';paths=set()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 rel=p.relative_to(P)
 if any('private' in x or x in {'tmp','__pycache__','raw_sources'} for x in rel.parts):return
 assert p.suffix not in {'.pdf','.png','.html','.log'};paths.add(p.relative_to(R).as_posix())
assert git('branch','--show-current').strip()==b'main'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert not git('diff','--name-only','--diff-filter=U').strip()
receipt=json.loads((A/'root_original_reproduction_receipt.json').read_bytes());assert receipt['status']=='PASS' and receipt['check_count']==387 and receipt['binding_count']==29
previous=json.loads((B/'GIT_PUBLICATION_RECEIPT.json').read_bytes());assert previous['status']=='OBSERVED_FINAL_PR366_AUDIT_PUBLICATION_PASS'
assert subprocess.run(['git','merge-base','--is-ancestor',previous['published_audit_commit'],'HEAD'],cwd=R).returncode==0
now=datetime.now(timezone.utc).isoformat();criteria={'pr':365,'problem_id':2303002,'original_head':'4245f1af53840a07f43c05c928c4783bc6c3a467','accepted_status_hypothesis':'already_solved','actual_source_gate_turns':'0/5','workflow_completion_percent':50,'credited_resolution_percent':100,'new_theorem_percent':0,'root_original_checks':387,'original_paths':19,'mathematical_files':18,'nested_instances':29,'family_closures_pending':True,'whole_adversary_pending':True,'exact_live_pending':True,'actual_merge_pending':True,'post_merge_pending':True,'novelty_certified':False,'historical_all_refs_search_reproduced':False,'no_paper_zenodo_doi_tracker_release':True}
(A/'acceptance_criteria.json').write_text(json.dumps(criteria,indent=2)+'\n')
o=json.loads((P/'inventory.json').read_bytes());assert o['completed_by_descending']==23;e=next(e for e in o['items'] if e['number']==365);e.update({'audit_completion_percent':50,'audit_workflow_percent':50,'audit_disposition':'PRIMARY_AND_ANALYTICAL_PROOF_AND_ORIGINAL_REPRODUCTION_PASS_FINAL_LIVE_PENDING','original_frozen_head':criteria['original_head'],'credited_resolution_percent':100,'novel_original_problem_resolution_claimed':False,'root_original_checks':387});(P/'inventory.json').write_text(json.dumps(o,indent=2)+'\n')
note=f'{now}: PR365 source/math checkpoint50%; credited original resolution100%, new theorem0%. Fresh complete primaries, ROOT source-first and pre-code math seals, full18-file proof/implementation/history review, actual0 discovery turns/10 source-gate author files, all19 whole Git/API/mode/blob bindings/all29 nested instances and entireoriginalQUEUE405 statuscell8 only/0turns PASS; ROOT387 checks and whole3675/1667/1665 byte replays. Two independent families and new whole adversary closing; exact live/actual/post/publication pending. Program23/349=6.5903%; PR366 core audit already published11590683569346ea67151a497e798094347c8d29; observed post-publication receipt included now. No paper/Zenodo/DOI/tracker/release/outside-person communication.\n'
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'README.md']:
 with p.open('a') as f:f.write('\n'+note)
for p in A.iterdir():
 if p.is_file():add(p)
for d in [A/'snapshot',A/'root_original_streams']:
 for p in d.rglob('*'):
  if p.is_file():add(p)
for n in ['root_record_publication.py','GIT_PUBLICATION_RECEIPT.json','acceptance_criteria.json','CURRENT_ACCEPTANCE_STATUS.md','RESEARCH_LOG.md']:add(B/n)
for n in ['inventory.json','RESEARCH_LOG.md','checkpoint_366_final_publication.stdout','checkpoint_366_final_publication.stderr','checkpoint_366_final_stage.stdout','checkpoint_366_final_stage.stderr','checkpoint_366_final_commit.stdout','checkpoint_366_final_commit.stderr','checkpoint_366_final_push.stdout','checkpoint_366_final_push.stderr',Path(__file__).name]:add(P/n)
allow=P/'checkpoint_365_math_allowlist.json';paths.add(allow.relative_to(R).as_posix());allow.write_text(json.dumps({'utc':now,'explicit_owned_paths':sorted(paths),'scope':'PR365 source/math50%, final/livepending, plus observed PR366 core publication receipts; no unfinished family namespace or private/rawsource/foreign data'},indent=2)+'\n')
def foreign():
 out={}
 for row in git('ls-files','--stage','-z').split(b'\0'):
  if row:
   meta,p=row.split(b'\t',1)
   if p.decode() not in paths:out.setdefault(p,[]).append(meta)
 return out
f=foreign();parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Checkpoint credited harmonic-path proof and complete source reproduction','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 z=subprocess.run(args,cwd=R,capture_output=True);(P/('checkpoint_365_math_'+label+'.stdout')).write_bytes(z.stdout);(P/('checkpoint_365_math_'+label+'.stderr')).write_bytes(z.stderr);assert z.returncode==0,(label,z.stderr);assert foreign()==f,'foreign index changed'
c=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',c).decode().splitlines());assert changed<=paths
print(json.dumps({'status':'PUBLISHED_PR365_SOURCE_MATH_CHECKPOINT','commit':c,'parent':parent,'owned_changed_paths':len(changed),'foreign_index_preserved':True,'program_completed':23,'program_total':349},indent=2))
