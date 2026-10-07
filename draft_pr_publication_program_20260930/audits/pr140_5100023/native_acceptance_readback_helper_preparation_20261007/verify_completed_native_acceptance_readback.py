"""ROOT-only full native readback and receipt capture; import-safe and uninvoked at preparation."""
from pathlib import Path, PurePosixPath
import datetime,hashlib,json,os,re,signal,stat,subprocess,sys,time
R = Path('/Users/alec/Documents/Math')
C = R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A = C/'draft_pr_publication_program_20260930/audits/pr140_5100023'
D = A/'native_publication_operator_preparation_20261007'
G = '/opt/homebrew/Cellar/git/2.38.2/bin/git'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
URL = 'https://github.com/AlecKriebel/Math.git'
AUDIT = ('draft_pr_publication_program_20260930/audits/pr140_5100023/',)
K, CODE = '5100023', 'AMR-050-0023'
ORIGINAL_HEAD = '9e908ae58b5ceee6a0825bbebd8acf565db55340'
REVIEW_HASH = '374cf32e1f1b5885551fe8b3a02d43c749e7b392715cc4eb0b4ac77f628a865b'
STATEMENT_HASH = '70a4186cf9778db261377679ae614deec32ed1c2e80e209f809fba637b4e4b89'
ORIGINAL_MANIFEST_SHA = '687a08ae8eba9789f65a8a4c64650b9de7ea2ac6a4b970710cc9a33b83ebb672'
R1_REVIEWED_MANIFEST_SHA = '0d4f2a1fe22d06a787712b60821d477b54880c63c3f5716307a7a2eb0cf4b00f'
ORIGINAL_AUTHOR_LOG_SHA = '4670501b285b8d577b53097a7fdb17cabc0abc7ba28a88f28a258e583da4ffb3'
ORIGINAL_QUEUE_ROW_SHA = '0976537e7836d8d1a7dac530af9d0cc5a66dcdba3b670ddb38942d38e8439114'
SHEET_ID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
ATTEMPT_PREFIX = 'unsolved_math_prioritization/attempts/5100023/'
BACKEND = ('assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','QUEUE.md')
CANONICAL_METADATA = ('assessment.json','HISTORICAL_DESK_ASSESSMENT.json','PUBLICATION_EVIDENCE.json','ACCEPTANCE_EVIDENCE.json','README.md','RESEARCH_LOG.md')
NATIVE = {'unsolved_math_prioritization/'+n for n in BACKEND}|{ATTEMPT_PREFIX+n for n in CANONICAL_METADATA}
ATTEMPT = {ATTEMPT_PREFIX+n for n in ('PROOF.md','verify.py','verification.json','SHA256SUMS','independent_review/independent_checks.py','independent_review/independent_results.json','independent_review/author_replay/PROOF.md','independent_review/author_replay/verify.py','independent_review/author_replay/verification.json')}
PROGRAM = {'draft_pr_publication_program_20260930/'+s for s in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
def require(ok, message):
    if not ok: raise RuntimeError(message)

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(body): return hashlib.sha256(body).hexdigest()

def safe(path):
    path = Path(path)
    require(path.is_absolute(), 'absolute path required')
    for p in [path, *path.parents]:
        require(not p.is_symlink(), 'symlink: '+str(p))
    return path

def pin(path):
    path = safe(path); fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        s=os.fstat(fd);require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'regular single-link file required')
        h=hashlib.sha256()
        while b:=os.read(fd,1048576):h.update(b)
        after=os.fstat(fd); named=path.lstat()
        signature=lambda z:(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns,z.st_mode,z.st_nlink)
        require(signature(s)==signature(after)==signature(named),'file changed during pin read')
        return {'bytes':s.st_size,'mode':stat.S_IMODE(s.st_mode),'sha256':h.hexdigest()}
    finally:os.close(fd)

def check(path, expected):
    require(pin(path) == {k:expected[k] for k in ['bytes','mode','sha256']}, 'pin mismatch: '+str(path))

