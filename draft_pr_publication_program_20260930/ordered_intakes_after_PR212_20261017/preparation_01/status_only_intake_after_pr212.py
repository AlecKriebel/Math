"""INACTIVE ordered preserved-QUEUE status intake after actual PR212 administrative skip.
No mathematical body review or PR-opening-transaction/author-turn inference.
Import is inert; execution is gated by an externally pinned actual Root receipt.
"""
import argparse,base64,datetime,hashlib,json,math,os,re,selectors,stat,subprocess,sys,time,types
from pathlib import Path
SOURCE_DIR=Path(__file__).absolute().parent
HERE=SOURCE_DIR.parent
PROGRAM=HERE.parent
PRIOR=PROGRAM/'audits/pr212_30005310'
BASELINE_PIN={'bytes':853,'sha256':'b4fe8858faebc0f14ab956d8849af28072837807f3fc87e85a2abe356bfb2f1e'}
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
REGISTRY=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/claimed_solved_scope_20261003/LIVE_DRAFT_ELIGIBILITY_REGISTRY.json')
REGISTRY_PIN={'bytes':572299,'sha256':'f2f9e56fbdee7dac6121bd40c1faee16ec22f6ae4e172f613f1c533157f68c33'}
SCHEMA='ordered-preserved-submission-status-only-intake-after-pr212-v1'
MAX_BODY=4000000
ACTIVE_PR=None
REQUESTS=[]
TREES={}
FAILED=False

def need(value,message):
    if type(value) is not bool or not value:raise RuntimeError(message)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def hexid(value,n=40):return type(value) is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',value) is not None
def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b
def decode(raw):
    def pairs(rows):
        out={}
        for key,value in rows:need(key not in out,'Duplicate JSON key');out[key]=value
        return out
    def finite(value):
        out=float(value);need(math.isfinite(out),'Nonfinite JSON number');return out
    return json.loads(raw,object_pairs_hook=pairs,parse_float=finite,parse_constant=lambda _:need(False,'Nonfinite JSON constant'))
def bytepin(value):
    need(type(value) is dict and set(value)=={'bytes','sha256'} and type(value['bytes']) is int and 1<=value['bytes']<=MAX_BODY and hexid(value['sha256'],64),'Exact bounded external byte pin')
    return value

def regular(path,immutable=True):
    need(path.is_absolute() and path.resolve()==path,'Canonical immutable record required')
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY);parents=[]
    try:
        for part in path.parts[1:-1]:
            nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);parents.append(fd);fd=nxt
        leaf=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            before=os.fstat(leaf);need(stat.S_ISREG(before.st_mode) and (not immutable or stat.S_IMODE(before.st_mode)==0o444) and before.st_size<=MAX_BODY,'Bounded immutable ordinary file')
            raw=os.read(leaf,MAX_BODY+1)
            identity=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode)
            need(identity(before)==identity(os.fstat(leaf))==identity(os.stat(path.name,dir_fd=fd,follow_symlinks=False)) and len(raw)==before.st_size,'Immutable record changed during read')
            need(path.resolve()==path,'Immutable record ancestor changed');return raw
        finally:os.close(leaf)
    finally:
        os.close(fd)
        for ancestor in reversed(parents):os.close(ancestor)

def api_argv(num,route):
    need(type(num) is int and 213<=num<=10000,'Selected ordered PR number')
    paged=r'\?page=(?:[1-9]|1[0-9]|20)&per_page=100'
    allowed=route=='pulls/'+str(num) or re.fullmatch(r'(?:pulls/'+str(num)+r'/commits|issues/'+str(num)+r'/timeline)'+paged,route) is not None or re.fullmatch(r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',route) is not None or re.fullmatch(r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}',route) is not None
    need(allowed,'Only selected PR metadata/timeline and native GET routes allowed')
    return [GH,'api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/'+route]

