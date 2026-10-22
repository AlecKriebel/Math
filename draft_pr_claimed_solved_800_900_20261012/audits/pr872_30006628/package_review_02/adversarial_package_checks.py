#!/usr/bin/env python3
"""Independent tiny-fixture attack suite. Never edits or executes changed candidate bytes."""
import hashlib,json,os,runpy,shutil,subprocess,sys,tempfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parents[1]/'work/pr872_revision_r1';PORT=ROOT/'publication_20261015/verification_package'
def require(v,m):
 if not v:raise ValueError(m)
def h(b):return hashlib.sha256(b).hexdigest()
programs={ROOT/'verify_current_publication.py':'57b78a4813329b5964f94879b3fbff796d2e0d1e1298f3889b804117ec06d8fe',PORT/'verify_package.py':'bf4b7f54267ec12bf3ed14bd8ae7410e2e3497943249bdc320bd8108fc9fc9aa',PORT/'check_originals.py':'7e5980d58b749c2e017e860b6f8874267b86833e468d2c287330eaa0cf194318',PORT/'build_verification.py':'94f3250eda9748d99353ac5339226ce3556cd9b7828a909a1fab2be318ef4404'}
for path,pin in programs.items():require(h(path.read_bytes())==pin,'external startup trust failure')
mode='optimized' if sys.flags.optimize else 'normal';flags=['-I','-S','-B']+(['-O'] if sys.flags.optimize else []);records=[]
def record(label,fn,reason=None):
 try:fn()
 except (ValueError,OSError,TypeError,KeyError) as e:
  require(reason is None or reason in str(e),label+' wrong reason: '+str(e));records.append({'case':label,'status':'REJECTED_AS_INTENDED','reason':str(e)});return
 raise ValueError('negative control accepted: '+label)
# The four implementations are separately authenticated before imported execution.
for path in programs:
 g=runpy.run_path(str(path),run_name='authenticated_review_module')
 for label,raw,reason in [('duplicate',b'{"x":1,"x":2}','duplicate JSON key'),('nested_duplicate',b'{"x":{"y":1,"y":2}}','duplicate JSON key'),('nan',b'{"x":NaN}','nonfinite JSON constant'),('infinity',b'{"x":Infinity}','nonfinite JSON constant'),('overflow',b'{"x":1e999}','nonfinite JSON number')]:
  record(path.name+':'+label,lambda raw=raw:g['strict_json'](raw),reason)
 for name in ('../escape','a//b','./a','a/./b','a/../b','a\\b','a:b','a\x00b','a\nb','/absolute','a/'):
  record(path.name+':path:'+repr(name),lambda name=name:g['safe_name'](name),'path')
 row={'path':'one','bytes':1,'sha256':'0'*64}
 record(path.name+':boolean_size',lambda:g['rows_map']([{**row,'bytes':True}]),'byte count')
 record(path.name+':floating_size',lambda:g['rows_map']([{**row,'bytes':1.0}]),'byte count')
 record(path.name+':oversized',lambda:g['rows_map']([{**row,'bytes':2**40}]),'byte count')
 record(path.name+':duplicate_rows',lambda:g['rows_map']([row,row]),'duplicate inventory path')
 record(path.name+':file_directory_collision',lambda:g['rows_map']([row,{**row,'path':'one/two'}]),'collision')
 require(g['strict_json'](b'{"x":1e10,"y":0}')=={'x':1e10,'y':0},'finite JSON positive')
records.append({'case':'all four finite JSON positive controls','status':'PASS'})

def invoke(args):
 t=time.monotonic();p=subprocess.run([sys.executable,*flags,*map(str,args)],cwd=HERE,capture_output=True,timeout=15)
 require(not p.stderr,'unexpected stderr: '+p.stderr.decode())
 return p,json.loads(p.stdout),time.monotonic()-t
