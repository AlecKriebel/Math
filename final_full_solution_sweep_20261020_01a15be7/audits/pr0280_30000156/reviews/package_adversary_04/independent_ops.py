#!/usr/bin/env python3
"""Fresh independent actual-function boundary controls; all providers synthetic."""
from pathlib import Path
import importlib.util,sys,json,tempfile,copy,subprocess,datetime
from unittest.mock import patch
R=Path(__file__).resolve().parent;A=R.parents[1];P=A.parents[1]/'private/pr0280_package_adversary_04'
sys.path.insert(0,str(P/'ops_replay'));sys.argv.append('--canonical')
spec=importlib.util.spec_from_file_location('review04_fixture',P/'ops_replay/integrated_controls.py');T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T)
results=[]
def require(value,name):
 if not value:raise RuntimeError(name)
 results.append({'case':name,'pass':True})
with patch.object(subprocess,'run',T.forbidden):
 modules=T.implementation(True);B,C,G,V,D=modules
 # Additional pipeline forms and all four columns; no equivalent spelling is
 # made equal to the exact desired row by normalization.
 variants=['urn:doi:10.5281/ZeNoDo.999','doi:10.5281/zenodo.%39%39%39','https://DX.DOI.ORG/10.5281/ZENODO.999','(https://doi.org/10.5281/ze%6eodo.999).','10.5281/zenodo.999?urlappend=/appendix','10.5281/zenodo.999\tcomment','10.5281%252fzenodo.999#x','https://zenodo.org/records/000999/files/a.pdf']
 with tempfile.TemporaryDirectory(dir=P,prefix='review04_pipeline_') as t:
  for k,value in enumerate(variants):
   for column in range(4):
    row=['generic','','',''];row[column]=value
    outcome=T.run_pipeline(Path(t)/('case'+str(k)+'_'+str(column)),modules,[row],True)
    require(outcome['collector_matching_rows']==1 and not outcome['gate_accepted'] and outcome['append_calls']==0,'new alias pipeline '+str(k)+' column'+str(column))
  # A newly introduced alias after an absence read must reject readback.
  alias=['generic','','urn:doi:10.5281/ZENODO.999','']
  after=[B.HEADERS,D.desired_row(999),alias]
  outcome=T.run_pipeline(Path(t)/'postread',modules,[],True,after_override=after)
  require(outcome['append_calls']==1 and not outcome['append_returned_verified'],'postread concurrent alias rejects receipt')
 # Direct independent pagination fixtures.
 def rec(i):return {'id':i,'metadata':{'title':'draft' if i==2 else 'published'},'files':[],'is_published':i!=2}
 class Client:
  base='https://synthetic.invalid'
  def __init__(self,pages):self.pages=iter(pages)
  def request(self,m,u):
   if m!='GET':raise RuntimeError('Non-GET attempted')
   return next(self.pages)
 def page(total,ids,next=None):return {'hits':{'total':total,'hits':[rec(i) for i in ids]},'links':{'next':next} if next else {}}
 good=[page(2,[1],'https://synthetic.invalid/next'),page(2,[2])]
 require(len(C.account_search(Client(good),'')['records'])==2,'complete two page published plus draft')
 bads={
 'total changes':[page(2,[1],'https://synthetic.invalid/next'),page(3,[2])],
 'last page absent':[page(3,[1])],
 'inexact total':[page({'value':1,'relation':'gte'},[1])],
 'repeated record':[page(2,[1],'https://synthetic.invalid/next'),page(2,[1])],
 'cross host':[page(2,[1],'https://other.invalid/next')],
 'http downgrade':[page(2,[1],'http://synthetic.invalid/next')],
 'loop':[page(3,[1],'https://synthetic.invalid/next'),page(3,[2],'https://synthetic.invalid/next')],
 'noninteger total':[page(True,[1])],
 }
 for name,pages in bads.items():
  try:C.account_search(Client(pages),'')
  except (RuntimeError,KeyError,TypeError):require(True,'pagination rejects '+name)
  else:raise RuntimeError('Pagination accepted '+name)
 for item in [{'metadata':{},'files':{}},{'metadata':[],'files':[]}]:
  try:B.identity_projection(item)
  except RuntimeError:require(True,'metadata/full-file type rejects '+repr(item))
  else:raise RuntimeError('Malformed projection accepted')
 for value in [{'values':[B.HEADERS,['','','','','outside']]},{'values':[B.HEADERS,['',1]]},{'values':[['wrong']]}]:
  try:B.schema_rows(value)
  except RuntimeError:require(True,'sheet schema rejects '+repr(value))
  else:raise RuntimeError('Malformed sheet accepted')
 for when in [(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=181)).isoformat(),(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=60)).isoformat(),'2026-10-21T00:00:00']:
  try:B.fresh(when)
  except RuntimeError:require(True,'freshness rejects '+when)
  else:raise RuntimeError('Stale/naive gate accepted')
 try:B.require_release_clearance()
 except FileNotFoundError:require(True,'absent affirmative root clearance fails closed')
 else:raise RuntimeError('Clearance unexpectedly present')
print(json.dumps({'utc':B.stamp(),'optimization':sys.flags.optimize,'controls':len(results),'actual_provider_attempts':len(T.ACTUAL_PROVIDER_ATTEMPTS),'results':results},indent=2))
