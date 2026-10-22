"""Actual frozen17 parsed actions: literal UTF8 surrogate pairs lose identity."""
from pathlib import Path
import subprocess,sys,os,http.client,math
CONTROLLED_POPEN=subprocess.Popen
engine=Path(__file__).with_name('ENGINE17.py')
text=engine.read_text().replace("DEST=REVIEW/'private'/('final_phase17_'+MODE)","DEST=REVIEW/'private'/('pair_fidelity17_'+MODE)")
exec(compile(text,str(engine)+'[independent noninjective string-codec cases]','exec',dont_inherit=True,optimize=0),globals())
CHILD=ROOT/'cold_reentry17.py';CHILD_PIN=sha(CHILD.read_bytes());FINDINGS=[]
def lossless(value):
    t=type(value)
    if t is str:return ['str',[ord(c)for c in value]]
    if t is dict:return ['dict',[[lossless(k),lossless(value[k])]for k in sorted(value)]]
    if t is list:return ['list',[lossless(v)for v in value]]
    if t is bool:return ['bool',value]
    if t is int:return ['int',str(value)]
    if t is float:return ['float',value.hex()]
    if value is None:return ['null']
    raise RuntimeError('Unexpected spy type')
def store(path,data):
    with path.open('xb')as f:f.write(data);f.flush();os.fsync(f.fileno())
