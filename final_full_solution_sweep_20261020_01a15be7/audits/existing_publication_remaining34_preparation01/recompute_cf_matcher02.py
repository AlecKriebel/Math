"""Adopt the actual inherited decoded recursive matcher, preserving prior full matrices."""
from pathlib import Path
import types,sys,json,gzip,hashlib,datetime
O=Path(__file__).resolve().parent;D=O.parent/'existing_publication_remaining_rows_inventory01'
for name in['ops_core','identity_gate']:
 p=O/'source'/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(p.read_bytes(),str(p),'exec',optimize=0),m.__dict__)
core=sys.modules['ops_core'];matcher=sys.modules['identity_gate'].matched
def gz(root,n):return json.loads(gzip.decompress((root/'private'/(n+'.json.gz')).read_bytes()))
plan=json.loads((O/'PROPOSAL.json').read_bytes());sem=gz(O,'SEMANTIC_DECISIONS');old={(d['pr'],d['carrier_index']):d for d in sem['decisions']};old.update({(d['pr'],d['carrier_index']):d for d in json.loads((O/'CF_COMPLETE_SCOPE_REBINDING.json').read_bytes())['rebound_carriers']});idx=gz(O,'FULL_CARRIER_REFERENCE_INDEX')['carriers'];base={x['key']:x['full_carrier']for x in gz(D,'closing_FULL_CARRIERS')};own=gz(D,'terminal_owned_complete_pass1')['records'];loc=gz(D,'terminal_LOCAL_SCIENTIFIC_CARRIERS')['items'];numeric=gz(O,'numeric_complete')['values'];groups=gz(O,'SEMANTIC_READING_GROUPS')['groups'];groupmap={c['index']:i for i,g in enumerate(groups)for c in g['carriers']};scope=sem['all_scope_witnesses'];out=[];new=[];unread=[]
for c in idx:
 source=c['source'];key=c['key'];body=own[source['records_key']]if'records_key'in source else loc[source['items_index']]if'items_index'in source else numeric[236]if key=='sheet:237'else base[key];i=idx.index(c)
 for target in plan['items']:
  h=matcher(body,target)
  if not h:continue
  k=(target['pr'],i);previous=old.get(k);g=groupmap.get(i)
  if previous:witness=previous['scope_witness'];reason=previous['scientific_reason'];classification=previous['classification']
  elif c['kind']=='proposal':
   other=next(t for t in plan['items']if t['pr']==int(key.split(':')[1]));witness={'note':other['scope_note'],'complete_source_contract':other['original_source_contract']};reason='Other exact result scope: '+other['scope_note']+' Target exact result scope: '+target['scope_note'];classification='DISTINCT_SPECIFIC_CARRIER_SCOPE_PROPOSED'
  elif g is not None:witness=scope[str(g)];reason=witness['note']+' Target exact result scope: '+target['scope_note'];classification='DISTINCT_SPECIFIC_CARRIER_SCOPE_PROPOSED'
  elif key=='sheet:237':witness=scope['391'];reason=witness['note']+' Target exact result scope: '+target['scope_note'];classification='DISTINCT_SPECIFIC_CARRIER_SCOPE_PROPOSED'
  else:witness=None;reason=None;classification='HOLD_NEW_MATCHER_CARRIER_SCOPE_NOT_READ';unread.append({'pr':target['pr'],'carrier_index':i,'carrier_key':key,'source':source,'matched':h})
  d={'pr':target['pr'],'kind':c['kind'],'carrier_index':i,'carrier_key':key,'body_sha256':core.sha(core.canonical(body)),'matched':h,'scientific_reason':reason,'classification':classification,'scope_witness':witness,'target_four_cells_sha256':target['row_sha256'],'source':source,'root_adopted':False};out.append(d)
  if not previous:new.append({'pr':target['pr'],'carrier_index':i,'carrier_key':key,'matched':h,'classification':classification})
raw=(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'matcher':'Byte-identical CF25source03 ops_core recursive_identity_hits, including HTML/percent/Unicode decoding and exact PR/arXiv grammar. No metadata projection/author waiver.','decisions':out,'new_positive_pairs':new,'unread_new_carriers':unread,'all_pairs_considered':34*len(idx),'action_authority':False},ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode();p=O/'private/CF_TYPED_MATCHER_SEMANTICS02.json.gz';assert not p.exists();p.write_bytes(gzip.compress(raw,mtime=0));print(json.dumps({'actual_recursive_positive_pairs':len(out),'additional_pairs':len(new),'unread_new_carriers':unread,'physical_bytes':sum(p.lstat().st_blocks*512 for p in[O,*O.rglob('*')])}))