def run(argv, journal, env=None, data=None, allowed=(0,)):
    e={'UTC_start':utc(),'argv':argv}; journal['children'].append(e)
    try:child = subprocess.Popen(argv,cwd=R,env=env,stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    except BaseException:
        # A constructor exception may occur after fork. No PID custody was
        # obtained here: retain the operation barrier and report uncertainty.
        e.update(UTC_end=utc(),child_started=None,child_reaped=False,process_group_empty=False,constructor_outcome_unresolved=True)
        raise
    e['PID']=child.pid
    out=b'';err=b''; failure=None
    try:out,err=child.communicate(data,timeout=45)
    except BaseException as exc:
        failure=exc;e['timed_out']=isinstance(exc,subprocess.TimeoutExpired)
    finally:
        try:os.killpg(child.pid,0);empty=False
        except ProcessLookupError:empty=True
        except OSError as exc:empty=False;e['group_probe_error']=str(exc)
        if child.returncode is None or not empty:
            try:os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            except OSError as exc:e['group_kill_error']=str(exc)
            if child.returncode is None:
                try:out,err=child.communicate(timeout=5)
                except BaseException as exc:e['reap_error']=type(exc).__name__
        until=time.monotonic()+1
        while True:
            try:os.killpg(child.pid,0);empty=False
            except ProcessLookupError:empty=True
            except OSError as exc:empty=False;e['group_probe_error']=str(exc)
            if empty or time.monotonic()>=until:break
            time.sleep(.05)
        e.update(UTC_end=utc(),exit_code=child.returncode,child_reaped=child.returncode is not None,process_group_empty=empty,stdout_bytes=len(out),stdout_sha256=digest(out),stderr_bytes=len(err),stderr_sha256=digest(err))
    if failure is not None:raise failure
    require(empty and not e.get('timed_out') and child.returncode in allowed,'child failed; see journal: '+argv[0])
    return out

def git(args,journal,index=None,data=None,allowed=(0,)):
    env=os.environ.copy()
    for k in list(env):
        if k.startswith('GIT_'): del env[k]
    env['GIT_OPTIONAL_LOCKS']='0'
    env['GIT_NO_REPLACE_OBJECTS']='1'
    if index is not None: env['GIT_INDEX_FILE']=str(index)
    return run([G,'-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','core.splitIndex=false',*args],journal,env,data,allowed)

def tree_oid(value):
    require(isinstance(value, str) and len(value)==40 and all(c in '0123456789abcdef' for c in value), 'invalid Git object ID')
    return value

def native_json(body):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result, 'duplicate JSON key');result[key]=value
        return result
    def bad(value):raise RuntimeError('nonfinite JSON constant')
    return json.loads(body,object_pairs_hook=pairs,parse_constant=bad)

def native_equal(a,b):
    return json.dumps(a,sort_keys=True,ensure_ascii=False,allow_nan=False)==json.dumps(b,sort_keys=True,ensure_ascii=False,allow_nan=False)

def actual_utc(value):
    require(isinstance(value,str), 'actual UTC string required')
    try:dt=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:raise RuntimeError('invalid actual UTC')
    require(dt.tzinfo is not None and dt.utcoffset()==datetime.timedelta(0), 'actual UTC offset required')
    return dt

def actual_doi(value):
    prefix='10.5281/zenodo.'
    require(isinstance(value,str) and value.startswith(prefix), 'actual Zenodo version DOI required')
    tail=value[len(prefix):]
    require(tail and tail[0]!='0' and all(c in '0123456789' for c in tail), 'invalid actual Zenodo version DOI')
    return value