with tempfile.TemporaryDirectory(prefix='private review02 fixtures ',dir=HERE) as td:
 base=Path(td);fixture=base/'tiny';fixture.mkdir();marker=base/'CODE_EXECUTED';verifier=PORT/'verify_package.py'
 payload={'check_originals.py':b'raise RuntimeError("stub must not execute")\n','verify_package.py':b'nonexecuted payload\n','root_evidence/SOURCE_MANIFEST.json':b'{}\n'}
 def reset():
  if fixture.exists():shutil.rmtree(fixture)
  fixture.mkdir()
  for name,data in payload.items():
   dest=fixture/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
  return {'schema':'random-property-t-verification-v1','problem_id':'30006628','files':[{'path':name,'bytes':len(data),'sha256':h(data)} for name,data in payload.items()]}
 def write_index(index,raw=None):
  data=raw if raw is not None else json.dumps(index).encode();(fixture/'package_index.json').write_bytes(data);return h(data)
 def cli(label,index,raw=None,full=False,expect=None):
  pin=write_index(index,raw);args=[verifier,pin,'--root',fixture]+(['--full'] if full else []);p,r,sec=invoke(args)
  require(p.returncode==1 and r['status']=='REJECTED',label+' accepted')
  require(expect is None or expect in r['reason'],label+' incorrect rejection '+r['reason'])
  require(not marker.exists(),'changed code executed')
  records.append({'case':label,'status':'REJECTED_AS_INTENDED','reason':r['reason'],'resealed_external_index':True,'seconds':sec,'marker_absent':True})
 index=reset();pin=write_index(index);p,r,sec=invoke([verifier,pin,'--root',fixture]);require(p.returncode==0 and r['status']=='PASS','tiny positive rejected');records.append({'case':'valid tiny closed inventory','status':'PASS','member_count':r['package_member_count']})
 # Freshly recompute each external fixture pin; these specifically exercise parsing rather than digest failure.
 for label,raw,expect in [('resealed duplicate key',b'{"schema":"x","schema":"y"}','duplicate JSON key'),('resealed NaN',b'{"x":NaN}','nonfinite JSON constant'),('resealed overflow',b'{"x":1e999}','nonfinite JSON number')]:
  cli(label,reset(),raw=raw,expect=expect)
 index=reset();(fixture/'check_originals.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n');cli('changed checker before full execution',index,full=True,expect='mismatch')
 index=reset();(fixture/'extra_empty_directory').mkdir();cli('unlisted empty directory',index,expect='unlisted directory')
 index=reset();(fixture/'extra_file').write_text('x');cli('unlisted file',index,expect='unlisted file')
 index=reset();(fixture/'check_originals.py').unlink();(fixture/'check_originals.py').symlink_to(PORT/'check_originals.py');cli('internal leaf alias',index,expect='nonregular')
 index=reset();shutil.rmtree(fixture/'root_evidence');(fixture/'root_evidence').symlink_to(PORT/'root_evidence',target_is_directory=True);cli('internal directory alias',index,expect='nonregular')
 index=reset();(fixture/'check_originals.py').unlink();os.mkfifo(fixture/'check_originals.py');cli('FIFO pre-read rejection',index,expect='nonregular')
 index=reset();index['files'][0]['bytes']+=1;cli('pinned size disagreement',index,expect='byte count mismatch')
 index=reset();index['files'].append(index['files'][0]);cli('resealed duplicate inventory row',index,expect='duplicate inventory path')
 index=reset();index['files'][0]['path']='x/../check_originals.py';cli('resealed noncanonical path',index,expect='unsafe relative path')
 index=reset();index['files'][0]['bytes']=True;cli('resealed boolean byte count',index,expect='invalid pinned byte count')
 # Authenticate a full ordinary copied tree, then mutate its inner startup code only.
 full=base/'outer';shutil.copytree(ROOT,full)
 changed=full/'publication_20261015/verification_package/verify_package.py';changed.write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n')
 manifest_path=full/'PUBLICATION_MANIFEST.json';manifest=json.loads(manifest_path.read_bytes())
 row=next(x for x in manifest['files'] if x['path']=='publication_20261015/verification_package/verify_package.py');data=changed.read_bytes();row.update(bytes=len(data),sha256=h(data));raw=json.dumps(manifest).encode();manifest_path.write_bytes(raw)
 # The outer startup remains byte-authenticated. Resealing outer inventory cannot bypass inner index binding.
 p,r,sec=invoke([full/'verify_current_publication.py',h(raw),'--root',full,'--full']);require(p.returncode==1 and r['status']=='REJECTED' and 'portable verify_package.py' in r['reason'],'outer inner-code guard');require(not marker.exists(),'changed inner code executed')
 records.append({'case':'changed inner verifier with resealed outer manifest','status':'REJECTED_AS_INTENDED','reason':r['reason'],'marker_absent':True,'seconds':sec})
 # Builder independently requires the verifier external hash before executing it.
 index=reset();index['files'][1]['sha256']='f'*64;pin=write_index(index)
 p,r,sec=invoke([PORT/'build_verification.py',fixture,pin,'bf4b7f54267ec12bf3ed14bd8ae7410e2e3497943249bdc320bd8108fc9fc9aa',base/'not-created-output']);require(p.returncode==1 and 'startup verifier external pin mismatch' in r['reason'],'builder pin guard');require(not (base/'not-created-output').exists() and not marker.exists(),'builder wrote before validation')
 records.append({'case':'builder verifier external pin conflict','status':'REJECTED_AS_INTENDED','reason':r['reason'],'output_absent':True,'marker_absent':True})
print(json.dumps({'status':'PASS','mode':mode,'external_startup_hashes_verified':{str(p.relative_to(ROOT)):v for p,v in programs.items()},'negative_controls':sum(x['status']=='REJECTED_AS_INTENDED' for x in records),'positive_controls':sum(x['status']=='PASS' for x in records),'records':records,'private_fixtures_removed':True,'limits':'Trusted Python/stdlib/filesystem; no hostile concurrent ancestor replacement. Resealed parser fixtures deliberately trust their new index only; they are not claims to defeat a fixed external pin.'},indent=2))
