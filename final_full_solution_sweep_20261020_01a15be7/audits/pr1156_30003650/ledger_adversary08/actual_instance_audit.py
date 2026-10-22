#!/usr/bin/env python3
"""Independent context inventory of the exact preserved197/181 instance.
No helper or project imports; no I/O outside this review folder except rechecking pins.
"""
import collections,hashlib,json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
HERE=Path(__file__).resolve().parent
PINS=json.loads((HERE/'SOURCE_PINS.json').read_text())['files']
byname={Path(e['original']).name:e for e in PINS}
def load(e):
 b=(HERE/e['snapshot']).read_bytes()
 if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Snapshot mismatch')
 if Path(e['original']).read_bytes()!=b:raise RuntimeError('Original input changed')
 return json.loads(b)
account_entry=byname['account.json'];ledger_entry=byname['ledger_live.json'];plan_entry=byname['LEDGER_RECONCILIATION_PLAN.json']
account=load(account_entry);rows=load(ledger_entry)['response']['values'];plan=load(plan_entry)
if account['total']!=197 or len(account['records'])!=197 or len(rows)!=181 or account['query']!='':raise RuntimeError('Specific fixture cardinality/query mismatch')
if rows[0]!=['Original Problem','Solution Chat URL','DOI','Notes'] or any(not isinstance(r,list) or len(r)>4 or any(not isinstance(v,str) for v in r) for r in rows):raise RuntimeError('Ledger schema mismatch')
if 23408971 not in {r['id'] for r in account['records']}:raise RuntimeError('Known-owned positive control absent')

def strings(value,path='$'):
 if isinstance(value,str):yield path,value
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from strings(v,path+'['+str(i)+']')
 elif isinstance(value,dict):
  for k,v in value.items():
   if isinstance(k,str):yield path+'.KEY('+k+')',k
   yield from strings(v,path+'.'+str(k))

def decode(value):
 for depth in range(8):
  nxt=unquote(value)
  if nxt==value:return value,depth
  value=nxt
 if unquote(value)!=value:raise RuntimeError('Depth exceeds bounded independent review')
 return value,8
BARE=re.compile(r'(?<![A-Za-z0-9.])10/[A-Za-z0-9]+',re.I)
RESOLVER=re.compile(r'(?<![A-Za-z0-9_.-])(?:www\.)?(?:shortdoi\.org|(?:dx\.)?doi\.org)\.*[^\s<>"\[\]{}\x27]*',re.I)
URL=re.compile(r'https?://[^\s<>"\x27]+',re.I)
SEMANTIC=re.compile(r'30003650|OWR.?15957.?003|CP[ _^+–-]*plus|cp\^?\+|positive[ -]?factor[ -]?rank|2335036[34]|Dickinson.{0,60}rank|/pull/1156(?!\d)|\bPR\s*#?1156(?!\d)',re.I)
TARGET_LONG=re.compile(r'10\.5281/zenodo\.(23350363|23350364)(?![0-9])',re.I)
known_md5={f['checksum'].lower().removeprefix('md5:') for f in plan['existing_publication']['files']}
all_text=[]
for item in account['records']:
 for p,v in strings(item):all_text.append(('account',item['id'],p,v))
