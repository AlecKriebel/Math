"""PR204 original-HEAD-safe lifecycle candidate; Root adoption required.

Explicit bind/prepare/verify/accept/sync/pointer phases only. Ref, PR metadata,
publication and tracker mutations remain external Root operations.
"""
import sys
if sys.flags.optimize or not sys.dont_write_bytecode:
    raise RuntimeError('Ordinary Python -B required')
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,re
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent;ROOT=P.parent

def need(ok,message):
    if not ok:raise RuntimeError(message)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def bpin(raw):return {**pin(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
def enc(value):return (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
def no_constant(value):raise RuntimeError('Nonfinite JSON '+value)
def decode(raw):return json.loads(raw,parse_constant=no_constant)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rel(value):
    need(isinstance(value,str) and value and not value.startswith('/') and '\\' not in value and all(x not in ('','.','..') for x in value.split('/')),'Unsafe relative path');return value
def bp(value):
    need(isinstance(value,dict) and set(value)=={'bytes','sha256'} and type(value['bytes']) is int and value['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',str(value['sha256'])) is not None,'Invalid byte pin');return value
def pp(path,value):return {'path':rel(path),**bp(value)}
def valid_sha(value):return re.fullmatch('[0-9a-f]{40}',str(value)) is not None
def digest_selected(selected):return hashlib.sha256(json.dumps(selected,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def frozen(path,expected=None,readonly=True):
    rel(path);f=A
    for part in path.split('/'):
        f=f/part;need(not f.is_symlink(),'Symlink input '+path)
    need(readonly or expected is not None,'Nonreadonly input requires explicit pin');need(f.is_file() and (not readonly or f.stat().st_mode&0o777==0o444),'Regular/policy input required '+path);raw=f.read_bytes()
    if expected is not None:need(pin(raw)==bp(expected),'Input pin drift '+path)
    return raw
def module(name,path,expected,readonly=True):
    raw=frozen(path,expected,readonly);s=importlib.util.spec_from_file_location(name,A/path);m=importlib.util.module_from_spec(s);exec(compile(raw,str(A/path),'exec'),m.__dict__);return m
READY_PIN={'bytes':27378,'sha256':'20ffe7dac7218df8a098fd4715ae118973f1e8f80a780ae6183bbb0b2b616bdd'}
OPS_PIN={'bytes':9504,'sha256':'fd3bc7731c12dc35639cf63d58fd416aa90e3842699d0ce3b79fbfaba6f4c3e4'}
TRACKER_SOURCE_PIN={'bytes':9680,'sha256':'b245072605f9ffdb86e62d7c16de9771b43f6acccdb70c445d99fe176f4953ea'}
CUSTODY_PIN={'bytes':7837,'sha256':'5011318581db86668f4a6d27939808957875c55b70c1cc71b61ed63bb1f18a93'}
QUEUE_RECEIPT='ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json'
QUEUE_RECEIPT_PIN={'bytes':1833,'sha256':'15e03207a966aa4923269d4fbec455a2fa451519a9491b35ecbe4bb597660e46'}
BASE_ROW_PIN={'bytes':123,'sha256':'580ee80fcac4c7511613cd1073ff58532859b5bc4ddcec0c4363ee47ed3c5967'}
HEAD_ROW_PIN={'bytes':584,'sha256':'ef999905156e3ea339cfb861cd5e869fc27806a425f61518c27a638fb31ae5b2'}
READY_ADOPTION='ROOT_READINESS_HELPER_PREPARATION_ACCEPTANCE_02.json'
READY_ADOPTION_PIN={'bytes':10328,'sha256':'fb9ba6e78f6c952a2efef3624f2b35943b977fc0645026c43a70e9ea1332196f'}
R=module('pr204_Root_reviewed_ready02','publication_checkpoint_02/checkpoint_ready204.py',READY_PIN);v=R.v
ops=module('pr204_Root_reviewed_operations02','publication_operations_01/revision_02/operations_common.py',OPS_PIN)
HEAD=R.HEAD;CASE=R.CASE;PREFIX=R.PREFIX;Q=R.Q;VIEWS=R.VIEWS;NATIVE='unsolved_math_prioritization/attempts/5100012/'
OWN=CASE+'publication_lifecycle_02/'
PHASE={'merge':('ready',90,95,'published_pending_merge'),'factual':('merge',95,98,'actual_merge_accepted'),'completion':('factual',98,100,'factual_checkpoint_accepted')}
POINTER={'ready':'ROOT_ACTUAL_READY_CHECKPOINT.json','merge':'ROOT_ACTUAL_MERGE_CHECKPOINT.json','factual':'ROOT_ACTUAL_FACTUAL_CHECKPOINT.json','completion':'ROOT_ACTUAL_COMPLETION_CHECKPOINT.json'}
WRAPPERS={'README.md','SOURCES.md','MANIFEST.json','PUBLICATION_MANIFEST.json','PUBLICATION_STATUS.md'}
ADDED={'CURRENT_STATUS.json','CURRENT_PROOF.md','CURRENT_SOURCE_AND_PRIORITY.json','QUALIFIED_PRIORITY.md','CURRENT_RESEARCH_LOG.md','NATIVE_PRESENTATION_RECEIPT.json','SHA256SUMS'}
OWN_FILES={'finish204.py','offline_guard_tests.py','CONTRACT.md','RESEARCH_LOG.md','OFFLINE_GUARD_REPORT.json','ACTUAL_LOCAL_RECEIPT_COMPATIBILITY.json','SAFE_AUTHORED_MANIFEST.json'}
BASE_COUNTS={'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
DONE_COUNTS={'fully_completed_count':47,'published_count':31,'last_completed_PR':204,'next_numeric_intake_cursor':205,'advance_to_next_PR_authorized_now':True,'goal_complete':False}

def counts(phase,actual=False):
    need(phase in PHASE and type(actual) is bool,'Phase/actual selector');return dict(DONE_COUNTS if phase=='completion' and actual else BASE_COUNTS)
def generation(name):
    need(re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Unsafe generation');return D/name
def record(name,filename):return decode(frozen('publication_lifecycle_02/'+generation(name).name+'/'+rel(filename)))
def save(path,raw,pointer=False):
    need((path.parent==A and path.name in POINTER.values()) if pointer else path.resolve().is_relative_to(D),'Output scope')
    with path.open('xb') as stream:
        need(stream.write(raw)==len(raw),'Short record write');stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
    R.fsync_directory(path.parent)
def manifest():
    raw=frozen('publication_lifecycle_02/SAFE_AUTHORED_MANIFEST.json');j=decode(raw)
    need(set(j['files'])==OWN_FILES-{'SAFE_AUTHORED_MANIFEST.json'},'Exact lifecycle authored files')
    for name,x in j['files'].items():frozen('publication_lifecycle_02/'+name,x)
    return pin(raw)
def actual(which):
    need(which in POINTER,'Unknown actual phase');j=decode(frozen(POINTER[which]));directory=rel(j['directory'])
    need(directory.startswith('publication_checkpoint_02/') if which=='ready' else directory.startswith('publication_lifecycle_02/'),'Actual predecessor source version')
    ab=frozen(directory+'/ACCEPTANCE.json',j['acceptance_pin']);a=decode(ab);r=decode(frozen(directory+'/PREPARATION.json'));x=decode(frozen(directory+'/ACCEPTANCE_CURRENT_SELECTED_MAP.json',a['actual_current_map_file']))
    need(j['PR']==a['PR']==204 and j['phase']==which and a['accepted'] is True and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True and a['all_overlay_body_identities_verified'] is True and a['full_foreign_tree_scope_preserved'] is True,'Actual predecessor full-scope receipt')
    need(a['checkpoint_commit']==r['commit']==j['checkpoint_commit'] and a['main_observed']==j['main_observed'] and valid_sha(a['checkpoint_commit']) and valid_sha(a['main_observed']) and valid_sha(a['actual_tree']) and a['original_head']==HEAD,'Actual predecessor identity')
    need(a['case_percent']=={'ready':90,'merge':95,'factual':98,'completion':100}[which],'Actual predecessor percent')
    need(r['selected_map_sha256']==a['selected_map_sha256']==digest_selected(r['selected_files']) and len(x['selected_files'])==a['selected_files'] and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==digest_selected(x['selected_files']),'Actual predecessor every-selected digest')
    return directory,a,r,x
def originals():
    j=decode(frozen('ORIGINAL_SUBMISSION_CUSTODY.json',CUSTODY_PIN));need(j['original_head']==HEAD and j['file_count']==20 and j['total_native_bytes']==59343 and j['original_QUEUE_status']=='claimed_solved' and j['original_QUEUE_effort_cell']=='1/5','Original custody extent')
    out={}
    for name,x in j['files'].items():
        raw=frozen('original_submitted_head/'+rel(name));need(bpin(raw)=={k:x[k] for k in ('bytes','sha256','git_blob')},'Original archive drift '+name);out[name]=raw
    need(len(out)==20 and WRAPPERS<=set(out) and len(set(out)-WRAPPERS)==15,'Original native preservation set');return j,out
def native_adoption(record_pin):
    raw=frozen(record_pin['path'],{k:record_pin[k] for k in ('bytes','sha256')});j=decode(raw)
    need(j['accepted'] is True and j['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and j['original_head']==HEAD,'Root native02 adoption absent')
    source=j['constructor'];need(set(source)=={'path','bytes','sha256'} and source['path']=='native_publication_preparation_02/make_native.py','Native02 exact adopted source required')
    frozen(source['path'],{k:source[k] for k in ('bytes','sha256')},False);return source
def adopted_artifacts(record_pin,source):
    j=decode(frozen(record_pin['path'],{k:record_pin[k] for k in ('bytes','sha256')}));safe=j['safe_artifacts'];need(isinstance(safe,dict) and safe.get(source['path'])=={k:source[k] for k in ('bytes','sha256')},'Root adopted native02 artifact map/source')
    for path,x in safe.items():
        rel(path);need(path.startswith('native_publication_preparation_02/') and not any(part in ('__pycache__','private_operations','private_tree_cache') or part.startswith('private_') for part in path.split('/')) and not path.endswith(('.pyc','.pyo')),'Native02 adopted artifact scope');frozen(path,x,False)
    return safe
def metadata_ack(record_pin):
    j=decode(frozen(record_pin['path'],{k:record_pin[k] for k in ('bytes','sha256')}))
    need(j['schema']=='pr204-root-pr-metadata-acknowledgement-v1' and j['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and j['PR']==204 and j['original_head']==HEAD and j['accepted'] is True,'Root actual PR metadata acknowledgement absent')
    need(all(j[k] is True for k in ('actual_PR_readback_verified','acknowledged_actual_PR_open_nondraft','original_native_range_delta_unchanged')) and j['original_native_custody_pin']==CUSTODY_PIN and j['expected_base_ref']=='main' and isinstance(j['expected_title'],str),'PR acknowledgement scope')
    bp(j['expected_body_pin']);return j
def tracker_row(gate,doi):
    # Exact pure row projection of the adopted revision02 tracker operation.
    notes=(gate['metadata']['title']+'. Signed original area times origin pedal to complete original sidelines; a>b>0,0<lambda<b^2,proper confocal ellipse,least N odd or divisible by4,coprime stars/reversal. '
        'Ferudun DOI10.5281/zenodo.23085904 gives the exact theorem/dn-trace identity; DOI10.5281/zenodo.23400541 supplies the credited adjacent-foot method. '
        'Source Table3 does not literally state least period; doubled-six/listed-twelve counterexample protects that qualification. '
        'PR204 and the exact centered record both show October1 object dates,which establish neither firstness,independence nor simultaneity. '
        'No novelty claim. Extensive AI;unrefereed,no conventional human peer review. PR204.')
    return ['k203b: centered original-side pedal-area product (AMR-050-0012)','','https://doi.org/'+doi,notes]
def tracker(context,pub,pubpin):
    frozen('publication_operations_01/revision_02/update_tracker.py',TRACKER_SOURCE_PIN);raw=frozen('ROOT_TRACKER_RECEIPT.json');t=decode(raw)
    for k in ('actual_tracker_row_verified','own_row_readback_verified','foreign_rows_retained','original_preappend_baseline_retained','two_fresh_full_prechecks','RAW_INSERT_ROWS','B_intentionally_blank_no_verified_chat_share_URL'):
        need(t[k] is True,'Actual tracker evidence '+k)
    need(t['PR']==204 and t['doi']==pub['doi'] and t['gate_sha256']==context['gate_pin']['sha256'] and t['publication_receipt']==pubpin and t['context']==ops.context_pin(context),'Tracker exact context')
    need(t['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and t['sheet_gid']==1254632077 and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",t['range']) is not None,'Tracker actual authorized row')
    need(t['row']==tracker_row(context['gate'],pub['doi']),'Exact tracker four cells/blank B/DOI URL')
    baseline=t['original_preappend_baseline'];need(set(baseline)=={'file','pin','row_count','counter_sha256'} and type(baseline['row_count']) is int and baseline['row_count']>0 and re.fullmatch('[0-9a-f]{64}',baseline['counter_sha256']) is not None,'Original tracker baseline evidence');bp(baseline['pin']);return raw,t
def queue_rows():
    raw=frozen(QUEUE_RECEIPT,QUEUE_RECEIPT_PIN);need(pin(raw)==QUEUE_RECEIPT_PIN,'Original QUEUE receipt identity');j=decode(raw)
    need(j['original_head']==HEAD and j['range_base']=='5f672f535a9f76da203d99020263a83d5f2de5ce' and all(j[k] is True for k in ('foreign_QUEUE_rows_identical','own_only_changed_row','all_queue_bytes_retrievable_by_immutable_native_blob_ID')),'Original QUEUE receipt scope')
    base=j['base_own_row']['text'].encode();head=j['original_QUEUE_row']['text'].encode()
    for row,key,expected in ((base,'base_own_row',BASE_ROW_PIN),(head,'original_QUEUE_row',HEAD_ROW_PIN)):
        need(pin(row)==expected and bpin(row)=={k:j[key][k] for k in ('bytes','sha256','git_blob')},'Authenticated original QUEUE row '+key)
    bc=base.decode().rstrip('\n').split('|');hc=head.decode().rstrip('\n').split('|')
    need(len(bc)==len(hc)==14 and bc[:8]==hc[:8] and (bc[8].strip(),bc[9].strip())==('queued','0/5') and (hc[8].strip(),hc[9].strip())==('claimed_solved','1/5'),'Original BASE-to-HEAD eligibility/status/effort')
    return j,base,head
def inputs(phase,adoption,ack):
    need(phase in PHASE,'Unknown phase');own_manifest=manifest();queue_rows();ready_adoption=decode(frozen(READY_ADOPTION,READY_ADOPTION_PIN));need(ready_adoption['accepted_preparation_only'] is True and ready_adoption['original_head']==HEAD,'Ready02 operational source adoption');source=native_adoption(adoption);native_safe=adopted_artifacts(adoption,source);metadata_ack(ack);context=ops.load_context(A);gate=R.gate_inputs(context['gate_pin']);pubpath,pub=ops.publication_receipt(context);pubraw=frozen('ROOT_PUBLICATION_RECEIPT.json');pubpin=pin(pubraw);traw,t=tracker(context,pub,pubpin);custody,old=originals()
    prior=actual(PHASE[phase][0]);selected=prior[3]['selected_files'];g=decode(frozen('ROOT_PUBLICATION_GATE_01.json'));seal_file=rel(g.get('package_seal_file','PACKAGE_SEAL.json'))
    need(selected.get(CASE+QUEUE_RECEIPT)==bpin(frozen(QUEUE_RECEIPT,QUEUE_RECEIPT_PIN)),'Actual prior map does not bind original QUEUE receipt')
    for name,raw in old.items():need(selected.get(CASE+'original_submitted_head/'+name)==bpin(raw),'Actual prior map does not bind archive '+name)
    expected_seal=gate['package_seal'] if phase=='merge' else pp(gate['package']+'/'+seal_file,gate['package_seal'])
    need(prior[1]['package']==gate['package'] and prior[1]['package_seal']==expected_seal,'Actual predecessor final package')
    need(all(prior[1][k]==x for k,x in BASE_COUNTS.items()),'Actual predecessor program counters')
    return {'phase':phase,'native_Root_adoption':adoption,'native_constructor':source,'native_safe_artifacts':native_safe,'PR_metadata_acknowledgement':ack,'ready02_operational_source_adoption_pin':READY_ADOPTION_PIN,'original_QUEUE_row_receipt_pin':QUEUE_RECEIPT_PIN,'actual_predecessor':{'directory':prior[0],'acceptance_pin':pin(frozen(prior[0]+'/ACCEPTANCE.json')),'pointer_pin':pin(frozen(POINTER[PHASE[phase][0]]))},'Root_publication_gate_pin':context['gate_pin'],'publication_receipt_pin':pubpin,'tracker_receipt_pin':pin(traw),'package':gate['package'],'package_seal':gate['package_seal'],'package_seal_file':seal_file,'whole_package_review_events':gate['whole_package_review_events'],'whole_package_reviews_completed':gate['whole_package_reviews_completed'],'DOI':pub['doi'],'record_id':pub['id'],'tracker_range':t['range'],'authored_manifest_pin':own_manifest}
def bind(phase,name,adoption,ack):
    dest=generation(name);need(not dest.exists(),'Fresh lifecycle generation required');j=inputs(phase,adoption,ack);j['UTC']=now();dest.mkdir();save(dest/'LIFECYCLE_INPUT_BINDINGS.json',enc(j));print(json.dumps({'bound':True,'phase':phase,'generation':name,'no_remote_mutation':True}))
def binding(phase,name):
    need((generation(name)/'LIFECYCLE_INPUT_BINDINGS.json').is_file(),'Actual lifecycle input binding missing before runtime/API');j=record(name,'LIFECYCLE_INPUT_BINDINGS.json');fresh=inputs(phase,j['native_Root_adoption'],j['PR_metadata_acknowledgement']);need({k:x for k,x in j.items() if k!='UTC'}==fresh,'Lifecycle binding drift');return j
def baseline(c,phase):
    directory,a,r,x=actual(PHASE[phase][0]);need(r['selected_map_sha256']==c.selected_digest(r['selected_files']) and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files']),'Runtime predecessor every-selected digest')
    if phase=='merge':need(a['publication_ready'] is True and a['actual_publication_verified'] is False,'Actual ready90 prerequisite')
    else:need(a['actual_merge_accepted'] is True and a['actual_publication_verified'] is True and a['actual_tracker_row_verified'] is True,'Actual integration predecessor')
    if phase=='completion':need(a['actual_factual_accepted'] is True and a['completed'] is False and a['case_percent']==98,'Actual incomplete factual98 prerequisite')
    return {'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}
def native_facts(phase,stamp,b):
    need(phase in PHASE,'Native facts phase')
    f={'schema':'pr204-native-facts-v1','original_head':HEAD,'UTC':stamp,'package_seal':pp(b['package']+'/'+rel(b['package_seal_file']),b['package_seal']),'publication_ready_gate':pp('ROOT_PUBLICATION_GATE_01.json',b['Root_publication_gate_pin']),'publication_receipt':pp('ROOT_PUBLICATION_RECEIPT.json',b['publication_receipt_pin']),'tracker_receipt':pp('ROOT_TRACKER_RECEIPT.json',b['tracker_receipt_pin'])}
    for kind in (['merge'] if phase=='factual' else ['merge','factual'] if phase=='completion' else []):
        directory,a,r,x=actual(kind);f[kind+'_receipt']=pp(directory+'/ACCEPTANCE.json',pin(frozen(directory+'/ACCEPTANCE.json')))
    return f
def queue(old,doi):
    need(re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*',doi) is not None and doi not in ('10.5281/zenodo.23085904','10.5281/zenodo.23400541'),'Actual own assigned DOI required')
    rows=old.splitlines(keepends=True);ix=[i for i,row in enumerate(rows) if b'| 5100012 / AMR-050-0012 |' in row];need(len(ix)==1,'Exactly one own QUEUE row');i=ix[0]
    receipt,base,head=queue_rows();need(rows[i]==base,'Fresh MAIN own QUEUE row must equal exact original BASE queued0/5');cells=head.decode().rstrip('\n').split('|')
    cells[10]=' https://github.com/AlecKriebel/Math/pull/204 ';cells[11]=' Qualified attributed origin-only Jacobi/direct-foot note: a>b>0,0<lambda<b^2,physical least N odd or divisible4; admitted coprime stars and reversal; signed shoelace areas in both orientations. In this strict centered domain A,B are positive forward and both negative under reversal; their product is strictly positive. Source least-period qualification explicit; repeated-list extension false. Exact theorem/formula/method overlap credited to Ferudun DOI10.5281/zenodo.23085904 and10.5281/zenodo.23400541; classical sources credited. No theorem/formula/method novelty, first disclosure, independent discovery or literal simultaneity established. Original claimed_solved1/5 retained; author turns and actual model/reasoning effort unverified. Extensive AI; unrefereed/no conventional human peer review. ';cells[12]=' ['+doi+'](https://doi.org/'+doi+') ';rows[i]='|'.join(cells).encode()+b'\n';new=b''.join(rows)
    need(len(rows[i].split(b'|'))==14 and [j for j,(x,y) in enumerate(zip(old.splitlines(keepends=True),rows)) if x!=y]==[i],'Foreign QUEUE bytes altered');return new
def original(h,phase,b,after=False,merge_commit=None):
    ack=metadata_ack(b['PR_metadata_acknowledgement']);p=h.api('pulls/204')
    need(p['head']['sha']==HEAD and p['base']['ref']==ack['expected_base_ref'] and p['title']==ack['expected_title'] and pin((p['body'] or '').encode())==ack['expected_body_pin'],'Original HEAD/Root-acknowledged PR metadata drift')
    if phase=='merge' and not after:need(p['state']=='open' and p['draft'] is False and p['merged'] is False,'PR must be actually ready before merge')
    else:
        expected=merge_commit if phase=='merge' else actual('merge')[1]['checkpoint_commit'];need(p['state']=='closed' and p['merged'] is True and p['merge_commit_sha']==expected,'Actual original-HEAD-safe GitHub merge not verified')
    custody,old=originals();head=h.api('git/commits/'+HEAD);base=h.api('git/commits/'+custody['original_range_base'])
    need(head['tree']['sha']==custody['original_tree'] and [x['sha'] for x in head['parents']]==[custody['original_sole_parent']],'Original commit identity')
    for name,raw in old.items():need(h.lookup(custody['original_tree'],NATIVE+name)==('100644','blob',bpin(raw)['git_blob']),'Original native custody '+name)
    qreceipt,base_row,head_row=queue_rows();need(h.lookup(base['tree']['sha'],Q)==('100644','blob',qreceipt['base_QUEUE_blob']['git_blob']) and qreceipt['original_QUEUE_blob']['git_blob']==custody['original_QUEUE_blob']['git_blob'],'Original native BASE/HEAD QUEUE blob identities')
    need(h.lookup(custody['original_tree'],Q)==('100644','blob',custody['original_QUEUE_blob']['git_blob']) and h.changed_leaves(base['tree']['sha'],custody['original_tree'])==set(custody['complete_original_delta']),'Original full range delta changed');v.validate_caches(h)
def selected(c,base,out,old,phase):
    need({k for k in out if k.startswith(NATIVE)}=={NATIVE+n for n in set(old)|ADDED},'Exact native27 postimage path set')
    for name,raw in old.items():
        need(name in WRAPPERS or out[NATIVE+name]==raw,'Preserved native scientific/historical bytes changed');need(base.get(CASE+'original_submitted_head/'+name)==c.byte_pin(raw),'Original archive selected identity drift')
    for k,raw in out.items():
        need(k.startswith((CASE,NATIVE)) or k in set(VIEWS)|{Q},'Foreign overlay scope')
        if k in base and k not in set(VIEWS)|{Q} and not k.startswith(NATIVE):need(c.byte_pin(raw)==base[k],'Previously selected case artifact rewrite '+k)
        if k==Q and phase!='merge':need(c.byte_pin(raw)==base[Q],'Later QUEUE rewrite')
    return {**base,**{k:c.byte_pin(raw) for k,raw in out.items()}}

def project(case,progress,stamp,phase,b,name):
    """Construct conditional metadata in memory; actual authority is receipt based."""
    case=decode(enc(case));p=decode(enc(progress));prior_completion={k:p[k] for k in p if k.startswith(('last_completed_','last_published_'))}
    need((case['PR'],case['original_head'],case['case_percent'])==(204,HEAD,PHASE[phase][1]),'Case phase predecessor')
    need((p['current_PR'],p['current_PR_workflow_percent'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'])==(204,PHASE[phase][1],46,30,203),'Program phase/counter predecessor')
    case.setdefault('historical_phase_snapshots',[]).append({'UTC':stamp,'PR':204,'prior_percent':PHASE[phase][1],'values':{k:x for k,x in case.items() if k!='historical_phase_snapshots'}})
    p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':204,'prior_percent':PHASE[phase][1],'values':{k:x for k,x in p.items() if k.startswith('current_')}})
    complete=phase=='completion';merged=phase!='merge';pct=PHASE[phase][2]
    status={'merge':'ACTUAL_PUBLICATION_TRACKER_HEAD_SAFE_MERGE_POSTIMAGE_PENDING_ACCEPTANCE','factual':'ACTUAL_MERGE_ACCEPTED_FACTUAL_POSTIMAGE_PENDING_ACCEPTANCE','completion':'QUALIFIED_ATTRIBUTED_NOTE_COMPLETION_POSTIMAGE_PENDING_OWN_ACTUAL_ACCEPTANCE'}[phase]
    remain={'merge':'Accept actual original-HEAD-safe merge; factual and own100 completion acceptance before205.','factual':'Accept factual98 MAIN then own100 completion before205.','completion':'Only after actual full-scope acceptance of this100 checkpoint may original-status-only205 intake begin.'}[phase]
    effective='This postimage is effective only after its own actual trueparent/fullforeignscope/everyselectedidentity MAIN acceptance; proposed100 totals supply no earlier completion or intake authority.'
    case.update(UTC=stamp,status=status,case_percent=pct,publication_ready=True,publication_package=b['package'],publication_package_seal=b['package_seal'],NEW_whole_package_reviews_completed=b['whole_package_reviews_completed'],whole_package_review_events=b['whole_package_review_events'],actual_Zenodo_published=True,actual_tracker_updated=True,actual_publication_verified=True,actual_tracker_row_verified=True,DOI=b['DOI'],Zenodo_record_id=b['record_id'],tracker_range=b['tracker_range'],actual_original_PR_merged=merged,actual_merge_accepted=merged,actual_factual_MAIN_accepted=complete,completed=complete,priority_clearance=True,priority_clearance_scope='bounded_priority_audit_and_qualified_attributed_note_only',priority_novelty_clearance=False,historical_firstness_independence_established=False,historical_novelty_or_firstness_established=False,qualified_attributed_note_editorially_cleared=True,current_native_source_priority_statement=NATIVE+'CURRENT_SOURCE_AND_PRIORITY.json',remaining_required_steps=remain,completion_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance=True,program_snapshot_authority_condition=effective,expected_own_actual_acceptance='publication_lifecycle_02/'+name+'/ACCEPTANCE.json',**counts(phase,complete))
    p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=pct,current_workflow_estimate_percent=pct,current_completed=complete,current_closed=merged,current_closed_without_merge=False,current_original_PR_state='closed' if merged else 'open',current_original_PR_merged=merged,current_original_PR_open_draft=False,current_Zenodo_published=True,current_DOI=b['DOI'],current_tracker_updated=True,current_tracker_range=b['tracker_range'],current_actual_publication_verified=True,current_actual_tracker_row_verified=True,current_actual_merge_accepted=merged,current_actual_factual_checkpoint_accepted=complete,current_publication_ready=True,current_priority_clearance=True,current_priority_clearance_scope='bounded_priority_audit_and_qualified_attributed_note_only',current_priority_novelty_clearance=False,current_qualified_attributed_note_editorially_cleared=True,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_publication_package=b['package'],current_publication_package_seal=b['package_seal'],current_NEW_whole_publication_package_reviews_completed=b['whole_package_reviews_completed'],current_NEW_whole_publication_package_review_active=False,current_whole_package_review_loop_complete=True,current_whole_package_review_events=b['whole_package_review_events'],current_native_source_priority_statement=NATIVE+'CURRENT_SOURCE_AND_PRIORITY.json',current_native_source_scope_presentation_update_pending=False,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,conditional_next_numeric_intake_cursor=205,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=204,next_status_only_intake_performed=False,persistent_goal_complete=False,goal_work_continuing=True,current_completion_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance=True,current_expected_own_actual_acceptance='audits/pr204_5100012/publication_lifecycle_02/'+name+'/ACCEPTANCE.json',program_snapshot_authority_condition=effective,**{k:x for k,x in counts(phase,complete).items() if k!='goal_complete'})
    if complete:
        prior=prior_completion;p.setdefault('historical_prior_completion_metadata',[]).append({'UTC':stamp,'PR':203,'superseded_by':204,'values':prior})
        for k in prior:del p[k]
        for key,size in [('fully_completed_eligible_PRs',46),('published_PRs',30)]:
            need(len(set(p[key]))==len(p[key])==size and 203 in p[key] and 204 not in p[key],'Completion list baseline');p[key].append(204)
        fraction=round(100*47/p['dated_eligible_total'],1);merge=actual('merge');factual=actual('factual')
        p.update(fully_completed_fraction_percent=fraction,workflow_estimate_percent=fraction,workflow_estimate_definition='47/dated99 completed,31published; historical denominator, not a fresh eligibility census.',last_completed_PR=204,last_completed_PR_workflow_percent=100,last_completed_original_head=HEAD,last_completed_original_QUEUE_status='claimed_solved',last_completed_original_budget=case['original_effort'],last_completed_mathematical_result_valid=True,last_completed_priority_clearance=True,last_completed_priority_clearance_scope='Bounded priority and qualified attributed note only; exact overlap/no novelty/firstness/independence/simultaneity.',last_completed_historical_firstness_or_guaranteed_novelty_certified=False,last_completed_bounded_priority_audit_complete=True,last_completed_outcome='Qualified centered-origin Jacobi/direct-foot note published/tracked/original-HEAD-safe merged.',last_completed_DOI=b['DOI'],last_completed_DOI_file_identity_verified=True,last_completed_merge_commit=merge[1]['checkpoint_commit'],last_completed_tracker_range=b['tracker_range'],last_completed_record='audits/pr204_5100012/CURRENT_CASE_STATUS.json',last_completed_actual_factual_receipt='audits/pr204_5100012/'+factual[0]+'/ACCEPTANCE.json',last_completed_actual_factual_receipt_sha256=pin(frozen(factual[0]+'/ACCEPTANCE.json'))['sha256'],last_completed_completion_effective_only_after_own_actual_acceptance=True,last_published_PR=204,last_published_DOI=b['DOI'],last_published_tracker_range=b['tracker_range'])
        p.setdefault('historical_completed_case_records',[]).append({'UTC':stamp,'PR':204,'original_head':HEAD,'DOI':b['DOI'],'completion_postimage_effective_only_after_own_actual_acceptance':True});p.setdefault('historical_skip_windows',[]).append({'UTC':stamp,'prior_last_completed_PR':203,'skipped_before_last_completion':p.get('skipped_before_last_completion',[]),'skipped_since_last_completion':p.get('skipped_since_last_completion',[])});p['skipped_before_last_completion']=[];p['skipped_since_last_completion']=[]
    note='\n'+stamp+' — PR204 '+phase+' '+str(pct)+'% postimage: actual publication '+b['DOI']+' and tracker '+b['tracker_range']+' verified; '+str(b['whole_package_reviews_completed'])+' Root-accepted final package review events. Qualified strict centered least-period signed shoelace areas in both orientations; product strictly positive. Exact Ferudun23085904/23400541 overlap/no novelty/firstness/independence/simultaneity. All20 archive/15native historical bytes and original claimed_solved1/5 retained. '+effective+' '+remain+'\n'
    return case,p,note.encode()

def overlay(c,h,parent,stamp,phase,b,name):
    # No native02 import/call until exact, independently pinned Root adoption.
    source=native_adoption(b['native_Root_adoption']);n=module('pr204_exact_Root_adopted_native02',source['path'],{k:source[k] for k in ('bytes','sha256')},False);out=n.construct(PHASE[phase][3],native_facts(phase,stamp,b));custody,old=originals()
    def add(path):out[CASE+path]=frozen(path)
    for path,x in b['native_safe_artifacts'].items():out[CASE+path]=frozen(path,x,False)
    for path in ('ROOT_PUBLICATION_RECEIPT.json','ROOT_TRACKER_RECEIPT.json',READY_ADOPTION,b['native_Root_adoption']['path'],b['PR_metadata_acknowledgement']['path'],POINTER[PHASE[phase][0]]):add(path)
    for filename in OWN_FILES:add('publication_lifecycle_02/'+filename)
    add('publication_lifecycle_02/'+name+'/LIFECYCLE_INPUT_BINDINGS.json');directory,a,r,x=actual(PHASE[phase][0])
    # Prior full maps/preparation inventories remain private; receipts bind them.
    for filename in ('ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','FOREIGN_QUEUE_RECONCILIATION.json'):add(directory+'/'+filename)
    pt=h.api('git/commits/'+parent)['tree']['sha']
    if phase=='merge':
        need(all(h.lookup(pt,k) is None for k in out if k.startswith(NATIVE)),'Native204 already exists on fresh MAIN');out[Q]=queue(v.native_body(h,Q,parent),b['DOI'])
    case=decode(v.native_body(h,CASE+'CURRENT_CASE_STATUS.json',parent));p=decode(v.native_body(h,PREFIX+'CURRENT_PROGRESS.json',parent));case,p,note=project(case,p,stamp,phase,b,name)
    out[CASE+'CURRENT_CASE_STATUS.json']=enc(case);out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
    for path in (CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md'):out[path]=v.native_body(h,path,parent)+note
    return out,old

def parents(phase,parent):
    need(phase in PHASE and valid_sha(parent),'Native parent/phase');return [parent,HEAD] if phase=='merge' else [parent]
def message(phase,digest):return 'PR204 '+phase+': qualified attributed centered-origin Jacobi/direct-foot note\n\nOriginal HEAD safe; exact contemporary overlap credited; no novelty/firstness/independence/simultaneity. Actual publication/tracker bound.\nSelected-map SHA256: '+digest
def verify(c,h,r,out,ex,phase):
    need(r['phase']==phase and r['original_head']==HEAD and r['selected_files']==ex and r['selected_map_sha256']==c.selected_digest(ex),'Preparation facts/digest')
    co=h.api('git/commits/'+r['commit'])
    need([x['sha'] for x in co['parents']]==parents(phase,r['expected_main']) and co['tree']['sha']==r['tree'] and co['message']==message(phase,c.selected_digest(ex)),'Exact native commit parents/tree/message')
    need(h.api('git/commits/'+r['expected_main'])['tree']['sha']==r['parent_tree'],'True parent tree');h.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],ex)
    for k,x in ex.items():need(h.lookup(r['tree'],k)==('100644','blob',x['git_blob']),'Every selected native identity '+k)
    changes={k for k,x in ex.items() if h.lookup(r['parent_tree'],k)!=('100644','blob',x['git_blob'])}
    need(changes==h.changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']) and changes<=set(out)==set(r['overlay_paths']),'Full foreign changed-leaf scope');v.validate_caches(h)
def accepted_aliases(phase,b,commit,stamp):
    need(phase in PHASE and valid_sha(commit),'Accepted phase/commit')
    common={'schema':'pr204-root-'+{'merge':'merge','factual':'factual','completion':'completion'}[phase]+'-receipt-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','UTC':stamp,'original_head':HEAD,'package_seal':pp(b['package']+'/'+b['package_seal_file'],b['package_seal']),'publication_receipt_sha256':b['publication_receipt_pin']['sha256'],'tracker_receipt_sha256':b['tracker_receipt_pin']['sha256'],'completed':phase=='completion','completion_facts':{'case_completed':phase=='completion',**counts(phase,phase=='completion')}}
    if phase=='merge':common.update(merged=True,original_HEAD_safe=True,full_scope_verified=True,merge_commit=commit)
    else:common.update(full_scope_MAIN_accepted=True,actual_factual_accepted=True,merge_receipt_sha256=pin(frozen(actual('merge')[0]+'/ACCEPTANCE.json'))['sha256'])
    return common
def run(phase,mode,name):
    need(mode in ('prepare','verify','accept'),'Unknown mode');b=binding(phase,name) # Missing facts fail before runtime/API.
    c,h,rv,legacy_native=v.load();base=baseline(c,phase);dest=generation(name)
    if mode=='prepare':
        need(not (dest/'PREPARATION.json').exists(),'Generation already prepared');parent=h.api('git/ref/heads/main')['object']['sha'];need(h.api('compare/'+base['commit']+'...'+parent)['status'] in ('identical','ahead'),'MAIN lacks actual predecessor')
        inherited,ack=v.reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);original(h,phase,b);stamp=now();local_pre={}
        for path in VIEWS:
            body=v.native_body(h,path,parent);f=ROOT/path;need(f.is_file() and not f.is_symlink() and pin(f.read_bytes())==pin(body),'Fresh parent/local five drift '+path);local_pre[path]=pin(body)
        save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',enc(ack));out,old=overlay(c,h,parent,stamp,phase,b,name);out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=frozen('publication_lifecycle_02/'+name+'/FOREIGN_QUEUE_RECONCILIATION.json');ex=selected(c,inherited,out,old,phase)
        tree=h.api('git/trees','POST',{'base_tree':pt,'tree':R.m.entries(c,h,out)})['sha'];commit=h.api('git/commits','POST',{'tree':tree,'parents':parents(phase,parent),'message':message(phase,c.selected_digest(ex))})['sha']
        r={'UTC':stamp,'PR':204,'phase':phase,'original_head':HEAD,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':commit,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in ex.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'local_five_expected_preimages':local_pre,'MAIN_moved':False};save(dest/'PREPARATION.json',enc(r))
    else:
        r=record(name,'PREPARATION.json');parent=r['expected_main'];ack=record(name,'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**base['selected_files'],Q:ack['current_QUEUE']};out,old=overlay(c,h,parent,r['UTC'],phase,b,name);out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=frozen('publication_lifecycle_02/'+name+'/FOREIGN_QUEUE_RECONCILIATION.json');ex=selected(c,inherited,out,old,phase)
    verify(c,h,r,out,ex,phase);main=h.api('git/ref/heads/main')['object']['sha']
    if mode in ('prepare','verify'):
        need(main==parent,'MAIN lease changed; new generation required');original(h,phase,b)
        if mode=='prepare':save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc({'UTC':now(),'PR':204,'phase':phase,'commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_parent_list_fullforeignscope_everyselectedidentity_verified':True,'original_head_unchanged':True,'actual_MAIN_acceptance':False,'case_percent':PHASE[phase][2]}))
        print(json.dumps({'mode':mode,'phase':phase,'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'MAIN_moved':False}));return
    need(h.api('compare/'+r['commit']+'...'+main)['status'] in ('identical','ahead'),'Actual MAIN lacks checkpoint');current,post=v.reconcile(c,h,r,main);tree=c.selected_current(h,main,current,r['tree']);original(h,phase,b,True,r['commit'] if phase=='merge' else None)
    for k,raw in out.items():need(c.byte_pin(raw)==ex[k] and h.lookup(tree,k)==('100644','blob',ex[k]['git_blob']),'Actual overlay identity '+k)
    v.validate_caches(h);binding(phase,name);body=enc({'selected_files':current,'selected_map_sha256':c.selected_digest(current),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
    a={'PR':204,'phase':phase,'accepted':True,'checkpoint_commit':r['commit'],'parents':[x['sha'] for x in h.api('git/commits/'+r['commit'])['parents']],'sole_parent':parent if phase!='merge' else None,'main_observed':main,'actual_tree':tree,'original_head':HEAD,'original_PR_actual_merged':True,'actual_merge_accepted':True,'actual_factual_accepted':phase in ('factual','completion'),'completion_metadata_accepted':phase=='completion','case_percent':PHASE[phase][2],'DOI':b['DOI'],'tracker_range':b['tracker_range'],'package':b['package'],'selected_files':len(current),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(current),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'exact_foreign_QUEUE_acknowledgement_if_changed':True,'original_native_custody_retained':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':True,'priority_clearance_scope':'bounded_priority_audit_and_qualified_attributed_note_only','priority_novelty_clearance':False,'historical_firstness_independence_established':False,'historical_priority_established':False,'qualified_attributed_note_editorially_cleared':True,'bounded_priority_audit_complete':True,'publication_ready':True,'actual_publication_verified':True,'actual_tracker_row_verified':True,'NEW_whole_package_reviews_completed':b['whole_package_reviews_completed'],**counts(phase,True),**accepted_aliases(phase,b,r['commit'],now())}
    save(dest/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
def own_acceptance(phase,name):
    a=record(name,'ACCEPTANCE.json');r=record(name,'PREPARATION.json');raw=frozen('publication_lifecycle_02/'+name+'/ACCEPTANCE_CURRENT_SELECTED_MAP.json',a['actual_current_map_file']);x=decode(raw)
    need(a['PR']==204 and a['accepted'] is True and a['phase']==phase and a['checkpoint_commit']==r['commit'] and a['original_head']==HEAD and a['case_percent']==PHASE[phase][2],'Own actual phase acceptance')
    need(all(a[k] is True for k in ('every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved')) and all(a[k]==value for k,value in counts(phase,True).items()),'Own actual full-scope/counters')
    need(r['selected_map_sha256']==a['selected_map_sha256']==digest_selected(r['selected_files']) and len(x['selected_files'])==a['selected_files'] and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==digest_selected(x['selected_files']),'Own actual selected digest');return a,r,x
def revalidate(c,h,a,r,x,b,phase):
    main=h.api('git/ref/heads/main')['object']['sha'];need(h.api('compare/'+r['commit']+'...'+main)['status'] in ('identical','ahead'),'Actual checkpoint absent')
    base={'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files']};current,ack=v.reconcile(c,h,base,main);c.selected_current(h,main,current,a['actual_tree']);original(h,phase,b,True,r['commit'] if phase=='merge' else None);v.validate_caches(h);return main,ack
def sync(phase,name):
    b=binding(phase,name);a,r,x=own_acceptance(phase,name);c,h,rv,n=v.load();main,ack=revalidate(c,h,a,r,x,b,phase);images=[]
    # Check every preimage before touching any one of the five views.
    for path in VIEWS:
        f=ROOT/path;post=v.native_body(h,path,r['commit']);need(c.byte_pin(post)==r['selected_files'][path] and f.is_file() and not f.is_symlink(),'View identity');old=f.read_bytes();need(pin(old) in (r['local_five_expected_preimages'][path],pin(post)),'Local five unexpected prior image '+path);images.append((path,f,old,post))
    for path,f,old,post in images:
        need(f.read_bytes()==old,'Local view changed after precheck '+path)
        if old!=post:
            tmp=f.with_name(f.name+'.pr204_lifecycle_sync_tmp')
            with tmp.open('xb') as stream:
                need(stream.write(post)==len(post),'Short view write');stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
            os.replace(tmp,f);R.fsync_directory(f.parent)
        f.chmod(0o444);need(f.read_bytes()==post,'Local five readback')
    save(generation(name)/'LOCAL_GLOBAL_FIVE_SYNC.json',enc({'UTC':now(),'PR':204,'phase':phase,'actual_checkpoint':r['commit'],'fresh_MAIN_revalidated_before_sync':main,'fresh_foreign_QUEUE_reconciliation':ack,'all_five_local_files_match_actual_checkpoint':True,'files':[{'path':path,'postimage':pin(post)} for path,f,old,post in images],**counts(phase,True)}));print(json.dumps({'phase':phase,'all_five_synced':True}))
def pointer(phase,name):
    need(phase in ('merge','factual','completion'),'Actual lifecycle pointer phase');b=binding(phase,name);a,r,x=own_acceptance(phase,name);sync_record=record(name,'LOCAL_GLOBAL_FIVE_SYNC.json')
    need(sync_record['phase']==phase and sync_record['actual_checkpoint']==r['commit'] and sync_record['all_five_local_files_match_actual_checkpoint'] is True and {row['path'] for row in sync_record['files']}==set(VIEWS),'Own actual five-view sync required before pointer')
    for path in VIEWS:
        f=ROOT/path;need(f.is_file() and not f.is_symlink() and f.stat().st_mode&0o777==0o444 and bpin(f.read_bytes())==r['selected_files'][path],'Own actual local five postimage before pointer '+path)
    c,h,rv,n=v.load();main,ack=revalidate(c,h,a,r,x,b,phase)
    j={'UTC':now(),'PR':204,'phase':phase,'directory':'publication_lifecycle_02/'+name,'checkpoint_commit':a['checkpoint_commit'],'main_observed':a['main_observed'],'fresh_MAIN_revalidated_before_pointer':main,'fresh_foreign_QUEUE_reconciliation':ack,'acceptance_pin':pin(frozen('publication_lifecycle_02/'+name+'/ACCEPTANCE.json')),'Root_recorded_only_after_actual_full_scope_acceptance':True}
    save(A/POINTER[phase],enc(j),True);print(json.dumps(j))
if __name__=='__main__':
    need(len(sys.argv)>=2,'bind PHASE GEN NATIVE_ACK BYTES SHA PR_ACK BYTES SHA | prepare/verify/accept/sync/pointer PHASE GEN');mode=sys.argv[1]
    if mode=='bind':
        need(len(sys.argv)==10 and sys.argv[5].isdigit() and sys.argv[8].isdigit(),'Exact native adoption and actual metadata acknowledgement pins required');bind(sys.argv[2],sys.argv[3],pp(sys.argv[4],{'bytes':int(sys.argv[5]),'sha256':sys.argv[6]}),pp(sys.argv[7],{'bytes':int(sys.argv[8]),'sha256':sys.argv[9]}))
    else:
        need(len(sys.argv)==4 and sys.argv[2] in PHASE,'Explicit phase/generation required')
        if mode=='sync':sync(sys.argv[2],sys.argv[3])
        elif mode=='pointer':pointer(sys.argv[2],sys.argv[3])
        else:run(sys.argv[2],mode,sys.argv[3])
