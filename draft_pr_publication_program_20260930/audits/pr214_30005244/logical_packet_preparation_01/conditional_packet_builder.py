"""Inactive PR214 packet constructor. Pure bytes in/out; no transport or filesystem writer.

Import is inert. No CLI activates this source. Future Root supplies authenticated
capture bytes, resolved final source/review closures, then separately reviews the
exact result. Returned copy schedule is data, never executed here.
"""
import copy,datetime,hashlib,json,math,re
from pathlib import PurePosixPath

PROGRAM='draft_pr_publication_program_20260930/'
CASE=PROGRAM+'audits/pr214_30005244/'
VIEWS=(CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md',
       PROGRAM+'CURRENT_PROGRESS.json',PROGRAM+'CURRENT_PROGRESS.md',PROGRAM+'RESEARCH_LOG.md')
ENGINE=CASE+'native_completion_preparation_02'
STAGING='_private_logical_packet_01'
MAX_FILES=600;MAX_TOTAL=8_000_000;MAX_BODY=4_000_000
QUEUE_POLICY='PARENT_AND_C_WHOLE_QUEUE_FIXED_R_FOREIGN_ROWS_ONLY_OWN_EXACT'
BODY_POLICY='ACTUAL_NATIVE_SELECTED_BLOB_GETS_PER_API_INSTANCE'
WRITER={'path':PROGRAM+'ROOT_GLOBAL_FIVE_WRITER.lock','device':16777232,'inode':439078796,
        'bytes':153,'sha256':'61404e167a3dedccc0fd17a1a1823fd772bc12a9144a4f012ab26d5e2a26fc0a'}
MEMBERSHIP_PIN={'bytes':853,'sha256':'b4fe8858faebc0f14ab956d8849af28072837807f3fc87e85a2abe356bfb2f1e'}
ENGINE_SOURCE_MANIFEST_PIN={'bytes':3105,'sha256':'a1f2fd7a1749af748add130a6ad2e3961e476a7ea48f069c9e927a2f035b5ad3'}
CARRY_PIN={'bytes':150305,'sha256':'47c291d5f4c3bb86ad6745a10d72628d850825d10733707584416550d546ec13'}
FROZEN_GATE_PINS={
 'ROOT_CASE_READY_ADOPTION_ACCEPTANCE_01.json':{'bytes':3806,'sha256':'60c5947b07294abaf6f6ce633415793bf3796645b646b83c237d5ab135fc6b5e'},
 'ROOT_NATIVE_COMPLETION_IDENTITY_ACCEPTANCE_01.json':{'bytes':20506,'sha256':'5869f171efe2953fb0644b84804450582018bd5506fe19dbdf3b266e15437f0a'},
 'ROOT_COMPLETION_ENGINE_SOURCE_ACCEPTANCE_02.json':{'bytes':5973,'sha256':'a31e782e1b58df53b2c8eaa3f279a37f9dca1ebd2753c3dce902a5be1acc9aa3'},
 'ROOT_POST_MERGE_MAIN_DRIFT_ACCEPTANCE_01.json':{'bytes':2845,'sha256':'6647655e01303c0e5d34cdef4bead0c2fcff2483920c1c4ca9d4769f90b2de45'}}
FACTS={'active_PR':214,'workflow_percent':100,'completed':True,
 'fully_completed_count':54,'published_count':38,'last_completed_PR':214,'next_numeric_intake_cursor':215,
 'goal_complete':False,'completed_eligible_workflow':True,'publication_workflow_completed':True,'publication_ready':True,
 'original_eligible_status':'claimed_solved','current_status':'claimed_solved','actual_original_PR_merged':True,
 'adopted_existing_publication':True,'no_new_provider_publication_or_tracker_append':True,
 'current_head':'95ba37055ebf1e7b4f9d76aa43816c9978c7bce8','original_merge_commit':'4abf30daa991860a275b3d25745159852757ad35',
 'existing_publication_DOI':'10.5281/zenodo.23390551','existing_tracker_range':"'Math Puzzles'!A105:D105",
 'numeric_advance_conditional_on_actual_Root_terminal':True,'advance_to_next_PR_authorized_now':False}

