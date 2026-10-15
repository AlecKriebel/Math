#!/usr/bin/env python3
"""Fresh independent controls. Mutations are private disposable copies; no archive harness is run."""
from pathlib import Path
from fractions import Fraction as F
import copy, hashlib, io, json, os, runpy, shutil, stat, struct, subprocess, sys, tempfile, zipfile
R=Path(__file__).resolve().parent;A=R.parent;V=A/'replay/portable_r1_polished';P=A/'preprint';O=A/'replay/revision_r1'
T=R/'private'/'controls';T.mkdir(parents=True,exist_ok=True);os.environ['TMPDIR']=str(T);tempfile.tempdir=str(T)
def need(c,m):
 if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def encode(x):return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
rows=[]
def check(label,f,reject=True,model='known authenticated code, private synthetic helper fixture'):
 try:r=f()
 except (ValueError,OSError,TypeError,KeyError,UnicodeError,zipfile.BadZipFile) as e:
  need(reject,label+' unexpectedly rejected '+str(e));rows.append({'label':label,'expected':'REJECT','actual':'REJECT','reason':str(e),'model':model})
 else:
  need(not reject,label+' unexpectedly accepted');rows.append({'label':label,'expected':'ACCEPT','actual':'ACCEPT','model':model})
idx_raw=(V/'package_index.json').read_bytes();idxsha=sha(idx_raw)
need(idxsha=='7af74074708d9ee7b462be7d74546ef1f090a3262223d538082e872288e3df3d','index startup')
modules={}
for n,path,h in [('portable',V/'verify_package.py','73faad1cfa4ab2e9c7e6cfa214e58fadb361ccf4de3199ed87e96883ae6a351a'),('checker',V/'check_originals.py','e78f97d36210f29e466636861767124a338c9ad0fe48e050eeec2a5355c3771f'),('builder',V/'build_verification.py','a1d76f65b2438236f2251c0f4dc850140fd1495a6e7ed418bfbf10fc86e23cca'),('outer',O/'verify_current_publication.py','b8279f4945b2f05b3755bfec20ae6c78dbbb00d053abdb04f87d8068f2ff62a7'),('assembler',A/'local_tools/pr880_assemble.py','939fea38779e6df5e81f7930a6a39153a082bcea046ad2879dabc4e0b8115055')]:
 need(sha(path.read_bytes())==h,'startup '+n);modules[n]=runpy.run_path(str(path),run_name='independent_review_library')
# Check identical safety helper semantics in every executable startup body.
for n,m in modules.items():
 for label,raw in [('overflow',b'{"x":1e9999}'),('duplicate',b'{"x":0,"x":1}'),('nan',b'{"x":NaN}')]:check(n+':strict_'+label,lambda m=m,raw=raw:m['strict_json'](raw))
 for path in ('../parent','a//b','a/./b','/absolute','a:b','a\\b','control\x01name'):
  check(n+':path_'+repr(path),lambda m=m,path=path:m['safe_name'](path))
 row={'path':'p','bytes':True,'sha256':'0'*64};check(n+':boolean_bytes',lambda m=m:m['pin_row'](row))
 check(n+':file_directory_collision',lambda m=m:m['rows_map']([{'path':'p','bytes':0,'sha256':'0'*64},{'path':'p/q','bytes':0,'sha256':'0'*64}]))
 check(n+':ordinary_json',lambda m=m:m['strict_json'](b'{"x":0.125}'),False)
