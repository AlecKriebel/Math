"""Freeze PR207 merge95 source overlay with GET-only native preimages.
No ref, PR, publication, tracker, Git, or existing local-view mutation.
"""
from pathlib import Path
import json,hashlib,datetime,importlib.util,stat,os
A=Path(__file__).resolve().parent.parent
B=A/'native_integration_preparation_01'
P=A.parents[1];C=P.parent
CASE='draft_pr_publication_program_20260930/audits/pr207_5100044/'
PROGRAM='draft_pr_publication_program_20260930/'
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(o):return (json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def jp(p):return json.loads(p.read_text())
def put(p,b):
 p.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444)
helper=B/'native207_v2.py';need(pin(helper.read_bytes())=={'bytes':31634,'sha256':'e850bb9adcb40db4d9949251c103677e37651f3ec3daad16219227729f7e1efc'},'Helper source')
sp=importlib.util.spec_from_file_location('pr207_root_frozen_native_helper',helper);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
c=h.core();facts=h.phase_facts('merge95');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ready=jp(A/'ROOT_ACTUAL_PR_READY_01.json')
need(pin((A/'ROOT_ACTUAL_PR_READY_01.json').read_bytes())=={'bytes':2324,'sha256':'7031be731dc4954aed2b1b68b73314f7c74eca4f980d3267905c03f186fbee84'} and ready['accepted'] is True and ready['actual_PR_ready_for_review'] is True and ready['actual_original_head']==h.HEAD,'Actual ready PR')
ops=jp(A/'ROOT_NATIVE_INTEGRATION_PREPARATION_ACCEPTANCE_01.json')
need(pin((A/'ROOT_NATIVE_INTEGRATION_PREPARATION_ACCEPTANCE_01.json').read_bytes())=={'bytes':2722,'sha256':'c4aea44071dd66c7a0931950792b8194645b28c128d86309bead5185485f7772'} and ops['required_repairs']==[] and ops['factual_only_finalization_accepted'] is True,'Actual ops/factual Root acceptance')
api=h.API(h.journal_new('root_merge95_freeze_get_01'),mutate=False)
parent=api('GET','git/ref/heads/main')['object']['sha'];commit=api('GET','git/commits/'+parent)
need(commit['sha']==parent,'Actual parent association')
h.original_pr(api,'merge95');trees=c.NativeTrees(api)
prep=jp(B/'ROOT_PUBLIC_SOURCE_COPY_PREPARATION_01.json');selected={}
def add(target,raw):
 c.rel(target)
 need(target.startswith(CASE) or target.startswith(h.ATTEMPT) or target in h.VIEWS[2:] or target==h.QUEUE,'Own overlay scope')
 if target in selected:need(selected[target]==raw,'Duplicate source disagreement');return
 selected[target]=raw
for row in prep['files']:
 raw=(B/row['source']).read_bytes();need(pin(raw)=={k:row[k] for k in ('bytes','sha256')} and c.native('blob',raw)==row['git_blob'],'Owned prepared source')
 add(row['path'],raw)
# Only exact peer public allowlist; no fixture/private tree recursion.
ad=A/'native_integration_adversary_01';am=jp(ad/'PUBLIC_ARTIFACT_MANIFEST.json')
need(pin((ad/'FINAL_SEAL.json').read_bytes())=={'bytes':926,'sha256':'53ffb17dd736c31c5fe3d26085baa4a5968e48672411d67c9a712004b2e479f2'},'Ops adversary seal')
for row in am['files']:
 raw=(ad/row['path']).read_bytes();need(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'Ops public source');add(CASE+'native_integration_adversary_01/'+row['path'],raw)
