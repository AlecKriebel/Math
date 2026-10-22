"""Deliberately overbroad literal10/ scan with neither token boundary required."""
import collections,json,re
from pathlib import Path
from urllib.parse import unquote
H=Path(__file__).resolve().parent
account=json.loads((H/'private/source_14_account.json').read_bytes());ledger=json.loads((H/'private/source_10_ledger_live.json').read_bytes())['response']['values']
def strings(v,p='$'):
 if isinstance(v,str):yield p,v
 elif isinstance(v,list):
  for i,x in enumerate(v):yield from strings(x,p+'['+str(i)+']')
 elif isinstance(v,dict):
  for k,x in v.items():
   yield p+'.KEY('+k+')',k
   yield from strings(x,p+'.'+k)
items=[]
for r in account['records']:
 for p,s in strings(r):items.append(('account',r['id'],p,s))
for p,s in strings(ledger):items.append(('ledger',None,p,s))
extra=[]
for kind,identifier,p,s in items:
 for _ in range(8):
  n=unquote(s)
  if n==s:break
  s=n
 for m in re.finditer('10/[A-Za-z0-9]+',s):
  if not m.start() or not(s[m.start()-1].isascii() and s[m.start()-1].isalnum() or s[m.start()-1]=='.'):continue
  category=None
  if any(d.start()<=m.start()<d.end() for d in re.finditer(r'10\.[0-9]{4,9}/[^\s<>"\x27]+',s)):category='Substring inside a fully spelled long DOI name or its year/suffix'
  elif kind=='account' and any(d.start()<=m.start()<d.end() for d in re.finditer(r'(?:/records/|/record:|/draft:)[1-9][0-9]*/',s)):category='Trailing digits of an already independently classified owned record ID'
  elif kind=='ledger' and p=='$[132][3]' and m.group()=='10/20' and 'dated10/20 (October2020)' in s:category='Explicit calendar date10/20 (October2020) in row133 notes'
  extra.append({'kind':kind,'id':identifier,'path':p,'match':m.group(),'context':s[max(0,m.start()-60):m.end()+100],'classification':category or 'UNRESOLVED'})
result={'adds_to_the5_standalone_bare_occurrences':len(extra),'category_counts':dict(collections.Counter(e['classification'] for e in extra)),'unresolved':[e for e in extra if e['classification']=='UNRESOLVED'],'results':extra,'scope':'Overbroad substring controls, not extra standalone short DOI names; no project/helper imports or services.'}
(H/'private/LITERAL10_SUPPLEMENT_CONTEXTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(H/'LITERAL10_SUPPLEMENT.json').write_text(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
