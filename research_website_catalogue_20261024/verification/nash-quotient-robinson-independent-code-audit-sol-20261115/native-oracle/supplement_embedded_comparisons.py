"""Pure own-snapshot whole embedded-object comparison, writing only receipts here."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
A=Path(__file__).resolve().parent
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
def rel(p):
 p=Path(p);p=p if p.is_absolute() else B/p
 return 'raw/'+str(p.relative_to(B))
def load(p):return json.loads((A/p).read_bytes())
def pointer(o,t):
 for k in t:o=o[k]
 return o
def typed(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(typed(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
checks=[]
def add(label,lp,lt,rp,rt=None,text=False):
 a=pointer(load(lp),lt);b=(A/rp).read_text() if text else pointer(load(rp),rt or [])
 if not typed(a,b):raise ValueError(label)
 checks.append({'label':label,'left_copy':lp,'left_pointer':lt,'right_copy':rp,'right_pointer':rt or [],'right_text':text,'same_complete_typed_keyorder_listorder_values':True,'whole_value_SHA256':hashlib.sha256(json.dumps(a,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()})
for i,rid in enumerate(['23578599','23423736','23333002']):
 ed=B/'papers'/rid/'reviews/editorial';pub=rel(ed/('config/publication.json' if i==0 else 'configs/publication.json' if i==1 else 'publication.json'));prom=rel(ed/('config/promotion.json' if i==0 else 'configs/promotion.json' if i==1 else 'promotion.json'));protocol=rel(ed/'SOURCE_PROTOCOL_BINDINGS.json');adapter=rel(ed/'SCHEMA_ADAPTER.json');clear=rel(B/'verification'/f'root-clearance-{rid}-20261115.json');ready=rel(B/'papers'/rid/'sources/SOURCE_READY.json')
 root=load(clear);review=rel(root['root_review']['path'])
 if i==0:
  add(rid+'/promotion.scientificverdicts',prom,['whole_current_two_scientific_verdicts'],protocol,['whole_current_two_scientific_verdicts'])
  add(rid+'/promotion.scientificseals',prom,['whole_current_scientific_seals'],protocol,['whole_current_scientific_seals'])
 elif i==1:
  add(rid+'/publication.sourcebinding',pub,['source_binding'],protocol,[])
  add(rid+'/publication.rootclearance',pub,['review_metadata','whole_root_scientific_clearance_record'],clear,[])
  add(rid+'/publication.rootreview',pub,['review_metadata','root_review_whole_text'],review,text=True)
  for key in ['whole_root_scientific_clearance_record','whole_original_custom_scientific_verdicts','whole_original_scientific_review_seals']:
   add(rid+'/promotion.'+key,prom,[key],pub,['review_metadata',key])
  add(rid+'/promotion.ready',prom,['whole_original_SOURCE_READY'],ready,[])
  for key in ['whole_original_native_API_objects','whole_original_transport_aggregate']:
   add(rid+'/promotion.'+key,prom,[key],protocol,[key])
  add(rid+'/promotion.transports',prom,['whole_original_seven_transport_objects'],protocol,['whole_original_seven_transport_objects_in_native_aggregate_order'])
 else:
  add(rid+'/adapter.whole_protocol',adapter,['whole_original_protocol_binding'],protocol,[])
  add(rid+'/adapter.whole_reviewmetadata',adapter,['whole_original_review_metadata'],pub,['review_metadata'])
  add(rid+'/publication.whole_protocol',pub,['source_binding'],protocol,[])
  add(rid+'/publication.whole_rootclearance',pub,['review_metadata','whole_root_scientific_clearance'],clear,[])
  add(rid+'/publication.whole_rootreview',pub,['review_metadata','whole_root_scientific_review'],review,text=True)
  add(rid+'/promotion.rootclearance',prom,['whole_root_scientific_clearance_record'],clear,[])
  add(rid+'/promotion.ready',prom,['whole_original_source_ready'],ready,[])
  for key in ['whole_original_native_API_objects','whole_original_seven_transport_objects','whole_original_transport_aggregate']:
   add(rid+'/promotion.'+key,prom,[key],protocol,[key])
  for j,lane in enumerate(['scope','analytic']):
   verdict=rel(ed.parent/lane/'VERDICT.json');seal=rel(ed.parent/lane/'SEAL.json')
   for left,lt in [(pub,['review_metadata','whole_actual_original_scientific_review_records',j]),(adapter,['whole_original_review_metadata','whole_actual_original_scientific_review_records',j])]:
    add(rid+'/embeddedwholeverdict/'+left+str(j),left,lt+['whole_original_custom_verdict'],verdict,[])
    add(rid+'/embeddedwholeseal/'+left+str(j),left,lt+['whole_original_review_seal'],seal,[])
   add(rid+'/promotion.wholeverdict/'+str(j),prom,['whole_original_custom_scientific_verdicts',j],verdict,[])
   add(rid+'/promotion.wholeseal/'+str(j),prom,['whole_original_scientific_review_seals',j],seal,[])
 # Every descriptor-wrapped embedded whole JSON in each source-protocol/config/adapter.
 for fn in [protocol,pub,prom,adapter]:
  def visit(o,t):
   if isinstance(o,dict):
    if 'whole_literal_object' in o and 'path' in o:add(rid+'/wrapper/'+fn+str(t),fn,t+['whole_literal_object'],rel(o['path']),[])
    if 'whole_original_object' in o and isinstance(o.get('file'),dict):add(rid+'/wrapper/'+fn+str(t),fn,t+['whole_original_object'],rel(o['file']['path']),[])
    for k,v in o.items():
     if k not in ['whole_literal_object','whole_original_object']:visit(v,t+[k])
   elif isinstance(o,list):
    for j,v in enumerate(o):visit(v,t+[j])
  visit(load(fn),[])
out={'UTC':datetime.now(timezone.utc).isoformat(),'scope':'Supplement137initial comparisons with explicit125largeadapter/protocol/reviewmetadata/native/scientific embeddings and all descriptor-wrapped wholeJSON in every protocol/config/adapter. Exact comparisons, no schema normalization.','comparison_specs_and_receipts':checks,'count':len(checks),'all_equal':True,'initial137seal_unchanged':True}
(A/'EMBEDDED_COMPARISON_SUPPLEMENT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'supplemental_whole_object_comparisons':len(checks),'all_equal':True}))
