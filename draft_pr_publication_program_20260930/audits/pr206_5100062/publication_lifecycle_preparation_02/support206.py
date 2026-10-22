"""Prepared PR206 lifecycle native guards. Root injects reviewed modules/authority.
No historical loader, backend import, service/ref mutation or CLI is provided.
"""
from pathlib import Path
import base64, copy, datetime, fcntl, hashlib, json, os, re, stat, sys, tempfile
D=Path(__file__).absolute().parent
A=D.parent
ROOT=A.parent.parent.parent
P='draft_pr_publication_program_20260930/'
CASE=P+'audits/pr206_5100062/'
OWN=CASE+'publication_lifecycle_preparation_02/'
NATIVE='unsolved_math_prioritization/attempts/5100062/'
ALL_NATIVE='unsolved_math_prioritization/attempts/'
Q='unsolved_math_prioritization/QUEUE.md'
VIEWS=(CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md')+tuple(P+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md'))
PHASES={'ready':(10,90,None),'merge':(90,95,'ready'),'factual':(95,98,'merge'),'completion':(98,100,'factual')}
POINTER={k:CASE+'ROOT_ACTUAL_'+k.upper()+'_CHECKPOINT.json' for k in PHASES}
HEAD='488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7'
HEAD_TREE='c67029118e3090c49c8601f6121fc0b93019e7ac'
HEAD_PARENT='0a13fdb1f33dc1e6351b5d8ce7a55e36b5eedd00'
FORK='5f672f535a9f76da203d99020263a83d5f2de5ce'
DECLARED='a7e588da5ac76913e00f979681f2dfff2d9a56be'
BASE_COMMIT='03a935d0ca4361d6923f53b6fe918719ec1b20d3'
BASE_TREE='6d8b62ecba9dfbb39f35f244dcea4bb487b4c63f'
BASE_DIGEST='8e9ba46e89c1caae681852724b146c99d5c8d108e7eea12421fd723d4ac182de'
BASE_DIRECTORY='custody_checkpoint_02/custody10_03/'
BASE_ACCEPT={'bytes':1372,'sha256':'040243d2be20384468efc4b827adea3d654d57def8f3580e4975a1d3360f33ad'}
BASE_MAP={'bytes':1327176,'sha256':'a5ed7edc7e4deef0baf5017d2539b0533f930c001e02bd3e6592f4cb7bd15df6'}
BASE_VERIFY={'bytes':1919,'sha256':'b3f5a5e4489aac7eec1ded4270214de954b6e540aa644df0823db005bf31a9d4'}
BASE_POINTER={'bytes':738,'sha256':'639d9b554aa12892308f9280fb7506d4b9fdba5eed37bd7b5c307a3ca089c1bf'}
BASE_SYNC={'bytes':1765,'sha256':'e514bb5557660f7bd6d61c342ffec98a7c6ca96a34050fac91856bd7c56a087b'}
BASE_ROW={'bytes':123,'sha256':'702a187848c9d2debcd519061ba1497a7e56688ef9106eddbc8c95bb2cc150ef'}
HEAD_ROW={'bytes':511,'sha256':'7406859e7ca2b290833c8a59910f69140244ccf81bb975b254f1024ae246b4d9'}
ORIGINAL_METADATA={'bytes':18017,'sha256':'198a22a7e5b536d6b96f65597446e3b7d2d5e7648d2ad23390106dc49d48800a'}
CUSTODY={'bytes':9605,'sha256':'118ac187bf927f3dce246ca1b3eb31fb1bca6c87b61089b8af38ed01b7e33f02'}
QRECEIPT={'bytes':2590,'sha256':'63d776ec793be2bd05dfe9af684f04603e7bad3d8e21d8fab301c034f0feea5a'}
INVENTORY={'bytes':7826,'sha256':'9ce95e0155ea64c1cec9f41fe6b4431a437fdfaae7ef45e146befc649720fb6e'}
COLLECTOR='original_custody_collector_01_20261016T174700Z/'
PORTABLE={'bytes':21804,'sha256':'dfa1ff339e1f3a6004563aec9c01f6f14d6bb65a94e2437f3ba3a41e5b393d85'}
FIXED_GATES={
'ROOT_MATHEMATICAL_SOURCE_GATE_01.json':{'bytes':3027,'sha256':'d7c10c5c4001efd49749f805a523cc6b4a95c82840d5ef31a0e0231633a694da'},
'ROOT_PRIORITY_EDITORIAL_GATE_01.json':{'bytes':5297,'sha256':'f81e10f7e0b45659b97080438c7bd7cfdb695d73c3c35e54bf6e14dec2a7f45b'},
'ROOT_SOURCE_BIBLIOGRAPHIC_CORRECTION_01.json':{'bytes':936,'sha256':'234f8ae1418f9eda2537bf2c7b3510a5715d3debfe4ec1bf409fc9bac11b6d75'},
'ROOT_CURRENT_VERIFIER_ADOPTION_01.json':{'bytes':2684,'sha256':'f65c076a1b8f8742d10db02bf1a5243dfc6a75caf948035688ea688e45605d9a'}}
SOURCE_ADOPTION='ROOT_LIFECYCLE_SOURCE_ADOPTION_01.json'
PUBLICATION_GATE='ROOT_PUBLICATION_GATE_01.json'
SOURCES=frozenset(('support206.py','ready206.py','lifecycle206.py','make_native206.py'))
SOURCE_FILES=SOURCES|{'race_guards.py','RACE_GUARDS_NORMAL.json','RACE_GUARDS_OPTIMIZED.json','CONCURRENCY_CONTRACT.md','REPAIR_PROVENANCE.json','offline_guards.py','CHECKPOINT_CONTRACT.md','ROOT_FUTURE_INTERFACE.json','NATIVE_CONSTRUCTOR_PROTOCOL.json','BASELINE_AUTHORITY.json','FROZEN_PREPARATION_PLAN.json','SOURCE_FORMAT_REFERENCES.json','OFFLINE_GUARDS_NORMAL.json','OFFLINE_GUARDS_OPTIMIZED.json','RESEARCH_LOG.md'}
SOURCE_PUBLIC=SOURCE_FILES|{'SAFE_AUTHORED_MANIFEST.json','SOURCE_SEAL.json'}
BASE_COUNTS={'fully_completed_count':48,'published_count':32,'last_completed_PR':205,'next_numeric_intake_cursor':206,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
DONE_COUNTS={'fully_completed_count':49,'published_count':33,'last_completed_PR':206,'next_numeric_intake_cursor':207,'advance_to_next_PR_authorized_now':True,'goal_complete':False}
RECEIPT_ALIASES=frozenset(('Root_publication_gate_pin','package','package_seal','publication_ready','NEW_whole_package_reviews_completed','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','priority_clearance','priority_novelty_clearance','historical_firstness_independence_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged','completed'))|set(BASE_COUNTS)
CLAIM='For a proper nested confocal ellipse pair admitting an odd primitive Poncelet billiard family, the product of the signed areas obtained by unit-circle inversion of the original orbit vertices in the two original foci is constant along each admitted family, including all coprime stars and reversal. For every integer r>=1, repeating an odd primitive cycle r times scales each signed area by r and the product by r squared.'
CREDIT='Attributed verification/research note: the historical RGK k903,a target is Table10 on page12, row k903,a dated10/20 (October2020); RGH N=3 and Conjecture1 are credited. Alper Ferudun, DOI10.5281/zenodo.23096994, treats the same target with substantially the same compact flag-curve mechanism. The RGH public-preprint delta defect is disclosed; journal full text/typography were uninspected and no general corrected RGH formula is claimed. Chavez-Caliz DOI10.1007/s40598-020-00154-8 is used. No theorem/formula/method novelty, absolute firstness, certified discovery independence, literal simultaneity or current-open status is claimed. Specified GitHub/Zenodo record dates do not certify first public availability of every byte or repository visibility history.'
EFFORT='Original submitted claimed_solved1/5 is preserved; author turns and actual model/reasoning effort remain unverified. Four Git commits are not four author turns; later audits are separate.'
SOURCE_FACTS={'RGK_target_table':10,'RGK_table_page':12,'RGK_row_identifier':'k903,a','RGK_row_date':'10/20','RGK_row_date_meaning':'October2020','repetition_multiplicity':'every integer r>=1 for an odd primitive cycle','Chavez_DOI':'10.1007/s40598-020-00154-8','Ferudun_DOI':'10.5281/zenodo.23096994','Ferudun_same_target_and_substantially_same_mechanism':True,'RGH_journal_full_text_and_typography_inspected':False,'RGH_general_corrected_formula_claimed':False,'RGH_preprint_delta_defect_disclosed':True,'current_openness_established':False,'novelty_established':False,'absolute_firstness_established':False,'certified_discovery_independence':False,'literal_simultaneity_established':False}
MAX_BYTES=32*1024*1024
MAX_SELECTED=12000
MAX_OVERLAY=400
MAX_CHANGED=30000
MAX_NATIVE_WORK=30000
MAX_NATIVE_DEPTH=64
_backend=None
_authority_pin=None
_drivers={}
_validation_stack=[]
PROGRAM_VIEW_LOCK=P+'ROOT_GLOBAL_FIVE_WRITER.lock'
PROGRAM_VIEW_LOCK_BYTES=b'PR publication program: stable Root cooperating global-five writer lock v1\nNever unlink or replace this inode; every existing-view writer must flock it.\n'
_writer_lease=None
_view_session=None


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


def writer_protocol():
    return {'schema':'pr206-program-view-writer-protocol-v1','lock_path':PROGRAM_VIEW_LOCK,'lock_payload':pin(PROGRAM_VIEW_LOCK_BYTES),'every_existing_view_writer_must_hold_same_stable_inode':True,'never_unlink_or_replace_lock_inode':True,'Root_alone_operates_existing_views':True,'uncooperative_same_UID_content_CAS_guaranteed':False}


def _identity(relative):
    try:value=_path(relative).lstat()
    except FileNotFoundError:return None
    need(stat.S_ISREG(value.st_mode),'Regular unchanged local target identity')
    return (value.st_dev,value.st_ino,value.st_size,stat.S_IMODE(value.st_mode))


def _owned_artifacts(directory):
    need(type(directory) is str and directory.startswith(OWN) and directory.endswith('/'),'Owned generation artifact directory')
    name=directory[len(OWN):-1];need(generation(name)==directory,'One exact owned generation directory')
    target=_path(directory[:-1]);need(stat.S_ISDIR(target.lstat().st_mode),'Existing owned generation directory')
    return target


def _evidence(directory,label,raw):
    pin(raw);target=_owned_artifacts(directory)
    fd,name=tempfile.mkstemp(prefix='.pr206_'+label+'_',dir=target)
    # Failure leaves this staged/evidence inode in its owned generation.
    with os.fdopen(fd,'wb') as stream:
        need(stream.write(raw)==len(raw),'Short owned evidence write')
        stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
    _fsync_dir(target)
    return Path(name)


def _failure(directory,label,error,conflict=False,observed=None):
    record={'schema':'pr206-local-write-failure-v2','UTC':now(),'target':label,'error':str(error),'detected_conflict':conflict,'successful_sync_or_pointer':False}
    if type(observed) is bytes:
        path=_evidence(directory,'observed_conflict',observed);record['preserved_observed']={'file':path.name,**pin(observed)}
    _evidence(directory,'failure',enc(record))
    if conflict:
        target=_owned_artifacts(directory)/'LOCAL_WRITE_CONFLICT.json'
        try:fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
        except FileExistsError:return
        with os.fdopen(fd,'wb') as stream:
            raw=enc(record);need(stream.write(raw)==len(raw),'Short conflict latch write');stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
        _fsync_dir(target.parent)


def _generation_clean(directory):
    _owned_artifacts(directory)
    need(optional(directory+'LOCAL_WRITE_CONFLICT.json') is None,'Detected local writer conflict: generation is permanently barred from sync/pointer; Root recovery review required')


def _writer_owned():
    need(_writer_lease is not None and _writer_lease['pid']==os.getpid(),'Current-process program-level writer ownership required')
    fd=_writer_lease['fd'];opened=os.fstat(fd);current=_path(PROGRAM_VIEW_LOCK).lstat()
    need(stat.S_ISREG(opened.st_mode) and stat.S_ISREG(current.st_mode) and stat.S_IMODE(current.st_mode)==0o444 and (opened.st_dev,opened.st_ino)==_writer_lease['identity']==(current.st_dev,current.st_ino),'Stable opened program-lock inode/path identity')
    need(read(PROGRAM_VIEW_LOCK)==PROGRAM_VIEW_LOCK_BYTES,'Exact stable program-lock payload')


class WriterOwnership:
    """Advisory serialization for cooperating Root writers, not arbitrary-UID CAS."""
    def __init__(self,artifact_directory=None):self.artifact_directory=artifact_directory
    def __enter__(self):
        global _writer_lease
        need(_writer_lease is None,'Program writer lease is nonreentrant')
        target=_path(PROGRAM_VIEW_LOCK);before=target.lstat()
        need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444,'Root must separately install the stable readonly regular program lock')
        fd=os.open(target,os.O_RDONLY|os.O_NOFOLLOW)
        try:
            opened=os.fstat(fd);need((opened.st_dev,opened.st_ino)==(before.st_dev,before.st_ino),'Program lock changed before acquire')
            fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            _writer_lease={'fd':fd,'pid':os.getpid(),'identity':(opened.st_dev,opened.st_ino)};_writer_owned()
        except BaseException:
            _writer_lease=None;os.close(fd);raise
        return self
    def __exit__(self,kind,value,tb):
        global _writer_lease
        lease=_writer_lease
        try:_writer_owned()  # Detect renamed/replaced lock even on failure exit.
        except BaseException as error:
            if self.artifact_directory is not None:_failure(self.artifact_directory,'PROGRAM_VIEW_LOCK',error,True)
            raise
        finally:
            _writer_lease=None
            if lease is not None:
                try:fcntl.flock(lease['fd'],fcntl.LOCK_UN)
                finally:os.close(lease['fd'])
        return False