def cold(w,action):
    need(sha(CHILD.read_bytes())==CHILD_PIN,'Cold script changed')
    child=CONTROLLED_POPEN([sys.executable,'-I','-S','-B',str(CHILD),str(w.place),action,MS,BS],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(timeout=60);need(child.returncode==0,'Fresh cold failure '+err.decode());r=json.loads(out)
    need(r['pid']!=os.getpid()and r['status']=='PASS','Not fresh cold success');return r
SDK=c.zenodo.ZenodoClient
def parse_actual(raw,kind,metadata):
    calls=[]
    class Transport:
        def __init__(self,*a,**k):pass
        def putrequest(self,method,target):calls.append([method,target])
        def putheader(self,key,value):
            if key=='Authorization':need(value=='Bearer OFFLINE_SENTINEL_NO_CREDENTIAL','Not inert token')
        def endheaders(self):pass
        def send(self,data):pass
        def getresponse(self):return types.SimpleNamespace(status=200,read=lambda maximum:raw)
        def close(self):pass
    with model.patch((http.client,'HTTPSConnection',Transport)):
        client=SDK('production','OFFLINE_SENTINEL_NO_CREDENTIAL')
        value=client.create(metadata)if kind=='create'else client.publish(777)
    need(len(calls)==1 and calls[0][0]=='POST','Actual SDK parser not invoked once');return value,calls
for mechanism in ['title_pair_coalescence','distinct_key_collision']:
    for kind in ['create','publish']:
        label='literal_pair_'+mechanism+'_'+kind;action='resume-stage'if kind=='create'else'publish'
        w=setup(label,'stage'if kind=='create'else'publish');original=getattr(w.native,kind);spy={};exchanges=[]
        def returned(*args):
            value=original(*args)
            if mechanism=='title_pair_coalescence':value['title']='Contrary literal UTF8 title '+chr(0xd83d)+chr(0xde00)
            else:
                value['literal_pair_'+chr(0xd83d)+chr(0xde00)]='first distinct parser key'
                value['literal_pair_'+chr(0x1f600)]='second distinct parser key'
            raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8','surrogatepass')
            parsed,calls=parse_actual(raw,kind,w.native.metadata);exchanges.extend(calls);spy['body']=copy.deepcopy(parsed)
            # Complete numeric-codepoint-tagged independent object and actual
            # SDK input are durable BEFORE returning to any actor receipt path.
            store(w.place/'SDK_RESPONSE_LITERAL_SURROGATE_UTF8.bin',raw)
            store(w.place/'ADVERSARY_PARSED_ORIGINAL_LOSSLESS_CODEPOINTS.json',(json.dumps(lossless(parsed),ensure_ascii=True,sort_keys=True,indent=2)+'\n').encode('ascii'))
            return parsed
        setattr(w.native,kind,returned);before=len(w.native.calls)
        with w.installed():a,e=run(w,action)
        need(e and e['type']=='ConsumedResponseError','Contrary source unexpectedly accepted')
        holds=[json.loads(p.read_bytes())for p in m.RUNTIME.glob('CONSUMED_RESPONSE17_HOLD_*')]
        need(holds and all(h['known_id']==777 for h in holds),'Known identity/HOLD absent')
        receipts=[]
        for p in m.PRIVATE.glob('service_original_*.json'):
            body=p.read_bytes();value=json.loads(body)
            if value['kind']==kind:
                receipts.append((p,body,value))
        need(len(receipts)==1,'Not exactly one contested METHOD receipt')
        p,body,value=receipts[0];replayed=value['response']
        need(not m.SHEET_POLICY.typed_equal(replayed,spy['body']),'Expected exact-content loss did not occur')
        need(json.dumps(replayed,ensure_ascii=True,sort_keys=True)==json.dumps(spy['body'],ensure_ascii=True,sort_keys=True)if mechanism=='title_pair_coalescence'else len(replayed)==len(spy['body'])-1,'Wrong noninjectivity mechanism')
        refs=[r for h in holds for r in h['all_consumed_response_custody']if r['path']==str(p)and r['kind']==kind]
        need(refs and all(r['durable_write_returned']is True and r['expected_integrity_verified']is True and r['pin']==c.pin(body)for r in refs),'Receipt expected-byte integrity not actually passed')
        need(value['known_service_fact']['requested_or_known_id']==777,'Combined known fact absent')
        need(len(w.native.calls)-before==1 and not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists()and not list(m.RUNTIME.glob('PRIVATE_PUBLICATION_STATE_*')),'Retry or false success')
        if kind=='create':need(not(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'False stage certificate')
        strict_error=None
        try:c.strict_json(body)
        except Exception as error:strict_error={'type':type(error).__name__,'message':str(error)}
        if mechanism=='distinct_key_collision':need(strict_error and strict_error['message']=='Duplicate JSON key','Collided receipt unexpectedly strict-parseable')
        if mechanism=='title_pair_coalescence':
            difference={'original_title_codepoints':[ord(c)for c in spy['body']['title']],'actor_receipt_reloaded_title_codepoints':[ord(c)for c in replayed['title']]}
            need(difference['original_title_codepoints'][-2:]==[0xd83d,0xde00]and difference['actor_receipt_reloaded_title_codepoints'][-1:]==[0x1f600],'Unexpected pair conversion')
        else:
            difference={'original_distinct_key_codepoints':[[ord(c)for c in k]for k in spy['body']if k.startswith('literal_pair_')],'actor_receipt_reloaded_key_codepoints':[[ord(c)for c in k]for k in replayed if k.startswith('literal_pair_')],'original_key_count':len(spy['body']),'receipt_reloaded_key_count':len(replayed)}
        child=cold(w,action)
        v={'case':label,'status':'CONFIRMED_MATERIAL_NONINJECTIVE_PARSED_ORIGINAL_CUSTODY','kind':kind,'mechanism':mechanism,'error':e,'SDK_exchanges':exchanges,'SDK_admitted_original':True,'complete_original_typed_equal':False,'difference':difference,'receipt_expected_bytes_integrity_passed':True,'strict_receipt_error':strict_error,'known777_and_HOLD_preserved':True,'false_phase_certificate':False,'private_published_summary_absent':True,'native_calls':w.native.calls,'contested_delta':1,'appends':w.appends,'cold_reentry':child,'source_manifest_sha256':MS,'bootstrap_sha256':BS,'actual_effects':0,'no_claim_current_Zenodo_emits_malformed_UTF8':True}
        store(w.place/'PAIR_FIDELITY_FINDING.json',(json.dumps(v,ensure_ascii=True,indent=2)+'\n').encode('ascii'))
        (DEST/(label+'.json')).write_text(json.dumps(v,ensure_ascii=True,indent=2)+'\n');FINDINGS.append(v);archive_completed()
need(not model.ATTEMPTS,'Real external adapter attempted')
(ROOT/'private/PAIR_FIDELITY_FINDINGS.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'MATERIAL_HOLD','findings':FINDINGS,'hot_calls':len(CLI_INVOCATIONS),'cold_calls':4,'actual_effects':0,'readiness':False,'repair_required':'Lossless injective parsed-object custody across the actual SDK admitted string domain, including literal UTF8 surrogate pairs and distinct keys. ASCII JSON alone is noninjective; preserve codepoint-tagged originals or a comparably checkable exact representation, with known fact before postchecks. No normalization/laterGET substitution/retry/SDK or manifest/state-key replacement.'},ensure_ascii=True,indent=2)+'\n')
print(json.dumps({'findings':len(FINDINGS),'status':'MATERIAL_HOLD','actual_effects':0}))
