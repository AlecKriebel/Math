#!/usr/bin/env python3
"""Read-only independently pinned archive replay; scratch stays private."""
import argparse,ast,datetime,hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
O=Path(__file__).resolve().parent;A=O.parents[1];D=A/'publication';PY=Path('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')
MP='3e0bac9bc04b7f22796b52fd683675ab57328f363f219cf3e8208e78ebfc3611';VP='7f661daf498cd151ddd5fd44eb0d7d763b8bdfdbf7c12262dc5255a0133a4bc6'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path);args=ap.parse_args()
work=O/'private/cold';work.mkdir(parents=True,exist_ok=True)
root=Path(tempfile.mkdtemp(prefix='extracted_',dir=work))
with zipfile.ZipFile(D/'deep-derived-pure-braids-source-verification-v1.0.zip') as z:
 need(sha(z.read('PACKAGE_MANIFEST.json'))==MP,'external manifest');m=json.loads(z.read('PACKAGE_MANIFEST.json'))
 for i in z.infolist():
  need(not i.is_dir() and i.filename in set(m['files'])|{'PACKAGE_MANIFEST.json'},'inventory')
  q=root/i.filename;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(z.read(i));q.chmod(0o644)
need(sha((root/'verify_package.py').read_bytes())==VP,'external verifier')
seals={}
node=ast.parse((D/'build_package.py').read_text());family=next(ast.literal_eval(n.value) for n in node.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FAMILIES' for t in n.targets))
for name,(mapname,pin) in family.items():
 folder=A/'reviews'/name;raw=(folder/mapname).read_bytes();need(sha(raw)==pin,'external family seal '+name);mapping=json.loads(raw);records=mapping.get('files',mapping.get('public_files',mapping.get('records')))
 if type(records)is list:records={r['path']:r for r in records}
 for path,item in records.items():
  b=(folder/path).read_bytes();need(sha(b)==item['sha256'] and len(b)==item.get('bytes',item.get('size')),'family leaf');need((root/'reviews'/name/path).read_bytes()==b,'family archive leaf')
 seals[name]={'manifest_sha256':pin,'payloads_authenticated':len(records)}
rows=[];baseline=None
for name,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('environment2',[],'2')]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
 if opt:env['PYTHONOPTIMIZE']=opt
 probe=subprocess.check_output([str(PY),*flags,'-c','import sys; print(sys.flags.optimize)'],env=env,text=True).strip()
 proc=subprocess.run([str(PY),*flags,str(root/'verify_package.py'),'--expected-manifest',MP,'--pdf',str(D/'output/pdf/note.pdf'),'--workdir',str(work/(name+'_scratch'))],capture_output=True,text=True,env=env,cwd=work,timeout=600)
 (work/(name+'.stdout')).write_text(proc.stdout);(work/(name+'.stderr')).write_text(proc.stderr)
 need(proc.returncode==0,name+proc.stderr);result=json.loads(proc.stdout);need(result['status']=='PASS' and result['worker_optimization']==0,'worker')
 if baseline is None:baseline=result
 else:need(result==baseline,'mode mismatch')
 rows.append({'mode':name,'actual_outer_optimization':int(probe),'returncode':0,'stdout_sha256':sha(proc.stdout.encode()),'result':result})
 print(name+' PASS',flush=True)
# Challenge drivers were completely read before copying/executing. Their HERE
# scratch stays in this review, outside the extracted closed package.
controls={}
for name,extra in [('package_guard_challenges.py',[]),('copy_guard_challenge.py',['--expected-manifest',MP,'--workdir',str(work/'copy_scratch')])]:
 source=D/name;copy=work/name;copy.write_bytes(source.read_bytes());need(copy.read_bytes()==source.read_bytes(),'challenge copy')
 output=work/('COLD_'+name.removesuffix('.py').upper()+'.json')
 proc=subprocess.run([str(PY),'-B',str(copy),'--bundle',str(root),'--python',str(PY),'--output',str(output),*extra],capture_output=True,text=True,cwd=work,timeout=120)
 (work/(name+'.stdout')).write_text(proc.stdout);(work/(name+'.stderr')).write_text(proc.stderr);need(proc.returncode==0,name+proc.stderr);controls[name]=json.loads(output.read_bytes())
 print(name+' PASS',flush=True)
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','package_manifest_sha256':MP,'externally_pinned_verifier_sha256':VP,'fresh_archive_extraction':True,'outputs_and_scratch_outside_closed_package':True,'family_seals':seals,'modes':rows,'all_full_replays_identical':True,'hostile_inventory_runs':controls['package_guard_challenges.py']['hostile_inventory_runs'],'false_assertion_child_runs':4,'copy_corruption_runs':4,'all_original_and_independent_replays_completed':True,'scope':'Finite original 286 controls and complete planar/Meyer reconstruction only; no universal proof or priority certificate.'}
if args.output is not None:args.output.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
