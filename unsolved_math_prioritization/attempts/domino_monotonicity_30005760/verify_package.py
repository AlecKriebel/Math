#!/usr/bin/env python3
"""Inventory first, content second. Trust anchor is the external manifest receipt."""
import ast,hashlib,json,os,stat
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise RuntimeError(message)

def verify(root=ROOT):
    # Only the manifest is read before exact filesystem shape/type acceptance.
    manifest_path=root/'MANIFEST.json'
    need(stat.S_ISREG(manifest_path.lstat().st_mode),'manifest is not a regular file')
    manifest=json.loads(manifest_path.read_text())
    expected=set(manifest['files'])|{'MANIFEST.json'}
    dirs={str(Path(x).parent) for x in expected if str(Path(x).parent)!='.'}
    actual=set();actual_dirs=set()
    for base,ds,fs in os.walk(root,followlinks=False):
        for name in ds+fs:
            f=Path(base)/name;rel=f.relative_to(root).as_posix();mode=f.lstat().st_mode
            need(not stat.S_ISLNK(mode),'symlink rejected: '+rel)
            need(stat.S_ISREG(mode) or stat.S_ISDIR(mode),'special entry rejected: '+rel)
            (actual_dirs if stat.S_ISDIR(mode) else actual).add(rel)
    need(actual==expected,'file inventory mismatch')
    need(actual_dirs==dirs,'directory inventory mismatch')
    for rel,m in manifest['files'].items():
        data=(root/rel).read_bytes()
        need(len(data)==m['bytes'] and hashlib.sha256(data).hexdigest()==m['sha256'],'content mismatch: '+rel)
    provenance=json.loads((root/'PROVENANCE.json').read_text())
    for rel,m in provenance['modules'].items():
        tree=ast.parse((root/rel).read_text())
        need(hashlib.sha256(ast.dump(tree,include_attributes=False).encode()).hexdigest()==m['whole_module_ast_sha256'],'whole AST mismatch: '+rel)
    receipt=json.loads((root/'domino_1890_audit/RECEIPT.json').read_text())
    need(len(receipt['reviewed_files'])==23,'reviewed scope')
    for rel,m in {**receipt['reviewed_files'],**receipt['audit_evidence_files']}.items():
        need(manifest['files'][rel]['sha256']==m['sha256'] and manifest['files'][rel]['bytes']==m['bytes'],'audit provenance: '+rel)
    need(receipt['full_conjecture']=='UNRESOLVED','status inflation')
    return {'status':'PASS_PARTIAL_ONLY','problem_id':'30005760','row':1890,'reviewed_files':23,'payload_files':len(manifest['files']),'full_conjecture':'UNRESOLVED'}
if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
