#!/usr/bin/env python3
"""Read-only native custody and scope closure. No network or scientific reruns.

Preserves the literal source-native schema, including uppercase SHA256 fields.
Hashes and replay bindings verify evidence identity, not formal mathematical truth.
"""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat,sys
R=Path(__file__).resolve().parent;B=R.parents[1];S=B/'sources';checks=0
def require(p,m):
    global checks
    checks+=1
    if not p:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
ready=obj(S/'SOURCE_READY.json');oldseal=obj(S/'SOURCE_READY_SEAL.json')
require(sha(S/'SOURCE_READY.json')==oldseal['SOURCE_READY_SHA256']=='1f728d52dd3bb791833a837fb3bae7eab1b3a37ce7ecd9c4655b94f4d693cf46','literal source-ready pin')
require(sha(S/'SOURCE_READY_MANIFEST.json')==oldseal['manifest_SHA256'],'source-ready manifest seal')
for f in obj(S/'SOURCE_READY_MANIFEST.json')['files']:
    p=S/f['path'];require(p.stat().st_size==f['bytes'] and sha(p)==f['SHA256'],'original source manifest '+f['path'])
raw=obj(Path(ready['native_record_body_path']))
require(raw['id']==ready['record_id']==23430498 and raw['metadata']['version']==ready['version']=='1.0','exact native record/version')
require(raw['metadata']['publication_date']==ready['publication_date_declared']=='2026-10-13','declared date retained')
require(raw['created']==ready['record_created'] and raw['updated']==ready['record_updated'],'created/updated retained separately')
require(obj(S/'latest.raw.json')['id']==23430498,'exact native latest record')
versions=obj(S/'versions.page-001.raw.json')['hits'];total=versions['total']
require((total.get('value') if isinstance(total,dict) else total)==ready['all_native_versions_total']==1,'native complete versions count')
require(len(raw['files'])==len(ready['all_native_assets_in_original_order'])==2,'all native files')
for native,a in zip(raw['files'],ready['all_native_assets_in_original_order']):
    p=Path(a['path']);z=p.read_bytes()
    require(native==a['original_api_file_object'],'complete native file object/order')
    require(len(z)==native['size']==a['bytes'],'native full byte count')
    require('md5:'+hashlib.md5(z).hexdigest()==native['checksum'] and hashlib.md5(z).hexdigest()==a['MD5'],'native MD5')
    require(hashlib.sha256(z).hexdigest()==a['SHA256'],'native full SHA256')
require(sha(Path(ready['selected_actual_PDF']['path']))==ready['selected_actual_PDF']['SHA256'] and ready['selected_actual_PDF']['pages']==13,'literal actual PDF path')
require(sha(Path(ready['controlling_TeX']['path']))==ready['controlling_TeX']['SHA256'] and len(Path(ready['controlling_TeX']['path']).read_text().splitlines())==865,'literal controlling TeX')
ledger=obj(S/'archive-custody.json');members=ledger['regular_members'];require(len(members)==194,'all194 original archive occurrences')
require(len(ledger['containers'])==1 and not ledger['nested_archives'],'exact archive container scope')
with zipfile.ZipFile(ledger['containers'][0]['source_path']) as z:
    infos=z.infolist();require(len(infos)==194,'complete native ZIP directory')
    seen=set()
    for m in members:
        a=infos[m['entry_ordinal']-1];path=PurePosixPath(a.filename);canonical='/'.join(path.parts)
        require(a.filename==m['original_member_name'] and not path.is_absolute() and '..' not in path.parts and '\\' not in a.filename and canonical not in seen,'safe unique literal ZIP path')
        seen.add(canonical)
        require(not(a.flag_bits&1) and stat.S_IFMT(a.external_attr>>16) in (0,stat.S_IFREG),'regular unencrypted ZIP payload')
        body=z.read(a)
        require(len(body)==m['bytes']==m['declared_uncompressed_bytes'] and f'{a.CRC:08x}'==m['CRC32'] and hashlib.sha256(body).hexdigest()==m['SHA256'],'whole original CRC/hash payload')
        require(sha(Path(m['extracted_path']))==m['SHA256'],'exact extracted original payload')