def need(condition,message):
    if type(condition) is not bool or not condition:raise ValueError(message)

def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def pin(b):
    need(type(b) is bytes,'Bytes required')
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def native(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def enc(o):return (json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()

def decode(raw):
    def pairs(rows):
        result={}
        for k,v in rows:
            need(k not in result,'Duplicate JSON key');result[k]=v
        return result
    def finite(v):
        n=float(v);need(math.isfinite(n),'Nonfinite JSON number');return n
    return json.loads(raw,object_pairs_hook=pairs,parse_float=finite,
                      parse_constant=lambda x:need(False,'Nonfinite JSON constant'))

def rel(p):
    need(type(p) is str and 0<len(p.encode())<=4096 and not PurePosixPath(p).is_absolute()
         and '\\' not in p and all(32<=ord(c)!=127 for c in p)
         and all(x not in ('','.','..') for x in p.split('/')),'Unsafe relative path')
    return p

def bytepin(v):
    need(type(v) is dict and set(v)=={'bytes','sha256'} and type(v['bytes']) is int
         and 0<=v['bytes']<=MAX_BODY and type(v['sha256']) is str
         and re.fullmatch('[0-9a-f]{64}',v['sha256']) is not None,'Exact bounded byte pin')
    return v

def public(p):
    rel(p)
    if not p.startswith(CASE) or p in VIEWS:return False
    forbidden=('private','_private','packet','journal','runtime','_runtime','sandbox','_synthetic',
               'root_admin214_','root_complete214_')
    parts=p[len(CASE):].split('/')
    return not any(x.lower().startswith(forbidden) or x.lower() in ('extracted','objects','inputs') for x in parts) and PurePosixPath(p).suffix.lower() in ('.json','.md','.py','.txt','.tex','.csv','.patch','.sha256')

def regular_tuple(v,tree=False):
    if v is None:return None
    need(type(v) is dict and set(v)=={'mode','type','sha'} and
         (v['mode'],v['type'])==(('040000','tree') if tree else ('100644','blob')) and
         type(v['sha']) is str and re.fullmatch('[0-9a-f]{40}',v['sha']) is not None,'Exact native preimage tuple')
    return v

def validate_baseline(raw):
    need(exact(pin(raw),MEMBERSHIP_PIN),'Pinned53/37 baseline required')
    b=decode(raw)
    need(set(b)=={'fully_completed_eligible_PRs','published_PRs'},'Exact membership roles')
    for key,n in [('fully_completed_eligible_PRs',53),('published_PRs',37)]:
        v=b[key]
        need(type(v) is list and len(v)==n and all(type(x) is int for x in v)
             and v==sorted(set(v)) and 211 in v and all(x not in v for x in (212,213,214)),
             'Exact typed sorted baseline membership')
    need(set(b['published_PRs']).issubset(b['fully_completed_eligible_PRs']),'Published baseline subset')
    return b

def validate_carry(raw):
    need(exact(pin(raw),CARRY_PIN),'Exact149 carry inventory required')
    c=decode(raw)
    need(type(c.get('files')) is list and len(c['files'])==149,'Exactly149 positive carry leaves')
    out={}
    for r in c['files']:
        p=rel(r['path']);need(p not in out,'Duplicate carry path')
        out[p]=bytepin({k:r[k] for k in ('bytes','sha256')})
    need(sum(r['bytes'] for r in out.values())==784242,'Exact carry byte total')
    return out

def body_ok(b,wanted):
    need(type(b) is bytes and len(b)<=MAX_BODY and exact(pin(b),bytepin(wanted)),'Bounded selected byte identity')
    s=b.decode('utf-8');need('\0' not in s,'No NUL or binary selected body')
    return b

def validate_plan(plan,carry):
    need(type(plan) is dict and plan.get('schema')=='pr214-inactive-positive-selection-v1'
         and plan.get('operational_authority') is False,'Source-only selection plan')
    rows=plan.get('files')
    need(type(rows) is list and 0<len(rows)<=MAX_FILES-5,'Bounded positive selection')
    out={}
    for r in rows:
        need(type(r) is dict and set(r)=={'path','origin','bytes','sha256','git_blob','observed_source_mode','role','selection_basis'},
             'Exact selection row')
        p=rel(r['path']);need(p not in out and (public(p) or p in carry),'Positive scope only')
        bytepin({k:r[k] for k in ('bytes','sha256')})
        need(type(r['origin']) is str and r['origin'].startswith('/') and
             type(r['git_blob']) is str and re.fullmatch('[0-9a-f]{40}',r['git_blob']) is not None,
             'Absolute provenance and blob identity')
        rel(r['origin'][1:])
        need(r['observed_source_mode'] in ('0444','0644'),'Explicit existing source mode observation')
        if p in carry:need(exact({k:r[k] for k in ('bytes','sha256')},carry[p]),'Exact carry leaf body')
        out[p]=r
    need(set(carry).issubset(out),'Every149 carry leaf selected')
    slots=plan.get('unresolved_slots')
    need(type(slots) is list and all(type(x) is dict for x in slots),'Explicit unresolved slot objects')
    need(len({x.get('id') for x in slots})==len(slots),'Explicit unique unresolved slot list')
    for x in slots:
        need(type(x) is dict and set(x)=={'id','status','required','blocks_construction','resolution_stage'}
             and x['status']=='UNRESOLVED' and type(x['blocks_construction']) is bool
             and x['resolution_stage'] in ('before_final_selection','external_after_construction','capture_input'),
             'Explicit unresolved slot stage; no guessed pins')
    need(type(plan.get('total_files')) is int and plan['total_files']==len(rows)
         and type(plan.get('total_bytes')) is int and plan['total_bytes']==sum(r['bytes'] for r in rows)<=MAX_TOTAL,
         'Exact selected totals')
    return out

def merge_log_prefix(local,native_body):
    for b in (local,native_body):need(b is None or type(b) is bytes,'Separate native/local log bytes or absence')
    if local is None:return native_body or b''
    if native_body is None:return local
    if local.startswith(native_body):return local
    if native_body.startswith(local):return native_body
    need(False,'Divergent local/native log histories')

def marker():
    return ('<!-- PR214_NATIVE_PHASE_FACTS '+json.dumps(FACTS,sort_keys=True,separators=(',',':'))+' -->').encode()

def append_log(prefix,utc):
    need(b'<!-- PR214_NATIVE_PHASE_FACTS' not in prefix,'Current case marker must not already exist in baseline log')
    # Only append; even a non-newline-terminated captured prefix remains byte exact.
    return prefix+b'\n\n## '+utc.encode()+(' — PR214 conditional checkpoint proposal\n\n').encode()+(
        'Conditional proposal only. Existing qualified publication adopted at DOI10.5281/zenodo.23390551, '
        "tracker 'Math Puzzles'!A105:D105; no new publication, tracker append or PR action. "
        'Proposed54 completed/38 published,last214,cursor215; actual advancement still requires '
        'the separate native checkpoint, exact five sync and actual external Root terminal. Goal remains incomplete.\n\n'
    ).encode()+marker()+b'\n'

def baseline_progress(raw,baseline):
    need(type(raw) is bytes,'Native program JSON body required')
    o=decode(raw)
    for key,value in {'fully_completed_count':53,'published_count':37,'last_completed_PR':211,
                      'next_numeric_intake_cursor':213,'goal_complete':False,'dated_eligible_total':99}.items():
        need(key in o and exact(o[key],value),'Unreconciled baseline progress: '+key)
    for k,v in baseline.items():need(exact(o.get(k),v),'Baseline membership drift: '+k)
    return o

def all_ancestors(paths):
    return sorted({'/'.join(p.split('/')[:i]) for p in paths for i in range(1,len(p.split('/')))})

def construct(plan,selected_bodies,baseline_raw,carry_raw,capture):
    """Pure future construction. The current plan intentionally cannot pass: slots remain.
    
    capture contains Root-supplied dated full native/local preimage bodies and tuples.
    This constructor neither captures them nor authenticates a GET; the future native
    engine independently verifies all such state. Output is conditional bytes only.
    """
    baseline=validate_baseline(baseline_raw);carry=validate_carry(carry_raw);rows=validate_plan(plan,carry)
    need(not any(x['blocks_construction'] for x in plan['unresolved_slots']),'Unresolved selected source/review/self-closure slots prevent construction')
    need(type(selected_bodies) is dict and set(selected_bodies)==set(rows),'Exact positive selected bytes')
    payload={}
    for path,r in rows.items():
        b=body_ok(selected_bodies[path],{k:r[k] for k in ('bytes','sha256')})
        need(native(b)==r['git_blob'],'Selected native blob identity differs');payload[path]=b
    keys={'schema','UTC','engine_source_manifest','native_preimages','native_view_bodies','local_view_bodies',
          'ancestor_tuples','protected_queue','protected_queue_row_pin','retired_candidates',
          'evidence_references','native_identity_receipt'}
    need(type(capture) is dict and set(capture)==keys and capture['schema']=='pr214-future-root-capture-input-v1',
         'Exact future explicit capture interface')
    utc=capture['UTC']
    need(type(utc) is str and re.fullmatch(r'20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z',utc) is not None,
         'Explicit proposed UTC')
    s=capture['engine_source_manifest'];need(type(s) is dict and set(s)=={'path','bytes','sha256'}
        and s['path'].endswith('/'+ENGINE+'/SOURCE_MANIFEST.json'),'Only future repaired02 source manifest')
    need(exact({k:s[k] for k in ('bytes','sha256')},ENGINE_SOURCE_MANIFEST_PIN),'Exact final02 shared source pin')
    datetime.datetime.strptime(utc,'%Y-%m-%dT%H:%M:%SZ')
    # Resolve source manifest by explicitly archived natural target, never by current disk or inherited01 authority.
    need(ENGINE+'/SOURCE_MANIFEST.json' in payload and
         exact(pin(payload[ENGINE+'/SOURCE_MANIFEST.json']),{k:s[k] for k in ('bytes','sha256')}),
         'Final02 shared source manifest must be positively selected')
    sm=decode(payload[ENGINE+'/SOURCE_MANIFEST.json'])
    need(sm.get('source_only') is True and type(sm.get('files')) is list,'Source closure metadata')
    for r in sm['files']:
        n=rel(r['path']);need('/' not in n,'Basename-only shared source closure')
        need(ENGINE+'/'+n in payload,'Complete final02 source closure selected')
        body_ok(payload[ENGINE+'/'+n],{k:r[k] for k in ('bytes','sha256')})
    for n,p in FROZEN_GATE_PINS.items():body_ok(payload.get(CASE+n),p)
    ready=decode(payload[CASE+'ROOT_CASE_READY_ADOPTION_ACCEPTANCE_01.json'])
    identity=decode(payload[CASE+'ROOT_NATIVE_COMPLETION_IDENTITY_ACCEPTANCE_01.json'])
    evidence=capture['evidence_references']
    known_identity_path=ready['native_identity_receipt']['path']
    suffix=CASE+'ROOT_NATIVE_COMPLETION_IDENTITY_ACCEPTANCE_01.json'
    need(known_identity_path.endswith(suffix),'Natural accepted identity reference')
    checkout_prefix=known_identity_path[:-len(suffix)]
    need(s['path']==checkout_prefix+ENGINE+'/SOURCE_MANIFEST.json','Source manifest must be in the same accepted checkout')
    need(all(r['origin'].startswith(checkout_prefix) for r in rows.values()),'Selected original sources remain in the accepted checkout')
    need(type(evidence) is dict and set(evidence)=={'math','custody','priority','adoption','case_ready'},'Exact evidence roles')
    need(exact(evidence['case_ready'],{'path':checkout_prefix+CASE+'ROOT_CASE_READY_ADOPTION_ACCEPTANCE_01.json',**FROZEN_GATE_PINS['ROOT_CASE_READY_ADOPTION_ACCEPTANCE_01.json']}),'Exact readiness natural reference')
    need(exact(capture['native_identity_receipt'],ready['native_identity_receipt']),'Exact accepted native identity')
    need(exact({k:v for k,v in evidence.items() if k!='case_ready'},ready['evidence_references']),'Accepted readiness evidence bindings')
    for ref in [*evidence.values(),capture['native_identity_receipt']]:
        need(type(ref) is dict and set(ref)=={'path','bytes','sha256'},'Exact accepted evidence reference')
        need(type(ref['path']) is str and ref['path'].startswith(checkout_prefix+CASE),'Accepted natural case evidence path')
        target=ref['path'][len(checkout_prefix):]
        need(target in payload and exact(pin(payload[target]),{k:ref[k] for k in ('bytes','sha256')}),'Evidence selected byte binding')
    for k in ['accepted','mathematical_review_accepted','priority_review_accepted','existing_publication_adoption_accepted',
              'two_sequential_fresh_whole_package_reviews_accepted','prior_PR213_status_only_skip_accepted']:
        need(ready.get(k) is True,'Readiness gate: '+k)
    need(ready.get('numeric_advance_authorized_by_this_file') is False,'Readiness is not numeric authority')
    native_views=capture['native_view_bodies'];local=capture['local_view_bodies']
    need(type(native_views) is dict and type(local) is dict and set(native_views)==set(local)==set(VIEWS),
         'Five separate native and local view bodies')
    pre=capture['native_preimages'];need(type(pre) is dict and set(pre)==set(rows)|set(VIEWS),'Every native target preimage explicit')
    for p,v in pre.items():regular_tuple(v)
    for path,b in native_views.items():
        need(b is None or type(b) is bytes,'Native view bytes or absence')
        need((b is None)==(pre[path] is None),'Native absence/body mismatch')
        if b is not None:
            need(native(b)==pre[path]['sha'] and len(b)<=MAX_BODY,'Native view full byte/OID binding')
    for b in local.values():need(b is None or (type(b) is bytes and len(b)<=MAX_BODY),'Bounded separate local view')
    baseline_progress(native_views[VIEWS[2]],baseline)
    if local[VIEWS[2]] is not None:baseline_progress(local[VIEWS[2]],baseline)
    members={k:v+[214] for k,v in baseline.items()}
    common={**FACTS,'conditional_proposal_only':True,'UTC':utc,'phase_facts':copy.deepcopy(FACTS),
            'new_publication_or_tracker_append_performed':False}
    case={**common,'schema':'pr214-conditional-case-status-v1','PR':214,'problem_id':'30005244',
          'scientific_disposition':ready['scientific_disposition'],'historical_priority':'unresolved, qualified attributed note'}
    # Construct from explicit fields; stale case-specific keys from either prior JSON are not inherited.
    program={**common,**members,'schema':'math-draft-publication-conditional-progress-v1',
             'dated_eligible_total':99,'dated_eligible_total_is_not_current_census':True,
             'current_PR':214,'active_publication_DOI':FACTS['existing_publication_DOI'],
             'active_tracker_range':FACTS['existing_tracker_range']}
    payload[VIEWS[0]]=enc(case);payload[VIEWS[2]]=enc(program)
    for p in (VIEWS[1],VIEWS[4]):payload[p]=append_log(merge_log_prefix(local[p],native_views[p]),utc)
    payload[VIEWS[3]]=(('# Conditional publication program progress\n\n'
        'Proposed completed eligible workflows:54; proposed published/adopted results:38. '
        'The existing53/37 baseline remains the last actual completion accounting until the '
        'separate Root terminal succeeds. PR212 and PR213 remain excluded from both lists. '
        'Last proposed completion214; proposed numeric cursor215. Dated eligible denominator99 '
        'is not a current census. No numeric advance is authorized by this proposal.\n\n').encode()+marker()+b'\n')
    need(len(payload)<=MAX_FILES and sum(map(len,payload.values()))<=MAX_TOTAL,'Packet total bounds')
    for p,b in payload.items():body_ok(b,pin(b))
    for path,r in rows.items():
        need(pre[path] is None or pre[path]=={'mode':'100644','type':'blob','sha':r['git_blob']},
             'Nonview archive is add-or-exact-noop only')
    ancestors=capture['ancestor_tuples'];need(type(ancestors) is dict and set(ancestors)==set(all_ancestors(payload)),'Exact ancestor observation inventory')
    for p,t in ancestors.items():regular_tuple(t,tree=True)
    for p,t in ancestors.items():
        parent=p.rpartition('/')[0]
        if parent in ancestors and ancestors[parent] is None:need(t is None,'Child tree cannot exist below absent ancestor')
    for p,t in pre.items():
        if ancestors[p.rpartition('/')[0]] is None:need(t is None,'Leaf cannot exist below absent ancestor')
    changed=sorted(p for p,b in payload.items() if pre[p] is None or pre[p]['sha']!=native(b))
    newdirs=sorted(p for p,v in ancestors.items() if v is None)
    # Runtime will independently derive actual changed leaves/new directories from fresh native trees.
    need(bool(changed),'Nonempty exact changed scope')
    bytepin(capture['protected_queue_row_pin']);regular_tuple(capture['protected_queue'])
    need(capture['protected_queue'] is not None and exact(capture['protected_queue_row_pin'],identity['own_Main_QUEUE_row_pin']),
         'Explicit own MainQUEUE pin, no prepared/whole-root inference')
    retired=capture['retired_candidates']
    need(type(retired) is list and len(retired)<=100 and retired==sorted(set(retired))
         and all(type(x) is str and re.fullmatch('[0-9a-f]{40}',x) for x in retired),'Exact retired candidate denylist')
    sources={};file_rows=[]
    for i,(path,b) in enumerate(sorted(payload.items())):
        source=f'{STAGING}/sources/{i:04d}.txt';sources[source]=b
        file_rows.append({'path':path,'source':source,**pin(b),'git_blob':native(b),'preimage':pre[path]})
    local_rows=[]
    for i,p in enumerate(VIEWS):
        b=local[p];source=None if b is None else f'{STAGING}/local_preimages/{i:02d}.txt'
        if b is not None:sources[source]=b
        local_rows.append({'path':p,'preimage':None if b is None else pin(b),'source':source})
    manifest={'schema':'pr214-conditional-completion-logical-packet-v1','PR':214,'problem_id':'30005244',
       'phase':'completion100','facts':copy.deepcopy(FACTS),'files':file_rows,'total_files':len(file_rows),
       'total_bytes':sum(len(b) for b in payload.values()),'local_views':local_rows,
       'protected_queue':capture['protected_queue'],'protected_queue_row_pin':capture['protected_queue_row_pin'],
       'protected_nodes':identity['protected_nodes'],'protected_bodies':identity['protected_bodies'],
       'current_PR_opaque_body_pin':identity['current_PR_opaque_body_pin'],
       'expected_new_directories':newdirs,'expected_changed_paths':changed,
       'carryforward':[{'path':p,**v} for p,v in sorted(carry.items())],
       'commit_author':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},
       'commit_committer':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},
       'commit_message':'Archive PR214 accepted existing publication completion\n',
       'retired_candidates':retired,'body_proof_policy':BODY_POLICY,'QUEUE_policy':QUEUE_POLICY,
       'writer_lock':copy.deepcopy(WRITER),'evidence_references':evidence,
       'native_identity_receipt':capture['native_identity_receipt']}
    return {'manifest':manifest,'relative_source_bodies':sources,'postimages':payload,
            'source_only':True,'operational_authority':False}
