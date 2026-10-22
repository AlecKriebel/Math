#!/usr/bin/env python3
"""Actual independent corrupted copies; this is an integrity diagnostic only."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parent
pin=hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()
cases=['missing','extra_file','extra_dir','symlink','proof','audit','patch','archive','checker','repin_fixed_anchor','duplicate_key','unsafe_path','boolean_schema','float_schema','boolean_bytes','negative_bytes','bad_hash','wrong_external_pin']
positive=negative=0
with tempfile.TemporaryDirectory(prefix='knot-publication-mutations-') as td:
    for optimized in (False,True):
        for case in ['baseline']+cases:
            dst=pathlib.Path(td)/str(optimized)/case;shutil.copytree(root,dst);chosen=pin
            m=json.loads((dst/'MANIFEST.json').read_text())
            if case=='missing':(dst/'accepted/PROOF.md').unlink()
            elif case=='extra_file':(dst/'extra').write_text('extra')
            elif case=='extra_dir':(dst/'empty').mkdir()
            elif case=='symlink':(dst/'accepted/PROOF.md').unlink();(dst/'accepted/PROOF.md').symlink_to(root/'accepted/PROOF.md')
            elif case in ['proof','audit','patch','archive','checker']:
                name={'proof':'accepted/PROOF.md','audit':'independent_audit/AUDIT.md','patch':'independent_audit/CORRECTIONS.patch','archive':'AUTHOR_FREEZE.zip','checker':'accepted/verify_packet.py'}[case];f=dst/name;f.write_bytes(f.read_bytes()+b'\nmutation\n')
            elif case=='wrong_external_pin':chosen='0'*64
            elif case!='baseline':
                if case=='repin_fixed_anchor':
                    n='authored/MANIFEST.json';b=(dst/n).read_bytes()+b' ';(dst/n).write_bytes(b);m['files'][n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
                elif case=='unsafe_path':m['files']['../escape']=m['files']['README.md']
                elif case=='boolean_schema':m['schema']=True
                elif case=='float_schema':m['schema']=1.0
                elif case=='boolean_bytes':m['files']['README.md']['bytes']=True
                elif case=='negative_bytes':m['files']['README.md']['bytes']=-1
                elif case=='bad_hash':m['files']['README.md']['sha256']='x'*64
                raw=json.dumps(m)
                if case=='duplicate_key':raw=raw[:-1]+',"schema":1}'
                (dst/'MANIFEST.json').write_text(raw);chosen=hashlib.sha256(raw.encode()).hexdigest()
            command=[sys.executable,'-I','-S','-B']+(['-O'] if optimized else [])+[str(dst/'verify_publication.py'),'--manifest-sha256',chosen]
            r=subprocess.run(command,cwd=td,capture_output=True,timeout=240)
            if (r.returncode==0)!=(case=='baseline'):raise RuntimeError(str((optimized,case,r.stdout,r.stderr)))
            if case=='baseline':positive+=1
            else:negative+=1
print(json.dumps({'positive_runs':positive,'rejected_runs':negative,'cases':cases,'scope':'Actual publication-corruption diagnostics, normal and optimized.'},sort_keys=True))
