"""PR147 final checkpoint: explicit audit overlay and separate three-program install.

Source preparation only. Every actual action needs genuine completed native
acceptance and a fresh independent exact source/request/postimage/plan review.
"""
from pathlib import Path,PurePosixPath
import argparse,base64,hashlib,json,os,stat,types
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A=C/'draft_pr_publication_program_20260930/audits/pr147_5100001'
D=A/'final_completion_operator_preparation_20261008'
DEPENDENCY=A/'native_sparse_operator_preparation_20261008/native_sparse_operator_v1.py'
DEPENDENCY_SHA='9eed88db21f9018eedf6cd48ba79f3ea87b4499ea118c6d2817f8cd4574cc8ca'
NATIVE_GATE=A/'ROOT_ACTUAL_NATIVE_ACCEPTANCE_20261008.json'
HEAD='502de2f863a63ca205814da4194411847797a7c3'
MERGE='e8621548039130d471eae99580a29b32925f3c8f'
AUDIT=A.relative_to(C).as_posix()+'/'
PROGRAM={str(PurePosixPath('draft_pr_publication_program_20260930')/p) for p in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')}
# Load only one immutable audited dependency body; no builders or actual inputs.
body=DEPENDENCY.read_bytes()
if len(body)!=66660 or hashlib.sha256(body).hexdigest()!=DEPENDENCY_SHA:raise RuntimeError('audited dependency mismatch')
n=types.ModuleType('native_gate_audited_mechanisms');n.__file__=str(DEPENDENCY);exec(compile(body,str(DEPENDENCY),'exec'),n.__dict__)
m=types.ModuleType('final_checkpoint_audited_mechanisms');m.__file__=str(DEPENDENCY);exec(compile(body,str(DEPENDENCY),'exec'),m.__dict__);m.D=D
require=m.require;pin=m.pin;full_pin=m.full_pin;absolute=m.absolute;canonical=m.canonical;digest=m.digest;sha_value=m.sha_value;oid=m.tree_oid

def path_pin(path):return {'path':str(m.safe(path)),**pin(path)}
def read(spec):return m.read_pinned(spec)
def raw_spec(path):
 spec=path_pin(absolute(path));require(spec['mode']==420,'proposal mode100644');return spec

def relative(value):
 require(isinstance(value,str) and value and '\0' not in value and '\\' not in value,'relative path string')
 p=PurePosixPath(value);require(not p.is_absolute() and str(p)==value and all(x not in ('.','..') for x in p.parts),'canonical relative path')
 require(not any(x.casefold()=='.git' for x in p.parts),'no Git controls in selected overlay');return value

def scope(artifacts):
 require(isinstance(artifacts,list) and 0<len(artifacts)<=128,'explicit bounded artifact list')
 require(len(artifacts)==len(set(artifacts))==len({p.casefold() for p in artifacts}),'unique artifact paths')
 for value in artifacts:
  relative(value);require(value.startswith(AUDIT),'only explicit PR147 audit artifacts')
  first=value[len(AUDIT):].split('/')[0]
  require(not first.startswith('publication_package_') and first!='original_submitted_attempt','already-published package/original archive excluded')
 return PROGRAM|set(artifacts)

def compact(spec):return {k:spec[k] for k in ('bytes','mode','sha256')}

def native_acceptance(spec):
 require(spec['path']==str(NATIVE_GATE),'genuine final native gate path; public-only gate rejected')
 gate=m.native_json(read(spec))
 require(gate['schema']=='pr147-root-actual-native-final-acceptance/v1' and gate['status']=='ACCEPTED_NATIVE_PUBLIC_AND_LOCAL','completed actual native acceptance required')
 require(type(gate['actual_ROOT_PID']) is int and gate['actual_ROOT_PID']>0 and isinstance(gate['UTC'],str) and gate['UTC'],'actual ROOT custody')
 require(gate['PR']==147 and gate['original_head']==HEAD and gate['original_merge']==MERGE and gate['native_sole_parent']==MERGE,'exact original native ancestry')
 require(type(gate['native_remote_changed_path_count']) is int and gate['native_remote_changed_path_count']==19 and type(gate['native_local_installed_path_count']) is int and gate['native_local_installed_path_count']==32,'actual native19/32')
 for key in ('full_public_body_mode_readback','full_local_body_mode_readback','whole_parent_tree_preserved_outside_exact_overlay','real_git_controls_preserved'):require(gate[key] is True,'full native acceptance '+key)
 require(gate['original_effort']=='2/5' and gate['original_author_turn_ledger_present'] is True and gate['original_native_transition_ledger_present'] is False and type(gate['new_central_proof_search_turns']) is int and gate['new_central_proof_search_turns']==0 and gate['program3_changed'] is False and gate['overall_goal_complete'] is False,'faithful native-before-program stage')
 evidence=gate['evidence_pins'];require(set(evidence)=={'source','plan','review','publish','install'},'complete native evidence roles')
 for value in evidence.values():full_pin(value)
 require(evidence['source']['path']==str(DEPENDENCY) and evidence['source']['sha256']==DEPENDENCY_SHA,'accepted native source')
 plan=m.native_json(read(evidence['plan']));review=m.native_json(read(evidence['review']));pub=m.native_json(read(evidence['publish']));ins=m.native_json(read(evidence['install']))
 j={'source_sha256':DEPENDENCY_SHA,'plan_sha256':evidence['plan']['sha256'],'review_sha256':evidence['review']['sha256']}
 require(plan['source_sha256']==DEPENDENCY_SHA and plan['original_head']==HEAD and plan['base_commit']==MERGE and plan['original_effort']=='2/5' and plan['original_author_turn_ledger_present'] is True and plan['original_native_transition_ledger_present'] is False and plan['new_central_proof_search_turns']==0,'faithful exact accepted native plan')
 require(n.validate_publication_receipt(pub,plan,j)==gate['native_commit'],'native public receipt')
 require(review['schema']=='pr147-native-sparse-operator-source-plan-review/v1' and review['actual_review'] is True and review['verdict']=='PASS' and review['mandatory_findings']==[],'actual native source/data/plan review')
 require(review['source_sha256']==DEPENDENCY_SHA and review['plan_sha256']==evidence['plan']['sha256'] and review['request_sha256']==plan['request']['sha256'] and review['binding_sha256']==plan['binding']['sha256'],'native exact review binding')
 require(ins['schema']=='pr147-native-sparse-operation-receipt/v1' and ins['status']=='public_and_local_install_verified' and ins['action']=='install' and ins['fixture_only'] is False and ins['published_commit']==gate['native_commit'] and ins['source_sha256']==DEPENDENCY_SHA and ins['plan_sha256']==evidence['plan']['sha256'] and ins['review_sha256']==evidence['review']['sha256'] and ins['own_operation_lock_released'] is True and 'error_type' not in ins,'completed native install receipt')
 require(ins['program3_changed'] is False and ins['private_cache_installed'] is False and ins['raw_backend_installed'] is False,'native stage preserves program/source/cache')
 require(ins['local_readback_path_count']==32 and type(ins['local_readback_path_count']) is int and ins['local_full_body_mode_readback'] is True and set(ins['installed'])=={v['path'] for v in plan['install_members']} and len(ins['installed'])==32,'native complete selected local32')
 for record in (pub,ins):
  require(n.children_custody_complete(record),'native closed raw custody')
  for child in record['children']:n.authenticate_child_custody(child)
 root_execution=gate['independent_ROOT_execution'];full_pin(root_execution)
 require(root_execution['path']==str(DEPENDENCY.parent/'private/ROOT_ACTUAL_FINAL_READBACK_01/RECEIPT.json'),'actual independent final ROOT readback path')
 root=m.native_json(read(root_execution));require(root['schema']=='pr147-root-actual-native-readback/v1' and root['status']=='PASS' and root['actual_ROOT_PID']==gate['actual_ROOT_PID'] and root['source_sha256']==DEPENDENCY_SHA and root['plan_sha256']==evidence['plan']['sha256'] and root['review_sha256']==evidence['review']['sha256'] and root['native_commit']==gate['native_commit'] and root['full_public_readbacks']==32 and root['full_local_readbacks']==32 and root['real_git_controls_preserved'] is True and n.children_custody_complete(root),'independent actual ROOT public/local32 readback')
 for child in root['children']:n.authenticate_child_custody(child);require(child['exit_code']==0,'successful independent ROOT child')
 object_root=absolute(pub['object_workspace']);require(DEPENDENCY.parent/'private' in object_root.parents and object_root.name=='object_workspace' and object_root.is_dir(),'actual native public private workspace')
 n.validate_inventory(plan['remote_members'],plan['install_members'],plan['remote_unchanged_canonical_paths'])
 native=[]
 for member in plan['install_members']:
  spec=path_pin(C/member['path']);require(compact(spec)==member['post'],'current actual native32 body/mode preserved')
  native.append({'path':member['path'],'pin':spec,'post_blob':member['post_blob'],'post':member['post']})
 fixed_dirs=[v for v in plan['protected_directories'] if v['path'] in {str(A/'original_submitted_attempt'),str(A/'publication_package_v2')}]
 require(len(fixed_dirs)==2,'accepted original20/package90 directory custody')
 program_pins={v['path']:compact(v) for v in plan['protected'] if v['path'] in {str(C/p) for p in PROGRAM}}
 require(set(program_pins)=={str(C/p) for p in PROGRAM},'accepted unchanged C program3 preimages')
 return {'gate':path_pin(NATIVE_GATE),'original_package_directories':fixed_dirs,'program_preimages':program_pins,'native_commit':oid(gate['native_commit']),'object_workspace':str(object_root),'native_members':native,'evidence_pins':evidence,'independent_ROOT_execution':root_execution}

def protection(plan,check_bodies=True):
 files=plan['protected'];absences=plan['protected_absences'];dirs=plan['protected_directories']
 require(isinstance(files,list) and isinstance(absences,list) and isinstance(dirs,list),'complete protection lists')
 present={v['path'] for v in files};absent=set(absences);roots={v['path'] for v in dirs}
 require(len(present)==len(files) and len(absent)==len(absences) and not present&absent and len(roots)==len(dirs),'unique protection inventory')
 require(len(present|absent)==len({p.casefold() for p in present|absent}),'protection case aliases')
 required={str(root/'.git'/name) for root in (R,C) for name in n.GIT_FILES+n.GIT_LOCKS}
 required|={str(R/'unsolved_math_prioritization'/name) for name in n.BACKEND+('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}
 required|={str(R/p) for p in PROGRAM}|{str(C/'unsolved_math_prioritization'/name) for name in ('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}
 required|={v['pin']['path'] for v in plan['native']['native_members']}
 require(required<=present|absent,'full current real/native32/program protections')
 require({str(root/'.git'/name) for root in (R,C) for name in n.GIT_LOCKS}<=absent,'real writer locks absent')
 require({str(C/'unsolved_math_prioritization'/name) for name in ('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}<=absent,'C backend-source/cache remain absent')
 require({v['pin']['path'] for v in plan['native']['native_members']}<=present,'all actual native32 must stay present')
 native_pins={v['pin']['path']:v['pin'] for v in plan['native']['native_members']};protected_pins={v['path']:v for v in files}
 require(all(protected_pins[p]==v for p,v in native_pins.items()),'native32 protected pins equal accepted installed bodies')
 require({str(R/'unsolved_math_prioritization'/name) for name in n.BACKEND+('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}<=present,'R backend/source/cache must remain present')
 require(str(R/'draft_pr_publication_program_20260930/CURRENT_PROGRESS.md') in absent,'R progress document remains absent')
 require(not {str(C/p) for p in PROGRAM}&(present|absent),'selected C program preimages are separate mutable protection')
 required_roots={str(root/'.git/refs') for root in (R,C)}|{str(R/'unsolved_math_prioritization/cache'),str(A/'original_submitted_attempt'),str(A/'publication_package_v2'),str(C/n.ATTEMPT_PREFIX.rstrip('/')),plan['postimage_root']}
 require(required_roots<=roots,'closed refs/cache/original20/package90/native24/postimage protections')
 for accepted in plan['native']['original_package_directories']:
  require(next(v for v in dirs if v['path']==accepted['path'])==accepted,'immutable accepted original20/package90 bodies')
 for root in roots:
  absolute(root);require(not any(Path(root)==C/p or Path(root) in (C/p).parents for p in PROGRAM),'immutable directory cannot contain selected C program files')
  require(Path(root)!=D/'private' and not (D/'private').is_relative_to(Path(root)),'action receipts outside immutable roots')
 if check_bodies:
  for value in files:full_pin(value)
  for value in absences:require(not m.local_case_guard(value).exists(),'protected absence changed')
  for value in dirs:m.closed_directory(value)


def proposal(request_spec):
 q=m.native_json(read(request_spec))
 fields={'schema','native_acceptance','fresh_base_commit','R_HEAD','C_HEAD','git_executable','gh_executable','postimage_root','artifact_paths','postimages','remote_preimages','program_preimages','protected','protected_absences','protected_directories','commit_message'}
 require(set(q)==fields and q['schema']=='pr147-final-checkpoint-request/v1','exact actual final request contract')
 selected=scope(q['artifact_paths']);require(set(q['postimages'])==set(q['remote_preimages'])==selected and set(q['program_preimages'])==PROGRAM,'exact selected/three-program inventories')
 native=native_acceptance(q['native_acceptance']);root=absolute(q['postimage_root']);require(D/'private' in root.parents,'immutable future postimage root')
 members=[];total=0
 for path in sorted(selected):
  spec=q['postimages'][path];full_pin(spec);require(spec['path']==str(root/path) and spec['mode']==420 and spec['bytes']<=16*1024*1024,'bounded exact postimage source')
  data=read(spec);total+=len(data);pre=q['remote_preimages'][path]
  if pre is not None:
   require(set(pre)=={'bytes','mode','sha256','Git_blob'} and type(pre['bytes']) is int and pre['bytes']>=0 and type(pre['mode']) is int and pre['mode']==420,'typed remote preimage');sha_value(pre['sha256']);oid(pre['Git_blob'])
   require(pre['sha256']!=spec['sha256'],'every selected remote path must change')
  local=q['program_preimages'][path] if path in PROGRAM else None
  if path in PROGRAM:
   require(isinstance(local,dict) and set(local)=={'bytes','mode','sha256'} and type(local['bytes']) is int and local['bytes']>=0 and type(local['mode']) is int and local['mode']==420,'complete current C program preimages')
   sha_value(local['sha256']);require(local==native['program_preimages'][str(C/path)],'unchanged native-accepted C program preimage');m.check(C/path,local)
  members.append({'path':path,'source':spec['path'],'storage':{'encoding':'raw','pin':spec},'post':compact(spec),'post_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),'remote_pre':pre,'local_pre':local,'install':path in PROGRAM})
 require(total<=64*1024*1024,'small final overlay; no backend/package duplication')
 message=q['commit_message'];require(isinstance(message,str) and message.strip()==message and '147' in message and '\0' not in message,'scoped commit message')
 p={'schema':'pr147-final-program-audit-overlay/v1','source':path_pin(Path(__file__).resolve()),'dependency':path_pin(DEPENDENCY),'request':request_spec,'native_acceptance':q['native_acceptance'],'native':native,'base_commit':oid(q['fresh_base_commit']),
 'R_HEAD':oid(q['R_HEAD']),'C_HEAD':oid(q['C_HEAD']),'git_executable':q['git_executable'],'gh_executable':q['gh_executable'],'postimage_root':str(root),'artifact_paths':q['artifact_paths'],'members':members,'program_paths':sorted(PROGRAM),
 'protected':q['protected'],'protected_absences':q['protected_absences'],'protected_directories':q['protected_directories'],'commit_message':message,'new_central_proof_search_turns':0,'overall_goal_completion_claimed':False}
 require(p['source']['path']==str(D/'final_completion_operator.py'),'fixed final operator source path')
 require(p['git_executable']['path']==n.G and p['gh_executable']['path']==n.GH,'fixed audited executable paths');full_pin(p['git_executable']);full_pin(p['gh_executable']);protection(p)
 return p

def guard(plan,j):
 for value in (plan['source'],plan['dependency'],plan['request'],plan['native_acceptance'],plan['git_executable'],plan['gh_executable']):full_pin(value)
 protection(plan)
 for member in plan['members']:m.read_postimage(member)
 for root,expected in ((R,plan['R_HEAD']),(C,plan['C_HEAD'])):require(m.git(['rev-parse','HEAD','refs/heads/main'],j,root=root).decode().splitlines()==[expected,expected],'real HEAD/main unchanged')

def local_preimages(plan):
 for member in plan['members']:
  if member['install']:m.check(C/member['path'],member['local_pre'])

def load(plan_path,plan_sha,review_path,review_sha):
 raw=read({'path':str(absolute(plan_path)),**pin(plan_path)});require(digest(raw)==sha_value(plan_sha),'explicit whole plan SHA');p=m.native_json(raw)
 require(p['schema']=='pr147-final-program-audit-overlay/v1' and p['source']['sha256']==digest(Path(__file__).read_bytes()),'exact running final source')
 review_body=absolute(review_path).read_bytes();require(digest(review_body)==sha_value(review_sha),'independent complete review SHA');v=m.native_json(review_body)
 require(v['schema']=='pr147-final-checkpoint-source-plan-review/v1' and v['verdict']=='PASS' and v['mandatory_findings']==[] and v['actual_review'] is True and v['actual_native_final_gate_authenticated'] is True and v['actual_postimage_data_and_current_protections_authenticated'] is True,'fresh independent actual final source/data/plan PASS')
 require(type(v['actual_reviewer_PID']) is int and v['actual_reviewer_PID']>0 and v['actual_reviewer_PID']!=os.getpid() and isinstance(v['reviewer_identity'],str) and v['reviewer_identity'].strip()==v['reviewer_identity'] and v['reviewer_identity'],'actual independent reviewer identity')
 for key,expected in (('source_sha256',p['source']['sha256']),('dependency_sha256',DEPENDENCY_SHA),('request_sha256',p['request']['sha256']),('native_acceptance_sha256',p['native_acceptance']['sha256']),('plan_sha256',plan_sha),('postimage_root',p['postimage_root'])):require(v[key]==expected,'exact review '+key)
 require(v['local_install_path_count']==3 and type(v['local_install_path_count']) is int and type(v['remote_changed_path_count']) is int and v['remote_changed_path_count']==len(p['members']),'exact reviewed final scopes')
 require(canonical(proposal(p['request']))==raw,'canonical deterministic exact final plan replay');return p

def workspace(plan,j,run_dir):
 m.initialize_object_workspace(j,run_dir)
 # Replace only our own initial alternate file, after durable explicit intent.
 path=Path(j['object_workspace'])/'objects/info/alternates';old=path_pin(path);alternate=absolute(plan['native']['object_workspace'])/'objects';m.safe(alternate);require(alternate.is_dir(),'native actual private objects alternate')
 data=(str(alternate)+'\n').encode();j['native_readonly_alternate_intent']={'path':str(path),'prior':old,'new_body_sha256':digest(data),'state':'intended'};m.dump(run_dir/'RECEIPT.json',j)
 temporary=path.with_name('alternates.final.tmp');fd=os.open(temporary,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,420)
 try:
  info=os.fstat(fd);j['native_readonly_alternate_intent'].update(temporary_path=str(temporary),temporary_identity={'dev':info.st_dev,'ino':info.st_ino},state='temporary_created');m.dump(run_dir/'RECEIPT.json',j)
  view=memoryview(data)
  while view:
   written=os.write(fd,view);require(written>0,'alternate write progress');view=view[written:];j['native_readonly_alternate_intent']['written_bytes']=len(data)-len(view)
  os.fsync(fd)
 finally:os.close(fd)
 info=temporary.lstat();require(j['native_readonly_alternate_intent']['temporary_identity']=={'dev':info.st_dev,'ino':info.st_ino} and stat.S_ISREG(info.st_mode) and info.st_nlink==1,'owned alternate temporary inode');m.check(temporary,{'bytes':len(data),'mode':420,'sha256':digest(data)})
 m.check(path,old);os.replace(temporary,path);j['native_readonly_alternate_intent'].update(state='replaced',temporary_transferred_to_target=True);m.dump(run_dir/'RECEIPT.json',j)
 m.check(path,{'bytes':len(data),'mode':420,'sha256':digest(data)});j['native_readonly_alternate_intent']['post']=path_pin(path);m.dump(run_dir/'RECEIPT.json',j)
 # No fetch route: missing current base/native closure stops before push.
 m.git(['cat-file','-e',plan['base_commit']+'^{commit}'],j);m.git(['merge-base','--is-ancestor',plan['native']['native_commit'],plan['base_commit']],j);m.git(['merge-base','--is-ancestor',HEAD,plan['base_commit']],j)

def record(member,post=False):return m.expected_tree_record(member,post)
def remote_preimages(plan,j):
 for member in plan['members']:
  require(m.git(['ls-tree','-z',plan['base_commit'],'--',member['path']],j)==record(member),'selected remote preimage path/mode/blob')
  if member['remote_pre'] is not None:
   data=m.git(['cat-file','blob',member['remote_pre']['Git_blob']],j);require(len(data)==member['remote_pre']['bytes'] and digest(data)==member['remote_pre']['sha256'],'complete selected small remote preimage')
 for member in plan['native']['native_members']:
  require(m.git(['ls-tree','-z',plan['base_commit'],'--',member['path']],j)==('100644 blob '+member['post_blob']+'\t'+member['path']+'\0').encode(),'preserve native32 public tree')

def tree(plan,j):
 for member in plan['members']:require(m.tree_oid_output(m.git(['hash-object','-w','--stdin'],j,data=m.read_postimage(member)))==member['post_blob'],'exact final blob')
 base=m.tree_oid_output(m.git(['rev-parse',plan['base_commit']+'^{tree}'],j))
 proposed=m.sparse_overlay_tree(base,{x['path']:x['post_blob'] for x in plan['members']},lambda x:m.git(['ls-tree','-z',x],j),lambda x:m.tree_oid_output(m.git(['mktree','-z'],j,data=x)))
 changes=m.git(['diff','--no-ext-diff','--no-textconv','--no-renames','--name-only','-z',plan['base_commit'],proposed],j).split(b'\0')
 require(changes[-1]==b'' and sorted(x.decode() for x in changes[:-1])==sorted(x['path'] for x in plan['members']),'whole parent tree exact selected overlay only')
 return proposed

def public_readback(plan,j,commit):
 require(m.remote(j)==commit,'direct main must remain exact final commit')
 for member in plan['members']:
  require(m.git(['ls-tree','-z',commit,'--',member['path']],j)==record(member,True),'public final path/mode/blob')
  raw=m.native_json(m.run([n.GH,'api','repos/AlecKriebel/Math/git/blobs/'+member['post_blob']],j));require(raw['sha']==member['post_blob'] and raw['encoding']=='base64' and type(raw['size']) is int and raw['size']==member['post']['bytes'],'provider final blob identity')
  data=base64.b64decode(raw['content'].replace('\n',''),validate=True);require(len(data)==member['post']['bytes'] and digest(data)==member['post']['sha256'],'complete final public body')
  j.setdefault('public_readbacks',[]).append({'path':member['path'],**member['post'],'Git_blob':member['post_blob']})
 require(m.remote(j)==commit,'direct main unchanged after full public readback')

def publish(plan,j,run_dir):
 guard(plan,j);local_preimages(plan);require(m.remote(j)==plan['base_commit'],'fresh main changed; no retry')
 workspace(plan,j,run_dir);remote_preimages(plan,j);proposed=tree(plan,j)
 commit=m.tree_oid_output(m.git(['commit-tree',proposed,'-p',plan['base_commit']],j,data=(plan['commit_message']+'\n').encode()))
 data=m.git(['cat-file','commit',commit],j);headers=data.split(b'\n\n',1)[0].splitlines()
 require([h for h in headers if h.startswith(b'parent ')]==[b'parent '+plan['base_commit'].encode()] and [h for h in headers if h.startswith(b'tree ')]==[b'tree '+proposed.encode()],'sole exact final parent/tree')
 j.update(proposed_commit=commit,tree=proposed,status='push_dispatch_pending');m.dump(run_dir/'RECEIPT.json',j)
 guard(plan,j);local_preimages(plan);require(m.remote(j)==plan['base_commit'],'dispatch direct-main guard')
 j['status']='push_outcome_unresolved';m.dump(run_dir/'RECEIPT.json',j)
 m.git(['push','--no-verify','--no-follow-tags',n.URL,commit+':refs/heads/main'],j)
 j.update(published_commit=commit,status='public_published_program_install_pending_readback');m.dump(run_dir/'RECEIPT.json',j)
 public_readback(plan,j,commit);guard(plan,j);local_preimages(plan)
 j.update(status='published_program_install_pending',public_full_body_mode_readback=True,remote_changed_path_count=len(plan['members']),local_install_path_count=3,whole_parent_tree_preserved_outside_exact_overlay=True,sole_parent=plan['base_commit'])

def prior_public(prior,plan,j):
 require(prior['schema']=='pr147-final-checkpoint-operation-receipt/v1' and prior['action']=='publish' and prior['status']=='published_program_install_pending' and prior['fixture_only'] is False and 'error_type' not in prior and prior['own_operation_lock_released'] is True,'actual completed final public receipt')
 for key in ('source_sha256','plan_sha256','review_sha256','request_sha256','native_acceptance_sha256'):require(prior[key]==j[key],'same reviewed final publication '+key)
 require(type(prior['actual_PID']) is int and prior['actual_PID']>0 and m.children_custody_complete(prior) and prior['children'],'actual closed final publication children')
 require(prior['public_full_body_mode_readback'] is True and prior['whole_parent_tree_preserved_outside_exact_overlay'] is True and prior['sole_parent']==plan['base_commit'] and type(prior['remote_changed_path_count']) is int and prior['remote_changed_path_count']==len(plan['members']) and type(prior['local_install_path_count']) is int and prior['local_install_path_count']==3,'exact final public proof/scopes')
 for child in prior['children']:m.authenticate_child_custody(child);require(child['exit_code']==0,'successful final publisher child')
 root=absolute(prior['object_workspace']);require(D/'private' in root.parents and root.name=='object_workspace' and root.is_dir(),'prior final-public private workspace')
 return oid(prior['published_commit']),str(root)

def install(plan,j,run_dir,path,sha,exclusive):
 require(exclusive is True,'ROOT must confirm cooperative exclusion of all selected program writers now')
 spec=path_pin(absolute(path));require(spec['sha256']==sha_value(sha),'explicit whole final-public receipt SHA')
 prior=m.native_json(read(spec));commit,root=prior_public(prior,plan,j);j.update(object_workspace=root,published_commit=commit,known_selected_writer_exclusion_confirmed=True,status='public_program_install_pending',installed=[])
 guard(plan,j);local_preimages(plan);public_readback(plan,j,commit)
 j['published_receipt']=spec;m.dump(run_dir/'RECEIPT.json',j)
 for member in plan['members']:
  if member['install']:m.install_one(member,j,run_dir)
 installed=[]
 for member in plan['members']:
  if member['install']:
   spec=path_pin(C/member['path']);require(compact(spec)==member['post'],'complete installed program body/mode');installed.append(spec)
 require(len(installed)==3 and set(j['installed'])==PROGRAM,'exact three installed selected program files')
 guard(plan,j);require(m.remote(j)==commit,'final direct main unchanged after local install')
 j.update(status='public_and_program_install_verified',local_full_body_mode_readback=True,local_readback_path_count=3,installed_postimages=installed,whole_install_atomic=False,compare_and_swap_claimed=False,overall_goal_completion_claimed=False,independent_ROOT_final_acceptance_pending=True)

def operation(args):
 run_dir=absolute(args.run_dir);require(run_dir.parent==D/'private','fresh operation run-directory scope');run_dir.mkdir(exist_ok=False)
 j={'schema':'pr147-final-checkpoint-operation-receipt/v1','actual_PID':os.getpid(),'UTC_start':m.utc(),'action':args.action,'children':[],'child_custody_root':str(run_dir/'raw'),'source_sha256':digest(Path(__file__).read_bytes()),'dependency_sha256':DEPENDENCY_SHA,'plan_sha256':args.plan_sha,'review_sha256':args.review_sha,'fixture_only':False,'status':'starting','auto_retry_performed':False,'overall_goal_completion_claimed':False}
 lock=D/'private/OPERATION_LOCK.json';identity=None;owned=None
 try:
  m.local_case_guard(lock);fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,420)
  try:
   info=os.fstat(fd);identity=(info.st_dev,info.st_ino);j['operation_lock_identity']={'dev':info.st_dev,'ino':info.st_ino}
   view=memoryview(canonical({'actual_PID':os.getpid(),'UTC':m.utc(),'plan_sha256':args.plan_sha}))
   while view:written=os.write(fd,view);require(written>0,'owned lock write progress');view=view[written:]
   os.fsync(fd)
  finally:os.close(fd)
  owned=path_pin(lock);j['operation_lock']=owned;j['status']='plan_validation_pending';m.dump(run_dir/'RECEIPT.json',j);plan=load(args.plan,args.plan_sha,args.review,args.review_sha);j.update(request_sha256=plan['request']['sha256'],native_acceptance_sha256=plan['native_acceptance']['sha256']);j['status']='actual_plan_authenticated';m.dump(run_dir/'RECEIPT.json',j)
  if args.action=='publish':publish(plan,j,run_dir)
  else:install(plan,j,run_dir,args.published_receipt,args.published_receipt_sha,args.exclusive_known_writers_confirmed)
 except BaseException as error:
  j.update(error_type=type(error).__name__,error=str(error)[:4096])
  if isinstance(error,m.JournalWriteFailure):j['journal_write_failure']=error.journal_write_failure
  if j.get('published_commit'):j['failure_state']='public_published_program_install_pending'
  raise
 finally:
  safe=m.children_custody_complete(j);j['all_obtained_children_complete']=safe
  if identity is not None and safe:
   try:
    m.safe(lock);info=lock.lstat();require((info.st_dev,info.st_ino)==identity,'owned operation lock inode');require(owned is not None,'owned lock body pin unavailable; retain barrier');full_pin(owned);lock.unlink();j['own_operation_lock_released']=True
   except BaseException as error:j.update(own_operation_lock_released=False,lock_release_error=str(error))
  elif identity is not None:j.update(own_operation_lock_released=False,lock_retained_for_unresolved_custody=True)
  j['UTC_end']=m.utc()
  try:m.dump(run_dir/'RECEIPT.json',j)
  except BaseException:
   print(json.dumps({'final_receipt_persistence_failed':True,'journal':j},sort_keys=True));raise
 require(j.get('own_operation_lock_released') is True,'owned barrier release incomplete')
 print(json.dumps({'status':j['status'],'receipt':path_pin(run_dir/'RECEIPT.json')}))

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
 for action in ('plan-sha','prepare'):
  p=sub.add_parser(action);p.add_argument('--request',required=True);p.add_argument('--request-sha',required=True)
  if action=='prepare':p.add_argument('--expected-plan-sha',required=True);p.add_argument('--plan',required=True)
 for action in ('publish','install'):
  p=sub.add_parser(action)
  for key in ('plan','plan-sha','review','review-sha','run-dir'):p.add_argument('--'+key,required=True)
  if action=='install':p.add_argument('--published-receipt',required=True);p.add_argument('--published-receipt-sha',required=True);p.add_argument('--exclusive-known-writers-confirmed',action='store_true')
 args=parser.parse_args()
 if args.action in ('plan-sha','prepare'):
  spec=path_pin(absolute(args.request));require(spec['sha256']==sha_value(args.request_sha),'explicit complete actual request SHA');plan=proposal(spec);data=canonical(plan);sha=digest(data)
  if args.action=='prepare':
   require(sha==sha_value(args.expected_plan_sha),'exact expected plan SHA');path=absolute(args.plan);require(D/'private' in path.parents and not path.exists(),'fresh private canonical plan')
   with path.open('xb') as handle:handle.write(data);handle.flush();os.fchmod(handle.fileno(),420);os.fsync(handle.fileno())
   require(path.read_bytes()==data,'whole prepared plan readback')
  print(json.dumps({'status':'PLAN_ONLY_NOT_FINAL_ACCEPTANCE','plan_sha256':sha,'remote_paths':len(plan['members']),'local_install_paths':3}))
 else:operation(args)
if __name__=='__main__':main()