def atomic(relative,raw,expected,artifact_directory=None):
    """Absent target: unconditional no-replace. Existing views: cooperating lease."""
    need(relative.startswith(OWN) or relative in VIEWS or relative in POINTER.values(),'Exact local output scope')
    pin(raw);target=_path(relative)
    if relative in VIEWS:
        _writer_owned();need(_view_session is not None and relative in _view_session['records'],'All-five protected session required for every view write')
        directory=_view_session['directory'];need(expected==_view_session['records'][relative]['pin'],'Exact captured session preimage')
    else:
        need(expected is None,'Receipts and pointers are unconditionally create-only')
        directory=artifact_directory if artifact_directory is not None else relative.rsplit('/',1)[0]+'/'
        if relative in POINTER.values():_writer_owned()
    _generation_clean(directory);staged=_evidence(directory,'staged_postimage',raw)
    try:
        prior=optional(relative)
        if (None if prior is None else pin(prior))!=expected:
            _failure(directory,relative,'Stale local preimage',True,prior);raise RuntimeError('Local target preimage conflict')
        installation=_evidence(directory,'installation_postimage',raw)
        if expected is None:
            # link creates the destination entry only if absent, atomically.
            try:os.link(installation,target,follow_symlinks=False)
            except FileExistsError:
                _failure(directory,relative,'Atomic no-replace target already exists',True,optional(relative));raise
            _fsync_dir(target.parent);need(read(relative)==raw,'No-replace file readback')
            installation.unlink();_fsync_dir(installation.parent)
        else:
            _writer_owned();record=_view_session['records'][relative]
            if _identity(relative)!=record['identity'] or optional(relative)!=prior:
                _failure(directory,relative,'View identity/content changed under ownership',True,optional(relative));raise RuntimeError('View preimage conflict')
            # Every cooperating writer holds this same stable program lock.
            # Arbitrary same-UID writers ignoring flock are outside this model.
            os.replace(installation,target);_fsync_dir(target.parent)
            if read(relative)!=raw:
                _failure(directory,relative,'View changed before final readback',True,optional(relative));raise RuntimeError('View readback conflict')
    except BaseException as error:
        _failure(directory,relative,error,isinstance(error,(RuntimeError,FileExistsError)))
        raise



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


def validate_cache(h):
    need(len(h.m.native_tree_cache)<=MAX_CHANGED,'Bounded native tree cache')
    for oid,rows in h.m.native_tree_cache.items():h.m.verify_tree_object(oid,rows)


def api(h,endpoint,method='GET',body=None):
    need(method=='GET' or (method=='POST' and endpoint in ('git/trees','git/commits','git/blobs')),'Helper has no ref/PR/service mutation interface')
    if method=='GET':need(re.fullmatch(r'(git/ref/heads/main|git/commits/[0-9a-f]{40}|git/blobs/[0-9a-f]{40}|git/trees/[0-9a-f]{40}|compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}|pulls/206)',endpoint) is not None,'Exact native read endpoint')
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


def sync_images(images,artifact_directory):
    """All-five cooperative guard; atomicity is per file, with retained evidence."""
    global _view_session
    _writer_owned();_generation_clean(artifact_directory)
    need(_view_session is None and type(images) is list and len(images)==5 and {x[0] for x in images}==set(VIEWS),'Exactly five nonreentrant synchronization views')
    captured=[]
    try:
        for path,expected,post in images:
            pin(post);prior=optional(path)
            if (None if prior is None else pin(prior)) not in (expected,pin(post)):
                _failure(artifact_directory,path,'Unexpected full-five preimage',True,prior);raise RuntimeError('Unexpected local five preimage')
            identity=_identity(path);captured.append((path,None if prior is None else pin(prior),post,identity))
            if prior is not None:_evidence(artifact_directory,'view_preimage',prior)
        for path,prior,post,identity in captured:
            raw=optional(path)
            if (None if raw is None else pin(raw))!=prior or _identity(path)!=identity:
                _failure(artifact_directory,path,'Full-five set changed after precheck',True,raw);raise RuntimeError('Five-set preimage conflict')
        _view_session={'directory':artifact_directory,'records':{path:{'pin':prior,'identity':identity} for path,prior,post,identity in captured}}
        for path,prior,post,identity in captured:atomic(path,post,prior)
        for path,prior,post,identity in captured:
            if read(path)!=post:
                _failure(artifact_directory,path,'Final full-five readback conflict',True,optional(path));raise RuntimeError('Full-five readback conflict')
        _writer_owned();_generation_clean(artifact_directory)
        return [{'path':path,'postimage':pin(post)} for path,prior,post,identity in captured]
    except BaseException as error:
        _failure(artifact_directory,'ALL_FIVE',error,isinstance(error,RuntimeError))
        raise
    finally:_view_session=None


def frozen(name,expected=None,readonly=True):return read(CASE+rel(name),expected,readonly)
def artifact(name,expected=None):return decode(frozen(name,expected))
def pp(name,value):return {'path':rel(name),**bytepin(value)}
def counts(phase,actual=False):
    need(phase in PHASES and type(actual) is bool,'Phase/counter selector')
    return dict(DONE_COUNTS if phase=='completion' and actual else BASE_COUNTS)