for n in ['PUBLIC_ARTIFACT_MANIFEST.json','FINAL_SEAL.json']:add(CASE+'native_integration_adversary_01/'+n,(ad/n).read_bytes())
for n in ['ROOT_NATIVE_INTEGRATION_PREPARATION_ACCEPTANCE_01.json','ROOT_ACTUAL_PR_READY_01.json','root_native_integration_execution_01/freeze_merge95.py','native_integration_preparation_01/ROOT_PUBLIC_SOURCE_COPY_PREPARATION_01.json']:
 add(CASE+n,(A/n).read_bytes())
for n in ['PRE_UPDATE_NATIVE.json','UPDATE_METADATA_INTENT.json','UPDATE_TOOL_RESULT.json','POST_UPDATE_NATIVE.json','READY_INTENT.json','READY_TOOL_RESULT.json','READY_NATIVE_READBACK.json']:
 add(CASE+'root_pr_metadata_execution_01/'+n,(A/'root_pr_metadata_execution_01'/n).read_bytes())
# Record a gate for actual already-completed heterogeneous events, not a native CAS.
roles={'scientific':'ROOT_SCOPED_MATHEMATICAL_ASSESSMENT_01.json','whole_package_review':'ROOT_PUBLICATION_GATE_01.json','publication':'ROOT_ACTUAL_PUBLICATION_01.json','tracker':'ROOT_ACTUAL_TRACKER_01.json'}
receipts={}
for role,n in roles.items():
 raw=(A/n).read_bytes();add(CASE+n,raw);receipts[role]={'path':CASE+n,**pin(raw)}
g={'schema':'pr207-root-native-phase-gates-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','UTC':now,'PR':207,'phase':'merge95','accepted':True,'original_head':h.HEAD,'facts':facts,'scientific_accepted':True,'whole_package_accepted':True,'actual_publication_verified':True,'actual_tracker_verified':True,'ready_for_merge':True,'receipts':receipts,'actual_ready_PR_receipt':{'path':CASE+'ROOT_ACTUAL_PR_READY_01.json',**pin((A/'ROOT_ACTUAL_PR_READY_01.json').read_bytes())},'native_ref_or_merge_claimed_by_this_gate':False}
gatepath=CASE+'ROOT_NATIVE_MERGE95_GATES_01.json';put(A/'ROOT_NATIVE_MERGE95_GATES_01.json',enc(g));add(gatepath,enc(g))
oldprogress=jp(P/'CURRENT_PROGRESS.json')
oldcompleted=oldprogress['fully_completed_eligible_PRs'];oldpublished=oldprogress['published_PRs']
need(len(oldcompleted)==len(set(oldcompleted))==49 and oldcompleted[-1]==206 and 207 not in oldcompleted and len(oldpublished)==len(set(oldpublished))==33 and oldpublished[-1]==206 and 207 not in oldpublished,'Exact pre-phase memberships')
status=jp(A/'CURRENT_CASE_STATUS.json');progress=dict(oldprogress)
for obj in [status,progress]:
 obj.update(facts)
 obj.update(UTC=now,updated_UTC=now,current_PR=207,current_case_percent=95,current_publication_ready=True,current_status='published_tracked_native_merge_checkpoint_completion_pending',status='published_tracked_native_merge_checkpoint_completion_pending',whole_package_reviews_complete=True,new_distinct_whole_package_reviews_accepted=2,mandatory_publication_repairs=[],native_problem_or_QUEUE_modified=True,actual_publication_verified=True,actual_tracker_verified=True,active_publication_DOI='10.5281/zenodo.23428090',active_tracker_range="'Math Puzzles'!A134:D134",checkpoint_semantics='Candidate-only frozen95 overlay until actual external Root CAS/readback/full scope acceptance and exact locked local-five sync. Case completion and next intake remain false.',next_step='Verify and accept actual original-HEAD merger, then separate completion100 checkpoint; no next-case intake yet.',alternate_telescoping_route='Earlier23-check scoped Root replay plus two later accepted whole-publication-package reviews; known theorem and classical methods remain credited.')
 obj.pop('publication_or_merge_or_new_intake_authorized',None)
 obj['Root_publication_gate']={'path':CASE+'ROOT_PUBLICATION_GATE_01.json',**pin((A/'ROOT_PUBLICATION_GATE_01.json').read_bytes())}
 obj['actual_publication_receipt']={'path':CASE+'ROOT_ACTUAL_PUBLICATION_01.json',**pin((A/'ROOT_ACTUAL_PUBLICATION_01.json').read_bytes())}
 obj['actual_tracker_receipt']={'path':CASE+'ROOT_ACTUAL_TRACKER_01.json',**pin((A/'ROOT_ACTUAL_TRACKER_01.json').read_bytes())}
