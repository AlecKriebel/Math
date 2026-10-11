from pathlib import Path
import subprocess,sys,json,datetime,hashlib
a=Path(__file__).resolve().parent
name=sys.argv[1]; script=Path(sys.argv[2]).resolve(); args=sys.argv[3:]
b=a/'private/commands'/name
b.with_suffix('.source.py').write_bytes(script.read_bytes())
b.with_suffix('.stdin').write_bytes(b'')
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with b.with_suffix('.stdout').open('wb') as out,b.with_suffix('.stderr').open('wb') as err:
 p=subprocess.Popen([sys.executable,str(script),*args],stdout=out,stderr=err,cwd=a,stdin=subprocess.DEVNULL)
 code=p.wait()
record={'argv':[sys.executable,str(script),*args],'cwd':str(a),'pid':p.pid,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':code,'source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'stdin_sha256':hashlib.sha256(b'').hexdigest()}
b.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record));print(b.with_suffix('.stdout').read_text());print(b.with_suffix('.stderr').read_text())
sys.exit(code)
