"""Independent pure local custody verifier. No project imports, network, subprocess,
source execution, scientific replay, rendering, bytecode generation, or writes.
Default only reads this immutable oracle; --live-baseline additionally reads the
unchanged original research namespaces/stage blobs and native buffers. It never
requires the old live website aggregates, so it remains usable after installation.
"""
from pathlib import Path
import hashlib,json,sys
A=Path(__file__).resolve().parent
BASE=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
STAGE=BASE/'verification/nash-quotient-robinson-private-stage-sol-20261115'
checks=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 need(p.is_file() and not p.is_symlink(),'regular nonsymlink '+str(p));return p.read_bytes()
def load(p):return json.loads(read(p))
def typed(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(typed(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
def raw(path):
 p=Path(path);p=p if p.is_absolute() else BASE/p
 return A/'raw'/p.relative_to(BASE)
def same(label,a,b):need(typed(a,b),'whole typed ordered '+label)
need(sys.argv[1:] in ([],['--live-baseline'],['--preseal']),'bounded optional mode')
live=sys.argv[1:]==['--live-baseline'];pre=sys.argv[1:]==['--preseal']
inputs=load(A/'INPUT_MANIFEST.json');contract=load(A/'WHOLE_LITERAL_NATIVE_CONTRACT.json');comparison=load(A/'STAGE_NATIVE_COMPARISON.json')
need(len(inputs['files'])==628,'exact628ownoriginalinputs')
need('raw/' in read(A/'.gitignore').decode().splitlines(),'whole raw namespace ignored')
need(not any(p.is_symlink() for p in (A/'raw').rglob('*')),'raw symlinks forbidden')
need({str(p.relative_to(A)) for p in (A/'raw').rglob('*') if p.is_file()}=={r['copy'] for r in inputs['files']},'entire raw namespace no exclusions')
for r in inputs['files']:
 b=read(A/r['copy']);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'raw byte identity '+r['copy'])
 if live:need(read(Path(r['original']))==b,'optional original identity '+r['original'])
for n in inputs['namespaces']:
 relative=Path(n['path']).relative_to(BASE);root=A/'raw'/relative
 need(sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())==n['files'],'complete own namespace '+str(relative))
 if live:
  source=Path(n['path']);need(not any(p.is_symlink() for p in source.rglob('*')),'optional source namespace symlinks')
  need(sorted(str(p.relative_to(source)) for p in source.rglob('*') if p.is_file())==n['files'],'optional source namespace membership')
need([n['count'] for n in inputs['namespaces']]==[58,56,232,62,122,77],'exact six complete namespace counts')
for i,rec in enumerate(contract['records']):
 rid=rec['record_id'];ed=BASE/'papers'/rid/'reviews/editorial';s=rec['source_READY_whole_literal']
 for label,fn,key in [('SOURCE_READY',BASE/'papers'/rid/'sources/SOURCE_READY.json','source_READY_whole_literal'),('rights',ed/'RIGHTS_AND_IDENTITY.json','rights_whole_literal'),('publication',ed/rec['publication_config'],'original_publication_config_whole_literal'),('promotion',ed/rec['promotion_config'],'original_promotion_config_whole_literal'),('protocol',ed/'SOURCE_PROTOCOL_BINDINGS.json','source_protocol_whole_literal'),('rooteditorial',BASE/'verification'/f'root-editorial-{rid}-20261115.json','whole_root_editorial_authority')]:same(rid+'/'+label,load(raw(fn)),rec[key])
 for j,r in enumerate(s['whole_native_API_objects']):same(rid+'/API/'+str(j),load(raw(r['path'])),rec['native_API_whole_literal_objects'][j])
 same(rid+'/transport aggregate',load(raw(s['actual_transport_receipts']['path'])),rec['transports_whole_literal_aggregate'])
 same(rid+'/native schema',load(raw(s['native_schema_types']['path'])),rec['native_schema_whole_literal'])
 verdict_paths=[ed.parent/'scope/VERDICT.json',ed.parent/'analytic/CUSTOM_VERDICT.json'] if i==0 else [ed.parent/'analytic/VERDICT.json',ed.parent/'adversarial/VERDICT.json'] if i==1 else [ed.parent/'scope/VERDICT.json',ed.parent/'analytic/VERDICT.json']
 for j,v in enumerate(verdict_paths):same(rid+'/heterogeneous custom scientific verdict/'+str(j),load(raw(v)),rec['whole_original_scientific_custom_verdicts'][j])
 transports=rec['transports_whole_literal_aggregate']['receipts'];need(len(transports)==7 and [x['HTTP_status'] for x in transports]==[200,301,200,200,200,200,200],'literal transport count/order')
 for j,t in enumerate(transports):
  same(rid+'/transport/'+str(j),load(raw(t['body_path']+'.transport.json')),t)
  b=read(raw(t['body_path']));need(len(b)==t['body_bytes'] and sha(b)==t['body_SHA256'] and hashlib.md5(b).hexdigest()==t['body_MD5'],'literal transport wholebody identity')
 need(s['completion_percent_at_preseal']==95 and s['printed_title_date_version_inspected'] is False and s['publication_authority'] is False and s['scientific_verdict'] is None,'literal source history not revised')
 need(s['selected_actual_PDF']['pages']==[5,4,4][i] and s['whole_regular_payload_occurrences']==[21,195,85][i],'original pages/payloads')
 need(rec['separate_code_license_exact']==('MIT' if i==0 else None),'actual separate code instruments')
 pub=rec['original_publication_config_whole_literal'];need(pub['canonical_url'] is None and pub['AA'] is None and pub['follow_up'] is None,'immutable original nulls')
 for asset in s['all_native_assets_in_original_order']:
  b=read(raw(asset['path']));need(len(b)==asset['bytes'] and sha(b)==asset['SHA256'] and 'md5:'+hashlib.md5(b).hexdigest()==asset['original_api_file_object']['checksum'],'complete native asset identity')
stage=load(A/'stage-read/SOURCE_INPUTS.json');stage_lookup={r['path']:r for r in stage['files']};need(len(stage['files'])==1118,'actualstage1118sourcebindings')
need(len(comparison['whole_native_source_editorial_authority_files'])==628 and len(comparison['native_buffers'])==6,'actual bounded stage comparisons')
for r in inputs['files']:
 row=stage_lookup[r['original']];need(row['bytes']==r['bytes'] and row['SHA256']==r['SHA256'],'recorded stage whole binding equals independent original')
 if live:need(read(STAGE/row['blob'])==read(A/r['copy']),'optional actualstage blob identity')
for row in comparison['read_bindings']:
 b=read(A/row['own_copy']);need(len(b)==row['bytes'] and sha(b)==row['SHA256'],'whole stage reading copy')
for row in comparison['native_buffers']:
 need(row['both_whole_stage_buffers_equal_original'] is True,'both full renderbuffers compared')
 if live:
  b=read(STAGE/'candidate-a/public'/row['path']);c=read(STAGE/'candidate-b/public'/row['path']);need(b==c and len(b)==row['bytes'] and sha(b)==row['SHA256'],'optional actual fullnative buffer identity')
need(all(x['same_types_keys_keyorder_listorder_values'] for x in load(A/'COMPARISON_RECEIPTS.json')['whole_typed_ordered_comparisons']),'all137initialwholecomparisons')
supplement=load(A/'EMBEDDED_COMPARISON_SUPPLEMENT.json')
need(supplement['count']==123 and supplement['all_equal'] is True,'123supplementcomparisons')
for spec in supplement['comparison_specs_and_receipts']:
 left=load(A/spec['left_copy'])
 for token in spec['left_pointer']:left=left[token]
 right=read(A/spec['right_copy']).decode() if spec['right_text'] else load(A/spec['right_copy'])
 if not spec['right_text']:
  for token in spec['right_pointer']:right=right[token]
 same(spec['label'],left,right)
seal=load(A/'INITIAL_SEAL.json')
for r in seal['files']:
 b=read(A/r['path']);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'immutable prewriter nativeoracle initialseal')
if not pre:
 final=load(A/'SEAL.json');manifest=load(A/'MANIFEST.json')
 need(sha(read(A/'MANIFEST.json'))==final['manifest_SHA256'],'whole finalmanifest seal')
 need(not any(p.is_symlink() for p in A.rglob('*')),'own namespace symlinks forbidden')
 need({str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()}-{'MANIFEST.json','SEAL.json'}=={r['path'] for r in manifest['files']},'entireownnamespace exact rootterminal exclusions')
 for r in manifest['files']:
  b=read(A/r['path']);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'wholeownpayload identity')
print(json.dumps({'scope':'independent native own custody','mode':'preseal' if pre else 'live-baseline' if live else 'default own custody','positive_checks':checks,'whole_original_raw_files':628,'complete_original_source_editorial_namespaces':6,'editorial_files':195,'native_API_objects':12,'transport_receipts':21,'initial_whole_typed_ordered_comparisons':137,'whole_native_stage_buffers':6,'project_import_network_subprocess_execution_or_writes':False},ensure_ascii=False,indent=2))
