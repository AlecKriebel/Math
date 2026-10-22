#!/usr/bin/env python3
"""Minimal full-main reproducer using only this review's new private copies."""
import argparse,hashlib,json,runpy,sys
from html.parser import HTMLParser
from pathlib import Path
HERE=Path(__file__).resolve().parent
m=runpy.run_path(str(HERE/'offline_exact_instance.py'))
row=m['BASE_PLAN']['proposed_row'];copy=m['copy'];run=m['case_run']
alias='<a href="https://doi.org/10.5281/zenodo.&#50;3350364">same result</a>'
class Links(HTMLParser):
    def __init__(self):super().__init__();self.hrefs=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.hrefs += [v for k,v in attrs if k=='href']
p=Links();p.feed(alias)
if p.hrefs!=['https://doi.org/10.5281/zenodo.23350364']:raise RuntimeError('Independent HTML decoding failed')
results=[];original_loads=json.loads
for name,trailing in [('exact182_unchanged',None),('unreviewed_row', ['unreviewed ordinary row','','','']),('HTML_target_alias',['','','',alias]),('known_literal_target',['','','','https://doi.org/10.5281/zenodo.23350364'])]:
    capture=[]
    def tracked_loads(data,*a,**kw):
        value=original_loads(data,*a,**kw)
        if isinstance(value,dict) and value.get('read_back_exact') is True and value.get('status')=='verified':capture.append(value)
        return value
    cfg={'edit_rows':lambda r:r.append(copy.deepcopy(row))}
    if trailing is not None:cfg['edit_immediate_rows']=lambda r,v=trailing:r.append(copy.deepcopy(v))
    json.loads=tracked_loads
    try:result=run({'name':name,'expect':'pass' if trailing is None else 'reject','cfg':cfg})
    finally:json.loads=original_loads
    result.update({'before_rows':182,'final_trailing_row':trailing,'verification_receipt':capture[-1] if capture else None})
    results.append(result)
output={'schema':1,'mode':sys.flags.optimize,'helper_sha256':m['EXPECTED_HELPER'],'plan_sha256':m['EXPECTED_PLAN'],'network_and_process_attempts':m['DENIED'],'private_fixtures_only':True,'alias_markup':alias,'independent_HTMLParser_href':p.hrefs,'results':results,'finding':'Idempotent path accepts unreviewed after-read rows and issues verified receipt; known literal alias still rejects. No append in any reproducer.'}
(HERE/('CRITICAL_MODE_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'mode':sys.flags.optimize,'accepted_unreviewed':[(r['case'],r['simulated_ledger_rows']) for r in results if r['error'] is None and r['final_trailing_row'] is not None],'all_appends_zero':all(r['state']['append']==0 for r in results),'offline_denials':m['DENIED']},indent=2))