def native_full_pin(spec):
    require(isinstance(spec,dict) and all(k in spec for k in ['path','bytes','mode','sha256']), 'complete actual input pin required')
    require(isinstance(spec['path'],str) and Path(spec['path']).is_absolute() and str(Path(spec['path']))==spec['path'] and '..' not in Path(spec['path']).parts, 'canonical absolute input path')
    require(type(spec['bytes']) is int and spec['bytes']>=0 and type(spec['mode']) is int and spec['mode'] in (292,420,493), 'actual pin byte/mode types')
    require(isinstance(spec['sha256'],str) and len(spec['sha256'])==64 and all(c in '0123456789abcdef' for c in spec['sha256']), 'actual pin SHA256')
    check(spec['path'],spec)

def original_archive(plan):
    spec=plan['original17_manifest']
    require(spec['path']==str(A/'ORIGINAL17_MANIFEST.json') and spec['sha256']==ORIGINAL_MANIFEST_SHA, 'frozen original17 manifest')
    native_full_pin(spec);manifest=native_json(Path(spec['path']).read_bytes())
    require(manifest['head']==ORIGINAL_HEAD and manifest['originals_captured']==17 and len(manifest['members'])==17, 'original17 manifest identity')
    required={}
    for m in manifest['members']:
        rel=m['relative'];require(isinstance(rel,str) and str(PurePosixPath(rel))==rel and not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts, 'original relative path')
        require(m['path']==ATTEMPT_PREFIX+rel and m['Git_mode']=='100644' and m['mode']==420, 'original path/mode')
        tree_oid(m['Git_blob']);path=str(A/'original'/rel)
        require(path not in required, 'duplicate original archive path')
        required[path]={k:m[k] for k in ['bytes','mode','sha256']}
    protected={x['path']:{k:x[k] for k in ['bytes','mode','sha256']} for x in plan['protected']}
    require(all(protected.get(p)==v for p,v in required.items()), 'all17 frozen archive bodies must be protected')
    return manifest

def native_protection_contract(plan):
    present={x['path'] for x in plan['protected']};absent=set(plan['protected_absences'])
    require(len(present)==len(plan['protected']) and len(absent)==len(plan['protected_absences']) and not present&absent, 'unique protected resources')
    required={str(root/'.git'/name) for root in (R,C) for name in ['index','config','HEAD','packed-refs','FETCH_HEAD','refs/heads/main','refs/remotes/origin/main','index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock']}
    required|={str(C/'unsolved_math_prioritization'/name) for name in ['queue.py','manifest.json','policy.json','cache/catalog.sqlite']}
    require(required<=present|absent, 'exact real Git and backend-presence baselines required')
    require(all(str(C/'unsolved_math_prioritization'/name) in absent for name in ['queue.py','manifest.json','policy.json','cache/catalog.sqlite']), 'intentional checkout backend/cache absences must stay absent')
    require(all(str(root/'.git'/name) in absent for root in (R,C) for name in ['index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock']), 'real Git writer locks must remain absent')
    installing={str(C/m['path']) for m in plan['members'] if m['install']}
    require(not installing&(present|absent), 'installed paths cannot be immutable protected resources')

