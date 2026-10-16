#!/usr/bin/env python3
"""Outer integrity controls; all mutations are disposable, never executed code."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

MODES=[('normal',[]),('-O',['-O']),('-OO',['-OO'])]

def need(ok,msg):
    if not ok:raise ValueError(msg)

def sha(b):return hashlib.sha256(b).hexdigest()

def thaw(root):
    root.chmod(0o755)
    for p in root.rglob('*'):
        if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)

def freeze(root):
    for p in sorted(root.rglob('*'),key=lambda p:len(p.parts),reverse=True):
        p.chmod(0o555 if p.is_dir() else 0o444)
    root.chmod(0o555)

def main():
    need(len(sys.argv)==5,'expected root and three trusted pins')
    root=Path(os.path.abspath(sys.argv[1]));mp,bp,vp=sys.argv[2:]
    wrapper=(root/'verify_publication.py').read_bytes()
    need(sha(wrapper)==vp,'external verifier identity')
    trusted={'__name__':'trusted_publication'}
    exec(compile(wrapper,'<trusted-publication>','exec'),trusted)
    snap,parsed=trusted['integrity'](root,mp,bp)
    need(os.getuid()==os.geteuid()!=0,'actual nonroot required')
    with tempfile.TemporaryDirectory(prefix='ep1133-publication-controls-') as td:
        work=Path(td);cwd=work/'cwd';cwd.mkdir();shadow=work/'shadow';shadow.mkdir()
        sentinel=work/'SHADOW_EXECUTED'
        for name in ['sitecustomize.py','usercustomize.py','json.py','hashlib.py','tarfile.py']:
            (shadow/name).write_text('open('+repr(str(sentinel))+',"w").write("bad")\nraise SystemExit(71)\n')
        env=dict(PATH=os.defpath,HOME=str(work),TMPDIR=str(work),LC_ALL='C',PYTHONPATH=str(shadow),
                 PYTHONSTARTUP=str(shadow/'sitecustomize.py'),PYTHONINSPECT='1',PYTHONOPTIMIZE='9',
                 PYTHONDONTWRITEBYTECODE='0')
        boot=root/'BOOTSTRAP.py'
        def baseline(packet,flags):
            x=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(boot),str(packet)],cwd=shadow,
                env=env,capture_output=True,timeout=360)
            need(x.returncode==0 and x.stderr==b'','baseline failed: '+x.stderr.decode()[:200])
            return x.stdout
        outputs=[baseline(root,flags) for _,flags in MODES]
        need(len(set(outputs))==1,'optimization outputs differ')
        ro=work/'readonly';shutil.copytree(root,ro);freeze(ro)
        denied=0
        try:
            for p in [ro/'NEW_FILE',ro/'README.md',ro/'author/public/REPORT.md',ro/'independent_audit/SCOPE.json']:
                try:
                    with p.open('ab') as f:f.write(b'forbidden')
                except PermissionError:denied+=1
                else:raise ValueError('read-only write succeeded')
            outputs.extend(baseline(ro,flags) for _,flags in MODES)
            need(len(set(outputs))==1,'read-only outputs differ')
            trusted['integrity'](ro,mp,bp)
        finally:thaw(ro)
        need(not sentinel.exists(),'hostile environment was executed')
        # Rejections execute only the original externally pinned verifier. The
        # mutated packet's Python is always data, even when code is replaced.
        runner=work/'trusted_integrity.py'
        runner.write_bytes(b'import sys\nns={"__name__":"trusted"}\nexec(compile('+repr(wrapper).encode()+b',"<trusted>","exec"),ns)\ntry:\n ns["integrity"](ns["Path"](sys.argv[1]),sys.argv[2],sys.argv[3])\nexcept (ValueError,OSError,TypeError,KeyError,ns["tarfile"].TarError):\n print("REJECT: integrity",file=sys.stderr);sys.exit(1)\n')
        labels=['payload','missing','extra','extra_directory','payload_symlink','directory_symlink','fifo','root_symlink',
            'verifier_code','bootstrap_code','control_code','archive_bytes','independent_archive_bytes',
            'wrong_manifest_pin','wrong_bootstrap_pin','manifest_boolean_size','manifest_float_size',
            'manifest_negative_size','manifest_boolean_schema','manifest_float_problem','manifest_duplicate_path',
            'manifest_unknown_path','manifest_traversal','manifest_absolute','manifest_wrong_digest','manifest_extra_key',
            'manifest_duplicate_key','manifest_nan','manifest_infinity','manifest_float_overflow','accepted_claim_repin']
        rows=[]
        for label in labels:
            cp=work/('case-'+label);shutil.copytree(root,cp);thaw(cp);pin=mp;bootstrap_pin=bp;target=cp
            p=cp/'PUBLICATION_MANIFEST.json'
            if label=='payload':(cp/'README.md').write_bytes(b'changed')
            elif label=='missing':(cp/'README.md').unlink()
            elif label=='extra':(cp/'EXTRA').write_bytes(b'extra')
            elif label=='extra_directory':(cp/'EXTRA').mkdir()
            elif label=='payload_symlink':
                (cp/'README.md').unlink();(cp/'README.md').symlink_to(root/'README.md')
            elif label=='directory_symlink':
                shutil.rmtree(cp/'author');(cp/'author').symlink_to(root/'author',target_is_directory=True)
            elif label=='fifo':
                (cp/'README.md').unlink();os.mkfifo(cp/'README.md')
            elif label=='root_symlink':
                target=work/'linked-root';target.symlink_to(cp,target_is_directory=True)
            elif label in ['verifier_code','bootstrap_code','control_code']:
                file={'verifier_code':'verify_publication.py','bootstrap_code':'BOOTSTRAP.py','control_code':'mutation_tests.py'}[label]
                (cp/file).write_text('raise SystemExit(0)\n')
            elif label in ['archive_bytes','independent_archive_bytes']:
                file='ROBUST_INTERPOLATION_2508_'+('INDEPENDENT_AUDIT' if label=='independent_archive_bytes' else 'AUDIT')+'.tar.gz'
                (cp/file).write_bytes((cp/file).read_bytes()+b'changed')
            elif label=='wrong_manifest_pin':pin='0'*64
            elif label=='wrong_bootstrap_pin':bootstrap_pin='0'*64
            elif label=='accepted_claim_repin':
                file=cp/'author/public/CLAIMS.json';obj=json.loads(file.read_bytes());obj['community_acceptance_verified']=True
                file.write_text(json.dumps(obj))
                obj=json.loads(p.read_bytes())
                for row in obj['files']:
                    raw=(cp/row['path']).read_bytes();row.update(bytes=len(raw),sha256=sha(raw))
                p.write_text(json.dumps(obj));pin=sha(p.read_bytes())
            else:
                obj=json.loads(p.read_bytes());row=obj['files'][0]
                if label=='manifest_boolean_size':row['bytes']=True
                elif label=='manifest_float_size':row['bytes']=1.0
                elif label=='manifest_negative_size':row['bytes']=-1
                elif label=='manifest_boolean_schema':obj['schema']=True
                elif label=='manifest_float_problem':obj['problem_id']=2508.0
                elif label=='manifest_duplicate_path':obj['files'].append(dict(row))
                elif label=='manifest_unknown_path':row['path']='UNKNOWN'
                elif label=='manifest_traversal':row['path']='../README.md'
                elif label=='manifest_absolute':row['path']='/README.md'
                elif label=='manifest_wrong_digest':row['sha256']='A'*64
                elif label=='manifest_extra_key':obj['extra']=True
                raw=json.dumps(obj)
                if label=='manifest_duplicate_key':raw=raw.replace('"schema": 1','"schema": 1,"schema": 1',1)
                elif label=='manifest_nan':raw=raw.replace('"schema": 1','"schema": NaN',1)
                elif label=='manifest_infinity':raw=raw.replace('"schema": 1','"schema": Infinity',1)
                elif label=='manifest_float_overflow':raw=raw.replace('"schema": 1','"schema": 1e999',1)
                p.write_text(raw);pin=sha(p.read_bytes())
            for mode,flags in MODES:
                x=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(runner),str(target),pin,bootstrap_pin],
                    cwd=cwd,env=env,capture_output=True,timeout=30)
                need(x.returncode!=0 and x.stderr.startswith(b'REJECT:'),'accepted mutation: '+label)
                rows.append(dict(label=label,mode=mode,rejected=True))
        # Directly challenge archive structure as well as its fixed outer hash.
        archive_rows=[]
        original=snap['ROBUST_INTERPOLATION_2508_AUDIT.tar.gz'];prefix='author/';names=trusted['AUTHOR']
        for label in ['duplicate','missing','traversal','absolute','symlink','hardlink','directory','changed_bytes','pax']:
            out=io.BytesIO()
            with tarfile.open(fileobj=io.BytesIO(original),mode='r:gz') as src,tarfile.open(fileobj=out,mode='w:gz') as dest:
                members=src.getmembers()
                for i,e in enumerate(members):
                    data=src.extractfile(e).read()
                    if i==0:
                        if label=='missing':continue
                        if label=='traversal':e.name='../'+e.name
                        if label=='absolute':e.name='/'+e.name
                        if label=='symlink':e.type=tarfile.SYMTYPE;e.linkname='README.md';e.size=0;data=b''
                        if label=='hardlink':e.type=tarfile.LNKTYPE;e.linkname=members[1].name;e.size=0;data=b''
                        if label=='directory':e.type=tarfile.DIRTYPE;e.size=0;data=b''
                        if label=='changed_bytes':data=b'x'+data[1:]
                        if label=='pax':e.pax_headers={'comment':'untrusted'}
                    dest.addfile(e,io.BytesIO(data))
                    if i==0 and label=='duplicate':dest.addfile(e,io.BytesIO(data))
            try:trusted['archive'](out.getvalue(),snap,prefix,names)
            except (ValueError,tarfile.TarError):archive_rows.append(dict(label=label,rejected=True))
            else:raise ValueError('accepted archive mutation: '+label)
        trusted['integrity'](root,mp,bp)
        need(all((root/n).read_bytes()==b for n,b in snap.items()),'original packet changed')
        print(json.dumps(dict(status='PASS',baseline_modes=[x[0] for x in MODES],readonly_modes=[x[0] for x in MODES],
            six_outputs_identical=True,actual_nonroot=True,readonly_write_probes_denied=denied,
            hostile_environment_ignored=True,packet_mutation_categories=len(labels),packet_mutation_rejections=len(rows),
            archive_structural_rejections=len(archive_rows),rejections=rows,archive_rejections=archive_rows,
            baseline_output_sha256=sha(outputs[0]),baseline=json.loads(outputs[0]),frozen_packet_unchanged=True),sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired,tarfile.TarError) as e:
        print('CONTROL FAILURE: '+str(e),file=sys.stderr);sys.exit(1)
