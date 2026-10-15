#!/usr/bin/env python3
"""Independent hostile packaging and legacy-trust boundary probes in own tmp."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).absolute().parent
sys.path.insert(0,str(HERE))
import HARDENED_VERIFY as H

def need(v,m):
 if not v:raise RuntimeError(m)
def dump(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def main():
 source=Path(sys.argv[1]);pins=H.load_pins();original=H.inventory(str(source),pins);workspace=HERE/'tmp';env=H.sanitized_env(workspace)
 # Authenticate trusted historical module bytes before compiling this exact buffer.
 data=original['VERIFY_PUBLICATION.py'];need(H.sha(data)==H.VERIFIER,'Historical wrapper pin mismatch')
 legacy={'__name__':'authenticated_legacy_publication','__file__':str(source/'VERIFY_PUBLICATION.py')};exec(compile(data,str(source/'VERIFY_PUBLICATION.py'),'exec'),legacy)
 results=[]
 def fixture():
  td=tempfile.TemporaryDirectory(prefix='hostile-',dir=workspace);root=Path(td.name)/'packet';root.mkdir()
  for rel,b in original.items():p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  return td,root
 def reject(fn,label):
  try:fn()
  except Exception as e:results.append({'case':label,'rejected':True,'error_class':type(e).__name__});return
  raise RuntimeError('Accepted hostile case '+label)
 def mutate_outer(root,fn):
  p=root/'PUBLICATION_MANIFEST.json';m=H.decode(p.read_bytes());fn(m);p.write_bytes(dump(m));return H.sha(p.read_bytes())
 # All strong-gate input mutations are rejected independently of attacker manifest rebinding.
 mutations={
 'changed_proof':lambda r:(r/'public/PROOF.md').write_bytes(original['public/PROOF.md']+b'x'),
 'extra_empty_directory':lambda r:(r/'EXTRA').mkdir(),
 'extra_regular_file':lambda r:(r/'EXTRA').write_bytes(b'x'),
 'extra_fifo':lambda r:os.mkfifo(r/'PIPE'),
 'missing_member':lambda r:(r/'public/README.md').unlink(),
 'member_symlink':lambda r:((r/'public/README.md').unlink(),(r/'public/README.md').symlink_to(source/'public/README.md')),
 'manifest_symlink':lambda r:((r/'PUBLICATION_MANIFEST.json').unlink(),(r/'PUBLICATION_MANIFEST.json').symlink_to(source/'PUBLICATION_MANIFEST.json')),
 'directory_symlink':lambda r:(shutil.rmtree(r/'public'),(r/'public').symlink_to(source/'public',target_is_directory=True)),
 'substituted_checker':lambda r:(r/'public/CHECKS.py').write_text('print("PASS")\n'),
 'substituted_wrapper':lambda r:(r/'VERIFY_PUBLICATION.py').write_text('print("PASS")\n'),
 }
 for label,mutation in mutations.items():
  td,root=fixture()
  with td:mutation(root);reject(lambda:H.inventory(str(root),pins),'pinned_'+label)
 for label,modifier in [
  ('duplicate_member',lambda m:m['files'].append(m['files'][0].copy())),
  ('boolean_size',lambda m:m['files'][0].update(bytes=True)),
  ('float_size',lambda m:m['files'][0].update(bytes=float(m['files'][0]['bytes']))),
  ('negative_size',lambda m:m['files'][0].update(bytes=-1)),
  ('boolean_problem',lambda m:m.update(problem_id=True)),
  ('float_problem',lambda m:m.update(problem_id=30002555.0)),
  ('unknown_top_level_key',lambda m:m.update(unknown='x')),
  ('unknown_member_key',lambda m:m['files'][0].update(unknown='x')),
  ('null_files',lambda m:m.update(files=None)),
  ('object_files',lambda m:m.update(files={})),
  ('nonstring_digest',lambda m:m['files'][0].update(sha256=True)),
  ('nan_size',lambda m:m['files'][0].update(bytes=float('nan'))),
  ('path_traversal',lambda m:m['files'][0].update(path='../escape')),
  ('path_double_slash',lambda m:m['files'][0].update(path='public//PROOF.md')),
  ('path_dot',lambda m:m['files'][0].update(path='public/./PROOF.md')),
  ('path_absolute',lambda m:m['files'][0].update(path='/tmp/escape')),
  ('path_backslash',lambda m:m['files'][0].update(path='public\\PROOF.md')),
  ('path_nul',lambda m:m['files'][0].update(path='public/\x00PROOF.md')),
 ]:
  td,root=fixture()
  with td:
   anchor=mutate_outer(root,modifier)
   reject(lambda:legacy['verify'](root,anchor),'legacy_'+label)
   reject(lambda:H.inventory(str(root),pins),'pinned_'+label)
 td,root=fixture()
 with td:
  p=root/'PUBLICATION_MANIFEST.json';p.write_bytes(b'{"schema":"duplicate",'+p.read_bytes().lstrip()[1:]);anchor=H.sha(p.read_bytes());reject(lambda:legacy['verify'](root,anchor),'legacy_duplicate_JSON_key');reject(lambda:H.inventory(str(root),pins),'pinned_duplicate_JSON_key')
 td,root=fixture()
 with td:
  linked=Path(td.name)/'link';linked.symlink_to(root,target_is_directory=True)
  reject(lambda:legacy['verify'](linked,H.OUTER),'legacy_direct_root_symlink');reject(lambda:H.inventory(str(linked),pins),'pinned_direct_root_symlink')
  # A symlink ancestor is a benign alias accepted by the legacy wrapper; stronger gate rejects it.
  parentlink=Path(td.name)/'parentlink';parentlink.symlink_to(root.parent,target_is_directory=True);alias=parentlink/root.name
  need(legacy['verify'](alias,H.OUTER)==26,'Legacy ancestor alias unexpectedly rejected');results.append({'case':'legacy_symlink_ancestor_alias','accepted':True,'interpretation':'Same authenticated bytes; legacy only bans root itself and members, not all ancestors.'});reject(lambda:H.inventory(str(alias),pins),'pinned_symlink_ancestor_alias')
  reject(lambda:H.inventory(str(root)+'/../packet',pins),'pinned_lexical_parent_alias');reject(lambda:H.inventory(str(root)+'/./',pins),'pinned_lexical_dot_alias')
 # Co-rebinding tests characterize external-anchor trust rather than inventing an attack on fixed pins.
 td,root=fixture()
 with td:
  p=root/'README.md';p.write_bytes(original['README.md']+b'\nControlled metadata mutation.\n')
  def rebind(m):
   for v in m['files']:
    if v['path']=='README.md':v.update(bytes=p.stat().st_size,sha256=H.sha(p.read_bytes()))
  replacement=mutate_outer(root,rebind)
  reject(lambda:legacy['verify'](root,H.OUTER),'legacy_metadata_rebind_fixed_external_anchor')
  need(legacy['verify'](root,replacement)==26,'Replacement manifest boundary probe failed')
  results.append({'case':'legacy_metadata_rebind_supplied_replacement_anchor','accepted':True,'interpretation':'Expected trust boundary: accepting a newly supplied external anchor changes trusted outer metadata.'})
  reject(lambda:H.inventory(str(root),pins),'pinned_metadata_and_manifest_corebound')
 td,root=fixture()
 with td:
  q=root/'public/CHECKS.py';q.write_text('import sys\nassert False, "controlled sentinel"\nsys.stdout.buffer.write('+repr(original['public/CHECK_RESULTS.json'])+')\n')
  innerpath=root/'public/MANIFEST.json';inner=H.decode(innerpath.read_bytes())
  for item in inner['files']:
   if item['path']=='CHECKS.py':item.update(bytes=q.stat().st_size,sha256=H.sha(q.read_bytes()))
  innerpath.write_bytes(dump(inner));inneranchor=H.sha(innerpath.read_bytes())
  # Reauthenticate the preserved legacy verifier and controlled fixture checker before execution.
  need((root/'public/VERIFY.py').read_bytes()==original['public/VERIFY.py'],'Legacy author verifier changed');checker= q.read_bytes();controlled_sha=H.sha(checker)
  def run_author(poison):
   need(q.read_bytes()==checker and H.sha(q.read_bytes())==controlled_sha,'Controlled checker changed before execution');need((root/'public/VERIFY.py').read_bytes()==original['public/VERIFY.py'],'Wrapper changed before execution')
   return subprocess.run([sys.executable,'-I','-B',str(root/'public/VERIFY.py'),inneranchor],cwd=root,env=dict(env,**({'PYTHONOPTIMIZE':'2'} if poison else {})),capture_output=True,timeout=30)
  ordinary=run_author(False);poisoned=run_author(True)
  need(ordinary.returncode!=0 and b'Arithmetic replay failed' in ordinary.stderr,'Assertion sentinel not caught in clean ordinary legacy run')
  need(poisoned.returncode==0 and H.decode(poisoned.stdout)['status']=='PASS','Inherited optimization boundary probe did not expose legacy issue')
  results.append({'case':'legacy_author_checker_assert_false_with_rebound_manifest','clean_environment_rejected':True,'inherited_PYTHONOPTIMIZE_2_accepted':True,'controlled_checker_sha256':controlled_sha,'interpretation':'Standalone historical author wrapper inherits optimization in children. Frozen outer wrapper sanitizes PYTHON variables and pins inner manifest; the all-27 gate rejects altered checker before execution.'})
  def outer_rebind(m):
   for item in m['files']:
    if item['path'] in ('public/CHECKS.py','public/MANIFEST.json'):
     member=root/item['path'];item.update(bytes=member.stat().st_size,sha256=H.sha(member.read_bytes()))
  replacement_outer=mutate_outer(root,outer_rebind)
  reject(lambda:legacy['verify'](root,replacement_outer),'legacy_assert_false_corebind_frozen_inner_anchor')
  reject(lambda:H.execute_checked(root,'public/CHECKS.py',[],[],pins,env),'copied_checker_reauthentication_before_execution')
  reject(lambda:H.inventory(str(root),pins),'pinned_assert_false_checker_fixture')
 # Strict output decoding/type/schema controls do not execute any hostile code.
 model={'status':'PASS','count':1}
 for label,raw in [('bool_count',b'{"status":"PASS","count":true}'),('float_count',b'{"status":"PASS","count":1.0}'),('extra_key',b'{"status":"PASS","count":1,"extra":0}'),('list_output',b'[]'),('duplicate_output',b'{"status":"PASS","count":1,"count":1}'),('nonfinite_output',b'{"status":"PASS","count":NaN}')]:reject(lambda raw=raw:H.same_schema(H.decode(raw),model),'stdout_'+label)
 need(H.inventory(str(source),pins)==original,'Original mutated')
 out={'status':'PASS','results':results,'rejections':sum(bool(x.get('rejected')) for x in results),'observed_boundary_acceptances':3,'source_unchanged':True,'limits':'Probes run only reviewed historical code and one explicit safe assertion fixture; no arbitrary external program is executed. Acceptance under a replacement external anchor is a trust-boundary observation.'}
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
