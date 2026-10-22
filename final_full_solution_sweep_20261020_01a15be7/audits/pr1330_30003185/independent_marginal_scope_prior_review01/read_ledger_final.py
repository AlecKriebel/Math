from pathlib import Path
import subprocess,json,datetime,unicodedata,re,urllib.parse,hashlib,gzip
P=Path(__file__).resolve().parent
B='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';G=1254632077
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
D=P/'private_readonly'/('ledger_'+stamp);D.mkdir(exist_ok=False)
def strict(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(strict(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
 return a==b
def get(name,parts,params,body=None):
 c=['gws','sheets','spreadsheets',*parts,'--params',json.dumps(params)]
 if body is not None:c+=['--json',json.dumps(body)]
 r=subprocess.run(c,capture_output=True);(D/(name+'.stdout.gz')).write_bytes(gzip.compress(r.stdout,mtime=0));(D/(name+'.stderr.gz')).write_bytes(gzip.compress(r.stderr,mtime=0))
 if r.returncode:raise RuntimeError('read-only CLI failed '+name)
 return json.loads(r.stdout)
m=get('metadata_before',['get'],{'spreadsheetId':B,'fields':'spreadsheetId,sheets(properties)'})
if m['spreadsheetId']!=B:raise RuntimeError('wrong book')
s=[x['properties'] for x in m['sheets'] if x['properties']['sheetId']==G]
if len(s)!=1 or s[0]['title']!='Math Puzzles' or s[0]['gridProperties']['columnCount']!=43:raise RuntimeError('sheet identity')
views={}
for mode in ['UNFORMATTED_VALUE','FORMULA']:
 j=get(mode,['values','batchGetByDataFilter'],{'spreadsheetId':B},{'dataFilters':[{'gridRange':{'sheetId':G}}],'majorDimension':'ROWS','valueRenderOption':mode})
 if j['spreadsheetId']!=B or len(j['valueRanges'])!=1:raise RuntimeError('read book/matches')
 match=j['valueRanges'][0]
 if not strict(match['dataFilters'],[{'gridRange':{'sheetId':G}}]):raise RuntimeError('filter')
 v=match['valueRange']
 if v['range']!="'Math Puzzles'!A1:AQ"+str(s[0]['gridProperties']['rowCount']) or v['majorDimension']!='ROWS':raise RuntimeError('extent')
 rows=v['values']
 if rows[0]!=['Original Problem','Solution Chat URL','DOI','Notes'] or any(type(x)is not list or len(x)>43 for x in rows):raise RuntimeError('schema')
 views[mode]=rows
n=get('metadata_after',['get'],{'spreadsheetId':B,'fields':'spreadsheetId,sheets(properties)'})
if not strict(m,n):raise RuntimeError('metadata drift')
leads=[]
needles=['30003185','bray','involution','strong involution','centraliser','centralizer','10.1016/j.jalgebra.2017.11.047','10.1016/j.jalgebra.2019.09.009','1812.01362','14745-003','dixon','roney-dougal','glasby','2603.22638','classical group']
for mode,rows in views.items():
 for k,row in enumerate(rows[1:],2):
  t=urllib.parse.unquote(unicodedata.normalize('NFKC',' '.join(map(str,row)))).casefold()
  found=[s for s in needles if s in t]
  if re.search(r'(?<!\w)(?:pr\s*#?\s*|pull\s+request\s*#?\s*)1330(?!\w)|github\.com/aleckriebel/math/pull/1330(?!\d)',t):found.append('PR/source-label')
  if found:leads.append({'mode':mode,'row':k,'leads':found})
res={'at':stamp,'sheet_gid':G,'columns':43,'row_counts':{k:len(v) for k,v in views.items()},'metadata_stable':True,'typed_views_identical':strict(*views.values()),'lead_count':len(leads),'lead_locations':leads,'private_capture':str(D.relative_to(P)),'service_write_calls':0}
(P/'LEDGER_DUPLICATE_CHECK_FINAL.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