def acceptance_inputs(plan):
    spec=plan['actual_acceptance_inputs']
    require(spec['path']==str(A/'ROOT_NATIVE_PUBLICATION_INPUTS_AUTHENTICATION_20261007.json'), 'fixed actual ROOT input attestation path')
    native_full_pin(spec);a=native_json(Path(spec['path']).read_bytes())
    require(a['schema']=='pr140-actual-native-publication-inputs/v1' and a['owner']=='ROOT' and a['fixture_only'] is False and type(a['actual_ROOT_PID']) is int and a['actual_ROOT_PID']>0, 'actual ROOT acceptance identity')
    actual_utc(a['UTC'])
    require(a['original_head']==ORIGINAL_HEAD and a['review_hash']==REVIEW_HASH and a['statement_hash']==STATEMENT_HASH and a['original_effort']=='2/5' and type(a['new_central_proof_search_turns']) is int and a['new_central_proof_search_turns']==0, 'accepted original source/effort')
    require(a['package_finally_reviewed_and_published'] is True and a['actual_tracker_row_verified'] is True and a['actual_original_head_merge_verified'] is True, 'actual package/publication/tracker/merge completion required')
    actual_doi(a['DOI']);native_full_pin(a['package_manifest_pin'])
    require(isinstance(a['package_member_pins'],list) and a['package_member_pins'], 'full accepted package member inventory')
    package_paths=[]
    for pin_spec in a['package_member_pins']:
        native_full_pin(pin_spec);package_paths.append(pin_spec['path'])
    require(len(package_paths)==len(set(package_paths)) and any(p.endswith('.pdf') for p in package_paths) and any(p.endswith('.zip') for p in package_paths), 'unique actual accepted PDF/support inventory')
    require(isinstance(a['roles'],dict) and set(a['roles'])=={'package','whole_package_R1','whole_package_R2','publication','tracker','merge'}, 'exact actual evidence roles')
    for role,pin_spec in a['roles'].items():native_full_pin(pin_spec)
    require(a['R1_reviewed_manifest_sha256']==R1_REVIEWED_MANIFEST_SHA and a['R2_final_reviewed_manifest_sha256']==a['package_manifest_pin']['sha256'], 'dated first review and final corrected package identity')
    relation_pin=a['review_relationship_pin'];native_full_pin(relation_pin)
    require(relation_pin['path']==str(A/'ROOT_ACTUAL_R1_FINAL_PACKAGE_REPAIR_RELATIONSHIP_20261007.json'), 'actual dated review relationship path')
    relation=native_json(Path(relation_pin['path']).read_bytes())
    require(relation['schema']=='pr140-actual-R1-to-final-package-repair-relationship/v1' and relation['owner']=='ROOT' and relation['fixture_only'] is False and type(relation['actual_ROOT_PID']) is int and relation['actual_ROOT_PID']>0, 'actual review relationship identity')
    actual_utc(relation['UTC'])
    require(relation['R1_reviewed_manifest_sha256']==a['R1_reviewed_manifest_sha256'] and relation['final_package_manifest_sha256']==a['R2_final_reviewed_manifest_sha256'] and relation['R1_result_pin']==a['roles']['whole_package_R1'] and relation['R2_result_pin']==a['roles']['whole_package_R2'] and relation['whole_package_clean_gate_pin']==a['roles']['package'], 'actual dated review/corrected-final/gate custody')
    require(relation['R1_mandatory_findings']==[] and relation['optional_bibliography_correction_applied'] is True and relation['TEX_exact_single_printed_title_substitution'] is True and relation['all_mathematical_proof_text_equations_assumptions_and_code_unchanged'] is True and relation['all_metadata_verification17_README_audit_summary_license_unchanged'] is True and relation['new_fresh_R2_review_of_final_package_is_PASS_with_no_findings'] is True and relation['R1_is_not_claimed_to_have_reviewed_final_changed_bytes'] is True and relation['repair_loop_fulfilled_by_dated_R1_then_repair_then_fresh_clean_final_R2'] is True, 'truthful preserved first review then repair then clean final review')
    comparison=relation['full29_member_comparison'];require(isinstance(comparison,list) and len(comparison)==29, 'full archived/final package comparison')
    seen=set();final_paths=set()
    for member in comparison:
        rel=member['relative'];require(isinstance(rel,str) and str(PurePosixPath(rel))==rel and not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts and rel not in seen, 'unique canonical compared package member')
        seen.add(rel);native_full_pin(member['R1']);native_full_pin(member['final_R2']);final_paths.add(member['final_R2']['path'])
        require(member['full_body_equal'] is (member['R1']['bytes']==member['final_R2']['bytes'] and member['R1']['sha256']==member['final_R2']['sha256']), 'full compared package body equality labels')
    require(final_paths==set(package_paths), 'actual final package inventory binds full review relationship')
    native_full_pin(a['raw_deposition_pin']);native_full_pin(a['actual_original17_local_materialization_pin'])
    require(a['intended_metadata_exactly_matches_all_supplied_provider_fields'] is True and set(a['provider_added_metadata_fields'])=={'doi','imprint_publisher','prereserve_doi'}, 'supplied metadata exactness with truthful provider additions')
    merge=plan['PR140_merge'];require(native_equal(merge,a['PR140_merge']), 'actual merge/plan binding')
    require(merge['original_head']==ORIGINAL_HEAD and merge['url']=='https://github.com/AlecKriebel/Math/pull/140' and merge['base_ref']=='main' and type(merge['draft']) is bool, 'actual merged PR identity')
    tree_oid(merge['commit']);actual_utc(merge['merged_at'])
    sheet=a['sheet'];require(sheet['spreadsheet_id']==SHEET_ID and sheet['gid']==1254632077 and sheet['title']=='Math Puzzles', 'actual tracker identity')
    require(isinstance(sheet['range'],str) and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",sheet['range']), 'actual four-cell tracker range')
    require(isinstance(sheet['values'],list) and len(sheet['values'])==4 and all(isinstance(x,str) for x in sheet['values']) and all(sheet['values'][i].strip() for i in [0,2,3]), 'actual tracker four-cell readback')
    require(sheet['values'][2] in [a['DOI'],'https://doi.org/'+a['DOI']] and K+' / '+CODE in sheet['values'][3], 'actual DOI/problem tracker cells')
    return a

HELPER_PREPARATION=A/'native_acceptance_readback_helper_preparation_20261007'
SOURCE=A/'native_publication_operator_preparation_20261007/successor_casefold_curation_v3/native_publication_operator_v3.py'
PLAN=A/'native_acceptance_candidate_plan_preparation_v2_20261007/NATIVE_ACCEPTANCE_CANDIDATE_PLAN.json'
COMBINED=A/'ROOT_NATIVE_PLAN_207_COMBINED_SOURCE_DATA_ACCEPTANCE_20261007.json'
SOURCE_SHA='adc52e0722e58a15ecfb7e6f92b4ea71657115478d72569ab9292253b1f89b75'
PLAN_SHA='8c3aeb57b8ce68111961e4e69098e9e6d915ae5214cc801910f92d1a159c2460'
COMBINED_SHA='e7e476d08acf7649bcef0c33983e83322037a5dfc130f256e4ccc7944c877e40'
PUBLISHED_COMMIT='0d5ae675f8a51e0eaead04d0bf20cdce3f182c8d'
PARENT='3eb0c843cf29502142370e066e8a23ef294c148d'
PUB_PATH=D/'private/actual_native_publish_01/RECEIPT.json'
INSTALL_PATH=D/'private/actual_native_install_03/RECEIPT.json'
PUBLICATION_RECEIPT_SHA='2fbaa99712516bed6e4fa8592034de0deff3e7c19c8f466dee7b62505e71adab'
INSTALLATION_RECEIPT_SHA='41785ff8359470bb810b2d0545c5a5c5346006de4a79d9eabf3f932d6e300451'
READBACK=A/'actual_native_root_readback_20261007/ROOT_READBACK.json'
ACCEPTANCE=A/'ROOT_NATIVE_PUBLICATION_INSTALLATION_ACCEPTANCE_20261007.json'
def full(path):return {'path':str(path),**pin(path)}
def frozen(path,sha):
    value=full(path);require(value['sha256']==sha,'frozen input SHA mismatch '+str(path));return value,native_json(Path(path).read_bytes())
def validate_operation_receipts(pub,ins):
    for receipt,action in [(pub,'publish'),(ins,'install')]:
        require(receipt['schema']=='pr140-native-publication-operation-receipt/v1' and receipt['transaction']=='native_acceptance' and receipt['action']==action,'genuine separate native operation roles')
        require(receipt['source_sha256']==SOURCE_SHA and receipt['plan_sha256']==PLAN_SHA and receipt['review_sha256']==COMBINED_SHA,'exact accepted source/plan/review operation binding')
        require(type(receipt['actual_PID']) is int and receipt['actual_PID']>0,'actual operation PID')
        actual_utc(receipt['UTC_start']);actual_utc(receipt['UTC_end'])
        require('error_type' not in receipt and 'error' not in receipt and receipt['own_operation_lock_released'] is True,'no failed operation relabeling or retained barrier')
        require(isinstance(receipt['children'],list) and receipt['children'],'actual operation child journal')
        for child in receipt['children']:
            require(type(child['PID']) is int and child['PID']>0 and type(child['exit_code']) is int and child['exit_code']==0 and child['child_reaped'] is True and child['process_group_empty'] is True,'all actual operation children exited/reaped/groups absent')
        require(receipt['published_commit']==PUBLISHED_COMMIT,'actual published native commit')
    require(pub['status']=='published_local_install_pending' and pub['public_full_body_readback'] is True and pub['whole_parent_tree_preserved_outside_exact_overlay'] is True,'completed native publication receipt')
    require(ins['status']=='public_and_local_install_verified' and ins['local_full_body_mode_readback'] is True and ins['private_cache_installed'] is False,'completed future successful installation receipt required')
def verify_local_and_custody(plan,journal):
    require(len(plan['protected'])==517 and len(plan['protected_absences'])==26,'exact accepted protected family')
    native_protection_contract(plan)
    for x in plan['protected']:check(x['path'],x)
    for x in plan['protected_absences']:require(not safe(x).exists(),'protected absence changed '+x)
    require(not safe(D/'private/OPERATION_LOCK.json').exists(),'native operation barrier still present')
    for root,expected in [(R,plan['R_HEAD']),(C,plan['C_HEAD'])]:
        got=git(['-C',str(root),'rev-parse','HEAD','refs/heads/main'],journal).decode().splitlines()
        require(got==[expected,expected],'real local HEAD/main changed')
    manifest=original_archive(plan)
    for member in manifest['members']:check(A/'original'/member['relative'],member)
    installed=[]
    for member in plan['members']:
        if member['install']:
            require(member['path'] in NATIVE|ATTEMPT,'unexpected installed scope')
            path=C/member['path'];check(path,member['post']);installed.append(full(path))
    require(len(installed)==23 and {str(C/p) for p in NATIVE}<={x['path'] for x in installed},'complete native14 and repair9 physical readbacks')
    current_selected={x['path'] for x in plan['members'] if x['install']}
    historical=[]
    for member in manifest['members']:
        if member['path'] not in current_selected:
            check(C/member['path'],member);historical.append(full(C/member['path']))
    require(len(historical)==6,'six unselected canonical original history files conserved')
    # Intentional repairs change9 plus README/log, while archive17 remains original.
    return installed,historical
def verify_services(plan,journal):
    custody=acceptance_inputs(plan)
    pr134=native_json(run([GH,'api','--method','GET','repos/AlecKriebel/Math/pulls/134'],journal))
    require(pr134['state']=='closed' and pr134['merged_at'] is None and pr134['draft'] is True and pr134['head']['sha']==plan['previous_PR134_original_head'],'PR134 disposition changed')
    comment=native_json(run([GH,'api','--method','GET','repos/AlecKriebel/Math/issues/comments/6028564660'],journal))
    require(digest(comment['body'].encode())==plan['closing_comment_body_sha256'],'PR134 closing comment changed')
    pr140=native_json(run([GH,'api','--method','GET','repos/AlecKriebel/Math/pulls/140'],journal));merge=plan['PR140_merge']
    require(pr140['state']=='closed' and pr140['merged'] is True and pr140['merged_at']==merge['merged_at'] and pr140['merge_commit_sha']==merge['commit'] and pr140['draft']==merge['draft'] and pr140['head']['sha']==ORIGINAL_HEAD and pr140['base']['ref']=='main','PR140 actual merge facts changed')
    return custody
def verify_public(plan,journal):
    require(len(plan['members'])==207 and len(plan['expected_changed_paths'])==206 and plan['base_commit']==PARENT,'exact reviewed public overlay')
    parent=git(['rev-list','--parents','-n','1',PUBLISHED_COMMIT],journal).decode().strip().split()
    require(parent==[PUBLISHED_COMMIT,PARENT],'actual published sole parent')
    changed=set(git(['diff','--no-ext-diff','--no-textconv','--no-renames','--name-only','-z',PARENT,PUBLISHED_COMMIT],journal).decode().split('\0'))-{''}
    require(changed==set(plan['expected_changed_paths']),'full parent tree complement/exact206 diff')
    paths=[m['path'] for m in plan['members']]
    require(len(paths)==len(set(paths)),'unique207 selection')
    raw=git(['ls-tree','-r','-z',PUBLISHED_COMMIT,'--',*paths],journal);entries={}
    for entry in raw.split(b'\0'):
        if not entry:continue
        meta,path=entry.split(b'\t',1);mode,kind,oid=meta.decode().split();name=path.decode()
        require(mode=='100644' and kind=='blob' and name not in entries,'published mode/blob/identity')
        tree_oid(oid);entries[name]=oid
    require(set(entries)==set(paths),'complete207 public tree modes')
    for member in plan['members']:require(entries[member['path']]==member['post_blob'],'published planned blob identity')
    ids=sorted(set(entries.values()));raw=git(['cat-file','--batch'],journal,data=('\n'.join(ids)+'\n').encode());view=memoryview(raw);pos=0;verified={}
    for oid in ids:
        end=raw.index(b'\n',pos);header=raw[pos:end].decode().split()
        require(len(header)==3 and header[:2]==[oid,'blob'],'full public blob frame')
        size=int(header[2]);require(size>=0,'blob size');pos=end+1
        require(pos+size<len(raw) and raw[pos+size:pos+size+1]==b'\n','full body framing')
        body=view[pos:pos+size];sha1=hashlib.sha1();sha1.update(('blob '+str(size)+'\0').encode());sha1.update(body)
        require(sha1.hexdigest()==oid,'full public Git blob hash')
        verified[oid]={'bytes':size,'mode':420,'sha256':hashlib.sha256(body).hexdigest()};pos+=size+1
    require(pos==len(raw),'full batch coverage')
    readbacks=[]
    for member in plan['members']:
        require(verified[entries[member['path']]]==member['post'],'full public body/size/mode pin')
        readbacks.append({'path':member['path'],'Git_blob':entries[member['path']],**verified[entries[member['path']]]})
    remote=run([GH,'api','--method','GET','repos/AlecKriebel/Math/git/ref/heads/main','--jq','.object.sha'],journal).decode().strip()
    require(remote==PUBLISHED_COMMIT,'current direct remote changed; fresh readback required')
    return readbacks,sorted(changed)
def write_once(path,value):
    path=safe(path);path.parent.mkdir(parents=True,exist_ok=True);safe(path.parent)
    require(not path.exists(),'completion/readback output already exists; never overwrite')
    body=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
    # Exclusive creation: an interrupted partial output is not a valid JSON receipt.
    with path.open('xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
    os.chmod(path,420);require(pin(path)=={'bytes':len(body),'mode':420,'sha256':digest(body)},'receipt full write readback')
def main():
    pub_arg,pub_sha,ins_arg,ins_sha=sys.argv[1:]
    require(str(safe(pub_arg))==str(PUB_PATH),'fixed actual native publication receipt')
    ins_path=safe(ins_arg);require(ins_path==INSTALL_PATH and pub_sha==PUBLICATION_RECEIPT_SHA and ins_sha==INSTALLATION_RECEIPT_SHA,'exact actual successful install03/publication01 receipt pins')
    source_pin,_source_unused=full(SOURCE),None
    require(source_pin['sha256']==SOURCE_SHA,'source bytes changed')
    plan_pin,plan=frozen(PLAN,PLAN_SHA);combined_pin,combined=frozen(COMBINED,COMBINED_SHA)
    require(combined['verdict']=='PASS' and combined['scope']=='PR140_actual_native_publication_source_and_data' and combined['actual_review'] is True and combined['actual_data_inputs_authenticated'] is True and combined['actual_DOI_tracker_merge_authenticated'] is True and combined['owner']=='ROOT' and combined['fixture_only'] is False and combined['source_sha256']==SOURCE_SHA and combined['plan_sha256']==PLAN_SHA,'genuine combined source/data acceptance')
    require(combined['source']==source_pin and combined['plan']==plan_pin,'full source/plan custody')
    pub_pin,pub=frozen(PUB_PATH,pub_sha);ins_pin,ins=frozen(ins_path,ins_sha)
    validate_operation_receipts(pub,ins)
    check(G,plan['git_executable']);check(GH,plan['gh_executable'])
    journal={'children':[]}
    installed,historical=verify_local_and_custody(plan,journal)
    custody=verify_services(plan,journal)
    public,changed=verify_public(plan,journal)
    # Recheck all current resources after the public/service reads.
    installed2,historical2=verify_local_and_custody(plan,journal)
    require(installed==installed2 and historical==historical2,'current native/history changed during readback')
    for path,value in [(SOURCE,source_pin),(PLAN,plan_pin),(COMBINED,combined_pin),(PUB_PATH,pub_pin),(ins_path,ins_pin)]:check(path,value)
    require(all(c['child_reaped'] is True and c['process_group_empty'] is True and c['exit_code']==0 for c in journal['children']),'all bounded reader children closed')
    readback={'schema':'pr140-root-native-public-local-full-readback/v1','UTC':utc(),'actual_ROOT_PID':os.getpid(),'owner':'ROOT','fixture_only':False,'source':source_pin,'plan':plan_pin,'combined_source_data_acceptance':combined_pin,'publish':pub_pin,'install':ins_pin,'published_commit':PUBLISHED_COMMIT,'sole_parent':PARENT,'exact_changed_paths':changed,'whole_parent_tree_complement_preserved':True,'public_member_count':207,'full_public_readbacks':public,'local_installed_count':23,'installed_postimages':installed,'historical_six_canonical_readbacks':historical,'original17_archive_preserved':True,'protected_count':517,'protected_absence_count':26,'R_C_refs_HEAD_indices_config_conserved':True,'private_cache_and_backend_absences_preserved':True,'actual_acceptance_inputs':plan['actual_acceptance_inputs'],'actual_DOI':custody['DOI'],'actual_tracker_range':custody['sheet']['range'],'children':journal['children'],'all_bounded_children_reaped_groups_absent':True,'actual_native_full_readbacks_complete':True,'program3_or_overall_goal_completion_claimed':False}
    write_once(READBACK,readback)
    acceptance={'schema':'pr140-root-native-installation-acceptance/v1','UTC':utc(),'actual_ROOT_PID':os.getpid(),'owner':'ROOT','fixture_only':False,'public_native_full_readback':True,'local_native_full_readback':True,'original17_archive_preserved':True,'private_cache_and_backend_absences_preserved':True,'actual_acceptance_inputs':plan['actual_acceptance_inputs'],'source':source_pin,'plan':plan_pin,'publish':pub_pin,'install':ins_pin,'root_readback':full(READBACK),'published_commit':PUBLISHED_COMMIT,'installed_postimages':installed,'combined_source_data_acceptance':combined_pin,'program3_or_overall_goal_completion_claimed':False}
    write_once(ACCEPTANCE,acceptance)
    print(json.dumps({'root_readback':full(READBACK),'native_acceptance':full(ACCEPTANCE),'actual_ROOT_PID':os.getpid(),'native_verification_complete':True,'global_completion_pending':True}))
if __name__=='__main__':main()
