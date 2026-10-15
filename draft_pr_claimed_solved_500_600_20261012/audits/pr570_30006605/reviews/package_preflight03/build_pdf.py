#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess
H=Path(__file__).resolve().parent;P=H.parent.parent/'publication';C=H/'.cache/pdfbuild';C.mkdir(parents=True,exist_ok=True)
shutil.copy2(P/'weighted_centers.tex',C/'weighted_centers.tex')
profile='(version 1)(allow default)(deny network*)(deny file-write*)(allow file-write* (subpath "'+str(H)+'") (literal "/dev/null"))'
env=dict(os.environ,SOURCE_DATE_EPOCH='1792022400',TMPDIR=str(C))
p=subprocess.run(['/usr/bin/sandbox-exec','-p',profile,'/opt/homebrew/bin/tectonic','--only-cached','--outdir',str(C),str(C/'weighted_centers.tex')],cwd=C,env=env,capture_output=True,text=True)
(H/'PDF_BUILD.stdout.txt').write_text(p.stdout);(H/'PDF_BUILD.stderr.txt').write_text(p.stderr)
assert p.returncode==0,(p.returncode,p.stderr,p.stdout)
b=(C/'weighted_centers.pdf').read_bytes();assert b==(P/'weighted_centers.pdf').read_bytes()
result={'status':'PASS','compiler':subprocess.check_output(['/opt/homebrew/bin/tectonic','--version'],text=True).strip(),'source_date_epoch':1792022400,'network_denied':True,'only_cached':True,'writes_restricted_to_review_folder':True,'pdf_sha256':hashlib.sha256(b).hexdigest(),'pdf_bytes':len(b),'byte_identical':True,'editor_changed':False,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(H/'PDF_BUILD_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
R=H/'.cache/render';R.mkdir(exist_ok=True)
p=subprocess.run(['/opt/homebrew/bin/pdftoppm','-r','110','-png',str(P/'weighted_centers.pdf'),str(R/'publication')],capture_output=True,text=True)
assert p.returncode==0,p.stderr
print(json.dumps(result,indent=2))