progress['published_PRs']=oldpublished+[207]
progress['fully_completed_eligible_PRs']=list(oldcompleted)
progress['fully_completed_fraction_percent']=100*49/99
progress['denominator_semantics']='Dated October3 census99;49/99 is workflow completion, not novelty/discovery or current-openness certification.'
need(progress['fully_completed_eligible_PRs']==oldcompleted and progress['published_PRs'][:-1]==oldpublished,'Exact previous IDs preserved')
add(h.VIEWS[0],enc(status));add(h.VIEWS[2],enc(progress))
mark=h.marker(facts).decode()
claim=status['positive_theorem'];limits=status['alternative_reading_resolution']
entry=now+' — PR207 merge95 freeze: two clean new whole-package reviews; attributed known-result verification published DOI10.5281/zenodo.23428090, trackerA134:D134 readback verified. Classical methods/Ferudun23093706 credited, least-period4n scope and exact repeated-list counterexample retained.49completed/34published,last206,cursor207,advancefalse,goalfalse. Candidate is prospective until Root actual CAS/native acceptance/locked local sync; completion100 and next intake require later actual merge proof.'
for target,local in [(h.VIEWS[1],A/'RESEARCH_LOG.md'),(h.VIEWS[4],P/'RESEARCH_LOG.md')]:
 text=local.read_text();need('<!-- PR207_NATIVE_PHASE_FACTS ' not in text,'Unexpected current phase marker')
 add(target,(text.rstrip()+'\n\n'+entry+'\n\n'+mark+'\n').encode())
