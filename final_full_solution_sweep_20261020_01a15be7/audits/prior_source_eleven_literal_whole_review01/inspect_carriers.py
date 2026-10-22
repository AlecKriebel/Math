"""Offline, read-only scan of complete observed carriers; writes own review output only."""
import gzip,hashlib,json,pathlib,re
O=pathlib.Path(__file__).resolve().parent;B=O.parents[1]
def ld(p):return json.loads(p.read_bytes())
def gz(p):return json.loads(gzip.decompress(p.read_bytes()))
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sh(x):return hashlib.sha256(canon(x)).hexdigest()
P={932:r'\b30003471\b|Stoker|polytopal tensegrit|dihedral.rigid',967:r'\b2616\b|21[._]107|expansive|ultrafilter',1036:r'\b5500042\b|vertex.unfold|vertex.ununfold',1063:r'\b30000391\b|Farley|Bj[oö]rner|geometric.lattic|matching.points',1170:r'\b2009\b|Erd[oőö]s.{0,10}252|Tokengr|factorial.divisor',1182:r'\b2141\b|Erd[oőö]s.{0,10}486|delayed.siev|multiscalar',1183:r'\b2142\b|Erd[oőö]s.{0,10}488|Gessel|density.doubling',1184:r'\b2166\b|Erd[oőö]s.{0,10}538|STARFLEET|reciprocal.sum',1189:r'\b2334\b|Erd[oőö]s.{0,10}(839|867)|Freud|consecutive.sum|Coppersmith',1190:r'\b2283\b|Erd[oőö]s.{0,10}730|Blair|binomial|prime.divisor',1224:r'\b2302\b|Erd[oőö]s.{0,10}783|Dickman|sieving|coprime'}
P[932]+=r'|\bWinter\b'
P[967]+=r'|\bKinyon\b|\bUrban\b'
P[1036]+=r'|\bAbel\b|\bDemaine\b'
P[1224]+=r'|\bTao\b|\bChojecki\b'
for pr in P:P[pr]+=r'|/pull/'+str(pr)+r'\b'
obs=gz(O/'initial_observation.json.gz');C=[]
for i,r in enumerate(obs['value_raw']['valueRanges'][0]['valueRange']['values'],1):C.append(('ledger',str(i),r))
for x in obs['local']:C.append(('local',pathlib.Path(x['path']).name,x['value']))
R=B/'audits/pr1330_30003185/root_ledger_preflight01/private';passes=[]
for k in [0,1]:
 records=[]
 for p in sorted(R.glob('account_pass'+str(k)+'_page*.json.gz'),key=lambda p:int(re.search('page([0-9]+)',p.name)[1])):
  records+=gz(p)
 assert len(records)==204 and len({str(x['id'])for x in records})==204
 passes.append({str(x['id']):x for x in records})
assert sh(passes[0])==sh(passes[1])
for k,v in passes[0].items():C.append(('dated_owned',k,v))
f=ld(B/'audits/existing_publication_remaining_rows_inventory01/FROZEN_PROPOSALS.json')
for v in f['items']:C.append(('frozen34',str(v['pr']),v['row']))
def title(x):
 if isinstance(x,list):return str(x[0])+' :: '+str(x[3])[:240] if len(x)>3 else str(x)
 if not isinstance(x,dict):return ''
 for key in ['metadata','publication','original_metadata','target_metadata','original','target']:
  z=x.get(key)
  if isinstance(z,dict):
   if z.get('title'):return z['title']+' :: '+str(z.get('description',''))[:260]
   if isinstance(z.get('metadata'),dict) and z['metadata'].get('title'):return z['metadata']['title']+' :: '+str(z['metadata'].get('description',''))[:260]
 return str(x.get('manifest',''))
leads=[]
for pr,pat in P.items():
 r=re.compile(pat,re.I)
 for kind,key,v in C:
  t=json.dumps(v,ensure_ascii=False,sort_keys=True);ms=list(r.finditer(t))
  if ms:leads.append({'pr':pr,'kind':kind,'key':key,'complete_carrier_sha256':sh(v),'title_scope':title(v),'matched':list(dict.fromkeys(m.group()for m in ms)),'snippets':[t[max(0,m.start()-90):m.end()+100]for m in ms[:3]]})
rows=ld(B/'PRIOR_SOURCE_ELEVEN_ROOT_ADOPTED_LITERAL_ROWS.json')['rows'];assert [v['pr']for v in rows]==list(P)
exact=[]
for v in rows:
 for kind,key,carrier in C:
  if isinstance(carrier,list)and carrier[:4]==v['values'] and all(x==''for x in carrier[4:]):exact.append({'pr':v['pr'],'kind':kind,'key':key})
out={'patterns':P,'complete_carrier_counts':{'ledger':239,'local':250,'dated_owned':204,'frozen34':34},'dated_owned_two_passes_equal':True,'dated_owned_snapshot_hash':sh(passes[0]),'fresh_owned_absence_claim':False,'exact_row_matches':exact,'leads':leads}
(O/'CARRIER_LEADS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'counts':out['complete_carrier_counts'],'lead_count':len(leads),'exact':exact}))
for i,v in enumerate(leads):print(i,v['pr'],v['kind'],v['key'],v['matched'],v['title_scope'][:250])
