from pathlib import Path
import hashlib,json,datetime,os,stat,sys
A=Path(sys.argv[1]);P=A.parents[1];C=P.parent;R=Path('/Users/alec/Documents/Math')
D=A/'scoped_active_checkpoint_20261008'
S=D/'scoped_checkpoint_publish_v1.py'
ns={'__file__':str(S),'__name__':'checkpoint_preparation_only'}
exec(compile(S.read_bytes(),str(S),'exec'),ns)
pin=ns['pin'];digest=ns['digest'];run=ns['run'];git=ns['git']
T=D/'private/prepare_package_02';T.mkdir();(T/'raw').mkdir()
j={'actual_ROOT_PID':os.getpid(),'UTC_start':ns['utc'](),'children':[],'raw_directory':str(T/'raw'),'action':'read_only_plan_preparation','provider_mutation':False,'publication_executed':False}
selected=[]
def select(path):
 if not path.is_file():raise RuntimeError('selection absent '+str(path))
 selected.append(path)
names=['ROOT_ACTUAL_CHECKPOINT_ACCEPTANCE_20261008.json','ROOT_WHOLE_PUBLICATION_R1_ACCEPTANCE_20261008.json','ROOT_R1_GLOBAL_REPAIR_20261008.json','ROOT_V2_PACKAGE_PREPARATION_20261008.json','ROOT_V2_REPRODUCTION_ACCEPTANCE_20261008.json','ROOT_WHOLE_PUBLICATION_R2_ACCEPTANCE_20261008.json','ROOT_FINAL_MATH_PACKAGE_GATE_20261008.json','RESEARCH_LOG.md']
for n in names:select(A/n)
K=A/'publication_package_v2'
for path in sorted(K.rglob('*')):
 if path.is_file():select(path)
for folder in ['whole_publication_adversary_r1_20261008','whole_publication_adversary_r2_20261008']:
 for n in ['REVIEW.md','RESULT.json','AUDIT_MANIFEST.json','FINAL_READBACK.json']:
  select(A/folder/n)
