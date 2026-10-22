"""PR204 custody/source15 checkpoint. Root alone runs native object preparation.
No local Git/index/ref/branch operation, remote ref mutation, PR write or cache write.
Ordinary Python, -B, explicit allowlist, full native-tree identities, actual-only acceptance.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import base64, datetime, hashlib, importlib.util, json, os, re, subprocess, sys
if sys.flags.optimize or not sys.dont_write_bytecode:
    raise RuntimeError('Use ordinary Python with -B; optimization or bytecode writes are forbidden')
D=Path(__file__).resolve().parent; A=D.parent; P=A.parent.parent; ROOT=P.parent
PREFIX='draft_pr_publication_program_20260930/'
CASE=PREFIX+'audits/pr204_5100012/'; OWN=CASE+'custody_checkpoint_01/'
Q='unsolved_math_prioritization/QUEUE.md'; NATIVE='unsolved_math_prioritization/attempts/5100012/'
HEAD='551a524e2db65fec90684485ef676d0b4179378d'
BASE_COMMIT='20c8cb80f5d21b2598a580a18da095d4fec86940'
BASE_TREE='10219264c92feb4bc95603c6568c79924b0d8d2b'
BASE_DIGEST='e3863786dbeff2dedb23a379aea57a05143ed61638fce247df2f77bb18848bd3'
BASE_DIR=A.parent/'pr203_5100011/publication_lifecycle_01/completion100_01'
BASE_ACCEPT={'bytes':1637,'sha256':'796e99ed9fb444f30e638d3d8529612349c3905c935c312569d4c9f052126d5a'}
BASE_MAP={'bytes':1034198,'sha256':'839d6a3008631360bde902c9f5be7c5fdaa36f16e7cd58d431a147bd38218b5c'}
FAMILIES=['math_source_analytic_01','math_direct_geometry_01','math_independent_complex_01','math_algebra_physical_01']
VIEWS=[CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md']+[PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']]
STATUS='ORIGINAL_CUSTODY_AND_SOURCE_CONTRACT_RECORDED_FOUR_NEW_MATH_FAMILIES_ACTIVE'
REMAIN='Complete four independently frozen mathematical approaches and adversarial source/code/effort checks; then bounded priority audit. Mathematics and priority NOT CLEARED. No theorem acceptance, paper, deposit, tracker, PR mutation or next-PR advance.'
CLAIM='Hypothesis only: a>b>0,0<lambda<b^2; fixed proper confocal elliptical caustic; physical least N>=3 odd or divisible4; signed trajectory area times signed area of perpendicular feet from center O to original complete supporting side lines is phase independent. Include admitted coprime stars, either direction, signed zero/negative; no segment clipping or repeated-list extension.'
INPUTS=['ORIGINAL_STATUS_INTAKE.json','ORIGINAL_PR_METADATA.json','ORIGINAL_SUBMISSION_CUSTODY.json','ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json','PRIMARY_SOURCE_ACCESS_01.json','ROOT_SOURCE_FIRST_CONTRACT_01.md','freeze_original_custody.py','original_git_metadata/ORIGINAL_COMMIT.json','original_git_metadata/RANGE_BASE_COMMIT.json','original_git_metadata/ALL_AUTHENTICATED_NONRECURSIVE_TREES.json']
OWN_FILES=['checkpoint204.py','INDEPENDENT_CUSTODY_RECHECK.json','CHECKPOINT_CONTRACT.md','BASELINE_AUTHORITY.json','READ_ONLY_MAIN_AUDIT.json','RESEARCH_LOG.md','SAFE_AUTHORED_MANIFEST.json']
TREE_CACHE={}
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def enc(j): return (json.dumps(j,indent=2)+'\n').encode()
def read(p): return json.loads(p.read_bytes())
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def bpin(b): return {**pin(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def save(p,b):
    require(p.resolve().is_relative_to(D),'Helper artifacts must remain inside own folder')
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    p.chmod(0o444)
def get(endpoint):
    require(not endpoint.startswith(('http:','https:')),'Repository-relative endpoint only')
    p=subprocess.run(['gh','api','repos/AlecKriebel/Math/'+endpoint,'--method','GET'],capture_output=True,timeout=90)
    require(p.returncode==0,'Authenticated read failed '+endpoint+' '+p.stderr.decode()[:250])
    return json.loads(p.stdout)
def valid_tree(sha,j):
    require(j.get('sha')==sha and not j.get('truncated'),'Tree identity/truncation')
    rows=j['tree']; require(len({x['path'] for x in rows})==len(rows),'Duplicate tree names')
    raw=[]
    for x in sorted(rows,key=lambda x:x['path'].encode()+(b'/' if x['type']=='tree' else b'')):
        require('/' not in x['path'] and '\0' not in x['path'] and x['path'] not in ['.','..'],'Unsafe tree entry')
        require((x['mode'],x['type']) in [('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')],'Tree mode/type')
        require(re.fullmatch('[0-9a-f]{40}',x['sha']) is not None,'Malformed native ID')
        raw.append(x['mode'].lstrip('0').encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha']))
    body=b''.join(raw); require(hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()==sha,'Native Git tree identity mismatch')
    return {x['path']:x for x in rows}
def tree(sha):
    if sha is None:return {}
    if sha not in TREE_CACHE:TREE_CACHE[sha]=valid_tree(sha,get('git/trees/'+sha))
    return TREE_CACHE[sha]
def lookup(sha,path):
    parts=path.split('/')
    for i,name in enumerate(parts):
        x=tree(sha).get(name)
        if x is None:return None
        if i==len(parts)-1:return x
        require(x['type']=='tree','Non-directory parent '+path);sha=x['sha']
def walk(sha,prefix=''):
    out={}
    for name,x in tree(sha).items():
        if x['type']=='tree':out.update(walk(x['sha'],prefix+name+'/'))
        else:require(x['mode']=='100644' and x['type']=='blob','Nonregular original');out[prefix+name]=x
    return out
def delta(a,b,prefix=''):
    if a==b:return set()
    left,right=tree(a),tree(b);out=set()
    for name in left.keys()|right.keys():
        x,y=left.get(name),right.get(name)
        if x==y:continue
        xt=x is not None and x['type']=='tree';yt=y is not None and y['type']=='tree'
        if xt or yt:out|=delta(x['sha'] if xt else None,y['sha'] if yt else None,prefix+name+'/')
        if (x is not None and not xt) or (y is not None and not yt):out.add(prefix+name)
    return out
def blob(sha):
    j=get('git/blobs/'+sha);require(j.get('encoding')=='base64','Blob encoding')
    b=base64.b64decode(j['content'],validate=False)
    require(j['sha']==sha==bpin(b)['git_blob'] and j['size']==len(b),'Native blob identity/size')
    return b
def unchanged_pr():
    p=get('pulls/204');saved=read(A/'ORIGINAL_PR_METADATA.json')
    for k in ['number','title','body','state','draft','merged','created_at','updated_at','commits','changed_files']:
        require(p[k]==saved[k],'Original PR metadata changed '+k)
    require(p['head']['sha']==HEAD and p['state']=='open' and p['draft'] is True and p['merged'] is False,'PR204 original head/state changed')
    require(p['created_at']==p['updated_at']=='2026-10-01T05:28:14Z' and p['commits']==2,'Original PR chronology/chain count')
    return {'head':HEAD,**{k:p[k] for k in ['state','draft','merged','created_at','updated_at','commits','changed_files']}}
def custody():
    i=read(A/'ORIGINAL_STATUS_INTAKE.json');r=read(A/'ORIGINAL_SUBMISSION_CUSTODY.json');q=read(A/'ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json')
    require((i['PR'],i['problem_id'],i['original_submitted_head'],i['original_QUEUE_status'],i['original_QUEUE_effort_cell'],i['eligible'])==(204,5100012,HEAD,'claimed_solved','1/5',True),'Original status gate')
    require(r['original_head']==HEAD and r['file_count']==20 and r['total_native_bytes']==59343 and len(r['files'])==20,'Custody census')
    trees=read(A/'original_git_metadata/ALL_AUTHENTICATED_NONRECURSIVE_TREES.json');require(len(trees)==8,'Eight original native trees required')
    for sha,j in trees.items():
        expected=valid_tree(sha,j);fresh=tree(sha)
        require({k:(x['mode'],x['type'],x['sha']) for k,x in fresh.items()}=={k:(x['mode'],x['type'],x['sha']) for k,x in expected.items()},'Fresh tree differs')
    co=get('git/commits/'+HEAD);bc=get('git/commits/'+i['original_range_base'])
    require(co==read(A/'original_git_metadata/ORIGINAL_COMMIT.json') and bc==read(A/'original_git_metadata/RANGE_BASE_COMMIT.json'),'Fresh immutable commit metadata differs')
    require(co['tree']['sha']==i['head_tree']==r['original_tree'] and [p['sha'] for p in co['parents']]==[i['head_sole_parent']],'Original commit containment')
    before=unchanged_pr();native=lookup(co['tree']['sha'],NATIVE.rstrip('/'));require(native and native['type']=='tree','Native root absent')
    files=walk(native['sha']);require(set(files)==set(r['files']),'Original file set')
    pins={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        bodies=list(pool.map(lambda x:blob(x['sha']),files.values()))
    for (name,x),b in zip(files.items(),bodies):
        require(b==(A/'original_submitted_head'/name).read_bytes(),'Archive differs '+name)
        pins[name]={**bpin(b),'mode':x['mode']};require(pins[name]==r['files'][name],'Custody pin differs '+name)
    require(sum(x['bytes'] for x in pins.values())==59343,'Byte census')
    changes=delta(bc['tree']['sha'],co['tree']['sha'])
    require(changes==set(r['complete_original_delta'])=={Q}|{NATIVE+n for n in files},'Complete original range contains foreign delta')
    old=blob(lookup(bc['tree']['sha'],Q)['sha']);new=blob(lookup(co['tree']['sha'],Q)['sha'])
    require(bpin(old)==q['base_QUEUE_blob'] and bpin(new)==q['original_QUEUE_blob']==r['original_QUEUE_blob'],'Original QUEUE pins')
    ol,nl=old.splitlines(keepends=True),new.splitlines(keepends=True);require(len(ol)==len(nl),'QUEUE shape')
    ix=[k for k,(x,y) in enumerate(zip(ol,nl)) if x!=y];require(ix==[q['one_based_row']-1],'QUEUE single own row delta')
    k=ix[0];require(b'| 5100012 / AMR-050-0012 |' in ol[k] and b'| 5100012 / AMR-050-0012 |' in nl[k],'QUEUE own identity')
    require(bpin(ol[k])=={z:q['base_own_row'][z] for z in ['bytes','sha256','git_blob']} and bpin(nl[k])=={z:q['original_QUEUE_row'][z] for z in ['bytes','sha256','git_blob']},'QUEUE row pins')
    require(nl[k].decode().split('|')[8:10]==[' claimed_solved ',' 1/5 '],'Original claimed solved effort')
    source=read(A/'PRIMARY_SOURCE_ACCESS_01.json');source_pins=[]
    for x in source['primary_files']:
        p=Path(x['existing_readonly_path']);require(pin(p.read_bytes())=={z:x[z] for z in ['bytes','sha256']},'Primary PDF source byte drift')
        source_pins.append({z:x[z] for z in ['file','url','bytes','sha256']})
    require(len(source_pins)==4,'Four primary PDFs')
    contract=(A/'ROOT_SOURCE_FIRST_CONTRACT_01.md').read_bytes();require(b'Source and mathematics are NOT yet cleared' in contract,'Source contract clearance gate')
    after=unchanged_pr();require(before==after,'PR race during custody')
    return {'UTC':now(),'PR':204,'problem_id':5100012,'independent_operational_recheck':True,'no_math_candidate_or_favorable_review_semantics_consumed':True,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_QUEUE_effort_cell':'1/5','file_count':20,'total_native_bytes':59343,'all_native_blob_identities_and_local_archive_bytes_verified':True,'all_eight_saved_native_tree_identities_recomputed_and_freshly_authenticated':True,'original_range_delta_count':len(changes),'original_range_exact_twenty_native_plus_single_own_QUEUE_row':True,'foreign_original_QUEUE_lines_identical':True,'fresh_original_PR_unchanged':after,'input_pins':{n:pin((A/n).read_bytes()) for n in INPUTS},'original_files':pins,'primary_pdf_byte_pins':source_pins,'source_contract_pin':pin(contract),'source_contract_recorded_only':True,'mathematical_clearance':False,'priority_clearance':False,'historical_firstness_or_independence_certified':False,'case_percent':15,'independent_math_families':FAMILIES,'family_state_at_initial_checkpoint':'Four new independent families active; no proof or family result accepted here.','publication_ready':False,'theorem_acceptance':False,'paper_or_deposit_prepared':False,'no_remote_mutation':True}
def load():
    p=A.parent/'pr203_5100011/publication_lifecycle_01/finish203.py';s=importlib.util.spec_from_file_location('custody204_prior_primitives',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
    return v.load() # finish203.load explicitly unregisters the legacy authenticated-cache writer.
def validate_caches(h):
    for sha,rows in h.m.native_tree_cache.items():h.m.verify_tree_object(sha,rows)
def baseline(c):
    ab=(BASE_DIR/'ACCEPTANCE.json').read_bytes();mb=(BASE_DIR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes();a=json.loads(ab);x=json.loads(mb)
    require(pin(ab)==BASE_ACCEPT and pin(mb)==BASE_MAP,'Actual PR203 receipt/map byte pin')
    require(a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['completion_metadata_accepted'],'Actual baseline acceptance absent')
    require(a['checkpoint_commit']==a['main_observed']==BASE_COMMIT and a['actual_tree']==BASE_TREE,'Actual baseline commit/tree')
    require(len(x['selected_files'])==a['selected_files']==3449 and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])==BASE_DIGEST,'Baseline every-selected map identity')
    require((a['fully_completed_count'],a['published_count'],a['last_completed_PR'],a['next_numeric_intake_cursor'])==(46,30,203,204),'PR203 baseline program counters')
    return {'commit':BASE_COMMIT,'tree':BASE_TREE,'selected_files':x['selected_files'],'selected_map_sha256':BASE_DIGEST}
def native_body(h,path,commit):
    t=h.api('git/commits/'+commit)['tree']['sha'];x=h.lookup(t,path)
    if x is None:return None
    require(x[0:2]==('100644','blob'),'Nonregular selected body '+path)
    b=blob(x[2]);require(bpin(b)['git_blob']==x[2],'Native body mismatch');return b
def reconcile(c,h,b,parent):
    old=native_body(h,Q,b['commit']);new=native_body(h,Q,parent)
    require(c.byte_pin(old)==b['selected_files'][Q],'Baseline QUEUE pin drift')
    protected={k.split('/')[2] for k in b['selected_files'] if k.startswith('unsolved_math_prioritization/attempts/')};protected.add('5100012')
    ol,nl=old.splitlines(keepends=True),new.splitlines(keepends=True);require(len(ol)==len(nl),'Foreign QUEUE line count changed');changes=[]
    for k,(x,y) in enumerate(zip(ol,nl)):
        if x==y:continue
        def ident(z):
            cells=z.decode().split('|');require(len(cells)==14 and cells[1].strip().isdigit(),'Malformed changed QUEUE row');return cells[2].strip().split(' / ')[0]
        pid=ident(x);require(ident(y)==pid and pid not in protected,'Protected or own QUEUE row changed')
        changes.append({'one_based_line':k+1,'foreign_problem_id':pid,'old_line':bpin(x),'new_line':bpin(y)})
    require([x for x in ol if b'| 5100012 / AMR-050-0012 |' in x]==[x for x in nl if b'| 5100012 / AMR-050-0012 |' in x],'Current own QUEUE row changed')
    return {**b['selected_files'],Q:c.byte_pin(new)},{'UTC':now(),'baseline_actual_commit':b['commit'],'observed_actual_MAIN':parent,'old_QUEUE':c.byte_pin(old),'current_QUEUE':c.byte_pin(new),'protected_native_problem_ids':sorted(protected),'foreign_changed_rows':changes,'all_other_QUEUE_bytes_identical':True,'all_protected_and_own_QUEUE_rows_identical':True,'own_checkpoint_writes_no_QUEUE_bytes':True,'scope':'Byte custody only; no endorsement of concurrent foreign mathematics.'}
def check_local_manifest():
    j=read(D/'SAFE_AUTHORED_MANIFEST.json');require(set(j['files'])==set(OWN_FILES)-{'SAFE_AUTHORED_MANIFEST.json'},'Exact helper authored allowlist')
    for n,x in j['files'].items():
        p=D/n;require(p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444 and pin(p.read_bytes())==x,'Authored file drift '+n)
    return j
def overlay(c,h,parent,stamp):
    check_local_manifest();cr=read(D/'INDEPENDENT_CUSTODY_RECHECK.json');require(cr['case_percent']==15 and cr['mathematical_clearance'] is False and cr['priority_clearance'] is False,'Custody receipt scope')
    out={}
    def add(rel):
        p=A/rel;require(p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444,'Unsafe/unfrozen input '+rel);out[CASE+rel]=p.read_bytes()
    for rel in INPUTS:
        require(pin((A/rel).read_bytes())==cr['input_pins'][rel],'Custody input drift '+rel);add(rel)
    for rel,x in cr['original_files'].items():
        require(bpin((A/'original_submitted_head'/rel).read_bytes())=={z:x[z] for z in ['bytes','sha256','git_blob']},'Archive publication drift '+rel);add('original_submitted_head/'+rel)
    for name in OWN_FILES:add('custody_checkpoint_01/'+name)
    p=json.loads(native_body(h,PREFIX+'CURRENT_PROGRESS.json',parent))
    require((p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'],p['current_completed'])==(203,46,30,203,100,True),'Actual PR203 must remain preceding case')
    # Retire ALL prior current/next/provenance keys; no 203 authority survives as 204 current data.
    retired={k:p[k] for k in list(p) if k.lower().startswith(('current_','next_','conditional_','program_snapshot_')) or k in ['advance_to_next_PR_authorized_now','remaining_current_step','next_step','latest_ordered_intake_record','latest_ordered_intake_records']}
    p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':203,'prior_phase':'actual_completed_before204_custody15','actual_completion_commit':BASE_COMMIT,'actual_completion_receipt_pin':BASE_ACCEPT,'values':retired})
    for k in retired:del p[k]
    case={'UTC':stamp,'PR':204,'problem_id':5100012,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_QUEUE_effort_cell':'1/5','original_effort':'Original QUEUE reports 1/5; author turn count and actual model/reasoning effort unverified. New audits do not count as original author effort.','status':STATUS,'case_percent':15,'exact_claim_hypothesis':CLAIM,'source_contract_record':'ROOT_SOURCE_FIRST_CONTRACT_01.md','source_contract_recorded':True,'source_contract_clearance':False,'source_provenance_warning':'RGK Table3 k203,b is signed original trajectory area times original-side origin-pedal area in a confocal ellipse pair, N not congruent2mod4. Source omits literal primitive/least; least physical period is explicit scope hypothesis. Dated question marks/imported OPEN-TRIAGE do not certify current openness or priority.','original_archive_files':20,'original_native_bytes':59343,'independent_mathematical_families':FAMILIES,'independent_mathematical_families_active':True,'independent_mathematical_families_complete':0,'mathematical_clearance':False,'mathematical_result_valid':None,'priority_audit_active':False,'priority_audit_complete':False,'priority_clearance':False,'historical_novelty_or_firstness_established':False,'independent_discovery_certified':False,'publication_ready':False,'theorem_accepted':False,'paper_prepared':False,'deposit_prepared':False,'whole_publication_package_reviews_complete':False,'actual_Zenodo_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'actual_factual_MAIN_accepted':False,'completed':False,'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'conditional_next_numeric_intake_cursor':205,'advance_to_next_PR_authorized_now':False,'remaining_required_steps':REMAIN,'goal_complete':False,'checkpoint_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance':True}
    out[CASE+'CURRENT_CASE_STATUS.json']=enc(case)
    note='\n'+stamp+' — PR204 custody/source checkpoint15%: original HEAD'+HEAD+', claimed_solved1/5, all20 files59343B and8 native trees independently reauthenticated; complete original range only20 native files plus single own QUEUE row, all foreign lines identical. Source-first exact hypothesis recorded; four new independent mathematical families active. Mathematics and priority NOT CLEARED; no theorem acceptance, paper, deposit, tracker, PR mutation or next-PR advance.46completed/30published,last203,cursor204/advancefalse; goal active.\n'
    initial=(A/'RESEARCH_LOG.md').read_bytes();require(pin(initial)==cr.get('initial_case_log_pin',pin(initial)),'Initial local case log changed')
    out[CASE+'RESEARCH_LOG.md']=initial+note.encode()
    p.update(UTC=stamp,updated_UTC=stamp,current_PR=204,current_problem_id=5100012,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_QUEUE_effort_cell='1/5',current_original_budget=case['original_effort'],current_PR_workflow_percent=15,current_workflow_estimate_percent=15,current_status=STATUS,current_completed=False,current_closed=False,current_closed_without_merge=False,current_original_PR_state='open',current_original_PR_merged=False,current_original_PR_open_draft=True,current_mathematical_clearance=False,current_mathematics_cleared=False,current_mathematical_result_valid=None,current_source_contract_recorded=True,current_source_contract_clearance=False,current_source_contract='audits/pr204_5100012/ROOT_SOURCE_FIRST_CONTRACT_01.md',current_source_provenance_warning=case['source_provenance_warning'],current_independent_mathematical_audit_active=True,current_independent_mathematical_audit_families=4,current_independent_mathematical_audit_families_complete=0,current_independent_mathematical_audit_names=FAMILIES,current_priority_audit_active=False,current_priority_audit_complete=False,current_priority_clearance=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_theorem_novelty_cleared=False,current_proof_method_novelty_cleared=False,current_publication_ready=False,current_publication_package=None,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_actual_publication_verified=False,current_actual_tracker_row_verified=False,current_actual_merge_accepted=False,current_actual_factual_checkpoint_accepted=False,current_record='audits/pr204_5100012/CURRENT_CASE_STATUS.json',current_exact_claim_hypothesis=CLAIM,current_remaining_required_steps=REMAIN,remaining_current_step=REMAIN,next_step=REMAIN,next_numeric_intake_cursor=204,conditional_next_numeric_intake_cursor=205,advance_to_next_PR_authorized_now=False,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=204,next_status_only_intake_performed=True,latest_ordered_intake_record='audits/pr204_5100012/ORIGINAL_STATUS_INTAKE.json',persistent_goal_complete=False,goal_work_continuing=True,program_snapshot_semantics='PR203 actual completion retained:46completed/30published,last203. PR204 original claimed_solved1/5 custody and exact source hypothesis recorded; four fresh independent mathematical families active; mathematics and priority NOT CLEARED. No theorem acceptance, paper, deposit or next-PR advance.',program_snapshot_authority_condition='Custody15 postimage effective only after Root actual trueparent/fullforeignscope/everyselectedidentity acceptance; no self-certified actual acceptance.')
    out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
    for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:out[PREFIX+n]=native_body(h,PREFIX+n,parent)+note.encode()
    require(Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in out),'Forbidden QUEUE/native overlay')
    return out

def message(d):return 'PR204 custody15: original submission and source-first hypothesis\n\nFour fresh independent mathematical families active. Mathematics and priority NOT CLEARED; no theorem acceptance, paper or deposit.46completed/30published,last203,cursor204,advancefalse.\nPR204 custody selected-map SHA256: '+d

def selected(c,inherited,out):
    for k,b in out.items():
        require(k in VIEWS or k.startswith(CASE),'Overlay outside exact case/global scope '+k)
        if k in inherited and k not in VIEWS:require(c.byte_pin(b)==inherited[k],'Selected immutable overwrite '+k)
    return {**inherited,**{k:c.byte_pin(b) for k,b in out.items()}}

def verify(c,h,r,out,expected):
    require(r['selected_files']==expected and r['selected_map_sha256']==c.selected_digest(expected),'Prepared map differs')
    co=h.api('git/commits/'+r['commit']);require([x['sha'] for x in co['parents']]==[r['expected_main']] and co['tree']['sha']==r['tree'] and co['message']==message(c.selected_digest(expected)),'Exact single true-parent commit')
    require(h.api('git/commits/'+r['expected_main'])['tree']['sha']==r['parent_tree'],'Parent tree drift')
    h.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],expected)
    for k,x in expected.items():require(h.lookup(r['tree'],k)==('100644','blob',x['git_blob']),'Selected identity mismatch '+k)
    changes={k for k,x in expected.items() if h.lookup(r['parent_tree'],k)!=('100644','blob',x['git_blob'])}
    require(changes==h.changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']) and changes<=set(out),'Full foreign tree changed outside exact overlay')
    require(Q not in changes and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in changes),'QUEUE/native write forbidden')
    for k,b in out.items():require(c.byte_pin(b)==expected[k],'Overlay body map mismatch '+k)
    validate_caches(h);unchanged_pr()

def generation(name):
    require(re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Unsafe generation name');return D/name

def run(mode,name):
    c,h,rv,n=load();b=baseline(c);dest=generation(name)
    if mode=='prepare':
        require(not dest.exists(),'Generation already exists')
        parent=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+BASE_COMMIT+'...'+parent)['status'] in ['identical','ahead'],'Fresh MAIN must descend from actual PR203')
        inherited,ack=reconcile(c,h,b,parent);pt=c.selected_current(h,parent,inherited,BASE_TREE);validate_caches(h);unchanged_pr();stamp=now()
        out=overlay(c,h,parent,stamp);dest.mkdir();save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',enc(ack))
        out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes()
        expected=selected(c,inherited,out)
        # These are the only remote writes this helper can issue. Root alone runs prepare.
        entries=[{'path':k,'mode':'100644','type':'blob','content':z.decode('utf-8')} for k,z in sorted(out.items())]
        tr=h.api('git/trees','POST',{'base_tree':pt,'tree':entries})['sha']
        co=h.api('git/commits','POST',{'tree':tr,'parents':[parent],'message':message(c.selected_digest(expected))})['sha']
        local_pre={}
        for rel in VIEWS:
            p=ROOT/rel;local_pre[rel]=pin(p.read_bytes()) if p.exists() else None
            remote=native_body(h,rel,parent)
            if rel.startswith(PREFIX) and not rel.startswith(CASE):require(remote is not None and local_pre[rel]==pin(remote),'Global local files must match fresh parent before preparation')
            elif rel==CASE+'CURRENT_CASE_STATUS.json':require(not p.exists() and remote is None,'New case status must be absent')
            else:require(remote is None and local_pre[rel]==pin((A/'RESEARCH_LOG.md').read_bytes()),'New case log local intake pin')
        r={'UTC':stamp,'PR':204,'case_percent':15,'original_head':HEAD,'expected_main':parent,'parent_tree':pt,'tree':tr,'commit':co,'selected_files':expected,'selected_map_sha256':c.selected_digest(expected),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in expected.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'local_five_expected_preimages':local_pre,'MAIN_moved':False,'mathematical_clearance':False,'priority_clearance':False,'advance_to_next_PR_authorized_now':False}
        save(dest/'PREPARATION.json',enc(r))
    else:
        r=read(dest/'PREPARATION.json');parent=r['expected_main'];stamp=r['UTC'];pt=r['parent_tree'];ack=read(dest/'FOREIGN_QUEUE_RECONCILIATION.json')
        inherited={**b['selected_files'],Q:ack['current_QUEUE']};out=overlay(c,h,parent,stamp);out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=selected(c,inherited,out)
    verify(c,h,r,out,expected);main=h.api('git/ref/heads/main')['object']['sha']
    if mode in ['prepare','verify']:
        require(main==parent,'MAIN changed since exact preparation; regenerate against fresh parent')
        pre={'UTC':now(),'PR':204,'commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_single_trueparent_fullforeignscope_everyselectedidentity_verified':True,'original_head_unchanged':True,'no_QUEUE_native_or_PR_mutation':True,'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'case_percent':15,'mathematical_clearance':False,'priority_clearance':False,'publication_ready':False,'actual_MAIN_acceptance':False}
        if mode=='prepare':save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc(pre))
        print(json.dumps({'mode':mode,'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'changed_paths':len(r['changed_paths']),'observed_MAIN':main,'mathematical_clearance':False,'priority_clearance':False}));return
    require(mode=='accept','Unsupported phase')
    require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Actual MAIN does not contain checkpoint')
    current,post=reconcile(c,h,r,main);actual_tree=c.selected_current(h,main,current,r['tree']);validate_caches(h);unchanged_pr()
    for k,z in out.items():require(c.byte_pin(z)==expected[k] and h.lookup(actual_tree,k)==('100644','blob',expected[k]['git_blob']),'Actual overlay identity drift '+k)
    # Parent-tree exact delta already proves checkpoint preserved all foreign paths. Current
    # descendants may contain fresh unprotected QUEUE rows, acknowledged by exact bytes above.
    body=enc({'selected_files':current,'selected_map_sha256':c.selected_digest(current),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
    a={'UTC':now(),'PR':204,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':actual_tree,'original_head':HEAD,'original_PR_open_draft_unchanged':True,'case_percent':15,'selected_files':len(current),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(current),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved_at_checkpoint':True,'foreign_QUEUE_exact_byte_acknowledgement':True,'QUEUE_native_original_PR_unchanged_by_checkpoint':True,'source_contract_recorded':True,'source_contract_clearance':False,'mathematical_clearance':False,'priority_clearance':False,'historical_firstness_independence_established':False,'publication_ready':False,'theorem_accepted':False,'paper_or_deposit_prepared':False,'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
    save(dest/'ACCEPTANCE.json',enc(a));print(json.dumps(a))

def sync(name):
    c,h,rv,n=load();dest=generation(name);r=read(dest/'PREPARATION.json');a=read(dest/'ACCEPTANCE.json');mp=read(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
    require(a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==r['commit'] and a['actual_current_map_file']==pin((dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes()),'Actual acceptance required before local sync')
    require(mp['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(mp['selected_files']),'Actual accepted map drift')
    main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Checkpoint no longer on MAIN');c.selected_current(h,main,mp['selected_files'],a['actual_tree']);validate_caches(h)
    rows=[]
    for rel in VIEWS:
        p=ROOT/rel;post=native_body(h,rel,r['commit']);require(c.byte_pin(post)==r['selected_files'][rel],'Accepted local postimage drift')
        old=p.read_bytes() if p.exists() else None
        require((None if old is None else pin(old)) in [r['local_five_expected_preimages'][rel],pin(post)],'Unexpected local view change '+rel)
        if old!=post:
            tmp=p.with_name(p.name+'.pr204_custody_sync_tmp')
            with tmp.open('xb') as f:f.write(post);f.flush();os.fsync(f.fileno())
            require(tmp.read_bytes()==post,'Sync temporary bytes');tmp.chmod(0o444);os.replace(tmp,p)
        p.chmod(0o444);require(p.read_bytes()==post,'Local sync readback')
        rows.append({'path':rel,'postimage':pin(post),'prior_or_postimage_guard':True})
    j={'UTC':now(),'PR':204,'actual_checkpoint':r['commit'],'all_five_local_files_match_actual_checkpoint':True,'files':rows,'mathematical_clearance':False,'priority_clearance':False,'case_percent':15};save(dest/'LOCAL_GLOBAL_FIVE_SYNC.json',enc(j));print(json.dumps(j))

if __name__=='__main__':
    require(len(sys.argv)>=2,'custody | prepare GEN | verify GEN | accept GEN | sync GEN')
    mode=sys.argv[1]
    if mode=='custody':
        require(len(sys.argv)==2,'Custody takes no generation');j=custody();j['initial_case_log_pin']=pin((A/'RESEARCH_LOG.md').read_bytes());save(D/'INDEPENDENT_CUSTODY_RECHECK.json',enc(j));print(json.dumps({k:j[k] for k in ['UTC','file_count','total_native_bytes','original_range_delta_count','case_percent','mathematical_clearance','priority_clearance','no_remote_mutation']}))
    elif mode=='sync':require(len(sys.argv)==3,'sync GEN');sync(sys.argv[2])
    else:require(mode in ['prepare','verify','accept'] and len(sys.argv)==3,'Unknown phase');run(mode,sys.argv[2])
