"""Supplemental current06 actual action-entry and immediate dispatch guards."""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B')
from pathlib import Path
import json,types,contextlib,io,shutil,copy
O=Path(__file__).resolve().parent
# Reuse this review's explicit in-memory Git transport, not an older adapter.
ns={'__name__':'_entry_context_','__file__':str(O/'service_boundaries.py')};code=(O/'service_boundaries.py').read_text().split('# Captured kit bytes')[0];exec(compile(code,str(O/'service_boundaries.py'),'exec'),ns)
N=ns['N'];a=ns['a'];d=ns['d'];p=ns['p'];ctx=ns['ctx'];accepted=ns['accepted'];F=ns['freeze'];results=[];extra=a/'reviews/full_package_08'
def reject(label,fn):
 try:
  with contextlib.redirect_stdout(io.StringIO()):fn()
 except (RuntimeError,OSError,ValueError,KeyError) as ex:
  assert 'Unexpected fake' not in str(ex) and 'External dispatch' not in str(ex),(label,str(ex));results.append({'case':label,'rejected':True,'reason':str(ex)[:300]});return
 raise RuntimeError('Invalid dispatch accepted '+label)
for kind in ['pending','adverse']:
 extra.mkdir()
 if kind=='adverse':(extra/'RESULT.json').write_text('{"required_issues":[{"id":"SYNTHETIC"}]}')
 for action in ['merge','tracker_append','native_write','finalize']:
  nativepath=a/'NATIVE_PUBLICATION_RECEIPT.json';oldreceipt=nativepath.read_bytes()
  if action=='native_write':nativepath.unlink()
  reject(kind+'_entry_'+action,lambda:N[action](types.SimpleNamespace(),ctx))
  if action=='native_write':nativepath.write_bytes(oldreceipt)
 for action in ['stage','publish','inspect']:reject(kind+'_entry_kit_'+action,lambda:N['zenodo'](types.SimpleNamespace(action=action),ctx))
 shutil.rmtree(extra)
real_save=N['save'];N['subprocess'].run=lambda *args,**kw:(_ for _ in ()).throw(RuntimeError('External dispatch prohibited'))
targets={'acceptance':a/'ACCEPTANCE.json','tex':d/'research_note.tex','dependency':p/'accept_pr946.py'}
for boundary in ['tracker','native','final_metadata']:
 for kind,path in targets.items():
  old=path.read_bytes();trigger=[False]
  def save(where,value,**kw):
   real_save(where,value,**kw);name=Path(where).name
   match=name=='TRACKER_APPEND_INTENT.json' if boundary=='tracker' else name.startswith('NATIVE_PUBLICATION_CAS_') and name.endswith('_INTENT.json') if boundary=='native' else name=='PR_FINAL_METADATA_INTENT.json'
   if match:
    trigger[0]=True
    if kind=='acceptance':obj=json.loads(old);obj['accepted']=False;path.write_text(json.dumps(obj))
    else:path.write_bytes(old+b'\n')
  N['save']=save
  for q in list(a.glob('*INTENT.json')):q.unlink()
  if boundary=='tracker':
   def gws(argv):
    if argv[1:3]==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}]}
    return {'values':[['Original Problem','Solution Chat URL','DOI','Notes']]}
   N['gws']=gws;fn=lambda:N['tracker_append'](types.SimpleNamespace(),ctx)
  elif boundary=='native':
   saved=a/'NATIVE_PUBLICATION_RECEIPT.json';oldnative=saved.read_bytes();saved.unlink();fn=lambda:N['native_write'](types.SimpleNamespace(),ctx)
  else:
   # Positive full native verification is separately exercised in SERVICE_BOUNDARIES.
   N['native_verify']=lambda *args:{'synthetic_positive_to_reach_metadata_boundary':True};tracker=json.loads((a/'TRACKER_RECEIPT.json').read_text());N['gws']=lambda argv:{'range':tracker['updated_range'],'values':[tracker['row']]};fn=lambda:N['finalize'](types.SimpleNamespace(),ctx)
  reject('immediately_before_'+boundary+'_'+kind,fn);assert trigger[0],boundary;path.write_bytes(old)
  if boundary=='native':saved.write_bytes(oldnative)
N['save']=real_save
(O/'ACTION_ENTRY_CONTROLS.json').write_text(json.dumps({'status':'PASS','candidate_revision':6,'actual_current07_context':True,'all_shared_guards_real':True,'Git_and_services_fake':True,'final_metadata_native_verify_stub_disclosed':True,'actual_external_mutations':0,'cases':results,'case_count':len(results)},indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(results)}))
