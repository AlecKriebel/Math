"""Read-only candidate replay in private copies; complete outputs are public receipts."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,shutil,hashlib,json,os,time
ROOT=Path('/Users/alec/Documents/Math'); OWN=ROOT/'draft_pr_descending_audit_20261002/audits/pr367_11000151/clean_final_adversary'; PREFIX='problems/11000151_artin_a5_quotient'; HEAD='d977c9564f079cde975a7b4261776eb9061c5f5f'
PYTHON=ROOT/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
files=subprocess.check_output(['git','ls-tree','-r','--name-only',HEAD,'--',PREFIX],cwd=ROOT).decode().splitlines();out=OWN/'fullstreams';out.mkdir(exist_ok=True)
rows=[]
def run(label,command,cwd):
 start=datetime.now(timezone.utc).isoformat(); stamp=time.monotonic();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 with (out/(label+'.stdout')).open('wb') as stdout,(out/(label+'.stderr')).open('wb') as stderr:
  r=subprocess.run(list(map(str,command)),cwd=cwd,stdout=stdout,stderr=stderr,env=env)
 row={'label':label,'command':list(map(str,command)),'start_utc':start,'elapsed_seconds':time.monotonic()-stamp,'exit_code':r.returncode}
 for stream in ['stdout','stderr']:
  b=(out/(label+'.'+stream)).read_bytes();row[stream]={'path':'fullstreams/'+label+'.'+stream,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 rows.append(row);(OWN/'receipts/replays.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,flush=True)
 return row
scripts=['check_turn_1.py','check_turn_2.py','check_turn_3.py','check_turn_4.py','verify_turn_4_cpp.py','review/independent_check.py','review/replay_author.py','verify_publication.py']
for mode in ['without_sources','with_sources']:
 packet=OWN/'private_runtime'/mode;packet.mkdir(parents=True,exist_ok=True)
 for f in files:
  rel=Path(f).relative_to(PREFIX);dest=packet/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(subprocess.check_output(['git','show',HEAD+':'+f],cwd=ROOT))
 if mode=='with_sources':
  source=packet/'source';source.mkdir(exist_ok=True)
  for src,dst in [('mcgbook.pdf','mcgbook.pdf'),('arxiv_1412.0352.pdf','positive-factorizations.pdf'),('agt-v17-n3-p06-s.pdf','positive-factorizations-published.pdf'),('basic-braids.pdf','basic-braids.pdf')]:shutil.copyfile(OWN/'private_sources'/src,source/dst)
 for script in scripts:
  label=mode+'_'+script.replace('/','_').replace('.py','');args=[PYTHON,packet/script]
  if script=='review/replay_author.py':args.append(packet)
  run(label,args,packet)
 exe=packet/'compiled_cpp';run(mode+'_cpp_compile',['g++','-O3','-std=c++17',packet/'check_turn_4.cpp','-o',exe],packet)
 run(mode+'_cpp_plain',[exe],packet);run(mode+'_cpp_stream',[exe,'--stream'],packet)
print('COMPLETE',flush=True)
