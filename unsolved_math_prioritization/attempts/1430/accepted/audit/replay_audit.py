#!/usr/bin/env python3
"""Replay a pinned envelope and reject bounded mutations in disposable copies.

Usage: replay_audit.py ENVELOPE EXTERNAL_PINS_JSON
Authenticate this script and supplied pins through a separate trusted channel first.
The envelope contains packet/, freeze/, and their externally identified pins.
No source documents or source datasets are needed. Emits a path-free JSON receipt.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(base):
    return {str(p.relative_to(base)): {'bytes':p.stat().st_size,'sha256':digest(p),
             'mode':stat.S_IMODE(p.stat().st_mode)}
            for sub in ('packet','freeze') for p in sorted((base/sub).iterdir())}


def main(base, pins_path):
    pins = json.loads(pins_path.read_bytes())
    before = snapshot(base)
    need(digest(base/'freeze/bootstrap.py') == pins['bootstrap_sha256'], 'external bootstrap digest')
    need(digest(base/'freeze/AUTHOR_MANIFEST.json') == pins['manifest_sha256'], 'external manifest digest')
    need(os.geteuid() != 0, 'read-only replay requires non-root')
    denied = []
    for sub in ('packet','freeze'):
        need(not os.access(base/sub, os.W_OK), 'envelope directory is writable')
        for p in (base/sub).iterdir():
            need(not os.access(p, os.W_OK), 'envelope file is writable')
        # Exclusive file creation can never modify an existing file.
        try:
            with (base/sub/'audit_write_probe').open('xb'):
                pass
        except PermissionError:
            denied.append(sub+'/audit_write_probe')
        else:
            raise RuntimeError('directory read-only probe unexpectedly succeeded')
    # Opening without truncation tests whether the actual existing file is writable.
    for name in ('packet/README.md','freeze/bootstrap.py'):
        try:
            fd = os.open(base/name, os.O_WRONLY)
        except PermissionError:
            denied.append(name)
        else:
            os.close(fd)
            raise RuntimeError('file read-only probe unexpectedly succeeded')

    modes = [[],['-O'],['-OO']]
    results = []

    def run(root, mode, expect):
        if digest(root/'freeze/bootstrap.py') != pins['bootstrap_sha256']:
            need(not expect, 'trusted bootstrap changed')
            return {'exit':None,'rejection':'external bootstrap digest'}
        proc = subprocess.run([sys.executable,'-I','-S','-B',*mode,
              str(root/'freeze/bootstrap.py'),str(root/'packet')],
              stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
        need((proc.returncode==0)==expect, 'unexpected bootstrap acceptance')
        if expect:
            value=json.loads(proc.stdout)
            need(value['status']=='PASS' and value['manifest_sha256']==pins['manifest_sha256'], 'bootstrap result')
        else:
            need(b'REJECT:' in proc.stderr,'missing explicit rejection')
        return {'exit':proc.returncode,'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),
                'rejection':proc.stderr.decode().strip().replace(str(root),'<test-envelope>') if proc.returncode else None}

    for mode in modes:
        results.append({'case':'nonroot_readonly_original','mode':mode,'result':run(base,mode,True)})

    with tempfile.TemporaryDirectory(prefix='word-audit-') as tmp:
        scratch=Path(tmp)

        def fresh(name):
            root=scratch/name
            root.mkdir()
            for sub in ('packet','freeze'):
                shutil.copytree(base/sub,root/sub)
                (root/sub).chmod(0o755)
                for p in (root/sub).iterdir():
                    p.chmod(0o644)
            return root

        relocated=fresh('relocated')
        for sub in ('packet','freeze'):
            for p in (relocated/sub).iterdir():
                p.chmod(0o444)
            (relocated/sub).chmod(0o555)
        for mode in modes:
            results.append({'case':'relocated_readonly','mode':mode,'result':run(relocated,mode,True)})

        def rewrite_manifest(root, mutate):
            p=root/'freeze/AUTHOR_MANIFEST.json'
            data=json.loads(p.read_bytes())
            mutate(data)
            p.write_text(json.dumps(data))

        def reseal(root):
            def update(data):
                for entry in data['files']:
                    p=root/'packet'/entry['path']
                    entry.update(bytes=p.stat().st_size,sha256=digest(p))
            rewrite_manifest(root,update)

        def mutate(root, name):
            p=root/'packet/README.md'
            if name=='payload_byte':
                p.write_bytes(p.read_bytes()+b'altered')
            elif name=='missing_payload':
                p.unlink()
            elif name=='extra_payload':
                (root/'packet/extra').write_bytes(b'extra')
            elif name=='extra_directory':
                (root/'packet/extra').mkdir()
            elif name=='payload_symlink':
                p.unlink();p.symlink_to(base/'packet/README.md')
            elif name=='root_symlink':
                (root/'packet').rename(root/'actual')
                (root/'packet').symlink_to(root/'actual')
            elif name=='fifo':
                p.unlink();os.mkfifo(p)
            elif name=='unsafe_mode':
                p.chmod(0o666)
            elif name=='manifest_byte':
                p=root/'freeze/AUTHOR_MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
            elif name=='manifest_duplicate_key':
                p=root/'freeze/AUTHOR_MANIFEST.json';p.write_bytes(b'{"schema":"x",'+p.read_bytes()[1:])
            elif name=='manifest_unsafe_path':
                rewrite_manifest(root,lambda d:d['files'][0].update(path='../outside'))
            elif name=='manifest_duplicate_path':
                rewrite_manifest(root,lambda d:d['files'].append(d['files'][0]))
            elif name=='manifest_boolean_bytes':
                rewrite_manifest(root,lambda d:d['files'][0].update(bytes=True))
            elif name=='resealed_payload':
                p.write_bytes(p.read_bytes()+b'altered');reseal(root)
            elif name=='resealed_hostile_verifier':
                (root/'packet/verify.py').write_text("from pathlib import Path\nPath('../HOSTILE_EXECUTED').write_text('unsafe')\n")
                reseal(root)
            elif name=='bootstrap_byte':
                p=root/'freeze/bootstrap.py';p.write_bytes(p.read_bytes()+b'\n# altered\n')
            else:
                raise RuntimeError('unknown mutation')

        variants=['payload_byte','missing_payload','extra_payload','extra_directory','payload_symlink',
                  'root_symlink','fifo','unsafe_mode','manifest_byte','manifest_duplicate_key',
                  'manifest_unsafe_path','manifest_duplicate_path','manifest_boolean_bytes',
                  'resealed_payload','resealed_hostile_verifier','bootstrap_byte']
        for name in variants:
            root=fresh(name);mutate(root,name)
            for mode in modes:
                results.append({'case':name,'mode':mode,'result':run(root,mode,False)})
            need(not (root/'HOSTILE_EXECUTED').exists(),'untrusted verifier executed')

        direct=['missing_mask','wrong_mask_word','boolean_letter','nonuniform_word','duplicate_key',
                'nonfinite','overflow_float','invalid_syntax','oversize','wrong_top_level']
        for name in direct:
            root=fresh('direct_'+name);p=root/'packet/SMALL_WITNESSES.json'
            data=json.loads(p.read_bytes())
            if name=='missing_mask':
                del data['5']['10'];p.write_text(json.dumps(data))
            elif name=='wrong_mask_word':
                data['2']['0']=data['2']['1'];p.write_text(json.dumps(data))
            elif name=='boolean_letter':
                data['2']['0'][0]=True;p.write_text(json.dumps(data))
            elif name=='nonuniform_word':
                data['2']['0'].pop();p.write_text(json.dumps(data))
            elif name=='duplicate_key':
                p.write_bytes(b'{"1":{},'+p.read_bytes()[1:])
            elif name=='nonfinite':
                p.write_bytes(b'{"1":NaN}')
            elif name=='overflow_float':
                p.write_bytes(b'{"1":1e9999}')
            elif name=='invalid_syntax':
                p.write_bytes(b'{')
            elif name=='oversize':
                p.write_bytes(b' '*2000001)
            elif name=='wrong_top_level':
                p.write_bytes(b'[]')
            for mode in modes:
                proc=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'packet/verify.py')],
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
                need(proc.returncode!=0 and b'REJECT:' in proc.stderr,'direct malformed input accepted')
                results.append({'case':'direct_'+name,'mode':mode,'result':{'exit':proc.returncode,
                    'rejection':proc.stderr.decode().strip().replace(str(root),'<test-envelope>')}})
        # Read-only relocation is intentionally retained until all replays finish.
        for sub in ('packet','freeze'):
            (relocated/sub).chmod(0o755)

    need(snapshot(base)==before,'frozen bytes or modes changed')
    return {'schema':'independent-word-representation-replay-v1','status':'PASS','problem_id':1430,
       'effective_uid':os.geteuid(),'pins':pins,'readonly_write_probes_denied':denied,
       'original_snapshot_unchanged':True,'bootstrap_positive_runs':6,'integrity_mutant_variants':len(variants),
       'integrity_mutant_mode_runs':3*len(variants),'direct_malformed_variants':len(direct),
       'direct_malformed_mode_runs':3*len(direct),'total_runs':len(results),'results':results,
       'limits':['Non-root permission-enforced read-only packet and freeze; no mount-isolation claim.',
                 'Manifest corruptions fail the external hash gate before parsing; direct payload controls separately test semantics and parsing.',
                 'No concurrent-hostile-filesystem claim; no external Lean build or certificate reproduction.']}


if __name__=='__main__':
    need(len(sys.argv)==3,'usage: replay_audit.py ENVELOPE EXTERNAL_PINS_JSON')
    print(json.dumps(main(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve()),indent=2,sort_keys=True))
