"""Independent adversarial validation harness; never run candidate code before integrity validation."""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile

if len(sys.argv) != 3:
    raise SystemExit('usage: recheck_author_controls.py INPUT_DIRECTORY EXTERNAL_OUTPUT_JSON')
base = pathlib.Path(sys.argv[1]).resolve()
destination = pathlib.Path(sys.argv[2]).absolute()
if destination == base or base in destination.parents:
    raise SystemExit('output must be outside the input directory')
prefix = 'HEIGHT_COUNTS_30002439_AUTHOR'
archive = base/(prefix+'_SAFE_FREEZE.zip')
manifest = base/(prefix+'_EXTERNAL_MANIFEST.json')
bootstrap = base/(prefix+'_BOOTSTRAP.py')
expected_zip = '94ec6adf37a9b6cdd4532ef448ae72ed46ac739b50c81c69686ffa34370e7304'
expected_manifest = '3527edc41af60fc640160c63416aacccc212d99d04f6f9a0c54cd7e477b4cfec'
expected_bootstrap = '6602a795c3fad2853e7f8ab4a3dc5ce801282d71f91e5acb52020ab23845eeb3'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

for p, digest in [(archive, expected_zip),(manifest, expected_manifest),(bootstrap, expected_bootstrap)]:
    require(hashlib.sha256(p.read_bytes()).hexdigest() == digest, 'untrusted audit input '+p.name)
data = json.loads(manifest.read_bytes())
with zipfile.ZipFile(archive) as z:
    require(set(z.namelist()) == set(data['files']) and len(z.namelist()) == len(data['files']), 'input inventory')
    payloads = {name:z.read(name) for name in z.namelist()}
for name, value in payloads.items():
    require(hashlib.sha256(value).hexdigest() == data['files'][name]['sha256'], 'untrusted member')
expected = payloads['RESULTS.json']
records = []

def check(label, args, accepted, cwd=None, env=None, diagnostic=None):
    p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, timeout=30)
    ok = (p.returncode == 0 and p.stdout == expected and not p.stderr) if accepted else (p.returncode != 0 and p.stdout == b'')
    if diagnostic is not None:
        ok = ok and diagnostic.encode() in p.stderr
    require(ok, (label, p.returncode, p.stdout, p.stderr))
    records.append({'test':label,'result':'PASS','expected':'accept exact checker output' if accepted else 'reject without checker output','exit_code':p.returncode,'diagnostic':p.stderr.decode(errors='replace').strip()[:250]})

