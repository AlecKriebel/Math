from pathlib import Path
import sys,subprocess,os,json,shutil,hashlib,zipfile,io,importlib.util,tempfile,contextlib
from unittest.mock import patch
R=Path(__file__).resolve().parent;A=R.parent.parent;P=A/'publication';EX=R/'tmp/extracted'; PY=sys.executable
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('prepare_integration',A/'prepare_integration.py');p=importlib.util.module_from_spec(spec);sys.modules['prepare_integration']=p;spec.loader.exec_module(p)
spec=importlib.util.spec_from_file_location('record_tracker',A/'record_tracker.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
O,F=p.load_snapshot(A/'native'/p.PREFIX);PUB={n:(P/n).read_bytes() for n in p.PUB_NAMES};SOURCE=(P/'CURRENT_PRIORITY_AND_STATUS.md').read_bytes(); DOI='10.5281/zenodo.99999999'
results={'python_optimization':sys.flags.optimize,'portable_negative_controls':[],'schema_archive_controls':[],'actual_receipt_snapshot_controls':[],'tracker_additional_controls':[]}
def need(x,msg):
 if not x:raise ValueError(msg)
manifest=json.loads((EX/'PACKAGE_MANIFEST.json').read_text())
cases=['schema_true','schema_false','schema_float','schema_zero','schema_negative','schema_two','modified','missing','extra','empty_directory','symlink','duplicate_path','duplicate_json_key','traversal','absolute','backslash','wrong_count','boolean_count','boolean_size','negative_size','wrong_hash','invalid_hash','invalid_path_normalization']
for flags in [[],['-O']]:
 for label in cases:
  with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='manifest-') as td:
   root=Path(td)/'package';shutil.copytree(EX,root);mf=json.loads(json.dumps(manifest));target=root/'requirements.txt'
   if label.startswith('schema_'):mf['schema']={'schema_true':True,'schema_false':False,'schema_float':1.0,'schema_zero':0,'schema_negative':-1,'schema_two':2}[label]
   elif label=='modified':target.write_bytes(target.read_bytes()+b'!')
   elif label=='missing':target.unlink()
   elif label=='extra':(root/'extra').write_bytes(b'x')
   elif label=='empty_directory':(root/'empty').mkdir()
   elif label=='symlink':target.unlink();target.symlink_to(EX/'requirements.txt')
   elif label=='duplicate_path':mf['files'].append(mf['files'][0]);mf['file_count']+=1
   elif label in ['traversal','absolute','backslash','invalid_path_normalization']:mf['files'][0]['path']={'traversal':'../escape','absolute':'/tmp/escape','backslash':'foo\\bar','invalid_path_normalization':'./README.md'}[label]
   elif label=='wrong_count':mf['file_count']+=1
   elif label=='boolean_count':mf['file_count']=True
   elif label=='boolean_size':mf['files'][0]['bytes']=True
   elif label=='negative_size':mf['files'][0]['bytes']=-1
   elif label=='wrong_hash':mf['files'][0]['sha256']='0'*64
   elif label=='invalid_hash':mf['files'][0]['sha256']='G'*64
   data=json.dumps(mf)
   if label=='duplicate_json_key':data=data.replace('"schema": 1','"schema": 1, "schema": 1',1)
   (root/'PACKAGE_MANIFEST.json').write_text(data)
   q=subprocess.run([PY,*flags,str(root/'verify_package.py'),'--integrity-only'],capture_output=True)
   need(q.returncode!=0,'accepted '+label)
   results['portable_negative_controls'].append({'case':label,'flags':flags,'returncode':q.returncode,'last_error':q.stderr.decode().splitlines()[-1]})
with zipfile.ZipFile(io.BytesIO(PUB['gns_verification.zip'])) as z:members={n:z.read(n) for n in z.namelist()}
for schema in [1,True,False,1.0,0,-1,2]:
 mf=p.parse_json(members['PACKAGE_MANIFEST.json']);mf['schema']=schema;alt=members|{'PACKAGE_MANIFEST.json':p.json_bytes(mf)};buffer=io.BytesIO()
 with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_DEFLATED)as z:
  for n,d in alt.items():z.writestr(n,d)
 try:p.archive_binding(buffer.getvalue(),O,PUB,SOURCE);accepted=True
 except ValueError:accepted=False
 need(accepted==(type(schema)is int and schema==1),'wrong archive schema acceptance')
 results['schema_archive_controls'].append({'schema':schema,'type':type(schema).__name__,'accepted':accepted})