def generation(name):
    need(type(name) is str and re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Safe generation name')
    return OWN+name+'/'


def configure_backend(c,h):
    global _backend
    need(_backend is None,'Fresh Root dispatcher instance required')
    need(all(callable(getattr(c,k,None)) for k in ('byte_pin','selected_digest','selected_current')) and all(callable(getattr(h,k,None)) for k in ('api','lookup','changed_leaves')),'Injected direct c191/h190 interface')
    need(callable(getattr(getattr(h,'m',None),'verify_tree_object',None)) and type(h.m.native_tree_cache) is dict,'Injected native tree interface')
    _backend=(c,h)


def configure_authority(wanted):
    global _authority_pin
    need(_authority_pin is None,'Fresh source authority required')
    wanted=copy.deepcopy(bytepin(wanted));authority(wanted);_authority_pin=wanted


def authority(wanted=None):
    wanted=_authority_pin if wanted is None else wanted
    need(wanted is not None,'Missing future exact actual Root lifecycle source adoption')
    value=artifact(SOURCE_ADOPTION,wanted)
    need(value.get('schema')=='pr206-root-lifecycle-source-adoption-v1' and value.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and value.get('accepted_preparation_only') is True and value.get('PR')==206 and value.get('original_head')==HEAD,'Actual Root lifecycle source adoption')
    need(value.get('external_dispatcher_owns_authenticated_direct8_adapter_and_all_alias_cache_cleanup') is True,'External Root dispatcher ownership')
    need(enc(value['program_view_writer_protocol'])==enc(writer_protocol()),'Exact Root-adopted cooperating-writer protocol; no uncooperative same-UID CAS promise')
    need(set(value['sources'])=={D.name+'/'+name for name in SOURCES},'Exact four adopted source paths')
    manifest=artifact(D.name+'/SAFE_AUTHORED_MANIFEST.json',value['source_manifest'])
    need(set(manifest['files'])==SOURCE_FILES,'Exact authored safe manifest')
    for name,p in manifest['files'].items():frozen(D.name+'/'+name,bytepin(p))
    for name,p in value['sources'].items():need(p==manifest['files'][name.split('/')[-1]],'Exact adopted source buffer pins')
    seal=artifact(D.name+'/SOURCE_SEAL.json',value['source_seal']);need(seal['safe_manifest']==value['source_manifest'],'Exact source seal')
    need(value['expected_publication_gate']['path']==PUBLICATION_GATE and set(value['expected_publication_gate'])=={'path','bytes','sha256'},'Mandatory exact future publication gate binding')
    bytepin({k:value['expected_publication_gate'][k] for k in ('bytes','sha256')})
    return value


def runtime():
    need(not sys.flags.optimize and sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.safe_path,'Ordinary Python -E -S -B -P required')
    authority();need(_backend is not None,'Root must explicitly inject native backend')
    return _backend


def register(phase,driver):
    need(phase in PHASES and phase not in _drivers,'Distinct configured phase driver')
    need(set(driver)=={'inputs','overlay','parents','original','queue_before','queue_after','facts','mutable'} and all(callable(v) for v in driver.values()),'Complete explicit phase driver')
    _drivers[phase]=driver


def originals():
    custody=artifact('ORIGINAL_SUBMISSION_CUSTODY.json',CUSTODY)
    inventory=artifact(COLLECTOR+'ORIGINAL_NATIVE_FILE_INVENTORY.json',INVENTORY)
    need(custody['original_head']==HEAD and custody['original_tree']==HEAD_TREE and custody['original_sole_parent']==HEAD_PARENT and custody['authenticated_authored_range_base']==FORK and custody['declared_PR_base']==DECLARED,'Both exact original range baselines')
    files=inventory['files'];need(len(files)==21 and sum(x['bytes'] for x in files.values())==55033 and custody['file_count']==21 and custody['total_native_bytes']==55033,'Original21/55033 extent')
    out={}
    for name,value in files.items():
        raw=frozen('original_submitted_head/'+rel(name));need(bpin(raw)=={k:value[k] for k in ('bytes','sha256','git_blob')},'Original immutable archive '+name);out[name]=raw
    return custody,out


def queue_rows():
    q=artifact('ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json',QRECEIPT);base=q['base_own_row']['text'].encode();head=q['original_QUEUE_row']['text'].encode()
    need(q['original_head']==HEAD and q['declared_PR_base']==DECLARED and q['authenticated_authored_range_base']==FORK and q['foreign_QUEUE_bytes_identical_for_both_ranges'] is True and q['own_only_changed_row'] is True,'Original own-only QUEUE range')
    need(pin(base)==BASE_ROW and pin(head)==HEAD_ROW and (q['BASE_status'],q['BASE_effort'],q['HEAD_status'],q['HEAD_effort'])==('queued','0/5','claimed_solved','1/5'),'BASE123 versus original HEAD511 eligibility')
    return q,base,head


def published_row(doi):
    need(type(doi) is str and re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*',doi) is not None,'Actual published DOI')
    cells=queue_rows()[2].decode().rstrip('\n').split('|')
    cells[10]=' https://github.com/AlecKriebel/Math/pull/206 '
    cells[11]=' '+CLAIM+' '+CREDIT+' '+EFFORT+' Extensive AI; unrefereed; no conventional human peer review. '
    cells[12]=' ['+doi+'](https://doi.org/'+doi+') '
    return '|'.join(cells).encode()+b'\n'


def replace_queue(raw,doi):
    rows=raw.splitlines(keepends=True);ix=[i for i,row in enumerate(rows) if b'| 5100062 / AMR-050-0062 |' in row]
    need(len(ix)==1 and rows[ix[0]]==queue_rows()[1],'First merge requires exact own BASE123 row')
    result=list(rows);result[ix[0]]=published_row(doi)
    need([i for i,(a,b) in enumerate(zip(rows,result)) if a!=b]==ix,'Only own merge QUEUE row changes')
    return b''.join(result)


def reconcile_rows(old,new,selected,own):
    pin(old);pin(new);pin(own)
    a,b=old.splitlines(keepends=True),new.splitlines(keepends=True);need(len(a)==len(b),'QUEUE line count')
    protected={path.split('/')[2] for path in selected if path.startswith(ALL_NATIVE)}|{'5100062'}
    def identity(row):
        cells=row.decode().split('|');need(len(cells)==14 and cells[1].strip().isdigit(),'Changed QUEUE row schema')
        code=cells[2].strip().split(' / ');need(len(code)==2 and code[0].isdigit(),'Changed QUEUE identity');return code[0]
    changed=[]
    for index,(x,y) in enumerate(zip(a,b)):
        if x==y:continue
        target=identity(x);need(identity(y)==target and target not in protected,'Own/protected QUEUE mutation')
        changed.append({'line':index+1,'problem_id':target,'before':bpin(x),'after':bpin(y)})
    marker=b'| 5100062 / AMR-050-0062 |'
    need([x for x in a if marker in x]==[own]==[x for x in b if marker in x],'Phase-specific exact own QUEUE row')
    return changed


def reconcile(c,h,base,main,own,stamp):
    old,new=body(h,Q,base['commit']),body(h,Q,main);need(bpin(old)==base['selected_files'][Q],'Accepted baseline QUEUE pin')
    changed=reconcile_rows(old,new,base['selected_files'],own)
    return {**base['selected_files'],Q:bpin(new)},{'UTC':stamp,'baseline_actual_commit':base['commit'],'observed_MAIN':main,'old_QUEUE':bpin(old),'current_QUEUE':bpin(new),'foreign_unprotected_row_changes':changed,'own_and_all_protected_rows_unchanged':True}


def baseline_custody():
    receipt=artifact(BASE_DIRECTORY+'ACCEPTANCE.json',BASE_ACCEPT);mapping=artifact(BASE_DIRECTORY+'ACCEPTANCE_CURRENT_SELECTED_MAP.json',BASE_MAP)
    verification=artifact('ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json',BASE_VERIFY);pointer=artifact('ROOT_ACTUAL_CUSTODY_CHECKPOINT.json',BASE_POINTER)
    artifact(BASE_DIRECTORY+'LOCAL_GLOBAL_FIVE_SYNC.json',BASE_SYNC)
    need(receipt['accepted'] is True and receipt['case_percent']==10 and receipt['checkpoint_commit']==receipt['main_observed']==BASE_COMMIT and receipt['actual_tree']==BASE_TREE,'Actual custody10 baseline')
    need(receipt['every_selected_identity_checked_at_actual_observed_MAIN'] is True and receipt['full_foreign_tree_scope_preserved'] is True and verification['actual_custody_checkpoint_fully_accepted'] is True and verification['all_five_local_views_pins_and_readonly_modes_verified'] is True,'Actual custody full-scope authority')
    selected=mapping['selected_files'];need(len(selected)==4416 and digest(selected)==mapping['selected_map_sha256']==receipt['actual_current_selected_map_sha256']==BASE_DIGEST and receipt['actual_current_map_file']==BASE_MAP,'Complete4416 custody selected map')
    need(all(type(receipt[k]) is type(v) and receipt[k]==v for k,v in BASE_COUNTS.items()),'Baseline counters')
    return {'commit':BASE_COMMIT,'tree':BASE_TREE,'selected_files':selected,'directory':BASE_DIRECTORY.rstrip('/'),'acceptance_pin':BASE_ACCEPT,'pointer_pin':BASE_POINTER}


def fixed_gates():
    records={name:artifact(name,p) for name,p in FIXED_GATES.items()}
    math=records['ROOT_MATHEMATICAL_SOURCE_GATE_01.json'];priority=records['ROOT_PRIORITY_EDITORIAL_GATE_01.json'];portable=records['ROOT_CURRENT_VERIFIER_ADOPTION_01.json'];bibliography=records['ROOT_SOURCE_BIBLIOGRAPHIC_CORRECTION_01.json']
    need(math['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and math['accepted_universal_theorem'] is True and math['accepted_exact_source_contract'] is True,'Root exact universal/source theorem')
    need(priority['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and priority['bounded_priority_audit_accepted_complete'] is True and priority['manuscript_preparation_authorized'] is True and priority['exact_overlap_verified'] is True and priority['overlap_proof_mechanism_substantially_same'] is True and priority['overlap_DOI']==SOURCE_FACTS['Ferudun_DOI'],'Qualified prior exact overlap')
    need(all(priority[k] is False for k in ('novelty_established','absolute_firstness_established','certified_discovery_independence','literal_simultaneity_established','current_openness_established')),'No false novelty/independence/openness')
    need(portable['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and portable['accepted_finite_exact_source'] is True and {k:portable['source'][k] for k in ('bytes','sha256')}==PORTABLE and bibliography['correct_DOI']==SOURCE_FACTS['Chavez_DOI'],'Root finite verifier/bibliography')
    frozen(portable['source']['path'],PORTABLE,False)
    return records


def safe_public(name):
    rel(name)
    need(not any(part.startswith('private') or part in ('__pycache__','.venv','site-packages','node_modules') for part in name.split('/')) and not name.endswith(('.pyc','.pyo')) and 'ACCEPTANCE_CURRENT_SELECTED_MAP' not in name and not name.startswith(COLLECTOR+'api/'),'Public safe artifact scope')
    return name


def validate_gate_shape(g):
    need(g.get('schema')=='pr206-root-publication-ready-v1' and g.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and (g.get('PR'),g.get('problem_id'),g.get('original_head'))==(206,5100062,HEAD),'Final actual Root publication gate identity')
    need(all(g.get(k) is True for k in ('publication_ready_gate_accepted','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','current_verifier_source_accepted')),'All final ready qualifications')
    need(all(g.get(k) is False for k in ('historical_priority_established','theorem_novelty_cleared','formula_novelty_cleared','proof_method_novelty_cleared','first_disclosure_certified','independent_discovery_certified','literal_simultaneity_established','current_openness_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged')),'No readiness future/novelty facts')
    need(g['claim']==CLAIM and g['source_facts']==SOURCE_FACTS,'Exact qualified target/source facts')
    need(type(g['metadata']) is dict and type(g['metadata'].get('title')) is str and g['metadata']['title'].strip(),'Final Root-approved title/metadata, never guessed')
    events=g['whole_package_review_events'];need(type(events) is list and 2<=len(events)<=32,'Fresh whole-package Root events, not two mathematical author reviews')
    seen=set();receipts=set()
    for index,event in enumerate(events,1):
        need(event['review_number']==index and type(event['review_number']) is int and event['whole_package_scope'] is True and type(event['open_findings']) is int and event['open_findings']>=0 and event['directory'] not in seen and event['Root_acceptance_file'] not in receipts,'Distinct ordered actual whole-package reviews')
        need(event['verdict']!='CLEANPASS' or event['open_findings']==0,'Clean event cannot have findings');seen.add(event['directory']);receipts.add(event['Root_acceptance_file'])
    final=events[-1]
    need(final['verdict']=='CLEANPASS' and final['open_findings']==0 and final['reviewed_package']==g['package'] and final['reviewed_package_seal']==g['package_seal'],'Last fresh clean review of exact final package seal')
    if any(event['verdict']!='CLEANPASS' for event in events):need(g.get('fresh_final_review_after_documented_editorial_repairs') is True,'Fresh final review after repairs')


def gate(wanted=None):
    adopted=authority();bound=adopted['expected_publication_gate'];expected={k:bound[k] for k in ('bytes','sha256')}
    need(wanted is None or bytepin(wanted)==expected,'Exact Root-activated final publication gate')
    g=artifact(PUBLICATION_GATE,expected);validate_gate_shape(g);fixed_gates()
    package=rel(g['package']);need(re.fullmatch('publication_package_[a-zA-Z0-9_]+',package) is not None,'Final package directory')
    safe=g['package_safe_files'];need(type(safe) is dict and 0<len(safe)<=MAX_OVERLAY,'Exact bounded package safe map')
    files={PUBLICATION_GATE:expected}
    for name,p in safe.items():safe_public(name);frozen(package+'/'+name,bytepin(p));files[package+'/'+name]=p
    actual=set()
    for path in (A/package).rglob('*'):
        mode=path.lstat().st_mode;need(stat.S_ISDIR(mode) or stat.S_ISREG(mode),'No symlink/special package payload')
        if stat.S_ISREG(mode):actual.add(str(path.relative_to(A/package)))
    need(actual==set(safe),'Every final package file manifested')
    need(safe[g['package_seal_file']]==bytepin(g['package_seal']),'Exact final package seal')
    need(safe[g['portable_source_file']]==PORTABLE,'Accepted portable source exact21804')
    uploads=g['intended_upload_files'];need(type(uploads) is dict and len(uploads)==3 and sorted(Path(n).suffix for n in uploads)==['.pdf','.tex','.zip'],'Exactly final manuscript PDF/source/ZIP')
    need(all(Path(n).name==n and safe[n]==bytepin(p) for n,p in uploads.items()),'Exact final upload file pins')
    need(g['manuscript_source_file'] in uploads and g['manuscript_source_file'].endswith('.tex') and g['manuscript_pdf_file'] in uploads and g['manuscript_pdf_file'].endswith('.pdf'),'Native proof-copy protocol')
    metadata=artifact(package+'/'+g['metadata_file'],safe[g['metadata_file']]);need(metadata['metadata']==g['metadata'] and len(metadata['files'])==3 and {item['path'] for item in metadata['files']}==set(uploads),'Exact final metadata/upload manifest')
    for event in g['whole_package_review_events']:
        directory=rel(event['directory']);rs=event['safe_files'];need(type(rs) is dict and event['report_file'] in rs and event['report_pin']==rs[event['report_file']],'Bound whole-package report')
        for name,p in rs.items():safe_public(directory+'/'+name);frozen(directory+'/'+name,bytepin(p));files[directory+'/'+name]=p
        af=rel(event['Root_acceptance_file']);ar=artifact(af,event['Root_acceptance_pin']);files[af]=event['Root_acceptance_pin']
        need(ar['schema']=='pr206-root-whole-package-review-acceptance-v1' and ar['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and ar['accepted'] is True and ar['review_accepted'] is True and ar['PR']==206 and ar['original_head']==HEAD and ar['NEW_whole_package_reviews_completed']==event['review_number'],'Actual Root whole-package acceptance')
        need(ar['review_event']=={k:v for k,v in event.items() if k not in ('Root_acceptance_file','Root_acceptance_pin')},'Exact Root-accepted event envelope')
        frozen(rel(event['reviewed_package'])+'/'+g['package_seal_file'],event['reviewed_package_seal'])
    need(ar['review_cycle_repairs_required_now'] is False,'All final whole-package findings resolved')
    other=g['other_safe_files'];need(type(other) is dict and all(other.get(name)==p for name,p in FIXED_GATES.items()),'All current fixed Root gates carried')
    for name,p in other.items():safe_public(name);need(name!=PUBLICATION_GATE,'No recursive publication gate');frozen(name,bytepin(p));files[name]=p
    for name in SOURCE_PUBLIC:files[D.name+'/'+name]=pin(frozen(D.name+'/'+name))
    files[SOURCE_ADOPTION]=copy.deepcopy(_authority_pin)
    need(len(files)<=MAX_OVERLAY-20,'Bounded final public overlay')
    return g,files


def tracker_row(g,doi):
    return ['k903,a: focal inversion signed-area product (AMR-050-0062)','','https://doi.org/'+doi,g['metadata']['title']+'. '+CLAIM+' '+CREDIT+' '+EFFORT+' Extensive AI; unrefereed; no conventional human peer review. PR206.']


def ready_context():
    state=actual('ready');a=state['receipt'];g,files=gate(a['facts']['Root_publication_gate_pin'])
    need(a['facts']['actual_publication_verified'] is False and a['facts']['actual_tracker_row_verified'] is False and a['facts']['completed'] is False,'Ready90 carries no future operational facts')
    for name,p in files.items():need(state['mapping']['selected_files'][CASE+name]==bpin(frozen(name,p)),'Actual ready complete final materials')
    return g,{'gate_pin':a['facts']['Root_publication_gate_pin'],'ready_pointer_pin':pin(read(POINTER['ready'])),'ready_acceptance_pin':pin(read(state['directory']+'ACCEPTANCE.json')),'checkpoint_commit':a['checkpoint_commit'],'package':g['package'],'package_seal':g['package_seal'],'manifest_pin':pin(frozen(g['package']+'/'+g['metadata_file']))}


def operations():
    g,context=ready_context();p=artifact('ROOT_PUBLICATION_RECEIPT.json');t=artifact('ROOT_TRACKER_RECEIPT.json')
    need(p.get('schema')=='pr206-root-publication-receipt-v1' and p.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and p.get('PR')==206 and p.get('state')=='published','Actual Root publication receipt')
    need(all(p[k] is True for k in ('actual_publication_verified','metadata_exact_verified','all_three_public_download_SHA256_verified')),'Actual publication/readback flags')
    need(p['context']==context and p['package']==g['package'] and p['gate_sha256']==context['gate_pin']['sha256'] and p['metadata_normalizations']==[],'Exact actual publication context')
    need(enc({key:p[key] for key in ('metadata','package_safe_files','intended_upload_files')})==enc({key:g[key] for key in ('metadata','package_safe_files','intended_upload_files')}) and p['original_head']==HEAD and type(p['problem_id']) is int and p['problem_id']==5100062,'Exact copied publication metadata/package/native identity facts')
    need(type(p['id']) is int and p['id']>0 and p['doi']=='10.5281/zenodo.'+str(p['id']) and p['doi_url']=='https://doi.org/'+p['doi'] and p['record_url']=='https://zenodo.org/records/'+str(p['id']),'Actual record/DOI, not proposed values')
    need(p['doi_resolution']['http_status']==200 and p['doi_resolution']['status']=='resolved','Actual DOI resolution')
    need(len(p['files'])==3 and {x['name']:{'bytes':x['size'],'sha256':x['sha256']} for x in p['files']}==g['intended_upload_files'],'Exact actual upload readback')
    need(len(p['public_downloads'])==3 and {x['name']:{'bytes':x['bytes'],'sha256':x['sha256']} for x in p['public_downloads']}==g['intended_upload_files'] and all(x['url'].startswith('https://') and x['final_url'].startswith('https://') for x in p['public_downloads']),'Exact actual public downloads')
    need(t.get('schema')=='pr206-root-tracker-receipt-v1' and t.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and t.get('PR')==206,'Actual Root tracker receipt')
    need(all(t[k] is True for k in ('actual_tracker_row_verified','own_row_readback_verified','foreign_rows_retained','original_preappend_baseline_retained','two_fresh_full_prechecks','two_fresh_full_readbacks','RAW_INSERT_ROWS','B_intentionally_blank_no_verified_chat_share_URL')),'Actual tracker prechecks/readback')
    need(t['doi']==p['doi'] and t['context']==context and t['publication_receipt']==pin(frozen('ROOT_PUBLICATION_RECEIPT.json')) and t['gate_sha256']==context['gate_pin']['sha256'] and t['row']==tracker_row(g,p['doi']),'Exact tracker row/DOI/context')
    need(enc(t['publication_facts'])==enc({key:p[key] for key in ('id','doi','doi_url','record_url','metadata','package','package_safe_files','intended_upload_files','original_head','problem_id')}),'Exact tracker copied publication facts subset')
    need(t['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and t['sheet_gid']==1254632077 and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",t['range']) is not None,'Actual target sheet/range')
    baseline=t['original_preappend_baseline'];need(set(baseline)=={'file','pin','row_count','counter_sha256'} and type(baseline['row_count']) is int and baseline['row_count']>0 and re.fullmatch('[0-9a-f]{64}',baseline['counter_sha256']) is not None,'Tracker retained original baseline')
    bytepin(baseline['pin']);return g,p,t,context


def metadata_ack(record):
    need(type(record) is dict and set(record)=={'path','bytes','sha256'} and record['path']=='ROOT_PR_METADATA_ACKNOWLEDGEMENT_01.json','Explicit future actual metadata acknowledgement')
    value=artifact(record['path'],{k:record[k] for k in ('bytes','sha256')});g,p,t,context=operations()
    need(value.get('schema')=='pr206-root-pr-metadata-acknowledgement-v1' and value.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and value.get('accepted') is True and value.get('PR')==206 and value.get('original_head')==HEAD,'Actual metadata acknowledgement identity')
    need(all(value[k] is True for k in ('Root_authorized_final_metadata_update','actual_PR_readback_verified','acknowledged_actual_PR_open_nondraft','original_native_range_delta_unchanged')),'Root final metadata update only after actual publication/tracker')
    need(value['publication_receipt_pin']==pin(frozen('ROOT_PUBLICATION_RECEIPT.json')) and value['tracker_receipt_pin']==pin(frozen('ROOT_TRACKER_RECEIPT.json')) and value['publication_gate_pin']==context['gate_pin'],'Actual metadata/publication context')
    need(value['expected_base_ref']=='main' and value['expected_title']==g['metadata']['title'] and type(value['expected_title']) is str,'Final Root-approved title')
    bytepin(value['expected_body_pin']);return value


def original_native(h):
    custody,old=originals();q,base,head=queue_rows()
    commit=api(h,'git/commits/'+HEAD);fork=api(h,'git/commits/'+FORK)
    need(commit['sha']==HEAD and commit['tree']['sha']==HEAD_TREE and [p['sha'] for p in commit['parents']]==[HEAD_PARENT],'Original native HEAD commit identity')
    for name,raw in old.items():need(h.lookup(HEAD_TREE,NATIVE+name)==('100644','blob',bpin(raw)['git_blob']),'Original21 immutable native leaves')
    need(h.lookup(HEAD_TREE,Q)==('100644','blob',q['original_QUEUE_blob']['git_blob']) and h.lookup(fork['tree']['sha'],Q)==('100644','blob',q['base_QUEUE_blob']['git_blob']),'Original BASE/HEAD QUEUE objects')
    delta=h.changed_leaves(fork['tree']['sha'],HEAD_TREE)
    need(type(delta) is set and delta=={NATIVE+name for name in old}|{Q} and len(delta)==22,'Original authored22 only; never declared-base foreign39')
    validate_cache(h)


def native_leaves(h,tree,prefix):
    rel(prefix.rstrip('/'));entry=h.lookup(tree,prefix.rstrip('/'))
    if entry is None:return {}
    need(entry[:2]==('040000','tree'),'Regular native attempt directory')
    result={};authenticated={};active=set();budget={'work':0,'visits':0}
    def descend(oid,path,depth):
        need(depth<=MAX_NATIVE_DEPTH and oid not in active,'Bounded acyclic native-tree depth');rel(path.rstrip('/'))
        need(budget['visits']<MAX_NATIVE_WORK,'Bounded total native-tree visits');budget['visits']+=1
        if oid in authenticated:rows=authenticated[oid]
        else:
            response=api(h,'git/trees/'+oid);rows=response['tree']
            need(response['sha']==oid and response['truncated'] is False and type(rows) is list and len(rows)<=MAX_CHANGED,'Complete bounded nonrecursive native tree')
        # Charge the GLOBAL expanded-row budget before validating/storing or
        # descending this occurrence; shared DAG children cannot evade it.
        need(len(rows)<=MAX_NATIVE_WORK-budget['work'],'Incremental global native work budget');budget['work']+=len(rows)
        if oid not in authenticated:
            seen=set();serialized=[]
            for row in rows:
                name=row['path'];need(type(name) is str and name and name not in ('.','..') and '/' not in name and '\0' not in name and name not in seen and len(name.encode())<=255,'Bounded native tree entry name');seen.add(name)
                kind=row['type'];mode=row['mode'];need((mode,kind) in (('040000','tree'),('100644','blob')) and type(row['sha']) is str and re.fullmatch('[0-9a-f]{40}',row['sha']) is not None,'Native current tree entry identity')
                rel(path+name);key=name.encode()+(b'/' if kind=='tree' else b'');payload=mode.lstrip('0').encode()+b' '+name.encode()+b'\0'+bytes.fromhex(row['sha']);serialized.append((key,payload))
            raw=b''.join(value for key,value in sorted(serialized));need(len(raw)<=MAX_BYTES and hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid,'Native nonrecursive tree SHA1 before descent')
            authenticated[oid]=rows
        active.add(oid)
        try:
            for row in rows:
                name=row['path'];rel(path+name)
                if row['type']=='tree':descend(row['sha'],path+name+'/',depth+1)
                else:
                    need(len(result)<MAX_CHANGED,'Incremental global native leaf budget')
                    need(path+name not in result,'Unique complete native leaf path')
                    result[path+name]=(row['mode'],row['type'],row['sha'])
        finally:active.remove(oid)
    descend(entry[2],prefix,0)
    return result


def entries(h,out):
    result=[]
    for path,raw in sorted(out.items()):
        rel(path);pin(raw)
        try:text=raw.decode('utf-8')
        except UnicodeDecodeError:text=None
        if text is None or Path(path).suffix in ('.pdf','.zip'):
            oid=api(h,'git/blobs','POST',{'encoding':'base64','content':base64.b64encode(raw).decode()})['sha'];need(oid==bpin(raw)['git_blob'],'Created binary native blob identity');result.append({'path':path,'mode':'100644','type':'blob','sha':oid})
        else:result.append({'path':path,'mode':'100644','type':'blob','content':text})
    return result


def local_preimages(h,parent):
    result={}
    for path in VIEWS:
        remote=body(h,path,parent);local=optional(path)
        need(type(remote) is bytes and local==remote,'All five local views must match fresh MAIN preimages')
        result[path]=pin(remote)
    return result


def selected(inherited,out,mutable):
    need(type(out) is dict and 0<len(out)<=MAX_OVERLAY and type(mutable) is set,'Bounded overlay/mutable scope')
    for path,raw in out.items():
        need(path in VIEWS or path.startswith(CASE) or path.startswith(NATIVE) or path==Q,'Exact lifecycle overlay scope')
        if path in inherited and path not in mutable:need(bpin(raw)==inherited[path],'Inherited selected immutable identity overwrite '+path)
    result={**inherited,**{path:bpin(raw) for path,raw in out.items()}};digest(result);return result


def driver(phase):
    need(phase in PHASES and phase in _drivers,'Configured phase driver required');return _drivers[phase]


def bind(phase,name,argument):
    authority();d=driver(phase);data=d['inputs'](argument);g=generation(name)
    need(not os.path.lexists(ROOT/g),'Fresh generation required')
    target=_path(g.rstrip('/'));target.mkdir();_fsync_dir(target.parent)
    value={'schema':'pr206-lifecycle-binding-v1','UTC':now(),'PR':206,'phase':phase,'argument':argument,'source_adoption_pin':copy.deepcopy(_authority_pin),'data':data}
    save(g+'INPUT_BINDINGS.json',value);return value


def binding(phase,name):
    _generation_clean(generation(name))
    value=obj(generation(name)+'INPUT_BINDINGS.json')
    need(value['schema']=='pr206-lifecycle-binding-v1' and value['PR']==206 and value['phase']==phase and value['source_adoption_pin']==_authority_pin,'Exact phase/source binding')
    need(value['data']==driver(phase)['inputs'](value['argument']),'Phase prerequisite binding drift')
    return value['data']


def base_for(phase,data):
    if phase=='ready':return baseline_custody()
    state=actual(PHASES[phase][2]);a=state['receipt'];bound=data['predecessor']
    need(bound=={'phase':PHASES[phase][2],'directory':state['directory'],'acceptance_pin':pin(read(state['directory']+'ACCEPTANCE.json')),'pointer_pin':pin(read(POINTER[PHASES[phase][2]]))},'Exact actual predecessor acceptance/pointer')
    return {'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':state['mapping']['selected_files']}


def message(phase,selected_digest):
    return 'PR206 '+phase+str(PHASES[phase][1])+': qualified focal-inversion verification lifecycle\n\nOriginalHEAD '+HEAD+'; native tree scope only; no inherited foreign39 import. '+('Conditional completion postimage; actual own full acceptance/local five sync/pointer required before cursor207.' if phase=='completion' else '48completed32published,last205,cursor206,advancefalse; incomplete.')+'\nSelected-map SHA256: '+selected_digest


def facts(phase,data,actual_accepted=False):return driver(phase)['facts'](data,actual_accepted)


def check_candidate(phase,r,commit,parent_tree,expected,out,changes,actual_changes,parents):
    need(r['schema']=='pr206-lifecycle-preparation-v1' and r['phase']==phase and r['PR']==206 and r['case_percent']==PHASES[phase][1] and r['original_head']==HEAD,'Prepared phase identity')
    need(r['selected_files']==expected and r['selected_map_sha256']==digest(expected) and r['overlay_paths']==sorted(out),'Full prepared expected identities/body scope')
    need(commit['sha']==r['commit'] and [p['sha'] for p in commit['parents']]==parents and commit['tree']['sha']==r['tree'] and commit['message']==message(phase,digest(expected)) and parent_tree==r['parent_tree'],'Exact phase parents/tree/message')
    need(type(actual_changes) is set and len(actual_changes)<=MAX_CHANGED and changes==actual_changes and r['changed_paths']==sorted(changes) and changes<=set(out),'Full fresh-parent foreign changed-leaf scope')
    need(Q not in changes or phase=='merge','Only95 may change own QUEUE row')
    need(not any(path.startswith(ALL_NATIVE) and not path.startswith(NATIVE) for path in changes),'No foreign native attempt changes')
    if phase=='ready':need(not any(path.startswith(NATIVE) for path in changes),'Ready90 no native attempt write')


def _prepared(phase,name):
    c,h=runtime();data=binding(phase,name);d=driver(phase);g=generation(name);r=obj(g+'PREPARATION.json');base=base_for(phase,data)
    need(r['source_adoption_pin']==_authority_pin and enc(r['facts'])==enc(facts(phase,data,False)),'Prepared exact authority/facts')
    need(api(h,'compare/'+base['commit']+'...'+r['expected_main'])['status'] in ('identical','ahead'),'True fresh parent retains actual predecessor')
    inherited,ack=reconcile(c,h,base,r['expected_main'],d['queue_before'](data),r['UTC']);need(ack==obj(g+'FOREIGN_QUEUE_RECONCILIATION.json'),'Exact original parent QUEUE reconciliation')
    out=d['overlay'](h,r['expected_main'],r['UTC'],data,name);out[g+'INPUT_BINDINGS.json']=read(g+'INPUT_BINDINGS.json');out[g+'FOREIGN_QUEUE_RECONCILIATION.json']=read(g+'FOREIGN_QUEUE_RECONCILIATION.json')
    expected=selected(inherited,out,d['mutable'](data));commit=api(h,'git/commits/'+r['commit']);parent_tree=api(h,'git/commits/'+r['expected_main'])['tree']['sha']
    need(c.selected_current(h,r['commit'],expected,parent_tree)==r['tree'] and c.selected_digest(expected)==digest(expected),'Every selected candidate native identity')
    changes={path for path,p in expected.items() if h.lookup(parent_tree,path)!=('100644','blob',p['git_blob'])}
    check_candidate(phase,r,commit,parent_tree,expected,out,changes,h.changed_leaves(parent_tree,r['tree']),d['parents'](r['expected_main']))
    need(set(r['local_five_expected_preimages'])==set(VIEWS),'All five prepared preimage keys')
    for path in VIEWS:need(r['local_five_expected_preimages'][path]==pin(body(h,path,r['expected_main'])),'Exact native-parent local preimage binding')
    if phase!='ready':
        own={path:('100644','blob',bpin(raw)['git_blob']) for path,raw in out.items() if path.startswith(NATIVE)}
        need(native_leaves(h,r['tree'],NATIVE)==own,'Complete current native path set and every native identity')
        if phase=='merge':need(native_leaves(h,parent_tree,NATIVE)=={},'Original native directory absent before safe merge95')
    original_native(h);validate_cache(h)
    return c,h,data,d,g,r,out,expected


def prepare(phase,name):
    c,h=runtime();data=binding(phase,name);d=driver(phase);g=generation(name);need(optional(g+'PREPARATION.json') is None,'Fresh preparation generation required');base=base_for(phase,data)
    parent=api(h,'git/ref/heads/main')['object']['sha'];need(api(h,'compare/'+base['commit']+'...'+parent)['status'] in ('identical','ahead'),'Fresh MAIN lacks actual predecessor')
    stamp=now();inherited,ack=reconcile(c,h,base,parent,d['queue_before'](data),stamp);parent_tree=c.selected_current(h,parent,inherited,base['tree']);validate_cache(h);original_native(h);d['original'](h,data,False,None)
    local=local_preimages(h,parent);out=d['overlay'](h,parent,stamp,data,name)
    need(api(h,'git/ref/heads/main')['object']['sha']==parent,'Stale MAIN lease; fresh generation required')
    save(g+'FOREIGN_QUEUE_RECONCILIATION.json',ack);out[g+'INPUT_BINDINGS.json']=read(g+'INPUT_BINDINGS.json');out[g+'FOREIGN_QUEUE_RECONCILIATION.json']=read(g+'FOREIGN_QUEUE_RECONCILIATION.json');expected=selected(inherited,out,d['mutable'](data))
    tree=api(h,'git/trees','POST',{'base_tree':parent_tree,'tree':entries(h,out)})['sha'];need(api(h,'git/ref/heads/main')['object']['sha']==parent,'Lease stale after tree; abandon generation')
    parents=d['parents'](parent);commit=api(h,'git/commits','POST',{'tree':tree,'parents':parents,'message':message(phase,digest(expected))})['sha']
    value={'schema':'pr206-lifecycle-preparation-v1','UTC':stamp,'PR':206,'phase':phase,'case_percent':PHASES[phase][1],'original_head':HEAD,'expected_main':parent,'parent_tree':parent_tree,'tree':tree,'commit':commit,'selected_files':expected,'selected_map_sha256':digest(expected),'overlay_paths':sorted(out),'changed_paths':sorted(path for path,p in expected.items() if h.lookup(parent_tree,path)!=('100644','blob',p['git_blob'])),'local_five_expected_preimages':local,'source_adoption_pin':copy.deepcopy(_authority_pin),'facts':facts(phase,data,False),'conditional_completion_postimage':phase=='completion','actual_program_counts_before_acceptance':dict(BASE_COUNTS),'MAIN_moved':False}
    save(g+'PREPARATION.json',value);_prepared(phase,name)
    need(api(h,'git/ref/heads/main')['object']['sha']==parent,'Lease stale after full verification; fresh generation required')
    save(g+'ROOT_PRE_MOVE_VERIFICATION.json',{'UTC':now(),'PR':206,'phase':phase,'commit':commit,'expected_main':parent,'parents':parents,'observed_MAIN':parent,'exact_parents_fullforeign_everyselected_verified':True,'actual_MAIN_acceptance':False})
    return {'expected_main':parent,'commit':commit,'tree':tree,'parents':parents,'selected_files':len(expected),'MAIN_moved':False}


def verify(phase,name):
    c,h,data,d,g,r,out,expected=_prepared(phase,name)
    need(api(h,'git/ref/heads/main')['object']['sha']==r['expected_main'],'Stale MAIN lease; fresh generation required')
    need(local_preimages(h,r['expected_main'])==r['local_five_expected_preimages'],'All five preimages before external CAS');d['original'](h,data,False,None)
    return {'verified':True,'phase':phase,'expected_main':r['expected_main'],'commit':r['commit'],'tree':r['tree'],'parents':d['parents'](r['expected_main']),'no_ref_mutation':True}


def _native_state(c,h,phase,data,r,expected,main):
    need(api(h,'compare/'+r['commit']+'...'+main)['status'] in ('identical','ahead'),'Checkpoint absent from receipted actual MAIN')
    current,ack=reconcile(c,h,{'commit':r['commit'],'tree':r['tree'],'selected_files':expected},main,driver(phase)['queue_after'](data),now())
    tree=c.selected_current(h,main,current,r['tree']);native=api(h,'git/commits/'+main);need(native['sha']==main and native['tree']['sha']==tree,'Native actual MAIN-to-tree identity');validate_cache(h)
    return tree,current,ack


def accept(phase,name):
    c,h,data,d,g,r,out,expected=_prepared(phase,name);main=api(h,'git/ref/heads/main')['object']['sha'];tree,current,ack=_native_state(c,h,phase,data,r,expected,main);observed_pr=d['original'](h,data,True,r['commit'] if phase=='merge' else None)
    need(api(h,'git/ref/heads/main')['object']['sha']==main,'MAIN advanced during actual acceptance; revalidate')
    mapping={'selected_files':current,'selected_map_sha256':digest(current),'foreign_QUEUE_reconciliation_after_checkpoint':ack};raw=enc(mapping);atomic(g+'ACCEPTANCE_CURRENT_SELECTED_MAP.json',raw,None)
    phase_facts=facts(phase,data,True)
    receipt={'schema':'pr206-lifecycle-actual-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','UTC':now(),'PR':206,'phase':phase,'accepted':True,'case_percent':PHASES[phase][1],'checkpoint_commit':r['commit'],'parents':d['parents'](r['expected_main']),'sole_parent':None if phase=='merge' else r['expected_main'],'main_observed':main,'actual_tree':tree,'original_head':HEAD,'selected_files':len(current),'selected_map_sha256':digest(expected),'actual_current_selected_map_sha256':digest(current),'actual_current_map_file':pin(raw),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'original_native_custody_retained':True,'actual_original_PR_head':observed_pr['head']['sha'],'actual_original_PR_is_draft':observed_pr['draft'],'actual_original_PR_state':observed_pr['state'],'facts':phase_facts,**{key:phase_facts[key] for key in RECEIPT_ALIASES}}
    save(g+'ACCEPTANCE.json',receipt);return receipt


def check_acceptance(phase,receipt,mapping,r,expected,phase_facts,parents):
    fields={'schema','evidence_scope','UTC','PR','phase','accepted','case_percent','checkpoint_commit','parents','sole_parent','main_observed','actual_tree','original_head','selected_files','selected_map_sha256','actual_current_selected_map_sha256','actual_current_map_file','every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','original_native_custody_retained','actual_original_PR_head','actual_original_PR_is_draft','actual_original_PR_state','facts'}|RECEIPT_ALIASES
    need(type(receipt) is dict and set(receipt)==fields and type(mapping) is dict and set(mapping)=={'selected_files','selected_map_sha256','foreign_QUEUE_reconciliation_after_checkpoint'},'Exact phase acceptance/map schema')
    need(receipt['schema']=='pr206-lifecycle-actual-acceptance-v1' and receipt['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and receipt['accepted'] is True and type(receipt['PR']) is int and receipt['PR']==206 and receipt['phase']==phase and receipt['case_percent']==PHASES[phase][1],'Own actual lifecycle acceptance')
    need(receipt['parents']==parents and receipt['sole_parent']==(None if phase=='merge' else r['expected_main']) and receipt['checkpoint_commit']==r['commit'] and receipt['original_head']==HEAD,'Exact original HEAD/phase parents')
    need(all(type(receipt[k]) is str and re.fullmatch('[0-9a-f]{40}',receipt[k]) is not None for k in ('checkpoint_commit','main_observed','actual_tree','original_head')),'Native acceptance SHA fields')
    need(type(receipt['UTC']) is str and datetime.datetime.fromisoformat(receipt['UTC']).tzinfo is not None,'Actual timestamp');bytepin(receipt['actual_current_map_file'])
    need(all(receipt[k] is True for k in ('every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','original_native_custody_retained')) and enc(receipt['facts'])==enc(phase_facts),'Full actual guards and exact Root-gated phase facts')
    need(all(receipt[key]==phase_facts[key] and type(receipt[key]) is type(phase_facts[key]) for key in RECEIPT_ALIASES),'Exact top-level ready/operation/counter aliases')
    need(receipt['actual_original_PR_head']==HEAD and receipt['actual_original_PR_is_draft'] is (phase=='ready') and receipt['actual_original_PR_state']==('open' if phase=='ready' else 'closed'),'Freshly authenticated actual original PR facts')
    accepted=mapping['selected_files'];digest(expected)
    need(Q in expected and type(accepted) is dict and set(accepted)==set(expected) and type(receipt['selected_files']) is int and receipt['selected_files']==len(expected)==len(accepted),'Exact complete prepared selected path set/count')
    need(all(accepted[path]==p for path,p in expected.items() if path!=Q),'Every non-QUEUE accepted pin equals complete prepared expected')
    need(receipt['selected_map_sha256']==digest(expected) and digest(accepted)==mapping['selected_map_sha256']==receipt['actual_current_selected_map_sha256'],'Full selected map digests')


def _accepted(phase,name):
    c,h,data,d,g,r,out,expected=_prepared(phase,name);receipt=obj(g+'ACCEPTANCE.json');mapping=obj(g+'ACCEPTANCE_CURRENT_SELECTED_MAP.json',receipt['actual_current_map_file'])
    check_acceptance(phase,receipt,mapping,r,expected,facts(phase,data,True),d['parents'](r['expected_main']))
    # Reconstruct from the original checkpoint and full expected map, never from
    # supplied receipt protection. This closes the historical custody-v1 gap.
    tree,reconstructed,ack=_native_state(c,h,phase,data,r,expected,receipt['main_observed'])
    need(tree==receipt['actual_tree'] and reconstructed==mapping['selected_files'],'Native receipted MAIN/tree and complete independently reconstructed map')
    recorded=mapping['foreign_QUEUE_reconciliation_after_checkpoint'];need(type(recorded) is dict and {k:v for k,v in recorded.items() if k!='UTC'}=={k:v for k,v in ack.items() if k!='UTC'},'Original-checkpoint-to-receipted-MAIN protected QUEUE continuity')
    return c,h,data,d,g,r,out,expected,receipt,mapping


def _fresh_accepted(phase,name):
    c,h,data,d,g,r,out,expected,receipt,mapping=_accepted(phase,name);main=api(h,'git/ref/heads/main')['object']['sha']
    need(api(h,'compare/'+receipt['main_observed']+'...'+main)['status'] in ('identical','ahead'),'Fresh MAIN retains authenticated receipt ancestry')
    current,ack=reconcile(c,h,{'commit':receipt['main_observed'],'tree':receipt['actual_tree'],'selected_files':mapping['selected_files']},main,d['queue_after'](data),now())
    c.selected_current(h,main,current,receipt['actual_tree']);validate_cache(h);original_native(h);d['original'](h,data,True,r['commit'] if phase=='merge' else None)
    need(api(h,'git/ref/heads/main')['object']['sha']==main,'MAIN advanced during fresh actual checks')
    return c,h,data,d,g,r,out,receipt,main,ack


def sync(phase,name):
    with WriterOwnership(generation(name)):
        c,h,data,d,g,r,out,receipt,main,ack=_fresh_accepted(phase,name)
        rows=sync_images([(path,r['local_five_expected_preimages'][path],out[path]) for path in VIEWS],g)
        need(api(h,'git/ref/heads/main')['object']['sha']==main,'MAIN advanced during sync; no success receipt')
        result={'schema':'pr206-lifecycle-five-sync-v1','UTC':now(),'PR':206,'phase':phase,'actual_checkpoint':r['commit'],'acceptance_pin':pin(read(g+'ACCEPTANCE.json')),'all_five_local_files_match_actual_checkpoint':True,'files':rows,'fresh_MAIN_revalidated':main,'facts':facts(phase,data,True)}
        save(g+'LOCAL_GLOBAL_FIVE_SYNC.json',result);return result


def pointer(phase,name):
    with WriterOwnership(generation(name)):
        c,h,data,d,g,r,out,receipt,main,ack=_fresh_accepted(phase,name);sy=obj(g+'LOCAL_GLOBAL_FIVE_SYNC.json')
        need(sy['schema']=='pr206-lifecycle-five-sync-v1' and sy['PR']==206 and sy['phase']==phase and sy['actual_checkpoint']==r['commit'] and sy['acceptance_pin']==pin(read(g+'ACCEPTANCE.json')) and sy['all_five_local_files_match_actual_checkpoint'] is True and sy['facts']==facts(phase,data,True),'Own actual full acceptance and successful complete five-sync')
        need(sy['files']==[{'path':path,'postimage':pin(out[path])} for path in VIEWS],'Exact five sync postimage pins')
        for path in VIEWS:need(read(path)==out[path],'All five readonly actual postimages before pointer')
        need(api(h,'git/ref/heads/main')['object']['sha']==main,'MAIN changed before pointer')
        value={'schema':'pr206-lifecycle-actual-pointer-v1','UTC':now(),'PR':206,'phase':phase,'directory':D.name+'/'+name,'checkpoint_commit':r['commit'],'main_observed':receipt['main_observed'],'fresh_MAIN_revalidated_before_pointer':main,'acceptance_pin':pin(read(g+'ACCEPTANCE.json')),'Root_recorded_only_after_actual_full_scope_acceptance':True}
        atomic(POINTER[phase],enc(value),None,g);return value


def actual(phase):
    need(phase in PHASES and phase not in _validation_stack and len(_validation_stack)<4,'Bounded acyclic actual phase chain')
    _validation_stack.append(phase)
    try:
        p=decode(read(POINTER[phase]));need(p['schema']=='pr206-lifecycle-actual-pointer-v1' and p['PR']==206 and p['phase']==phase and p['Root_recorded_only_after_actual_full_scope_acceptance'] is True,'Actual predecessor pointer')
        directory=rel(p['directory']);need(directory.startswith(D.name+'/') and len(directory.split('/'))==2,'Own phase generation directory');name=directory.split('/')[1]
        c,h,data,d,g,r,out,expected,a,mapping=_accepted(phase,name)
        need(g==CASE+directory+'/' and p['checkpoint_commit']==a['checkpoint_commit'] and p['main_observed']==a['main_observed'] and p['acceptance_pin']==pin(read(g+'ACCEPTANCE.json')),'Pointer exact actual acceptance binding')
        sy=obj(g+'LOCAL_GLOBAL_FIVE_SYNC.json');need(sy['phase']==phase and sy['actual_checkpoint']==r['commit'] and sy['acceptance_pin']==p['acceptance_pin'] and sy['all_five_local_files_match_actual_checkpoint'] is True and sy['files']==[{'path':path,'postimage':pin(out[path])} for path in VIEWS],'Historical actual predecessor full-sync receipt')
        main=api(h,'git/ref/heads/main')['object']['sha'];need(api(h,'compare/'+a['main_observed']+'...'+main)['status'] in ('identical','ahead'),'Historical actual receipt must remain in fresh MAIN ancestry')
        need(api(h,'git/ref/heads/main')['object']['sha']==main,'MAIN advanced during historical actual ancestry checks')
        # Later phases legitimately replace five views/native presentation. Only
        # immutable receipted MAIN is reconstructed here; active sync/pointer use
        # _fresh_accepted for the fresh complete selected map and mutable PR state.
        return {'directory':g,'receipt':a,'preparation':r,'mapping':mapping,'data':data,'overlay':out}
    finally:_validation_stack.pop()


def project(phase,case,progress,stamp,data):
    need(phase in PHASES and (case['PR'],case['original_head'],case['case_percent'])==(206,HEAD,PHASES[phase][0]) and (progress['current_PR'],progress['current_PR_workflow_percent'])==(206,PHASES[phase][0]),'Actual predecessor view phase')
    need(all(type(case[k]) is type(v) and case[k]==v and type(progress[k]) is type(v) and progress[k]==v for k,v in BASE_COUNTS.items()) and case['completed'] is False,'Incomplete predecessor exact48/32 counters')
    case=copy.deepcopy(case);progress=copy.deepcopy(progress);g=copy.deepcopy(data['gate'])
    case.setdefault('historical_phase_snapshots',[]).append({'UTC':stamp,'phase':PHASES[phase][0],'values':{k:v for k,v in case.items() if k!='historical_phase_snapshots'}})
    retired={k:v for k,v in progress.items() if k.startswith(('current_','next_','conditional_','program_snapshot_')) or k in ('advance_to_next_PR_authorized_now','remaining_current_step','next_step','latest_ordered_intake_record')}
    progress.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':206,'phase':PHASES[phase][0],'values':retired})
    for key in retired:del progress[key]
    phase_facts=facts(phase,data,False);conditional=phase=='completion';postcounts=DONE_COUNTS if conditional else BASE_COUNTS
    status={'ready':'ROOT_FINAL_EXACT_ATTRIBUTED_PACKAGE_READY90','merge':'PUBLISHED_TRACKED_ORIGINAL_HEAD_SAFE_MERGE95_POSTIMAGE','factual':'ACTUAL_MERGE95_ACCEPTED_FACTUAL98_INCOMPLETE_POSTIMAGE','completion':'COMPLETION100_CONDITIONAL_POSTIMAGE_REQUIRES_OWN_ACTUAL_ACCEPTANCE_SYNC_POINTER'}[phase]
    remain='Own actual100 full-scope acceptance, complete local-five sync and actual completion pointer are required before any207 intake.' if conditional else 'Remaining actual publication/tracker, original-HEAD-safe95, incomplete factual98 and separate actual100 steps as applicable; no207 intake.'
    case.update(phase_facts,UTC=stamp,status=status,case_percent=PHASES[phase][1],problem_id=5100062,claim=CLAIM,credit_and_limits=CREDIT,source_facts=SOURCE_FACTS,original_effort=EFFORT,original_author_effort_unverified=True,original_author_commit_count=4,original_archive_files=21,original_native_bytes=55033,declared_PR_base=DECLARED,authenticated_authored_range_base=FORK,theorem_accepted=True,mathematical_result_valid=True,paper_prepared=True,package_prepared=True,publication_package=g['package'],whole_package_review_events=g['whole_package_review_events'],DOI=phase_facts.get('DOI'),record_id=phase_facts.get('record_id'),tracker_range=phase_facts.get('tracker_range'),remaining_required_steps=remain,completed=conditional,completion_postimage_effective_only_after_own_actual_MAIN_acceptance_sync_pointer=conditional)
    case.update(postcounts)
    for key,value in phase_facts.items():progress['current_'+key]=value
    progress.update(UTC=stamp,updated_UTC=stamp,current_PR=206,current_problem_id=5100062,current_status=status,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_QUEUE_effort_cell='1/5',current_original_effort=EFFORT,current_original_archive_files=21,current_original_native_bytes=55033,current_original_author_commit_count=4,current_original_author_effort_unverified=True,current_PR_workflow_percent=PHASES[phase][1],current_workflow_estimate_percent=PHASES[phase][1],current_completed=conditional,current_exact_claim=CLAIM,current_credit_and_limits=CREDIT,current_source_facts=SOURCE_FACTS,current_theorem_accepted=True,current_mathematical_result_valid=True,current_independent_discovery_certified=False,current_literal_simultaneity_established=False,current_historical_novelty_or_firstness_established=False,current_theorem_novelty_cleared=False,current_formula_novelty_cleared=False,current_proof_method_novelty_cleared=False,current_current_openness_established=False,current_verification_code_publication_clearance=True,current_verification_integrity_required_repairs_complete=True,current_whole_package_review_events=g['whole_package_review_events'],current_NEW_whole_publication_package_reviews_completed=len(g['whole_package_review_events']),current_NEW_whole_publication_package_review_active=False,current_publication_package_reviews_complete=True,current_record='audits/pr206_5100062/CURRENT_CASE_STATUS.json',remaining_current_step=remain,next_step=remain,next_status_only_intake_performed=False,next_intake_requires_actual_completed_PR=206,next_intake_requires_actual_completion_receipt=True,program_snapshot_semantics='PR206 '+phase+'. '+CREDIT+' '+('49/33,last206,cursor207 are conditional postimage values until own actual100 acceptance/local-five sync/pointer.' if conditional else '48/32,last205,cursor206,advancefalse; incomplete.'),program_snapshot_authority_condition='Only actual accepted native checkpoint and corresponding full local-five sync/pointer supply current authority. No207 intake from a proposal.',current_new_publication_ledger=[] if phase=='ready' else [{'PR':206,'DOI':phase_facts['DOI'],'publication_receipt_pin':data['publication_receipt_pin'],'tracker_receipt_pin':data['tracker_receipt_pin']}],advance_requires_actual100_acceptance_local_five_sync_pointer=True)
    progress.update(postcounts)
    if conditional:
        for key,count in (('fully_completed_eligible_PRs',48),('published_PRs',32)):
            need(type(progress[key]) is list and len(progress[key])==len(set(progress[key]))==count and 206 not in progress[key],'Exact completion list preimage');progress[key].append(206)
        previous={k:v for k,v in progress.items() if k.startswith(('last_completed_','last_published_'))}
        progress.setdefault('historical_prior_completion_metadata',[]).append({'UTC':stamp,'PR':205,'values':previous})
        for key in previous:del progress[key]
        need(type(progress['dated_eligible_total']) is int and progress['dated_eligible_total']>=49,'Dated denominator, no new census')
        fraction=round(4900/progress['dated_eligible_total'],1)
        progress.update(last_completed_PR=206,last_completed_PR_workflow_percent=100,last_completed_original_head=HEAD,last_completed_original_QUEUE_status='claimed_solved',last_completed_original_budget=EFFORT,last_completed_DOI=phase_facts['DOI'],last_completed_tracker_range=phase_facts['tracker_range'],last_completed_priority_clearance=True,last_completed_priority_clearance_scope='Qualified attributed verification only; explicit same-target/same-mechanism overlap, no novelty/firstness/independence certificate',last_completed_record='audits/pr206_5100062/CURRENT_CASE_STATUS.json',last_completed_actual_factual_receipt=data['predecessor']['directory']+'ACCEPTANCE.json',last_published_PR=206,last_published_DOI=phase_facts['DOI'],last_published_tracker_range=phase_facts['tracker_range'],fully_completed_fraction_percent=fraction,workflow_estimate_percent=fraction,workflow_estimate_definition='49/dated historical eligible denominator completed,33published; conditional until own actual100 acceptance/sync/pointer; no new eligibility census.')
    need(phase!='factual' or (case['completed'] is False and all(case[k]==v and progress[k]==v for k,v in BASE_COUNTS.items())),'Factual98 is strictly incomplete')
    return case,progress


def views_overlay(h,parent,stamp,phase,data):
    case,progress=project(phase,decode(body(h,VIEWS[0],parent)),decode(body(h,P+'CURRENT_PROGRESS.json',parent)),stamp,data)
    out={VIEWS[0]:enc(case),P+'CURRENT_PROGRESS.json':enc(progress)}
    note=('\n'+stamp+' — PR206 '+phase+' '+str(PHASES[phase][1])+'%. '+CLAIM+' '+CREDIT+' '+EFFORT+' '+case['remaining_required_steps']+'\n').encode()
    for path in (VIEWS[1],P+'CURRENT_PROGRESS.md',P+'RESEARCH_LOG.md'):out[path]=body(h,path,parent)+note
    return out
