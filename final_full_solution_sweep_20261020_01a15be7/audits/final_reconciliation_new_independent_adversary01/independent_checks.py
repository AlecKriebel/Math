"""Independent read-only final coverage and strict numeric-ingress checker.
No services, writes, mathematical programs, action authority or final adoption.
"""
from pathlib import Path
import sys,stat,json,hashlib,gzip,lzma,collections,math,datetime,argparse
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
J=R/'audits/final_reconciliation_join_preparation01'
BOOK='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';GID=1254632077
GWS='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws'
GWS_SHA='0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e'
JPIN='612b8e085f388e133e94a4c87cc3514e69d0f2931cec5999809f80d7ffaf0b1d'
MF='620f22164fe099650f31196258b55ab21fc52b8da0c6a8c0912c875fe2816417'
SCHEMA=['Original Problem','Solution Chat URL','DOI','Notes']
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def need(v,msg):
 if not v:raise RuntimeError(msg)
def strict(b):
 def pairs(ps):
  o={}
  for k,v in ps:need(k not in o,'Duplicate JSON member');o[k]=v
  return o
 def bad(v):raise RuntimeError('Nonfinite JSON number '+v)
 return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
def typed(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(typed(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(typed(x,y)for x,y in zip(a,b))
 if type(a)is float and not math.isfinite(a):return False
 return a==b
def frozen_join():
 p=J/'join_readonly.py';b=p.read_bytes();need(H(b)==JPIN,'Join code external pin')
 n={'__file__':str(p),'__name__':'_independent_readonly_join'}
 exec(compile(b,str(p),'exec',optimize=0),n);n['verify_closed'](MF);return n
def readpin(p):
 path=Path(p['path']);path=path if path.is_absolute()else R/path
 for part in [path,*path.parents]:need(not part.is_symlink(),'Pinned path has symlink')
 need(stat.S_ISREG(path.lstat().st_mode),'Pinned input not regular');b=path.read_bytes()
 need(type(p['bytes'])is int and len(b)==p['bytes']and H(b)==p['sha256'],'Exact external input pin')
 return b
def objpin(p):
 b=readpin(p)
 if str(p['path']).endswith('.gz'):b=gzip.decompress(b)
 elif str(p['path']).endswith('.xz'):b=lzma.decompress(b)
 return strict(b)
def strict_sheet(s):
 need(type(s)is dict and set(s)>={'metadata','value_raw','formula_raw','values','formulas'},'Full snapshot shape')
 m=s['metadata'];need(type(m)is dict and m.get('spreadsheetId')==BOOK and type(m.get('sheets'))is list,'Complete workbook metadata')
 targets=[t['properties']for t in m['sheets']if type(t)is dict and type(t.get('properties'))is dict and type(t['properties'].get('sheetId'))is int and t['properties']['sheetId']==GID]
 need(len(targets)==1,'Unique exact typed numeric target')
 t=targets[0];g=t.get('gridProperties')
 need(t.get('title')=='Math Puzzles'and t.get('sheetType')=='GRID'and type(g)is dict,'Target title/type')
 need(type(g.get('columnCount'))is int and g['columnCount']==43 and type(g.get('rowCount'))is int and g['rowCount']>0,'Full allocated extent')
 filt=[{'gridRange':{'sheetId':GID,'startRowIndex':0,'endRowIndex':g['rowCount'],'startColumnIndex':0,'endColumnIndex':43}}]
 for key,rowskey in [('value_raw','values'),('formula_raw','formulas')]:
  raw=s[key];need(type(raw)is dict and raw.get('spreadsheetId')==BOOK,'Raw workbook identity')
  a=raw.get('valueRanges');need(type(a)is list and len(a)==1 and type(a[0])is dict,'One complete numeric match')
  v=a[0];need(typed(v.get('dataFilters'),filt),'Entire numeric allocated range/filter')
  vr=v.get('valueRange');need(type(vr)is dict and vr.get('majorDimension')=='ROWS'and vr.get('range')=="'Math Puzzles'!A1:AQ"+str(g['rowCount']),'Whole ROWS A1 endpoint')
  rows=vr.get('values');need(type(rows)is list and bool(rows)and typed(rows[0],SCHEMA),'Exact four-column header')
  need(len(rows)<=g['rowCount']and all(type(row)is list and len(row)<=43 and all(type(c)in(str,int,float,bool)and typed(c,c)for c in row)for row in rows),'Typed rows within full43 allocation')
  need(typed(rows,s[rowskey]),'Full raw/derived rows')
 need(typed(s['value_raw'],s['formula_raw'])and typed(s['values'],s['formulas']),'Entire VALUE/FORMULA identity')
 return {'rows':len(s['values']),'allocated_rows':g['rowCount'],'columns':43,'gid':GID,'title':t['title'],'full_filter':filt}
def raw_cli(e,role,d):
 import base64
 need(type(e)is dict and type(e.get('returncode'))is int and e['returncode']==0,'Native original returncode')
 need('stdout_base64'in e and 'stderr_base64'in e and type(e.get('argv'))is list,'All original native transports/full argv required')
 for k in ['stdout_base64','stderr_base64']:base64.b64decode(e[k],validate=True)
 argv=e['argv'];need(all(type(a)is str for a in argv),'Native argv string vector')
 if role in ['metadata_before','metadata_after']:
  need(len(argv)==6 and argv[:5]==[GWS,'sheets','spreadsheets','get','--params'],'Only full unprojected metadata request')
  need(typed(strict(argv[5]),{'spreadsheetId':BOOK,'includeGridData':False}),'Complete metadata request params')
 else:
  need(len(argv)==9 and argv[:6]==[GWS,'sheets','spreadsheets','values','batchGetByDataFilter','--params']and argv[7]=='--json','Only full numeric unprojected dual request')
  need(typed(strict(argv[6]),{'spreadsheetId':BOOK}),'Numeric request params')
  body={'dataFilters':d['full_filter'],'majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'if role=='values'else'FORMULA'}
  need(typed(strict(argv[8]),body),'Exact numeric request/mode/full allocated filter')
 return strict(base64.b64decode(e['stdout_base64'],validate=True))
def final_ingress(overlay_pin):
 env=objpin(overlay_pin);need(env.get('schema')=='root-adopted-final-join-overlay-v1','Final overlay schema')
 payload=env['payload'];ad=objpin(env['root_adoption'])
 need(ad.get('kind')=='ROOT_ADOPTED_FINAL_JOIN_OVERLAY'and ad.get('all_native_receipts_reviewed')is True and ad.get('payload_sha256')==H(C(payload)),'ROOT exact final payload adoption')
 l=payload['final_ledger'];s=objpin(l['snapshot']);d=strict_sheet(s);roles=l['original_transports']
 need(set(roles)=={'metadata_before','values','formulas','metadata_after'},'Exact four original roles')
 native={k:raw_cli(objpin(p),k,d)for k,p in roles.items()}
 need(typed(native['metadata_before'],native['metadata_after'])and typed(native['metadata_before'],s['metadata']),'Full metadata bracket identity')
 need(typed(native['values'],s['value_raw'])and typed(native['formulas'],s['formula_raw']),'Original full dual raw responses')
 need(H(Path(GWS).read_bytes())==GWS_SHA,'Native binary pin')
 at=datetime.datetime.fromisoformat(l['observed_at']);need(at.tzinfo is not None,'Aware actual observation timestamp required')
 return {'status':'PASS_STRICT_AUTHENTIC_FINAL_NUMERIC43_INGRESS','snapshot_pin':l['snapshot'],'original_transports':roles,'actual_observed_at':l['observed_at'],'full_details':d,'actual_service_effects':0,'final_reconciliation_complete':False,'note':'Explicit dated evidence; no guarantee of no subsequent service change.'}
def foundation():
 n=frozen_join();v=n['baseline']();stored=strict(lzma.decompress((J/'EFFECTIVE_JOIN.json.xz').read_bytes()));need(typed(v,stored),'Whole mapping reconstruction')
 ins=strict(lzma.decompress((J/'private/LOCAL_ORIGINAL_INPUTS.json.xz').read_bytes()))
 ap=next(p for p in ins['external_pins']if p['path'].endswith('/REFERENCE_BYTES_EXCEPT_REST.json.gz'));ar=objpin(ap);originals={}
 for r in v['rows']:
  p=r['original_disposition'];b=ar[p['preserved_original_archive_key']]['text'].encode()
  need(len(b)==p['bytes']and H(b)==p['sha256']and (R/p['path']).read_bytes()==b,'Every original complete byte preservation')
  o=strict(b);need(o['pr']==r['pr'],'Original per-slot identity');originals[r['pr']]=o
  status=[o['explicit_pr_queue_status']]if'explicit_pr_queue_status'in o else o.get('explicit_pr_queue_statuses',[])
  need(typed(status,r['explicit_historical_QUEUE_statuses']),'Historical full QUEUE status preservation')
  need(any('claimed_solved'in s for s in status)is r['historical_claimed_marker'],'Historical claimed-marker coverage')
  if r.get('classification_reference'):
   q=Path(r['classification_reference']);q=q if q.is_absolute()else R/q;need(q.is_file(),'Missing classification artifact')
 need(sorted(originals)==list(range(9,1447)),'Independent numeric coverage')
 missing=[r for r in v['rows']if not r['explicit_historical_QUEUE_statuses']]
 null=[r for r in missing if r['missing_status_examined']is None]
 need(len(missing)==404 and len(null)==138 and sum(r['effective_coverage_bucket']=='publication_recorded'for r in null)==137,'Published-first null cohort')
 admin=next(r for r in null if r['effective_coverage_bucket']!='publication_recorded');need(admin['pr']==415,'Unexpected unexamined missing-status case')
 cl=strict((R/'PR0415_MISSING_STATUS_CLASSIFICATION.json').read_bytes());need(cl['head']==admin['live_head']and cl['changed_paths']==['unsolved_math_prioritization/QUEUE.md']and cl['classification']=='administrative_header_restore_no_mathematical_claim'and len(cl['added_lines'])==3,'Administrative-only examination')
 sheet=objpin(next(p for p in ins['external_pins']if p['path'].endswith('/AFTER_COMPLETE_SHEET.json')));d=strict_sheet(sheet)
 doi=lambda s:str(s).lower().replace('https://doi.org/','').replace('http://doi.org/','').strip()
 groups=collections.defaultdict(list)
 for r in v['rows']:
  c=r.get('coverage')
  if not c:continue
  need(type(c['row'])is int and 1<=c['row']<=len(sheet['values']),'Actual row index')
  if c.get('doi'):
   hits=[i for i,x in enumerate(sheet['values'],1)if len(x)>2 and doi(x[2])==doi(c['doi'])]
   need(hits==[c['row']],'Actual DOI row unique');groups[doi(c['doi'])].append(r['pr'])
  else:need(H(C(sheet['values'][c['row']-1][:4]))==c['literal_four_cells_sha256'],'Source literal row identity')
 need({k:x for k,x in groups.items()if len(x)>1}=={'10.48550/arxiv.2609.25107':[1169,1176]},'Unexpected DOI multi-PR equivalence')
 fs=v['pending_family_obligations'];need(len(fs)==34 and sum(len(f['associated_prs'])for f in fs)==35,'Exact34/35 families')
 need(next(f for f in fs if f['family_pr']==1270)['associated_prs']==[1270,1277]and not any(f['family_pr']==1277 for f in fs),'Single joint family')
 need({f['family_pr']for f in fs if not f['selected_C_DOI']}=={1292,1310,1312},'Intentional unestablished DOI blanks')
 need(len({f['selected_C_DOI']for f in fs if f['selected_C_DOI']})==31,'No duplicated selected31 prior DOIs')
 need(len(v['own_publications'])==13 and len({x['doi']for x in v['own_publications']})==13,'Actual13 distinct publications')
 need(v['final_reconciliation_complete']is False and v['uncompleted_new_publication_PRs']==[1131]and v['pending_family_count']==34,'No premature completion')
 return {'status':'PASS_DATED_INDEPENDENT_COVERAGE_FOUNDATION_ONLY','original_slots_checked':1438,'historical_claimed':sum(r['historical_claimed_marker']for r in v['rows']),'missing_usable_status':len(missing),'missing_flags_true':sum(r['missing_status_examined']is True for r in missing),'null_published_first_cases':137,'null_administrative_case':415,'counts':dict(collections.Counter(r['effective_coverage_bucket']for r in v['rows'])),'dated_sheet':d,'multi_PR_DOI_equivalences':{k:x for k,x in groups.items()if len(x)>1},'actual_new_publications':13,'pending_existing_families':34,'pending_associated_PRs':35,'actual_effects':0,'final_clearance':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['foundation','final-ingress']);p.add_argument('--overlay');p.add_argument('--overlay-sha256');a=p.parse_args()
 if a.mode=='foundation':r=foundation()
 else:
  need(a.overlay and a.overlay_sha256,'Actual final overlay external pin required');p=Path(a.overlay);r=final_ingress({'path':str(p),'bytes':p.stat().st_size,'sha256':a.overlay_sha256})
 print(json.dumps(r,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False))
if __name__=='__main__':main()
