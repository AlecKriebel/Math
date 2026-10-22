"""New independent SDK-key/string and exact authority/printed-head controls."""
from pathlib import Path
import subprocess,sys,os,inspect,http.client
CONTROLLED_POPEN=subprocess.Popen
engine=Path(__file__).with_name('ENGINE17.py')
text=engine.read_text().replace("DEST=REVIEW/'private'/('final_phase17_'+MODE)","DEST=REVIEW/'private'/('adversary17_'+MODE)")
exec(compile(text,str(engine)+'[new independent cohort]','exec',dont_inherit=True,optimize=0),globals())
CHILD=ROOT/'cold_reentry17.py';CHILD_PIN=sha(CHILD.read_bytes());EXTRA=[]
def cold(w,action):
    need(sha(CHILD.read_bytes())==CHILD_PIN,'Cold script changed')
    child=CONTROLLED_POPEN([sys.executable,'-I','-S','-B',str(CHILD),str(w.place),action,MS,BS],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(timeout=60);need(child.returncode==0,'Own cold failure '+err.decode())
    result=json.loads(out);need(result['pid']!=os.getpid()and result['status']=='PASS','No fresh cold success');return result
SDK=c.zenodo.ZenodoClient
def actual_parse(raw,kind,metadata):
    exchanges=[]
    class Transport:
        def __init__(self,*a,**k):pass
        def putrequest(self,method,target):exchanges.append([method,target])
        def putheader(self,key,value):
            if key=='Authorization':need(value=='Bearer OFFLINE_SENTINEL_NO_CREDENTIAL','Actual token attempted')
        def endheaders(self):pass
        def send(self,data):pass
        def getresponse(self):return types.SimpleNamespace(status=200,read=lambda maximum:raw)
        def close(self):pass
    with model.patch((http.client,'HTTPSConnection',Transport)):
        client=SDK('production','OFFLINE_SENTINEL_NO_CREDENTIAL')
        if kind=='create':value=client.create(metadata)
        elif kind=='publish':value=client.publish(777)
        elif kind=='update':value=client.update(777,metadata)
        elif kind=='get':value=client.get(777)
        else:value=client.request('PUT','https://zenodo.org/api/files/inert/upload')
    need(len(exchanges)==1,'SDK parser not called exactly once');return value,exchanges
for kind in ['create','publish','update','upload','get']:
    label='adversarial_sdk_surrogate_keys_'+kind;action='publish'if kind in {'publish','get'}else'resume-stage'
    w=setup(label,'publish'if kind in {'publish','get'}else'stage');original=getattr(w.native,kind);spy={};transport=[]
    def changed(*args):
        value=original(*args)
        selected=kind!='get'or inspect.currentframe().f_back.f_code is m.EdgeDelegate.get.__code__
        if selected and not spy:
            value['unknown_'+chr(0xd800)]={'low-key_'+chr(0xdc00):['x'+chr(0xdfff),'literal \\ud800','\x00','café Δ','😀']}
            raw=json.dumps(value,ensure_ascii=True,sort_keys=True).encode('ascii');parsed,ex=actual_parse(raw,kind,w.native.metadata)
            spy.update(body=copy.deepcopy(parsed),wire=raw);transport.extend(ex);return parsed
        return value
    setattr(w.native,kind,changed);before=len(w.native.calls)
    with w.installed():a,e=run(w,action)
    for name,data in [('ADVERSARY_ONLY_RETURNED_BODY_SPY.json',(json.dumps(spy['body'],ensure_ascii=True,sort_keys=True,indent=2)+'\n').encode('ascii')),('INERT_SDK_RESPONSE_ASCII.json',spy['wire'])]:
        with(w.place/name).open('xb')as f:f.write(data);f.flush();os.fsync(f.fileno())
    holds=[json.loads(p.read_bytes())for p in m.RUNTIME.glob('CONSUMED_RESPONSE17_HOLD_*')]
    originals=[(p,json.loads(p.read_bytes()))for p in m.PRIVATE.glob('service_original_*.json')]
    exact=[(p,v)for p,v in originals if v['kind']==kind and m.SHEET_POLICY.typed_equal(v['response'],spy['body'])]
    need(e and e['type']=='ConsumedResponseError'and len(exact)==1 and holds,'Unknown Unicode-key original not retained')
    p,v=exact[0];refs=[r for h in holds for r in h['all_consumed_response_custody']if r['path']==str(p)and r['kind']==kind]
    need(refs and all(r['expected_integrity_verified']is True and r['pin']==c.pin(p.read_bytes())for r in refs),'Exact byte custody not verified')
    need(p.read_bytes()==(json.dumps(v,ensure_ascii=True,sort_keys=True,indent=2)+'\n').encode('ascii'),'Original Unicode key normalized or representation changed')
    expected={'create':1,'publish':1,'update':4,'upload':2,'get':0}[kind]
    need(len(w.native.calls)-before==expected and not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists()and not list(m.RUNTIME.glob('PRIVATE_PUBLICATION_STATE_*')),'False success/retry')
    child=cold(w,action)
    result={'case':label,'status':'PASS_POSTCUSTODY_REJECTION','kind':kind,'error':e,'SDK_exchanges':transport,'complete_METHOD_original_retained':True,'Unicode_keys_and_values_unchanged':True,'native_calls':w.native.calls,'contested_delta':expected,'appends':w.appends,'cold':child,'actual_effects':0}
    (DEST/(label+'.json')).write_text(json.dumps(result,ensure_ascii=True,indent=2)+'\n');EXTRA.append(result);archive_completed()
w=setup('independent_authority_and_printed_head');original=w.ad_path.read_bytes();authority=json.loads(original)
authority_cases=[('whole_review_false',lambda d:d.__setitem__('whole17_review_adopted',False)),('ready_integer',lambda d:d.__setitem__('publication_ready',1)),('wrong_freeze',lambda d:d.__setitem__('source_freeze_sha256','0'*64)),('no_stage_authority',lambda d:d.__setitem__('allowed_actions',['publish'])),('duplicate_actions',lambda d:d.__setitem__('allowed_actions',['resume-stage','resume-stage'])),('unknown_action',lambda d:d.__setitem__('allowed_actions',['resume-stage','integrate']))]
for label,change in authority_cases:
    d=copy.deepcopy(authority);change(d);w.ad_path.write_text(json.dumps(d,indent=2)+'\n');w.clearance_sha=sha(w.ad_path.read_bytes())
    with w.installed():a,e=run(w,'resume-stage')
    need(e and not w.native.calls and not(m.RUNTIME/'RESUME_STAGE_INTENT.json').exists(),'Contrary bound authority reached action')
    EXTRA.append({'case':label,'status':'PASS_PREACTION_REJECTION','error':e,'actual_effects':0})
w.ad_path.write_bytes(original);w.clearance_sha=sha(original)
args=['resume-stage','--expected-pr-head','bacae693a1f2a33c89565b0bd716620885831289','--clearance-sha256',w.clearance_sha]
with w.installed():error=failure(lambda:m.main(args))
need(error['message']=='Only the accepted actual merged head is permitted'and not w.native.calls,'Original printed head not rejected safely')
EXTRA.append({'case':'original_preparation_plan_printed_head','status':'CONFIRMED_DOCUMENTATION_DEFECT','expected_head':m.HEAD,'wrong_displayed_head':args[2],'error':error,'native_calls':0,'action_intent_absent':not(m.RUNTIME/'RESUME_STAGE_INTENT.json').exists(),'actual_effects':0})
with w.installed():a,e=run(w,'resume-stage')
need(e is None and a['state']=='ready_to_publish'and len(w.native.calls)==4,'Corrected merged-head invocation failed')
EXTRA.append({'case':'corrected_merged_head_command','status':'PASS_INERT_STAGE','head':m.HEAD,'answer':a,'native_calls':w.native.calls,'actual_effects':0})
(DEST/(w.place.name+'.json')).write_text(json.dumps({'case':w.place.name,'all_controls_completed':True,'actual_effects':0},indent=2)+'\n');archive_completed()
need(not model.ATTEMPTS,'Real external adapter attempted')
(ROOT/'private/INDEPENDENT_ADVERSARY_RESULTS.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':EXTRA,'source_manifest_sha256':MS,'bootstrap_sha256':BS,'hot_calls':len(CLI_INVOCATIONS)+1,'cold_calls':5,'actual_effects':0,'readiness':False},ensure_ascii=True,indent=2)+'\n')
print(json.dumps({'new_controls':len(EXTRA),'actual_effects':0,'root_adoption_required':True,'printed_plan_command_is_not_clean':True}))
