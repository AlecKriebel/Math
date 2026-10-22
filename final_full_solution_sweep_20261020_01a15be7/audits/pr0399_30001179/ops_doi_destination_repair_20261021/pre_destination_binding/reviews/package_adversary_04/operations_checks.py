#!/usr/bin/env python3
"""Independent actual-function probes. Real network and subprocesses are trapped."""
from pathlib import Path
from contextlib import ExitStack
from unittest.mock import patch
import argparse,copy,hashlib,json,socket,subprocess,sys,types
R=Path(__file__).resolve().parent;A=R.parents[1];P=A.parents[1]/'private/pr0399_package04'
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);args=parser.parse_args()
OUTPUT=R
if args.output is not None:
 if not args.output.is_absolute() or not args.output.is_relative_to(A.parents[1]/'private'):raise RuntimeError('New private output required')
 args.output.mkdir(parents=True,exist_ok=False);OUTPUT=args.output
NAMES=['ops_binding','prepublication_check','publication_live_gates','repository_integration','verify_published_files','publication_lifecycle','record_publication_ledger']
mods=[]
for name in NAMES:
 m=types.ModuleType(name);m.__file__=str(A/(name+'.py'));sys.modules[name]=m
 exec(compile((A/(name+'.py')).read_bytes(),str(A/(name+'.py')),'exec'),m.__dict__);mods.append(m)
B,C,G,I,V,Y,L=mods
results=[];attempts=[]
def require(v,m):
 if not v:raise RuntimeError(m)
def forbid(*a,**kw):attempts.append('forbidden');raise RuntimeError('REAL PROVIDER ACCESS TRAPPED')
def outcome(label,fn,expected):
 try:r=fn();actual='accept'
 except (RuntimeError,ValueError,KeyError,FileNotFoundError,B.zenodo.DepositError):actual='reject'
 require(actual==expected,label+': '+actual);results.append({'label':label,'outcome':actual})
