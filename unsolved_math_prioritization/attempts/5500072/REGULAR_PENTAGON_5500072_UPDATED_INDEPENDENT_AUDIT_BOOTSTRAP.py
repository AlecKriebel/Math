#!/usr/bin/env python3
"""Pinned audit ZIP verification and unrelated-directory isolated replay; no network."""
import argparse,hashlib,json,pathlib,subprocess,sys,tempfile,zipfile
PREFIX="REGULAR_PENTAGON_5500072_UPDATED_INDEPENDENT_AUDIT_"
EXPECTED_ARCHIVE={'bytes': 42841, 'sha256': '16c162ea9c25dcdceabcef62069bb34b7971278467667c4434cdfcf2c54bcb57'}
def require(x,msg):
 if not x:raise ValueError(msg)
def fp(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def main():
 ap=argparse.ArgumentParser();home=pathlib.Path(__file__).resolve().parent
 ap.add_argument('--archive',type=pathlib.Path,default=home/(PREFIX+'SAFE.zip'));ap.add_argument('--manifest',type=pathlib.Path,default=home/(PREFIX+'EXTERNAL_MANIFEST.json'))
 for n in ['catalog','problems','reports','source-dir']:ap.add_argument('--'+n,type=pathlib.Path)
 args=ap.parse_args();m=json.loads(args.manifest.read_text());raw=args.archive.read_bytes()
 require(m['problem_id']==5500072 and m['archive']==EXPECTED_ARCHIVE,'manifest identity/archive pin');require(fp(raw)==EXPECTED_ARCHIVE,'archive changed')
 require(fp(pathlib.Path(__file__).read_bytes())==m['bootstrap'],'bootstrap changed')
 forwarded=[]
 for name in ['catalog','problems','reports','source_dir']:
  p=getattr(args,name)
  if p is not None:forwarded+=['--'+name.replace('_','-'),str(p.resolve())]
 outputs=[]
 with zipfile.ZipFile(args.archive) as z:
  names=z.namelist();require(len(names)==len(set(names)) and set(names)==set(m['files']),'member inventory')
  require(all(pathlib.PurePosixPath(n).name==n and n not in ['.','..'] and not z.getinfo(n).is_dir() for n in names),'unsafe names')
  require(all((z.getinfo(n).external_attr>>16)&0o170000 !=0o120000 for n in names),'symlink member')
  require(z.testzip() is None,'ZIP CRC')
  for n in names:require(fp(z.read(n))==m['files'][n],'member changed: '+n)
  for optimized in [False,True]:
   with tempfile.TemporaryDirectory(prefix='pentagon audit fresh replay ') as tmp:
    tmp=pathlib.Path(tmp);packet=tmp/'packet';packet.mkdir();cwd=tmp/'unrelated';cwd.mkdir();z.extractall(packet)
    flags=['-I']+(['-O'] if optimized else [])
    run=subprocess.run([sys.executable]+flags+[str(packet/'audit_replay.py')]+forwarded,cwd=cwd,capture_output=True,text=True,timeout=240)
    require(run.returncode==0,'replay failed: '+run.stderr);j=json.loads(run.stdout);require(j['accepted_original_unchanged'] and not j['full_resolution'],'wrong result');outputs.append(j)
    require(sorted(p.name for p in packet.iterdir())==sorted(names),'post-replay inventory')
    for n in names:require(fp((packet/n).read_bytes())==m['files'][n],'post-replay member changed: '+n)
 require(outputs[0]==outputs[1],'normal optimized mismatch')
 print(json.dumps({'problem_id':5500072,'archive_verified':True,'all_members_verified':True,'normal_optimized_identical':True,'replay':outputs[0]},indent=2,sort_keys=True))
if __name__=='__main__':main()