md='# Current research progress\n\nFrozen '+now+': **PR207 at95%**, publication and tracker verified;49completed/34published,last206,cursor207. Case completion and next intake remain pending. Dated workflow census99:49.49%.\n\n'+claim+'\n\n'+limits+'\n\nThe theorem/boundary is already known from Alper Ferudun, DOI10.5281/zenodo.23093706. Local/cyclic Jacobi and generalized Landen methods are classical. No theorem/method novelty, firstness, causal independence, simultaneity or current-openness certification. Extensive AI use; unrefereed, without conventional human peer review or proof-assistant formalization.\n\nPublished [verification note](https://doi.org/10.5281/zenodo.23428090); tracker Math Puzzles A134:D134. Two new whole-package reviews and documentary-only finalization accepted. Original20-file/61131-byte submitted archive remains unchanged;claimed_solved1/5 preserved, author/model effort unverified. Native merge and completion require actual Root receipts.\n\nPublished PRs(34): '+', '.join(map(str,progress['published_PRs']))+'.\n\n'+mark+'\n'
add(h.VIEWS[3],md.encode())
# Derive exactly one own-row replacement from fresh MAIN; preserve all foreign bytes.
qtuple=trees.lookup(commit['tree']['sha'],h.QUEUE);need(qtuple and qtuple[:2]==('100644','blob'),'Existing native QUEUE')
queue=h.read_blob(c,api,qtuple[2]);lines=queue.splitlines(keepends=True);idx=[i for i,line in enumerate(lines) if b'| 5100044 / AMR-050-0044 |' in line];need(len(idx)==1,'One own row')
cells=lines[idx[0]].split(b'|');need(len(cells)==14,'Exact own table cells')
cells[8]=b' claimed_solved ';cells[9]=b' 1/5 '
cells[11]=b' 2026-10-17: Verified least-period4n focal-inversion area product for proper nested confocal ellipses/all coprime stars/either focus; exact repeated-list obstruction. Attributed verification of known Ferudun DOI10.5281/zenodo.23093706; classical local/cyclic/Landen methods credited. Two new whole-package AI reviews clean; AI-assisted/unrefereed, no novelty/independence/simultaneity claim. Author/model effort unverified. [Current proof](attempts/5100044/PUBLICATION_STATUS.md). '
cells[12]=b' [10.5281/zenodo.23428090](https://doi.org/10.5281/zenodo.23428090) '
newlines=list(lines);newlines[idx[0]]=b'|'.join(cells);newqueue=b''.join(newlines);h.queue_change(queue,newqueue,'merge95');add(h.QUEUE,newqueue)
# Resolve all fresh native preimages; preserve every existing non-view/cue artifact.
rows=[];source_root=B/'phase_merge95_sources'
for path,raw in sorted(selected.items()):
 pre=trees.lookup(commit['tree']['sha'],path);wanted=('100644','blob',c.native('blob',raw))
 if pre is not None and path not in h.VIEWS and path!=h.QUEUE:need(pre==wanted,'Existing immutable/current native source collision: '+path)
 if path.startswith(h.ATTEMPT):need(pre is None,'Original PR207 attempt is unexpectedly already on MAIN')
 source=source_root/path
 if source.exists():need(source.read_bytes()==raw and stat.S_IMODE(source.stat().st_mode)==0o444,'Owned copy changed')
 else:put(source,raw)
 rows.append({'path':path,'source':source.relative_to(B).as_posix(),**pin(raw),'git_blob':wanted[2],'preimage':None if pre is None else dict(zip(['mode','type','sha'],pre))})
local=[]
for path in h.VIEWS:
 f=C/path;need(f.resolve()==f and f.is_file() and not f.is_symlink(),'Existing local five regular')
 raw=f.read_bytes();pre=trees.lookup(commit['tree']['sha'],path);need(pre==('100644','blob',c.native('blob',raw)),'Local/native old view mismatch')
 local.append({'path':path,'preimage':pin(raw)})
need(api('GET','git/ref/heads/main')['object']['sha']==parent,'MAIN changed during source freeze')
m={'schema':'pr207-native-integration-inputs-v1','PR':207,'phase':'merge95','anchor':h.ANCHOR,'original_head':h.HEAD,'original_head_tree':h.HEAD_TREE,'expected_parent':parent,'helper_pin':pin(helper.read_bytes()),'core_pin':h.CORE_PIN,'facts':facts,'files':rows,'total_files':len(rows),'total_bytes':sum(x['bytes'] for x in rows),'local_views':local,'gate_receipt':gatepath,'commit_message':'Publish attributed PR207 verification and merge corrected original submission'}
manifest=B/'MERGE95_INPUTS_01.json';put(manifest,enc(m))
summary={'schema':'pr207-root-merge95-source-freeze-v1','UTC':now,'state':'FROZEN_SOURCES_GET_ONLY_NOT_NATIVE_ACCEPTANCE','parent':parent,'parent_tree':commit['tree']['sha'],'manifest':pin(manifest.read_bytes()),'selected_files':len(rows),'selected_bytes':m['total_bytes'],'all_previous49_completed_IDs_exact':progress['fully_completed_eligible_PRs']==oldcompleted,'all_previous33_published_IDs_exact':progress['published_PRs'][:-1]==oldpublished,'only_added_published_ID':207,'original_archived_files':20,'native_current_files':22,'no_native_ref_or_local_current_write':True,'goal_complete':False}
put(A/'root_native_integration_execution_01/MERGE95_SOURCE_FREEZE.json',enc(summary))
print(json.dumps(summary))
