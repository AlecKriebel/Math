"""Reviewer-owned command recorder; inputs remain read-only and outputs stay here."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
R=Path(__file__).resolve().parent
A=R.parent
PYTHON='/opt/homebrew/opt/python@3.14/bin/python3.14'
BASE=[PYTHON,'-E','-S','-B','-P']
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(label,argv,cwd=A,source_paths=(),save=True,env_extra=None):
    start=stamp(); env=dict(os.environ);env['TMPDIR']=str(R/'temp');(R/'temp').mkdir(exist_ok=True)
    if env_extra:env.update(env_extra)
    p=subprocess.run([str(x) for x in argv],cwd=cwd,capture_output=True,env=env)
    receipt={'UTC_start':start,'UTC_end':stamp(),'actual_argv':[str(x) for x in argv],'cwd':str(cwd),'exit':p.returncode,'sources':{str(x):digest(Path(x).read_bytes()) for x in source_paths},'stdout':digest(p.stdout),'stderr':digest(p.stderr)}
    if save:
        (R/(label+'.stdout')).write_bytes(p.stdout);(R/(label+'.stderr')).write_bytes(p.stderr)
    (R/(label+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'label':label,'exit':p.returncode,'stdout':receipt['stdout'],'stderr':receipt['stderr']}),flush=True)
    return p

def main():
    proof=A/'publication_package_v2/verification'
    sources=list((proof/'current').glob('*.py'))
    for opt in (False,True):
        for name in ('check_manifest.py','current/run_verification.py'):
            label=('optimized_' if opt else 'normal_')+Path(name).stem
            r=run(label,BASE+(['-O'] if opt else [])+[proof/name],proof,[proof/name]+sources)
            if r.returncode:raise RuntimeError(label+' failed: '+r.stderr.decode(errors='replace'))
    for name in ('independent_exact.py','independent_face_word.py','independent_double_pentagon.py'):
        r=run('ordinary_'+Path(name).stem,BASE+[proof/'independent'/name],proof,[proof/'independent'/name])
        if r.returncode:raise RuntimeError(name+' failed')
    render=R/'render';render.mkdir(exist_ok=True)
    tex=A/'publication_package_v2/dodecahedron_endpoint.tex'
    r=run('cached_tectonic',['/opt/homebrew/bin/tectonic','--only-cached','--keep-logs','--outdir',render,tex],R,[tex])
    if r.returncode:raise RuntimeError('compile failed')
    pdf=render/'dodecahedron_endpoint.pdf'
    for label,p in [('supplied',A/'publication_package_v2/dodecahedron_endpoint.pdf'),('rebuilt',pdf)]:
        r=run(label+'_pdfinfo',['/opt/homebrew/bin/pdfinfo',p],R,[p])
        r=run(label+'_pdftotext',['/opt/homebrew/bin/pdftotext','-layout',p,'-'],R,[p])
        r=run(label+'_render',['/opt/homebrew/bin/pdftoppm','-scale-to','1500','-png',p,render/label],R,[p])
        if r.returncode:raise RuntimeError('render failed')
if __name__=='__main__':main()
