#!/usr/bin/env python3
"""Fail-closed verification of the exact public file set and canonical manifest."""
import argparse
import hashlib
import json
import re
import stat
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parent

def require(ok,message):
    if not ok: raise RuntimeError(message)

def no_duplicate_keys(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'Duplicate JSON key: '+key)
        result[key]=value
    return result

def verify(expected=None):
    entries=list(ROOT.rglob('*'))
    require(all(not p.is_symlink() for p in entries),'Symlink in public payload')
    require(all(stat.S_ISREG(p.lstat().st_mode) or stat.S_ISDIR(p.lstat().st_mode) for p in entries),'Nonregular object in public payload')
    raw=(ROOT/'MANIFEST.json').read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if expected is not None: require(digest==expected,'External manifest pin mismatch')
    manifest=json.loads(raw,object_pairs_hook=no_duplicate_keys)
    require(raw==(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode(),'Noncanonical manifest encoding')
    require(manifest.get('schema')=='handlebody-public-manifest-v1','Wrong manifest schema')
    rows=manifest['files'];require(isinstance(rows,list),'Files must be a list')
    paths=[]
    for row in rows:
        require(set(row)=={'path','bytes','sha256'},'Unexpected file-entry fields')
        rel=row['path'];require(isinstance(rel,str),'Nonstring path')
        parts=PurePosixPath(rel)
        require(not parts.is_absolute() and '..' not in parts.parts and str(parts)==rel and '\\' not in rel and rel not in ('','.','MANIFEST.json'),'Unsafe or self-referential path')
        require(type(row['bytes']) is int and row['bytes']>=0,'Invalid byte count')
        require(isinstance(row['sha256'],str) and re.fullmatch('[0-9a-f]{64}',row['sha256']),'Invalid hash')
        p=ROOT/rel
        require(p.is_file() and not p.is_symlink(),'Missing file or symlink: '+rel)
        data=p.read_bytes()
        require(len(data)==row['bytes'],'Wrong byte count: '+rel)
        require(hashlib.sha256(data).hexdigest()==row['sha256'],'Wrong hash: '+rel)
        paths.append(rel)
    require(paths==sorted(set(paths)),'Unsorted or duplicate manifest paths')
    actual={p.relative_to(ROOT).as_posix() for p in entries if p.is_file()}
    allowed_dirs={str(parent) for rel in paths for parent in PurePosixPath(rel).parents if str(parent)!='.'}
    actual_dirs={p.relative_to(ROOT).as_posix() for p in entries if p.is_dir()}
    require(actual_dirs==allowed_dirs,'Unexpected or missing payload directory')
    require(actual==set(paths)|{'MANIFEST.json'},'Unexpected or unlisted payload files')
    identities=json.loads((ROOT/'ORIGINAL_IDENTITIES.json').read_bytes(),object_pairs_hook=no_duplicate_keys)
    require(identities['schema']=='handlebody-original-public-identities-v1','Wrong original-identity schema')
    bypath={row['path']:row for row in identities['files']}
    require(len(bypath)==len(identities['files']),'Duplicate original identity path')
    for rel,row in bypath.items():
        require(rel in paths,'Original identity not in payload')
        data=(ROOT/rel).read_bytes()
        require(type(row['original_bytes']) is int and row['original_bytes']>0,'Invalid original size')
        require(re.fullmatch('[0-9a-f]{64}',row['original_sha256']) is not None,'Invalid original hash')
        require(len(data)==row['public_bytes'] and hashlib.sha256(data).hexdigest()==row['public_sha256'],'Public identity mismatch: '+rel)
    anchor_pins={
        'pass1_audit/AUDIT.md': (18063,'515f62b1113721b44bbf9a10214ad27fe70f92dc7ec221c2afa6a2526d6e7539'),
        'pass1_audit/MANIFEST.json': (3371,'94ec2598c7056dc95690f8d5863195e57abafc12b9dca346160f133f9001c3c5'),
        'pass1_genus_two/GENUS_TWO_GENERATORS.md': (11497,'155447c1da5d4d607e6e4dd26974c8c39048961b52187a9705aaae7af7bc2870'),
        'pass1_johnson_obstruction/PROOF.md': (12792,'650aaf736c5a621ca98ed985e7d7ceb0c8cfd84362c5c81fa7e9500ddb71799e'),
        'pass1_constructive/CONSTRUCTIVE_JOHNSON_GENERATORS.md': (16380,'8f81a0877e3775bcebde93b97c5950b7926f4d861a1fa39c0c0f1f180c3f5a5f'),
        'pass1_closed_transfer/SOURCE_ACCEPTANCE_REPORT.md': (19315,'a0f3a91809990384976c1a13a07f50e487ff04d89204e2cb641592c2b38d707f'),
        'pass1_exact_validation/AUDIT.md': (18594,'8e12cec618e4a38d65d42ea551d5fe564ecbffdfe0d5bd0b2956d4ee9e3c604c'),
        'pass1_exact_validation/verify_exact_formulas.py': (12081,'ed2bb84f65f073aff3a591620245dc7ee4a0187a5816f621c3a80b980302151e')}
    for rel,(size,pin) in anchor_pins.items():
        require(bypath[rel]['original_bytes']==size and bypath[rel]['original_sha256']==pin,'Original acceptance anchor differs: '+rel)
    bindings=json.loads((ROOT/'AUDIT_BINDINGS.json').read_bytes(),object_pairs_hook=no_duplicate_keys)
    require(bindings['schema']=='handlebody-audit-bindings-v1' and bindings['status']=='PASS','Acceptance bindings missing')
    require({b['path'] for b in bindings['bindings']}==set(bypath),'Original binding coverage differs')
    for binding in bindings['bindings']:
        row=bypath[binding['path']]
        require(binding['audited_original']=={'bytes':row['original_bytes'],'sha256':row['original_sha256']},'Audit original binding differs')
        require(binding['public_copy']=={'bytes':row['public_bytes'],'sha256':row['public_sha256']},'Audit public binding differs')
    for key,rel in [('original_final_audit','pass1_audit/AUDIT.md'),('original_final_audit_manifest','pass1_audit/MANIFEST.json')]:
        row=bypath[rel];require(bindings[key]=={'path':rel,'bytes':row['original_bytes'],'sha256':row['original_sha256']},'Final anchor field differs')
    def check_original(rel,pin):
        row=bypath[rel]
        require(row['original_bytes']==pin['bytes'] and row['original_sha256']==pin['sha256'],'Original acceptance pin differs: '+rel)
    final=json.loads((ROOT/'pass1_audit/MANIFEST.json').read_bytes(),object_pairs_hook=no_duplicate_keys)
    require(final['status']=='FINAL_PASS' and final['reviewed_hashes_match'] is True,'Combined audit incomplete')
    for key in ['reviewed_inputs','audit_artifacts']:
        for pin in final[key]:check_original(pin['path'],pin)
    for prefix in ['pass1_exact_validation','pass1_closed_transfer','pass1_genus_two','pass1_johnson_obstruction']:
        item=json.loads((ROOT/prefix/'MANIFEST.json').read_bytes(),object_pairs_hook=no_duplicate_keys)
        groups=[item] if isinstance(item,list) else [item.get(k,[]) for k in ['reviewed_inputs','artifacts','files']]
        for group in groups:
            for pin in group:
                rel=pin.get('path',pin.get('name'));rel=rel if rel.startswith('pass1_') else prefix+'/'+rel
                check_original(rel,pin)
    for pin in json.loads((ROOT/'pass1_constructive/RESULT.json').read_bytes())['artifacts']:check_original('pass1_constructive/'+pin['path'],pin)
    acceptance=json.loads((ROOT/'pass1_audit/RESULT.json').read_bytes(),object_pairs_hook=no_duplicate_keys)
    require(acceptance['status']=='PASS' and acceptance['unresolved_mathematical_objections']==[],'Final acceptance absent')
    require({(r['branch'],r['genus'],r['verdict']) for r in acceptance['coverage']}=={('HI','g=2','PASS'),('HK','g=2','PASS'),('HI','g>=3','PASS'),('HK','g>=3','PASS')},'Acceptance coverage changed')
    require(acceptance['normal_ambient_groups']=={'HI_normal_seed':'H_g','HK_optional_normal_family':'HI_g'},'Normal ambient groups changed')
    require(acceptance['novelty_certified'] is False and acceptance['finite_generation_claimed'] is False,'Scope guard changed')
    exact=json.loads((ROOT/'pass1_exact_validation/MANIFEST.json').read_bytes())
    require(exact['status']=='PASS' and exact['exact_checks']==62840 and exact['optimized_output_identical'] is True,'Independent exact acceptance differs')
    closed=json.loads((ROOT/'pass1_closed_transfer/RESULT.json').read_bytes())
    require(closed['verdict']=='PASS' and closed['inspected_constructive_note_sha256']==anchor_pins['pass1_constructive/CONSTRUCTIVE_JOHNSON_GENERATORS.md'][1],'Closed-transfer acceptance differs')
    historical=[(ROOT/p).read_bytes() for p in ['pass1_exact_validation/EXACT_CHECKS.json','pass1_exact_validation/EXACT_CHECKS_OPTIMIZED.json','ROOT_EXACT_CHECKS.json']]
    require(historical[0]==historical[1]==historical[2],'Historical independent/root receipts differ')
    return {'status':'PASS','payload_file_count':len(paths)+1,'all_hashes_and_sizes_match':True,'exact_file_set':True,'canonical_manifest':True,'acceptance_and_original_public_bindings':True,'external_pin_checked':expected is not None,'manifest_sha256':digest}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--manifest-sha256')
    args=parser.parse_args();print(json.dumps(verify(args.manifest_sha256),sort_keys=True))
if __name__=='__main__':main()