# Actual final immutable bytes, separately for each receipt; mutate after first capture.
def receipt():return {'environment':'production','state':'published','receipt_saved':True,'title':p.TITLE,'doi':DOI,'doi_url':'https://doi.org/'+DOI,'id':99999999,'record_url':'https://zenodo.org/records/99999999','verified_utc':'2026-10-14T00:00:00Z','doi_resolution':{'status':'resolved','http_status':200},'files':[{'name':n,'size':len(PUB[n]),'sha256':p.sha(PUB[n])} for n in ['gns_generation_counterexample.pdf','gns_verification.zip']]}
for which in ['publication','inspection','notice']:
 with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='capture-')as td:
  root=Path(td)
  for n,d in PUB.items():(root/n).write_bytes(d)
  notice=root/'CURRENT_PRIORITY_AND_STATUS.md';notice.write_bytes(SOURCE)
  rp=root/'receipt.json';ip=root/'inspection.json';data=p.json_bytes(receipt());rp.write_bytes(data);ip.write_bytes(data)
  target={'publication':rp,'inspection':ip,'notice':notice}[which];invalid=SOURCE+b'UNVALIDATED CHANGE\n' if which=='notice' else p.json_bytes(receipt()|{'title':'wrong changed title'})
  count={};real=p.regular_bytes
  def capture(path):
   count[path]=count.get(path,0)+1;out=real(path)
   if path==target:target.write_bytes(invalid)
   return out
  with patch.object(p,'regular_bytes',side_effect=capture):files,source,val=p.publication_inputs(root,DOI,rp,ip,notice,O)
  need(source==SOURCE and files==PUB,'capture substituted changed payload')
  need(all(count[n]==1 for n in [rp,ip,notice]),'duplicate capture')
  key={'publication':'publication_receipt_sha256','inspection':'inspection_receipt_sha256','notice':'current_source_notice_sha256'}[which]
  need(val[key]==p.sha(SOURCE if which=='notice' else data),'wrong attested bytes')
  _,qrec=p.patch_queue(('prefix\n| 651 | 30001184 / OWR-3392-012 | title | .1 | 6 | 3 | 2009 | queued | 0/5 | | | |\nend').encode(),DOI)
  current=p.build_current_files(O,F,files,source,DOI,'local mocked time',qrec)
  need(current['CURRENT_SOURCE_AUDIT.md'].endswith(SOURCE),'changed notice installed')
  try:p.publication_inputs(root,DOI,rp,ip,notice,O)
  except ValueError:fresh_reject=True
  else:fresh_reject=False
  need(fresh_reject,'fresh changed input accepted')
  results['actual_receipt_snapshot_controls'].append({'target':which,'read_count':count[target],'validated_hash':val[key],'changed_disk_hash':p.sha(invalid),'fresh_changed_input_rejected':fresh_reject,'source_installed_from_capture':True})
# Pin gid, title and exact headers: these are never live calls.
for label,info,headers in [('wrong_gid',{'sheets':[{'properties':{'sheetId':1,'title':t.TAB}}]},[t.HEADERS]),('wrong_title',{'sheets':[{'properties':{'sheetId':t.GID,'title':'Other'}}]},[t.HEADERS]),('wrong_headers',{'sheets':[{'properties':{'sheetId':t.GID,'title':t.TAB}}]},[['A','B','C','D']])]:
 with patch.object(t,'call',side_effect=[info,{'values':headers},{'values':[]}]):
  try:t.inspect()
  except ValueError:rejected=True
  else:rejected=False
 need(rejected,'tracker '+label+' accepted');results['tracker_additional_controls'].append({'case':label,'rejected':True})
row=t.wanted_row(DOI)
# Malformed range/count, exact readback failure, and dispatch failure must keep marker durable.
for label in ['wrong_tab','range_two_rows','header_row','wrong_columns','wrong_readback','dispatch_failure']:
 with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='tracker-')as td:
  pending=Path(td)/'pending.json';counts={'append':0}
  updates={'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':4,'updatedCells':4}
  if label=='wrong_tab':updates['updatedRange']="'Other'!A2:D2"
  elif label=='range_two_rows':updates['updatedRange']="'Math Puzzles'!A2:D3"
  elif label=='header_row':updates['updatedRange']="'Math Puzzles'!A1:D1"
  elif label=='wrong_columns':updates['updatedColumns']=3
  def call(resource,method,params,body=None):
   if method=='append':
    counts['append']+=1;need(pending.exists(),'marker absent before dispatch')
    if label=='dispatch_failure':raise RuntimeError('mock ambiguous dispatch')
    return {'updates':updates}
   if params['range'].endswith('A2:D2'):return {'values':[['WRONG']] if label=='wrong_readback' else [row]}
   return {'values':[t.HEADERS,row]}
  with patch.object(t,'PENDING',pending),patch.object(t,'inspect',return_value=[t.HEADERS]),patch.object(t,'call',side_effect=call):
   try:t.append_once(DOI,row,{})
   except (ValueError,RuntimeError):rejected=True
   else:rejected=False
   need(rejected and counts['append']==1,'bad tracker reply accepted')
   need(p.parse_json(pending.read_bytes())['action_outcome']!='confirmed','marker incorrectly confirmed')
   with patch.object(t,'call',side_effect=AssertionError('retry must not dispatch')):
    try:t.append_once(DOI,row,{})
    except ValueError:retry_blocked=True
    else:retry_blocked=False
   need(retry_blocked,'blind retry permitted')
  results['tracker_additional_controls'].append({'case':label,'rejected':True,'durable_unconfirmed_marker':True,'blind_retry_blocked':True})
results['result']='PASS';(R/('ADDITIONAL_CONTROLS_O'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'result':'PASS','portable_rejections':len(results['portable_negative_controls']),'schema_archive_controls':len(results['schema_archive_controls']),'actual_capture_controls':len(results['actual_receipt_snapshot_controls']),'tracker_additional_controls':len(results['tracker_additional_controls'])}))
