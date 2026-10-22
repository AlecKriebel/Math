#!/usr/bin/env python3
"""Mock-only tests: all fixtures in fresh --scratch directories; no live services."""
import argparse,contextlib,copy,hashlib,importlib.util,io,json,os
from pathlib import Path
import sys,tempfile,threading
from unittest.mock import patch

def need(x,s):
 if not x:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
class Fixture:
 def __init__(self,inp,w,edition='final'):
  self.root=w/'sweep';self.audit=self.root/'audits/pr1132_30005952';(self.audit/'private').mkdir(parents=True)
  pref='' if edition=='old' else edition+'_';self.helper=self.audit/'reconcile_external_ledger.py';self.helper.write_bytes((inp/(pref+'reconcile_external_ledger.py')).read_bytes());self.pp=self.audit/'LEDGER_RECONCILIATION_PLAN.json';self.pp.write_bytes((inp/(pref+'LEDGER_RECONCILIATION_PLAN.json')).read_bytes());self.plan=json.loads(self.pp.read_text());self.row=self.plan['proposed_row'];self.live=json.loads((inp/'live_pr.json').read_text());self.inv={'pull_requests':[{'number':1132,'headRefOid':self.live['head']['sha'],'baseRefOid':self.live['base']['sha'],'body':self.live['body']}]}
  b=self.root/'raw/pr1132/zenodo_23063072.json';b.parent.mkdir(parents=True);b.write_bytes((inp/'provider_baseline.json').read_bytes());self.provider=json.loads(b.read_bytes());self.account={'total':0,'records':[]};self.sheet=[self.plan['schema_columns']];self.appends=0;self.reads=0;self.afterdup=False;self.unknown=False;self.badresponse=False;self.resolution={'status':200,'final_url':'https://zenodo.org/records/23063072'};self.lock=threading.Lock();(self.audit/'review_pin.txt').write_bytes(b'reviewed');self.adopt={'ready_for_existing_publication_record':True,'plan_sha256':sha(self.pp.read_bytes()),'helper_sha256':sha(self.helper.read_bytes()),'review_pins':[{'path':'review_pin.txt','sha256':sha(b'reviewed')}]}
  (self.root/'publication_check.py').write_text("SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'\ndef get(url): raise RuntimeError('LIVE CALL FORBIDDEN')\n")
  (self.root/'sweep_io.py').write_text("import json\ndef atomic_json(p,v):\n p.parent.mkdir(parents=True,exist_ok=True)\n p.write_text(json.dumps(v,indent=2)+'\\n')\n")
  reader=self.root/'audits/pr0399_30001179/prepublication_check.py';reader.parent.mkdir(parents=True);reader.write_text("import json\nfrom pathlib import Path\ndef verify_destination(): pass\nclass zenodo:\n @staticmethod\n def token_for(x): return 'MOCK-NOT-A-TOKEN'\n class ZenodoClient:\n  def __init__(self,*a): pass\ndef account_search(c,q): return json.loads((Path(__file__).resolve().parents[2]/'mock_account.json').read_text())\n")
 def sync(self):
  put(self.root/'rest_inventory.json',self.inv);put(self.root/'mock_account.json',self.account);put(self.audit/'ROOT_LEDGER_REVIEW_ACCEPTANCE.json',self.adopt)
 def load(self,n='one'):
  for key in ['publication_check','sweep_io']:sys.modules.pop(key,None)
  sys.path.insert(0,str(self.root));s=importlib.util.spec_from_file_location('mock1132_'+n,self.helper);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.cli=self.cli;m.get=self.get;m.subprocess.check_output=lambda *a,**k:'main\n';return m
 def get(self,u):
  if u=='https://zenodo.org/api/records/23063072':return json.dumps(self.provider).encode(),{'status':200}
  if u=='https://doi.org/10.5281/zenodo.23063072':return b'',self.resolution
  raise RuntimeError('UNMOCKED URL '+u)
 def cli(self,a):
  with self.lock:
   if a[:2]==['gh','api']:
    if a[2].endswith('/pulls/1132'):return copy.deepcopy(self.live)
    if a[2].endswith('/git/ref/heads/main'):return {'object':{'sha':'a'*40}}
   if a[:5]==['gws','sheets','spreadsheets','values','get']:
    self.reads+=1;return {'values':copy.deepcopy(self.sheet+([self.row] if self.afterdup and self.reads>=2 else []))}
   if a[:5]==['gws','sheets','spreadsheets','values','append']:
    p=json.loads(a[a.index('--params')+1]);b=json.loads(a[a.index('--json')+1]);need(p['spreadsheetId']==self.plan['spreadsheet_id'] and p['range']=="'Math Puzzles'!A:D" and p['valueInputOption']=='RAW' and p['insertDataOption']=='INSERT_ROWS' and p['includeValuesInResponse'] is True,'wrong mocked append destination/mode');need(b=={'majorDimension':'ROWS','values':[self.row]},'wrong mocked payload');self.appends+=1;self.sheet.append(copy.deepcopy(self.row))
    if self.unknown:raise RuntimeError('MOCK unknown append outcome after server commit')
    return {'updates':{'updatedRows':2 if self.badresponse else 1,'updatedColumns':4,'updatedData':{'values':[self.row]}}}
  raise RuntimeError('UNMOCKED COMMAND '+repr(a))
 def run(self):
  self.sync();m=self.load();o=io.StringIO()
  with contextlib.redirect_stdout(o):
   try:m.main();error=None
   except Exception as e:error=type(e).__name__+': '+str(e)
  p=self.audit/'LEDGER_PUBLICATION_VERIFICATION.json';return {'error':error,'appends':self.appends,'intent':(self.audit/'LEDGER_RECONCILIATION_INTENT.json').exists(),'receipt':json.loads(p.read_text()) if p.exists() else None,'stdout':o.getvalue()}
