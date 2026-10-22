#!/usr/bin/env python3
"""Read-only closure verifier; no project execution, network, tokens or subprocess."""
import hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def strict_load(path):
    def pairs(entries):
        out={}
        for k,v in entries:
            require(k not in out,'Duplicate JSON key');out[k]=v
        return out
    return json.loads(path.read_bytes(),object_pairs_hook=pairs)
manifest=strict_load(HERE/'MANIFEST.json')
actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and not p.is_symlink() and p.name not in {'MANIFEST.json','MANIFEST.sha256'} and '__pycache__' not in p.parts}
require(actual=={e['path'] for e in manifest['files']},'Manifest is not an exact retained-file inventory')
for e in manifest['files']:
    p=HERE/e['path'];b=p.read_bytes();require(not p.is_symlink() and len(b)==e['bytes'] and sha(b)==e['sha256'],'Manifest mismatch: '+e['path'])
source=strict_load(HERE/'SOURCE_PINS.json')
for e in source['files']:
    p=HERE/e['snapshot'];b=p.read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'Private source pin mismatch')
    require(Path(e['original']).read_bytes()==b,'Original source pin changed: '+e['original'])
expected=[f'finite_idempotent_after_new_unknown_{n}_column_{c}' for n in range(5) for c in range(4)]
mode_names=['RESULTS_NORMAL.json','RESULTS_OPTIMIZED.json','RESULTS_DOCSTRINGS_REMOVED.json'];orders=[]
for mode,name in enumerate(mode_names):
    value=strict_load(HERE/name);rs=value['results'];orders.append([r['case'] for r in rs])
    require(value['mode']==mode and value['case_count']==651 and value['full_main_executions']==651 and len(rs)==651,'Wrong mode/count')
    require(value['originals_unchanged'] and value['offline_only'] and not value['denied_real_service_attempts'] and value['retained_case_trees']==0,'Offline/custody condition failed')
    require([r['case'] for r in rs if not r['passed']]==expected,'Unreconciled guard result')
    for r in rs:
        require(not r['unexpected_service_paths'],'Unexpected service path')
        require(not r['error'] or '[Errno 28]' not in r['error'],'Infrastructure failure cannot certify rejection')
        if not r['passed']:require(r['error'] is None and r['state']['append']==0 and r['receipt_saved'] and r['simulated_ledger_rows']==183,'Finding evidence differs')
    critical=strict_load(HERE/f'CRITICAL_MODE_{mode}.json');require(critical['mode']==mode and not critical['network_and_process_attempts'],'Critical mode/offline mismatch')
    require(critical['independent_HTMLParser_href']==['https://doi.org/10.5281/zenodo.23350364'],'HTML identity demonstration mismatch')
    cr=critical['results'];require(len(cr)==4 and all(r['state']['append']==0 for r in cr),'Critical mock append occurred')
    require(cr[0]['passed'] and cr[0]['simulated_ledger_rows']==182 and cr[3]['passed'] and cr[3]['error'] is not None,'Critical negative/positive control failed')
    for r in cr[1:3]:
        receipt=r['verification_receipt'];require(r['error'] is None and receipt['status']=='verified' and receipt['read_back_exact'] is True and receipt['unique_target_and_DOI'] is True and receipt['ledger_rows_before']==182 and receipt['ledger_rows_after']==183 and receipt['new_row'] is False,'False receipt reproduction differs')
require(orders[0]==orders[1]==orders[2] and len(set(orders[0]))==651,'Mode case order mismatch')
replay=strict_load(HERE/'CONTEXT_REPLAY.json');require(all(e['byte_identical'] for e in replay['checks']),'Context replay mismatch')
require(not (HERE.parent/'ROOT_EXACT_INSTANCE_ACCEPTANCE.json').exists(),'Unexpected v1 root acceptance exists')
print(json.dumps({'verified':True,'verdict':'changes_required','helper_sha256':manifest['helper_sha256'],'primary_executions':1953,'all_full_main_executions':1970,'unexpected_verified_receipts_primary':60,'unresolved_material_findings':1,'originals_unchanged':True,'offline_only':True,'manifest_sha256':sha((HERE/'MANIFEST.json').read_bytes())},indent=2))
