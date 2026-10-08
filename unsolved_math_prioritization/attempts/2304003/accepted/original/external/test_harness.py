#!/usr/bin/env python3
"""Reproduce nonroot, hostile-input, read-only, and snapshot integrity controls."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(ok,msg):
    if not ok: raise RuntimeError(msg)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(cmd,raw=None,cwd=None,env=None):
    return subprocess.run(cmd,input=raw,capture_output=True,cwd=cwd,env=env,timeout=40)
def modeflags(mode):return [] if mode=="normal" else ["-"+mode]
def copytree(src,dst):
    shutil.copytree(src,dst)
    os.chmod(dst,0o755)
    for p in dst.rglob('*'):
        if p.is_dir():os.chmod(p,0o755)
        else:os.chmod(p,0o644)
    return dst

def main():
    need(len(sys.argv)==4,"usage: test_harness.py PUBLIC EXTERNAL TRUSTED_MANIFEST_SHA256")
    public=Path(sys.argv[1]).resolve();external=Path(sys.argv[2]).resolve();pin=sys.argv[3]
    need(os.getuid()!=0 and os.geteuid()!=0,"genuine nonroot run required")
    baseline={p.name:digest(p) for p in public.iterdir()}
    fixture=(public/'fixtures.json').read_bytes();obj=json.loads(fixture)
    manifest=(external/'MANIFEST.json');bootstrap=(external/'bootstrap.py')
    need(digest(manifest)==pin,"initial manifest pin mismatch")
    reports=[]
    malformed=[]
    def mutate(label,key,value):
        v=copy.deepcopy(obj);v[key]=value
        malformed.append((label,json.dumps(v,allow_nan=True).encode()))
    mutate('bool_int','energy_max_terms',True)
    mutate('float_int','landau_max_index',64.0)
    mutate('nan','fejer_max_index',float('nan'))
    mutate('positive_infinity','fejer_max_index',float('inf'))
    mutate('negative_infinity','fejer_max_index',-float('inf'))
    mutate('range_overflow','rudin_shapiro_max_depth',1000000)
    mutate('negative_bound','fejer_max_index',-1)
    mutate('status_overclaim','status','SOLVED')
    mutate('extra_key','extra',0)
    mutate('incorrect_count','approaches_counted',4)
    v=copy.deepcopy(obj);del v['status'];malformed.append(('missing_key',json.dumps(v).encode()))
    malformed.append(('duplicate_key',fixture.replace(b'"schema_version": 1',b'"schema_version": 1, "schema_version": 1')))
    malformed.append(('nonobject',b'[]'))
    malformed.append(('excess_size',b' '*100001))
    for label,change in [('bad_coefficient',('coefficients',[2,5,-1])),
                         ('boolean_coefficient',('coefficients',[True,4,-1])),
                         ('zero_denominator',('objective_squared',[4,0])),
                         ('noncanonical_rational',('objective_squared',[8,6])),
                         ('bad_slack',('slack_coefficients',[2,-8,9])),
                         ('false_norm',('normalization_squared',28))]:
        v=copy.deepcopy(obj);v['quadratic'][change[0]]=change[1]
        malformed.append((label,json.dumps(v).encode()))
    with tempfile.TemporaryDirectory(prefix='bounded_partial_audit_') as temp:
        t=Path(temp);ro=copytree(public,t/'readonly');hostile=t/'hostile';hostile.mkdir()
        for name in ['json.py','fractions.py','hashlib.py','subprocess.py','sitecustomize.py']:
            (hostile/name).write_text("from pathlib import Path\nPath('HOSTILE_IMPORT_EXECUTED').write_text('bad')\nraise RuntimeError('hostile import')\n")
        for p in ro.iterdir():p.chmod(0o444)
        ro.chmod(0o555)
        try:
            with open(ro/'fixtures.json','ab') as f:f.write(b'bad')
            raise RuntimeError('read-only append unexpectedly succeeded')
        except PermissionError:pass
        try:
            (ro/'WRITE_PROBE').write_text('bad')
            raise RuntimeError('read-only create unexpectedly succeeded')
        except PermissionError:pass
        env=dict(os.environ);env.update({'PYTHONPATH':str(hostile),'TMPDIR':str(ro),
                                         'PYTHONDONTWRITEBYTECODE':'1'})
        for mode in ['normal','O','OO']:
            flags=modeflags(mode)
            cmd=[sys.executable,'-I','-B',*flags,str(ro/'verify.py'),'--stdin']
            good=run(cmd,fixture,cwd=hostile,env=env)
            need(good.returncode==0,'positive verifier failed')
            parsed=json.loads(good.stdout)
            need(parsed['ok'] is True and parsed['analytic_proof_mechanized'] is False,'wrong positive report')
            labels=[]
            for label,raw in malformed:
                bad=run(cmd,raw,cwd=hostile,env=env)
                need(bad.returncode!=0,'accepted malformed fixture: '+label)
                need(json.loads(bad.stderr)['ok'] is False,'nonstructured rejection: '+label)
                labels.append(label)
            bc=[sys.executable,'-I','-B',*flags,str(bootstrap),str(ro),str(manifest),pin,mode]
            br=run(bc,cwd=hostile,env=env)
            need(br.returncode==0,'snapshot bootstrap failed')
            need(json.loads(br.stdout)['euid']!=0,'root bootstrap invalidates control')
            reports.append({'mode':mode,'positive_exact_identities':parsed['counts'],
              'hostile_fixtures_rejected':labels,'snapshot_bootstrap_passed':True,
              'readonly_existing_file_append_denied':True,'readonly_new_file_create_denied':True,
              'hostile_imports_ignored':True})
        need(not (hostile/'HOSTILE_IMPORT_EXECUTED').exists(),'hostile module executed')
        need({p.name:digest(p) for p in ro.iterdir()}==baseline,'read-only snapshot changed')
        tamper=[]
        for i,label in enumerate(['changed_report','changed_verifier','missing_file','extra_file','symlink_file','wrong_pin']):
            pack=copytree(public,t/('tamper'+str(i)))
            usepin=pin
            if label=='changed_report':(pack/'REPORT.md').write_bytes((pack/'REPORT.md').read_bytes()+b'X')
            elif label=='changed_verifier':(pack/'verify.py').write_bytes(b'print("forged")\n')
            elif label=='missing_file':(pack/'fixtures.json').unlink()
            elif label=='extra_file':(pack/'extra.txt').write_text('unexpected')
            elif label=='symlink_file':
                (pack/'fixtures.json').unlink();(pack/'fixtures.json').symlink_to(public/'fixtures.json')
            elif label=='wrong_pin':usepin='0'*64
            for mode in ['normal','O','OO']:
                br=run([sys.executable,'-I','-B',*modeflags(mode),str(bootstrap),str(pack),str(manifest),usepin,mode])
                need(br.returncode!=0,'bootstrap accepted tamper: '+label)
            tamper.append(label)
        for i,(label,edit) in enumerate([
                ('manifest_boolean_size',lambda m:m['files'][0].update(bytes=True)),
                ('manifest_unsafe_name',lambda m:m['files'][0].update(name='../escape')),
                ('manifest_duplicate_file',lambda m:m['files'].append(m['files'][0])),
                ('manifest_extra_key',lambda m:m.update(extra=1))]):
            m=json.loads(manifest.read_bytes());edit(m);badm=t/('bad_manifest'+str(i)+'.json')
            badm.write_text(json.dumps(m));p=digest(badm)
            for mode in ['normal','O','OO']:
                br=run([sys.executable,'-I','-B',*modeflags(mode),str(bootstrap),str(public),str(badm),p,mode])
                need(br.returncode!=0,'bootstrap accepted malformed manifest: '+label)
            tamper.append(label)
        # Owner needs write permission restored for TemporaryDirectory cleanup.
        ro.chmod(0o755)
        for p in ro.iterdir():p.chmod(0o644)
    need({p.name:digest(p) for p in public.iterdir()}==baseline,'original packet changed')
    print(json.dumps({'ok':True,'uid':os.getuid(),'euid':os.geteuid(),
      'manifest_sha256':pin,'python_version':sys.version.split()[0],
      'reports':reports,'tamper_controls_rejected_in_all_modes':tamper,
      'all_original_hashes_unchanged':True,'root_required':False,
      'scope':'Exact identities and software robustness, not formal verification of analytic proof.'},
      indent=2,sort_keys=True,allow_nan=False))

if __name__=='__main__':main()
