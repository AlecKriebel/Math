"""Read-only native candidate-plan capture. No operator/import/writer/Git mutation."""
from pathlib import Path,PurePosixPath
import ast,datetime,hashlib,json,os,signal,stat,subprocess,time
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A=C/'draft_pr_publication_program_20260930/audits/pr140_5100023'
D=A/'native_acceptance_candidate_plan_preparation_v2_20261007'
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
def main():
    require(pin(SOURCE)['sha256']==EXPECTED_SOURCE,'source changed before candidate capture')
    old=jsonread(A/'scoped_active_checkpoint_20261007/PLAN_ACTIVE_v2.json')
    authpath=A/'ROOT_NATIVE_PUBLICATION_INPUTS_AUTHENTICATION_20261007.json';auth=jsonread(authpath)
    nativepath=A/'native_data_source_preparation_20261007/actual_request_preparation_v1/POSTIMAGE_MANIFEST.json';native=jsonread(nativepath)
    repairpath=A/'canonical_repair_preparation_v1_20261007/NINE_REPAIR_MANIFEST.json';repairs=jsonread(repairpath)
    originalpath=A/'ORIGINAL17_MANIFEST.json';original=jsonread(originalpath)
    base=run([GH,'api','repos/AlecKriebel/Math/git/ref/heads/main','--jq','.object.sha']).decode().strip()
    require(base==native['actual_MAIN']==auth['PR140_merge']['commit'],'fresh candidate base is actual merged3eb; rebuild if changed')
    git(['cat-file','-e',base+'^{commit}'])
    heads={}
    for label,root in [('R',R),('C',C)]:
        h=git(['-C',str(root),'rev-parse','HEAD','refs/heads/main']).decode().splitlines()
        require(len(h)==2 and h[0]==h[1],'main HEAD required');heads[label]=h[0]
    protected={};absences=set(old['protected_absences']);old_changes=[]
    for x in old['protected']:
        current=pin(x['path']);require(current=={k:x[k] for k in ['bytes','mode','sha256']},'prior273 protected pin changed '+x['path'])
        protected[x['path']]={**x}
    for p in list(absences):require(not safe(p).exists(),'prior protected absence changed '+p)
    def protect(p):
        p=safe(p);sp=str(p)
        if p.exists():
            v=full(p);require(sp not in absences,'protected present/absent collision');protected[sp]=v
        else:require(sp not in protected,'protected absence/present collision');absences.add(sp)
    for root in [R,C]:
        for name in ['index','config','HEAD','packed-refs','FETCH_HEAD','refs/heads/main','refs/remotes/origin/main','index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock']:protect(root/'.git'/name)
    for name in ['queue.py','manifest.json','policy.json','cache/catalog.sqlite']:
        p=C/'unsolved_math_prioritization'/name;require(not safe(p).exists(),'backend/cache must remain absent');protect(p)
    for name in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']:protect(C/'draft_pr_publication_program_20260930'/name)
    for m in original['members']:protect(A/'original'/m['relative'])
    members=[]
    for m in native['members']:
        post=m['postimage'];local=m['physical_C_preimage']
        require(local['path']==str(C/m['repo_relative']),'native physical identity')
        if local['present']:expect(local['path'],local);pre={k:local[k] for k in ['bytes','mode','sha256']}
        else:require(not safe(local['path']).exists(),'new native path became present');pre=None
        members.append({'path':m['repo_relative'],'source':post['path'],'post':{k:post[k] for k in ['bytes','mode','sha256']},'install':True,'local_pre':pre})
    for m in repairs['members']:
        expect(m['source'],m['post']);expect(m['physical_original_preimage']['path'],m['physical_original_preimage'])
        members.append({'path':m['repo_relative'],'source':m['source'],'post':m['post'],'install':True,'local_pre':{k:m['physical_original_preimage'][k] for k in ['bytes','mode','sha256']}})
    require(len(members)==23 and len({m['path'] for m in members})==23,'native14 plus repair9')
    selected={m['path'] for m in members}
    for m in original['members']:
        if m['path'] not in selected:protect(C/m['path'])
    curated=[
      'ROOT_NATIVE_PUBLICATION_INPUTS_AUTHENTICATION_20261007.json','ROOT_ACTUAL_R1_FINAL_PACKAGE_REPAIR_RELATIONSHIP_20261007.json','ROOT_CLEAN_PUBLICATION_GATE_20261007.json',
      'actual_published_record_20261007/RESULT.json','actual_tracker_20261007/RESULT.json','actual_tracker_20261007/SHEET_RECEIPT.json','actual_original_head_merge_20261007/RESULT.json',
      'merged_original17_local_materialization_20261007/RECEIPT.json',
      'native_data_source_preparation_20261007/actual_request_preparation_v1/POSTIMAGE_MANIFEST.json',
      'canonical_repair_preparation_v1_20261007/NINE_REPAIR_MANIFEST.json','canonical_repair_preparation_v1_20261007/PREPARATION_RECEIPT.json',
      'native_data_source_preparation_20261007/successor_actual_review_lineage_v4/native_data_builder_v4_r1.py',
      'native_data_source_preparation_20261007/successor_actual_review_lineage_v4/SOURCE_SEAL_V4.json',
    ]
    for sub,name in [('native_publication_operator_preparation_20261007','SOURCE_PREPARATION_SEAL.json'),
                     ('native_publication_operator_preparation_20261007/successor_lifecycle_admission_v2','SOURCE_PREPARATION_SEAL_V2.json'),
                     ('native_publication_operator_preparation_20261007/successor_casefold_curation_v3','SOURCE_PREPARATION_SEAL_V3.json')]:
        seal=jsonread(A/sub/name);curated.append(sub+'/'+name)
        for x in seal['members']:expect(x['path'],x);curated.append(str(Path(x['path']).relative_to(A)))
    curated+=['native_publication_operator_preparation_20261007/PREPARATION_SCOPE_CLARIFICATION.md']
    curated+=['RESEARCH_LOG.md','ROOT_NATIVE_V5_DRAFT_REQUEST_CUSTODY_ACCEPTANCE_20261007.json','ROOT_GENUINE_NATIVE_SOURCE_FINDINGS_AUTHENTICATION_20261007.json','object_only_merged_main_fetch_20261007/RECEIPT.json']
    for folder in ['native_publication_operator_source_adversary_20261007/v1_lifecycle_fail_20261007','native_publication_operator_source_adversary_20261007/v2_case_filter_fail_20261007','native_data_builder_source_and_data_adversary_20261007']:
        for name in ['REPORT.md','RESULT.json','FINAL_MANIFEST.json']:curated.append(folder+'/'+name)
    folder='native_data_source_preparation_20261007/successor_typed_numeric_v5'
    for name in ['native_data_builder_v5.py','SOURCE_SEAL_V5.json','V5_ACTUAL14_MEMORY_EQUIVALENCE.json','SOURCE_EXISTING14_SIDECAR_SEAL_V5.json','REPORT_V5.md','REPORT_V5_DATA_RELATIONSHIP.md','AST_DELTA_V5.json','SOURCE_DIFF_V4_TO_V5.patch','RESEARCH_LOG_V5.md']:curated.append(folder+'/'+name)
    relationship=jsonread(A/'ROOT_ACTUAL_R1_FINAL_PACKAGE_REPAIR_RELATIONSHIP_20261007.json')
    for member in relationship['full29_member_comparison']:
        for phase in ['R1','final_R2']:
            x=member[phase];expect(x['path'],x);curated.append(str(Path(x['path']).relative_to(A)))
    for folder in ['whole_publication_adversary_r1_20261007','whole_publication_adversary_r2_20261007']:
        manifest=jsonread(A/folder/'FINAL_MANIFEST.json');require(len(manifest['members'])==manifest['member_count'],'closed whole-package review inventory')
        curated.append(folder+'/FINAL_MANIFEST.json')
        for m in manifest['members']:
            rel=m['relative'];require(str(PurePosixPath(rel))==rel and not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts,'canonical public review member')
            require(not any(x.casefold().startswith('private') or x.casefold() in ['cache','.git'] for x in PurePosixPath(rel).parts),'private whole-review member forbidden')
            expect(A/folder/rel,m);curated.append(folder+'/'+rel)
    curated+=['ROOT_PACKAGE_R2_CANDIDATE_READBACK.json','ROOT_PACKAGE_R1_ACCEPTANCE_AND_REPAIR_PREPARATION.json','ROOT_PACKAGE_PREPARATION_20261007.json','ROOT_PACKAGE_CANDIDATE_READBACK.json','OWN_COMPLETED_GIT_RECOVERABLE_CACHES_CLEANUP_20261007.json','ROOT_PURE_V5_SOURCE_AND_DRAFT14_AUTHENTICATION_20261007.json']
    mode_copies=[]
    for rel in sorted(set(curated)):
        path=A/rel;original_pin=full(path);post=pin(path);source=path
        if post['mode']==292:
            source=D/'private_controls/public_payload'/rel;source.parent.mkdir(parents=True,exist_ok=True)
            if source.exists():expect(source,{**post,'mode':420})
            else:source.write_bytes(path.read_bytes());os.chmod(source,420)
            post=pin(source);require(post['bytes']==original_pin['bytes'] and post['sha256']==original_pin['sha256'],'mode-copy full bytes changed')
            mode_copies.append({'publication_path':str(path.relative_to(C)),'original':original_pin,'prepared0644_copy':full(source)});protect(path)
        require(post['mode']==420,'only original0644 or exact copy of closed0444 may be selected')
        rp=str(path.relative_to(C));require(not any(x.casefold().startswith('private') or x.casefold() in ['cache','.git','postimages14'] for x in PurePosixPath(rp).parts),'private/duplicate selection')
        members.append({'path':rp,'source':str(source),'post':post,'install':False,'local_pre':None});protect(path)
    dependencies={'unsolved_math_prioritization/'+n for n in ['queue.py','manifest.json','policy.json','SHORTLIST.md']}
    dependencies|={m['path'] for m in original['members']}
    needed=sorted(dependencies|{m['path'] for m in members})
    raw=git(['ls-tree','-r','-z',base,'--',*needed]);entries={}
    for entry in raw.split(b'\0'):
        if not entry:continue
        meta,path=entry.split(b'\t',1);mode,typ,oid=meta.decode().split()
        name=path.decode();require(typ=='blob' and mode=='100644' and name not in entries,'immutable input blob/mode/identity')
        entries[name]={'Git_blob':oid,'Git_mode':mode,'tree_sha256':digest(entry+b'\0')}
    ids=sorted({x['Git_blob'] for x in entries.values()});body=git(['cat-file','--batch'],('\n'.join(ids)+'\n').encode());view=memoryview(body);pos=0;blobs={}
    for oid in ids:
        end=body.index(b'\n',pos);fields=body[pos:end].decode().split();require(fields[0]==oid and fields[1]=='blob','full batch frame identity');size=int(fields[2]);pos=end+1
        require(len(body)>=pos+size+1 and body[pos+size:pos+size+1]==b'\n','full batch frame length')
        bv=view[pos:pos+size];gh=hashlib.sha1();gh.update(('blob '+str(size)+'\0').encode());gh.update(bv);require(gh.hexdigest()==oid,'full Git blob ID')
        blobs[oid]={'bytes':size,'sha256':hashlib.sha256(bv).hexdigest()};pos+=size+1
    require(pos==len(body),'batch exact coverage');del view,body
    remote_inputs=[]
    for name in sorted(dependencies):
        require(name in entries,'required original/dependency absent');remote_inputs.append({'path':name,**blobs[entries[name]['Git_blob']],'tree_sha256':entries[name]['tree_sha256']})
    for m in original['members']:
        require(entries[m['path']]['Git_blob']==m['Git_blob'] and blobs[m['Git_blob']]=={k:m[k] for k in ['bytes','sha256']},'all17 original merged canonical immutable bodies')
    changed=[]
    for m in members:
        e=entries.get(m['path']);m['pre_tree_sha256']=e['tree_sha256'] if e else digest(b'');m['post_blob']=blob_oid(m['source'],m['post'])
        if e is None or e['Git_blob']!=m['post_blob']:changed.append(m['path'])
        protect(Path(m['source']))
    install_paths={str(C/m['path']) for m in members if m['install']}
    prior_authorized_target_exclusions=[]
    install_by_path={str(C/m['path']):m for m in members if m['install']}
    for path in sorted(install_paths):
        local_pre=install_by_path[path]['local_pre']
        if path in protected:
            require(local_pre=={k:protected[path][k] for k in ['bytes','mode','sha256']},'authorized install preimage must match inherited protection')
            prior_authorized_target_exclusions.append({'path':path,'prior_protected':protected.pop(path),'local_pre':local_pre,'reason':'exact authorized native/repair installation; preimage protected through local_pre and immutable Git'})
        if path in absences:
            require(local_pre is None and not safe(path).exists(),'authorized absent installation has unexpected preimage')
            absences.remove(path);prior_authorized_target_exclusions.append({'path':path,'prior_absent':True,'local_pre':None,'reason':'exact authorized native/repair new path'})
    require(not install_paths&(set(protected)|absences),'selected install/protected collision')
    require(run([GH,'api','repos/AlecKriebel/Math/git/ref/heads/main','--jq','.object.sha']).decode().strip()==base,'remote moved during capture')
    for x in protected.values():expect(x['path'],x)
    for p in absences:require(not safe(p).exists(),'absence changed during capture')
    plan={'schema':'pr140-native-publication-overlay/v1','transaction':'native_acceptance','UTC':utc(),'actual_preparer_PID':os.getpid(),'action_executed':False,'operation_clearance':False,'candidate_SOURCE_and_DATA_reviews_pending':True,
          'source_sha256':EXPECTED_SOURCE,'base_commit':base,'R_HEAD':heads['R'],'C_HEAD':heads['C'],'previous_PR134_original_head':old['previous_PR134_original_head'],'closing_comment_body_sha256':old['closing_comment_body_sha256'],'current_PR140_original_head':auth['original_head'],'PR140_merge':auth['PR140_merge'],'original17_manifest':full(originalpath),'actual_acceptance_inputs':full(authpath),
          'canonical_repair_paths':sorted(m['repo_relative'] for m in repairs['members']),'members':sorted(members,key=lambda m:m['path']),'expected_changed_paths':sorted(changed),'protected':sorted(protected.values(),key=lambda x:x['path']),'protected_absences':sorted(absences),'protected_remote_inputs':remote_inputs,'git_executable':pin(G),'gh_executable':pin(GH),'commit_message':'Accept and publish verified PR140 antipedal centroid result with canonical evidence and repairs',
          'native14_postimage_manifest':full(nativepath),'canonical9_repair_manifest':full(repairpath),'prior_protected_authorized_install_target_exclusions':prior_authorized_target_exclusions,'package29_final_and_R1_snapshot29_curated':True,'complete_whole_package_R1_R2_public_corpora_curated':True,'predecessor_candidate_plan':full(A/'native_acceptance_candidate_plan_preparation_20261007/NATIVE_ACCEPTANCE_CANDIDATE_PLAN.json'),'program3_selected':False,'data_preparer_source_pending_V5_successor':True}
    path=D/'NATIVE_ACCEPTANCE_CANDIDATE_PLAN.json';path.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n')
    report={'schema':'pr140-native-readonly-candidate-plan-preparation/v1','UTC':utc(),'actual_PID':os.getpid(),'plan':full(path),'source':full(SOURCE),'full_immutable_main':base,'native_count':14,'repair_count':9,'publication_package29_and_archivedR1_29_selected':True,'R1_public25_plus_manifest_and_R2_public40_plus_manifest_selected':True,'audit_member_count':len(members)-23,'member_count':len(members),'expected_changed_path_count':len(changed),'protected_count':len(protected),'prior273_all_whole_verified_before_authorized_install_target_partition':True,'prior_protected_authorized_install_target_exclusions':prior_authorized_target_exclusions,'original17_Git_and_archive_preserved':True,'six_historical_C_canonical_pinned':True,'program3_excluded_and_current_physical_pinned':True,'full_input_batch_blob_count':len(ids),'source_mode_copies':mode_copies,'children':children,'all_read_children_reaped_groups_absent':all(x['reaped'] and x['group_absent'] for x in children),'data_SOURCE_V5_and_SOURCE_V3_DATA_actualplan_reviews_pending':True,'protected_maps_source_refs_indices_config_caches_unchanged':True,'source_operator_import_or_action':False,'Git_or_native_or_service_mutation':False,'scope':'READ_ONLY_CANDIDATE_NOT_OPERATION_CLEARANCE'}
    rp=D/'CANDIDATE_PREPARATION_RECEIPT.json';rp.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({'plan':full(path),'receipt':full(rp),'actual_PID':os.getpid(),'member_count':len(members),'protected_count':len(protected)}))
if __name__=='__main__':
    try:main()
    except BaseException as exc:
        out=D/'private_controls/FAILED_CAPTURE.json'
        if out.exists():out=out.with_name('FAILED_CAPTURE_'+str(os.getpid())+'.json')
        out.write_text(json.dumps({'UTC':utc(),'actual_PID':os.getpid(),'error_type':type(exc).__name__,'error':str(exc),'children':children,'operator_or_writer_action':False},indent=2,sort_keys=True)+'\n');raise
