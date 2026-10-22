#!/usr/bin/env python3
"""Verify safe audit and exact frozen author input; no network or external writes."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, subprocess, sys, tempfile, zipfile
import independent_controls, reconstruct_author_scope

ROOT=Path(__file__).resolve().parent

def digest(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(ok, label):
    if not ok: raise ValueError(label)
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('author_zip',type=Path)
    args=parser.parse_args()
    binding=json.loads((ROOT/'BINDING.json').read_text())
    require(digest(args.author_zip)=={k:binding['author_zip'][k] for k in ('bytes','sha256')},'Author ZIP binding mismatch')
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    actual={p.name for p in ROOT.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
    require(actual=={r['path'] for r in manifest['files']},'Unexpected/missing audit file')
    for row in manifest['files']:
        require(digest(ROOT/row['path'])=={k:row[k] for k in ('bytes','sha256')},'Audit digest mismatch: '+row['path'])
    with tempfile.TemporaryDirectory(prefix='coding-audit-') as temp:
        temp=Path(temp)
        with zipfile.ZipFile(args.author_zip) as z:
            names=z.namelist()
            require(len(names)==binding['zip_entries'] and len(names)==len(set(names)),'Invalid ZIP entry count')
            for info in z.infolist():
                p=PurePosixPath(info.filename)
                require(not p.is_absolute() and '..' not in p.parts and len(p.parts)==2 and p.parts[0]=='coding_efficiency_30005026','Unsafe ZIP path')
                require(((info.external_attr>>16)&0o170000)!=0o120000,'Symlink forbidden')
            z.extractall(temp)
        author=temp/'coding_efficiency_30005026'
        require(digest(author/'AUTHOR_MANIFEST.json')==binding['author_manifest'],'Author manifest binding mismatch')
        am=json.loads((author/'AUTHOR_MANIFEST.json').read_text())
        require(len(am['files'])==binding['manifest_entries_verified'],'Author manifest count mismatch')
        for row in am['files']:
            require(digest(author/row['path'])=={k:row[k] for k in ('bytes','sha256')},'Author digest mismatch: '+row['path'])
        result=json.loads(subprocess.check_output([sys.executable,'-B',str(author/'verify.py')],cwd=temp,text=True,timeout=60))
        require(result==json.loads((ROOT/'AUTHOR_REPLAY.json').read_text()),'Author replay changed')
    rebuilt=reconstruct_author_scope.run()
    independent=independent_controls.run()
    require(rebuilt==json.loads((ROOT/'RECONSTRUCTED_RESULTS.json').read_text()),'Reconstruction changed')
    require(independent==json.loads((ROOT/'INDEPENDENT_RESULTS.json').read_text()),'Independent controls changed')
    print(json.dumps({'status':'PASS','author_manifest_files':10,'audit_manifest_files':len(manifest['files']),
        'author_assertions':result['assertions'],'independently_reconstructed_assertions':rebuilt['assertions'],
        'additional_independent_assertions':independent['assertions'],
        'author_input_unchanged':True,'original_target':'UNRESOLVED','approaches_used':'5/5'},indent=2,sort_keys=True))
if __name__=='__main__': main()