for name in ['INPUT_MANIFEST.json','OWNED_MANIFEST.json']:
    for f in obj(R/name)['files']:
        p=Path(f['path']) if name.startswith('INPUT') else R/f['path']
        require(p.is_file() and p.stat().st_size==f['bytes'] and sha(p)==f['sha256'],name+': '+f['path'])
ex={'OWNED_MANIFEST.json','verification_output.json','SEAL.json'}
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and str(p.relative_to(R)) not in ex}
require(actual=={f['path'] for f in obj(R/'OWNED_MANIFEST.json')['files']},'all owned evidence inventoried')
initial=obj(R/'INITIAL_SEAL.json')
require(sha(R/'INITIAL_RECONSTRUCTION.md')==initial['reconstruction_sha256']=='76e9e91076301b028c864b653d2dbfc4b429d135d0866e4299e08dba4a35c73d','independent initial seal')
require(initial['full_actual_pdf_pages']==initial['full_fresh_rasters_personally_viewed']==13 and not initial['foreign_primary_bodies_read'] and not initial['support_programs_or_results_read'],'initial reading/exposure receipt')
require(len(list((R/'visual').glob('page-*.png')))==13,'all13actual rasters retained')
replays=obj(R/'NATIVE_REPLAY_RECEIPTS.json');require(len(replays)==6,'three native checkers in two modes')
outputs={}
for e in replays:
    require(sha(Path(e['source_path']))==sha(Path(e['exact_copy_path']))==e['source_sha256'] and e['exit_code']==0,'unmodified source/isolated copy/exit '+e['tag'])
    outputs[e['tag'],e['mode']]=obj(Path(e['stdout_path']))
    require(not Path(e['stderr_path']).read_text(),'no native replay stderr')
for tag in ['degree-two','wheel','symbolic']:
    a=outputs[tag,'normal'].copy();b=outputs[tag,'optimized'].copy();a.pop('utc',None);b.pop('utc',None)
    require(a==b,'complete replay objects equal excluding recorded time '+tag)
require(outputs['degree-two','normal']['status']=='PASS' and outputs['degree-two','normal']['determinants']['six_rows']==-48,'degree-two replay scope')
require(outputs['wheel','normal']['all_checks_pass'] and outputs['wheel','normal']['direct_16_by_16_adjoint_value']==6,'wheel replay scope')
require(outputs['symbolic','normal']['passed'] and outputs['symbolic','normal']['all_unknowns_symbolic']==['r','s','t','u','v'],'symbolic replay scope')
ind=obj(R/'independent-normal.json')
require(ind==obj(R/'independent-optimized.json') and ind['status']=='PASS','independent whole result equality')
require(ind['lie_action_components_verified']==3 and ind['symbolic_determinants']==[-48,2,-16,-24] and ind['adjoint_trace']==6 and ind['reversed_trace']==-6 and ind['Alexander_Conway_values']=={'2,3':1,'3,4':5},'independent exact result scope')
for e in obj(R/'INDEPENDENT_EXECUTION_RECEIPTS.json'):
    require(e['exit_code']==0 and sha(R/'independent_algebra.py')==e['program_sha256'],'independent program/exit binding')
v=obj(R/'VERDICT.json');require(not v['current_sibling_scientific_findings_read'] and not v['scientific_findings_sent_before_root_gate'] and v['completion_estimate_percent']==100,'literal verdict and exposure')
sealed='--unsealed-preflight' not in sys.argv
if sealed:
    seal=obj(R/'SEAL.json')
    for name,key in [('INPUT_MANIFEST.json','input_manifest_sha256'),('OWNED_MANIFEST.json','owned_manifest_sha256'),('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('verify_read_only.py','read_only_verifier_sha256'),('verification_output.json','verification_output_sha256')]:
        require(sha(R/name)==seal[key],'final seal '+name)
    require(seal['source_ready_sha256']==sha(S/'SOURCE_READY.json') and seal['completion_estimate_percent']==100,'final input/completion seal')
print(json.dumps({'status':'PASS','record_id':23430498,'mode':'sealed' if sealed else 'unsealed preflight','closure_checks':checks,'native_regular_payloads':194,'actual_pdf_pages':13,'all_original_bytes_unchanged':True,'read_only':True,'limitation':'Evidence identity and recorded checks; not formal proof certification.'},indent=2))
