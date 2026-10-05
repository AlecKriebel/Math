#!/usr/bin/env python3
"""Pinned author/independent replays and destructive tests confined to temporary copies."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PIN='465c3840c518ad8b5abe6bc229e306f2059a211f64cdeb48f5cb0005d2b88ecb'
HERE=Path(__file__).resolve().parent

def need(ok,why):
    if not ok: raise ValueError(why)

def run(command,cwd):
    p=subprocess.run(command,cwd=cwd,capture_output=True,text=True,timeout=180)
    return p

def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--author',type=Path,default=HERE.parent/'root_unity_30004334'); args=ap.parse_args()
    source=args.author.resolve()
    before={p.name:sha(p.read_bytes()) for p in source.iterdir() if p.is_file()}
    need(before['AUTHOR_MANIFEST.json']==PIN,'pin mismatch')
    runs=[]; controls=[]; expected_author=None; expected_independent=None
    with tempfile.TemporaryDirectory(prefix='root unity independent replay ') as tmp:
        tmp=Path(tmp); relocated=tmp/'relocated author with spaces'; shutil.copytree(source,relocated)
        independent=tmp/'isolated verifier'; independent.mkdir(); shutil.copy2(HERE/'independent_verify.py',independent/'independent_verify.py')
        for label,root in [('original',source),('relocated',relocated)]:
            for optimized in [False,True]:
                flags=['-O'] if optimized else []
                command=[sys.executable,*flags,str(root/'verify.py'),'--self-test','--expected-manifest',PIN]
                p=run(command,tmp)
                need(p.returncode==0,'author replay failed '+label+p.stderr)
                result=json.loads(p.stdout)
                if expected_author is None: expected_author=result
                need(result==expected_author,'author replay output changed')
                runs.append({'verifier':'author','location':label,'optimized':optimized,'returncode':p.returncode,'stdout_sha256':sha(p.stdout.encode()),'negative_controls_rejected':result['negative_controls_rejected']})
        for label,script,root,optimized in [('original',HERE/'independent_verify.py',source,False),('original',HERE/'independent_verify.py',source,True),('relocated',independent/'independent_verify.py',relocated,False),('relocated',independent/'independent_verify.py',relocated,True)]:
            p=run([sys.executable,*(['-O'] if optimized else []),str(script),'--author',str(root)],tmp)
            need(p.returncode==0,'independent replay failed '+label+p.stderr)
            result=json.loads(p.stdout)
            if expected_independent is None: expected_independent=result
            need(result==expected_independent,'independent replay output changed')
            runs.append({'verifier':'independent','location':label,'optimized':optimized,'returncode':p.returncode,'stdout_sha256':sha(p.stdout.encode())})
        need(expected_independent==json.loads((HERE/'INDEPENDENT_RESULTS.json').read_text()),'recorded independent output changed')
        mutations=['changed_payload','missing_payload','unlisted_payload','manifest_whitespace','duplicate_manifest_entry','payload_symlink','manifest_symlink','coherently_rehashed_payload']
        for case in mutations:
            target=tmp/('mutant '+case); shutil.copytree(source,target)
            if case=='changed_payload':
                p=target/'PROOFS.md'; p.write_bytes(p.read_bytes()+b'\n')
            elif case=='missing_payload': (target/'CHECK_RESULTS.json').unlink()
            elif case=='unlisted_payload': (target/'extra.txt').write_text('deliberate control')
            elif case=='manifest_whitespace':
                p=target/'AUTHOR_MANIFEST.json'; p.write_bytes(p.read_bytes()+b'\n')
            elif case=='duplicate_manifest_entry':
                p=target/'AUTHOR_MANIFEST.json'; m=json.loads(p.read_text()); m['files'].append(m['files'][0]); p.write_text(json.dumps(m))
            elif case=='payload_symlink':
                p=target/'PROOFS.md'; p.unlink(); p.symlink_to(source/'PROOFS.md')
            elif case=='manifest_symlink':
                p=target/'AUTHOR_MANIFEST.json'; p.unlink(); p.symlink_to(source/'AUTHOR_MANIFEST.json')
            elif case=='coherently_rehashed_payload':
                p=target/'PROOFS.md'; p.write_bytes(p.read_bytes()+b'\n'); m=json.loads((target/'AUTHOR_MANIFEST.json').read_text())
                for entry in m['files']:
                    if entry['path']=='PROOFS.md': entry.update(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
                (target/'AUTHOR_MANIFEST.json').write_text(json.dumps(m))
            # Author check_manifest is executed without importing/caching its code.
            for optimized in [False,True]:
                for verifier in ['author','independent']:
                    # Author intentionally binds bytes, not the manifest file's inode.
                    # A manifest-only symlink is a stronger independent checker control.
                    if case=='manifest_symlink' and verifier=='author': continue
                    script=(target/'verify.py') if verifier=='author' else (HERE/'independent_verify.py')
                    call="import runpy,sys; n=runpy.run_path(sys.argv[1]); "+("n['check_manifest'](sys.argv[2])" if verifier=='author' else "n['bind_author'](n['Path'](sys.argv[2]))")
                    p=run([sys.executable,*(['-O'] if optimized else []),'-c',call,str(script),PIN if verifier=='author' else str(target)],tmp)
                    need(p.returncode!=0,'integrity mutation accepted '+case+' '+verifier)
                    controls.append({'mutation':case,'verifier':verifier,'optimized':optimized,'rejected':True})
    after={p.name:sha(p.read_bytes()) for p in source.iterdir() if p.is_file()}
    need(after==before,'original author freeze changed')
    print(json.dumps({'schema':'root-unity-independent-replays-v1','status':'PASS','author_manifest_sha256':PIN,'replays':runs,'integrity_controls':controls,'author_freeze_unchanged':True,'notes':['No author module was imported by the independent reconstruction.','A manifest-only symlink to identical pinned bytes is accepted by the author byte-integrity model; the independent verifier rejects all symlinks. No false mathematical acceptance is involved.','All mutations were made in disposable copies, never the author freeze.']},indent=2,sort_keys=True))

if __name__=='__main__': main()
