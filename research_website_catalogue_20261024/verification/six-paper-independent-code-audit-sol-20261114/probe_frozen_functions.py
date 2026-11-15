"""Bounded in-memory final-code reproduction and pure adapter probes only."""
from pathlib import Path
import sys,json,copy,hashlib
E=Path(__file__).resolve().parent;P=E.parents[1];W=P/'verification/six-paper-private-stage-sol-20261114';sys.path.insert(0,str(W));sys.dont_write_bytecode=True
from six_source import load_bundles,native_assets,validate_transports,validate_authorities
from six_common import safe_output,safe_name,contained,load,require
from build_private import article_bytes,overlays
from six_body_contract import check_page
def need(ok,s):
 if not ok:raise ValueError(s)
def canonical(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'),default=str)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 before={x['path']:h(W/x['path']) for x in load(W/'OWNED_MANIFEST.json')['files']};frozen=load(W/'FROZEN_INPUT_SET.json');bundles=load_bundles();generated=overlays(bundles,'2026-11-15');probes=[];preserved=[];bodychecks=0
 for b in bundles:
  c=b['c'];rid=b['rid'];prefix='research/'+c['slug']+'/';snapshot=canonical(b);generated[prefix+'index.html']=article_bytes(b,'2026-11-15');generated[prefix+'citation.bib']=b['prepared_bibtex']
  for a in b['asset_view']:generated[prefix+a['name']]=Path(a['path']).read_bytes()
  need(canonical(b)==snapshot,'builder caller input preserved');files={p.name:p.read_bytes() for p in (W/'final-build-a/public/research'/c['slug']).iterdir() if p.is_file()};checks=check_page(b,files['index.html'],files,build_date='2026-11-15');need(all(checks.values()),'actual complete code contract positive');bodychecks+=len(checks)
  spec=frozen['native_specs'][rid];S=b['paper']/'sources';ready=load(S/'SOURCE_READY.json');api=load(S/'record.raw.json');tr=[load(S/n) for n in spec['transport_files']];science=load(spec['whole_root_science']['path']);original=canonical([ready,api,tr,c,b['g'],science,spec])
  native_assets(rid,b['paper'],ready,api,c,spec);validate_transports(rid,b['paper'],tr,spec);validate_authorities(rid,c,b['g'],science)
  need(canonical([ready,api,tr,c,b['g'],science,spec])==original,'all caller-owned native/authority objects preserved');preserved.append(rid)
  def reject(label,fn):
   try:fn()
   except (ValueError,KeyError,TypeError):probes.append({'record_id':rid,'fault':label,'rejected':True})
   else:raise ValueError('fault accepted '+rid+'/'+label)
  rr=copy.deepcopy(ready);aa=copy.deepcopy(api);rr[spec['ready_array']].reverse();aa['files'].reverse();reject('asset_order_both_copies_changed',lambda:native_assets(rid,b['paper'],rr,aa,c,spec))
  tt=copy.deepcopy(tr)
  def change_header(x):
   if isinstance(x,dict):
    for k,v in x.items():
     if 'headers' in k and isinstance(v,list) and len(v)>1:v.reverse();return True
     if change_header(v):return True
   elif isinstance(x,list):
    for v in x:
     if change_header(v):return True
   return False
  need(change_header(tt),'actual received headers found');reject('ordered_received_headers_reversed',lambda:validate_transports(rid,b['paper'],tt,spec))
  gg=copy.deepcopy(b['g']);gg['status']='PASS';reject('qualified_status_coerced_to_generic_PASS',lambda:validate_authorities(rid,c,gg,science))
  gg=copy.deepcopy(b['g']);gg['AA']='https://example.org/unverified/';reject('premature_native_AA',lambda:validate_authorities(rid,c,gg,science))
  reject('unsupported_record_ID_no_source_access',lambda:native_assets('not-authorized',b['paper'],ready,api,c,spec))
 actual={str(p.relative_to(W/'final-build-a/public')):p.read_bytes() for p in (W/'final-build-a/public').rglob('*') if p.is_file()};need(generated==actual and len(actual)==26,'all final-code outputs reproduce in memory')
 escapes=[]
 for path in [E/'private-fixtures/forbidden-output',Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/forbidden-output')]:
  try:safe_output(path)
  except ValueError:escapes.append(str(path))
  else:raise ValueError('external output accepted')
 need(len(escapes)==2,'both output escapes rejected')
 for x in frozen['files']:
  p=Path(x['path']);need(p.stat().st_size==x['bytes'] and h(p)==x['sha256'],'all1084original frozen inputs unchanged')
 need({x['path']:h(W/x['path']) for x in load(W/'OWNED_MANIFEST.json')['files']}==before,'candidate owned bytes unchanged after functions/probes')
 return {'status':'PASS_BOUNDED_FROZEN_FUNCTION_REPRODUCTION_AND_ADAPTER_PROBES','whole_output_files_reproduced_in_memory':26,'all_record_caller_owned_original_objects_preserved':preserved,'pure_negative_adapter_probes':probes,'outside_private_namespace_output_paths_rejected':escapes,'actual_body_contract_checks':bodychecks,'all_original_frozen_input_bindings_unchanged':len(frozen['files']),'candidate_owned_payloads_unchanged':len(before),'disk_builder_runs':0,'source_scientific_programs_or_old_campaigns_run':0,'production_site_or_native_writes':0,'network_requests':0}
if __name__=='__main__':print(json.dumps(main(),indent=2))
