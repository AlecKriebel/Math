"""No shared guard or source gate stub: deterministic local read/accept windows."""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B')
from pathlib import Path
import json,hashlib,types,copy,contextlib,io
O=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';root=O/'private/current05_context';p=root/P.name;a=p/'audits/pr946_6000001';d=a/'preprint'
N={'__name__':'_late_refresh_','__file__':str(P/'accept_pr946.py')};raw=(P/'accept_pr946.py').read_bytes();assert hashlib.sha256(raw).hexdigest()=='62fa159687104c889195863303fa5642d877e52257bc9e4fb2bc97e89ea2b919';exec(compile(raw,N['__file__'],'exec'),N);N.update(ROOT=root,P=p,A=a,D=d);N['freeze_check'].__defaults__=(d,False);N['archive_check'].__defaults__=(d,)
F=json.loads((d/'FREEZE.json').read_bytes());FP=hashlib.sha256((d/'FREEZE.json').read_bytes()).hexdigest();ctx=N['capture_inventory'](F['operations_inventory_sha256']);accepted=json.loads((a/'ACCEPTANCE.json').read_text());originals=json.loads((O/'AUTHENTICATION_START.json').read_text())['originals'];HEAD=N['HEAD'];queue=json.loads((O/'AUTHENTICATION_START.json').read_text())['immutable_queue_row'].encode();catalog=json.dumps([x for x in json.loads((R/N['CATALOG']).read_text()) if str(x.get('id'))=='6000001']).encode()
def blob(ref,name):
 if name in originals:return (a/'original'/name).read_bytes()
 return {N['QUEUE']:queue,N['CATALOG']:catalog,N['RELATED']:b'{"groups":[]}'}[name]
def run(argv,**kw):
 if argv[:2]==['git','ls-tree']:return '100644 blob '+originals[argv[-1]]['git_blob']+'\t'+argv[-1]+'\n'
 if argv[:2]==['git','fetch']:return ''
 if argv[:2]==['git','merge-base']:return 'a'*40+'\n'
 if argv[:2]==['gh','api']:return '\n'.join([*originals,N['QUEUE']])+'\n'
 raise RuntimeError('Unexpected fake transport '+repr(argv))
N.update(blob=blob,run=run,remote_main=lambda:'a'*40,subprocess=types.SimpleNamespace(run=lambda *args,**kw:(_ for _ in ()).throw(RuntimeError('External dispatch prohibited'))));records=[]
real_read=N['read_regular'];call=lambda fn:fn()
for name in ['FULL_AUDIT.md','MANIFEST.json']:
 path=a/'reviews/full_package_05'/name;old=path.read_bytes();reads=[0];fired=[False]
 def hooked(patharg,*args,**kw):
  result=real_read(patharg,*args,**kw)
  if Path(patharg)==d/'FREEZE.json':
   reads[0]+=1
   if reads[0]==2:path.write_bytes(old+b'\n');fired[0]=True
  return result
 N['read_regular']=hooked;N['accepted_review_check'](accepted,F,ctx);N['read_regular']=real_read;assert fired[0]
 try:N['accepted_package'](ctx)
 except RuntimeError as ex:records.append({'case':'sealed_'+name+'_changed_inside_second_current_FREEZE_read','guard_returned':True,'fresh_entry_rejected':str(ex),'defect':'FP05-OPS-002','read_regular_hook_only':True,'actual_review_check_unmodified':True})
 else:raise RuntimeError('Invalid tree unexpectedly accepted')
 path.write_bytes(old)
# Real premerge_gate and real source_gate. Fake Git answers remain exact authenticated scope.
acceptpath=a/'ACCEPTANCE.json';oldacc=acceptpath.read_bytes();tex=d/'research_note.tex';oldtex=tex.read_bytes();acceptpath.unlink();source_calls=[0];real_source=N['source_gate']
def source(parent):
 result=real_source(parent);source_calls[0]+=1
 if source_calls[0]==2:tex.write_bytes(oldtex+b'\n% changed during final actual source gate\n')
 return result
N['source_gate']=source;N['pr_view']=lambda:{'number':946,'state':'OPEN','isDraft':True,'baseRefName':'main','headRefOid':HEAD,'body':(d/'ORIGINAL_PR_DESCRIPTION.md').read_text()};specs=[f"{x['round']:02d}:"+x['manifest_sha256'] for x in accepted['full_package_reviews']]
with contextlib.redirect_stdout(io.StringIO()):N['accept'](types.SimpleNamespace(freeze=FP,review=specs),ctx)
assert source_calls[0]==2 and acceptpath.exists() and tex.read_bytes()!=oldtex
try:N['accepted_package'](ctx)
except RuntimeError as ex:records.append({'case':'initial_accept_current_TeX_drift_inside_final_actual_source_gate','canonical_acceptance_written':True,'fresh_entry_rejected':str(ex),'defect':'FP05-OPS-001','actual_premerge_and_source_gate':True})
else:raise RuntimeError('Stale acceptance was not invalidated')
tex.write_bytes(oldtex);acceptpath.write_bytes(oldacc);N['source_gate']=real_source
N['accepted_package'](ctx)
(O/'LATE_REFRESH_CONTROLS.json').write_text(json.dumps({'status':'DEFECTS_REPRODUCED','candidate_revision':5,'actual_shared_guards_unmodified':True,'fake_Git_and_PR_transport_only':True,'actual_external_mutations':0,'cases':records,'restored_valid_chain_pass':True},indent=2)+'\n');print(json.dumps({'status':'DEFECTS_REPRODUCED','cases':len(records),'external_mutations':0}))
