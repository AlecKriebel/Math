#!/usr/bin/env python3
"""Independent actual-code negative controls, confined to review-owned extraction."""
import copy,datetime,hashlib,importlib.util,json,pathlib,sys
F=pathlib.Path(__file__).resolve().parent;A=F.parents[1];P=A/'publication';R=F/'_local/extracted'
def need(c,m):
 if not c: raise RuntimeError(m)
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(b):return hashlib.sha256(b).hexdigest()
def reject(f,label):
 try:f()
 except (ValueError,RuntimeError,FileNotFoundError,KeyError) as e:return {'case':label,'rejected':True,'error':str(e)}
 raise RuntimeError('unexpected acceptance: '+label)
def main():
 v=load('actual_portable_verifier',R/'verify.py');t=load('actual_tracker',P/'append_tracker.py');b=json.loads((P/'BUILD_RECEIPT.json').read_text());anchors=b['verification_anchors'];c=json.loads((A/'CURRENT_PR1280_CONTEXT.json').read_text());out=[]
 verify=lambda:v.verify(R,anchors['manifest'],anchors['context'],anchors['snapshot'])
 for key in anchors:
  changed=dict(anchors);changed[key]='0'*64;out.append(reject(lambda:v.verify(R,changed['manifest'],changed['context'],changed['snapshot']),'wrong_outside_'+key))
 for raw in ['current_edition/PROOF.md','original_submitted/PROOF.md','provenance/SUBMITTED_SNAPSHOT.json','provenance/CURRENT_PR1280_CONTEXT.json','manuscript/main.tex',c['diagnostic_replays'][0]['program']]:
  p=R/raw;old=p.read_bytes()
  try:p.write_bytes(old+b'\nCORRUPTION\n');out.append(reject(verify,'actual_payload_'+raw))
  finally:p.write_bytes(old)
 extra=R/'unexpected_payload';extra.write_bytes(b'EXTRA')
 try:out.append(reject(verify,'extra_actual_member'))
 finally:extra.unlink()
 missing=R/'current_edition/README.md';old=missing.read_bytes();missing.unlink()
 try:out.append(reject(verify,'missing_actual_member'))
 finally:missing.write_bytes(old)
 out.append(reject(lambda:v.member(R,'Current_edition/PROOF.md'),'actual_case_mismatch'))
 for raw in ['../x','/absolute','x//y','x/./y','x/../y','x\\y']:
  out.append(reject(lambda raw=raw:v.safe(raw),'unsafe_'+raw))
 reg=c['authored_freezes'][0]
 for label,mutate in [('guessed_member_key',lambda r:r.update(path_key='path')),('input_path_as_member',lambda r:r.update(path_key='input_path')),('absolute_mode',lambda r:r.update(path_mode='absolute_under_family_root')),('escaped_base',lambda r:r.update(base='../outside')),('unknown_role',lambda r:r.update(role='source'))]:
  changed=copy.deepcopy(reg);mutate(changed);out.append(reject(lambda:v.authenticate_nested_manifests(R,[changed],require_complete=False),label))
 p=R/reg['path'];old=p.read_bytes();obj=json.loads(old);first=obj[reg['entries_key']][0]
 for label,mutate in [('nested_selected_absolute',lambda d:d[reg['entries_key']][0].update({reg['path_key']:'/MUST/NOT/FOLLOW'})),('nested_duplicate',lambda d:d[reg['entries_key']].append(copy.deepcopy(d[reg['entries_key']][0]))),('nested_hash_wrong',lambda d:d[reg['entries_key']][0].update(sha256='0'*64))]:
  bad=copy.deepcopy(obj);mutate(bad);p.write_text(json.dumps(bad));r=copy.deepcopy(reg);r['sha256']=sha(p.read_bytes())
  try:out.append(reject(lambda:v.authenticate_nested_manifests(R,[r],require_complete=False),label))
  finally:p.write_bytes(old)
 # Actual receipt absolute/source path fields are not membership: unused values
 # can be arbitrary, while the declared relative member still authenticates.
 bad=copy.deepcopy(obj)
 for row in bad[reg['entries_key']]:row['input_path']='/MISSING/PRIVATE/SOURCE';row['path']='/MISSING/PRIVATE/INVENTORY'
 p.write_text(json.dumps(bad));r=copy.deepcopy(reg);r['sha256']=sha(p.read_bytes())
 try:v.authenticate_nested_manifests(R,[r],require_complete=False)
 finally:p.write_bytes(old)
 pub={'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123'}
 positives=['[30003587]','Problem:30003587;','\nPR\t#\t1280\n','PR: https://github.com/AlecKriebel/Math/pull/1280/files?x=1','(https://github.com/AlecKriebel/Math/pull/1280/checks#L2)','See:10.5281/zenodo.123;','DOI:https://doi.org/10.5281/zenodo.123?download=1','[https://doi.org/10.5281/zenodo.123#v1]','OWR-00015585-000006','oWr_15585_6']
 negatives=['300035870','x30003587','30003587x','PR12801','XPR1280','PR1280x','#1280','https://github.com/AlecKriebel/Math/pull/1280/checksx','https://github.com/AlecKriebel/Math/pull/1280/checks/extra','https://github.com/AlecKriebel/Math/pull/1280/unknown','https://github.com/AlecKriebel/Math/pull/1280x','https://github.com/AlecKriebel/Math/pull/12800/files','https://doi.org/10.5281/zenodo.1234?x=1','10.5281/zenodo.123.2','10.5281/zenodo.123/extra','DOI:10.5281/zenodo.123x','OWR155850069','OWR15585006x']
 ids=[]
 for expected,items in [(True,positives),(False,negatives)]:
  for raw in items:
   for col in range(4):
    row=['']*4;row[col]=raw;got=t.row_has_problem_identity(row,pub);need(got is expected,'identity differs '+raw);ids.append({'text':raw,'column':col,'matches':got})
 # All eleven actual supplied fields, including nested creator and list order.
 m=load('actual_public_metadata',P/'check_public_downloads.py');wanted=c['metadata'];actual=copy.deepcopy(wanted);actual['resource_type']={'type':actual.pop('upload_type'),'subtype':actual.pop('publication_type')};actual['license']={'id':actual['license']};need(m.verify_public_metadata(actual,wanted)==sorted(wanted),'baseline actual metadata projection')
 metadata=[]
 for key in wanted:
  bad=copy.deepcopy(actual)
  if key=='upload_type':bad['resource_type']['type']='dataset'
  elif key=='publication_type':bad['resource_type']['subtype']='article'
  elif key=='license':bad['license']['id']='cc0-1.0'
  elif key=='creators':bad[key][0]['affiliation']=None
  elif key in {'keywords','related_identifiers'}:bad[key]=list(reversed(bad[key]))
  else:bad[key]=None
  metadata.append(reject(lambda:m.verify_public_metadata(bad,wanted),'actual_metadata_'+key))
 return {'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimization':sys.flags.optimize,'archive_and_schema_rejections':out,'identity_probes':ids,'metadata_rejections':metadata,'unselected_absolute_receipts_ignored':True,'scope':'Actual operative functions over the actual review-owned extracted archive/current metadata, plus clearly labeled token and corruption fixtures. No service/Git operation or frozen file mutation.'}
if __name__=='__main__':
 result=main();(F/('ADVERSARIAL_MODE_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'optimization':sys.flags.optimize,'archive_rejections':len(result['archive_and_schema_rejections']),'identity_probes':len(result['identity_probes']),'metadata_rejections':len(result['metadata_rejections'])}))