with ExitStack() as st:
 st.enter_context(patch.object(socket,'socket',forbid));st.enter_context(patch.object(subprocess,'run',forbid))
 # Explicit empty/family target recognition and bibliography does not mask another alias.
 id=29999991;target='10.5281/zenodo.'+str(id)
 refs=['https://zenodo.org/record/'+str(id)+'/', 'https://www.zenodo.org:0443/records/./'+str(id)+'/export/json?x=1#r', '//zenodo.org/records/'+str(id)+'/files/x.pdf', 'https://doi.org/10.5281/ZENODO.'+str(id), '10.5281%2fzenodo%2e'+str(id)]
 for j,s in enumerate(refs):
  for col in range(4):
   row=['','','',''];row[col]=s
   outcome('new alias '+str(j)+' cell '+str(col),lambda row=row:require(B.target_in_row(row,id),'target missed'),'accept')
 for s in ['https://zenodo.org/research/'+str(id),'https://zenodo.org/records/'+str(id)+'/unknown','https://user@zenodo.org/records/'+str(id),'https://zenodo.org./records/'+str(id),'https://doi.org/abcd','10/abc','OWR 10/2016 pp.479–481 DOI 10.4171/OWR/2017/10']:
  outcome('ambiguity '+s,lambda s=s:B.row_identity_names([s]),'reject')
 bib='OWR 10/2016 pp.479–481 DOI 10.4171/OWR/2016/10'
 outcome('exact bibliography role',lambda:B.row_identity_names([bib]),'accept')
 outcome('bibliography cannot mask second shortDOI',lambda:B.row_identity_names([bib+' 10/abc']),'reject')
 outcome('model first cannot hide later ambiguity',lambda:L.matches([B.HEADERS,['tensor core','','','https://zenodo.org/unknown']],id),'reject')
 for s in ['https://zenodo.org.evil.example/records/'+str(id),'https://example.org/path/zenodo.org/records/'+str(id),'10.5281/zenodo.0'+str(id),'10.5281/zenodo.'+str(id)+'1']:
  outcome('nearby distinct '+s,lambda s=s:require(not B.target_in_row([s],id),'overmatch'),'accept')
 # Exact account inventory including draft-shaped entries, pagination, metadata and full files.
 class Client:
  base='https://zenodo.org'
  def __init__(self,pages):self.pages=copy.deepcopy(pages)
  def request(self,method,url):require(method=='GET','mutating method');return self.pages.pop(0)
 def rec(i):return {'id':i,'metadata':{'title':'draft'},'files':[{'key':'x','checksum':'md5:abcd'}],'is_published':False}
 page=lambda items,total,next=None:{'hits':{'total':total,'hits':items},'links':({'next':next} if next else {})}
 good=[page([rec(1)],{'value':2,'relation':'eq'},'https://zenodo.org/api/user/records?page=2'),page([rec(2)],2)]
 outcome('account two pages include drafts',lambda:require(C.account_search(Client(good),'')['total']==2,'draft lost'),'accept')
 cases=[('inexact',[page([rec(1)],{'value':1,'relation':'gte'})]),('duplicate',[page([rec(1),rec(1)],2)]),('missing',[page([rec(1)],2)]),('changed total',[page([rec(1)],2,'https://zenodo.org/api/user/records?page=2'),page([rec(2)],3)]),('foreign next',[page([rec(1)],2,'https://example.org/next')])]
 for label,pages in cases:outcome('account '+label,lambda pages=pages:C.account_search(Client(pages),''),'reject')
 # Exact public metadata / files: actual bytes and actual verifier.
 meta,selected=B.manifest();downloads={e['name']:((B.PUBLICATION/e['name']).read_bytes(),200,'https://zenodo.org/records/'+str(id)+'/files/'+e['name']) for e in selected}
 pm=copy.deepcopy(meta);pm.pop('upload_type');pm.pop('publication_type');pm['resource_type']={'type':'publication','subtype':'preprint','title':'Preprint'};pm['license']={'id':meta['license']}
 public={'id':id,'doi':target,'metadata':pm,'files':[{'key':e['name'],'size':e['size'],'checksum':'md5:'+e['md5']} for e in selected]}
 inspection={'id':id,'state':'published','doi':target,'doi_url':'https://doi.org/'+target,'doi_resolution':{'http_status':200,'resolved_url':'https://zenodo.org/records/'+str(id)}}
 for field in meta:
  changed=copy.deepcopy(public);changed['metadata'][field]='tamper'
  outcome('public metadata '+field,lambda changed=changed:V.verify_public_record(id,meta,selected,inspection,changed,downloads,200),'reject')
 bad=copy.deepcopy(downloads);n=selected[0]['name'];d,c,u=bad[n];bad[n]=(bytes([d[0]^1])+d[1:],c,u)
 outcome('public PDF same-size corruption',lambda:V.verify_public_record(id,meta,selected,inspection,public,bad,200),'reject')
 outcome('public baseline',lambda:V.verify_public_record(id,meta,selected,inspection,public,downloads,200),'accept')
 doi_findings=[]
 class Response:
  status=200;url='https://zenodo.org/records/29999990'
  def __enter__(self):return self
  def __exit__(self,*args):return False
 class Opener:
  def open(self,*args,**kwargs):return Response()
 with patch.object(B.zenodo,'build_opener',lambda *a:Opener()):
  actual_doi_status=B.zenodo.doi_status(target)
 require(actual_doi_status['http_status']==200 and actual_doi_status['resolved_url']==Response.url,'actual DOI status fixture')
 doi_findings.append({'pipeline':'actual zenodo.doi_status with synthetic HTTP response','actual_output':actual_doi_status})
 for destination in ['https://zenodo.org/records/29999990','https://example.org/unrelated']:
  wrong=copy.deepcopy(inspection);wrong['doi_resolution']['resolved_url']=destination
  receipt=V.verify_public_record(id,meta,selected,wrong,public,downloads,200)
  doi_findings.append({'resolved_url':destination,'actual_verifier_accepted':True,'receipt_doi_status':receipt['doi_resolution']['status']})
 # Actual verify_live -> actual appender with synthetic, explicitly bypassed clearance/collector prerequisites.
 work=P/('append_wrong_doi_'+('optimized' if sys.flags.optimize else 'normal'));index=0
 while work.exists():
  index+=1;work=P/('append_wrong_doi_'+('optimized' if sys.flags.optimize else 'normal')+'_'+str(index))
 work.mkdir(exist_ok=False)
 (work/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').write_text(json.dumps({'ledger_leads':[]}))
 V.AUDIT=L.AUDIT=work;V.PRIVATE=L.PRIVATE=work;V.require_release_clearance=L.require_release_clearance=lambda:None
 wrong=copy.deepcopy(inspection);wrong['doi_resolution']=actual_doi_status
 V.zenodo.run=lambda *a,**k:copy.deepcopy(wrong)
 def fetch(url):
  if url=='https://zenodo.org/api/records/'+str(id):return json.dumps(public).encode(),200,url
  for e in selected:
   if '/files/'+e['name'] in url:return downloads[e['name']]
  raise RuntimeError('unexpected fixture URL')
 V.fetch=fetch
 rows=[B.HEADERS.copy()];appends=[]
 def gws(action,params,body=None):
  if action=='get':return {'values':copy.deepcopy(rows)}
  require(action=='append','unexpected mutation');require((work/'LEDGER_APPEND_INTENT.json').exists(),'intent absent')
  row=body['values'][0];rows.append(row);appends.append(row)
  return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[row]}}}
 L.gws=gws
 L.collect=lambda *a,**k:({'expected_identity_record_ids':[id],'ledger_sha256':B.digest(rows),'started_utc':B.stamp(),'receipt':str(work/'synthetic-gate.json')},{})
 receipt=L.append_verified('0'*40,id)
 require(receipt['new_row'] and receipt['unique_target_and_DOI'] and len(appends)==1,'full appender fixture')
 doi_findings.append({'pipeline':'actual verify_live -> actual append_verified','wrong_destination':'https://zenodo.org/records/29999990','synthetic_appends':len(appends),'readback_exact':receipt['read_back_exact'],'gate_clearance_prerequisites':'explicitly simulated; no real permission or provider state claimed'})
 require(not attempts,'actual provider attempt')
output={'optimization':sys.flags.optimize,'helper_bindings':[{'path':n+'.py','sha256':hashlib.sha256((A/(n+'.py')).read_bytes()).hexdigest()} for n in NAMES],'passing_controls':results,'new_material_finding':{'id':'P399-04-OPS-01','mechanism':'DOI200 final destination not checked against target record','reproductions':doi_findings},'actual_provider_attempts':len(attempts)}
(OUTPUT/('OPERATIONS.normal.json' if not sys.flags.optimize else 'OPERATIONS.optimized.json')).write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'controls':len(results),'wrong_destination_acceptances':len(doi_findings),'actual_provider_attempts':len(attempts)},indent=2))