with tempfile.TemporaryDirectory(prefix='independent-height-audit-') as tmp:
    t=pathlib.Path(tmp)
    root=t/'extracted';root.mkdir()
    for name,value in payloads.items():
        (root/name).write_bytes(value)
    # Fully relocate the external trust root too.
    a=t/archive.name;a.write_bytes(archive.read_bytes())
    m=t/manifest.name;m.write_bytes(manifest.read_bytes())
    boot=t/bootstrap.name;boot.write_bytes(bootstrap.read_bytes())
    shadow=t/'hostile';shadow.mkdir();marker=t/'EXECUTED'
    malicious='from pathlib import Path\nPath('+repr(str(marker))+').write_text("unexpected execution")\nraise RuntimeError("unexpected execution")\n'
    for name in ('json.py','hashlib.py','zipfile.py','pathlib.py','fractions.py','sitecustomize.py','usercustomize.py'):
        (shadow/name).write_text(malicious)
    env=dict(os.environ, PYTHONPATH=str(shadow), PYTHONSTARTUP=str(shadow/'sitecustomize.py'), PYTHONPYCACHEPREFIX=str(t/'externalcache'))
    def command(r=root, ar=a, ma=m, bp=boot, opts=('-I','-S')):
        return [sys.executable,*opts,str(bp),str(r),str(ar),str(ma)]
    for opts in (('-I','-S'),('-I','-S','-O')):
        mode='optimized' if '-O' in opts else 'normal'
        check(mode+' fully relocated baseline',command(opts=opts),True)
        check(mode+' cwd and PYTHONPATH shadows ignored',command(opts=opts),True,cwd=shadow,env=env)
        require(not marker.exists(), 'shadow executed')
        for extra,kind in [('__pycache__','dir'),('empty','dir'),('unexpected.txt','file'),('json.py','file'),('verify_math.pyc','file')]:
            p=root/extra
            if kind=='dir':p.mkdir()
            else:p.write_text(malicious)
            check(mode+' unexpected '+extra,command(opts=opts),False,diagnostic='strict root inventory mismatch')
            if kind=='dir':p.rmdir()
            else:p.unlink()
        for name in payloads:
            p=root/name;p.write_bytes(payloads[name]+b'\n')
            check(mode+' tampered '+name,command(opts=opts),False,diagnostic='member digest mismatch')
            p.write_bytes(payloads[name])
        p=root/'verify_math.py';p.write_text(malicious)
        check(mode+' malicious replacement checker',command(opts=opts),False,diagnostic='member digest mismatch')
        require(not marker.exists(), 'replacement checker executed');p.write_bytes(payloads[p.name])
        p=root/'README.md';p.unlink()
        check(mode+' missing member',command(opts=opts),False,diagnostic='strict root inventory mismatch')
        p.write_bytes(payloads[p.name]);p.unlink();p.symlink_to(shadow/'json.py')
        check(mode+' symlink member',command(opts=opts),False,diagnostic='symlink path forbidden');p.unlink();p.write_bytes(payloads[p.name])
        p=root/'README.md';p.unlink();p.mkdir()
        check(mode+' directory replacing member',command(opts=opts),False,diagnostic='expected regular file');p.rmdir();p.write_bytes(payloads[p.name])
        p=root/'README.md';p.unlink();os.mkfifo(p)
        check(mode+' FIFO replacing member',command(opts=opts),False,diagnostic='expected regular file');p.unlink();p.write_bytes(payloads[p.name])
        link=t/('link_'+mode);link.symlink_to(root,target_is_directory=True)
        check(mode+' symlink root',command(r=link,opts=opts),False,diagnostic='symlink path forbidden')
        outer=t/('outer_'+mode);outer.symlink_to(t,target_is_directory=True)
        check(mode+' symlink root ancestor',command(r=outer/root.name,opts=opts),False,diagnostic='symlink path forbidden')
        alink=t/('archive_'+mode);alink.symlink_to(a)
        check(mode+' symlink archive',command(ar=alink,opts=opts),False,diagnostic='symlink path forbidden')
        mlink=t/('manifest_'+mode);mlink.symlink_to(m)
        check(mode+' symlink manifest',command(ma=mlink,opts=opts),False,diagnostic='symlink path forbidden')
        bad=t/('tampered_'+mode+'.zip');bad.write_bytes(a.read_bytes()+b'corruption')
        check(mode+' archive corruption',command(ar=bad,opts=opts),False,diagnostic='archive digest mismatch')
        bm=t/('tampered_'+mode+'.json');bm.write_bytes(m.read_bytes()+b' ')
        check(mode+' manifest corruption',command(ma=bm,opts=opts),False,diagnostic='pinned external manifest mismatch')
        check(mode+' archive path within root',command(ar=root/'PROOF.md',opts=opts),False,diagnostic='must be external')
        check(mode+' manifest path within root',command(ma=root/'README.md',opts=opts),False,diagnostic='must be external')
        check(mode+' direct checker', [sys.executable,*opts,str(root/'verify_math.py')],False,diagnostic='Direct execution/import forbidden')
        code='import runpy;runpy.run_path('+repr(str(root/'verify_math.py'))+')'
        check(mode+' runpy checker entrypoint', [sys.executable,*opts,'-c',code],False,diagnostic='Direct execution/import forbidden')
        check(mode+' restored baseline',command(opts=opts),True)
        require(not marker.exists(), 'malicious marker created')
    for opts in ((),('-I',),('-S',),('-O',),('-S','-O')):
        check('startup flags '+repr(opts),command(opts=opts),False,diagnostic='Use python -I -S')
    check('missing command arguments',[sys.executable,'-I','-S',str(boot)],False,diagnostic='usage: bootstrap')
    require(set(p.name for p in root.iterdir())==set(payloads),'cache or other file created in root')
    require(not (t/'externalcache').exists(),'PYTHONPYCACHEPREFIX not ignored')
    records.append({'test':'all malicious execution markers and cache side effects absent','result':'PASS'})
out={'problem_id':30002439,'independent':True,'input_archive_sha256':expected_zip,'control_count':len(records),'all_controls_passed':True,'controls':records,'scope':'Validation of pinned original author packet; finite checks and startup/inventory controls only'}
dest=destination
dest.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(json.dumps({'result':'PASS','control_count':len(records),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},sort_keys=True))
