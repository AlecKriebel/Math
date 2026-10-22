from pathlib import Path
import json, subprocess, datetime, hashlib, unicodedata, re, urllib.parse, gzip, sys
P=Path(__file__).resolve().parent
SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'; GID=1254632077
phase=sys.argv[1] if len(sys.argv)>1 else 'initial'
if phase not in ['initial','final']:raise RuntimeError('phase')
D=P/'private'/('ledger_'+phase);D.mkdir(exist_ok=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def get(name,params):
 c=['gws','sheets','spreadsheets']+(['get'] if name.startswith('metadata') else ['values','get'])+['--params',json.dumps(params)]
 r=subprocess.run(c,capture_output=True)
 (D/(name+'.stderr')).write_bytes(r.stderr)
 if r.returncode:raise RuntimeError('read failed '+name)
 (D/(name+'.json.gz')).write_bytes(gzip.compress(r.stdout,mtime=0))
 return json.loads(r.stdout),{'name':name,'raw_sha256':sha(r.stdout),'raw_bytes':len(r.stdout)}
m,mi=get('metadata_before',{'spreadsheetId':SID,'fields':'spreadsheetId,sheets(properties)'})
if m['spreadsheetId']!=SID:raise RuntimeError('wrong spreadsheet')
s=[x['properties'] for x in m['sheets'] if x['properties']['sheetId']==GID]
if len(s)!=1 or s[0]['title']!='Math Puzzles' or s[0]['gridProperties']['columnCount']!=43:raise RuntimeError('wrong tab')
last=s[0]['gridProperties']['rowCount'];ran="'Math Puzzles'!A1:AQ"+str(last)
views={};receipts=[mi]
for mode in ['UNFORMATTED_VALUE','FORMULA']:
 j,receipt=get(mode,{'spreadsheetId':SID,'range':ran,'valueRenderOption':mode,'majorDimension':'ROWS'})
 if j['range']!=ran or j['majorDimension']!='ROWS':raise RuntimeError('range mismatch')
 rows=j['values']
 if rows[0]!=['Original Problem','Solution Chat URL','DOI','Notes'] or any(type(x)is not list or len(x)>43 for x in rows):raise RuntimeError('schema')
 views[mode]=rows;receipts.append(receipt)
n,ni=get('metadata_after',{'spreadsheetId':SID,'fields':'spreadsheetId,sheets(properties)'})
if m!=n:raise RuntimeError('metadata drift')
receipts.append(ni)
def normalize(t):
 t=urllib.parse.unquote(unicodedata.normalize('NFKD',t)).casefold()
 t=''.join(c for c in t if not unicodedata.combining(c))
 return re.sub(r'[^a-z0-9]+','',t)
exact=['30003208', '30002897', 'PR1329', 'https://github.com/AlecKriebel/Math/pull/1329', 'Dykema Kostler Williams', 'Question5.3.5', 'tail algebra generation', 'symmetric states', 'Quantum symmetric states on free product']
semantic=['dykema', 'köstler', 'kostler', 'weihua liu', 'symmetric state', 'tail algebra', 'tail generation', 'free product', '5.3.5', 'conditional expectation']
leads=[]
for mode,rows in views.items():
 for num,row in enumerate(rows[1:],2):
  text=' '.join(map(str,row));plain=normalize(text)
  hits=[x for x in exact if normalize(x) in plain]
  words=[x for x in semantic if x in unicodedata.normalize('NFKC',text).casefold()]
  if hits or words:leads.append({'mode':mode,'row':num,'exact_alias_hits':hits,'semantic_hits':words,'values':row})
result={'schema':'pr1329-preparation-ledger-check/v1','phase':phase,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'spreadsheet_id':SID,'numeric_gid':GID,'range':ran,'column_count':43,'row_counts':{k:len(v) for k,v in views.items()},'typed_views_equal':type(views['FORMULA'])is type(views['UNFORMATTED_VALUE']) and views['FORMULA']==views['UNFORMATTED_VALUE'],'metadata_stable':True,'exact_aliases':exact,'semantic_aliases':semantic,'leads':leads,'captures':receipts,'service_write_calls':0}
(D/'leads.json').write_text(json.dumps(leads,indent=2,ensure_ascii=False)+'\n')
result['leads']=[{k:v for k,v in x.items() if k!='values'} for x in leads]
(P/(phase.upper()+'_LEDGER_CHECK.json')).write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['leads','exact_aliases','semantic_aliases','captures']},indent=2));print('lead rows',[(x['mode'],x['row'],x['exact_alias_hits'],x['semantic_hits']) for x in leads])
