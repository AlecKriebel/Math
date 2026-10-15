"""Independent read-only checkpoint authentication; never imports the operator."""
from pathlib import Path, PurePosixPath
import ast, datetime, difflib, hashlib, json, os, signal, stat, subprocess, time
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A=C/'draft_pr_publication_program_20260930/audits/pr141_30003818'
D=A/'checkpoint_preparation_20261007'
O=A/'checkpoint_source_plan_adversary_20261007'
G='/opt/homebrew/Cellar/git/2.38.2/bin/git'; GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def pin(p):
    p=Path(p);require(p.is_absolute(),'absolute file')
    for q in [p,*p.parents]:require(not q.is_symlink(),'symlink '+str(q))
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        s=os.fstat(fd);require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'regular single-link '+str(p))
        h=hashlib.sha256()
        while b:=os.read(fd,1048576):h.update(b)
        sig=lambda z:(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns,z.st_nlink)
        require(sig(s)==sig(os.fstat(fd))==sig(p.lstat()),'unstable '+str(p))
        return {'bytes':s.st_size,'mode':stat.S_IMODE(s.st_mode),'sha256':h.hexdigest()}
    finally:os.close(fd)
def check(p,x):require(pin(p)=={k:x[k] for k in ['bytes','mode','sha256']},'pin mismatch '+str(p))
children=[]
def run(args,data=None):
    e={'UTC_start':utc(),'argv':args};children.append(e)
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env.update(GIT_OPTIONAL_LOCKS='0',GIT_NO_REPLACE_OBJECTS='1')
    p=subprocess.Popen(args,cwd=R,env=env,stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);e['PID']=p.pid
    try:out,err=p.communicate(data,timeout=40)
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
    require(p.returncode==0 and empty,'read child failed')
    e.update(stdout_bytes=len(out),stdout_sha256=sha(out),stderr_bytes=len(err),stderr_sha256=sha(err));return out
