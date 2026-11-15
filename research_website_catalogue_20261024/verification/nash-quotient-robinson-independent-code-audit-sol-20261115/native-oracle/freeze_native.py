"""One-time private independent input freezer; never imports or runs project code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
BASE=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=Path(__file__).resolve().parent
UTC=datetime.now(timezone.utc).isoformat()
IDS=['23578599','23423736','23333002']
ROOTSHA=['82285503c698166536196e2f3ece128d44544bd47c03c64dee8b86caaac2bbac','6391146d989750994bc8270af220d5e57781540c5b30066eb63b90cd08380d5c','715f777230917df4e6c798468fe7659ab7ba69b155ecb515601765fe632f61cc']
def sha(x):return hashlib.sha256(x).hexdigest()
def write(n,o):
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def resolve(p):
 p=Path(p);return p if p.is_absolute() else BASE/p
def load(p):return json.loads(resolve(p).read_bytes())
def typed(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(typed(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
paths=set();namespaces=[];roots={};sources={};editors={}
for rid,pin in zip(IDS,ROOTSHA):
 p=BASE/'verification'/f'root-editorial-{rid}-20261115.json'
 if sha(p.read_bytes())!=pin:raise ValueError('root editorial pin mismatch')
 roots[rid]=load(p);paths.add(p)
 cp=BASE/'verification'/f'root-clearance-{rid}-20261115.json';paths.add(cp)
 c=load(cp);paths.add(resolve(c['root_review']['path']))
 for scope in ['sources','reviews/editorial']:
  d=BASE/'papers'/rid/scope;fs=sorted(x for x in d.rglob('*') if x.is_file())
  if any(x.is_symlink() for x in d.rglob('*')):raise ValueError('symlink in input namespace')
  namespaces.append({'path':str(d),'files':[str(x.relative_to(d)) for x in fs],'count':len(fs),'rule':'every recursive regular file; no basename exclusions'})
  paths.update(fs)
 for lane,fn,seal in ([('scope','VERDICT.json','SEAL.json'),('analytic','CUSTOM_VERDICT.json','FINAL_SEAL.json')] if rid==IDS[0] else [('analytic','VERDICT.json','SEAL.json'),('adversarial','VERDICT.json','FINAL_SEAL.json')] if rid==IDS[1] else [('scope','VERDICT.json','SEAL.json'),('analytic','VERDICT.json','SEAL.json')]):
  paths.add(BASE/'papers'/rid/'reviews'/lane/fn);paths.add(BASE/'papers'/rid/'reviews'/lane/seal)
 sources[rid]=load(BASE/'papers'/rid/'sources/SOURCE_READY.json')
 editors[rid]=load(BASE/'papers'/rid/'reviews/editorial/SOURCE_PROTOCOL_BINDINGS.json')
raw=[]
for p in sorted(paths):
 rel=p.relative_to(BASE);out=OWN/'raw'/rel;b=p.read_bytes();out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
 raw.append({'original':str(p),'copy':str(out.relative_to(OWN)),'bytes':len(b),'SHA256':sha(b)})
write('INPUT_MANIFEST.json',{'UTC':UTC,'scope':'All original source/editorial namespaces without terminal exceptions, root editorial/science/review authorities, current scientific verdicts/seals. Opaque source code copied but never executed.','files':raw,'namespaces':namespaces})
receipts=[]
def compare(label,a,b):
 ok=typed(a,b);receipts.append({'label':label,'same_types_keys_keyorder_listorder_values':ok,'left_tree_SHA256':sha(json.dumps(a,ensure_ascii=False,separators=(',',':')).encode()),'right_tree_SHA256':sha(json.dumps(b,ensure_ascii=False,separators=(',',':')).encode())})
 if not ok:raise ValueError(label)
def checkwrap(label,v):
 if isinstance(v,dict):
  if 'path' in v and 'whole_literal_object' in v:
   p=Path(v['path']);compare(label,load(p),v['whole_literal_object'])
  if 'file' in v and 'whole_original_object' in v:
   p=Path(v['file']['path']);compare(label,load(p),v['whole_original_object'])
  for k,x in v.items():
   if k not in ['whole_literal_object','whole_original_object']:checkwrap(label+'/'+k,x)
 elif isinstance(v,list):
  for i,x in enumerate(v):checkwrap(label+'/'+str(i),x)
records=[]
for i,rid in enumerate(IDS):
 s=sources[rid];e=editors[rid];ed=BASE/'papers'/rid/'reviews/editorial'
 cp='config/publication.json' if i==0 else 'configs/publication.json' if i==1 else 'publication.json'
 pp='config/promotion.json' if i==0 else 'configs/promotion.json' if i==1 else 'promotion.json'
 pub=load(ed/cp);prom=load(ed/pp);authority=roots[rid];clearance=load(BASE/'verification'/f'root-clearance-{rid}-20261115.json')
 compare(rid+'/root.editorialVerdict',load(ed/'VERDICT.json'),authority['whole_literal_editorial_verdict'])
 compare(rid+'/protocol.ready',s,e['whole_original_SOURCE_READY']['whole_literal_object'] if i<2 else e['whole_original_SOURCE_READY'])
 compare(rid+'/clearance.ready',s,clearance['whole_literal_source_ready'] if i==2 else clearance['whole_original_SOURCE_READY'])
 for label,obj in [('protocol',e),('publication',pub),('promotion',prom)]:checkwrap(rid+'/'+label,obj)
 if i:
  compare(rid+'/publication.source_binding',e,pub['source_binding'])
 if i==0:
  verdicts=[load(BASE/'papers'/rid/'reviews/scope/VERDICT.json'),load(BASE/'papers'/rid/'reviews/analytic/CUSTOM_VERDICT.json')]
  compare(rid+'/root.scopeVerdict',verdicts[0],clearance['whole_independent_scope_VERDICT']);compare(rid+'/root.analyticVerdict',verdicts[1],clearance['whole_independent_analytic_CUSTOM_VERDICT'])
 elif i==1:
  verdicts=[load(BASE/'papers'/rid/'reviews/analytic/VERDICT.json'),load(BASE/'papers'/rid/'reviews/adversarial/VERDICT.json')]
  compare(rid+'/root.analyticVerdict',verdicts[0],clearance['whole_independent_analytic_VERDICT']);compare(rid+'/root.adversarialVerdict',verdicts[1],clearance['whole_independent_adversarial_VERDICT'])
 else:
  verdicts=[load(BASE/'papers'/rid/'reviews/scope/VERDICT.json'),load(BASE/'papers'/rid/'reviews/analytic/VERDICT.json')]
  for j,v in enumerate(verdicts):compare(rid+'/root.customVerdict/'+str(j),v,clearance['independent_review_packets'][j]['whole_literal_custom_verdict'])
 api=[load(x['path']) for x in s['whole_native_API_objects']]
 transport=load(s['actual_transport_receipts']['path'])
 for j,receipt in enumerate(transport['receipts']):
  p=Path(receipt['body_path']);b=p.read_bytes()
  if len(b)!=receipt['body_bytes'] or sha(b)!=receipt['body_SHA256'] or hashlib.md5(b).hexdigest()!=receipt['body_MD5']:raise ValueError('receipt body identity')
  t=load(str(p)+'.transport.json');compare(rid+'/transport/'+str(j),receipt,t)
 if i==2:
  compare(rid+'/protocol.transportlist',transport['receipts'],e['whole_original_seven_transport_objects'])
  compare(rid+'/protocol.transportaggregate',transport,e['whole_original_transport_aggregate'])
  for j,x in enumerate(e['whole_original_native_API_objects']):compare(rid+'/protocol.API/'+str(j),api[j],x['whole_original_object'])
  compare(rid+'/protocol.archive',load(s['whole_archive_custody']['path']),e['whole_original_archive_custody'])
  compare(rid+'/protocol.schema',load(s['native_schema_types']['path']),e['whole_original_native_schema_types'])
 if [x['HTTP_status'] for x in transport['receipts']] != [200,301,200,200,200,200,200]:raise ValueError('status order')
 if pub['code_license']!=('MIT' if i==0 else None):raise ValueError('separate code license')
 if s['selected_actual_PDF']['pages']!=[5,4,4][i] or s['whole_regular_payload_occurrences']!=[21,195,85][i]:raise ValueError('page/payload count')
 for a in s['all_native_assets_in_original_order']:
  b=Path(a['path']).read_bytes()
  if len(b)!=a['bytes'] or sha(b)!=a['SHA256'] or 'md5:'+hashlib.md5(b).hexdigest()!=a['original_api_file_object']['checksum']:raise ValueError('native asset')
  compare(rid+'/asset.api-file',a['original_api_file_object'],next(x for x in api[0]['files'] if x['key']==a['original_api_file_object']['key']))
 files_api=api[3]
 # SOURCE_READY deliberately preserves record-vs-file endpoint object heterogeneity.
 records.append({'row':123+i,'record_id':rid,'publication_config':cp,'promotion_config':pp,'source_READY_whole_literal':s,'native_API_whole_literal_objects':api,'transports_whole_literal_aggregate':transport,'native_schema_whole_literal':load(s['native_schema_types']['path']),'whole_original_scientific_custom_verdicts':verdicts,'rights_whole_literal':load(ed/'RIGHTS_AND_IDENTITY.json'),'separate_code_license_exact':pub['code_license'],'original_publication_config_whole_literal':pub,'original_promotion_config_whole_literal':prom,'source_protocol_whole_literal':e,'whole_root_editorial_authority':authority})
write('WHOLE_LITERAL_NATIVE_CONTRACT.json',{'UTC':UTC,'records':records,'warning':'Whole heterogeneous literal original objects, without PASS coercion or schema normalization. This is a custody contract; no new scientific/publication authority.'})
write('COMPARISON_RECEIPTS.json',{'UTC':UTC,'whole_typed_ordered_comparisons':receipts,'count':len(receipts),'all_equal':all(x['same_types_keys_keyorder_listorder_values'] for x in receipts)})
summary={'UTC':UTC,'records':[{'record_id':r['record_id'],'row':r['row'],'PDF_pages':r['source_READY_whole_literal']['selected_actual_PDF']['pages'],'native_assets':[{k:a[k] for k in ['path','bytes','SHA256']} for a in r['source_READY_whole_literal']['all_native_assets_in_original_order']],'API_objects':4,'transport_receipts':7,'HTTP_status_sequence':[200,301,200,200,200,200,200],'recursive_archive_containers':r['source_READY_whole_literal']['recursive_archive_container_count'],'whole_regular_archive_payload_occurrences':r['source_READY_whole_literal']['whole_regular_payload_occurrences'],'separate_code_license_exact':r['separate_code_license_exact'],'source_READY_historical95':r['source_READY_whole_literal']['completion_percent_at_preseal'],'publication_config':r['publication_config'],'promotion_config':r['promotion_config']} for r in records],'namespace_counts':[{k:v for k,v in x.items() if k!='files'} for x in namespaces],'original_files_frozen':len(raw),'whole_typed_ordered_comparisons':len(receipts),'native_code_executed':False,'stage_writer_or_output_accessed':False,'completion_percent_bounded_custody_contract':80}
write('SUMMARY.json',summary)
write('INITIAL_SEAL.json',{'UTC':UTC,'scope':'independent native contract frozen before any stage writer/output access','completion_percent':80,'files':[{ 'path':str(p.relative_to(OWN)),'bytes':len(p.read_bytes()),'SHA256':sha(p.read_bytes())} for p in [OWN/'INPUT_MANIFEST.json',OWN/'WHOLE_LITERAL_NATIVE_CONTRACT.json',OWN/'COMPARISON_RECEIPTS.json',OWN/'SUMMARY.json']]})
(OWN/'RESEARCH_LOG.md').write_text(f'# Native oracle research log\n\n- {UTC}: Independently froze original source/editorial namespaces and whole native custody objects before writer access. Bounded native contract completion estimate: 80%. No project code, scientific campaign, network call, or publication action performed.\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
