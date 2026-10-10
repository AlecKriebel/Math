"""Adversarial tests against the strict verifier, using disposable bundle copies."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT=pathlib.Path(__file__).resolve().parent


def write_manifest(root, mutate=None):
    data=json.loads((root/'MANIFEST.json').read_text())
    if mutate:
        mutate(data)
    (root/'MANIFEST.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')


def rehash(root,name):
    def update(data):
        for row in data['files']:
            if row['path']==name:
                content=(root/name).read_bytes()
                row.update(bytes=len(content),sha256=hashlib.sha256(content).hexdigest())
    write_manifest(root,update)


def mutate(root,case):
    if case=='extra_file':
        (root/'unexpected.txt').write_text('unexpected')
    elif case=='omitted_file':
        (root/'AUDIT.md').unlink()
    elif case=='modified_file':
        with (root/'AUDIT.md').open('a') as file:file.write('changed')
    elif case=='boolean_byte_count':
        write_manifest(root,lambda d:d['files'][0].update(bytes=True))
    elif case=='traversal_path':
        write_manifest(root,lambda d:d['files'][0].update(path='../AUDIT.md'))
    elif case=='duplicate_member':
        write_manifest(root,lambda d:d['files'].append(d['files'][0].copy()))
    elif case=='duplicate_json_key':
        path=root/'MANIFEST.json'
        path.write_text(path.read_text().replace('"schema": 1','"schema": 1, "schema": 1'))
    elif case=='symlink_member':
        (root/'AUDIT.md').unlink()
        (root/'AUDIT.md').symlink_to(ROOT/'AUDIT.md')
    elif case=='forged_expected_results_rehashed':
        path=root/'EXPECTED_RESULTS.json';data=json.loads(path.read_text())
        data['counts']['short_path_projections']+=1
        path.write_text(json.dumps(data)+'\n');rehash(root,path.name)
    elif case=='forged_author_binding_rehashed':
        path=root/'AUTHOR_BINDING.json';data=json.loads(path.read_text())
        data['proof']['sha256']='0'*64
        path.write_text(json.dumps(data)+'\n');rehash(root,path.name)
    else:
        raise RuntimeError('unknown mutation')


def main():
    cases=['extra_file','omitted_file','modified_file','boolean_byte_count','traversal_path','duplicate_member','duplicate_json_key','symlink_member','forged_expected_results_rehashed','forged_author_binding_rehashed']
    results=[]
    for optimized in (False,True):
        with tempfile.TemporaryDirectory(prefix='wreath-review-2-integrity-') as parent:
            clean=pathlib.Path(parent)/'clean';shutil.copytree(ROOT,clean)
            flags=['-B']+(['-O'] if optimized else [])
            command=[sys.executable]+flags+[str(clean/'verify.py')]
            run=subprocess.run(command,capture_output=True,text=True,timeout=60)
            if run.returncode!=0:raise RuntimeError('clean replay failed: '+run.stderr)
            results.append({'mode':'optimized' if optimized else 'normal','case':'clean_bundle','accepted':True})
            for case in cases:
                trial=pathlib.Path(parent)/case;shutil.copytree(ROOT,trial)
                mutate(trial,case)
                run=subprocess.run([sys.executable]+flags+[str(trial/'verify.py')],capture_output=True,text=True,timeout=60)
                if run.returncode==0:raise RuntimeError('tampering accepted: '+case)
                results.append({'mode':'optimized' if optimized else 'normal','case':case,'rejected':True})
    return {'schema':1,'status':'passed','clean_replays':2,'tamper_rejections':20,'tests':results,'scope':'integrity and replay behavior only; no infinite-theorem certification'}


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
