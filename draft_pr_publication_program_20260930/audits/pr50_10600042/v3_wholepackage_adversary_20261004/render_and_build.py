from pathlib import Path
import subprocess,json,datetime,hashlib,shutil
a=Path(__file__).resolve().parent
source=a.parent/'current_promotion_adversary_20261004/private'
p=a.parent/'publication_package_v3'
out=a/'private/renders';out.mkdir(exist_ok=True)
def run(name,argv,cwd=a):
    b=a/'private/commands'/name;start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with b.with_suffix('.stdout').open('wb') as stdout,b.with_suffix('.stderr').open('wb') as stderr:
        child=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr);rc=child.wait()
    rec={'argv':argv,'cwd':str(cwd),'pid':child.pid,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':rc,'stdin':'empty; DEVNULL'}
    b.with_suffix('.json').write_text(json.dumps(rec,indent=2)+'\n');b.with_suffix('.stdin').write_bytes(b'')
    print(name,json.dumps(rec),b.with_suffix('.stdout').read_text(),b.with_suffix('.stderr').read_text())
    assert rc==0
run('render_submission',['pdftoppm','-scale-to','1600','-png',str(p/'even_strand_markov.pdf'),str(out/'v3')])
for name,first,last in [('kamada',4,7),('kl',30,30),('gks',5,5),('survey',34,34),('survey_publisher_correct',29,29)]:
    run('render_primary_'+name,['pdftoppm','-f',str(first),'-l',str(last),'-scale-to','1800','-png',str(source/(name+'.pdf')),str(out/name)])
run('pdfinfo_submission',['pdfinfo',str(p/'even_strand_markov.pdf')])
build=a/'private/build';build.mkdir(exist_ok=True)
shutil.copyfile(p/'even_strand_markov.tex',build/'even_strand_markov.tex')
run('tectonic_rebuild',['tectonic','--keep-logs','even_strand_markov.tex'],build)
run('render_rebuild',['pdftoppm','-scale-to','1600','-png',str(build/'even_strand_markov.pdf'),str(out/'rebuild')])
submission=sorted(out.glob('v3-*.png'));rebuilt=sorted(out.glob('rebuild-*.png'))
assert len(submission)==len(rebuilt)==5
for x,y in zip(submission,rebuilt):
    assert x.read_bytes()==y.read_bytes(),(x,y)
print('all five rebuilt page PNGs byte-identical')
print('rebuilt PDF sha256',hashlib.sha256((build/'even_strand_markov.pdf').read_bytes()).hexdigest())
