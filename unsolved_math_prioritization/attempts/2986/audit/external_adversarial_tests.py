from pathlib import Path
import tempfile,os,hashlib,json,subprocess,shutil,argparse
ROOT=Path(__file__).resolve().parent
SAFE=ROOT
parser=argparse.ArgumentParser(description='Adversarially test external input pins using temporary copies; never edit supplied inputs.')
parser.add_argument('--corpus-dir',required=True)
parser.add_argument('--source-dir',required=True)
args=parser.parse_args()
CORPUS=Path(args.corpus_dir).resolve()
SOURCES=Path(args.source_dir).resolve()
cnames=['catalog.json','problems.json','research_results.json']
snames=['k3.pdf','bowden_v3.pdf','christian_menke_v4.pdf','splitting_v1.pdf','flexible_published.pdf','breen_christian_v3.pdf','hozoori.pdf']
rows=[]
with tempfile.TemporaryDirectory(prefix='weinstein relocated sources ') as td:
 base=Path(td);c=base/'corpus inputs';s=base/'public PDFs';c.mkdir();s.mkdir()
 for name in cnames:shutil.copyfile(CORPUS/name,c/name)
 for name in snames:shutil.copyfile(SOURCES/name,s/name)
 for optimized in [False,True]:
  cmd=['python3','-I','-B']+(['-O'] if optimized else [])+[str(SAFE/'verify_audit.py'),'--corpus-dir',str(c),'--source-dir',str(s)]
  def run(name,expected):
   p=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=60)
   if (p.returncode==0)!=expected:raise RuntimeError(name+': unexpected result '+p.stderr)
   rows.append({'case':name,'optimized':optimized,'expected_acceptance':expected,'accepted':p.returncode==0,'returncode':p.returncode,'diagnostic':p.stderr.strip().replace(str(base),'<relocated inputs>'),'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'expected_outcome':True})
  run('relocated full external inputs baseline',True)
  for directory,names,origin in [(c,cnames,CORPUS),(s,snames,SOURCES)]:
   for name in names:
    target=directory/name;original=target.read_bytes();target.unlink()
    changed=bytearray(original);changed[-2]^=1;target.write_bytes(changed)
    run('same-size external corruption: '+name,False)
    target.unlink();shutil.copyfile(origin/name,target)
  for name in ['problems.json']:
   (c/name).unlink();run('missing full corpus input: '+name,False);shutil.copyfile(CORPUS/name,c/name)
  for name in ['christian_menke_v4.pdf']:
   (s/name).unlink();run('missing primary source: '+name,False);shutil.copyfile(SOURCES/name,s/name)
  partial=cmd[:-2]
  p=subprocess.run(partial,cwd='/',capture_output=True,text=True,timeout=60)
  if p.returncode==0:raise RuntimeError('unpaired input dirs accepted')
  rows.append({'case':'only corpus directory supplied','optimized':optimized,'expected_acceptance':False,'accepted':False,'returncode':p.returncode,'diagnostic':p.stderr.strip(),'expected_outcome':True})
print(json.dumps({'external_input_cases':rows,'executions':len(rows),'all_expected_outcomes':True},indent=2,sort_keys=True))
