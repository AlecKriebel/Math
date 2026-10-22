"""Actual06 native CAS/retry/uncertainty and next-status-only controls; all Git/services fake."""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B')
from pathlib import Path
import json,copy,types,contextlib,io,shutil
from datetime import datetime,timezone
O=Path(__file__).resolve().parent;source=(O/'service_boundaries.py').read_text();prefix=source[:source.index('# Native real tree')];ns={'__name__':'_native_actual06_setup_','__file__':str(O/'service_boundaries.py')}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(prefix,str(O/'service_boundaries.py'),'exec'),ns)
N=ns['N'];a=ns['a'];ctx=ns['ctx'];accepted=ns['accepted'];extra=a/'reviews/full_package_09';base_main=ns['MAIN'][0];baseline_catalog=ns['catalog'];acc=(a/'ACCEPTANCE.json').read_bytes();review=a/'reviews/full_package_08/FULL_AUDIT.md';rb=review.read_bytes();records=[]
def call(fn):
 with contextlib.redirect_stdout(io.StringIO()):return fn()
def reject(label,fn):
 try:call(fn)
 except (RuntimeError,OSError,ValueError,KeyError) as e:
  assert 'Unexpected fake' not in str(e);records.append({'case':label,'rejected':True,'reason':str(e)[:400]});return
 raise RuntimeError('INVALID ACCEPTED '+label)
for kind in ['pending','adverse','revocation','sealed_review','new_source_hold','uncertain_push']:
 ns['MAIN'][0]=base_main;ns['catalog']=baseline_catalog;review.write_bytes(rb);(a/'ACCEPTANCE.json').write_bytes(acc)
 if extra.exists():shutil.rmtree(extra)
 (a/'NATIVE_PUBLICATION_RECEIPT.json').unlink(missing_ok=True)
 for path in a.glob('NATIVE_PUBLICATION_CAS_*'):path.unlink()
 pushes=[]
 def push(argv,**kwargs):
  assert argv[:3]==['git','push','origin'];pushes.append(argv[3]);assert len(pushes)==1,'A late invalidation allowed a second dispatch'
  if kind=='uncertain_push':return types.SimpleNamespace(returncode=1,stdout='',stderr='remote outcome uncertain')
  old=ns['MAIN'][0];ns['MAIN'][0]='9'*40;ns['commits'][ns['MAIN'][0]]=copy.deepcopy(ns['commits'][old]);ns['trees'][ns['MAIN'][0]]=ns['trees'][old]
  if kind in ['pending','adverse']:
   extra.mkdir()
   if kind=='adverse':(extra/'RESULT.json').write_text('{"required_issues":[{"id":"SYNTHETIC_ADVERSE"}]}')
  elif kind=='revocation':j=json.loads(acc);j['accepted']=False;(a/'ACCEPTANCE.json').write_text(json.dumps(j))
  elif kind=='sealed_review':review.write_bytes(rb+b'\n')
  elif kind=='new_source_hold':j=json.loads(baseline_catalog);j[0]['holds']=['SYNTHETIC_NEW_HOLD'];ns['catalog']=json.dumps(j).encode()
  return types.SimpleNamespace(returncode=1,stdout='',stderr='non-fast-forward')
 N['subprocess'].run=push;reject('native_after_first_CAS_'+kind,lambda:N['native_write'](types.SimpleNamespace(),ctx));assert len(pushes)==1 and not(a/'NATIVE_PUBLICATION_RECEIPT.json').exists()
ns['catalog']=baseline_catalog;review.write_bytes(rb);(a/'ACCEPTANCE.json').write_bytes(acc)
if extra.exists():shutil.rmtree(extra)
# A separate exact actual next-status gate: no source, proof or math file is accessible.
seen=[]
def statusrun(argv,raw=False,**kw):
 seen.append(argv)
 if argv[:3]==['gh','pr','view']:
  number=int(argv[3]);return json.dumps({'number':number,'state':'CLOSED' if number==947 else 'OPEN','isDraft':number!=948,'headRefOid':str(number%10)*40,'baseRefName':'main'})
 if argv[:2]==['gh','api']:
  ref=argv[2].rsplit('=',1)[1];status='partially_solved' if ref.startswith('9') else 'claimed_solved';key='SYNTHETIC949' if ref.startswith('9') else 'SYNTHETIC950';return ('| 1 | '+key+' / status fixture | title | 0 | 0 | 0 | 0 | '+status+' | 1/5 | | | |\n').encode()
 raise RuntimeError('Math/source transport access forbidden')
N['run']=statusrun;inventory=[{'number':i,'entries':[{'id':'SYNTHETIC'+str(i)}]} for i in range(947,951)];state={'eligible_prs':list(range(947,951)),'completed_prs':[]};skipped,selected=N['gate_next'](inventory,state);assert len(skipped)==3 and selected['number']==950 and selected['math_source_read'] is False and len(seen)==6;records.append({'case':'actual_ascending_status_only_closed_nondraft_wrongstatus_skips','pass':True,'selected':950,'skipped':skipped,'commands':seen,'math_source_read':False})
(O/'NATIVE_RETRY08_CONTROLS.json').write_text(json.dumps({'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'actual_current08_context':True,'terminal08_explicitly_synthetic':True,'actual_native_source_tree_CAS_and_shared_guards':True,'only_Git_service_transport_fake':True,'actual_external_mutations':0,'cases':records,'case_count':len(records)},indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(records)}))
