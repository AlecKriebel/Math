"""Additional independent query/bibliography boundaries, full helper main."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ns={'__file__':str(HERE/'offline_whole_helper.py'),'__name__':'offline_review07_library'}
exec(compile((HERE/'offline_whole_helper.py').read_bytes(),ns['__file__'],'exec'),ns)
controls=[]
def add(name,url,expect='reject',actual=False):
 def edit(records):
  item=records[1];item.setdefault('links',{})['probe']=url
 controls.append({'name':name,'cfg':{'actual_account':actual,'edit_account':edit},'expect':expect,'appends':1 if expect=='pass' else 0})
enc=lambda s:''.join('%'+format(c,'02x') for c in s.encode())
for value in ['','?','?page=1','?preview=1','?sort=newest','?q=unrelated','?q=ordinary%20unrelated','?download=1','?format=json','?a=1&b=2']:
 add('safe_query_'+value,'https://zenodo.org/api/records/90000001'+value,'pass')
for lead in ['//shortdoi.org/abc','doi.org/abc','10/abc',enc('10.5281/zenodo.23350364'),enc('//shortdoi.org/abc'),enc('https://zenodo.org/records/23350363')]:
 for route in ['/api/records/90000001','/uploads/90000001','/api/iiif/record:90000001/manifest','/doi/10.5281/zenodo.90000001']:
  add('unsafe_query_'+route+'_'+lead,'https://zenodo.org'+route+'?related='+lead)
# Control difference: an identical separate resolver lead survives off projection.
for value in ['https://zenodo.org/api/records/90000001#//shortdoi.org/abc','https://zenodo.org/api/records/90000001/unknown?related=//shortdoi.org/abc']:
 add('unprojected_unsafe_'+value,value)
for prefix in ['', 'x', '1', '/', 'https://foreign.invalid/file-', 'doi:']:
 text='OWR 10/2025; '+prefix+'10.4171/OWR/2025/10'
 expected='pass' if prefix in ['', '/', 'https://foreign.invalid/file-', 'doi:'] else 'reject'
 controls.append({'name':'report_source_token_prefix_'+prefix,'cfg':{'edit_account':lambda r,v=text:r[1]['metadata'].__setitem__('description',v)},'expect':expected,'appends':1 if expected=='pass' else 0})
for suffix in ['.5','/extra','-extra','%2Fextra','_extra','EXTRA']:
 text='OWR 10/2025; 10.4171/OWR/2025/10'+suffix
 controls.append({'name':'report_source_token_suffix_'+suffix,'cfg':{'edit_account':lambda r,v=text:r[1]['metadata'].__setitem__('description',v)},'expect':'reject','appends':0})
for prefix in ['.','_']:
 text='OWR 10/2025; '+prefix+'10.4171/OWR/2025/10'
 controls.append({'name':'report_source_token_prefix_'+prefix,'cfg':{'edit_account':lambda r,v=text:r[1]['metadata'].__setitem__('description',v)},'expect':'reject','appends':0})
results=[ns['case_run'](c) for c in controls]
v={'mode':sys.flags.optimize,'case_count':len(results),'passed':sum(r['passed'] for r in results),'all_cases_passed':all(r['passed'] for r in results),'denied_actual_services':ns['DENIED'],'results':results}
(HERE/('QUERY_BOUNDARY_MODE_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({'mode':v['mode'],'cases':v['case_count'],'passed':v['passed'],'failures':[(r['case'],r['error']) for r in results if not r['passed']]},indent=2))
