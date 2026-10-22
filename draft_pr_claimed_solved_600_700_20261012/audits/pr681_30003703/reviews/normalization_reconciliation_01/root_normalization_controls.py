"""Root exact-current-helper controls; every receipt/transport is a fake fixture."""
from pathlib import Path
import datetime,hashlib,html,json,shutil,sys
R=Path(__file__).absolute().parent;A=R.parent.parent;base=A/'reviews/whole_package_round1/operations_controls.py'
n={'__file__':str(base),'__name__':'root_fixture_plumbing_only'};exec(compile(base.read_bytes(),str(base),'exec'),n)
n['R']=R;n['LIVE']=A;n['T']=R/'tmp'/('FAKE_FIXTURE_OPT'if sys.flags.optimize else'FAKE_FIXTURE_NORMAL')
if n['T'].exists():shutil.rmtree(n['T'])
n['T'].mkdir(parents=True)
F=n['Fixture'];checks=[];norm=[{'field':'description','kind':'plain_text_html_entities'}]
def need(c,m):
 if not c:raise RuntimeError(m)
def okay(name,fun):fun();checks.append({'case':name,'outcome':'PASS'})
def reject(name,fun):
 try:fun()
 except(ValueError,TypeError,KeyError,OSError):checks.append({'case':name,'outcome':'REJECTED'});return
 raise RuntimeError('hostile accepted '+name)
def setnorm(f,first,second):
 for name,value in zip(['ZENODO_PUBLICATION_RECEIPT.json','ZENODO_POST_PUBLICATION_INSPECTION.json'],[first,second]):f.mutate_json(name,lambda x,value=value:x.update(metadata_normalizations=value))
f=F();plain=f.inputs();description=json.loads((f.a/'publication/zenodo-deposit.json').read_bytes())['metadata']['description']
okay('exact_no_normalization_receipts_supported',lambda:need(plain['validation']['metadata_normalizations']==[],'plain list'))
okay('plain_description_hash_exact',lambda:need(plain['validation']['remote_description_representation_sha256']==hashlib.sha256(description.encode()).hexdigest(),'plain hash'))
setnorm(f,norm,norm);escaped=f.inputs()
okay('exact_documented_entity_normalization_supported',lambda:need(escaped['validation']['metadata_normalizations']==norm,'escaped list'))
okay('escaped_description_hash_exact',lambda:need(escaped['validation']['remote_description_representation_sha256']==hashlib.sha256(html.escape(description,quote=False).encode()).hexdigest(),'escaped hash'))
okay('entity_transform_reversible_and_nontrivial',lambda:need(html.unescape(html.escape(description,quote=False))==description and html.escape(description,quote=False)!=description,'not reversible'))
for label,value in [('unknown_kind',[{'field':'description','kind':'unspecified'}]),('wrong_field',[{'field':'title','kind':'plain_text_html_entities'}]),('extra_dict_field',[{'field':'description','kind':'plain_text_html_entities','ignored':True}]),('duplicate_entry',norm+norm),('string','plain_text_html_entities'),('mapping',norm[0]),('null',None),('boolean',False),('list_null',[None]),('list_boolean',[False])]:
 setnorm(f,value,value);reject('normalization_reject_'+label,f.inputs)
for label,left,right in [('first_only',norm,[]),('second_only',[],norm)]:
 setnorm(f,left,right);reject('receipt_lists_must_agree_'+label,f.inputs)
setnorm(f,norm,norm);captured=f.inputs();f.mutate_json('ZENODO_POST_PUBLICATION_INSPECTION.json',lambda x:x.update(metadata_normalizations=[]));reject('receipt_normalization_source_change_after_capture',lambda:f.h.recheck_sources(captured['validation']))
q=F();setnorm(q,norm,norm);ready=q.ready();q.final_gate('tracker',ready['publication_validation']);receipt=q.tr.append_once(ready)
okay('normalization_survives_exact_once_mock_tracker_path',lambda:need(q.append_count==1 and receipt['publication_validation']['metadata_normalizations']==norm,'tracker normalization'))
okay('tracker_readonly_reconcile_does_not_duplicate',lambda:need(q.tr.append_once(ready)['already_present']and q.append_count==1,'tracker repeated'))
q=F();setnorm(q,norm,norm);q.init_git();q.final_gate('integration');receipt=q.integration(True)
okay('normalization_survives_complete_mock_integration_push',lambda:need(receipt['pushed']and q.push_count==1 and receipt['publication_validation']['metadata_normalizations']==norm and q.git_snapshot()==q.git_initial,'integration normalization'))
reject('confirmed_mock_integration_cannot_repeat',lambda:q.integration(True));need(q.push_count==1,'repeated push')
print(json.dumps({'schema':'pr681-root-normalization-controls-v1','status':'PASS','count':len(checks),'checks':checks,'live_cloud_writes':0,'helper_sha256':{name:hashlib.sha256((A/name).read_bytes()).hexdigest()for name in ['prepare_integration.py','record_tracker.py']},'source_fixture_sha256':hashlib.sha256(base.read_bytes()).hexdigest()},indent=2,sort_keys=True))