def bounded_get(argv):
    process=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    selector=selectors.DefaultSelector();out=bytearray();err=bytearray();deadline=time.monotonic()+120
    try:
        for stream,label in ((process.stdout,'stdout'),(process.stderr,'stderr')):
            os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,label)
        while selector.get_map():
            left=deadline-time.monotonic();need(left>0,'Bounded GET timeout')
            for key,_ in selector.select(min(left,0.25)):
                chunk=os.read(key.fileobj.fileno(),65536)
                if not chunk:selector.unregister(key.fileobj);key.fileobj.close();continue
                target,cap=(out,12000000) if key.data=='stdout' else (err,65536)
                need(len(target)+len(chunk)<=cap,'Bounded GET output exceeded');target.extend(chunk)
        left=deadline-time.monotonic();need(left>0,'Bounded GET timeout')
        return types.SimpleNamespace(returncode=process.wait(timeout=left),stdout=bytes(out),stderr=bytes(err))
    except BaseException:
        if process.poll() is None:process.kill()
        process.wait(timeout=5);raise
    finally:
        selector.close()
        for stream in (process.stdout,process.stderr):
            if not stream.closed:stream.close()

def api(route):
    global FAILED
    need(not FAILED and len(REQUESTS)<100,'GET attempt stopped or request bound reached')
    argv=api_argv(ACTIVE_PR,route)
    try:
        result=bounded_get(argv)
        REQUESTS.append({'method':'GET','hostname':'github.com','route':route,'exit':result.returncode,'response_pin':pin(result.stdout),'stderr_pin':pin(result.stderr)})
        need(result.returncode==0,'GitHub GET failed; no retry, stderr suppressed')
        value=decode(result.stdout);need(type(value) in (dict,list),'Native GET object/list required');return value
    except BaseException:FAILED=True;raise

def pages(route,fetch=api):
    values=[]
    for page in range(1,21):
        batch=fetch(route+'?page='+str(page)+'&per_page=100');need(type(batch) is list,'Complete paginated list required');values.extend(batch)
        if len(batch)<100:return values
    raise RuntimeError('Pagination bound reached')
def tree(oid,fetch=api):
    need(hexid(oid),'Native tree identity')
    if oid not in TREES:
        value=fetch('git/trees/'+oid)
        need(value.get('sha')==oid and value.get('truncated') is False and type(value.get('tree')) is list and len(value['tree'])<=30000,'Complete bounded immediate tree')
        rows=value['tree'];names=set()
        for row in rows:
            name=row['path'];need(type(name) is str and name not in ('','.','..') and '/' not in name and '\0' not in name and name not in names,'Native basename');names.add(name)
            need((row['mode'],row['type']) in (('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')) and hexid(row['sha']),'Native mode/type/OID')
        ordered=sorted(rows,key=lambda row:row['path'].encode()+(b'/' if row['type']=='tree' else b''))
        raw=b''.join(row['mode'].lstrip('0').encode()+b' '+row['path'].encode()+b'\0'+bytes.fromhex(row['sha']) for row in ordered)
        need(rows==ordered and native('tree',raw)==oid,'Native tree SHA/order')
        TREES[oid]={row['path']:row for row in rows}
    return TREES[oid]
def lookup(oid,path,fetch=api):
    parts=path.split('/');need(1<=len(parts)<=65 and all(x not in ('','.','..') for x in parts),'Bounded native path')
    for i,name in enumerate(parts):
        row=tree(oid,fetch)[name]
        if i<len(parts)-1:need(row['type']=='tree','Native ancestor tree');oid=row['sha']
    return row

