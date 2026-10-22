"""Prepared PR206 custody10 operations. Importing this file grants no authority.

Root alone injects authenticated c191/h190 modules and exact future adoption pins.
No project import, loader, transport installation, ref operation or CLI is present.
"""
from pathlib import Path
import base64, copy, datetime, hashlib, json, os, re, stat, sys, tempfile

D = Path(__file__).absolute().parent
A = D.parent
ROOT = A.parent.parent.parent
P = 'draft_pr_publication_program_20260930/'
CASE = P + 'audits/pr206_5100062/'
OWN = CASE + 'custody_checkpoint_02/'
COLLECTOR = 'original_custody_collector_01_20261016T174700Z/'
Q = 'unsolved_math_prioritization/QUEUE.md'
NATIVE = 'unsolved_math_prioritization/attempts/'
VIEWS = (CASE + 'CURRENT_CASE_STATUS.json', CASE + 'RESEARCH_LOG.md') + tuple(P + n for n in ('CURRENT_PROGRESS.json', 'CURRENT_PROGRESS.md', 'RESEARCH_LOG.md'))
SOURCE_ADOPTION = 'ROOT_CUSTODY_SOURCE_ADOPTION_01.json'
CUSTODY_ADOPTION = 'ROOT_ORIGINAL_CUSTODY_ADOPTION_01.json'
POINTER = CASE + 'ROOT_ACTUAL_CUSTODY_CHECKPOINT.json'
HEAD = '488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7'
HEAD_TREE = 'c67029118e3090c49c8601f6121fc0b93019e7ac'
HEAD_PARENT = '0a13fdb1f33dc1e6351b5d8ce7a55e36b5eedd00'
DECLARED = 'a7e588da5ac76913e00f979681f2dfff2d9a56be'
FORK = '5f672f535a9f76da203d99020263a83d5f2de5ce'
BASE_COMMIT = '08a17b535ca650d98cf3ec2439e2865b31111e2a'
BASE_TREE = '28ccd52bdfa41d70c9e744d6be373cb19fcbe0c9'
BASE_DIGEST = '27784963c9e2b2d0d4140a814fc054214f4d2e0dfc5ea465af1924a14d7b4f3e'
BASE_DIR = P + 'audits/pr205_5100030/publication_lifecycle_preparation_01/completion100_01/'
BASE_ACCEPT = {'bytes':2831,'sha256':'984c795664ff58b04c3c3d365de1e9f27fb9018bfc75066572d66e2c45745cb4'}
BASE_MAP = {'bytes':1311388,'sha256':'d0e98d12f64e509bde5e44af350681dc1d1c5000441c5fc43a1544d27066493c'}
BASE_ROOT_RECEIPT = {'bytes':1635,'sha256':'7cf4f90a8b194e775ba717e79335f1b3249ee89dbbfbee2df2e9cb84d5879278'}
BASE_POINTER = {'bytes':567,'sha256':'2054b0d8dc649b4a0d243402765f84f858c7b8d95c627c89f05767b8bc4c63e7'}
BASE_ROW = {'bytes':123,'sha256':'702a187848c9d2debcd519061ba1497a7e56688ef9106eddbc8c95bb2cc150ef'}
HEAD_ROW = {'bytes':511,'sha256':'7406859e7ca2b290833c8a59910f69140244ccf81bb975b254f1024ae246b4d9'}
INTAKE_PIN = {'bytes':3559,'sha256':'a45f1c025d3302a902037deb1a4dbb50a0ba11b2f16c646e402fe2cbbfcb6ac1'}
INVENTORY_PIN = {'bytes':7826,'sha256':'9ce95e0155ea64c1cec9f41fe6b4431a437fdfaae7ef45e146befc649720fb6e'}
SOURCE_FILES = frozenset(('custody206.py','offline_guards.py','CHECKPOINT_CONTRACT.md','ROOT_ADOPTION_INTERFACE.json','BASELINE_AUTHORITY.json','FROZEN_PREPARATION_PLAN.json','SOURCE_FORMAT_REFERENCES.json','OFFLINE_GUARDS_NORMAL.json','OFFLINE_GUARDS_OPTIMIZED.json','RESEARCH_LOG.md','ACCEPTANCE_BINDING_REPAIR.md'))
SOURCE_PUBLIC = SOURCE_FILES | {'SAFE_AUTHORED_MANIFEST.json','SOURCE_SEAL.json'}
EVIDENCE = frozenset(COLLECTOR + n for n in ('COMPACT_CUSTODY_PROPOSAL.json','ORIGINAL_SUBMISSION_CUSTODY_PROPOSAL.json','ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT_PROPOSAL.json','ORIGINAL_NATIVE_FILE_INVENTORY.json','EXACT_DAG_AND_RANGE_CLASSIFICATION.json','EXACT_SAFE_ORIGINAL_AUTHORED_ALLOWLIST.json','INDEPENDENT_BYTE_AND_RANGE_RECHECK.json','FROZEN_ACQUISITION_PLAN.json','ACQUISITION_PLAN_AMENDMENT_01.json','CUSTODY_SEAL.json'))
CANONICAL = frozenset(('ROOT_ORIGINAL_STATUS_ONLY_INTAKE_01.json','ORIGINAL_SUBMISSION_CUSTODY.json','ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json','ORIGINAL_PR_METADATA.json'))
COUNTS = {'fully_completed_count':48,'published_count':32,'last_completed_PR':205,'next_numeric_intake_cursor':206,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
STATUS = 'ORIGINAL_PR206_CUSTODY_RECORDED_SCIENTIFIC_GATES_UNCLEARED'
REMAIN = 'Root must independently assess exact source contract, mathematics, verification integrity and bounded priority/editorial/publication gates. Custody supplies zero accepted scientific or whole-package events; no PR207 intake.'
MAX_BYTES = 8 * 1024 * 1024
MAX_SELECTED = 10000
MAX_OVERLAY = 160
MAX_CHANGED = 20000
_backend = None
_authority_pin = None


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def pin(raw):
    need(type(raw) is bytes and len(raw) <= MAX_BYTES, 'Bounded byte buffer required')
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def bpin(raw):
    return {**pin(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def bytepin(value):
    need(type(value) is dict and set(value)=={'bytes','sha256'} and type(value['bytes']) is int and 0<=value['bytes']<=MAX_BYTES and type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}',value['sha256']) is not None,'Exact bounded byte pin')
    return value


def enc(value):
    return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def decode(raw):
    pin(raw)
    def pairs(items):
        result={}
        for key,value in items:
            need(key not in result,'Duplicate JSON key')
            result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:need(False,'Nonfinite JSON'))


def rel(value):
    need(type(value) is str and len(value)<=1024 and value and not value.startswith('/') and '\\' not in value and '\0' not in value and all(x not in ('','.','..') for x in value.split('/')),'Safe relative path')
    return value


def _path(relative):
    target=ROOT/rel(relative)
    current=ROOT
    need(stat.S_ISDIR(current.lstat().st_mode) and not current.is_symlink(),'Regular workspace root')
    for component in relative.split('/')[:-1]:
        current=current/component
        need(stat.S_ISDIR(current.lstat().st_mode) and not current.is_symlink(),'Regular parent directory')
    return target


def optional(relative, readonly=False):
    target=_path(relative)
    try:
        before=target.lstat()
    except FileNotFoundError:
        return None
    need(stat.S_ISREG(before.st_mode) and (not readonly or stat.S_IMODE(before.st_mode)==0o444),'Regular file/type/mode '+relative)
    fd=os.open(target,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        opened=os.fstat(fd)
        need(stat.S_ISREG(opened.st_mode) and (opened.st_dev,opened.st_ino)==(before.st_dev,before.st_ino) and opened.st_size<=MAX_BYTES,'Bounded unchanged file identity')
        with os.fdopen(fd,'rb',closefd=False) as stream:
            raw=stream.read(MAX_BYTES+1)
        pin(raw)
        after=target.lstat()
        need((after.st_dev,after.st_ino,after.st_size)==(opened.st_dev,opened.st_ino,len(raw)),'File identity changed during read')
        return raw
    finally:
        os.close(fd)


def read(relative, expected=None, readonly=True):
    raw=optional(relative,readonly)
    need(raw is not None,'Missing required file '+relative)
    if expected is not None:
        need(pin(raw)==bytepin(expected),'Exact file pin '+relative)
    return raw


def obj(relative, expected=None):
    return decode(read(relative,expected))


def _fsync_dir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)


def atomic(relative, raw, expected):
    """Per-file atomic replacement; caller first checks the complete five-file set."""
    need(relative.startswith(OWN) or relative in VIEWS or relative==POINTER,'Exact local output scope')
    pin(raw)
    target=_path(relative)
    prior=optional(relative)
    need((None if prior is None else pin(prior))==expected,'Stale local file preimage '+relative)
    fd,tmp=tempfile.mkstemp(prefix='.'+target.name+'.pr206_',dir=target.parent)
    try:
        with os.fdopen(fd,'wb') as stream:
            need(stream.write(raw)==len(raw),'Short local write')
            stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
        again=optional(relative)
        need((None if again is None else pin(again))==expected,'Local preimage changed after staging')
        os.replace(tmp,target);_fsync_dir(target.parent)
        need(read(relative)==raw,'Atomic file readback')
    finally:
        if os.path.lexists(tmp):os.unlink(tmp)


def save(relative, value):
    atomic(relative,enc(value),None)


def digest(selected):
    need(type(selected) is dict and 0<len(selected)<=MAX_SELECTED,'Bounded selected map')
    for path,value in selected.items():
        rel(path)
        need(type(value) is dict and set(value)=={'bytes','sha256','git_blob'},'Selected pin schema')
        bytepin({k:value[k] for k in ('bytes','sha256')})
        need(type(value['git_blob']) is str and re.fullmatch('[0-9a-f]{40}',value['git_blob']) is not None,'Selected native blob identity')
    return hashlib.sha256(json.dumps(selected,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def configure_backend(c,h):
    global _backend
    need(_backend is None,'Backend already configured; use a fresh Root dispatcher instance')
    need(all(callable(getattr(c,k,None)) for k in ('byte_pin','selected_digest','selected_current')) and all(callable(getattr(h,k,None)) for k in ('api','lookup','changed_leaves')),'Injected direct native interface')
    need(callable(getattr(getattr(h,'m',None),'verify_tree_object',None)) and type(getattr(h.m,'native_tree_cache',None)) is dict,'Injected native tree authentication interface')
    _backend=(c,h)


def configure_authority(expected_source_adoption):
    global _authority_pin
    need(_authority_pin is None,'Authority already configured; fresh dispatcher required')
    wanted=copy.deepcopy(bytepin(expected_source_adoption))
    authority(wanted)
    _authority_pin=wanted


def authority(expected=None):
    wanted=expected if expected is not None else _authority_pin
    need(wanted is not None,'Future exact actual Root source/custody adoption is mandatory and absent by default')
    source=obj(CASE+SOURCE_ADOPTION,wanted)
    need(source.get('schema')=='pr206-root-custody10-source-adoption-v1' and source.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and source.get('accepted_preparation_only') is True and source.get('PR')==206 and source.get('original_head')==HEAD,'Actual Root source adoption')
    need(source.get('external_dispatcher_owns_authenticated_direct8_adapter_and_all_alias_cache_cleanup') is True,'Root external backend ownership')
    manifest=obj(OWN+'SAFE_AUTHORED_MANIFEST.json',source['source_manifest'])
    need(set(manifest['files'])==SOURCE_FILES,'Exact helper source-artifact allowlist')
    for name,value in manifest['files'].items():read(OWN+name,bytepin(value))
    seal=obj(OWN+'SOURCE_SEAL.json',source['source_seal'])
    need(seal['safe_manifest']==source['source_manifest'],'Source manifest seal')
    adoption=obj(CASE+CUSTODY_ADOPTION,source['custody_adoption'])
    need(adoption.get('schema')=='pr206-root-original-custody-adoption-v1' and adoption.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and adoption.get('accepted') is True and adoption.get('PR')==206 and adoption.get('original_head')==HEAD,'Actual Root original custody adoption')
    required={'original_tree':HEAD_TREE,'original_sole_parent':HEAD_PARENT,'declared_PR_base':DECLARED,'authenticated_authored_range_base':FORK,'file_count':21,'total_native_bytes':55033,'literal_delta_leaves':61,'authored_delta_leaves':22,'excluded_inherited_foreign_leaves':39}
    need(all(adoption.get(k)==v for k,v in required.items()),'Adopted exact original DAG/custody extent')
    local=source['initial_local_case_views']
    need(set(local)==set(VIEWS[:2]) and local[VIEWS[0]] is None,'Explicit new CURRENT preimage')
    if local[VIEWS[1]] is not None:bytepin(local[VIEWS[1]])
    return source,adoption


def runtime():
    need(not sys.flags.optimize and sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.safe_path,'Production requires ordinary Python -E -S -B -P')
    auth=authority()
    need(_backend is not None,'No default backend; Root must inject c191/h190')
    return *_backend,auth


def validate_cache(h):
    need(len(h.m.native_tree_cache)<=MAX_CHANGED,'Bounded native tree cache')
    for oid,rows in h.m.native_tree_cache.items():h.m.verify_tree_object(oid,rows)


def api(h,endpoint,method='GET',body=None):
    need(method=='GET' or (method=='POST' and endpoint in ('git/trees','git/commits')),'Helper has no ref/PR/service mutation interface')
    if method=='GET':need(re.fullmatch(r'(git/ref/heads/main|git/commits/[0-9a-f]{40}|git/blobs/[0-9a-f]{40}|compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}|pulls/206)',endpoint) is not None,'Exact native read endpoint')
    return h.api(endpoint,method,body) if method!='GET' else h.api(endpoint)


def body(h,path,commit):
    tree=api(h,'git/commits/'+commit)['tree']['sha'];entry=h.lookup(tree,rel(path))
    if entry is None:return None
    need(entry[:2]==('100644','blob'),'Native regular text body '+path)
    response=api(h,'git/blobs/'+entry[2]);need(response['sha']==entry[2] and response['encoding']=='base64','Immutable blob response')
    need(type(response['content']) is str and len(response['content'])<=2*MAX_BYTES,'Bounded native blob encoding')
    raw=base64.b64decode(''.join(response['content'].splitlines()),validate=True)
    need(len(raw)==response['size'] and bpin(raw)['git_blob']==entry[2],'Native blob header/size/hash')
    return raw


def baseline():
    receipt=obj(BASE_DIR+'ACCEPTANCE.json',BASE_ACCEPT)
    mapping=obj(BASE_DIR+'ACCEPTANCE_CURRENT_SELECTED_MAP.json',BASE_MAP)
    root=obj(P+'audits/pr205_5100030/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json',BASE_ROOT_RECEIPT)
    obj(P+'audits/pr205_5100030/ROOT_ACTUAL_COMPLETION_CHECKPOINT.json',BASE_POINTER)
    need(receipt['accepted'] is True and receipt['completion_metadata_accepted'] is True and receipt['every_selected_identity_checked_at_actual_observed_MAIN'] is True and receipt['full_scope_MAIN_accepted'] is True,'Actual205 completion authority')
    need(receipt['checkpoint_commit']==receipt['main_observed']==BASE_COMMIT and receipt['actual_tree']==BASE_TREE and receipt['actual_current_map_file']==BASE_MAP,'Exact actual205 checkpoint')
    selected=mapping['selected_files'];need(len(selected)==4363 and digest(selected)==mapping['selected_map_sha256']==receipt['actual_current_selected_map_sha256']==BASE_DIGEST,'All4363 inherited identities')
    for record in (receipt,root):
        need(tuple(record[k] for k in ('fully_completed_count','published_count','last_completed_PR','next_numeric_intake_cursor'))==(48,32,205,206),'Actual205 counts')
    return {'commit':BASE_COMMIT,'tree':BASE_TREE,'selected_files':selected}


def originals(auth):
    source,adoption=auth
    inventory=obj(CASE+COLLECTOR+'ORIGINAL_NATIVE_FILE_INVENTORY.json',INVENTORY_PIN)
    files=inventory['files'];need(len(files)==21 and sum(v['bytes'] for v in files.values())==55033,'Exact21 original leaves')
    required=EVIDENCE|CANONICAL|{'original_submitted_head/'+rel(n) for n in files}
    material=adoption['material'];need(set(material)==required,'Exact public custody material allowlist')
    raw={name:read(CASE+name,bytepin(value)) for name,value in material.items()}
    need(pin(raw['ROOT_ORIGINAL_STATUS_ONLY_INTAKE_01.json'])==INTAKE_PIN,'Original Root status-only intake pin')
    for name,entry in files.items():
        need(bpin(raw['original_submitted_head/'+name])=={k:entry[k] for k in ('bytes','sha256','git_blob')},'Original blob identity '+name)
    custody=decode(raw['ORIGINAL_SUBMISSION_CUSTODY.json']);queue=decode(raw['ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json'])
    need(custody['original_head']==queue['original_head']==HEAD and custody['original_tree']==HEAD_TREE and custody['original_sole_parent']==HEAD_PARENT and custody['file_count']==21 and custody['total_native_bytes']==55033,'Canonical exact original custody')
    need(custody['declared_PR_base']==DECLARED and custody['authenticated_authored_range_base']==FORK,'Canonical range distinction')
    need(queue['HEAD_status']=='claimed_solved' and queue['HEAD_effort']=='1/5' and queue['BASE_status']=='queued' and queue['BASE_effort']=='0/5','HEAD eligibility distinct from BASE')
    need(pin(queue['base_own_row']['text'].encode())==BASE_ROW and pin(queue['original_QUEUE_row']['text'].encode())==HEAD_ROW,'Exact BASE123/HEAD511 rows')
    need(custody.get('mathematical_clearance') is False and custody.get('priority_clearance') is False,'Custody carries no scientific clearance')
    return raw,files


def unchanged_pr(h,raw):
    original=decode(raw['ORIGINAL_PR_METADATA.json']);current=api(h,'pulls/206')
    need(current['head']['sha']==HEAD and current['head']['ref']=='dot/math-5100062' and current['base']['ref']=='main','Original PR206 HEAD/branch')
    for key in ('title','body','state','draft','merged','created_at','updated_at','commits','changed_files'):
        need(current[key]==original[key],'Original PR206 metadata drift '+key)
    need(current['state']=='open' and current['draft'] is True and current['merged'] is False,'Original open draft unchanged')


def reconcile_rows(old,new,selected):
    need(type(old) is bytes and type(new) is bytes,'Native QUEUE byte bodies')
    pin(old);pin(new)
    before,after=old.splitlines(keepends=True),new.splitlines(keepends=True)
    need(len(before)==len(after),'QUEUE line-count drift')
    protected={p.split('/')[2] for p in selected if p.startswith(NATIVE)}|{'5100062'}
    def identity(row):
        cells=row.decode().split('|')
        need(len(cells)==14 and cells[1].strip().isdigit(),'Changed QUEUE row shape')
        code=cells[2].strip().split(' / ')
        need(len(code)==2 and code[0].isdigit(),'Changed QUEUE target identity')
        return code[0]
    changes=[]
    for index,(a,b) in enumerate(zip(before,after)):
        if a==b:continue
        pid=identity(a);need(identity(b)==pid and pid not in protected,'Own or protected native QUEUE change')
        changes.append({'one_based_line':index+1,'problem_id':pid,'before':bpin(a),'after':bpin(b)})
    marker=b'| 5100062 / AMR-050-0062 |'
    a=[row for row in before if marker in row];b=[row for row in after if marker in row]
    need(len(a)==len(b)==1 and a==b and pin(b[0])==BASE_ROW,'Own MAIN row must remain exact BASE123 queued0/5, never HEAD511')
    return changes


def reconcile(c,h,base,parent,stamp):
    old,new=body(h,Q,base['commit']),body(h,Q,parent)
    need(bpin(old)==base['selected_files'][Q],'Prior accepted QUEUE native pin')
    changes=reconcile_rows(old,new,base['selected_files'])
    return {**base['selected_files'],Q:bpin(new)},{'UTC':stamp,'baseline_actual_commit':base['commit'],'observed_MAIN':parent,'old_QUEUE':bpin(old),'current_QUEUE':bpin(new),'foreign_unprotected_row_changes':changes,'own_BASE123_and_all_protected_QUEUE_bytes_unchanged':True,'custody_writes_no_QUEUE':True}


def project(prior,stamp):
    p=copy.deepcopy(prior)
    need(tuple(p[k] for k in ('current_PR','current_PR_workflow_percent','fully_completed_count','published_count','last_completed_PR','next_numeric_intake_cursor'))==(205,100,48,32,205,206),'Prior actual205 completion progress')
    retire={k:p[k] for k in p if k.lower().startswith(('current_','next_','conditional_','program_snapshot_')) or k in ('advance_to_next_PR_authorized_now','remaining_current_step','next_step','latest_ordered_intake_record','latest_ordered_intake_records')}
    p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':205,'actual_completion_commit':BASE_COMMIT,'actual_completion_receipt_pin':BASE_ACCEPT,'values':retire})
    for key in retire:del p[key]
    case={'UTC':stamp,'PR':206,'problem_id':5100062,'original_head':HEAD,'original_tree':HEAD_TREE,'declared_PR_base':DECLARED,'authenticated_authored_range_base':FORK,'original_QUEUE_status':'claimed_solved','original_QUEUE_effort_cell':'1/5','original_author_effort_unverified':True,'original_author_commit_count':4,'original_archive_files':21,'original_native_bytes':55033,'literal_declared_BASE_delta_leaves':61,'authored_delta_leaves':22,'excluded_inherited_foreign_delta_leaves':39,'status':STATUS,'case_percent':10,'source_contract_clearance':False,'mathematical_clearance':False,'mathematical_result_valid':None,'priority_clearance':False,'publication_ready':False,'theorem_accepted':False,'completed':False,'NEW_whole_package_reviews_completed':0,'whole_package_review_events':[],'DOI':None,'record_id':None,'tracker_range':None,'current_new_publication_ledger':[],'remaining_required_steps':REMAIN,**COUNTS}
    live={k:v for k,v in case.items() if k not in ('UTC','PR','case_percent') and k not in COUNTS}
    p.update({'current_'+k:v for k,v in live.items()})
    p.update(UTC=stamp,updated_UTC=stamp,current_PR=206,current_problem_id=5100062,current_status=STATUS,current_original_head=HEAD,current_original_PR_state='open',current_original_PR_open_draft=True,current_original_PR_merged=False,current_closed=False,current_closed_without_merge=False,current_completed=False,current_PR_workflow_percent=10,current_workflow_estimate_percent=10,current_record='audits/pr206_5100062/CURRENT_CASE_STATUS.json',latest_ordered_intake_record='audits/pr206_5100062/ROOT_ORIGINAL_STATUS_ONLY_INTAKE_01.json',remaining_current_step=REMAIN,next_step=REMAIN,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=206,next_status_only_intake_performed=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_whole_package_review_loop_complete=False,current_publication_package_reviews_complete=False,current_package_prepared=False,current_publication_package=None,current_publication_package_seal=None,current_whole_package_review_events=[],current_publication_gate=None,current_bounded_priority_audit_complete=False,current_priority_audit_complete=False,current_priority_novelty_clearance=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_literal_simultaneity_established=False,current_actual_publication_verified=False,current_actual_tracker_row_verified=False,current_actual_merge_accepted=False,current_actual_factual_checkpoint_accepted=False,current_Zenodo_published=False,current_tracker_updated=False,current_paper_prepared=False,current_deposit_prepared=False,current_new_publication_ledger=[],current_editorial_manuscript_preparation_authorized=False,current_mathematics_cleared=False,current_priority_novelty_clearance_scope=None,current_priority_clearance_scope=None,current_exact_claim=None,current_credit_and_limits=None,program_snapshot_semantics='PR206 custody10 only; authenticated21originalfiles/55033bytes, authored22leaves; exclude39inherited foreign differences. No scientific or publication clearance;48completed32published,last205,cursor206,advancefalse.',program_snapshot_authority_condition='Effective only after own actual full-scope MAIN acceptance. Custody supplies no mathematical/source/priority/publication gate.',**COUNTS)
    return case,p


def local_preimages(h,parent,auth):
    initial=auth[0]['initial_local_case_views'];result={}
    for path in VIEWS:
        remote=body(h,path,parent);local=optional(path)
        if path in VIEWS[:2]:
            need(remote is None,'New case remote view must be absent')
            wanted=initial[path]
            need((None if local is None else pin(local))==wanted,'Explicit new-case local preimage '+path)
        else:need(type(remote) is bytes and local==remote,'Global three must match fresh MAIN preimages')
        result[path]=None if local is None else pin(local)
    return result


def overlay(h,parent,stamp,auth,material,preimages,initial_log):
    out={CASE+name:raw for name,raw in material.items()}
    for name in SOURCE_PUBLIC:out[OWN+name]=read(OWN+name)
    for name in (SOURCE_ADOPTION,CUSTODY_ADOPTION):out[CASE+name]=read(CASE+name)
    case,progress=project(decode(body(h,P+'CURRENT_PROGRESS.json',parent)),stamp)
    out[VIEWS[0]]=enc(case);out[P+'CURRENT_PROGRESS.json']=enc(progress)
    log=initial_log;need((None if log is None else pin(log))==preimages[VIEWS[1]],'Root own-log frozen preimage')
    note=('\n'+stamp+' — PR206 custody10:21 original leaves/55033bytes; authored22leaf scope;39inherited foreign differences excluded. Original claimed_solved1/5 is eligibility only; own MAIN BASE123 row unchanged. No source/math/priority/publication clearance;0whole-package events;48completed32published,last205,cursor206,advancefalse. '+REMAIN+'\n').encode()
    out[VIEWS[1]]=(log or b'# PR206 custody\n')+note
    for path in VIEWS[3:]:out[path]=body(h,path,parent)+note
    need(len(out)<=MAX_OVERLAY and Q not in out and not any(k.startswith(NATIVE) for k in out),'Bounded custody-only overlay')
    return out


def expected_map(inherited,out):
    need(0<len(out)<=MAX_OVERLAY,'Bounded exact overlay')
    for path,raw in out.items():
        need(path in VIEWS or path.startswith(CASE),'Overlay scope')
        if path in inherited and path not in VIEWS:need(bpin(raw)==inherited[path],'Inherited selected overwrite '+path)
    result={**inherited,**{path:bpin(raw) for path,raw in out.items()}}
    digest(result)
    return result


def message(selected_digest):
    return 'PR206 custody10: exact original bytes and distinct authored/declared ranges\n\nNo QUEUE/native attempt/PR change. Source/math/priority/publication NOT CLEARED.48completed32published,last205,cursor206,advancefalse.\nSelected-map SHA256: '+selected_digest


def generation(name):
    need(type(name) is str and re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Fresh safe generation name')
    return OWN+name+'/'


def _context(name):
    c,h,auth=runtime();material,_=originals(auth);base=baseline();return c,h,auth,material,base,generation(name)


def _candidate(c,h,auth,material,base,g,r):
    need(r['schema']=='pr206-custody10-preparation-v1' and r['PR']==206 and r['case_percent']==10 and r['original_head']==HEAD,'Prepared identity')
    need(api(h,'compare/'+BASE_COMMIT+'...'+r['expected_main'])['status'] in ('identical','ahead'),'Candidate true parent lacks actual205 baseline')
    inherited,ack=reconcile(c,h,base,r['expected_main'],r['UTC'])
    need(ack==obj(g+'FOREIGN_QUEUE_RECONCILIATION.json'),'Exact generation foreign QUEUE acknowledgement')
    log_record=obj(g+'INITIAL_OWN_LOG_PREIMAGE.json')
    initial_log=None if log_record['text'] is None else log_record['text'].encode()
    need((None if initial_log is None else pin(initial_log))==auth[0]['initial_local_case_views'][VIEWS[1]],'Adopted initial own-log bytes')
    need(set(r['local_five_expected_preimages'])==set(VIEWS) and all(r['local_five_expected_preimages'][path]==auth[0]['initial_local_case_views'][path] for path in VIEWS[:2]),'Exact five prepared preimage bindings')
    for path in VIEWS[2:]:need(r['local_five_expected_preimages'][path]==pin(body(h,path,r['expected_main'])),'Exact fresh-parent global preimage binding')
    for path in VIEWS[:2]:need(body(h,path,r['expected_main']) is None,'New-case original parent views absent')
    out=overlay(h,r['expected_main'],r['UTC'],auth,material,r['local_five_expected_preimages'],initial_log)
    out[g+'FOREIGN_QUEUE_RECONCILIATION.json']=read(g+'FOREIGN_QUEUE_RECONCILIATION.json')
    expected=expected_map(inherited,out)
    need(r['selected_files']==expected and r['selected_map_sha256']==digest(expected)==c.selected_digest(expected) and r['overlay_paths']==sorted(out),'Every selected expected identity and overlay scope')
    co=api(h,'git/commits/'+r['commit'])
    parent_tree=api(h,'git/commits/'+r['expected_main'])['tree']['sha']
    need(c.selected_current(h,r['commit'],expected,parent_tree)==r['tree'],'Every selected candidate identity')
    changes={path for path,value in expected.items() if h.lookup(parent_tree,path)!=('100644','blob',value['git_blob'])}
    actual=h.changed_leaves(parent_tree,r['tree'])
    check_candidate_identity(r,co,parent_tree,expected,changes,actual,out)
    need(all(bpin(raw)==expected[path] for path,raw in out.items()),'Every overlay byte identity')
    validate_cache(h);unchanged_pr(h,material)
    return out,expected


def check_candidate_identity(r,co,parent_tree,expected,changes,actual,out):
    need(co['sha']==r['commit'] and [x['sha'] for x in co['parents']]==[r['expected_main']] and co['tree']['sha']==r['tree'] and co['message']==message(digest(expected)),'Exact sole fresh-MAIN parent/tree/message')
    need(parent_tree==r['parent_tree'],'Native parent tree')
    need(type(actual) is set and len(actual)<=MAX_CHANGED and changes==actual and r['changed_paths']==sorted(changes) and changes<=set(out),'Full changed-leaf foreign-tree preservation')
    need(Q not in changes and not any(path.startswith(NATIVE) for path in changes),'No QUEUE/native attempt change')


def prepare(name):
    c,h,auth,material,base,g=_context(name)
    need(not os.path.lexists(ROOT/g),'Fresh generation required')
    parent=api(h,'git/ref/heads/main')['object']['sha'];need(api(h,'compare/'+BASE_COMMIT+'...'+parent)['status'] in ('identical','ahead'),'Fresh MAIN ancestry from actual205')
    stamp=now();inherited,ack=reconcile(c,h,base,parent,stamp)
    parent_tree=c.selected_current(h,parent,inherited,BASE_TREE);validate_cache(h);unchanged_pr(h,material)
    pre=local_preimages(h,parent,auth);initial_log=optional(VIEWS[1]);out=overlay(h,parent,stamp,auth,material,pre,initial_log)
    need(api(h,'git/ref/heads/main')['object']['sha']==parent,'Stale MAIN lease; fresh generation required')
    target=_path(g.rstrip('/'));target.mkdir();_fsync_dir(target.parent)
    save(g+'INITIAL_OWN_LOG_PREIMAGE.json',{'text':None if initial_log is None else initial_log.decode(),'pin':None if initial_log is None else pin(initial_log)})
    save(g+'FOREIGN_QUEUE_RECONCILIATION.json',ack);out[g+'FOREIGN_QUEUE_RECONCILIATION.json']=read(g+'FOREIGN_QUEUE_RECONCILIATION.json')
    expected=expected_map(inherited,out)
    entries=[{'path':path,'mode':'100644','type':'blob','content':raw.decode('utf-8')} for path,raw in sorted(out.items())]
    tree=api(h,'git/trees','POST',{'base_tree':parent_tree,'tree':entries})['sha']
    need(api(h,'git/ref/heads/main')['object']['sha']==parent,'Stale lease after tree; abandon generation')
    commit=api(h,'git/commits','POST',{'tree':tree,'parents':[parent],'message':message(digest(expected))})['sha']
    r={'schema':'pr206-custody10-preparation-v1','UTC':stamp,'PR':206,'case_percent':10,'original_head':HEAD,'expected_main':parent,'parent_tree':parent_tree,'tree':tree,'commit':commit,'selected_files':expected,'selected_map_sha256':digest(expected),'overlay_paths':sorted(out),'changed_paths':sorted(path for path,value in expected.items() if h.lookup(parent_tree,path)!=('100644','blob',value['git_blob'])),'local_five_expected_preimages':pre,'Root_source_adoption_pin':copy.deepcopy(_authority_pin),'Root_custody_adoption_pin':auth[0]['custody_adoption'],'MAIN_moved':False,**COUNTS}
    save(g+'PREPARATION.json',r);_candidate(c,h,auth,material,base,g,r)
    need(api(h,'git/ref/heads/main')['object']['sha']==parent,'Stale lease after candidate verification; fresh generation required')
    save(g+'ROOT_PRE_MOVE_VERIFICATION.json',{'UTC':now(),'PR':206,'commit':commit,'expected_main':parent,'observed_MAIN':parent,'exact_single_trueparent_fullforeignscope_everyselectedidentity_verified':True,'actual_MAIN_acceptance':False})
    return {'expected_main':parent,'commit':commit,'tree':tree,'selected_files':len(expected),'selected_map_sha256':digest(expected),'no_ref_mutation':True}


def _prepared_context(name):
    c,h,auth,material,base,g=_context(name);r=obj(g+'PREPARATION.json')
    need(r['Root_source_adoption_pin']==_authority_pin and r['Root_custody_adoption_pin']==auth[0]['custody_adoption'],'Generation exact Root authority bindings')
    out,expected=_candidate(c,h,auth,material,base,g,r)
    return c,h,auth,material,base,g,r,out,expected


def verify(name):
    c,h,auth,material,base,g,r,out,expected=_prepared_context(name)
    need(api(h,'git/ref/heads/main')['object']['sha']==r['expected_main'],'Stale MAIN lease; fresh generation required')
    need(local_preimages(h,r['expected_main'],auth)==r['local_five_expected_preimages'],'All-five local preimages before external CAS')
    return {'verified':True,'expected_main':r['expected_main'],'commit':r['commit'],'tree':r['tree'],'no_ref_mutation':True}


def _actual(c,h,material,r,expected,base_commit,base_tree):
    main=api(h,'git/ref/heads/main')['object']['sha']
    need(api(h,'compare/'+r['commit']+'...'+main)['status'] in ('identical','ahead'),'Own checkpoint not in actual MAIN')
    need(api(h,'compare/'+base_commit+'...'+main)['status'] in ('identical','ahead'),'Actual MAIN must retain the authenticated receipt baseline')
    current,ack=reconcile(c,h,{'commit':base_commit,'tree':base_tree,'selected_files':expected},main,now())
    tree=c.selected_current(h,main,current,base_tree);validate_cache(h);unchanged_pr(h,material)
    need(api(h,'git/ref/heads/main')['object']['sha']==main,'MAIN advanced during actual full-scope checks; retry validation')
    return main,tree,current,ack


def accept(name):
    c,h,auth,material,base,g,r,out,expected=_prepared_context(name)
    main,tree,current,ack=_actual(c,h,material,r,expected,r['commit'],r['tree'])
    mapping={'selected_files':current,'selected_map_sha256':digest(current),'foreign_QUEUE_reconciliation_after_checkpoint':ack};raw=enc(mapping)
    atomic(g+'ACCEPTANCE_CURRENT_SELECTED_MAP.json',raw,None)
    receipt={'schema':'pr206-actual-custody10-acceptance-v2','evidence_scope':'ACTUAL_HELPER_NATIVE_RECHECK','UTC':now(),'PR':206,'accepted':True,'case_percent':10,'checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'original_head':HEAD,'selected_files':len(current),'actual_current_selected_map_sha256':digest(current),'actual_current_map_file':pin(raw),'every_selected_identity_checked_at_actual_observed_MAIN':True,'full_foreign_tree_scope_preserved':True,'all_overlay_body_identities_verified':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':False,'source_contract_clearance':False,'priority_clearance':False,'publication_ready':False,'NEW_whole_package_reviews_completed':0,**COUNTS}
    save(g+'ACCEPTANCE.json',receipt);return receipt


def _accepted_context(name):
    c,h,auth,material,base,g,r,out,expected=_prepared_context(name)
    receipt=obj(g+'ACCEPTANCE.json');mapping=obj(g+'ACCEPTANCE_CURRENT_SELECTED_MAP.json',receipt['actual_current_map_file'])
    check_acceptance(receipt,mapping,r,expected)
    received=receipt['main_observed']
    native_commit=api(h,'git/commits/'+received)
    ancestry=api(h,'compare/'+r['commit']+'...'+received)['status']
    check_receipted_commit(receipt,r,native_commit,ancestry)
    reconstructed,receipt_ack=reconcile(c,h,{'commit':r['commit'],'tree':r['tree'],'selected_files':expected},received,receipt['UTC'])
    check_receipted_map(mapping,reconstructed,receipt_ack)
    need(c.selected_current(h,received,reconstructed,r['tree'])==receipt['actual_tree'],'Every prepared selected identity at native receipted MAIN/tree')
    validate_cache(h)
    main,tree,current,ack=_actual(c,h,material,r,reconstructed,received,receipt['actual_tree'])
    return c,h,g,r,receipt,main,out,ack


def check_acceptance(receipt,mapping,r,prepared_expected):
    fields={'schema','evidence_scope','UTC','PR','accepted','case_percent','checkpoint_commit','sole_parent','main_observed','actual_tree','original_head','selected_files','actual_current_selected_map_sha256','actual_current_map_file','every_selected_identity_checked_at_actual_observed_MAIN','full_foreign_tree_scope_preserved','all_overlay_body_identities_verified','QUEUE_native_original_PR_unchanged','mathematical_clearance','source_contract_clearance','priority_clearance','publication_ready','NEW_whole_package_reviews_completed'}|set(COUNTS)
    need(type(receipt) is dict and set(receipt)==fields,'Exact actual acceptance receipt schema')
    need(type(mapping) is dict and set(mapping)=={'selected_files','selected_map_sha256','foreign_QUEUE_reconciliation_after_checkpoint'},'Exact actual acceptance map record schema')
    need(receipt['schema']=='pr206-actual-custody10-acceptance-v2' and receipt['accepted'] is True and type(receipt['PR']) is int and receipt['PR']==206 and type(receipt['case_percent']) is int and receipt['case_percent']==10 and receipt['checkpoint_commit']==r['commit'],'Own actual full acceptance before sync/pointer')
    need(all(type(receipt[k]) is str and re.fullmatch('[0-9a-f]{40}',receipt[k]) is not None for k in ('checkpoint_commit','sole_parent','main_observed','actual_tree','original_head')),'Exact acceptance native SHA fields')
    need(type(receipt['UTC']) is str and datetime.datetime.fromisoformat(receipt['UTC']).tzinfo is not None,'Explicit receipt timestamp')
    bytepin(receipt['actual_current_map_file'])
    need(all(type(receipt[k]) is type(v) and receipt[k]==v for k,v in COUNTS.items()) and all(receipt[k] is True for k in ('every_selected_identity_checked_at_actual_observed_MAIN','full_foreign_tree_scope_preserved','all_overlay_body_identities_verified','QUEUE_native_original_PR_unchanged')),'Acceptance complete factual guards')
    need(all(receipt[k] is False for k in ('mathematical_clearance','source_contract_clearance','priority_clearance','publication_ready')) and type(receipt['NEW_whole_package_reviews_completed']) is int and receipt['NEW_whole_package_reviews_completed']==0,'No scientific/publication/whole-package promotion at custody10')
    need(receipt.get('sole_parent')==r['expected_main'] and receipt.get('original_head')==HEAD and receipt.get('evidence_scope')=='ACTUAL_HELPER_NATIVE_RECHECK','Receipt original HEAD and exact prepared sole parent')
    accepted=mapping['selected_files']
    digest(prepared_expected)
    need(Q in prepared_expected and type(accepted) is dict and set(accepted)==set(prepared_expected),'Exact complete prepared acceptance-map path set')
    need(type(receipt['selected_files']) is int and receipt['selected_files']==len(accepted)==len(prepared_expected),'Full prepared acceptance-map count')
    need(all(accepted[path]==value for path,value in prepared_expected.items() if path!=Q),'All non-QUEUE accepted identities equal full prepared expected identities')
    need(digest(accepted)==mapping['selected_map_sha256']==receipt['actual_current_selected_map_sha256'],'Actual acceptance map')


def check_receipted_commit(receipt,r,native_commit,ancestry):
    need(native_commit['sha']==receipt['main_observed'] and native_commit['tree']['sha']==receipt['actual_tree'],'Native receipted MAIN commit-to-tree binding')
    need(ancestry in ('identical','ahead'),'Own checkpoint ancestry at receipted MAIN')
    need(receipt['sole_parent']==r['expected_main'] and receipt['original_head']==HEAD,'Receipted original HEAD and prepared parent')


def check_receipted_map(mapping,reconstructed,receipt_ack):
    recorded_ack=mapping['foreign_QUEUE_reconciliation_after_checkpoint']
    need(type(recorded_ack) is dict and {k:v for k,v in recorded_ack.items() if k!='UTC'}=={k:v for k,v in receipt_ack.items() if k!='UTC'},'Independently reconstructed checkpoint-to-receipt QUEUE continuity')
    need(reconstructed==mapping['selected_files'],'Complete receipt map must equal native reconstruction from prepared expected map')


def sync_images(images):
    """Pure filesystem guard primitive; images are exactly five bounded view records."""
    need(type(images) is list and len(images)==5 and {x[0] for x in images}==set(VIEWS),'Exactly five synchronization views')
    captured=[]
    for path,expected,post in images:
        pin(post);prior=optional(path)
        need((None if prior is None else pin(prior)) in (expected,pin(post)),'Unexpected local five preimage/type')
        captured.append((path,None if prior is None else pin(prior),post))
    for path,prior,post in captured:
        raw=optional(path);need((None if raw is None else pin(raw))==prior,'Five-set changed after precheck')
    for path,prior,post in captured:atomic(path,post,prior)
    for path,prior,post in captured:need(read(path)==post,'All-five final readback')
    return [{'path':path,'postimage':pin(post)} for path,prior,post in captured]


def sync(name):
    c,h,g,r,receipt,main,out,ack=_accepted_context(name)
    images=[(path,r['local_five_expected_preimages'][path],out[path]) for path in VIEWS]
    files=sync_images(images)
    need(api(h,'git/ref/heads/main')['object']['sha']==main,'MAIN advanced during sync; no success receipt')
    result={'UTC':now(),'PR':206,'actual_checkpoint':r['commit'],'acceptance_pin':pin(read(g+'ACCEPTANCE.json')),'all_five_local_files_match_actual_checkpoint':True,'files':files,'fresh_MAIN_revalidated':main,**COUNTS}
    save(g+'LOCAL_GLOBAL_FIVE_SYNC.json',result);return result


def pointer(name):
    c,h,g,r,receipt,main,out,ack=_accepted_context(name)
    synced=obj(g+'LOCAL_GLOBAL_FIVE_SYNC.json')
    need(synced['PR']==206 and synced['actual_checkpoint']==r['commit'] and synced['acceptance_pin']==pin(read(g+'ACCEPTANCE.json')) and synced['all_five_local_files_match_actual_checkpoint'] is True and synced['files']==[{'path':path,'postimage':pin(out[path])} for path in VIEWS],'Actual full five-sync receipt before pointer')
    for path in VIEWS:need(read(path)==out[path],'Pointer local five byte/mode readback')
    need(api(h,'git/ref/heads/main')['object']['sha']==main,'MAIN advanced before pointer; revalidate')
    value={'UTC':now(),'PR':206,'phase':'custody','directory':'custody_checkpoint_02/'+name,'checkpoint_commit':r['commit'],'main_observed':receipt['main_observed'],'fresh_MAIN_revalidated_before_pointer':main,'acceptance_pin':pin(read(g+'ACCEPTANCE.json')),'Root_recorded_only_after_actual_full_scope_acceptance':True,**COUNTS}
    atomic(POINTER,enc(value),None);return value
