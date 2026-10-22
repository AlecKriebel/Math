"""Adversarial fake-client tests of the additional exact-ID storage operator."""
import sys
if not sys.flags.isolated or not sys.flags.no_site or sys.flags.optimize or not sys.dont_write_bytecode:
    raise RuntimeError('Use -I -S -B')
import argparse,copy,hashlib,json,tempfile,subprocess
from pathlib import Path
ROOT=Path('/Users/alec/Documents/Math')
A=ROOT/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001'
source=A/'publication_operator.py'
N={'__name__':'_tested_publication_operator_','__file__':str(source)}
exec(compile(source.read_bytes(),str(source),'exec',dont_inherit=True,optimize=0),N)
kit_path=ROOT/'zenodo_deposit_tool/zenodo.py'
raw=kit_path.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
K={'__name__':'_actual_unchanged_kit_fake_client_','__file__':str(kit_path)}
exec(compile(raw,str(kit_path),'exec',dont_inherit=True,optimize=0),K)
metadata,files=K['load_manifest'](A/'operations_runtime/zenodo-deposit.json')
ident=N['IDENT'];notes=metadata['notes'];cases=[]
def obj():
    return {'id':ident,'submitted':False,'metadata':copy.deepcopy(metadata),
        'files':[{'filename':f['name'],'filesize':f['size'],'checksum':f['md5']} for f in files]}
def reject(label,fn):
    try:fn()
    except (RuntimeError,K['DepositError'],TypeError,KeyError,ValueError):
        cases.append({'case':label,'rejected':True});return
    raise RuntimeError('Invalid case accepted: '+label)
for label,text in [('identity',notes),('exact_observed_escape',notes.replace('Python>=3.11','Python&gt;=3.11'))]:
    d=obj();d['metadata']['notes']=text;logical,changed=N['normalize_notes'](d,notes)
    assert logical['metadata']['notes']==notes and d['metadata']['notes']==text
    assert changed==(label=='exact_observed_escape')
    K['verify'](logical,metadata,files);cases.append({'case':label,'pass':True})
for label,text in [('double_escape',notes.replace('Python>=3.11','Python&amp;gt;=3.11')),
                   ('changed_requirement',notes.replace('Python>=3.11','Python&gt;=3.12')),
                   ('extra_whitespace',notes+' '),('lost_text',notes[:-1]),
                   ('HTML_wrapper','<p>'+notes+'</p>'),('unrelated_entity',notes.replace('all33','all&#51;3')),
                   ('script',notes+'<script>x</script>'),('missing',None)]:
    d=obj();d['metadata']['notes']=text;reject(label,lambda:N['normalize_notes'](d,notes))
for kind in ['title','description','author','license','filename','checksum','size','extra_file','wrong_ID','bool_ID','state_type']:
    d=obj();d['metadata']['notes']=notes.replace('Python>=3.11','Python&gt;=3.11')
    if kind=='title':d['metadata']['title']+=' changed'
    elif kind=='description':d['metadata']['description']+=' changed'
    elif kind=='author':d['metadata']['creators'][0]['name']='changed'
    elif kind=='license':d['metadata']['license']='wrong'
    elif kind=='filename':d['files'][0]['filename']='wrong'
    elif kind=='checksum':d['files'][0]['checksum']='0'*32
    elif kind=='size':d['files'][0]['filesize']+=1
    elif kind=='extra_file':d['files'].append({'filename':'unexpected','filesize':1,'checksum':'0'*32})
    elif kind=='wrong_ID':d['id']+=1
    elif kind=='bool_ID':d['id']=True
    else:d['submitted']=0
    class Fake:
        def get(self,_):return copy.deepcopy(d)
    client=N['ExistingDraftClient'](Fake(),K,metadata,files,lambda:None,False)
    reject('proxy_reject_'+kind,lambda:client.get(ident))
reject('proxy_reject_other_requested_ID',lambda:N['ExistingDraftClient'](None,K,metadata,files,lambda:None,False).get(ident+1))

class FakeAPI:
    def __init__(self,lost=False):
        self.value=obj();self.value['metadata']['notes']=notes.replace('Python>=3.11','Python&gt;=3.11')
        self.calls=[];self.lost=lost
    def get(self,i):
        assert i==ident;self.calls.append('GET');return copy.deepcopy(self.value)
    def publish(self,i):
        assert i==ident;self.calls.append('POST_PUBLISH');self.value['submitted']=True
        self.value['doi']='10.5281/zenodo.23409904'
        if self.lost:raise K['DepositError']('Synthetic response loss after publication')
        return copy.deepcopy(self.value)

