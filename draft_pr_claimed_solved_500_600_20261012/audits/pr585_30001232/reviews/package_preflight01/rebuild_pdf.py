import pathlib, os, subprocess, json, hashlib
R=pathlib.Path(__file__).resolve().parent; A=R.parent.parent; P=A/'publication'; D=R/'.cache/tex'
(D/'seshadri_counterexample.tex').write_bytes((P/'seshadri_counterexample.tex').read_bytes())
env=dict(os.environ,SOURCE_DATE_EPOCH='1792022400',TMPDIR=str(R/'.cache/tmp'),PYTHONDONTWRITEBYTECODE='1')
cmd=['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)','/opt/homebrew/bin/tectonic','--only-cached','seshadri_counterexample.tex']
p=subprocess.run(cmd,cwd=D,env=env,capture_output=True,text=True)
(R/'PDF_REBUILD.stdout.txt').write_text(p.stdout); (R/'PDF_REBUILD.stderr.txt').write_text(p.stderr)
assert p.returncode==0,(p.stdout,p.stderr)
pdf=(D/'seshadri_counterexample.pdf').read_bytes(); expected=(P/'seshadri_counterexample.pdf').read_bytes()
assert pdf==expected
info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(D/'seshadri_counterexample.pdf')],capture_output=True,text=True,check=True).stdout
subprocess.run(['/opt/homebrew/bin/pdftoppm','-r','120','-png',str(D/'seshadri_counterexample.pdf'),str(R/'.cache/rendered/page')],check=True,capture_output=True)
subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(D/'seshadri_counterexample.pdf'),str(R/'.cache/paper.txt')],check=True,capture_output=True)
(R/'PDF_REBUILD.json').write_text(json.dumps({'status':'PASS','command':cmd,'compiler_version':subprocess.check_output(['/opt/homebrew/bin/tectonic','--version'],text=True).strip(),'SOURCE_DATE_EPOCH':env['SOURCE_DATE_EPOCH'],'pdf_bytes':len(pdf),'pdf_sha256':hashlib.sha256(pdf).hexdigest(),'byte_identical':True,'os_network_denied':True,'pdfinfo':info,'rendered_pages':[p.name for p in sorted((R/'.cache/rendered').glob('page-*.png'))],'visual_inspection_completed':False},indent=2)+'\n')
print(info)