def git(args,data=None):return run([G,'-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','core.splitIndex=false',*args],data)
def api(path):return json.loads(run([GH,'api','--method','GET',path]))
def readjson(p):return json.loads(Path(p).read_bytes())
def main():
    start=utc(); pp=D/'AUDIT_CHECKPOINT_PROPOSAL.json';sp=D/'scoped_audit_checkpoint_publish.py'
    require(pin(pp)=={'bytes':365510,'mode':420,'sha256':'9447a949312369dd24f38a78f310cba50ca23a680c5cd9ab5945ff92fb525feb'},'assigned plan')
    require(pin(sp)=={'bytes':21859,'mode':420,'sha256':'19ef8deeb6503256646af94edc69ad14d0715066e9008e68645b960f413ee431'},'assigned source')
    p=readjson(pp); source=sp.read_text();tree=ast.parse(source);compile(source,str(sp),'exec')
    delta=readjson(D/'SOURCE_CUSTODY_AND_DELTA.json');oldp=Path(delta['reviewed_sparse_source']['path']);check(oldp,delta['reviewed_sparse_source'])
    old=oldp.read_text(); oldtree=ast.parse(old)
    functions=lambda s,t:{n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,ast.FunctionDef)}
    f=functions(source,tree);g=functions(old,oldtree)
    same=sorted(k for k in f.keys()&g.keys() if f[k]==g[k]);changed=sorted(k for k in f.keys()&g.keys() if f[k]!=g[k]);removed=sorted(g.keys()-f.keys());added=sorted(f.keys()-g.keys())
    require(same==sorted(delta['byte_identical_functions']) and changed==sorted(delta['changed_functions']) and removed==delta['removed_functions'] and added==delta['new_functions'],'real function custody delta')
    expected=''.join(difflib.unified_diff(old.splitlines(True),source.splitlines(True),fromfile='accepted_PR140_sparse_source_9d5505',tofile='PR141_audit_only_source'))
    patch=(D/'SOURCE_DIFF_FROM_REVIEWED_SPARSE.patch').read_text();patch_equal=(expected==patch)
    oldresult=C/'draft_pr_publication_program_20260930/audits/pr140_5100023/sparse_tree_source_delta_adversary_20261007/RESULT.json'
    oldcombined=C/'draft_pr_publication_program_20260930/audits/pr140_5100023/scoped_active_checkpoint_20261007/COMBINED_ACTIVE_v3.json'
    oc=readjson(oldcombined);oe=[x for x in oc['evidence'] if x['path']==str(oldresult)][0]
    require(pin(oldresult)['bytes']==oe['bytes'] and pin(oldresult)['sha256']==oe['sha256'],'inherited source review pinned in ROOT combined acceptance')
    require(oc['verdict']=='PASS' and oc['source_sha256']==sha(oldp.read_bytes()) and readjson(oldresult)['verdict']=='PASS','inherited genuine source review')
    prior=p['previous_PR140_acceptance'];check(prior['path'],prior);a=readjson(prior['path'])
    require(a['status']=='ACCEPTED_COMPLETE' and a['owner']=='ROOT' and a['fixture_only'] is False and a['case_PR']==140 and a['case_percent']==100 and a['completed_count']==24 and a['published_count']==12 and a['overall_goal_complete'] is False,'actual prior completed authority')
    authority=[]
    for role in ['source','plan','publish','install','root_readback','native_acceptance','actual_acceptance_inputs','combined_source_data_acceptance']:
        x=a[role];check(x['path'],x);authority.append({'role':role,**x})
    pub=readjson(a['publish']['path']);inst=readjson(a['install']['path']);rr=readjson(a['root_readback']['path'])
    require(pub['status']=='published_local_install_pending' and pub['published_commit']==p['base_commit'] and pub['public_full_body_readback'] and pub['whole_parent_tree_preserved_outside_exact_overlay'],'prior actual publication')
    require(inst['status']=='public_and_local_install_verified' and inst['published_commit']==p['base_commit'] and inst['local_full_body_mode_readback'],'prior actual installation')
    for receipt in [pub,inst]:
        require(receipt['own_operation_lock_released'] is True and all(c['exit_code']==0 and c['child_reaped'] and c['process_group_empty'] for c in receipt['children']),'prior bounded children')
    protected=p['protected'];require(len({x['path'] for x in protected})==len(protected),'unique baseline')
    for x in protected:check(x['path'],x)
    for name in p['protected_absences']:
        q=Path(name)
        for z in [q,*q.parents]:require(not z.is_symlink(),'absent symlink')
        require(not q.exists(),'absence '+name)
    required={str(root/'.git'/n) for root in [R,C] for n in ['index','config','HEAD','packed-refs','FETCH_HEAD','refs/heads/main','refs/remotes/origin/main','index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock']}
    require(required<={x['path'] for x in protected}|set(p['protected_absences']),'real resource completeness')
    for root,k in [(R,'R_HEAD'),(C,'C_HEAD')]:require(git(['-C',str(root),'rev-parse','HEAD','refs/heads/main']).decode().splitlines()==[p[k],p[k]],'real HEAD main')
    require(api('repos/AlecKriebel/Math/git/ref/heads/main')['object']['sha']==p['base_commit'],'fresh exact remote main')
    pr134=api('repos/AlecKriebel/Math/pulls/134'); pr140=api('repos/AlecKriebel/Math/pulls/140');pr141=api('repos/AlecKriebel/Math/pulls/141');comment=api('repos/AlecKriebel/Math/issues/comments/6028564660')
    require(pr134['state']=='closed' and pr134['merged_at'] is None and pr134['draft'] and pr134['head']['sha']==p['previous_PR134_original_head'],'fresh previous disposition')
    require(sha(comment['body'].encode())==p['closing_comment_body_sha256'],'fresh closing body')
    require(pr140['merged'] and pr140['state']=='closed' and pr140['head']['sha']==p['previous_PR140_merge']['original_head'] and pr140['merge_commit_sha']==p['previous_PR140_merge']['commit'] and pr140['merged_at']==p['previous_PR140_merge']['merged_at'],'fresh previous accepted original merge')
    require(pr141['state']=='open' and pr141['draft'] and pr141['merged_at'] is None and pr141['head']['sha']==p['original_PR141_head'],'fresh current original intake')
    members=p['members'];require(len(members)==71 and len({m['path'].casefold() for m in members})==71,'exact member scope')
    member_evidence=[];bodies={}
    for m in members:
        check(m['source'],m['post']);b=Path(m['source']).read_bytes();bodies[m['path']]=b
        require(m['post_blob']==hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'post blob identity')
        path=PurePosixPath(m['path']);require(str(path)==m['path'] and not path.is_absolute() and '..' not in path.parts,'canonical public path')
        require(m['post']['mode']==420 and m['install'] is False and m['local_pre'] is None,'zero installs and normalized public mode')
        require(path.suffix in {'.json','.jsonl','.py','.md','.patch'} and not any(z.casefold().startswith('private') or z.casefold() in {'cache','.git','replay','working_controls'} for z in path.parts),'no primary exports/private/control paths')
        require(m['path'].startswith(('draft_pr_publication_program_20260930/audits/pr141_30003818/','draft_pr_publication_program_20260930/ordered_intake_20261007/after_PR140/')) or m['path'] in {'draft_pr_publication_program_20260930/audits/pr140_5100023/'+n for n in ['ROOT_FINAL_METADATA_ACCEPTANCE_20261007.json','RESEARCH_LOG.md','actual_final_metadata_root_readback_20261007/ROOT_READBACK.json']},'exact audit-only path')
        require(not b.startswith((b'%PDF-',b'\x89PNG',b'PK\x03\x04')) and b'JVBERi0' not in b and b'data:image/' not in b,'no raw exported primary media')
        if path.suffix=='.json':json.loads(b)
        member_evidence.append({'path':m['path'],'source':m['source'],'post':m['post'],'post_blob':m['post_blob']})
    custody=readjson(D/'DATED_PUBLIC_SOURCE_CUSTODY.json');check(p['dated_source_custody']['path'],p['dated_source_custody'])
    for s in custody['snapshots']:
        o=s['full_original_pin'];cp=s['dated0644_source_copy'];check(cp['path'],cp)
        require(o['bytes']==cp['bytes'] and o['sha256']==cp['sha256'] and cp['mode']==420,'snapshot complete body and mode mapping')
        require(s['original_body_mode_not_modified'] is True,'immutable snapshot declaration')
    for x in custody['closed_peer_original_member_pins']:check(x['full_original_pin']['path'],x['full_original_pin'])
    original=readjson(p['original20_manifest']['path']);require(len(original['files'])==20 and original['head']==p['original_PR141_head'],'original exact20')
    for m in original['files']:
        q=A/'original_submitted_attempt'/m['path'];check(q,m);b=q.read_bytes();require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==m['Git_blob'],'original full Git identity')
    gate=readjson(p['mathematical_gate']['path']);check(p['mathematical_gate']['path'],p['mathematical_gate'])
    require(gate['verdict']=='PASS_COMPLETE_EXPLICIT_TRANSFORM_LAW' and gate['case_percent']==40 and gate['submitted_effort']=='1/5' and gate['new_central_proof_turns']==0 and gate['mandatory_mathematical_corrections']==[] and not gate['overall_goal_complete'],'truthful mathematical gate')
    require(p['priority_clearance'] is False and p['case_publication_acceptance'] is False and p['goal_complete'] is False and p['native_canonical_and_program3_paths_selected'] is False and p['no_new_central_proof_turns']==0,'no promotion')
    need=sorted({m['path'] for m in members}|{x['path'] for x in p['protected_remote_inputs']})
    raw=git(['ls-tree','-r','-z',p['base_commit'],'--',*need]);entries={}
    for rec in raw.split(b'\0'):
        if rec:
            h,n=rec.split(b'\t',1);mode,kind,oid=h.decode().split();entries[n.decode()]={'raw':rec+b'\0','mode':mode,'kind':kind,'oid':oid}
    for m in members:require(sha(entries[m['path']]['raw'] if m['path'] in entries else b'')==m['pre_tree_sha256'],'full selective prior tree identity')
    changed_paths=sorted(m['path'] for m in members if m['path'] not in entries or entries[m['path']]['oid']!=m['post_blob'])
    require(changed_paths==p['expected_changed_paths'] and len(changed_paths)==71,'exact71 changed paths')
    for x in p['protected_remote_inputs']:
        e=entries[x['path']];require(e['mode']=='100644' and e['kind']=='blob' and sha(e['raw'])==x['tree_sha256'],'readonly remote tree')
        b=git(['show',p['base_commit']+':'+x['path']]);require(len(b)==x['bytes'] and sha(b)==x['sha256'],'readonly remote fullbody')
    for x in protected:check(x['path'],x)
    check(pp,{'bytes':365510,'mode':420,'sha256':'9447a949312369dd24f38a78f310cba50ca23a680c5cd9ab5945ff92fb525feb'})
    check(sp,{'bytes':21859,'mode':420,'sha256':'19ef8deeb6503256646af94edc69ad14d0715066e9008e68645b960f413ee431'})
    out={'schema':'pr141-independent-audit-checkpoint-readonly-authentication/v1','actual_reviewer_PID':os.getpid(),'UTC_start':start,'UTC_end':utc(),'source':{'path':str(sp),**pin(sp)},'plan':{'path':str(pp),**pin(pp)},'inherited_reviewed_source':delta['reviewed_sparse_source'],'same_functions':same,'changed_functions':changed,'removed_functions':removed,'new_functions':added,'patch_reproduces_final_exact_diff':patch_equal,'protected_count_full_body_mode_verified_twice':len(protected),'absence_count_verified':len(p['protected_absences']),'member_count_full_body_mode_verified':len(members),'changed_paths_verified':changed_paths,'members':member_evidence,'authority_input_pins':authority,'fresh_original_PR141_open_draft':True,'fresh_previous_PR140_merged_verified':True,'fresh_base_commit':p['base_commit'],'zero_installations':True,'original20_full_body_blob_mode_unchanged':True,'math_PASS40_priority_pending':True,'children':children,'all_read_children_reaped_groups_absent':all(z['exit_code']==0 and z['reaped'] and z['group_absent'] for z in children),'operator_import_or_execution':False,'writer_execution_or_native_global_ref_index_provider_actions':False}
    (O/'AUTHENTICATION.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'actual_PID':os.getpid(),'source_sha256':out['source']['sha256'],'plan_sha256':out['plan']['sha256'],'protected':len(protected),'members':len(members),'patch_exact':patch_equal,'children':len(children),'all_closed':out['all_read_children_reaped_groups_absent']}))
if __name__=='__main__':main()
