"""Independent JSON-boundary versus individual-string unresolved short-name tests."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ns={'__file__':str(HERE/'offline_whole_helper.py'),'__name__':'offline_review07_library'}
exec(compile((HERE/'offline_whole_helper.py').read_bytes(),ns['__file__'],'exec'),ns)
cases=[]
for value in ['10/abc','10/abc ','10/abc.','10/abc;','10/2025','10/2025 ','OWR 10/2025; 10.4171/OWR/2025/10; separately 10/abc','OWR 10/2025; 10.4171/OWR/2025/10; separately 10/abc.','OWR 10/2025; 10.4171/OWR/2025/10; separately %31%30%2F%61%62%63']:
 for field in ['metadata','links']:
  def edit(records,v=value,f=field):records[1].setdefault(f,{})['serialization_probe']=v
  cases.append({'name':'serialization_'+field+'_'+value,'cfg':{'edit_account':edit},'expect':'reject','appends':0})
# Recheck three corrected positive expectations without changing original observed
# results silently. Established binding intentionally recognizes draft descendants.
cases += [c for c in ns['fresh_cases']() if 'unknown_route_visible_' in c['name'] and c['name'].endswith('/draft/unknown')]
results=[ns['case_run'](c) for c in cases]
v={'mode':sys.flags.optimize,'case_count':len(results),'passed':sum(r['passed'] for r in results),'denied_actual_services':ns['DENIED'],'results':results}
(HERE/('SERIALIZATION_MODE_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({'mode':v['mode'],'cases':v['case_count'],'passed':v['passed'],'failures':[(r['case'],r['error']) for r in results if not r['passed']]},indent=2))
