"""Read-only native candidate-plan capture. No operator/import/writer/Git mutation."""
from pathlib import Path,PurePosixPath
import ast,datetime,hashlib,json,os,signal,stat,subprocess,time
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A=C/'draft_pr_publication_program_20260930/audits/pr140_5100023'
D=A/'final_metadata_proposal_preparation_20261007'
G='/opt/homebrew/Cellar/git/2.38.2/bin/git';GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
SOURCE=A/'native_publication_operator_preparation_20261007/successor_casefold_curation_v3/native_publication_operator_v3.py'
EXPECTED_SOURCE='adc52e0722e58a15ecfb7e6f92b4ea71657115478d72569ab9292253b1f89b75'
def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def safe(p):
    p=Path(p);require(p.is_absolute(),'absolute path')
    for q in [p,*p.parents]:require(not q.is_symlink(),'symlink '+str(q))
    return p
def pin(p):
    p=safe(p);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        a=os.fstat(fd);require(stat.S_ISREG(a.st_mode) and a.st_nlink==1,'regular single-link')
        h=hashlib.sha256()
        while b:=os.read(fd,1048576):h.update(b)
        z=os.fstat(fd);n=p.lstat()
        sig=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_size,x.st_mtime_ns,x.st_ctime_ns,x.st_nlink)
        require(sig(a)==sig(z)==sig(n),'changed while read')
        return {'bytes':a.st_size,'mode':stat.S_IMODE(a.st_mode),'sha256':h.hexdigest()}
    finally:os.close(fd)