with tempfile.TemporaryDirectory(prefix='fresh controls with spaces ') as td:
 work=Path(td);c=work/'portable';shutil.copytree(V,c)
 def cli(label,root=c,pin=idxsha,extra=(),success=False,script=None):
  cmd=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+[str(script or (V/'verify_package.py')),pin,'--root',str(root),*extra]
  proc=subprocess.run(cmd,cwd=work,capture_output=True,timeout=800)
  need(not proc.stderr,label+' unexpected stderr');r=json.loads(proc.stdout)
  need((proc.returncode==0 and r['status']=='PASS') if success else (proc.returncode!=0 and r['status']=='REJECTED'),label+' CLI status')
  rows.append({'label':label,'expected':'ACCEPT' if success else 'REJECT','actual':'ACCEPT' if success else 'REJECT','returncode':proc.returncode,'stdout_bytes':len(proc.stdout),'stdout_sha256':sha(proc.stdout),'reason':r.get('reason'),'model':'actual CLI; fixture copied from authenticated real portable root'})
 cli('baseline_closed_inventory',success=True)
 cli('wrong_external_index',pin='0'*64)
 cli('partial_source_arguments',extra=['--catalog',str(work/'absent')])
 cli('pdf_mapping_alone',extra=['--pdf-2012',str(work/'absent')])
 cli('all_sources_without_full',extra=['--catalog',str(work/'a'),'--problems',str(work/'b'),'--reports',str(work/'c'),'--pdf-dir',str(work/'d')])
 x=c/'unlisted_empty';x.mkdir();cli('empty_directory');x.rmdir()
 x=c/'unlisted_file';x.write_bytes(b'private fixture');cli('unlisted_regular');x.unlink()
 x=c/'note.pdf';saved=x.read_bytes();x.unlink();x.symlink_to(V/'note.pdf');cli('listed_leaf_symlink');x.unlink();x.write_bytes(saved);x.chmod(0o644)
 x.unlink();os.mkfifo(x);cli('listed_fifo_preopen');x.unlink();x.write_bytes(saved);x.chmod(0o644)
 p=c/'package_index.json'
 for label,raw in [('index_duplicate',idx_raw.replace(b'{',b'{"problem_id":"9700026",',1)),('index_overflow',idx_raw.replace(b'{',b'{"unused":1e9999,',1))]:
  p.write_bytes(raw);cli(label,pin=sha(raw))
 p.write_bytes(idx_raw)
 # Check modified indexed JSON under a newly explicit external fixture digest.
 name='metadata.json';saved=(c/name).read_bytes();bad=b'{"x":1,"x":2}'
 (c/name).write_bytes(bad);d=json.loads(idx_raw);next(r for r in d['files'] if r['path']==name).update(bytes=len(bad),sha256=sha(bad));new=encode(d);p.write_bytes(new);cli('reindexed_duplicate_payload',pin=sha(new));(c/name).write_bytes(saved);p.write_bytes(idx_raw)
 # An altered child is rejected before its injected marker can run.
 marker=work/'MUST_NOT_EXECUTE';child=c/'check_originals.py';saved=child.read_bytes()
 child.write_bytes(('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n').encode()+saved)
 cli('fixed_index_poisoned_child_preexecution',extra=['--full']);need(not marker.exists(),'poisoned child executed');child.write_bytes(saved)
 # Outer ZIP helper: real valid ZIP and payload map, then representation-only attacks.
 portable={p.relative_to(V).as_posix():p.read_bytes() for p in V.rglob('*') if p.is_file()};raw=(P/'verification.zip').read_bytes();outer=modules['outer']
 check('ZIP_real_positive',lambda:outer['archive_copies'](raw,portable),False)
 for label,bad in [('ZIP_prepended_bytes',b'X'+raw),('ZIP_trailing_bytes',raw+b'X'),('ZIP_local_DOS_time',raw[:10]+b'\x01\x00'+raw[12:]),('ZIP_local_name',raw[:30]+bytes([raw[30]^1])+raw[31:])]:check(label,lambda bad=bad:outer['archive_copies'](bad,portable))
 # Known outer copy binding must reject a portable-note discrepancy even when both trees are synthetic.
 blobs={p.relative_to(O).as_posix():p.read_bytes() for p in O.rglob('*') if p.is_file()}
 name='publication_20261015/preprint/note.tex';blobs[name]+=b'\n';check('outer_current_note_copy_binding',lambda:outer['portable_inputs'](blobs))
 # Builder may not write over an existing output or inside input tree.
 for label,out in [('builder_inside_assembly',c/'badoutput'),('builder_existing_output',work/'occupied')]:
  if label.endswith('existing_output'):out.mkdir();(out/'sentinel').write_bytes(b'unchanged')
  cmd=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+[str(P/'build_verification.py'),str(c),idxsha,sha((V/'verify_package.py').read_bytes()),str(out)]
  proc=subprocess.run(cmd,cwd=work,capture_output=True,timeout=800);r=json.loads(proc.stdout);need(proc.returncode!=0 and r['status']=='REJECTED',label)
  need(not (out/'verification.zip').exists(),label+' output created');rows.append({'label':label,'expected':'REJECT','actual':'REJECT','reason':r['reason'],'model':'real builder CLI on private copied assembly'})
 # Assembler must reject collision with its generated index before creating output.
 base=work/'minimal seed';base.mkdir();(base/'README.md').write_bytes(b'x');spec=work/'spec.json'
 for spelling in ('PUBLICATION_MANIFEST.json','PUBLICATION_MANIFEST.json/child'):
  # Outer required entries exist; all use same harmless source byte.
  entries=[{'source':'README.md','path':n,'bytes':1,'sha256':sha(b'x')} for n in ['README.md','RESEARCH_LOG.md','CURRENT_PUBLICATION.json','verify_current_publication.py']]
  # CURRENT_PUBLICATION.json must parse, so seed {} and pin that row.
  (base/'data.json').write_bytes(b'{}');next(e for e in entries if e['path']=='CURRENT_PUBLICATION.json').update(source='data.json',bytes=2,sha256=sha(b'{}'))
  entries.append({'source':'data.json','path':spelling,'bytes':2,'sha256':sha(b'{}')});rawspec=encode({'schema':'city-ode-explicit-assembly-v1','kind':'outer','files':entries});spec.write_bytes(rawspec);out=work/('assembler bad '+str(len(rows)))
  proc=subprocess.run([sys.executable,'-I','-S','-B',*(['-O'] if sys.flags.optimize else []),str(A/'local_tools/pr880_assemble.py'),str(base),str(spec),sha(rawspec),str(out)],cwd=work,capture_output=True,timeout=30);r=json.loads(proc.stdout)
  need(proc.returncode!=0 and r.get('reason')=='generated index file/directory collision' and not out.exists(),'assembler collision');rows.append({'label':'assembler_'+spelling,'expected':'REJECT','actual':'REJECT','reason':r['reason'],'model':'externally pinned explicit synthetic outer allowlist'})
 need(not marker.exists(),'marker appeared')
result={'status':'PASS','optimized':bool(sys.flags.optimize),'negative_controls':sum(r['expected']=='REJECT' for r in rows),'positive_controls':sum(r['expected']=='ACCEPT' for r in rows),'all_rows':rows,'private_fixture_cleanup':True,'limitation':'Fresh controls are finite rejection/acceptance evidence for enumerated mechanisms only; not all historical 106 cases, analytic proof, or hostile concurrent-filesystem sandbox.'}
(R/('CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'CONTROLS_NORMAL.json')).write_bytes(encode(result));print(json.dumps({k:v for k,v in result.items() if k!='all_rows'}))
