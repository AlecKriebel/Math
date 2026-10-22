"""Reproduce static directory preflight and meaningful hardlink controls privately."""
from pathlib import Path
import subprocess,shutil,os,json,hashlib,datetime
P=Path(__file__).absolute().parent
R=P/'private/release'
D=P/'private/extra-controls';D.mkdir(exist_ok=True)
N=['output/mixed-kato-counterexample-source-and-verification.zip','output/zenodo-upload-kit.zip','PACKAGE_RECEIPT.json']
def snapshot(p):
 st=p.stat()
 out={'inode':st.st_ino,'mtime_ns':st.st_mtime_ns,'is_directory':p.is_dir()}
 if p.is_file():
  b=p.read_bytes();out.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 return out
rows=[]
for optimized in [False,True]:
 for kind in ['directory','hardlink']:
  for i,n in enumerate(N):
   name=f'{kind}-{i}-{optimized}';root=D/name;outside=D/(name+'-outside');shutil.copytree(R,root);outside.mkdir()
   if kind=='directory':
    for other in N:(root/other).write_bytes(('PREEXISTING-'+other).encode())
    (root/n).unlink();(root/n).mkdir()
   else:
    (outside/'sentinel').write_bytes(b'PRIVATE HARDLINK SENTINEL: different from every generated payload\x00\xff')
    (root/n).unlink();os.link(outside/'sentinel',root/n)
   before={k:snapshot(root/k) for k in N};outside_before=snapshot(outside/'sentinel') if kind=='hardlink' else None
   proc=subprocess.run(['python3','-B',*(['-O'] if optimized else []),'build_package.py'],cwd=root,capture_output=True,timeout=30)
   after={k:snapshot(root/k) for k in N};outside_after=snapshot(outside/'sentinel') if kind=='hardlink' else None
   changes={k:{'content_changed':before[k].get('sha256')!=after[k].get('sha256'),'inode_changed':before[k]['inode']!=after[k]['inode'],'mtime_changed':before[k]['mtime_ns']!=after[k]['mtime_ns']} for k in N}
   row={'case':kind,'destination':n,'optimized':optimized,'exit':proc.returncode,'last_stderr':proc.stderr.decode().splitlines()[-1] if proc.stderr else '', 'before':before,'after':after,'changes':changes,'outside_before':outside_before,'outside_after':outside_after}
   if kind=='hardlink':
    row['outside_preserved']=outside_before==outside_after;row['output_matches_frozen']=all((root/k).read_bytes()==(R/k).read_bytes() for k in N)
    assert proc.returncode==0 and row['outside_preserved'] and row['output_matches_frozen'] and changes[n]['inode_changed']
   else:assert proc.returncode!=0
   rows.append(row);shutil.rmtree(root);shutil.rmtree(outside)
(P/'EXTRA_PATH_CONTROLS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(rows),'controls':rows},indent=2)+'\n')
print(json.dumps([{'case':x['case'],'destination':x['destination'],'optimized':x['optimized'],'exit':x['exit'],'changed_content':[k for k,v in x['changes'].items() if v['content_changed']],'outside_preserved':x.get('outside_preserved')} for x in rows],indent=2))
