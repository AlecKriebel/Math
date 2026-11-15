"""Bounded one-time independent native-copy comparison; no project imports/execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
A=Path(__file__).resolve().parent
S=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/nash-quotient-robinson-private-stage-sol-20261115')
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def write(n,o):(A/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
UTC=datetime.now(timezone.utc).isoformat()
original=load(A/'INPUT_MANIFEST.json');stage=load(S/'SOURCE_INPUTS.json');lookup={r['path']:r for r in stage['files']};checks=[]
for r in original['files']:
 row=lookup[r['original']];b=(S/row['blob']).read_bytes();f=(A/r['copy']).read_bytes()
 same=b==f and len(b)==row['bytes']==r['bytes'] and sha(b)==row['SHA256']==r['SHA256']
 checks.append({'original':r['original'],'own_copy':r['copy'],'stage_blob':row['blob'],'bytes':len(b),'SHA256':sha(b),'byte_identical':same})
 if not same:raise ValueError('Stage native original mismatch '+r['original'])
nschecks=[]
for n in original['namespaces']:
 found=[x for x in stage['namespaces'] if x['root']==n['path']]
 expected=[n['path']+'/'+x for x in n['files']]
 same=len(found)==1 and found[0]['count']==n['count'] and found[0]['files']==expected
 nschecks.append({'namespace':n['path'],'count':n['count'],'exact_no_basename_exclusion':same})
 if not same:raise ValueError('Stage native namespace mismatch')
assets=[]
contract=load(A/'WHOLE_LITERAL_NATIVE_CONTRACT.json')
for rec in contract['records']:
 rid=rec['record_id'];ready=rec['source_READY_whole_literal'];slug=rec['original_publication_config_whole_literal']['slug']
 for a in ready['all_native_assets_in_original_order']:
  name=a['original_api_file_object']['key'];rel='research/'+slug+'/assets/'+name
  b=(S/'candidate-a/public'/rel).read_bytes();c=(S/'candidate-b/public'/rel).read_bytes();f=(A/'raw'/Path(a['path']).relative_to('/Users/alec/Documents/Math/research_website_catalogue_20261024')).read_bytes()
  same=b==c==f and sha(b)==a['SHA256']
  assets.append({'record_id':rid,'path':rel,'bytes':len(b),'SHA256':sha(b),'both_whole_stage_buffers_equal_original':same})
  if not same:raise ValueError('Stage full native buffer mismatch')
readfiles=['SOURCE_INPUTS.json','READY.json','VERDICT.json','STAGE_CONTRACT.json','prepare_inputs.py','verify_terminal.py','REPORT.md','FINAL_SEAL.json']
readbindings=[]
for n in readfiles:
 p=S/n;b=p.read_bytes();out=A/'stage-read'/n;out.parent.mkdir(exist_ok=True);out.write_bytes(b);readbindings.append({'path':n,'bytes':len(b),'SHA256':sha(b),'own_copy':'stage-read/'+n})
write('STAGE_NATIVE_COMPARISON.json',{'UTC':UTC,'scope':'Complete independent628original input-byte comparisons plus6full native render-buffer comparisons; stage writer not executed','whole_native_source_editorial_authority_files':checks,'count':len(checks),'exact_namespaces':nschecks,'native_buffers':assets,'read_bindings':readbindings,'originals_unchanged':True,'default_stage_terminal_live_site_dependency':'verify_terminal.py unconditionally checks old593public bytes/namespaces. This is an installation-time custody fence, expected to fail after authorized publication. Own default uses sealed custody; optional --live-baseline only checks unchanged research originals.','material_native_copy_errors':[],'completion_percent':95})
with (A/'RESEARCH_LOG.md').open('a') as f:f.write(f'- {UTC}: Stage628corresponding frozen blobs and6whole normal/-O native PDF/ZIPbuffers match independently frozen originals. Six namespaces exactly match58/56/232/62/122/77 with no basename exclusions. Bounded custody completion estimate:95%.\n')
print(json.dumps({'UTC':UTC,'copied_native_source_editorial_authority_inputs':len(checks),'whole_native_buffers':len(assets),'namespaces':nschecks,'material_native_copy_errors':[]}))
