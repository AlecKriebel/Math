#!/usr/bin/env python3
"""Independent current/historical entry verification; changed paths reconstructed explicitly."""
from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parents[2];S=A/'final_robustness_repair_20261021';P=A.parents[1]/'private/pr0280_package06';O=Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def matches(p,e):return p.is_file() and not p.is_symlink() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256']
def ck(v,m):
    if not v:raise RuntimeError(m)
def main():
    result=[]
    old=json.loads((A/'reviews/package_adversary_05/HISTORICAL_AND_NESTED_SEALS.json').read_text())
    old += [{'manifest':'reviews/package_adversary_05/AUTHORED_FILE_MANIFEST.json','entry_base':'reviews/package_adversary_05','entries':33,'sha256':sha(A/'reviews/package_adversary_05/AUTHORED_FILE_MANIFEST.json')},
       {'manifest':'ops_record_url_repair_20261021/MANIFEST.json','entry_base':'.','entries':390,'sha256':'b12e7262026d780029a7eeee1fb8d0c8a514c4a2ab382faadebad40a84dba55d'},
       {'manifest':'ops_bibliographic_context_repair_20261021/PROPOSAL_MANIFEST.json','entry_base':'.','entries':451,'sha256':'9fe9a074277ca7ff4de522cc079647b3c3fdaa812848e902afa44af30fb499b3'},
       {'manifest':'final_robustness_repair_20261021/MANIFEST.json','entry_base':'.','entries':368,'sha256':'b1d1b426b75c131dd5161c95de0532ad1cf6132294921a42f66f48dd301a8253'}]
    for item in old:
        if 'nested_zip_manifest' in item:
            manifest=P/'archive/birational-cycle-verification'/item['nested_zip_manifest'];base=manifest.parent
        else:manifest=A/item['manifest'];base=A/item['entry_base']
        ck(sha(manifest)==item['sha256'],'Historical manifest hash changed '+str(manifest));data=json.loads(manifest.read_text());entries=data['files'];ck(len(entries)==item['entries'],'count changed')
        subs=[]
        for e in entries:
            exact=base/e['path']
            if matches(exact,e):continue
            candidates=[S/'before'/e['path'],A/'ops_bibliographic_context_repair_20261021/pre_bibliographic_binding'/e['path'],A/'preprint/prior_review_01_full'/e['path'],A/'ops_record_url_repair_20261021/pre_record_url_binding'/e['path'],A/'ops_doi_identity_repair_20261021/pre_review03_binding'/e['path']]
            if e['path'].startswith('preprint/publication/'):
                candidates.append(A/'preprint/release_history/release02_pre_all_odd_prime_robustness_20261021'/Path(e['path']).name)
            hit=next((p for p in candidates if matches(p,e)),None)
            ck(hit is not None,'Unreconstructable history '+str(manifest)+' '+e['path'])
            subs.append({'original_path':str(exact.relative_to(A)),'preserved_body':str(hit.relative_to(A)),'sha256':e['sha256']})
        result.append({'manifest':str(manifest.relative_to(A)) if manifest.is_relative_to(A) else str(manifest.relative_to(P)),'sha256':sha(manifest),'entries_verified':len(entries),'changed_current_paths_reconstructed':subs})
    current=json.loads((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_text());prior=json.loads((A/'publication_clearance_history/lead01_pre_scope_extension.json').read_text())
    ck(sha(A/'publication_clearance_history/lead01_pre_scope_extension.json')=='4db5e01602ed978612c58aaa1736cd894a8b4123f7de7c6d51e14a344546febb','old lead body')
    ck(all(current[k]==prior[k] for k in ['account_leads','ledger_leads','unrelated_local_state_exemptions','unresolved_leads']),'semantic exemption changed')
    ck((A/'ROOT_PUBLICATION_CLEARANCE.json').read_bytes()==(S/'before/ROOT_PUBLICATION_CLEARANCE.json').read_bytes(),'false root decision changed')
    (O/'HISTORICAL_BINDINGS.json').write_text(json.dumps({'all_verified':True,'manifests':result,'root_lead_semantics_unchanged':True,'root_clearance_unchanged_false':True},indent=2)+'\n')
    print(json.dumps({'manifests':len(result),'all_entries_verified':sum(x['entries_verified'] for x in result),'root_semantics_preserved':True}))
if __name__=='__main__':main()