def completion_proof(raw,wanted):
    """Require future actual administrative terminal; this is not case completion."""
    need(exact(pin(raw),bytepin(wanted)),'Externally pinned actual PR212 administrative terminal')
    proof=decode(raw)
    need(type(proof) is dict and proof.get('schema')=='pr212-root-actual-administrative-skip-verification-v1' and proof.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT','Actual Root administrative terminal schema/scope')
    facts={'PR':212,'administrative_checkpoint_percent':100,'fully_completed_count':53,'published_count':37,'last_completed_PR':211,'next_numeric_intake_cursor':213}
    for key,value in facts.items():need(type(proof.get(key)) is int and proof[key]==value,'Actual212 administrative terminal facts: '+key)
    for key in ('accepted','administrative_checkpoint_complete','advance_to_next_PR_authorized_now',
                'all_five_local_files_match_actual_checkpoint','full_scope_verified','all_selected_native_bodies_verified',
                'actual_Root_expected_SHA_force_false_ref_update_and_native_readback','original_stable_writer_lock_held_exact',
                'foreign_native_tuples_preserved','coherent_before_after_ref','all53_37_memberships_unchanged',
                'current_PR_open_draft_unmerged','no_PR_or_publication_actions'):
        need(proof.get(key) is True,'Actual212 administrative acceptance: '+key)
    for key in ('goal_complete','completed_eligible_workflow','publication_workflow_completed','publication_ready',
                'original_eligibility_rewritten_or_erased','numeric_advance_conditional_on_actual_Root_terminal',
                'CAS_or_completion_inferred_from_ancestry','perpetual_or_write_time_Main_equality_claimed'):
        need(proof.get(key) is False,'Actual administrative boundary: '+key)
    for key in ('completed','actual_original_PR_merged','original_PR_already_merged'):
        if key in proof:need(proof[key] is False,'Administrative skip cannot assert eligible completion or original merge: '+key)
    need(proof.get('original_eligible_status')=='claimed_solved' and proof.get('current_corrected_status')=='already_solved'
         and proof.get('disposition')=='ADMINISTRATIVE_ADVANCE_CORRECTED_NONCLAIMED_DRAFT_UNTOUCHED',
         'Original eligibility and current corrected untouched disposition required')
    baseline_raw=regular(SOURCE_DIR/'BASELINE_MEMBERSHIP.json')
    need(exact(pin(baseline_raw),BASELINE_PIN),'Frozen53/37 membership pin')
    baseline=decode(baseline_raw)
    for key,count in (('fully_completed_eligible_PRs',53),('published_PRs',37)):
        members=baseline[key]
        need(type(members) is list and len(members)==count and all(type(n) is int for n in members)
             and members==sorted(set(members)) and 211 in members and 212 not in members,
             'Exact prior eligible membership baseline: '+key)
        need(exact(proof.get(key),members),'Administrative skip must preserve53/37 membership exactly: '+key)
    for key in ('candidate','CAS_target','tree','CAS_target_tree','actual_MAIN_observed','actual_MAIN_tree'):
        need(hexid(proof.get(key)),'Exact actual administrative native identity: '+key)
    need(proof['CAS_target']==proof['candidate'] and proof['CAS_target_tree']==proof['tree'],'Canonical CAS-target aliases differ')
    # The actual Root receipt supplies the historical CAS and qualified C/R
    # observation authority; neither descendant ancestry nor this parser does.
    for key in ('selected_postimage_paths_verified','protected_body_paths_verified'):
        need(type(proof.get(key)) is int and 0<=proof[key]<=10000
             and (key!='selected_postimage_paths_verified' or proof[key]>0),'Bounded actual owned closure count: '+key)
    for key in ('native_final_ref_UTC','terminal_observation_boundary'):
        need(type(proof.get(key)) is str and bool(proof[key]),'Dated qualified Root terminal observation required: '+key)
    return proof


def preserved_status(dated,fetch=api):
    projection=dated['status_projection']
    need(dated['state']=='OPEN' and dated['isDraft'] is True and projection['target_ambiguity'] is False and len(projection['targets'])==1,'Unambiguous preserved draft registry snapshot')
    target=projection['targets'][0];pid=target['problem_id'];head=dated['headRefOid']
    need(type(pid) is str and pid.isdigit() and hexid(head),'Preserved target/head identity')
    need(re.fullmatch(r'(?:dot/math-|math/)'+re.escape(pid)+r'(?:-[^/]+)?',dated['headRefName']) is not None,'Preserved branch/target corroboration')
    commit=fetch('git/commits/'+head)
    need(commit.get('sha')==head and hexid(commit['tree']['sha']) and len(commit['parents'])==1 and hexid(commit['parents'][0]['sha']),'Original native commit/tree/sole parent')
    entry=lookup(commit['tree']['sha'],'unsolved_math_prioritization/QUEUE.md',fetch);need((entry['mode'],entry['type'])==('100644','blob'),'Original regular QUEUE')
    value=fetch('git/blobs/'+entry['sha']);need(value.get('sha')==entry['sha'] and value.get('encoding')=='base64' and type(value.get('size')) is int and 0<=value['size']<=MAX_BODY and type(value.get('content')) is str,'Bounded native QUEUE blob')
    raw=base64.b64decode(''.join(value['content'].split()),validate=True)
    need(len(raw)==value['size'] and native('blob',raw)==entry['sha']==projection['git_blob_oid'] and exact(pin(raw),{'bytes':projection['whole_QUEUE_bytes'],'sha256':projection['whole_QUEUE_sha256']}),'Exact preserved QUEUE identity')
    found=[]
    for row in raw.splitlines(keepends=True):
        cells=row.decode().split('|')
        if len(cells)==14 and cells[2].strip().split(' / ')[0]==pid:found.append((row,cells))
    need(len(found)==1,'Exactly one preserved target row');row,cells=found[0]
    need(hashlib.sha256(row.removesuffix(b'\n')).hexdigest()==target['selected_row_sha256'] and cells[2].strip()==target['code'] and cells[8].strip()==target['status'] and cells[9].strip()==target['turns'],'Exact target row/status/effort')
    return {'problem_id':pid,'head':head,'commit':commit,'entry':entry,'raw':raw,'row':row,'status':cells[8].strip(),'effort':cells[9].strip(),'eligible':cells[8].strip()=='claimed_solved'}

def current_custody(num,dated,original,explicit_head,fetch=api):
    pr=fetch('pulls/'+str(num));head=pr['head']['sha'];pid=original['problem_id']
    need(type(pr.get('number')) is int and pr['number']==num and hexid(head) and pr['head']['ref']==dated['headRefName'],'Exact current PR/branch/head')
    leading=re.match(r'^([0-9]+)\s*:',pr['title']);need(leading is not None and leading[1]==pid,'Current title/preserved target corroboration')
    if explicit_head is not None:need(hexid(explicit_head) and explicit_head==head,'Explicit custody extension must pin exact current HEAD')
    unchanged_open=pr.get('state')=='open' and pr.get('merged') is False and head==original['head']
    if unchanged_open:need(pr.get('draft') is True,'Unchanged open preserved submission must remain draft')
    else:
        need(explicit_head==head,'Changed or already-merged PR requires --descendant-custody-head with exact current HEAD; status custody only')
        need((pr.get('state')=='open' and pr.get('merged') is False and type(pr.get('draft')) is bool) or (pr.get('state')=='closed' and pr.get('merged') is True and pr.get('draft') is False and hexid(pr.get('merge_commit_sha')) and type(pr.get('merged_at')) is str and bool(pr['merged_at'])),'Only actual open or already-merged PR metadata')
        if head!=original['head']:
            comparison=fetch('compare/'+original['head']+'...'+head)
            need(comparison.get('status')=='ahead' and comparison['merge_base_commit']['sha']==original['head'],'Preserved HEAD must be ancestor of explicit current HEAD')
    commits=pages('pulls/'+str(num)+'/commits',fetch);events=pages('issues/'+str(num)+'/timeline',fetch)
    need(type(pr.get('commits')) is int and commits and len(commits)==pr['commits'] and commits[-1]['sha']==head,'Complete current PR commits/head')
    forced=any(event.get('event')=='head_ref_force_pushed' for event in events)
    if unchanged_open:
        need(all(len(item['parents'])==1 for item in commits),'Every unchanged submitted commit has one parent')
        need(all(right['parents'][0]['sha']==left['sha'] for left,right in zip(commits,commits[1:])),'Complete linear submitted chain')
        need(not forced,'Force-push requires separate original custody')
        need([event.get('sha') for event in events if event.get('event')=='committed']==[item['sha'] for item in commits],'Complete committed timeline must match')
    return pr,{'mode':'unchanged_open_original' if unchanged_open else 'explicit_descendant_status_custody','full_changed_head_artifact_custody_required_before_math':not unchanged_open,'unchanged_linear_and_timeline_checks_passed':unchanged_open,'head_ref_force_push_event_detected':forced,'current_PR_commit_count':len(commits),'current_PR_commits_metadata':commits,'current_timeline_event_types':[event.get('event') for event in events],'actual_head':head,'already_merged':pr.get('merged') is True}

def fresh_pr(num,dated,before,fetch=api):
    fresh=fetch('pulls/'+str(num))
    keys=('number','title','state','draft','merged','created_at','updated_at','commits','merge_commit_sha','merged_at')
    need(all(exact(fresh.get(key),before.get(key)) for key in keys) and fresh['head']['sha']==before['head']['sha'] and fresh['head']['ref']==before['head']['ref']==dated['headRefName'],'PR changed during status custody intake')
    need(exact(fresh.get('body'),before.get('body')),'Opaque PR metadata body changed; no mathematical interpretation performed')

def save(directory,name,value,raw=False):
    need(directory.resolve()==directory and directory.is_dir() and Path(name).name==name,'Canonical intake output directory/basename')
    body=value if raw else (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode();need(len(body)<=MAX_BODY,'Bounded intake receipt/evidence')
    with (directory/name).open('xb') as f:need(f.write(body)==len(body),'Short intake write');f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
    return pin(body)

def main():
    global ACTIVE_PR
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Ordinary Python -E -S -B -P without optimization required')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('PR',type=int);parser.add_argument('completion_bytes',type=int);parser.add_argument('completion_sha256');parser.add_argument('predecessor_bytes',type=int);parser.add_argument('predecessor_sha256');parser.add_argument('--descendant-custody-head',help='Explicit narrow status-only extension: exact current HEAD, not full artifact/math clearance')
    args=parser.parse_args();num=args.PR;need(213<=num<=10000,'Ordered numeric cursor213+');ACTIVE_PR=num
    completion_pin=bytepin({'bytes':args.completion_bytes,'sha256':args.completion_sha256});proof_raw=regular(PRIOR/'ROOT_ACTUAL_ADMINISTRATIVE_SKIP_VERIFICATION_01.json');proof=completion_proof(proof_raw,completion_pin)
    own_source_pin=pin(regular(Path(__file__).absolute()));last_pin=None
    for earlier in range(213,num):
        previous_raw=regular(HERE/('PR'+str(earlier)+'_PRESERVED_STATUS_INTAKE.json'));previous=decode(previous_raw)
        need(previous.get('schema')==SCHEMA and type(previous.get('PR')) is int and previous['PR']==earlier and previous.get('eligible') is False and previous.get('action')=='STATUS_ONLY_SKIP_UNTOUCHED' and type(previous.get('next_status_only_cursor')) is int and previous['next_status_only_cursor']==earlier+1 and type(previous.get('preserved_QUEUE_status')) is str and previous['preserved_QUEUE_status']!='claimed_solved','Exact authenticated skip predecessor')
        need(exact(previous.get('procedure_source'),own_source_pin) and exact(previous.get('prior_actual_administrative_terminal_pin'),completion_pin) and exact(previous.get('dated_registry_pin'),REGISTRY_PIN) and exact(previous.get('previous_skip_pin'),last_pin),'Full exact predecessor chain');last_pin=pin(previous_raw)
    if num==213:need(args.predecessor_bytes==0 and args.predecessor_sha256=='-','First cursor has no predecessor')
    else:need(exact(last_pin,bytepin({'bytes':args.predecessor_bytes,'sha256':args.predecessor_sha256})),'Externally pinned last predecessor')
    output=HERE/('PR'+str(num)+'_PRESERVED_STATUS_INTAKE.json');need(not output.exists() and not output.is_symlink(),'Existing intake receipt cannot be overwritten')
    registry_raw=regular(REGISTRY,False);need(exact(pin(registry_raw),REGISTRY_PIN),'Exact preserved registry byte pin');registry=decode(registry_raw);matches=[r for r in registry['rows'] if type(r.get('pr')) is int and r['pr']==num];need(len(matches)==1,'Exactly one preserved registry PR');dated=matches[0]
    # Status eligibility is authenticated BEFORE any current PR/history request.
    original=preserved_status(dated);eligible=original['eligible']
    record={'schema':SCHEMA,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':num,'problem_id':int(original['problem_id']),'preserved_submission_head':original['head'],'preserved_head_tree':original['commit']['tree']['sha'],'preserved_head_sole_parent':original['commit']['parents'][0]['sha'],'preserved_QUEUE_blob':{'git_blob':original['entry']['sha'],**pin(original['raw'])},'preserved_QUEUE_row_pin':pin(original['row']),'preserved_QUEUE_status':original['status'],'preserved_QUEUE_effort_cell':original['effort'],'eligible':eligible,'action':'ELIGIBLE_CUSTODY_REQUIRED_BEFORE_MATH' if eligible else 'STATUS_ONLY_SKIP_UNTOUCHED','next_status_only_cursor':num if eligible else num+1,'procedure_source':own_source_pin,'prior_actual_administrative_terminal_pin':completion_pin,'prior_actual_administrative_candidate':proof['candidate'],'prior_actual_administrative_CAS_target':proof['CAS_target'],'prior_actual_administrative_CAS_target_tree':proof['CAS_target_tree'],'prior_actual_MAIN_observed':proof['actual_MAIN_observed'],'prior_actual_MAIN_tree':proof['actual_MAIN_tree'],'prior_administrative_native_observation_UTC':proof['native_final_ref_UTC'],'prior_terminal_observation_boundary':proof['terminal_observation_boundary'],'prior_administrative_terminal_does_not_determine_current_status_eligibility':True,'prior_administrative_PR':212,'prior_administrative_checkpoint_complete':True,'prior_completed_eligible_workflow':False,'prior_publication_ready':False,'prior_last_completed_PR':211,'prior_completed_count':53,'prior_published_count':37,'previous_skip_pin':last_pin,'dated_registry_pin':REGISTRY_PIN,'dated_registry_row':dated,'no_mathematical_content_reviewed':True,'no_PR_comment_merge_close_reopen_paper_or_repair':True,'no_new_publication_or_tracker_action':True,'original_author_turns_and_model_effort_unverified':True,'date_partition_used_for_HEAD_selection':False,'goal_complete':False,'custody_limits':'Exact preserved dated submitted HEAD and native QUEUE/unique target establish only historical status eligibility. No exact PR-opening-transaction HEAD, author turns, model effort, historical visibility, independence, firstness or priority is inferred. Changed/merged current HEAD requires the explicit exact-HEAD status extension and later full original/revised artifact custody before mathematics.'}
    if eligible:
        before,custody=current_custody(num,dated,original,args.descendant_custody_head);record['current_status_custody']=custody;record['actual_PR']={k:before.get(k) for k in ('number','title','state','draft','merged','merged_at','merge_commit_sha','commits','created_at','updated_at','html_url')}
        if custody['mode']!='unchanged_open_original':record['action']='ELIGIBLE_ALREADY_MERGED_CUSTODY_REQUIRED_BEFORE_MATH' if custody['already_merged'] else 'ELIGIBLE_CHANGED_HEAD_CUSTODY_REQUIRED_BEFORE_MATH'
        fresh_pr(num,dated,before)
        folder=HERE/('PR'+str(num)+'_eligible_evidence');need(not folder.exists() and not folder.is_symlink(),'Eligible evidence already exists');folder.mkdir()
        record['preserved_QUEUE_evidence_pin']=save(folder,'PRESERVED_HEAD_QUEUE.md',original['raw'],True);record['eligible_preserved_own_row']=original['row'].decode();record['preserved_commit_native_metadata']=original['commit']
    else:record['current_PR_or_mathematical_artifact_not_inspected_for_nonclaimed_skip']=True
    record['api_response_hashes']=REQUESTS;receipt=save(HERE,output.name,record);fd=os.open(HERE,os.O_RDONLY);os.fsync(fd);os.close(fd)
    print(json.dumps({'PR':num,'problem_id':record['problem_id'],'preserved_HEAD':original['head'],'preserved_QUEUE_status':original['status'],'preserved_effort':original['effort'],'eligible':eligible,'next_status_only_cursor':record['next_status_only_cursor'],'record':receipt},sort_keys=True))
if __name__=='__main__':main()