def full(p):return {'path':str(p),**pin(p)}
def expect(p,s):require(pin(p)=={k:s[k] for k in ['bytes','mode','sha256']},'full pin changed '+str(p))
children=[]
def run(argv,data=None):
    e={'UTC_start':utc(),'argv':argv};children.append(e)
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env.update(GIT_OPTIONAL_LOCKS='0',GIT_NO_REPLACE_OBJECTS='1')
    p=subprocess.Popen(argv,cwd=R,env=env,stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);e['PID']=p.pid
    try:out,err=p.communicate(data,timeout=45)
    except BaseException:
        try:os.killpg(p.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        p.communicate(timeout=5);raise
    finally:
        try:os.killpg(p.pid,0);empty=False
        except ProcessLookupError:empty=True
        if not empty:
            try:os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            until=time.monotonic()+1
            while time.monotonic()<until:
                try:os.killpg(p.pid,0)
                except ProcessLookupError:empty=True;break
                time.sleep(.05)
        e.update(UTC_end=utc(),exit_code=p.returncode,reaped=p.returncode is not None,group_absent=empty)
    require(p.returncode==0 and empty,'bounded reader failed '+repr(argv))
    e.update(stdout_bytes=len(out),stdout_sha256=digest(out),stderr_bytes=len(err),stderr_sha256=digest(err));return out
def git(args,data=None):return run([G,'-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','core.splitIndex=false',*args],data)
def jsonread(p):return json.loads(safe(p).read_bytes())
def blob_oid(p,s):
    expect(p,s);h=hashlib.sha1();h.update(('blob '+str(s['bytes'])+'\0').encode())
    with safe(p).open('rb') as f:
        while b:=f.read(1048576):h.update(b)
    expect(p,s);return h.hexdigest()
PROGRAM_PREFIX='draft_pr_publication_program_20260930/'
PROGRAM={PROGRAM_PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
ACTUAL_NATIVE='0d5ae675f8a51e0eaead04d0bf20cdce3f182c8d'
COMPLETION_SHA='566642767a1a71f8c36081dae3bfa4d4bdb53ebbbe336ae1c94560a4c613f54c'
PROGRAM_MANIFEST_SHA='41f3641b63ff73fda25c668949ea4114dac77c21c3002714a9338128e258678c'

def main():
    require(not (D/'FINAL_METADATA_PROPOSAL.json').exists(),'distinct proposal only; never overwrite a frozen proposal')
    require(pin(SOURCE)['sha256']==EXPECTED_SOURCE,'accepted operator source changed')
    oldpath=A/'native_acceptance_candidate_plan_preparation_v2_20261007/NATIVE_ACCEPTANCE_CANDIDATE_PLAN.json'
    old=jsonread(oldpath)
    require(pin(oldpath)['sha256']=='8c3aeb57b8ce68111961e4e69098e9e6d915ae5214cc801910f92d1a159c2460','completed native plan pin')
    completionpath=A/'ROOT_NATIVE_PUBLICATION_INSTALLATION_ACCEPTANCE_20261007.json';completion=jsonread(completionpath)
    require(pin(completionpath)['sha256']==COMPLETION_SHA and completion['published_commit']==ACTUAL_NATIVE,'genuine native completion pin')
    for role in ['source','plan','publish','install','root_readback','combined_source_data_acceptance']:
        expect(completion[role]['path'],completion[role])
    authpath=A/'ROOT_NATIVE_PUBLICATION_INPUTS_AUTHENTICATION_20261007.json';auth=jsonread(authpath)
    require(full(authpath)==completion['actual_acceptance_inputs']==old['actual_acceptance_inputs'],'same actual publication/tracker/merge custody')
    programpath=A/'final_program3_current_readback_pointer_repair_20261007/MANIFEST.json';program=jsonread(programpath)
    require(pin(programpath)['sha256']==PROGRAM_MANIFEST_SHA,'actual corrected3 manifest')
    require(program['preparation_only'] is True and program['final_transaction_not_performed'] is True and program['final_metadata_commit'] is None,'honest unperformed final proposal')
    require({m['repo_path'] for m in program['files']}==PROGRAM and len(program['files'])==3,'exact program3')
    for x in program['full_inputs']:expect(x['path'],x)
    base=run([GH,'api','repos/AlecKriebel/Math/git/ref/heads/main','--jq','.object.sha']).decode().strip()
    require(base==ACTUAL_NATIVE,'remote moved since native completion; compose fresh proposal')
    git(['cat-file','-e',base+'^{commit}'])
    heads={}
    for label,root in [('R',R),('C',C)]:
        h=git(['-C',str(root),'rev-parse','HEAD','refs/heads/main']).decode().splitlines()
        require(len(h)==2 and h[0]==h[1],'actual local main HEAD');heads[label]=h[0]
    protected={};absences=set(old['protected_absences']);phase_changes=[]
    current_case_log=str(A/'RESEARCH_LOG.md')
    selected_program={str(C/name) for name in PROGRAM}
    for x in old['protected']:
        current=full(x['path'])
        if x['path']==current_case_log:
            require(current['mode']==420 and current['bytes']==8186,'ROOT case98 log expected exact current size/mode')
            phase_changes.append({'path':x['path'],'historical_native_plan_pin':x,'current_final_phase_pin':current,'reason':'ROOT dated98-percent checkpoint after actual native readback; historical native plan remains untouched'})
        else:require(current==x,'unapproved protected resource drift '+x['path'])
        protected[x['path']]=current
    for path in absences:require(not safe(path).exists(),'prior protected absence changed '+path)
    def protect(p):
        p=safe(p);sp=str(p)
        if p.exists():
            v=full(p);require(sp not in absences,'protected present/absent collision');protected[sp]=v
        else:
            require(sp not in protected,'protected absence/present collision');absences.add(sp)
    for root in [R,C]:
        for name in ['index','config','HEAD','packed-refs','FETCH_HEAD','refs/heads/main','refs/remotes/origin/main','index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock']:protect(root/'.git'/name)
    for name in ['queue.py','manifest.json','policy.json','cache/catalog.sqlite']:
        p=C/'unsolved_math_prioritization'/name;require(not safe(p).exists(),'backend/cache must remain absent');protect(p)
    require(len(completion['installed_postimages'])==23,'genuine completed14+9 inventory')
    for x in completion['installed_postimages']:expect(x['path'],x);protect(x['path'])
    original=jsonread(A/'ORIGINAL17_MANIFEST.json')
    for m in original['members']:expect(A/'original'/m['relative'],m);protect(A/'original'/m['relative'])
    members=[]
    for m in program['files']:
        rel=m['repo_path'];require(m['preimage']['path']==str(C/rel),'program physical preimage identity')
        expect(m['preimage']['path'],m['preimage']);expect(m['postimage']['path'],m['postimage'])
        if rel.endswith('.md'):require(Path(m['postimage']['path']).read_bytes().startswith(Path(m['preimage']['path']).read_bytes()),'complete existing program prose prefix')
        members.append({'path':rel,'source':m['postimage']['path'],'post':{k:m['postimage'][k] for k in ['bytes','mode','sha256']},'install':True,'local_pre':{k:m['preimage'][k] for k in ['bytes','mode','sha256']}})
    curated=[
        'RESEARCH_LOG.md',
        'ROOT_NATIVE_PUBLICATION_INSTALLATION_ACCEPTANCE_20261007.json',
        'actual_native_root_readback_20261007/ROOT_READBACK.json',
        'ROOT_NATIVE_ACTUAL_PUBLICATION_READBACK_20261007.json',
        'ROOT_NATIVE_PLAN_207_COMBINED_SOURCE_DATA_ACCEPTANCE_20261007.json',
        'ROOT_NATIVE_PLAN_207_CUSTODY_AUTHENTICATION_20261007.json',
        'ROOT_NATIVE_READBACK_HELPER_SOURCE_ACCEPTANCE_20261007.json',
        'ROOT_NATIVE_OPERATOR_V3_SOURCE_AUTHENTICATION_20261007.json',
        'ROOT_ACTUAL_NATIVE_DATA14_CANONICAL9_AUTHENTICATION_20261007.json',
        'ROOT_PURE_V5_SOURCE_AND_DRAFT14_AUTHENTICATION_20261007.json',
        'ROOT_GENUINE_NATIVE_SOURCE_FINDINGS_AUTHENTICATION_20261007.json',
        'ROOT_NATIVE_STARTUP_DIRECTORY_REPAIR_20261007.json',
        'ROOT_FRESH_GOAL_READBACK_FOR_FINAL_METADATA_20261007.json',
        'ROOT_NATIVE_STORAGE_FAILURE_RECOVERY_SEQUENCE_20261007.json',
        'OWN_COMPLETED_GIT_RECOVERABLE_CACHES_CLEANUP_20261007.json',
        'OWN_COMPLETED_IMMUTABLE_INDEX_LIST_CACHE_CLEANUP_20261007.json',
        'OWN_COMPLETED_IMMUTABLE_TREE_CACHE_CLEANUP_20261007.json',
        'OWN_COMPLETED_DUPLICATE_CACHE_RECOVERY_CLEANUP_20261007.json',
        'OWN_COMPLETED_BACKEND_SNAPSHOT_LOSSLESS_COMPRESSION_CLEANUP_20261007.json',
        'native_acceptance_candidate_plan_preparation_v2_20261007/NATIVE_ACCEPTANCE_CANDIDATE_PLAN.json',
        'native_acceptance_candidate_plan_preparation_v2_20261007/CANDIDATE_PREPARATION_RECEIPT.json',
        'native_acceptance_candidate_plan_preparation_v2_20261007/prepare_readonly_native_candidate_plan.py',
        'final_metadata_proposal_preparation_20261007/FRESH_MAIN_PROGRAM3_PHYSICAL_COMPARISON.json',
        'final_metadata_proposal_preparation_20261007/prepare_readonly_final_metadata_proposal.py',
        'final_metadata_proposal_preparation_20261007/RESEARCH_LOG.md',
    ]
    for folder in ['native_acceptance_readback_helper_preparation_20261007','final_program3_renderer_source_preparation_20261007','final_program3_current_readback_pointer_repair_20261007','final_program3_conditional_templates_preparation_20261007']:
        for p in sorted((A/folder).iterdir()):
            if p.is_file() and p.name!='.gitignore':curated.append(str(p.relative_to(A)))
    for folder,kind in [('native_publication_operator_source_adversary_20261007','members'),('native_data_builder_source_and_data_adversary_20261007/exact_plan_v2_data_review_20261007','files')]:
        mp=A/folder/'FINAL_MANIFEST.json';manifest=jsonread(mp);curated.append(str(mp.relative_to(A)))
        for m in manifest[kind]:
            p=Path(m['path']) if kind=='files' else A/folder/m['path']
            expect(p,m)
            if m.get('ignored_private_control') is True:continue
            if any(x.casefold().startswith('private') or x.casefold() in ['cache','.git','.gitignore'] for x in p.relative_to(A).parts):continue
            curated.append(str(p.relative_to(A)))
    copies=[]
    for label,path in [('PUBLISH_01',completion['publish']['path']),('INSTALL_03',completion['install']['path']),('FAILED_INSTALL_01',str(A/'native_publication_operator_preparation_20261007/private/actual_native_install_01/RECEIPT.json')),('FAILED_INSTALL_02',str(A/'native_publication_operator_preparation_20261007/private/actual_native_install_02/RECEIPT.json'))]:
        origin=full(path);target=D/'public_actual_native_operations'/(label+'_RECEIPT.json');target.parent.mkdir(parents=True,exist_ok=True)
        require(not target.exists(),'receipt copy must be newly prepared');target.write_bytes(Path(path).read_bytes());os.chmod(target,420)
        post=full(target);require(post['sha256']==origin['sha256'] and post['bytes']==origin['bytes'],'full operation receipt byte-copy identity')
        copies.append({'role':label,'original_pin':origin,'public0644_copy_pin':post,'original_status':jsonread(path)['status'],'bytes_verbatim_original_unchanged':True});protect(path);curated.append(str(target.relative_to(A)))
    custodypath=D/'PUBLIC_OPERATION_AND_MODE_COPY_CUSTODY.json'
    mode_copies=[]
    def append_audit(rel):
        path=A/rel;original_pin=full(path);post=pin(path);source=path
        if post['mode']==292:
            source=D/'private_controls/public_payload'/rel;source.parent.mkdir(parents=True,exist_ok=True)
            require(not source.exists(),'distinct closed-mode copy');source.write_bytes(path.read_bytes());os.chmod(source,420)
            post=pin(source);require(post['bytes']==original_pin['bytes'] and post['sha256']==original_pin['sha256'],'closed-mode copy full bytes')
            mode_copies.append({'publication_path':str(path.relative_to(C)),'original_pin':original_pin,'prepared0644_copy_pin':full(source)})
        require(post['mode']==420,'public postimage0644')
        rp=str(path.relative_to(C));require(not any(x.casefold().startswith('private') or x.casefold() in ['cache','.git','postimages3','postimages14'] for x in PurePosixPath(rp).parts),'no private/cache/raw-postimage selection')
        require(path.is_relative_to(A) and not rp.casefold().startswith(str(A.relative_to(C)).casefold()+'/original/') and path!=A/'ORIGINAL17_MANIFEST.json','ownaudit only; original archive immutable')
        members.append({'path':rp,'source':str(source),'post':post,'install':False,'local_pre':None});protect(path);protect(source)
    for rel in sorted(set(curated)):append_audit(rel)
    custody={'schema':'pr140-final-metadata-public-receipt-copy-custody/v1','UTC':utc(),'actual_preparer_PID':os.getpid(),'operation_receipt_copies':copies,'closed0444_mode_copies':mode_copies,'sealed_original_bytes_modes_unchanged':True,'failed_installations_remain_failures':True,'publication_or_installation_executed':False}
    custodypath.write_text(json.dumps(custody,indent=2,sort_keys=True)+'\n');append_audit(str(custodypath.relative_to(A)))
    require(len({m['path'].casefold() for m in members})==len(members),'unique casefold member inventory')
    dependencies={'unsolved_math_prioritization/'+n for n in ['queue.py','manifest.json','policy.json','SHORTLIST.md']}
    dependencies|={m['path'] for m in original['members']}
    dependencies|={str(Path(x['path']).relative_to(C)) for x in completion['installed_postimages']}
    needed=sorted(dependencies|{m['path'] for m in members})
    raw=git(['ls-tree','-r','-z',base,'--',*needed]);entries={}
    for entry in raw.split(b'\0'):
        if not entry:continue
        meta,path=entry.split(b'\t',1);mode,typ,oid=meta.decode().split();name=path.decode()
        require(typ=='blob' and mode=='100644' and name not in entries,'immutable selected/dependency blob/mode/identity')
        entries[name]={'Git_blob':oid,'Git_mode':mode,'tree_sha256':digest(entry+b'\0')}
    ids=sorted({x['Git_blob'] for x in entries.values()});body=git(['cat-file','--batch'],('\n'.join(ids)+'\n').encode());view=memoryview(body);pos=0;blobs={}
    for oid in ids:
        end=body.index(b'\n',pos);fields=body[pos:end].decode().split();require(fields[0]==oid and fields[1]=='blob','full batch frame identity');size=int(fields[2]);pos=end+1
        require(len(body)>=pos+size+1 and body[pos+size:pos+size+1]==b'\n','full batch frame length')
        bv=view[pos:pos+size];h=hashlib.sha1();h.update(('blob '+str(size)+'\0').encode());h.update(bv);require(h.hexdigest()==oid,'whole Git blob body ID')
        blobs[oid]={'bytes':size,'sha256':hashlib.sha256(bv).hexdigest()};pos+=size+1
    require(pos==len(body),'exact whole batch coverage');del bv,view,body
    remote_inputs=[]
    for name in sorted(dependencies):
        require(name in entries,'required native/history dependency absent');remote_inputs.append({'path':name,**blobs[entries[name]['Git_blob']],'tree_sha256':entries[name]['tree_sha256']})
    for x in completion['installed_postimages']:
        rel=str(Path(x['path']).relative_to(C));require(blobs[entries[rel]['Git_blob']]=={k:x[k] for k in ['bytes','sha256']},'all23 installed bodies equal fresh immutable native MAIN')
    fresh_program_comparison=[];changed=[]
    for m in members:
        e=entries.get(m['path']);m['pre_tree_sha256']=e['tree_sha256'] if e else digest(b'');m['post_blob']=blob_oid(m['source'],m['post'])
        if e is None or e['Git_blob']!=m['post_blob']:changed.append(m['path'])
        if m['install']:
            require(e is not None and blobs[e['Git_blob']]=={k:m['local_pre'][k] for k in ['bytes','sha256']},'fresh MAIN program3 preimage must equal complete current physical body')
            fresh_program_comparison.append({'path':m['path'],'full_MAIN_blob':e,'body':blobs[e['Git_blob']],'physical_local_pre':m['local_pre'],'equal_full_bytes_modes':True})
        protect(m['source'])
    exclusions=[]
    for m in members:
        if m['install']:
            path=str(C/m['path']);require(path in protected and m['local_pre']=={k:protected[path][k] for k in ['bytes','mode','sha256']},'exact program install preimage protected before partition')
            exclusions.append({'path':path,'prior_protected':protected.pop(path),'local_pre':m['local_pre'],'reason':'exact reviewed program3 installation; complete physical and immutable MAIN preimage custody retained'})
    require({m['path'] for m in members if m['install']}==PROGRAM,'program3 is only local installation family')
    require(not selected_program&(set(protected)|absences),'program installation/protection collision')
    for x in completion['installed_postimages']:require(protected[x['path']]==x,'all23 completed native outputs fully immutable')
    require(run([GH,'api','repos/AlecKriebel/Math/git/ref/heads/main','--jq','.object.sha']).decode().strip()==base,'remote moved during final proposal capture')
    for x in protected.values():expect(x['path'],x)
    for path in absences:require(not safe(path).exists(),'absence drift during capture')
    plan={'schema':'pr140-native-publication-overlay/v1','transaction':'final_metadata','UTC':utc(),'actual_preparer_PID':os.getpid(),'action_executed':False,'operation_clearance':False,'candidate_SOURCE_and_DATA_reviews_pending':True,
          'source_sha256':EXPECTED_SOURCE,'base_commit':base,'R_HEAD':heads['R'],'C_HEAD':heads['C'],'previous_PR134_original_head':old['previous_PR134_original_head'],'closing_comment_body_sha256':old['closing_comment_body_sha256'],'current_PR140_original_head':auth['original_head'],'PR140_merge':auth['PR140_merge'],'original17_manifest':full(A/'ORIGINAL17_MANIFEST.json'),'actual_acceptance_inputs':full(authpath),'actual_native_completion':full(completionpath),
          'canonical_repair_paths':[],'members':sorted(members,key=lambda m:m['path']),'expected_changed_paths':sorted(changed),'protected':sorted(protected.values(),key=lambda x:x['path']),'protected_absences':sorted(absences),'protected_remote_inputs':remote_inputs,'git_executable':pin(G),'gh_executable':pin(GH),'commit_message':'Record completed PR140 publication and native acceptance in program progress',
          'completed_native_plan_unchanged':full(oldpath),'corrected_program3_proposal_manifest':full(programpath),'fresh_MAIN_program3_equals_whole_physical_preimages':fresh_program_comparison,'protected_family_dated_phase_changes':phase_changes,'protected_family_exact_program3_install_exclusions':exclusions,'installed_native23_protected':True,'no_native_or_canonical_repair_selection':True,'program3_selected':True,'prior_goal_incomplete_and_active_is_preserved':True,'final_actual_commit_readback_acceptance_not_fabricated':True}
    out=D/'FINAL_METADATA_PROPOSAL.json';out.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n')
    receipt={'schema':'pr140-final-metadata-readonly-proposal-preparation/v1','UTC':utc(),'actual_preparer_PID':os.getpid(),'source':full(SOURCE),'plan':full(out),'program3_manifest':full(programpath),'native_completion':full(completionpath),'member_count':len(members),'program3_install_count':3,'audit_member_count':len(members)-3,'expected_changed_path_count':len(changed),'protected_count':len(protected),'absence_count':len(absences),'full_fresh_MAIN_base':base,'native23_immutable':True,'original17_archive_and_unselected_canonical_history_preserved':True,'fresh_MAIN_program3_equals_whole_physical_preimages':fresh_program_comparison,'dated_phase_changes':phase_changes,'exact_program3_protected_exclusions':exclusions,'copy_custody':full(custodypath),'children':children,'all_read_children_reaped_and_groups_absent':all(x['reaped'] and x['group_absent'] for x in children),'scope':'READ_ONLY_PROPOSAL_NOT_OPERATION_CLEARANCE','independent_exact_DATA_review_pending':True,'operator_import_factory_or_writer_run':False,'Git_native_backend_or_provider_mutations':False}
    rp=D/'PROPOSAL_PREPARATION_RECEIPT.json';rp.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(json.dumps({'plan':full(out),'receipt':full(rp),'member_count':len(members),'protected_count':len(protected),'absence_count':len(absences),'actual_PID':os.getpid()}))

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        out=D/'private_controls'/('FAILED_CAPTURE_'+str(os.getpid())+'.json')
        out.write_text(json.dumps({'UTC':utc(),'actual_PID':os.getpid(),'error_type':type(exc).__name__,'error':str(exc),'children':children,'operator_or_writer_action':False},indent=2,sort_keys=True)+'\n');raise
