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
    require(manifest.get('schema')=='subcategory-tqft-public-manifest-v1','Wrong manifest schema')
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
    identities=json.loads((ROOT/'ORIGINAL_IDENTITIES.json').read_bytes(),object_pairs_hook=no_duplicate_keys)['files']
    bypath={row['path']:row for row in identities}
    require(len(bypath)==len(identities),'Duplicate original identity path')
    for rel,row in bypath.items():
        require(rel in paths,'Original identity not in payload')
        data=(ROOT/rel).read_bytes()
        require(len(data)==row['public_bytes'] and hashlib.sha256(data).hexdigest()==row['public_sha256'],'Public identity mismatch: '+rel)
    bindings=json.loads((ROOT/'AUDIT_BINDINGS.json').read_bytes(),object_pairs_hook=no_duplicate_keys)
    require(bindings['status']=='PASS','Acceptance bindings missing')
    require(hashlib.sha256((ROOT/'pass1_audit/MANIFEST.json').read_bytes()).hexdigest()=='ae7d65b3fda8741dc740e177b97af2a4d1edd6fab7f341cffcaba22b8433c4ad','Final mathematical audit pin differs')
    require(bypath['pass1_scope/SOURCE_SCOPE_ACCEPTANCE.md']['original_sha256']=='ef7b9d186ae4a0f526ae1fadc1a39547d5fdf5b918a467cc1a919847070cef41','Final source-scope original pin differs')
    for binding in bindings['bindings']:
        row=bypath[binding['path']]
        require(binding['audited_original']=={'bytes':row['original_bytes'],'sha256':row['original_sha256']},'Audit original binding differs')
        require(binding['public_copy']=={'bytes':row['public_bytes'],'sha256':row['public_sha256']},'Audit public binding differs')
    def check_original(rel,pin):
        row=bypath[rel]
        require(row['original_bytes']==pin['bytes'] and row['original_sha256']==pin['sha256'],'Original acceptance pin differs: '+rel)
    for pin in json.loads((ROOT/'pass1_audit/MANIFEST.json').read_bytes())['files']:
        check_original('pass1_audit/'+pin['path'],pin)
    checked=json.loads((ROOT/'pass1_audit/CHECKS.json').read_bytes())
    require(checked['status']=='PASS_DECLARED_INTERFACE_RELATION' and checked['checked']['supplementary_center_report']=='PASS','Final math acceptance absent')
    for pin in checked['audited_artifacts']:check_original(pin['path'],pin)
    for pin in json.loads((ROOT/'pass1_scope/MANIFEST.json').read_bytes())['files']:
        check_original('pass1_scope/'+pin['file'],pin)
    disposition=json.loads((ROOT/'pass1_scope/DISPOSITION.json').read_bytes())
    require(disposition['source_scope_verdict']=='ACCEPT_EXISTING_RESULT_ANSWER' and disposition['source_formulation_satisfied'],'Final source acceptance absent')
    check_original('pass1_scope/SOURCE_SCOPE_ACCEPTANCE.md',disposition['report'])
    return {'status':'PASS','payload_file_count':len(paths)+1,'all_hashes_and_sizes_match':True,'exact_file_set':True,'canonical_manifest':True,'acceptance_and_original_public_bindings':True,'external_pin_checked':expected is not None,'manifest_sha256':digest}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--manifest-sha256')
    args=parser.parse_args();print(json.dumps(verify(args.manifest_sha256),sort_keys=True))
if __name__=='__main__':main()
