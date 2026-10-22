"""Independent source/cursor controls. Only temporary owned synthetic main() runs.
Actual provider/PR/native/cursor/Root-gate executions: zero.
"""
import ast,base64,contextlib,copy,datetime,hashlib,io,json,os,socket,subprocess,sys,tempfile,types
from pathlib import Path
OUT=Path(__file__).resolve().parent
PREP=OUT.parent/'preparation_01'
CHECKS=[];NEG=[];MAIN_RUNS=0
def ensure(v,msg):
    if type(v)is not bool or not v:raise AssertionError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(x):return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
def load(raw,file):
    m=types.ModuleType('owned_intake_fixture');m.__file__=str(file)
    exec(compile(raw,str(file),'exec'),m.__dict__);return m
def positive(label):CHECKS.append(label)
def refusal(label,fn,part=None):
    try:fn()
    except RuntimeError as ex:
        ensure(part is None or part in str(ex),'wrong refusal boundary '+label+': '+str(ex));NEG.append(label)
    else:raise AssertionError('accepted negative '+label)
def put(path,raw,mode=0o444):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():path.chmod(0o644)
    path.write_bytes(raw);path.chmod(mode)
def native(k,b):return hashlib.sha1(k.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def audit(event,args):
    if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.posix_spawn','os.posix_spawnp'):
        raise AssertionError('Forbidden live capability '+event)
sys.addaudithook(audit)
def main():
    raw=(PREP/'status_only_intake_after_pr212.py').read_bytes()
    ensure(pin(raw)=={'bytes':24760,'sha256':'0292388c3722d04cb2c11108d409c14759b61a370b0478fbbef41c92e19349eb'},'exact helper')
    manifest_raw=(PREP/'SOURCE_MANIFEST.json').read_bytes()
    ensure(pin(manifest_raw)=={'bytes':2052,'sha256':'685af682af841e6e38856d1ff7dfff78cf3cc02737593eff5ddd7f57cf01fe45'},'manifest pin')
    seal_raw=(PREP/'PREPARATION_SEAL.json').read_bytes()
    ensure(pin(seal_raw)=={'bytes':736,'sha256':'e3890404fa107018bae9520014695bac42babf4db495aace4bb726242b308f81'},'seal pin')
    manifests=json.loads(manifest_raw);finite=[]
    for r in manifests['files']:
        f=PREP/r['path'];b=f.read_bytes()
        ensure(f.resolve()==f and f.stat().st_mode&0o777==0o444 and pin(b)=={k:r[k] for k in ('bytes','sha256')},'finite source closure')
        finite.append({'path':r['path'],**pin(b)})
    ensure(len(finite)==8 and sum(x['bytes'] for x in finite)==80077,'eight payloads80077')
    positive('complete eight-source closure, manifest and seal rehashed0444')
    prog=PREP.parents[1]
    old=prog/'ordered_intakes_after_PR211_20261017/preparation_01/status_only_intake_after_pr211.py'
    prior=old.read_bytes()
    ensure(pin(prior)=={'bytes':22876,'sha256':'998468a6d21ab9424334dc3ee8352dcdb29967c6e19291e432faddaeaa888675'},'prior source')
    def defs(b):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,ast.FunctionDef)}
    before,after=defs(prior),defs(raw)
    unchanged=sorted(set(before)-{'api_argv','completion_proof','main'})
    ensure(len(unchanged)==17 and set(before)==set(after) and all(before[n]==after[n] for n in unchanged),'all17 inherited AST identities')
    positive('independently reconstructed17 inherited unchanged function ASTs')
    h=load(raw,PREP/'status_only_intake_after_pr212.py')
    baseline_raw=(PREP/'BASELINE_MEMBERSHIP.json').read_bytes();baseline=json.loads(baseline_raw)
    ensure(pin(baseline_raw)=={'bytes':853,'sha256':'b4fe8858faebc0f14ab956d8849af28072837807f3fc87e85a2abe356bfb2f1e'},'baseline pin')
    flags=('accepted','administrative_checkpoint_complete','advance_to_next_PR_authorized_now','all_five_local_files_match_actual_checkpoint','full_scope_verified','all_selected_native_bodies_verified','actual_Root_expected_SHA_force_false_ref_update_and_native_readback','original_stable_writer_lock_held_exact','foreign_native_tuples_preserved','coherent_before_after_ref','all53_37_memberships_unchanged','current_PR_open_draft_unmerged','no_PR_or_publication_actions')
    false=('goal_complete','completed_eligible_workflow','publication_workflow_completed','publication_ready','original_eligibility_rewritten_or_erased','numeric_advance_conditional_on_actual_Root_terminal','CAS_or_completion_inferred_from_ancestry','perpetual_or_write_time_Main_equality_claimed')
    sample={'schema':'pr212-root-actual-administrative-skip-verification-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
      'synthetic_only_not_actual_Root_authority':True,'PR':212,'administrative_checkpoint_percent':100,
      'fully_completed_count':53,'published_count':37,'last_completed_PR':211,'next_numeric_intake_cursor':213,
      'original_eligible_status':'claimed_solved','current_corrected_status':'already_solved',
      'disposition':'ADMINISTRATIVE_ADVANCE_CORRECTED_NONCLAIMED_DRAFT_UNTOUCHED',
      'candidate':'a'*40,'CAS_target':'a'*40,'tree':'b'*40,'CAS_target_tree':'b'*40,
      'actual_MAIN_observed':'c'*40,'actual_MAIN_tree':'d'*40,'selected_postimage_paths_verified':271,
      'protected_body_paths_verified':0,'native_final_ref_UTC':'synthetic observation only',
      'terminal_observation_boundary':'synthetic C != R; no actual Root or native truth',
      **baseline,**dict.fromkeys(flags,True),**dict.fromkeys(false,False)}
    def verify(x):
        b=enc(x);return h.completion_proof(b,pin(b))
    ensure(verify(sample)['actual_MAIN_observed']!=sample['candidate'],'qualified synthetic C/R accepted')
    positive('synthetic administrative terminal semantic positive, no completed/merge requirement, C!=R supported')
    for key in flags:
        for v in (False,1,None):
            bad={**sample,key:v};refusal('true flag '+key+' '+str(v),lambda b=bad:verify(b))
    for key in false:
        for v in (True,0,None):
            bad={**sample,key:v};refusal('false flag '+key+' '+str(v),lambda b=bad:verify(b))
    mutations=[('PR',True),('PR',211),('administrative_checkpoint_percent',100.0),
      ('fully_completed_count',54),('fully_completed_count',53.0),('published_count',38),('published_count',True),
      ('last_completed_PR',212),('last_completed_PR',211.0),('next_numeric_intake_cursor',212),
      ('next_numeric_intake_cursor',214),('next_numeric_intake_cursor',213.0),
      ('completed',True),('actual_original_PR_merged',True),('original_PR_already_merged',True),
      ('original_eligible_status','already_solved'),('current_corrected_status','claimed_solved'),
      ('disposition','CLAIMED_SOLVED_COMPLETE'),('CAS_target','e'*40),('CAS_target_tree','e'*40),
      ('selected_postimage_paths_verified',True),('selected_postimage_paths_verified',0),
      ('protected_body_paths_verified',False),('native_final_ref_UTC',''),('terminal_observation_boundary','')]
    for key,v in mutations:
        bad={**sample,key:v};refusal('fact '+key+' '+str(v),lambda b=bad:verify(b))
    for field in baseline:
        for kind in ('same-count-replace','bool','float','duplicate','reverse','missing'):
            b=copy.deepcopy(sample)
            if kind=='same-count-replace':b[field][-1]=212
            elif kind=='bool':b[field][0]=True
            elif kind=='float':b[field][0]=float(b[field][0])
            elif kind=='duplicate':b[field][-1]=b[field][-2]
            elif kind=='reverse':b[field].reverse()
            else:del b[field]
            refusal('membership '+field+' '+kind,lambda b=b:verify(b))
    for schema in ('pr211-root-actual-completion-verification-v1','pr212-current-case-conditional-administrative-status-v1',
       'pr212-root-conservative-administrative-disposition-v1','pr212-root-operational-source-protocol-acceptance-v1',
       'pr212-conditional-administrative-logical-packet-v1','pr212-root-fake-verification-v1'):
        b={**sample,'schema':schema};refusal('nonterminal schema '+schema,lambda b=b:verify(b))
    for scope in ('SOURCE_ONLY','CONDITIONAL_MODEL','PLANNED_ROOT_RECEIPT'):
        b={**sample,'evidence_scope':scope};refusal('nonactual scope '+scope,lambda b=b:verify(b))
    b=enc(sample);refusal('wrong external actual-terminal pin',lambda:h.completion_proof(b,{'bytes':len(b),'sha256':'0'*64}))
    oldterminal=(prog/'audits/pr211_5100063/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json').read_bytes()
    ensure(pin(oldterminal)=={'bytes':9799,'sha256':'8acd4bb99e504f4fe59b9c28a91b8fdcfc5a71502b3b0f54cb98070a29467477'},'old211 actual data pin')
    refusal('old211 actual terminal cannot grant213',lambda:h.completion_proof(oldterminal,pin(oldterminal)))
    positive('all semantic terminal/counter/list/conditional/fake-schema negative controls')
    # Unchanged main runs only in removable owned fake programs. No actual source constants,
    # registry, terminal, intake files or network are touched.
    @contextlib.contextmanager
    def fixture(status='already_solved'):
        with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=OUT) as temp:
            root=Path(temp);program=root/'program';here=program/'ordered_intakes_after_PR212_20261017';src=here/'preparation_01'
            source=src/'status_only_intake_after_pr212.py';put(source,raw);put(src/'BASELINE_MEMBERSHIP.json',baseline_raw)
            terminal=program/'audits/pr212_30005310/ROOT_ACTUAL_ADMINISTRATIVE_SKIP_VERIFICATION_01.json';put(terminal,enc(sample))
            pid='5100099';head='1'*40;parent='2'*40;branch='math/'+pid+'-synthetic'
            cells=['']*14;cells[1]=' fixture ';cells[2]=' '+pid+' / SYNTHETIC ';cells[8]=' '+status+' ';cells[9]=' 1/5 '
            row=('|'.join(cells)+'\n').encode();body=b'Owned synthetic QUEUE only\n'+row;blob=native('blob',body)
            def tree(rows):
                ordered=sorted(rows,key=lambda x:(x[0]+('/' if x[2]=='tree' else '')).encode())
                rb=b''.join(m.lstrip('0').encode()+b' '+n.encode()+b'\0'+bytes.fromhex(s) for n,m,t,s in ordered)
                oid=native('tree',rb);return oid,{'sha':oid,'truncated':False,'tree':[dict(path=n,mode=m,type=t,sha=s) for n,m,t,s in ordered]}
            inner,iv=tree([('QUEUE.md','100644','blob',blob)]);r,rv=tree([('unsolved_math_prioritization','040000','tree',inner)])
            dated={'state':'OPEN','isDraft':True,'headRefOid':head,'headRefName':branch,
              'status_projection':{'target_ambiguity':False,'git_blob_oid':blob,'whole_QUEUE_bytes':len(body),'whole_QUEUE_sha256':pin(body)['sha256'],
              'targets':[{'problem_id':pid,'code':cells[2].strip(),'status':status,'turns':'1/5','selected_row_sha256':hashlib.sha256(row[:-1]).hexdigest()}]}}
            registry=root/'registry.json';put(registry,enc({'rows':[dict(dated,pr=213),dict(dated,pr=214)]}),0o644)
            objects={'git/commits/'+head:{'sha':head,'tree':{'sha':r},'parents':[{'sha':parent}]},
              'git/trees/'+r:rv,'git/trees/'+inner:iv,'git/blobs/'+blob:{'sha':blob,'encoding':'base64','size':len(body),'content':base64.b64encode(body).decode()}}
            calls=[]
            def newmodule():
                mod=load(raw,source);mod.REGISTRY=registry;mod.REGISTRY_PIN=pin(registry.read_bytes())
                def transport(argv):
                    ensure(argv[:6]==[mod.GH,'api','--hostname','github.com','--method','GET'],'exact source GET argv')
                    route=argv[6].removeprefix('repos/AlecKriebel/Math/');calls.append(route)
                    if route in objects:v=objects[route]
                    elif route in ('pulls/213','pulls/214'):
                        num=int(route.split('/')[-1]);v={'number':num,'head':{'sha':head,'ref':branch},
                          'title':pid+': synthetic','state':'open','draft':True,'merged':False,'commits':1,
                          'created_at':'opaque','updated_at':'opaque','merge_commit_sha':None,'merged_at':None,'body':'opaque only'}
                    elif '/commits?' in route:v=[{'sha':head,'parents':[{'sha':parent}]}]
                    elif '/timeline?' in route:v=[{'event':'committed','sha':head}]
                    else:raise AssertionError('Unexpected synthetic route '+route)
                    return types.SimpleNamespace(returncode=0,stdout=enc(v),stderr=b'')
                mod.bounded_get=transport
                return mod
            def invoke(num=213,pred=None,terminalraw=None,terminalpin=None):
                global MAIN_RUNS
                if terminalraw is not None:put(terminal,terminalraw)
                mod=newmodule();t=terminal.read_bytes();tp=terminalpin or pin(t)
                predecessor=(0,'-') if pred is None else (len(pred),pin(pred)['sha256'])
                argv=[str(source),str(num),str(tp['bytes']),tp['sha256'],str(predecessor[0]),predecessor[1]]
                oldargv=sys.argv
                try:
                    sys.argv=argv
                    with contextlib.redirect_stdout(io.StringIO()) as out:mod.main()
                    MAIN_RUNS+=1;return mod,json.loads(out.getvalue())
                finally:sys.argv=oldargv
            yield types.SimpleNamespace(here=here,terminal=terminal,calls=calls,invoke=invoke,newmodule=newmodule)
    with fixture('already_solved') as f:
        m,out=f.invoke();receipt=f.here/'PR213_PRESERVED_STATUS_INTAKE.json';record=json.loads(receipt.read_bytes())
        ensure(record['eligible']is False and record['next_status_only_cursor']==214 and
          record['prior_completed_eligible_workflow']is False and record['prior_last_completed_PR']==211 and
          all(x.startswith('git/') for x in f.calls),'nonclaimed213 main no current requests, exact admin provenance')
        positive('unchanged main synthetic213 nonclaimed skips untouched to214 after terminal gate')
        original=receipt.read_bytes()
        for key,value in [('PR',True),('eligible',True),('action','ELIGIBLE'),('next_status_only_cursor',215),
          ('preserved_QUEUE_status','claimed_solved'),('prior_actual_administrative_terminal_pin',{'bytes':1,'sha256':'0'*64}),
          ('previous_skip_pin',{'bytes':1,'sha256':'0'*64}),('procedure_source',{'bytes':1,'sha256':'0'*64}),
          ('dated_registry_pin',{'bytes':1,'sha256':'0'*64})]:
            bad=json.loads(original);bad[key]=value;badraw=enc(bad);put(receipt,badraw);beforecalls=len(f.calls)
            refusal('full main bad predecessor '+key,lambda:f.invoke(214,badraw))
            ensure(len(f.calls)==beforecalls,'predecessor refused before native fetch')
        put(receipt,original);m,out=f.invoke(214,original)
        ensure(out['eligible']is False and out['next_status_only_cursor']==215,'contiguous214 skip after exact213 receipt')
        positive('full main rejects predecessor mutations before fetch and permits exact contiguous chain')
    with fixture('claimed_solved') as f:
        m,out=f.invoke();record=json.loads((f.here/'PR213_PRESERVED_STATUS_INTAKE.json').read_bytes())
        ensure(record['eligible']is True and record['next_status_only_cursor']==213 and
          record['action']=='ELIGIBLE_CUSTODY_REQUIRED_BEFORE_MATH' and
          (f.here/'PR213_eligible_evidence/PRESERVED_HEAD_QUEUE.md').exists() and
          len([r for r in f.calls if r=='pulls/213'])==2,'eligible main stops213 for custody')
        positive('unchanged main synthetic claimed213 stops cursor and requires full custody before mathematics')
    with fixture() as f:
        for label,bad in [('old211',json.loads(oldterminal)),('proposal',{**sample,'schema':'pr212-conditional-administrative-logical-packet-v1'}),
          ('source-only',{**sample,'evidence_scope':'SOURCE_ONLY'}),('fake-unaccepted',{**sample,'accepted':False})]:
            beforecalls=len(f.calls);refusal('full main prior gate '+label,lambda b=bad:f.invoke(terminalraw=enc(b)))
            ensure(len(f.calls)==beforecalls and not (f.here/'PR213_PRESERVED_STATUS_INTAKE.json').exists(),'prior gate prevents all fetch/output')
        put(f.terminal,enc(sample))
        refusal('full main wrong external pin',lambda:f.invoke(terminalpin={'bytes':len(enc(sample)),'sha256':'0'*64}))
        ensure(not f.calls,'wrong external pin before any fetch')
        positive('unchanged main rejects old/proposal/source-only/unaccepted/wrong-pin before all requests and output')
    result={'schema':'after212-independent-source-and-synthetic-cursor-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'subject':pin(raw),'source_manifest':pin(manifest_raw),'source_seal':pin(seal_raw),'finite_source_pins':finite,
      'positive_groups':CHECKS,'expected_refusals':NEG,'check_count':len(CHECKS)+len(NEG),
      'synthetic_main_successful_runs':MAIN_RUNS,'actual_production_intake_executions':0,
      'all_transport_deterministic_and_socket_subprocess_denied':True,'actual_Root_terminal_or_gate_created':False,
      'actual_PR213_or_native_requests':0,'actual_cursor_advanced':False,'existing_five_lock_Git_PR_provider_ref_effects':False,
      'mandatory_findings':[],'review_percent':100,
      'limitation':'Parser enforces pinned schema/semantics; external Root pin supplies authority. Actual-shaped synthetic dictionaries never establish actual Root origin.',
      'current_actual_completed':53,'current_actual_published':37,'last_completed':211,'actual_cursor':212,'goal_complete':False}
    b=enc(result);fd=os.open(OUT/'CONTROL_RESULT.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    try:ensure(os.write(fd,b)==len(b),'full own result');os.fsync(fd)
    finally:os.close(fd)
    print(json.dumps({'positive_groups':len(CHECKS),'expected_refusals':len(NEG),'synthetic_main_successes':MAIN_RUNS,'result':pin(b),'mandatory_findings':0}))
if __name__=='__main__':main()