def one(inp,scratch,label,change=None,edition='final',appends=0,error=None,success=False):
 with tempfile.TemporaryDirectory(prefix='mock1132_',dir=scratch) as t:
  f=Fixture(inp,Path(t),edition)
  if change:change(f)
  r=f.run();need(r['appends']==appends,label+' append count');need((r['error'] is None and r['receipt']) if success else (r['error'] is not None and (error is None or error in r['error'])),label+' outcome');return {'case':label,'edition':edition,'expected_confirmed':True,**r}
def race(inp,scratch,edition):
 with tempfile.TemporaryDirectory(prefix='mock1132_race_',dir=scratch) as t:
  f=Fixture(inp,Path(t),edition);f.sync();ms=[f.load('a'),f.load('b')];intent=f.audit/'LEDGER_RECONCILIATION_INTENT.json';exists0=Path.exists;gate=threading.Barrier(2);errors=[]
  def exists(p):
   if p==intent:gate.wait(timeout=8);return False
   return exists0(p)
  def run(m):
   try:m.main();errors.append(None)
   except Exception as e:errors.append(type(e).__name__+': '+str(e))
  with patch.object(Path,'exists',exists):
   ts=[threading.Thread(target=run,args=(m,)) for m in ms]
   for q in ts:q.start()
   for q in ts:q.join(timeout=15)
   need(all(not q.is_alive() for q in ts),'race deadlock')
  need(f.appends==(2 if edition=='old' else 1),'race count')
  if edition=='final':need(any(e and 'FileExistsError' in e for e in errors),'exclusive guard')
  return {'case':'concurrent_same_operation_stale_prechecks','edition':edition,'appends':f.appends,'errors':errors,'expected_confirmed':True}
def main():
 p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--scratch',type=Path,required=True);a=p.parse_args();a.scratch.mkdir(exist_ok=True,parents=True);rs=[]
 def add(n,c=None,**kw):rs.append(one(a.inputs,a.scratch,n,c,**kw))
 add('new_row',appends=1,success=True);add('existing_exact',lambda f:f.sheet.append(f.row),success=True)
 add('existing_incomplete',lambda f:f.sheet.append(['same','','https://doi.org/10.5281/zenodo.23063072','incomplete']),error='Concurrent/preexisting row')
 add('duplicate_exact',lambda f:f.sheet.extend([f.row,f.row]),error='Concurrent/preexisting row')
 add('semantic_existing',lambda f:f.sheet.append(['Strong geography question of Alfieri and Binns','','elsewhere','credited']),error='Concurrent/preexisting row')
 add('account_lead',lambda f:f.account.update(total=1,records=[{'id':999,'metadata':{'title':'Strong geography'}}]),error='own-account')
 add('unadopted',lambda f:f.adopt.update(ready_for_existing_publication_record=False),error='Independent review')
 add('plan_mutation',lambda f:f.pp.write_text(f.pp.read_text()+' '),error='Reviewed plan changed')
 add('helper_mutation',lambda f:f.helper.write_text(f.helper.read_text()+'\n# mutation\n'),error='Reviewed mutation helper changed')
 add('review_mutation',lambda f:(f.audit/'review_pin.txt').write_text('changed'),error='Adopted review changed')
 for field in ['head','base','body']:
  def changed(f,field=field):
   if field=='body':f.live['body']+=' changed';f.inv['pull_requests'][0]['body']=f.live['body']
   else:f.live[field]['sha']='b'*40;f.inv['pull_requests'][0][field+'RefOid']='b'*40
  add('both_live_inventory_'+field,changed,error='directly reviewed immutable plan')
  if field=='head':add('historical_unbound_head_gap',changed,edition='old',appends=1,success=True)
 add('provider_draft',lambda f:f.provider.update(state='draft'),error='Record not published')
 add('provider_metadata',lambda f:f.provider['metadata'].update(title='Different'),error='metadata changed')
 add('provider_files',lambda f:f.provider['files'].pop(),error='Published files changed')
 add('doi_destination',lambda f:f.resolution.update(final_url='https://zenodo.org/records/123'),error='DOI destination mismatch')
 add('schema',lambda f:f.sheet.__setitem__(0,['Different']),error='Sheet schema changed')
 add('prior_partial_intent',lambda f:(f.audit/'LEDGER_RECONCILIATION_INTENT.json').write_text('{partial'),error='Prior append intent')
 add('bad_append_response',lambda f:setattr(f,'badresponse',True),appends=1,error='Unexpected append response')
 add('external_append_race',lambda f:setattr(f,'afterdup',True),appends=1,error='Final row/uniqueness differs')
 with tempfile.TemporaryDirectory(prefix='mock1132_recovery_',dir=a.scratch) as t:
  f=Fixture(a.inputs,Path(t));f.unknown=True;r=f.run();need(r['appends']==1 and r['intent'] and not r['receipt'] and 'unknown append outcome' in r['error'],'unknown outcome');f.unknown=False;s=f.run();need(s['appends']==1 and s['error'] is None and s['receipt']['new_row'] is False,'recovery repeated append');rs.append({'case':'unknown_committed_append_recovery','first':r,'second':s,'expected_confirmed':True})
 sink=io.StringIO()
 with contextlib.redirect_stdout(sink):rs.extend([race(a.inputs,a.scratch,'old'),race(a.inputs,a.scratch,'final')])
 print(json.dumps({'status':'pass','cases':len(rs),'results':rs,'scope':'Copied helpers and fake clients only; no live mutations or historical math execution.'},sort_keys=True))
if __name__=='__main__':main()
