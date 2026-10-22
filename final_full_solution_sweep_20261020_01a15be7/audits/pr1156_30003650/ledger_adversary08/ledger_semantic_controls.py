#!/usr/bin/env python3
"""Fresh full-main controls for raw-versus-decoded ledger semantic leads."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ns={'__file__':str(HERE/'offline_whole_helper.py'),'__name__':'offline_review08_library'}
exec(compile((HERE/'offline_whole_helper.py').read_bytes(),ns['__file__'],'exec'),ns)
def controls():
 out=[];enc=lambda s:''.join('%'+format(c,'02x') for c in s.encode())
 leads=['30003650','OWR-15957-003','https://github.com/AlecKriebel/Math/pull/1156','https://github.com/AlecKriebel/Math/pull/%31%31%35%36','https://eulersolve.org/papers/%6f%77%72%2d%31%35%39%35%37%2d%30%30%33/']
 for col in range(4):
  for i,lead in enumerate(leads):
   value=enc(lead) if i<3 else lead
   out.append({'name':'v8_ledger_encoded_semantic_col'+str(col)+'_lead'+str(i),'cfg':{'edit_rows':lambda r,c=col,v=value:r.append(['' if j!=c else v for j in range(4)])},'expect':'reject','appends':0})
  for i,lead in enumerate(leads[:3]):
   out.append({'name':'v8_ledger_raw_semantic_col'+str(col)+'_lead'+str(i),'cfg':{'edit_rows':lambda r,c=col,v=lead:r.append(['' if j!=c else v for j in range(4)])},'expect':'reject','appends':0})
  out.append({'name':'v8_ledger_safe_encoded_unrelated_col'+str(col),'cfg':{'edit_rows':lambda r,c=col,v=enc('ordinary unrelated reference'):r.append(['' if j!=c else v for j in range(4)])},'expect':'pass','appends':1})
  out.append({'name':'v8_ledger_encoded_known_DOI_col'+str(col),'cfg':{'edit_rows':lambda r,c=col,v=enc('10.5281/zenodo.23350364'):r.append(['' if j!=c else v for j in range(4)])},'expect':'reject','appends':0})
 return out
if __name__=='__main__':
 results=[]
 for c in controls():
  r=ns['case_run'](c);results.append(r)
  if r['error'] and '[Errno 28]' in r['error']:raise RuntimeError('Infrastructure failure excluded')
 v={'mode':sys.flags.optimize,'case_count':len(results),'passed':sum(r['passed'] for r in results),'denied_actual_services':ns['DENIED'],'results':results}
 (HERE/('LEDGER_SEMANTIC_MODE_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(v,indent=2)+'\n')
 print(json.dumps({'mode':v['mode'],'cases':len(results),'passed':v['passed'],'unsafe_verified_appends':sum(not r['passed'] and r['error'] is None and r['state']['append']==1 and r['receipt_saved'] for r in results)},indent=2))
