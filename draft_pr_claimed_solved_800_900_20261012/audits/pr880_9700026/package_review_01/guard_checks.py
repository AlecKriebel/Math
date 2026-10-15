#!/usr/bin/env python3
"""Independent, bounded negative controls on externally pinned PR880 helpers."""
from pathlib import Path
import sys,hashlib,json,runpy,tempfile,os,copy,subprocess,struct
R=Path(__file__).resolve().parent;A=R.parent;V=A/'replay/portable_r1_polished';O=A/'replay/revision_r1'
PINS={'verify_package.py':'73faad1cfa4ab2e9c7e6cfa214e58fadb361ccf4de3199ed87e96883ae6a351a','check_originals.py':'e78f97d36210f29e466636861767124a338c9ad0fe48e050eeec2a5355c3771f','verify_current_publication.py':'b8279f4945b2f05b3755bfec20ae6c78dbbb00d053abdb04f87d8068f2ff62a7'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):
 need(hashlib.sha256(p.read_bytes()).hexdigest()==PINS[p.name],'independent pre-load pin')
 return runpy.run_path(str(p),run_name='reviewed_helpers_only')
def main():
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'use -I -S -B')
 v=load(V/'verify_package.py');w=load(O/'verify_current_publication.py');c=load(V/'check_originals.py');rows=[]
 def reject(label,fn):
  try:fn()
  except (ValueError,OSError,KeyError,TypeError,RuntimeError,OverflowError,RecursionError,UnicodeError) as e:
   rows.append({'label':label,'expected':'REJECT','observed':'REJECT','reason':str(e)})
  else:raise ValueError('accepted negative control: '+label)
 def accept(label,fn):
  fn();rows.append({'label':label,'expected':'ACCEPT','observed':'ACCEPT'})
 for label,raw in [('duplicate_key',b'{"x":1,"x":2}'),('nan',b'{"x":NaN}'),('overflow_float',b'{"x":1e999}')]:reject(label,lambda raw=raw:v['strict_json'](raw))
 for name in ['../escape','/absolute','a\\b','a\nb','a//b','a/./b','C:bad']:
  reject('unsafe_name_'+repr(name),lambda name=name:v['safe_name'](name))
 row={'path':'one','bytes':1,'sha256':'0'*64}
 reject('boolean_inventory_size',lambda:v['rows_map']([{**row,'bytes':True}]))
 reject('duplicate_inventory_path',lambda:v['rows_map']([row,row]))
 reject('file_directory_collision',lambda:v['rows_map']([row,{**row,'path':'one/two'}]))
 accept('legitimate_space_path',lambda:v['safe_name']('folder with spaces/file.json'))
 accept('finite_json',lambda:v['strict_json'](b'{"x":0.125}'))
 with tempfile.TemporaryDirectory(prefix='guards ',dir=R/'private') as td:
  d=Path(td);f=d/'ordinary';f.write_bytes(b'ok');link=d/'alias';link.symlink_to(f)
  reject('leaf_symlink',lambda:v['read_regular'](link))
  fifo=d/'pipe';os.mkfifo(fifo);reject('fifo_nonblocking_rejection',lambda:v['read_regular'](fifo));fifo.unlink();link.unlink()
  reject('wrong_size',lambda:v['read_regular'](f,3))
  accept('regular_exact_read',lambda:need(v['read_regular'](f,2)==b'ok','regular bytes'))
  reject('unlisted_file',lambda:v['closed_tree'](d,set()))
  (d/'empty_extra').mkdir();reject('unlisted_empty_directory',lambda:v['closed_tree'](d,{'ordinary'}));(d/'empty_extra').rmdir()
  sub=d/'sub';sub.symlink_to(d,target_is_directory=True);reject('interior_directory_alias',lambda:v['within'](d,'sub/ordinary'));sub.unlink()
  reject('external_index_wrong_digest',lambda:v['package_inputs'](V,'0'*64))
  # Source alias is rejected before reading any large corpus.
  repo=A.parents[2];link=d/'catalog.json';link.symlink_to(repo/'unsolved_math_prioritization/catalog.json')
  sources={'catalog':link,'problems':repo/'unsolved_math_prioritization/cache/problems.json','reports':repo/'unsolved_math_prioritization/cache/research_results.json','pdf_dir':A/'private_sources','pdf_2012':A/'private_sources/1209.5120v1.pdf'}
  reject('complete_input_leaf_alias',lambda:c['supplied_inputs'](sources))
 portable={p.relative_to(V).as_posix():p.read_bytes() for p in V.rglob('*') if p.is_file()}
 good=(A/'preprint/verification.zip').read_bytes()
 accept('valid_archive_boundary_and_payload',lambda:w['archive_copies'](good,portable))
 reject('zip_prepended_byte',lambda:w['archive_copies'](b'X'+good,portable))
 reject('zip_appended_byte',lambda:w['archive_copies'](good+b'X',portable))
 reject('zip_truncated_end_record',lambda:w['archive_copies'](good[:-1],portable))
 bad=bytearray(good);central=bad.find(b'PK\x01\x02');need(central>=0,'central header')
 # Same declared huge size in first local and first central record: must reject before decompression.
 struct.pack_into('<I',bad,22,0xffffffff);struct.pack_into('<I',bad,central+24,0xffffffff)
 reject('zip_huge_declared_member_size',lambda:w['archive_copies'](bytes(bad),portable))
 outer={p.relative_to(O).as_posix():p.read_bytes() for p in O.rglob('*') if p.is_file()}
 accept('valid_current_metadata_and_copies',lambda:w['portable_inputs'](outer))
 bad=dict(outer);name='publication_20261015/preprint/note.tex';bad[name]=bad[name]+b'\n'
 reject('preprint_inner_note_divergence',lambda:w['portable_inputs'](bad))
 bad=dict(outer);name='CURRENT_PUBLICATION.json';d=json.loads(bad[name]);d['zenodo_metadata']['version']='9.9.9';bad[name]=json.dumps(d).encode()
 reject('canonical_metadata_divergence',lambda:w['portable_inputs'](bad))
 bad=dict(outer);name='publication_20261015/preprint/zenodo-deposit.json';d=json.loads(bad[name]);d['files'][0]['name']='wrong.pdf';bad[name]=json.dumps(d).encode()
 reject('deposit_filename_divergence',lambda:w['portable_inputs'](bad))
 # CLI option guards use the exact genuine startup bytes, from unrelated cwd.
 for label,args in [('partial_source_options',['--full','--catalog','missing']),('source_without_full',['--catalog','a','--problems','b','--reports','c','--pdf-dir','d']),('pdf_override_alone',['--pdf-2012','missing'])]:
  cmd=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+[str(V/'verify_package.py'),'7af74074708d9ee7b462be7d74546ef1f090a3262223d538082e872288e3df3d','--root',str(V),*args]
  proc=subprocess.run(cmd,cwd=R/'private',capture_output=True,timeout=30)
  need(proc.returncode==1 and not proc.stderr and json.loads(proc.stdout)['status']=='REJECTED',label+' CLI rejection')
  rows.append({'label':label,'expected':'REJECT','observed':'REJECT','reason':json.loads(proc.stdout)['reason']})
 mode='OPTIMIZED' if sys.flags.optimize else 'NORMAL'
 out={'status':'PASS','mode':mode,'negative_count':sum(r['expected']=='REJECT' for r in rows),'positive_count':sum(r['expected']=='ACCEPT' for r in rows),'controls':rows,'limits':'Helper checks plus actual CLI option controls; not a hostile concurrent-filesystem sandbox or analytic proof.'}
 (R/('GUARD_CHECKS_'+mode+'.json')).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','mode':mode,'negative_count':out['negative_count'],'positive_count':out['positive_count']}))
if __name__=='__main__':main()
