"""Independent after214 consumer checks. All CLI runs use owned synthetic paths.

There are no live native requests. The real helper is unchanged and loaded into
an isolated module; only declared path/registry/transport dependencies of CLI
fixtures are substituted. Fixtures never have operational Root authority.
"""
from pathlib import Path
import ast,base64,contextlib,copy,datetime,difflib,hashlib,io,json,os,stat,sys,types

OWN=Path(__file__).absolute().parent
P=OWN.parents[1]
H=P/'ordered_intakes_after_PR214_20261017/preparation_01'
OLD=P/'ordered_intakes_after_PR212_20261017/preparation_01/status_only_intake_after_pr212.py'
CASE=P/'audits/pr214_30005244'
SOURCE=H/'status_only_intake_after_pr214.py'
SYNTH=CASE/'native_completion_inspect_roundtrip_02'
PUBLISHED=SYNTH/'_synthetic_checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json'
EXPECTED={'bytes':24956,'sha256':'a5dd2b47e66dff21fff04a1a0efac9edace7c911c2fba951471bac1013e7b7c0'}
CHECKS=[]

def need(x,label):
    if type(x)is not bool or not x:raise RuntimeError(label)
def check(x,label):need(x,label);CHECKS.append({'label':label,'outcome':'PASS'})
def reject(fn,label):
    try:fn()
    except (RuntimeError,ValueError,KeyError,TypeError,OSError,AttributeError,UnicodeError)as e:
        CHECKS.append({'label':label,'outcome':'REFUSED','exception':type(e).__name__});return
    raise RuntimeError('Expected refusal: '+label)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(x):return (json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def put(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb')as f:f.write(raw)
    p.chmod(0o444)
def module():
    raw=SOURCE.read_bytes();need(pin(raw)==EXPECTED,'Exact unchanged helper')
    m=types.ModuleType('owned_adversarial_after214');m.__file__=str(SOURCE)
    exec(compile(raw,str(SOURCE),'exec'),m.__dict__)
    return m
def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def verify(proof,m=None):
    m=module()if m is None else m;raw=enc(proof);return m.completion_proof(raw,pin(raw))

def native_fixture(num,status='unsolved',queue_mutator=None):
    """Canonical local native trees/blob and one-parent native commit identity."""
    pid=str(9400000+num);cells=['']*14
    cells[1]=' synthetic ';cells[2]=' '+pid+' / OWNED-TEST ';cells[8]=' '+status+' ';cells[9]=' 2/5 '
    row=('|'.join(cells)+'\n').encode();queue=b'SYNTHETIC, NEVER LIVE\n'+row
    if queue_mutator is not None:queue=queue_mutator(queue,row)
    blob=native('blob',queue)
    def tree(rows):
        rows=sorted(rows,key=lambda r:r['path'].encode()+(b'/'if r['type']=='tree'else b''))
        raw=b''.join(r['mode'].lstrip('0').encode()+b' '+r['path'].encode()+b'\0'+bytes.fromhex(r['sha'])for r in rows)
        oid=native('tree',raw);return oid,{'sha':oid,'truncated':False,'tree':rows}
    inner,iv=tree([{'path':'QUEUE.md','mode':'100644','type':'blob','sha':blob}])
    root,rv=tree([{'path':'unsolved_math_prioritization','mode':'040000','type':'tree','sha':inner}])
    parent='1'*40
    commit_raw=('tree '+root+'\nparent '+parent+'\nauthor Test <test.invalid> 1 +0000\ncommitter Test <test.invalid> 1 +0000\n\nOWNED SYNTHETIC\n').encode()
    head=native('commit',commit_raw)
    dated={'pr':num,'state':'OPEN','isDraft':True,'headRefOid':head,'headRefName':'dot/math-'+pid,
      'status_projection':{'target_ambiguity':False,'git_blob_oid':blob,'whole_QUEUE_bytes':len(queue),'whole_QUEUE_sha256':pin(queue)['sha256'],
      'targets':[{'problem_id':pid,'code':cells[2].strip(),'status':status,'turns':'2/5','selected_row_sha256':hashlib.sha256(row[:-1]).hexdigest()}]}}
    routes={'git/commits/'+head:{'sha':head,'tree':{'sha':root},'parents':[{'sha':parent}]},
      'git/trees/'+root:rv,'git/trees/'+inner:iv,'git/blobs/'+blob:{'sha':blob,'encoding':'base64','size':len(queue),'content':base64.b64encode(queue).decode()}}
    pr={'number':num,'title':pid+': owned synthetic','head':{'sha':head,'ref':dated['headRefName']},'state':'open','draft':True,'merged':False,
      'commits':1,'created_at':'opaque synthetic timestamp','updated_at':'opaque synthetic timestamp','merge_commit_sha':None,'merged_at':None,'body':'opaque only'}
    routes.update({'pulls/'+str(num):pr,'pulls/'+str(num)+'/commits?page=1&per_page=100':[{'sha':head,'parents':[{'sha':parent}]}],
      'issues/'+str(num)+'/timeline?page=1&per_page=100':[{'event':'committed','sha':head}]})
    return dated,routes

def main_fixture(name,statuses,changes=None):
    """Fresh owned filesystem, synthetic registry and local-only bounded_get."""
    root=OWN/'_private'/name;root.mkdir(parents=True)
    here=root/'ordered';here.mkdir();prior=root/'audits/pr214_30005244';prior.mkdir(parents=True)
    put(prior/'ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json',PUBLISHED.read_bytes())
    routes={};rows=[]
    for num,status in statuses.items():
        dated,local=native_fixture(num,status);rows.append(dated);routes.update(local)
    if changes is not None:changes(rows,routes)
    registry=root/'SYNTHETIC_REGISTRY.json';put(registry,enc({'rows':rows}))
    calls=[];m=module();m.HERE=here;m.PRIOR=prior;m.REGISTRY=registry;m.REGISTRY_PIN=pin(registry.read_bytes())
    def get(argv):
        need(argv[:7]==[m.GH,'api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/'+argv[-1].split('repos/AlecKriebel/Math/',1)[-1]],'Exact GET-only argv')
        route=argv[-1].split('repos/AlecKriebel/Math/',1)[1];calls.append(route)
        value=routes[route]
        if callable(value):value=value(len([r for r in calls if r==route]))
        return types.SimpleNamespace(returncode=0,stdout=enc(value),stderr=b'')
    m.bounded_get=get
    def run(num,pred=(0,'-'),head=None,terminal_pin=None):
        real=pin(PUBLISHED.read_bytes())if terminal_pin is None else terminal_pin
        args=[str(SOURCE),str(num),str(real['bytes']),real['sha256'],str(pred[0]),pred[1]]
        if head is not None:args+=['--descendant-custody-head',head]
        oldargv=sys.argv;buf=io.StringIO()
        try:
            sys.argv=args
            with contextlib.redirect_stdout(buf):m.main()
        finally:sys.argv=oldargv
        return json.loads(buf.getvalue())
    return m,root,here,rows,routes,calls,run

def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Ordinary -E -S -B -P')
    m=module();contract=json.loads((H/'EXPECTED_TERMINAL_CONTRACT.json').read_bytes())
    check(pin(SOURCE.read_bytes())==EXPECTED,'frozen consumer identity')
    check(pin((H/'EXPECTED_TERMINAL_CONTRACT.json').read_bytes())=={'bytes':4571,'sha256':'13930ca4af9ef7da0bec45b7aae268a2289254dfcfd1b0869a386a57059edcb7'},'frozen contract identity')
    manifest_raw=(H/'SOURCE_MANIFEST.json').read_bytes();manifest=json.loads(manifest_raw);seal=json.loads((H/'PREPARATION_SEAL.json').read_bytes())
    check(pin(manifest_raw)=={'bytes':3031,'sha256':'a35ffbe5d27107e9107223b6cab6ff708e3013de46b71c768883c8cdb60974e2'},'final producer manifest identity')
    check(pin((H/'PREPARATION_SEAL.json').read_bytes())=={'bytes':1129,'sha256':'3447103c26d6e9b284db225537e5e118d5f2d024ae28f39c45b3dd16b0fb2764'},'final producer seal identity')
    total=0
    for row in manifest['files']:
        path=H/row['path'];raw=path.read_bytes()
        check(Path(row['path']).name==row['path'] and pin(raw)=={k:row[k]for k in('bytes','sha256')}and stat.S_IMODE(path.lstat().st_mode)==0o444,'producer frozen leaf '+row['path']);total+=len(raw)
    check(len(manifest['files'])==12 and total==100841 and seal['selected_files']==12 and seal['selected_bytes']==total and seal['manifest']=={'path':'SOURCE_MANIFEST.json',**pin(manifest_raw)},'finite producer closure totals and seal')
    old=OLD.read_bytes();new=SOURCE.read_bytes()
    check(pin(old)=={'bytes':24760,'sha256':'0292388c3722d04cb2c11108d409c14759b61a370b0478fbbef41c92e19349eb'},'accepted predecessor exact bytes')
    funcs=lambda raw:{n.name:ast.dump(n,include_attributes=False)for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef)}
    of,nf=funcs(old),funcs(new);changed=sorted(k for k in of if of[k]!=nf[k])
    check(set(of)==set(nf)and changed==['api_argv','completion_proof','main'],'exact three changed functions and seventeen inherited functions')
    delta=''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='accepted_after212/status_only_intake_after_pr212.py',tofile='inactive_after214/status_only_intake_after_pr214.py')).encode()
    check(delta==(H/'PREDECESSOR_ADAPTATION_DELTA.patch').read_bytes(),'supplied full predecessor delta independently recomputed')
    pubraw=m.regular(PUBLISHED);check(pin(pubraw)=={'bytes':20760,'sha256':'01c99745c840fd898f5eed8da4b05d69dc0558c5e6403cee39a0c5afa0cea897'},'actually published synthetic record identity')
    proof=m.completion_proof(pubraw,pin(pubraw))
    check(proof['candidate']!=proof['actual_MAIN_observed']and proof['source_gate_checks']['refreshes_completed_before_record']==2 and proof['source_gates_verified']is True,'actual published record accepted with distinct C and R and executed source checks')
    natural=json.loads((SYNTH/'NATURAL_INSPECT_RESULT.json').read_bytes())
    check(pin((SYNTH/'NATURAL_INSPECT_RESULT.json').read_bytes())=={'bytes':1106,'sha256':'a464d72efc7899a49049bd0368d7e60137f9a3f0473b33ae1e9a50839b222610'}and natural['terminal_receipt']=={'path':str(PUBLISHED),**pin(pubraw)},'natural production inspect result binds exact saved path and bytes')
    source=CASE/'native_completion_preparation_02/ROOT_TERMINAL_INSPECTION.py'
    check(pin(source.read_bytes())=={'bytes':34201,'sha256':'d8a65d5d0c3c27d8a4ba915916135b19f0142f095724255e3a2c98f48eaf65b9'}and proof['terminal_source_pin']==pin(source.read_bytes()),'published record binds final exact production terminal source')
    check(natural['publication']['exclusive_atomic_publication']is True and natural['publication']['post_publication_mutable_guard_performed']is False,'natural exclusive publisher success and qualified observation ordering')
    # Every contract true/false fact is independently corrupted by omission,
    # wrong boolean, and numerically equal integer. Parser is actual production.
    for key in contract['required_exact_True']+contract['required_exact_False']:
        expected=key in contract['required_exact_True']
        for label,value in [('opposite',not expected),('integer',int(expected)),('null',None)]:
            bad=copy.deepcopy(proof);bad[key]=value;reject(lambda bad=bad:verify(bad,m),'terminal boolean '+key+' '+label)
        bad=copy.deepcopy(proof);bad.pop(key);reject(lambda bad=bad:verify(bad,m),'terminal boolean '+key+' omitted')
    for key,value in contract['strict_integer_facts'].items():
        for label,wrong in [('float',float(value)),('offbyone',value+1),('bool',True)]:
            bad=copy.deepcopy(proof);bad[key]=wrong;reject(lambda bad=bad:verify(bad,m),'terminal strict integer '+key+' '+label)
    for key,value in contract['required_exact_strings'].items():
        for label,wrong in [('different',value+'!'),('null',None)]:
            bad=copy.deepcopy(proof);bad[key]=wrong;reject(lambda bad=bad:verify(bad,m),'terminal exact string '+key+' '+label)
    for key in('fully_completed_eligible_PRs','published_PRs'):
        for change in('missing214','extra213','duplicate214','replace211','reversed','float'):
            bad=copy.deepcopy(proof);arr=bad[key]
            if change=='missing214':arr.pop()
            elif change=='extra213':arr.insert(-1,213)
            elif change=='duplicate214':arr.append(214)
            elif change=='replace211':arr[-2]=212
            elif change=='reversed':arr.reverse()
            else:arr[0]=float(arr[0])
            reject(lambda bad=bad:verify(bad,m),'terminal exact membership '+key+' '+change)
    for key in contract['native_oid_fields']:
        bad=copy.deepcopy(proof);bad[key]='Z'*40;reject(lambda bad=bad:verify(bad,m),'native typed lowercase SHA1 '+key)
    for key in('CAS_target','CAS_target_tree'):
        bad=copy.deepcopy(proof);bad[key]='8'*40;reject(lambda bad=bad:verify(bad,m),'native canonical alias '+key)
    for key,(lo,hi)in contract['strict_integer_bounds'].items():
        for wrong in(lo-1,hi+1,True,float(lo)):
            bad=copy.deepcopy(proof);bad[key]=wrong;reject(lambda bad=bad:verify(bad,m),'closure bounded strict integer '+key+' '+repr(wrong))
    for key in contract['nonempty_string_fields']:
        for wrong in('',None,1):
            bad=copy.deepcopy(proof);bad[key]=wrong;reject(lambda bad=bad:verify(bad,m),'qualified observation nonempty '+key+' '+repr(wrong))
    for key,wrong in [('schema','pr212-root-actual-administrative-skip-verification-v1'),('schema','pr214-root-terminal-inspector-source-acceptance-v1'),('evidence_scope','SOURCE_ONLY')]:
        bad=copy.deepcopy(proof);bad[key]=wrong;reject(lambda bad=bad:verify(bad,m),'source or old authority refused '+wrong)
    reject(lambda:m.completion_proof(pubraw,{'bytes':len(pubraw),'sha256':'0'*64}),'external terminal pin mismatch')
    for raw in(b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}',b'{"a":-Infinity}',b'{"a":1e9999}'):
        reject(lambda raw=raw:m.decode(raw),'duplicate or nonfinite JSON '+raw.decode())
    # Actual production CLI with exclusively owned synthetic registry, terminal,
    # receipts and local-only route provider. This is not an actual intake.
    seq=main_fixture('sequence',{215:'unsolved',216:'already_solved',217:'claimed_solved'})
    sm,root,here,rows,routes,calls,run=seq
    first=run(215);firstraw=(here/'PR215_PRESERVED_STATUS_INTAKE.json').read_bytes();firstrec=json.loads(firstraw)
    check(first['eligible']is False and firstrec['next_status_only_cursor']==216 and firstrec['previous_skip_pin']is None and all(r.startswith('git/')for r in calls),'owned CLI first215 nonclaimed touches original native objects only')
    second=run(216,(len(firstraw),pin(firstraw)['sha256']));secondraw=(here/'PR216_PRESERVED_STATUS_INTAKE.json').read_bytes()
    check(second['eligible']is False and json.loads(secondraw)['previous_skip_pin']==pin(firstraw),'owned CLI216 exact contiguous predecessor accepted')
    third=run(217,(len(secondraw),pin(secondraw)['sha256']))
    thirdrec=json.loads((here/'PR217_PRESERVED_STATUS_INTAKE.json').read_bytes())
    check(third['eligible']is True and third['next_status_only_cursor']==217 and thirdrec['action']=='ELIGIBLE_CUSTODY_REQUIRED_BEFORE_MATH','owned CLI217 exact claimed status stops numeric cursor')
    check(thirdrec['no_mathematical_content_reviewed']is True and thirdrec['current_status_custody']['unchanged_linear_and_timeline_checks_passed']is True,'owned eligible CLI obtains status custody without math clearance')
    eligiblefirst=main_fixture('eligible_first',{215:'claimed_solved'});ef=eligiblefirst[-1](215)
    check(ef['eligible']is True and ef['next_status_only_cursor']==215,'owned first215 eligible cannot be skipped')
    for name,num,pred,statuses in [('first_bad_predecessor',215,(1,'a'*64),{215:'unsolved'}),('missing_chain',216,(0,'-'),{216:'unsolved'}),('bad_lower',214,(0,'-'),{215:'unsolved'}),('bad_upper',10001,(0,'-'),{215:'unsolved'})]:
        fm,fr,fh,rows,routes,fc,fn=main_fixture(name,statuses)
        reject(lambda fn=fn,num=num,pred=pred:fn(num,pred),'owned CLI boundary '+name)
        check(fc==[],'no local fake native GET before refusal '+name)
    for field,value in [('eligible',True),('PR',215.0),('next_status_only_cursor',217),('preserved_QUEUE_status','claimed_solved'),('procedure_source',{'bytes':1,'sha256':'a'*64}),('previous_skip_pin',{'bytes':1,'sha256':'b'*64}),('prior_actual_completion_terminal_pin',{'bytes':1,'sha256':'c'*64}),('dated_registry_pin',{'bytes':1,'sha256':'d'*64})]:
        name='chain_'+field;fm,fr,fh,rows,routes,fc,fn=main_fixture(name,{215:'unsolved',216:'unsolved'})
        fn(215);prev=fh/'PR215_PRESERVED_STATUS_INTAKE.json';old=prev.read_bytes();bad=json.loads(old);bad[field]=value
        prev.chmod(0o644);prev.write_bytes(enc(bad));prev.chmod(0o444);fc.clear()
        reject(lambda fn=fn,bad=bad:fn(216,(len(enc(bad)),pin(enc(bad))['sha256'])),'owned CLI broken full chain '+field)
        check(fc==[],'broken chain rejected before next native access '+field)
    def duplicate(rows,routes):rows.append(copy.deepcopy(rows[0]))
    dm,dr,dh,rows,routes,dc,dn=main_fixture('duplicate_registry',{215:'unsolved'},duplicate)
    reject(lambda:dn(215),'owned CLI ambiguous registry row rejected');check(dc==[],'ambiguous registry refused before native access')
    tm,tr,th,rows,routes,tc,tn=main_fixture('tampered_registry',{215:'unsolved'})
    tm.REGISTRY.chmod(0o644);tm.REGISTRY.write_bytes(tm.REGISTRY.read_bytes()+b' ');tm.REGISTRY.chmod(0o444)
    reject(lambda:tn(215),'owned CLI wrong registry full byte pin rejected');check(tc==[],'registry mismatch refused before native access')
    # Subfunction native custody tests have independent canonical object fixtures.
    for status in('unsolved','already_solved','solved','Claimed_solved','claimed_solved'):
        d,rs=native_fixture(215,status);seen=[]
        def fetch(route):seen.append(route);return copy.deepcopy(rs[route])
        m.TREES.clear();orig=m.preserved_status(d,fetch)
        check(orig['eligible']==(status=='claimed_solved')and all(r.startswith('git/')for r in seen),'historical native exact eligibility '+status)
    for mode in('multiple_targets','ambiguous_flag','branch_target','status_mismatch','effort_mismatch','row_sha','whole_queue_pin','blob_oid','blob_size','commit_sha','multiple_parents','tree_truncated','tree_hash'):
        d,rs=native_fixture(215,'claimed_solved');proj=d['status_projection'];head=d['headRefOid']
        if mode=='multiple_targets':proj['targets'].append(copy.deepcopy(proj['targets'][0]))
        elif mode=='ambiguous_flag':proj['target_ambiguity']=True
        elif mode=='branch_target':d['headRefName']='dot/math-0'
        elif mode=='status_mismatch':proj['targets'][0]['status']='unsolved'
        elif mode=='effort_mismatch':proj['targets'][0]['turns']='3/5'
        elif mode=='row_sha':proj['targets'][0]['selected_row_sha256']='0'*64
        elif mode=='whole_queue_pin':proj['whole_QUEUE_sha256']='0'*64
        elif mode=='blob_oid':proj['git_blob_oid']='0'*40
        elif mode=='blob_size':rs[next(r for r in rs if r.startswith('git/blobs/'))]['size']+=1
        elif mode=='commit_sha':rs['git/commits/'+head]['sha']='0'*40
        elif mode=='multiple_parents':rs['git/commits/'+head]['parents'].append({'sha':'2'*40})
        elif mode=='tree_truncated':rs[next(r for r in rs if r.startswith('git/trees/'))]['truncated']=True
        else:rs[next(r for r in rs if r.startswith('git/trees/'))]['tree'][0]['sha']='9'*40
        m.TREES.clear();reject(lambda d=d,rs=rs:m.preserved_status(d,lambda route:copy.deepcopy(rs[route])),'native preserved custody corruption '+mode)
    d,rs=native_fixture(215,'claimed_solved');m.TREES.clear();fetch=lambda route:copy.deepcopy(rs[route]);orig=m.preserved_status(d,fetch)
    for mutation in('wrong_number','wrong_title','wrong_branch','notdraft','forcepush','timeline_missing','nonlinear','wrong_commit_count','changed_without_explicit','changed_wrong_explicit','nonancestor','closed_unmerged'):
        r=copy.deepcopy(rs);pr=r['pulls/215'];explicit=None
        if mutation=='wrong_number':pr['number']=True
        elif mutation=='wrong_title':pr['title']='0: synthetic'
        elif mutation=='wrong_branch':pr['head']['ref']='dot/math-0'
        elif mutation=='notdraft':pr['draft']=False
        elif mutation=='forcepush':r['issues/215/timeline?page=1&per_page=100'].append({'event':'head_ref_force_pushed'})
        elif mutation=='timeline_missing':r['issues/215/timeline?page=1&per_page=100']=[]
        elif mutation=='nonlinear':r['pulls/215/commits?page=1&per_page=100'][0]['parents'].append({'sha':'2'*40})
        elif mutation=='wrong_commit_count':pr['commits']=2
        elif mutation=='closed_unmerged':pr.update(state='closed',merged=False);explicit=pr['head']['sha']
        else:
            pr['head']['sha']='3'*40
            if mutation=='changed_wrong_explicit':explicit='4'*40
            if mutation=='nonancestor':
                explicit='3'*40;r['compare/'+orig['head']+'...'+'3'*40]={'status':'diverged','merge_base_commit':{'sha':'4'*40}}
        reject(lambda r=r,explicit=explicit:m.current_custody(215,d,orig,explicit,lambda route:copy.deepcopy(r[route])),'native current custody corruption '+mutation)
    changed=copy.deepcopy(rs);changed['pulls/215']['head']['sha']='3'*40
    changed['pulls/215/commits?page=1&per_page=100']=[{'sha':'3'*40,'parents':[{'sha':orig['head']},{'sha':'2'*40}]}]
    changed['compare/'+orig['head']+'...'+'3'*40]={'status':'ahead','merge_base_commit':{'sha':orig['head']}}
    cf=lambda route:copy.deepcopy(changed[route]);before,cu=m.current_custody(215,d,orig,'3'*40,cf)
    check(cu['full_changed_head_artifact_custody_required_before_math']is True and cu['mode']=='explicit_descendant_status_custody','explicit changed descendant remains status-only custody')
    changed['pulls/215'].update(state='closed',merged=True,draft=False,merge_commit_sha='4'*40,merged_at='opaque merged timestamp')
    before,cu=m.current_custody(215,d,orig,'3'*40,cf)
    check(cu['already_merged']is True and cu['full_changed_head_artifact_custody_required_before_math']is True,'explicit already merged descendant remains status-only custody')
    m.fresh_pr(215,d,before,cf);check(True,'fresh exact opaque metadata positive')
    for key,value in [('updated_at','changed'),('body','changed'),('draft',True),('merge_commit_sha','5'*40)]:
        bad=copy.deepcopy(changed);bad['pulls/215'][key]=value
        reject(lambda bad=bad:m.fresh_pr(215,d,before,lambda route:copy.deepcopy(bad[route])),'fresh exact metadata corruption '+key)
    # Only deliberately selected PR GET/native routes may be dispatched.
    for route in('pulls/214','pulls/216','pulls/215/merge','issues/215/comments','git/ref/heads/main','git/refs/heads/main','git/blobs/'+'A'*40,'pulls/215/commits?page=21&per_page=100'):
        reject(lambda route=route:m.api_argv(215,route),'GET firewall excludes '+route)
    for num in(True,214,10001):reject(lambda num=num:m.api_argv(num,'pulls/'+str(num)),'strict route numeric bound '+str(num))
    check(m.api_argv(10000,'pulls/10000')[5]=='GET','retained maximum10000 route')
    calls=[]
    def err(argv):calls.append(argv);return types.SimpleNamespace(returncode=1,stdout=b'{}',stderr=b'private error')
    m.ACTIVE_PR=215;m.bounded_get=err
    reject(lambda:m.api('pulls/215'),'first failed transport is refusal')
    reject(lambda:m.api('pulls/215'),'transport cannot retry after failure')
    check(len(calls)==1,'fail-stop suppresses second transport invocation')
    seen=[]
    def page_provider(route):seen.append(route);return [{}]*100
    reject(lambda:m.pages('pulls/215/commits',page_provider),'twenty full pages cannot be mistaken for complete list')
    check(len(seen)==20,'pagination bounded to twenty requests')
    # Artifact scope remains inactive: checking source controls cannot create
    # the actual Root receipt or native numeric-intake outputs.
    check(not(CASE/'ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json').exists(),'actual Root terminal absent at this independent review boundary')
    check(not(P/'ordered_intakes_after_PR214_20261017/PR215_PRESERVED_STATUS_INTAKE.json').exists(),'actual215 intake absent at this independent review boundary')
    out={'schema':'after214-independent-consumer-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','check_count':len(CHECKS),'checks':CHECKS,
      'consumer_source_pin':EXPECTED,'source_manifest_pin':pin(manifest_raw),'source_seal_pin':pin((H/'PREPARATION_SEAL.json').read_bytes()),
      'producer_payloads_rehashed':12,'producer_payload_bytes':total,'unchanged_inherited_functions':17,'changed_functions':changed if isinstance(changed,list)else['api_argv','completion_proof','main'],
      'published_synthetic_terminal_pin':pin(pubraw),'actual_intake_executions':0,'actual_Root_receipt_created':False,'network_requests':0,'provider_or_ref_or_PR_or_current_five_or_original_lock_actions':False,
      'owned_synthetic_main_used':True,'owned_synthetic_main_scope':'Only own _private subdirectories, exact unchanged helper source, overridden HERE/PRIOR/REGISTRY/REGISTRY_PIN and local-only bounded_get. Not operational authority.',
      'Goal_API_status_modified':False,'numeric_permission_granted':False}
    return out

if __name__=='__main__':
    result=main();print(json.dumps(result,sort_keys=True,indent=2))
