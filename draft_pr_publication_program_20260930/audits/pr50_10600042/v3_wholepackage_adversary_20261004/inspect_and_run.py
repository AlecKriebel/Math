from pathlib import Path
import zipfile, json, hashlib, subprocess, sys, datetime, shutil
a=Path(__file__).resolve().parent
p=a.parent/'publication_package_v3'
dest=a/'private/extracted'
dest.mkdir(exist_ok=True)
with zipfile.ZipFile(p/'even-strand-markov-verification-v3.zip') as z:
    for member in z.infolist():
        assert Path(member.filename).name==member.filename
        assert not member.is_dir()
        (dest/member.filename).write_bytes(z.read(member))
for name in ['verify_even_calculus.py','build_verification_zip.py','expected_results.json','VERIFICATION_RECORD.json','README.md','SOURCE_QUALIFICATIONS.md','LICENSE-TEXT.md','LICENSE-CODE.txt','SHA256SUMS']:
    print('\nFILE',name,'\n', (dest/name).read_text())
for name in ['zenodo-deposit.json','ACTUAL_RUN_AND_MATERIALS.json','REVISION_PREPARATION.json']:
    print('\nPACKAGE FILE',name,'\n',(p/name).read_text())
for line in (dest/'SHA256SUMS').read_text().splitlines():
    h,n=line.split('  ')
    assert hashlib.sha256((dest/n).read_bytes()).hexdigest()==h
assert (dest/'even_strand_markov.tex').read_bytes()==(p/'even_strand_markov.tex').read_bytes()
def execute(name,argv,cwd):
    b=a/'private/commands'/name
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with b.with_suffix('.stdout').open('wb') as out,b.with_suffix('.stderr').open('wb') as err:
        child=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
        rc=child.wait()
    rec={'argv':argv,'cwd':str(cwd),'pid':child.pid,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':rc,'stdin':'empty; DEVNULL'}
    b.with_suffix('.json').write_text(json.dumps(rec,indent=2)+'\n')
    b.with_suffix('.stdin').write_bytes(b'')
    print(name,json.dumps(rec),b.with_suffix('.stdout').read_text(),b.with_suffix('.stderr').read_text())
    return rc
assert execute('actual_zip_checker_corrected',[sys.executable,'-B',str(dest/'verify_even_calculus.py')],dest)==0
(dest/'actual_results.json').write_bytes((a/'private/commands/actual_zip_checker_corrected.stdout').read_bytes())
assert (dest/'actual_results.json').read_bytes()==(dest/'expected_results.json').read_bytes()
assert execute('actual_zip_builder',[sys.executable,str(dest/'build_verification_zip.py')],dest)==0
rebuilt=dest/'even-strand-markov-verification-v3.zip'
assert rebuilt.read_bytes()==(p/rebuilt.name).read_bytes()
print('ACTUAL checker result sha256',hashlib.sha256((dest/'actual_results.json').read_bytes()).hexdigest())
