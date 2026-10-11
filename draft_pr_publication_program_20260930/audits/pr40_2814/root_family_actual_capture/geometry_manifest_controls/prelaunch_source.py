#!/usr/bin/env python3
"""Private family-local malformed closure fixtures; all removed before sealing."""
from pathlib import Path
import hashlib, json, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parent
def pin(p, root):
    data=p.read_bytes()
    return {'path':p.relative_to(root).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def main():
    cases=[]
    for name in ['valid','extra_authored','tampered_authored','missing_authored','duplicate_manifest_row','extra_empty_directory','foreign_tamper','foreign_extra','foreign_symlink','nested_primary_hole','duplicate_json_key','arbitrary_foreign_prefix']:
        with tempfile.TemporaryDirectory(prefix='.private_closure_control_',dir=ROOT) as tmp:
            root=Path(tmp)
            (root/'primary').mkdir()
            (root/'primary'/'source.txt').write_text('foreign fixture\n')
            (root/'note.md').write_text('authored fixture\n')
            (root/'data.json').write_text('{"valid":true}\n')
            foreign={'foreign_prefix':'primary/','members':[pin(root/'primary'/'source.txt',root)],'directories':['primary']}
            (root/'FOREIGN_PRIMARY_INVENTORY.json').write_text(json.dumps(foreign))
            members=[pin(p,root) for p in sorted(root.iterdir()) if p.is_file()]
            manifest={'schema':'pr40-geodesic-authored-family/v1','root_name':root.name,
                      'self_excluded_paths':['ARTIFACT_MANIFEST.json'],'foreign_excluded_prefixes':['primary/'],
                      'bytecode_excluded_components':[],'foreign_inventory_path':'FOREIGN_PRIMARY_INVENTORY.json','directories':[],'members':members}
            if name=='extra_authored': (root/'unexpected.txt').write_text('extra')
            if name=='tampered_authored': (root/'note.md').write_text('changed')
            if name=='missing_authored': (root/'note.md').unlink()
            if name=='duplicate_manifest_row': manifest['members'].append(manifest['members'][0])
            if name=='extra_empty_directory': (root/'empty').mkdir()
            if name=='foreign_tamper': (root/'primary'/'source.txt').write_text('changed')
            if name=='foreign_extra': (root/'primary'/'extra.txt').write_text('extra')
            if name=='foreign_symlink': (root/'primary'/'link').symlink_to(root/'note.md')
            if name=='nested_primary_hole':
                (root/'notforeign').mkdir(); (root/'notforeign'/'primary').mkdir(); (root/'notforeign'/'primary'/'extra.txt').write_text('extra')
            if name=='duplicate_json_key':
                (root/'data.json').write_text('{"valid":true,"valid":false}\n')
                manifest['members']=[pin(root/p['path'],root) for p in manifest['members']]
            if name=='arbitrary_foreign_prefix': manifest['foreign_excluded_prefixes']=['primary/','notforeign/']
            (root/'ARTIFACT_MANIFEST.json').write_text(json.dumps(manifest))
            run=subprocess.run([sys.executable,'-B',str(ROOT/'verify_audit.py'),'--closure-only','--root',str(root)],capture_output=True)
            result=json.loads(run.stdout)
            expected=0 if name=='valid' else 1
            assert run.returncode==expected,(name,run.returncode,result)
            assert not run.stderr,(name,run.stderr)
            cases.append({'case':name,'expected_exit':expected,'actual_exit':run.returncode,'result':result})
        assert not root.exists()
    print(json.dumps({'status':'PASS','cases':cases,'private_fixture_roots_removed':True,'all_fixture_writes_within_owned_family':True},indent=2))

if __name__=='__main__': main()