with tempfile.TemporaryDirectory(prefix='notes-operator-',dir=Path(__file__).resolve().parent/'private') as tmp:
    K['STATE_DIR']=Path(tmp)/'state'
    K['doi_status']=lambda doi:{'status':'synthetic_resolved','doi':doi}
    manifest=(A/'operations_runtime/zenodo-deposit.json').resolve()
    place=K['state_path'](manifest,'production')
    for lost in [False,True]:
        K['save_state'](place,{'manifest':str(manifest),'environment':'production','id':ident})
        api=FakeAPI(lost);guards=[]
        proxy=N['ExistingDraftClient'](api,K,metadata,files,lambda:guards.append('fresh_guard'),True)
        r=K['run'](argparse.Namespace(command='publish',manifest=manifest,sandbox=False,confirm_id=ident,check_doi=True),client=proxy)
        assert r['state']=='published' and r['id']==ident and r['doi']=='10.5281/zenodo.23409904'
        assert api.calls.count('POST_PUBLISH')==proxy.posts==1 and len(guards)==2
        assert r['files']==[{'name':f['name'],'size':f['size'],'sha256':f['sha256']} for f in files]
        again=K['run'](argparse.Namespace(command='inspect',manifest=manifest,sandbox=False,check_doi=True),client=proxy)
        assert again['state']=='published' and api.calls.count('POST_PUBLISH')==1
        cases.append({'case':'unchanged_kit_single_POST_'+('lost_response' if lost else 'success'),
                      'pass':True,'calls':api.calls,'fresh_guards':len(guards)})
        reject('second_direct_POST_forbidden_'+str(lost),lambda:proxy.publish(ident))
    # A rejected fresh logical guard prevents any real API mutation.
    api=FakeAPI()
    def no():raise RuntimeError('Synthetic revoked complete approval')
    proxy=N['ExistingDraftClient'](api,K,metadata,files,no,True)
    reject('fresh_guard_blocks_POST',lambda:proxy.publish(ident));assert api.calls==[] and proxy.posts==0
    proxy=N['ExistingDraftClient'](api,K,metadata,files,lambda:None,False)
    reject('inspect_client_cannot_POST',lambda:proxy.publish(ident));assert api.calls==[]
    need_methods=['create','update','upload','request','edit','discard']
    assert not any(hasattr(proxy,name) for name in need_methods)
    cases.append({'case':'no_create_update_upload_or_generic_request_path','pass':True})
    for already in [False,True]:
        revoked=[False]
        class RevokingAPI(FakeAPI):
            def get(self,i):
                value=super().get(i);revoked[0]=True;return value
        api=RevokingAPI();api.value['submitted']=already
        def current_guard():
            if revoked[0]:raise RuntimeError('Synthetic approval revoked during final GET')
        proxy=N['ExistingDraftClient'](api,K,metadata,files,current_guard,True)
        reject('final_GET_revocation_blocks_POST_or_return_'+str(already),lambda:proxy.publish(ident))
        assert api.calls==['GET'] and proxy.posts==0

probe='import pathlib,sys; p=pathlib.Path(sys.argv[1]); exec(compile(p.read_bytes(),str(p),"exec",optimize=0),{"__name__":"_startup_probe_","__file__":str(p)})'
for label,flags in [('missing_S',['-I','-B']),('missing_I',['-S','-B']),
                    ('missing_B',['-I','-S']),('optimized',['-I','-S','-B','-O'])]:
    proc=subprocess.run([sys.executable,*flags,'-c',probe,str(source)],capture_output=True,text=True)
    assert proc.returncode!=0 and 'Use Python -I -S -B at optimization zero' in proc.stderr
    cases.append({'case':'actual_startup_rejects_'+label,'pass':True,'returncode':proc.returncode})
proc=subprocess.run([sys.executable,'-I','-S','-B','-c',probe,str(source)],capture_output=True,text=True)
assert proc.returncode==0
cases.append({'case':'actual_required_startup_imports_without_dispatch','pass':True})
report={'status':'PASS','utc':K['datetime'].now(K['timezone'].utc).isoformat(),
    'operator_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'unchanged_repository_kit_sha256':hashlib.sha256(raw).hexdigest(),
    'case_count':len(cases),'cases':cases,'all_API_clients_fake':True,'actual_external_mutations':0,
    'scope_limit':'These unit/fake-kit cases are not a replacement for a NEW entire postmerge package/operator review with real core guards in an isolated fake transport fixture.'}
(Path(__file__).resolve().parent/'OPERATOR36_CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','cases':len(cases),'operator_sha256':report['operator_sha256'],'actual_external_mutations':0}))
