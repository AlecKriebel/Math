"""Read-only native candidate-plan capture. No operator/import/writer/Git mutation."""
from pathlib import Path,PurePosixPath
import ast,datetime,hashlib,json,os,signal,stat,subprocess,time
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A=C/'draft_pr_publication_program_20260930/audits/pr141_30003818'
D=A/'checkpoint_preparation_20261007'
G='/opt/homebrew/Cellar/git/2.38.2/bin/git';GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
SOURCE=D/'scoped_audit_checkpoint_publish.py'
EXPECTED_SOURCE='19ef8deeb6503256646af94edc69ad14d0715066e9008e68645b960f413ee431'
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
P=C/'draft_pr_publication_program_20260930'
PREVIOUS=P/'audits/pr140_5100023'
def main():
    require(not (D/'AUDIT_CHECKPOINT_PROPOSAL.json').exists(),'never overwrite captured proposal')
    require(pin(SOURCE)['sha256']==EXPECTED_SOURCE,'prepared source unchanged')
    prior_path=PREVIOUS/'ROOT_FINAL_METADATA_ACCEPTANCE_20261007.json';prior=jsonread(prior_path)
    require(pin(prior_path)['sha256']=='cee4dff32b212eac03bfc29844bcc0facd8a6e779aa0ebb2f15191c5449305a5','actual PR140 accepted completion')
    for role in ['source','plan','publish','install','root_readback','native_acceptance','actual_acceptance_inputs']:expect(prior[role]['path'],prior[role])
    old=jsonread(prior['plan']['path'])
    original_path=A/'ORIGINAL_SUBMITTED_ATTEMPT_MANIFEST.json';original=jsonread(original_path)
    require(original['head']=='523247e3246a5f44c7b0089074bb304c1f642bd0' and len(original['files'])==20,'actual original20 intake')
    gate=jsonread(A/'ROOT_MATHEMATICAL_GATE.json')
    require(gate['verdict']=='PASS_COMPLETE_EXPLICIT_TRANSFORM_LAW' and gate['original_head']==original['head'] and gate['mandatory_mathematical_corrections']==[] and gate['new_central_proof_turns']==0 and gate['original_members_unchanged']==20 and len(gate['independent_reviews'])==2,'genuine completed two-family mathematical gate')
    for review in gate['independent_reviews']:require(pin(review['manifest_path'])['sha256']==review['manifest_sha256'],'genuine closed mathematical review manifest')
    base=run([GH,'api','--method','GET','repos/AlecKriebel/Math/git/ref/heads/main','--jq','.object.sha']).decode().strip()
    require(len(base)==40,'actual current remote main');git(['cat-file','-e',base+'^{commit}'])
    git(['merge-base','--is-ancestor',prior['metadata_commit'],base])
    heads={}
    for label,root in [('R',R),('C',C)]:
        values=git(['-C',str(root),'rev-parse','HEAD','refs/heads/main']).decode().splitlines();require(len(values)==2 and values[0]==values[1],'main checkout preserved');heads[label]=values[0]
    protected={};absences=set(old['protected_absences']);phase_changes=[]
    for x in old['protected']:
        value=full(x['path'])
        if x['path']==str(PREVIOUS/'RESEARCH_LOG.md'):
            require(value['bytes']==8947 and value['mode']==420 and value['sha256']=='09f407460b2dd667f98b6d4c1b3aee2a77ab3504c9b5c6c27a9684c5343da13a','genuine postcompletion PR140 log')
            phase_changes.append({'historical_final_plan_pin':x,'current_postcompletion_pin':value,'reason':'ROOT appended actual100-percent after completed final readback; historical plan remains frozen'})
        else:require(value==x,'unrelated protected resource changed '+x['path'])
        protected[x['path']]=value
    for name in absences:require(not safe(name).exists(),'previous protected absence changed')
    def protect(p):
        value=full(p);require(value['path'] not in absences,'present/absent collision');protected[value['path']]=value
    for x in prior['installed_postimages3']+prior['installed_native_postimages23']:expect(x['path'],x);protect(x['path'])
    for role in ['source','plan','publish','install','root_readback','native_acceptance','actual_acceptance_inputs']:protect(prior[role]['path'])
    protect(prior_path)
    rows=[]
    for m in original['files']:
        path=A/'original_submitted_attempt'/m['path'];expect(path,{'bytes':m['bytes'],'mode':m['mode'],'sha256':m['sha256']});require(blob_oid(path,m)==m['Git_blob'],'original whole-body Git identity');protect(path)
        rows.append({'path':str(path.relative_to(C)),'origin':path,'archive':True})
    public=[
        'ORIGINAL_SUBMITTED_ATTEMPT_MANIFEST.json','ORIGINAL_PR_METADATA.json','ORIGINAL_INTAKE_READERS.json','ORIGINAL_ARCHIVE_READERS.json','ORIGINAL_TOP_LEVEL_CONTENTS.json',
        'RESEARCH_LOG.md','ROOT_EXACT_CLAIM_SOURCE_CHECK.json','ROOT_PRIMARY_SOURCE_RETRIEVAL.json','ROOT_MATHEMATICAL_GATE.json',
        'root_kernel_audit_20261007/ANALYTIC_REVIEW.md','root_kernel_audit_20261007/RESULT.json','root_kernel_audit_20261007/check_image_and_spectral_flux.py',
        'checkpoint_preparation_20261007/scoped_audit_checkpoint_publish.py','checkpoint_preparation_20261007/capture_readonly_audit_proposal.py','checkpoint_preparation_20261007/SOURCE_CUSTODY_AND_DELTA.json','checkpoint_preparation_20261007/SOURCE_DIFF_FROM_REVIEWED_SPARSE.patch','checkpoint_preparation_20261007/SCOPE_AND_REUSE.md','checkpoint_preparation_20261007/RESEARCH_LOG.md',
    ]
    for p in sorted((A/'guard_repaired_verifier_20261007').iterdir()):
        if p.is_file() and p.suffix.casefold() in ['.py','.md','.json']:public.append(str(p.relative_to(A)))
    closed=[]
    for folder,key in [('probability_model_adversary_20261007','files'),('transform_determinacy_adversary_20261007','members')]:
        mp=A/folder/'FINAL_MANIFEST.json';manifest=jsonread(mp);public.append(str(mp.relative_to(A)))
        for m in manifest[key]:
            p=Path(m['path']) if Path(m['path']).is_absolute() else A/folder/m['path'];expected={'bytes':m['size'],'mode':m['mode'],'sha256':m['sha256']};expect(p,expected)
            rel=p.relative_to(A);selected=not any(x.casefold().startswith('private') or x.casefold() in ['replay','cache','.git'] for x in rel.parts) and p.suffix.casefold() in ['.md','.json','.py','.jsonl']
            closed.append({'full_original_pin':full(p),'selected_for_minimal_public_checkpoint':selected})
            if selected:public.append(str(rel));protect(p)
    for rel in sorted(set(public)):rows.append({'path':str((A/rel).relative_to(C)),'origin':A/rel,'archive':False})
    for p in sorted((P/'ordered_intake_20261007/after_PR140').iterdir()):
        if p.is_file() and p.suffix.casefold() in ['.py','.json','.md']:rows.append({'path':str(p.relative_to(C)),'origin':p,'archive':False})
    for p in [prior_path,Path(prior['root_readback']['path']),PREVIOUS/'RESEARCH_LOG.md']:rows.append({'path':str(p.relative_to(C)),'origin':p,'archive':False})
    members=[];snapshots=[]
    for row in rows:
        path=safe(row['origin']);origin=full(path);source=path
        require(not any(x.casefold().startswith('private') or x.casefold() in ['cache','.git','replay'] for x in Path(row['path']).parts),'explicit nonprivate public scope')
        if not row['archive']:
            source=D/'private/public_payload'/row['path'];source.parent.mkdir(parents=True,exist_ok=True)
            require(not source.exists(),'distinct small dated snapshot');source.write_bytes(path.read_bytes());os.chmod(source,420);expect(path,origin)
            after=full(source);require(after['bytes']==origin['bytes'] and after['sha256']==origin['sha256'],'complete dated snapshot identity')
            snapshots.append({'publication_path':row['path'],'full_original_pin':origin,'dated0644_source_copy':after,'original_body_mode_not_modified':True})
        post=pin(source);require(post['mode']==420,'public0644 postimage');members.append({'path':row['path'],'source':str(source),'post':post,'install':False,'local_pre':None});protect(source)
    custody=D/'DATED_PUBLIC_SOURCE_CUSTODY.json'
    custody.write_text(json.dumps({'schema':'pr141-audit-checkpoint-dated-source-custody/v1','UTC':utc(),'actual_preparer_PID':os.getpid(),'snapshots':snapshots,'closed_peer_original_member_pins':closed,'original20_unchanged':True,'copyrighted_primary_material_and_working_controls_excluded':True,'mathematical_gate_final_PASS_priority_pending':True,'publication_or_operator_execution':False},indent=2,sort_keys=True)+'\n')
    members.append({'path':str(custody.relative_to(C)),'source':str(custody),'post':pin(custody),'install':False,'local_pre':None});protect(custody)
    require(len({m['path'].casefold() for m in members})==len(members),'exact casefold public inventory')
    dependencies={'draft_pr_publication_program_20260930/'+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
    needed=sorted(dependencies|{m['path'] for m in members});raw=git(['ls-tree','-r','-z',base,'--',*needed]);entries={}
    for record in raw.split(b'\0'):
        if not record:continue
        meta,path=record.split(b'\t',1);mode,kind,oid=meta.decode().split();name=path.decode();require(mode=='100644' and kind=='blob' and name not in entries,'immutable audit/dependency blob/mode')
        entries[name]={'Git_blob':oid,'tree_sha256':digest(record+b'\0')}
    ids=sorted({entries[n]['Git_blob'] for n in dependencies});raw=git(['cat-file','--batch'],('\n'.join(ids)+'\n').encode());pos=0;blobs={}
    for oid in ids:
        end=raw.index(b'\n',pos);fields=raw[pos:end].decode().split();require(fields[:2]==[oid,'blob'],'whole dependency frame');size=int(fields[2]);pos=end+1;body=raw[pos:pos+size];require(raw[pos+size:pos+size+1]==b'\n','whole dependency body');require(hashlib.sha1(('blob '+str(size)+'\0').encode()+body).hexdigest()==oid,'whole dependency Git hash');blobs[oid]={'bytes':size,'sha256':digest(body)};pos+=size+1
    require(pos==len(raw),'exact dependency batch coverage')
    remote_inputs=[{'path':name,**blobs[entries[name]['Git_blob']],'tree_sha256':entries[name]['tree_sha256']} for name in sorted(dependencies)]
    changed=[]
    for m in members:
        current=entries.get(m['path']);m['pre_tree_sha256']=current['tree_sha256'] if current else digest(b'');m['post_blob']=blob_oid(m['source'],m['post'])
        if current is None or current['Git_blob']!=m['post_blob']:changed.append(m['path'])
    require(run([GH,'api','--method','GET','repos/AlecKriebel/Math/git/ref/heads/main','--jq','.object.sha']).decode().strip()==base,'main advanced during capture')
    for x in protected.values():expect(x['path'],x)
    for path in absences:require(not safe(path).exists(),'protected absence changed during capture')
    plan={'schema':'pr141-audit-only-checkpoint-overlay/v1','scope':'PR141_AUDIT_ONLY_PROVISIONAL','UTC':utc(),'actual_preparer_PID':os.getpid(),'source_sha256':EXPECTED_SOURCE,'base_commit':base,'R_HEAD':heads['R'],'C_HEAD':heads['C'],'previous_PR134_original_head':old['previous_PR134_original_head'],'closing_comment_body_sha256':old['closing_comment_body_sha256'],'previous_PR140_merge':old['PR140_merge'],'previous_PR140_acceptance':full(prior_path),'original_PR141_head':original['head'],'original20_manifest':full(original_path),'mathematical_gate':full(A/'ROOT_MATHEMATICAL_GATE.json'),'mathematical_review_status':'ROOT_PASS_AFTER_TWO_INDEPENDENT_FINALS','priority_clearance':False,'case_publication_acceptance':False,'case_percent_at_scientific_gate':40,'goal_complete':False,'goal_active_per_ROOT_assignment':True,'no_new_central_proof_turns':0,'native_canonical_and_program3_paths_selected':False,'members':sorted(members,key=lambda m:m['path']),'expected_changed_paths':sorted(changed),'protected':sorted(protected.values(),key=lambda x:x['path']),'protected_absences':sorted(absences),'protected_remote_inputs':remote_inputs,'git_executable':pin(G),'gh_executable':pin(GH),'commit_message':'Checkpoint PR141 original custody and completed mathematical audits with priority pending','operator_action_executed':False,'operation_clearance':False,'independent_source_and_plan_review_pending':True,'dated_source_custody':full(custody),'protected_dated_postcompletion_phase_change':phase_changes}
    out=D/'AUDIT_CHECKPOINT_PROPOSAL.json';out.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n')
    receipt={'schema':'pr141-readonly-audit-checkpoint-proposal-preparation/v1','UTC':utc(),'actual_preparer_PID':os.getpid(),'source':full(SOURCE),'proposal':full(out),'source_custody':full(custody),'members':len(members),'changed_paths':len(changed),'install_count':0,'protected_count':len(protected),'protected_absence_count':len(absences),'full_current_main':base,'original20_preserved':True,'mathematical_PASS_priority_pending':True,'goal_incomplete':True,'children':children,'all_read_children_closed':all(x['reaped'] and x['group_absent'] and x['exit_code']==0 for x in children),'source_operator_import_or_writer_execution':False,'ref_index_config_native_backend_global_provider_changes':False,'independent_source_and_plan_review_pending':True}
    rp=D/'PROPOSAL_PREPARATION_RECEIPT.json';rp.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(json.dumps({'proposal':full(out),'receipt':full(rp),'source':full(SOURCE),'actual_PID':os.getpid(),'member_count':len(members),'changed_count':len(changed)}))
if __name__=='__main__':
    try:main()
    except BaseException as exc:
        fail=D/'private'/('FAILED_READONLY_CAPTURE_'+str(os.getpid())+'.json');fail.write_text(json.dumps({'UTC':utc(),'actual_PID':os.getpid(),'error_type':type(exc).__name__,'error':str(exc),'children':children,'operator_or_writer_execution':False},indent=2,sort_keys=True)+'\n');raise