for p,v in strings(rows):all_text.append(('ledger',None,p,v))
bare=[];resolver=[];urlcontexts=[];semantic=[];md5=[];unresolved=[];deep=[]
for kind,identifier,path,raw in all_text:
 value,depth=decode(raw)
 if depth:deep.append({'kind':kind,'id':identifier,'path':path,'depth':depth})
 base={'kind':kind,'id':identifier,'path':path}
 for m in BARE.finditer(value):
  token=m.group();context=value[max(0,m.start()-100):min(len(value),m.end()+140)]
  reason=None
  if identifier==23442649 and 'math.hmc.edu' in value and '/sites/10/2019/06/' in value and token=='10/2019':reason='Ordinary dated external HTTP path sites/10/2019/06, followed by another path segment; no isolated short DOI.'
  elif identifier==23441890 and '21tkt-1.pdf' in value and '/2026/10/21tkt-1.pdf' in value and token=='10/21tkt':reason='Ordinary dated external PDF path2026/10/21tkt-1.pdf; the unbounded scanner takes only a filename prefix.'
  elif identifier==23385608 and token=='10/2016' and path in {'$.metadata.description','$.metadata.keywords[6]'} and 'Oberwolfach Report 10/2016' in value and any(ref.endswith('https://doi.org/10.4171/OWR/2016/10') and 'contribution pp. 479-481' in ref and 'Solotar' in ref for ref in next(r for r in account['records'] if r['id']==23385608)['metadata']['references']):reason='Typed Oberwolfach Report10/year2016 description or keyword; same exact record metadata.references[0] names A.Solotar, contributionpp479–481, and exact DOI10.4171/OWR/2016/10. Contextual instance adjudication only.'
  elif kind=='ledger' and path=='$[95][0]' and token=='10/2016' and 'Solotar, Koszul Calculus, OWR 10/2016 pp.479–481' in value and 'https://doi.org/10.4171/OWR/2016/10' in value:reason='Ledger row96 original-problem bibliography explicitly gives Solotar, Koszul Calculus, OWR10/2016 pp479–481 and exact report DOI10.4171/OWR/2016/10 in the same cell; distinct problem30003060.'
  e={**base,'match':token,'context':context,'classification':reason or 'UNRESOLVED'};bare.append(e)
  if not reason:unresolved.append(e)
 for m in RESOLVER.finditer(value):
  token=m.group().rstrip('.,;:!?)]}');lower=token.lower()
  match=re.fullmatch(r'(?:www\.)?(?:dx\.)?doi\.org/10\.[0-9]{4,9}/[^\s]+',token,re.I)
  canonical=bool(match and 'shortdoi.org' not in lower)
  e={**base,'reference':token,'classification':'Ordinary fully spelled long DOI resolver reference' if canonical else 'UNRESOLVED'};resolver.append(e)
  if not canonical:unresolved.append(e)
 for m in URL.finditer(raw):
  token=m.group().rstrip('.,;:!?)]}');dec,_=decode(token)
  try:parts=urlsplit(dec)
  except ValueError:unresolved.append({**base,'url':token,'classification':'UNPARSEABLE_URL'});continue
  urlcontexts.append({**base,'url':token,'decoded_url':dec,'host':parts.netloc,'path_component':parts.path,'query':parts.query,'fragment':parts.fragment})
 if SEMANTIC.search(raw) or SEMANTIC.search(value) or TARGET_LONG.search(value):semantic.append({**base,'matched':SEMANTIC.search(value).group() if SEMANTIC.search(value) else TARGET_LONG.search(value).group(),'context':value[:300]})
for item in account['records']:
 for i,f in enumerate(item['files']):
  c=str(f.get('checksum','')).lower().removeprefix('md5:')
  if c in known_md5:md5.append({'id':item['id'],'file':i,'checksum':c})
# Independently enumerate every recognized familyID from native identities.
owned=set();families=[]
for item in account['records']:
 ids={item['id']}
 if 'conceptrecid' in item:ids.add(int(item['conceptrecid']))
 if item.get('parent',{}).get('id') is not None:ids.add(int(item['parent']['id']))
 for version in item.get('metadata',{}).get('relations',{}).get('version',[]):ids.add(int(version['parent']['pid_value']))
 if item.get('conceptdoi'):ids.add(int(item['conceptdoi'].split('.')[-1]))
 owned|=ids;families.append({'record':item['id'],'ids':sorted(ids)})
# Bind every native machine URL's ID, route, and complete filename/suffix.
# This deliberately does not call v8's projection or identity reader.
records_by_id={r['id']:r for r in account['records']}
known_routes={'','/draft/pids/doi','/files','/media-files','/versions/latest','/latest','/versions','/draft','/access/links','/access/grants','/access/users','/access/request','/access','/communities','/communities-suggestions','/request-deletion','/file-modification','/quota-increase','/requests','/draft/files','/draft/media-files','/draft/actions/publish','/draft/review'}
machine=[];machine_shapes=collections.Counter();machine_unknown=[]
for u in urlcontexts:
 if u['kind']!='account' or not re.match(r'^\$\.(?:links\.|parent\.links\.|files\[[0-9]+\]\.links\.)',u['path']):continue
 shape=None;path=u['path_component'];r=records_by_id[u['id']];filekeys={f['key'] for f in r['files']}
 if u['fragment'] or u['query'] not in {'','preview=1'}:shape=None
 elif u['host']=='doi.org' and re.fullmatch(r'/10\.5281/zenodo\.([1-9][0-9]*)',path):
  m=re.fullmatch(r'/10\.5281/zenodo\.([1-9][0-9]*)',path)
  if int(m.group(1)) in owned and not u['query']:shape='long-owned-doi'
 elif u['host']=='zenodo.org':
  m=re.fullmatch(r'/(?:api/)?records/([1-9][0-9]*)(.*)',path)
  if m and int(m.group(1)) in owned:
   tail=m.group(2)
   if tail in known_routes and (not u['query'] or (u['query']=='preview=1' and tail=='' and path.startswith('/records/'))):shape='owned-record'+tail
   elif tail.startswith('/files/') and tail.endswith('/content') and tail[len('/files/'):-len('/content')] in filekeys and not u['query']:shape='owned-file-exact-key/content'
  m=re.fullmatch(r'/doi/10\.5281/zenodo\.([1-9][0-9]*)',path)
  if m and int(m.group(1)) in owned and not u['query']:shape='owned-doi-route'
  m=re.fullmatch(r'/uploads/([1-9][0-9]*)',path)
  if m and int(m.group(1)) in owned and not u['query']:shape='owned-upload'
  m=re.fullmatch(r'/api/iiif/(record|draft):([1-9][0-9]*)/(manifest|sequence/default)',path)
  if m and int(m.group(2)) in owned and not u['query']:shape='owned-IIIF-'+m.group(1)+'/'+m.group(3)
  m=re.fullmatch(r'/api/iiif/(record|draft):([1-9][0-9]*):(.+)/full/\^(10|50|100|250|750|1200),/0/default\.jpg',path)
  if m and int(m.group(2)) in owned and m.group(3) in filekeys and not u['query']:shape='owned-IIIF-exact-key/thumbnail'
 e={**u,'classification':shape or 'UNRESOLVED_NATIVE_MACHINE_URL'};machine.append(e)
 if shape:machine_shapes[shape]+=1
 else:machine_unknown.append(e);unresolved.append(e)
