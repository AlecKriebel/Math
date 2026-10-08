#!/usr/bin/env python3
"""Source-free audit controls; authored dummy mutations only. No assertions."""
import sys
sys.dont_write_bytecode=True
import pathlib,hashlib,json,subprocess,tempfile,shutil,importlib.util,tarfile,os
import argparse
parser=argparse.ArgumentParser(description='Reproduce bounded packet integrity and corruption controls against the frozen author input.')
parser.add_argument('--packet',required=True,help='Original author public directory')
parser.add_argument('--archive',required=True,help='Original author tar.gz archive')
args=parser.parse_args()
author=pathlib.Path(args.packet).absolute()
archive=pathlib.Path(args.archive).absolute()
anchor='e6f747996c9dcf7fd9d525cc34f347577538f169e620b4dd3a98269f27b31e29'
if hashlib.sha256(archive.read_bytes()).hexdigest()!='d6bf160fd3973409c26ed8b514bc231956b7d3d113cf888e5e15b5f6060779d1':raise RuntimeError('archive trust anchor')
if hashlib.sha256((author/'MANIFEST.json').read_bytes()).hexdigest()!=anchor:raise RuntimeError('manifest trust anchor')
manifest=json.loads((author/'MANIFEST.json').read_text())
for x in manifest['files']:
 b=(author/x['path']).read_bytes()
 if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']: raise RuntimeError('external file check')
with tarfile.open(archive,'r:gz') as t:
 names=t.getnames()
 if set(names)!={x.name for x in author.iterdir()}:raise RuntimeError('archive names')
 for member in t.getmembers():
  if not member.isfile() or t.extractfile(member).read()!=(author/member.name).read_bytes(): raise RuntimeError('archive mismatch')
spec=importlib.util.spec_from_file_location('author_verify_audited',author/'verify.py'); v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
results={'external_hash_and_archive_checks':'PASS','rejected':[],'expected_limitations':[],'execution':[]}
def trial(name,change,expected_reject=True,anchored=True):
 with tempfile.TemporaryDirectory(prefix='ramification-audit-') as d:
  packet=pathlib.Path(d)/'packet';shutil.copytree(author,packet);change(packet)
  try:v.verify_integrity(packet,anchor if anchored else None)
  except Exception as exc:
   if not expected_reject:raise
   results['rejected'].append({'test':name,'exception':type(exc).__name__})
  else:
   if expected_reject:raise RuntimeError('unexpected acceptance: '+name)
   results['expected_limitations'].append(name)
for x in manifest['files']:
 trial('one_byte_corruption_'+x['path'],lambda d,n=x['path']:(d/n).write_bytes(b'!'+(d/n).read_bytes()[1:]))
def edit(d,f):
 p=d/'MANIFEST.json'; data=json.loads(p.read_text());f(data);p.write_text(json.dumps(data))
mutations={
 'duplicate_json_key':lambda d:(d/'MANIFEST.json').write_text((d/'MANIFEST.json').read_text().replace('{','{"schema":"duplicate",',1)),
 'unexpected_manifest_key':lambda d:edit(d,lambda m:m.update(extra=1)),
 'duplicate_manifest_entry':lambda d:edit(d,lambda m:m['files'].append(m['files'][0])),
 'omitted_manifest_entry':lambda d:edit(d,lambda m:m['files'].pop()),
 'boolean_byte_count':lambda d:edit(d,lambda m:m['files'][0].update(bytes=True)),
 'negative_byte_count':lambda d:edit(d,lambda m:m['files'][0].update(bytes=-1)),
 'uppercase_digest':lambda d:edit(d,lambda m:m['files'][0].update(sha256=m['files'][0]['sha256'].upper())),
 'traversal_path':lambda d:edit(d,lambda m:m['files'][0].update(path='../secret.txt')),
 'absolute_path':lambda d:edit(d,lambda m:m['files'][0].update(path='/tmp/secret.txt')),
 'extra_dummy_source_pdf':lambda d:(d/'dummy.pdf').write_text('authored dummy'),
 'empty_nested_directory':lambda d:(d/'nested').mkdir(),
 'extra_hidden_file':lambda d:(d/'.unlisted').write_text('authored dummy'),
 'broken_file_symlink':lambda d:((d/'README.md').unlink(),(d/'README.md').symlink_to(d/'no-such-file')),
 'manifest_file_symlink':lambda d:((d/'MANIFEST.json').rename(d.parent/'manifest-backup'),(d/'MANIFEST.json').symlink_to(d.parent/'manifest-backup')),
 'missing_manifest':lambda d:(d/'MANIFEST.json').unlink(),
}
for name,mut in mutations.items():trial(name,mut,anchored=False)
def coordinated_prose(d):
 p=d/'01_UPPER_BREAK.md';p.write_text(p.read_text().replace('r\\geq p^a+1','r\\geq p^a',1))
 b=p.read_bytes()
 edit(d,lambda m:next(x for x in m['files'] if x['path']==p.name).update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
trial('coordinated_mathematical_prose_edit_anchored',coordinated_prose)
trial('coordinated_mathematical_prose_edit_unanchored_is_accepted',coordinated_prose,expected_reject=False,anchored=False)
with tempfile.TemporaryDirectory(prefix='ramification-isolated-') as d:
 packet=pathlib.Path(d)/'packet';shutil.copytree(author,packet)
 for optimized in (False,True):
  for script in ('verify.py','negative_controls.py'):
   cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(packet/script)]
   if script=='verify.py':cmd+=['--expected-manifest-sha256',anchor]
   run=subprocess.run(cmd,capture_output=True,text=True,cwd=d)
   if run.returncode:raise RuntimeError(run.stderr)
   results['execution'].append({'script':script,'optimized':optimized,'isolated':True,'returncode':run.returncode,'stdout_sha256':hashlib.sha256(run.stdout.encode()).hexdigest()})
  run=subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(packet/'verify.py'),'--math-only','--expected-manifest-sha256',anchor],capture_output=True,text=True,cwd=d)
  if not run.returncode:raise RuntimeError('math-only anchor conflict accepted')
  results['rejected'].append({'test':'math_only_anchor_conflict_'+str(optimized),'exception':'nonzero_exit'})
 # The API rejects a symlink root, but main resolves it before this check.
 link=pathlib.Path(d)/'linked-packet';link.symlink_to(packet,target_is_directory=True)
 try:v.verify_integrity(link,anchor)
 except RuntimeError:results['rejected'].append({'test':'API_symlink_root','exception':'RuntimeError'})
 else:raise RuntimeError('API symlink root accepted')
 run=subprocess.run([sys.executable,'-B',str(link/'verify.py'),'--expected-manifest-sha256',anchor],capture_output=True,text=True,cwd=d)
 results['expected_limitations'].append({'test':'CLI_symlink_root_resolved_before_guard','returncode':run.returncode,'interpretation':'CLI accepts a path alias to the same clean anchored packet; no extra payload accepted.'})
 if run.returncode:raise RuntimeError('unexpected CLI symlink outcome')
results['rejected_count']=len(results['rejected'])
results['result']='PASS_AUDIT_CONTROLS_WITH_DOCUMENTED_LIMITATIONS'
print(json.dumps(results,indent=2,sort_keys=True))
