import pathlib,subprocess,tempfile,shutil,json,hashlib,os
root=pathlib.Path(__file__).resolve().parent
outputs=[]
def run(d,args,label,expect=0):
 p=subprocess.run(['python','-B']+args,cwd=d,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 # Paths in exceptions are portable command-relative names, not private temp directories.
 stdout=p.stdout.replace(str(d),'.');stderr=p.stderr.replace(str(d),'.')
 outputs.append({'label':label,'command':['python','-B']+args,'returncode':p.returncode,'stdout':stdout,'stderr':stderr,'expected':'success' if expect==0 else 'failure'})
 if (p.returncode==0)!=(expect==0):raise RuntimeError('unexpected outcome '+label)
def inventory(d):
 rows=[]
 for p in sorted(d.rglob('*')):
  if p.is_file() and p.relative_to(d).as_posix()!='INVENTORY.json':
   b=p.read_bytes();rows.append({'path':p.relative_to(d).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 (d/'INVENTORY.json').write_text(json.dumps({'algorithm':'sha256','excludes':['INVENTORY.json'],'files':rows},indent=2)+'\n')
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td)/'package';shutil.copytree(root,d)
 for mode in [[],['-O']]:
  for script in ['exact_check.py','independent_audit.py','structure_checks.py']:
   run(d,mode+[script],('optimized ' if mode else 'normal ')+script)
  for name in ['exact_results.json','INDEPENDENT_CHECKS.json']:
   if (d/name).read_bytes()!=(root/name).read_bytes():raise RuntimeError('reproduction mismatch '+name)
 # Real mathematical program mutations, each run in both modes against its direct bounded checks.
 original=(d/'structure_checks.py').read_text()
 mutations={
 'threshold':('return d>=t and','return d>t and'),
 'oddpart':('return x\ndef power_count','return 1\ndef power_count'),
 'power_paths':('return min(L,q-1)+','return 1+min(L,q-1)+'),
 'transfer_edges':('return low%c==0','return False'),
 'cycle_mean':('return max(means)','return max(means)+1')}
 for label,(old,new) in mutations.items():
  if original.count(old)!=1:raise RuntimeError('mutation target not unique')
  (d/'structure_checks.py').write_text(original.replace(old,new))
  for mode in [[],['-O']]:run(d,mode+['structure_checks.py'],'mutation '+label+(' optimized' if mode else ' normal'),1)
 (d/'structure_checks.py').write_text(original)
 # Guard perturbation directly exercises rewritten witness and independent guards.
 data=json.loads((d/'exact_results.json').read_text());data[0]['maximum']+=1;(d/'exact_results.json').write_text(json.dumps(data))
 for mode in [[],['-O']]:run(d,mode+['independent_audit.py'],'corrupt witness count'+(' optimized' if mode else ' normal'),1)
 shutil.copyfile(root/'exact_results.json',d/'exact_results.json')
 # inventory controls on a temporary full copy; transcript is added only after controls finish.
 inventory(d)
 for mode in [[],['-O']]:run(d,mode+['verify_inventory.py'],'baseline inventory'+(' optimized' if mode else ' normal'))
 def test_inv(label,change,undo):
  change()
  for mode in [[],['-O']]:run(d,mode+['verify_inventory.py'],label+(' optimized' if mode else ' normal'),1)
  undo()
 p=d/'nested'/'unexpected.txt'
 test_inv('recursive extra file',lambda:(p.parent.mkdir(),p.write_text('extra')),lambda:(p.unlink(),p.parent.rmdir()))
 p=d/'nested'/'INVENTORY.json'
 test_inv('nested manifest extra file',lambda:(p.parent.mkdir(),p.write_text('{}')),lambda:(p.unlink(),p.parent.rmdir()))
 p=d/'README.md';b=p.read_bytes()
 test_inv('missing file',lambda:p.unlink(),lambda:p.write_bytes(b))
 test_inv('byte mutation',lambda:p.write_bytes(b+b'x'),lambda:p.write_bytes(b))
 p=d/'unexpected_link'
 test_inv('symlink',lambda:p.symlink_to('README.md'),lambda:p.unlink())
(root/'COMMAND_OUTPUTS.json').write_text(json.dumps({'scope':'Full outputs of direct normal and optimized runs, mathematical mutations, explicit-guard rejection, and recursive inventory controls. Temporary paths normalized.','runs':outputs},indent=2)+'\n')
inventory(root)
# Final output outside inventory avoids circular hash dependencies.
final=[]
for mode in [[],['-O']]:
 p=subprocess.run(['python','-B']+mode+['verify_inventory.py'],cwd=root,text=True,capture_output=True)
 final.append({'command':['python','-B']+mode+['verify_inventory.py'],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 if p.returncode:raise RuntimeError(p.stderr)
b=(root/'INVENTORY.json').read_bytes()
receipt={'package':'package/divisible_difference_sets_2225','state':'frozen for independent audit; no publication','inventory_sha256':hashlib.sha256(b).hexdigest(),'inventory_bytes':len(b),'files':len(json.loads(b)['files']),'full_command_log_sha256':hashlib.sha256((root/'COMMAND_OUTPUTS.json').read_bytes()).hexdigest(),'final_inventory_runs':final}
print(json.dumps(receipt,indent=2))
