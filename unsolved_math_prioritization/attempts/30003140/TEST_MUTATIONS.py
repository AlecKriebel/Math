#!/usr/bin/env python3
"""Exercise a separately pinned wrapper through an external bootstrap.

All changes occur in disposable fixtures. Original and audit freezes are retained.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BOOTSTRAP = r'''
import hashlib,pathlib,stat,sys
root=pathlib.Path(sys.argv[1]); expected_wrapper=sys.argv[2]; expected_manifest=sys.argv[3]
path=root/'VERIFY_PUBLICATION.py'
if not stat.S_ISREG(path.lstat().st_mode):
    raise SystemExit('BOOTSTRAP_REJECT: nonregular wrapper')
raw=path.read_bytes()
if hashlib.sha256(raw).hexdigest()!=expected_wrapper:
    raise SystemExit('BOOTSTRAP_REJECT: wrapper hash mismatch')
sys.argv=[str(path),'--packet',str(root),'--expected-manifest',expected_manifest,'--check-only']
exec(compile(raw,str(path),'exec'),{'__name__':'__main__','__file__':str(path)})
'''


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')


def refresh(root, names):
    path=root/'PUBLICATION_MANIFEST.json'
    m=json.loads(path.read_text())
    for item in m['files']:
        if item['path'] in names:
            raw=(root/item['path']).read_bytes()
            item.update(bytes=len(raw),sha256=sha(raw))
    write_json(path,m)


def mutate(root, name, pin):
    manifest=root/'PUBLICATION_MANIFEST.json'
    m=json.loads(manifest.read_text())
    repin=True
    if name=='wrong_external_pin':
        return '0'*64
    if name=='changed_wrapper':
        (root/'VERIFY_PUBLICATION.py').write_text("raise SystemExit(0)\n")
        refresh(root,{'VERIFY_PUBLICATION.py'})
    elif name=='missing_wrapper':
        (root/'VERIFY_PUBLICATION.py').unlink()
        repin=False
    elif name=='wrapper_symlink':
        (root/'VERIFY_PUBLICATION.py').unlink()
        (root/'VERIFY_PUBLICATION.py').symlink_to('original/verify.py')
        repin=False
    elif name=='changed_proof_stale_hash':
        with (root/'original/RESULT.md').open('ab') as stream:
            stream.write(b'\nchanged\n')
        repin=False
    elif name=='changed_proof_outer_repinned':
        with (root/'original/RESULT.md').open('ab') as stream:
            stream.write(b'\nchanged\n')
        refresh(root,{'original/RESULT.md'})
    elif name=='changed_proof_all_manifests_repinned':
        with (root/'original/RESULT.md').open('ab') as stream:
            stream.write(b'\nchanged\n')
        raw=(root/'original/RESULT.md').read_bytes()
        inner=json.loads((root/'original/MANIFEST.json').read_text())
        inner['files']['RESULT.md'].update(bytes=len(raw),sha256=sha(raw))
        write_json(root/'original/MANIFEST.json',inner)
        refresh(root,{'original/RESULT.md','original/MANIFEST.json'})
    elif name=='changed_audit':
        with (root/'independent_audit/FULL_AUDIT.md').open('ab') as stream:
            stream.write(b'\nchanged\n')
        refresh(root,{'independent_audit/FULL_AUDIT.md'})
    elif name=='missing_file':
        (root/'original/RESULT.md').unlink()
        repin=False
    elif name=='extra_file':
        (root/'original/unlisted.json').write_text('{}\n')
        repin=False
    elif name=='extra_empty_directory':
        (root/'original/unlisted').mkdir()
        repin=False
    elif name=='nested_empty_directory':
        (root/'independent_audit/unlisted/deeper').mkdir(parents=True)
        repin=False
    elif name=='payload_symlink':
        (root/'original/RESULT.md').unlink()
        (root/'original/RESULT.md').symlink_to('README.md')
        repin=False
    elif name=='directory_symlink':
        (root/'original/link').symlink_to('../independent_audit',target_is_directory=True)
        repin=False
    elif name=='special_file':
        os.mkfifo(root/'original/pipe')
        repin=False
    elif name=='executable_file_mode':
        (root/'original/verify.py').chmod(0o755)
        repin=False
    elif name=='directory_mode':
        (root/'independent_audit').chmod(0o700)
        repin=False
    elif name=='root_mode':
        root.chmod(0o700)
        repin=False
    elif name=='manifest_symlink':
        manifest.unlink()
        manifest.symlink_to('original/MANIFEST.json')
        repin=False
    elif name=='duplicate_manifest_key':
        manifest.write_text('{"status":"solved",'+manifest.read_text()[1:])
    elif name=='nonfinite_manifest':
        manifest.write_text(manifest.read_text().replace('"rank": 994','"rank": NaN'))
    elif name=='overflow_manifest':
        manifest.write_text(manifest.read_text().replace('"rank": 994','"rank": 1e9999'))
    elif name=='duplicate_auxiliary_key':
        p=root/'MUTATION_RESULTS.json'
        p.write_text('{"duplicate":1,"duplicate":2}\n')
        refresh(root,{'MUTATION_RESULTS.json'})
    elif name=='nonfinite_auxiliary':
        (root/'MUTATION_RESULTS.json').write_text('{"value":Infinity}\n')
        refresh(root,{'MUTATION_RESULTS.json'})
    else:
        if name=='false_disposition': m['status']='claimed_solved'
        elif name=='false_turns': m['turns']='0/5'
        elif name=='boolean_target': m['problem_id']=True
        elif name=='float_rank': m['rank']=994.0
        elif name=='boolean_bytes': m['files'][0]['bytes']=True
        elif name=='float_bytes': m['files'][0]['bytes']=1.0
        elif name=='negative_bytes': m['files'][0]['bytes']=-1
        elif name=='integer_digest': m['files'][0]['sha256']=123
        elif name=='unsafe_path': m['files'][0]['path']='../outside.md'
        elif name=='duplicate_inventory': m['files'].append(m['files'][0])
        elif name=='wrong_frozen_pin': m['frozen_manifest_anchors']['original']='0'*64
        elif name=='false_source_scope': m['source_files_redistributed']=0
        elif name=='nonobject_manifest': m=[]
        elif name=='empty_inventory': m['files']=[]
        elif name=='extra_schema_field': m['extra']=True
        else: raise ValueError('Unknown mutation: '+name)
        write_json(manifest,m)
    return sha(manifest.read_bytes()) if repin else pin


CASES = ['wrong_external_pin','changed_wrapper','missing_wrapper','wrapper_symlink',
         'changed_proof_stale_hash','changed_proof_outer_repinned','changed_proof_all_manifests_repinned',
         'changed_audit','missing_file','extra_file','extra_empty_directory','nested_empty_directory',
         'payload_symlink','directory_symlink','special_file','executable_file_mode','directory_mode',
         'root_mode','manifest_symlink','duplicate_manifest_key','nonfinite_manifest','overflow_manifest',
         'duplicate_auxiliary_key','nonfinite_auxiliary','false_disposition','false_turns','boolean_target',
         'float_rank','boolean_bytes','float_bytes','negative_bytes','integer_digest','unsafe_path',
         'duplicate_inventory','wrong_frozen_pin','false_source_scope','nonobject_manifest','empty_inventory',
         'extra_schema_field']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path,default=Path(__file__).absolute().parent)
    parser.add_argument('--expected-manifest',required=True)
    parser.add_argument('--expected-wrapper',required=True)
    args=parser.parse_args()
    root=args.packet.absolute()
    env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE']='1'
    positive,rejected,bootstrap_rejected=0,0,0
    for label,flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        def invoke(target,pin):
            return subprocess.run([sys.executable,'-I','-B',*flags,'-c',BOOTSTRAP,
                  str(target),args.expected_wrapper,pin],cwd='/',env=env,capture_output=True,timeout=30)
        cp=invoke(root,args.expected_manifest)
        need(cp.returncode==0 and json.loads(cp.stdout)['status']=='PASS_BOUNDED_PUBLICATION',
             'Positive bootstrap failed: '+label+': '+cp.stderr.decode(errors='replace'))
        positive+=1
        with tempfile.TemporaryDirectory(prefix='borcherds-bootstrap-controls-') as td:
            for name in CASES:
                fixture=Path(td)/name
                shutil.copytree(root,fixture)
                for p in [fixture,*fixture.rglob('*')]:
                    p.chmod(0o755 if p.is_dir() else 0o644)
                pin=mutate(fixture,name,args.expected_manifest)
                cp=invoke(fixture,pin)
                need(cp.returncode!=0,'Mutation accepted: '+label+'/'+name)
                if name in ('changed_wrapper','wrapper_symlink'):
                    need(b'BOOTSTRAP_REJECT' in cp.stderr,'Missing external bootstrap rejection')
                    bootstrap_rejected+=1
                rejected+=1
    print(json.dumps(dict(status='PASS_EXTERNAL_BOOTSTRAP_MUTATIONS',modes=['normal','-O','-OO'],
          positive=positive,rejected=rejected,cases_per_mode=len(CASES),cases=CASES,
          explicit_wrapper_bootstrap_rejections=bootstrap_rejected,
          limits='Disposable fixtures only; integrity checks are not a mathematical proof checker.'),indent=2,sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except Exception as error:
        print('MUTATION_TEST_REJECT: '+str(error),file=sys.stderr)
        sys.exit(1)