queries=[u for u in urlcontexts if u['query']]
fragments=[u for u in urlcontexts if u['fragment']]
query_classifications=[]
for u in queries:
 if u['kind']=='account' and u['host']=='zenodo.org' and u['query']=='preview=1' and re.fullmatch('/records/[1-9][0-9]*',u['path_component']):reason='Native provider preview flag1 for owned record; entire original query contains no alias or extra parameter.'
 elif u['kind']=='ledger' and u['host']=='ems.press' and u['query']=='nt=1' and re.fullmatch('/content/serial-article-files/[1-9][0-9]*',u['path_component']):reason='Ordinary EMS source download parameternt=1; no embedded identity alias.'
 elif u['kind']=='ledger' and u['host']=='publications.mfo.de' and u['path_component']=='/bitstream/handle/mfo/3111/OWR_2009_09.pdf' and u['query']=='isAllowed=y&sequence=1':reason='Ordinary MFO repository access/sequence flags on report2009/09; no embedded identity alias.'
 else:reason=None;unresolved.append({**u,'classification':'UNRESOLVED_QUERY'})
 query_classifications.append({**u,'classification':reason})
fragment_classifications=[]
for u in fragments:
 reason='PDF source page locator only' if u['kind']=='ledger' and re.fullmatch('page=[1-9][0-9]*',u['fragment']) and '.pdf' in u['path_component'].lower() or u['kind']=='ledger' and re.fullmatch('page=[1-9][0-9]*',u['fragment']) and u['host']=='ems.press' and '/content/serial-article-files/' in u['path_component'] or u['kind']=='ledger' and u['decoded_url']=='https://arxiv.org/pdf/1809.07200v2#page=172' else None
 if not reason:unresolved.append({**u,'classification':'UNRESOLVED_FRAGMENT'})
 fragment_classifications.append({**u,'classification':reason})
summary={'specific_instance_only':True,'account_input':account_entry,'ledger_input':ledger_entry,'plan_input':plan_entry,'account_records':197,'ledger_rows':181,'independent_owned_record_concept_union':len(owned),'text_cells_including_keys':len(all_text),'decoded_nontrivial_cells':len(deep),'bare10_occurrences':len(bare),'bare10_context_adjudications':bare,'resolver_occurrences':len(resolver),'noncanonical_resolver_occurrences':sum(r['classification']=='UNRESOLVED' for r in resolver),'all_url_occurrences':len(urlcontexts),'native_machine_url_occurrences':len(machine),'native_machine_shapes':dict(machine_shapes),'unresolved_native_machine_urls':len(machine_unknown),'query_occurrences':len(queries),'distinct_query_values':dict(collections.Counter(u['query'] for u in queries)),'query_adjudication_counts':dict(collections.Counter(u['classification'] for u in query_classifications)),'fragment_occurrences':len(fragments),'fragment_adjudication_counts':dict(collections.Counter(u['classification'] for u in fragment_classifications)),'semantic_or_target_leads':semantic,'known_payload_md5_leads':md5,'unresolved':unresolved,'no_unresolved_identity_leads':not unresolved and not semantic and not md5,'limits':'Finite lexical/context audit of exact preserved inputs only, no live observation, no alias resolution, no worldwide identity claim; fresh instance changes require new review. This is independent of generic helper approval and authorizes no mutation.'}
private={'bare10':bare,'resolvers':resolver,'all_urls':urlcontexts,'native_machine_urls':machine,'queries':query_classifications,'fragments':fragment_classifications,'decoded_fields':deep,'families':families}
(HERE/'private/ACTUAL_INSTANCE_CONTEXTS.json').write_text(json.dumps(private,ensure_ascii=False,indent=2)+'\n')
(HERE/'ACTUAL_INSTANCE_AUDIT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['account_input','ledger_input','plan_input']},ensure_ascii=False,indent=2))