select(A/'export_corrected_v2.py')
select(S)
notice=D/'PUBLIC_PACKAGE_CHECKPOINT_NOTICE_v2.md'
with notice.open('x') as f:
 f.write("""# PR147 corrected complete research-note checkpoint

The mathematical result and complete corrected publication_package_v2 passed a new fresh independent whole-publication review after the first review's provenance wording issue was repaired globally. Original submission and first review findings remain intact. The4-page note rigorously refutes the literal printed k107 product using primitive4-period orbits in one fixed confocal continuous family. The portable exact verification supplement, manuscript/PDF, metadata and source/history comparisons are complete.

Known Garcia–Reznik geometry and Ferudun's contemporary exact correction are explicitly credited. This is a narrow corrective note corresponding to the dated September30 repository counterexample, with no exclusive global priority or independent-discovery claim. The separately unidentified2020 in-preparation manuscript remains a bounded primary-search/access limit.

This public checkpoint has no Zenodo DOI, sheet row, PR147 merge or native promotion. Corrected operational scripts await their own final preparation review before those authorized future actions. Original author2/5 and zero new central discovery approaches are preserved; program remains25 completed/13 published and unfinished.

All files in the final publication package are distributed, with exact source/metadata/PDF/ZIP pins. Outside that package, the review manifests bind locally closed inspection evidence; this public report subset does not redistribute every locally inventoried file. Third-party full texts, screenshots and archives remain inspection-only outside the supplement. Authored work is unrefereed and extensively AI-assisted; no conventional human peer review is claimed.
""")
select(notice)
prev=P/'audits/pr141_30003818'
select(Path(__file__).resolve())
try:
 base=ns['remote'](j)
 if base!='9f5811ed2ea43acda528bb9904765c90d6e7ae0d':raise RuntimeError('remote changed')
 git(['cat-file','-e',base+'^{commit}'],j)
 prevpr=json.loads(run([ns['GH'],'api','repos/AlecKriebel/Math/pulls/141'],j))
 curr=json.loads(run([ns['GH'],'api','repos/AlecKriebel/Math/pulls/147'],j))
 if curr['head']['sha']!='502de2f863a63ca205814da4194411847797a7c3' or curr['state']!='open' or not curr['draft']:raise RuntimeError('current intake drift')
 if prevpr['state']!='closed' or not prevpr['merged_at'] or prevpr['merge_commit_sha']!='7431d02aed19d00fc8494a564b9048db203320e9':raise RuntimeError('prior acceptance drift')
 old=json.loads((prev/'final_actual_preparation_helper_20261008/private/ROOT_ACTUAL_PREPARATION_01/ACTUAL_FINAL_PLAN.json').read_bytes())
 protected_paths={x['path'] for x in old['protected']}
 protected_paths.update(str(P/n) for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md'])
 protected=[{'path':p,**pin(p)} for p in sorted(protected_paths)]
 absences=old['protected_absences']
 for p in absences:
  if Path(p).exists() or Path(p).is_symlink():raise RuntimeError('protected absence drift '+p)
 stage=T/'public_stage';stage.mkdir()
 members=[];seen=set()
 for i,p in enumerate(selected):
  rel=p.relative_to(C).as_posix()
  if rel in seen:raise RuntimeError('duplicate selection '+rel)
  seen.add(rel);b=p.read_bytes();dest=stage/str(i).zfill(4);dest.write_bytes(b);os.chmod(dest,0o644)
  z=git(['ls-tree','-z',base,'--',rel],j)
  blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  exists=bool(z)
  members.append({'path':rel,'source':str(dest),'source_original':str(p),'source_original_pin':pin(p),'post':pin(dest),'post_blob':blob,'pre_tree_sha256':digest(z),'install':False,'local_pre':None,'changed':z!=('100644 blob '+blob+'\t'+rel+'\0').encode()})
 remote_inputs=[]
 for x in old['preserved_remote_inputs']:
  rel=x['path'];z=git(['ls-tree','-z',base,'--',rel],j);b=git(['show',base+':'+rel],j)
  if digest(b)!=x['sha256'] or len(b)!=x['bytes']:raise RuntimeError('prior native remote drift '+rel)
  remote_inputs.append({'path':rel,'tree_sha256':digest(z),'bytes':len(b),'sha256':digest(b)})
 plan={'schema':'pr147-active-checkpoint-overlay/v1','source_sha256':digest(S.read_bytes()),'base_commit':base,'git_executable':pin(ns['G']),'gh_executable':pin(ns['GH']),'R_HEAD':old['R_HEAD'],'C_HEAD':old['C_HEAD'],'protected':protected,'protected_absences':absences,'previous_PR141_original_head':prevpr['head']['sha'],'previous_PR141_merge_commit':prevpr['merge_commit_sha'],'current_PR147_original_head':curr['head']['sha'],'members':members,'protected_remote_inputs':remote_inputs,'expected_changed_paths':sorted(x['path'] for x in members if x['changed']),'commit_message':'Checkpoint PR147 corrected k107 research note and portable exact package after fresh adversarial reviews','local_install':False,'new_central_proof_approaches':0,'author_approaches':2,'case_completion_percent':82,'whole_package_reviews_pending':False}
 ns['guard'](plan,j)
 ns['dump'](D/'PLAN_PACKAGE_01.json',plan)
 j.update(status='PASS_CONCRETE_PLAN_PREPARATION',plan_sha256=pin(D/'PLAN_PACKAGE_01.json')['sha256'],member_count=len(members),expected_changed_count=len(plan['expected_changed_paths']),source_pin=pin(S))
finally:
 j['UTC_end']=ns['utc']();ns['dump'](T/'PREPARATION_RECEIPT.json',j)
print(json.dumps({'status':j['status'],'plan':pin(D/'PLAN_PACKAGE_01.json'),'selected':j['member_count'],'changed':j['expected_changed_count'],'closed_children':len(j['children']),'PID':os.getpid()}))

