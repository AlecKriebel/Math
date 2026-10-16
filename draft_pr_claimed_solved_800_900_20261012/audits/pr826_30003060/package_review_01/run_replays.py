from pathlib import Path
import concurrent.futures,subprocess,sys,time,json,datetime,hashlib
OWN=Path(__file__).resolve().parent
ROOT=OWN/'replays/sealed_assembly'
OUTER='c43861f2fe0e0282f49833dcd26b3d28cbee0e202653dbeb2b154a6cc86b027b'
PIN='e5122815c93723664c499a2c8c90d1bf01423f4ab522998416fb2effaa950181'
PRE=ROOT/'publication_20261014/preprint';INNER=ROOT/'publication_20261014/verification_package'
plans=[]
for mode,extra in [('NORMAL',[]),('OPTIMIZED',['-O'])]:
 flags=['-I','-S','-B',*extra]
 if mode=='OPTIMIZED':plans.append(('OUTER_'+mode,[sys.executable,*flags,str(ROOT/'verify_publication.py'),OUTER,'--full'],'/'))
 plans.append(('PORTABLE_'+mode,[sys.executable,*flags,str(INNER/'verify_package.py'),PIN,'--full'],str(INNER)))
 plans.append(('BUILDER_'+mode,[sys.executable,*flags,'build_verification.py','--from-package','../verification_package','--trusted-index-sha256',PIN,'--output-root',str(OWN/'replays'/('rebuilt_'+mode.lower()))],str(PRE)))
plans.append(('ROOT_CONTROLS',[sys.executable,'-I','-S','-B',str(OWN/'replays/root_controls/check_release_integrity_controls.py'),'--label','r1'],'/'))
def run(plan):
 name,cmd,cwd=plan;t=time.monotonic();p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=1200)
 (OWN/'receipts'/f'{name}.stdout.json').write_text(p.stdout);(OWN/'receipts'/f'{name}.stderr.txt').write_text(p.stderr)
 d={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':cwd,'returncode':p.returncode,'elapsed_seconds':time.monotonic()-t,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr':p.stderr}
 if name.startswith('BUILDER') and p.returncode==0:
  output=OWN/'replays'/('rebuilt_'+name.split('_')[1].lower())
  d['byte_exact']={n:(output/n).read_bytes()==(PRE/n).read_bytes() for n in ['package_index.json','verification.zip']}
 (OWN/'receipts'/f'{name}.json').write_text(json.dumps(d,indent=2)+'\n');return {'name':name,**d}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for d in pool.map(run,plans):print(json.dumps(d),flush=True)
