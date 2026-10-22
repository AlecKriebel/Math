"""Read-only full GWS CLI / local-state observation. No owned client import.
Only exact get and values.batchGetByDataFilter processes are allowed.
"""
import datetime, gzip, hashlib, json, pathlib, shutil, subprocess, sys
O=pathlib.Path(__file__).resolve().parent
B='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
G=1254632077
ROOT=O.parents[2]
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def strict(b):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d: raise ValueError('duplicate key')
   d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def equal(a,b):
 if type(a) is not type(b): return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(equal(x,y)for x,y in zip(a,b))
 return a==b
def get(parts,p,body=None):
 assert parts in [['get'],['values','batchGetByDataFilter']]
 c=['gws','sheets','spreadsheets',*parts,'--params',json.dumps(p)]
 if body is not None:c+=['--json',json.dumps(body)]
 r=subprocess.run(c,capture_output=True,timeout=90)
 if r.returncode:raise ValueError('GWS read failed '+r.stderr.decode()[:1000])
 return strict(r.stdout)
def main(label):
 assert label in ['initial','closing']
 assert shutil.disk_usage(O).free>=150*1024*1024
 at=stamp();m=get(['get'],{'spreadsheetId':B,'includeGridData':False})
 assert m['spreadsheetId']==B
 sh=[x['properties']for x in m['sheets']if x['properties']['sheetId']==G];assert len(sh)==1
 s=sh[0];assert s['title']=='Math Puzzles' and s['sheetType']=='GRID'
 grid=s['gridProperties'];assert type(grid['columnCount'])is int and grid['columnCount']==43
 n=grid['rowCount'];assert type(n)is int and n>0
 filters=[{'gridRange':{'sheetId':G,'startRowIndex':0,'endRowIndex':n,'startColumnIndex':0,'endColumnIndex':43}}]
 views=[]
 for mode in ['UNFORMATTED_VALUE','FORMULA']:
  x=get(['values','batchGetByDataFilter'],{'spreadsheetId':B},{'dataFilters':filters,'majorDimension':'ROWS','valueRenderOption':mode})
  assert x['spreadsheetId']==B and len(x['valueRanges'])==1
  v=x['valueRanges'][0];assert equal(v['dataFilters'],filters)
  y=v['valueRange'];assert y['range']=="'Math Puzzles'!A1:AQ"+str(n)and y['majorDimension']=='ROWS'
  rows=y['values'];assert rows[0]==['Original Problem','Solution Chat URL','DOI','Notes']
  assert len(rows)<=n and all(type(r)is list and len(r)<=43 and all(type(c)in[str,int,float,bool]for c in r)for r in rows)
  views.append(x)
 end=get(['get'],{'spreadsheetId':B,'includeGridData':False})
 assert equal(m,end)and equal(*views)
 local=[]
 for p in sorted((ROOT/'.zenodo-state').glob('*.json')):
  assert p.is_file()and not p.is_symlink()
  b=p.read_bytes();local.append({'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'value':strict(b)})
 out={'started_at':at,'ended_at':stamp(),'metadata_first':m,'value_raw':views[0],'formula_raw':views[1],'metadata_last':end,'local':local}
 dest=O/(label+'_observation.json.gz');assert not dest.exists()
 dest.write_bytes(gzip.compress(json.dumps(out,ensure_ascii=False).encode(),mtime=0))
 summary={'started_at':at,'ended_at':out['ended_at'],'rows':len(rows),'allocated_rows':n,'columns':43,'full_raw_typed_equal':True,'metadata_stable':True,'local_count':len(local),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'observation':dest.name,'service_writes':0}
 (O/(label+'_receipt.json')).write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
if __name__=='__main__':main(sys.argv[1])
