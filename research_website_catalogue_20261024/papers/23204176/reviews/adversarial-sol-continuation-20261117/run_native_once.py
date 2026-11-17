"""Single unmodified ordinary route in a byte-identical isolated input copy."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, shutil, stat, subprocess, sys, time
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');A=P/'papers/23204176/reviews/adversarial-sol-continuation-20261117'
S=P/'papers/23204176/sources/archives/01-source-and-verification.zip.extracted';D=A/'native-isolated'
def snap(root):
    out={}
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();n='.' if p==root else str(p.relative_to(root));row={'mode':oct(stat.S_IMODE(st.st_mode))}
        if p.is_dir():row.update(kind='directory',empty=not any(p.iterdir()))
        elif p.is_file():
            b=p.read_bytes();row.update(kind='file',bytes=len(b),SHA256=hashlib.sha256(b).hexdigest())
        else:raise AssertionError('Nonregular native input '+n)
        out[n]=row
    return out
assert not D.exists() and not (A/'NATIVE_RUN.json').exists()
source_before=snap(S);shutil.copytree(S,D);copy_before=snap(D);assert source_before==copy_before
(A/'NATIVE_INPUT_BEFORE.json').write_text(json.dumps({'source':source_before,'isolated':copy_before},indent=2)+'\n')
temp=A/'native-temporary';temp.mkdir();env=os.environ.copy();env['TMPDIR']=str(temp)
argv=[sys.executable,str(D/'reproduce.py')];start=datetime.now(timezone.utc).isoformat();t=time.monotonic()
r=subprocess.run(argv,cwd=D,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);elapsed=time.monotonic()-t
(A/'NATIVE.stdout.bin').write_bytes(r.stdout);(A/'NATIVE.stderr.bin').write_bytes(r.stderr)
source_after=snap(S);copy_after=snap(D)
unchanged=source_after==source_before and all(copy_after.get(k)==v for k,v in copy_before.items() if k!='.')
(A/'NATIVE_INPUT_AFTER.json').write_text(json.dumps({'source':source_after,'isolated':copy_after,'all_original_inputs_exact':unchanged},indent=2)+'\n')
report={'start_UTC':start,'end_UTC':datetime.now(timezone.utc).isoformat(),'argv':argv,'cwd':str(D),'Python_executable':sys.executable,'elapsed_seconds':elapsed,'exit':r.returncode,
    'stdout_bytes':len(r.stdout),'stdout_SHA256':hashlib.sha256(r.stdout).hexdigest(),'stderr_bytes':len(r.stderr),'stderr_SHA256':hashlib.sha256(r.stderr).hexdigest(),
    'source_and_original_isolated_inputs_unchanged':unchanged,'attempts':1,'repairs_retries_interpreter_switches_installs':0,'scope':'Finite native checks and ordinary build only; not geometric algebraicity'}
(A/'NATIVE_RUN.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if r.returncode or not unchanged:sys.exit(1)
