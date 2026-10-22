#!/usr/bin/env python3
"""Compare preserved actual outputs without rewriting any of them."""
from pathlib import Path
import datetime,json,hashlib
R=Path(__file__).resolve().parent
def differences(a,b,path=''):
 if type(a)!=type(b):return [{'path':path,'a':a,'b':b}]
 if isinstance(a,dict):
  if set(a)!=set(b):return [{'path':path,'a':sorted(a),'b':sorted(b)}]
  return sum([differences(a[k],b[k],path+'/'+k) for k in a],[])
 if isinstance(a,list):
  if len(a)!=len(b):return [{'path':path,'a':len(a),'b':len(b)}]
  return sum([differences(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))],[])
 return [] if a==b else [{'path':path,'a':a,'b':b}]
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
out={}
for kind in ['portable','workflow','finite']:
 records=[json.loads((R/f'{kind}_mode{i}.json').read_text()) for i in range(3)]
 deltas=[]
 for i in [1,2]:
  ds=differences(records[0],records[i]);allowed=[]
  for d in ds:
   if d['path']=='/optimization':need(d['a']==0 and d['b']==i,'invalid optimization marker');reason='Explicit host optimization marker.'
   elif kind=='portable' and d['path'] in ['/negative_controls/0/reason','/negative_controls/1/reason']:
    need(isinstance(d['a'],str) and d['b']==d['a'].replace('/_local/portable_0/','/_local/portable_'+str(i)+'/'),'difference exceeds exact own scratch path');reason='Exact mode-specific scratch extraction path in binding-error text.'
   else:raise RuntimeError('Unexplained mode difference '+str(d))
   allowed.append({**d,'adjudication':reason})
  deltas.append({'compared_optimization':i,'all_exact_differences':allowed})
 out[kind]={'raw_outputs_sha256':[hashlib.sha256((R/f'{kind}_mode{i}.json').read_bytes()).hexdigest() for i in range(3)],'differences':deltas,'actual_substantive_results_identical':True,'raw_outputs_byte_identical':False,'raw_outputs_preserved':True}
need(records[0]['actual_programs'][0]['returncode']!=0,'false guard should reject')
report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'groups':out,'comparison_scope':'Only the explicit top-level optimization marker and two exact temporary extraction path strings differ. All mathematical replay results, metadata and current workflow results, each merged-blob rejection and final guard-copy hashes agree. No source or evidence output was rewritten to fabricate equality.'}
(R/'MODE_COMPARISON.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','groups':{k:[len(x['all_exact_differences']) for x in v['differences']] for k,v in out.items()}}))
