from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess
A=Path(__file__).resolve().parent;C=A.parents[2]
r=json.loads((A/'ROOT_CLOSURE_COMPLETION_20261006.json').read_text());release=json.loads((A/'ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json').read_text())
if not r['native_integration_complete'] or not release['remote_verified']:raise RuntimeError('no verified recovery point')
cp=r['native_checkpoint_commit'];prepared=json.loads((A/'native_prior_disposition_20261006/PREPARED_RECEIPT.json').read_text())
for pin in prepared['native_pins']:
 b=subprocess.check_output(['/usr/bin/git','show',cp+':'+pin['path']],cwd=C)
 if len(b)!=pin['bytes'] or hashlib.sha256(b).hexdigest()!=pin['sha256']:raise RuntimeError('recovery body mismatch')
removed=[]
for name in ['native_prior_disposition_20261006']:
 d=A/name/'private_backend'
 if not d.is_dir() or d.is_symlink() or not d.resolve().is_relative_to(A):raise RuntimeError('invalid owned backend')
 files=[p for p in d.rglob('*') if p.is_file()]
 if any(p.is_symlink() for p in d.rglob('*')):raise RuntimeError('backend symlink')
 removed.append({'path':str(d),'files':len(files),'logical_bytes':sum(p.stat().st_size for p in files),'regenerated_native_outputs_recoverable_from_commit':cp,
 'immutable_inputs_recoverable_from_commit':prepared['base_commit'],'cache_source_recovery':'Pinned dataset revision and verified primary catalog.sqlite; private copy-on-write snapshot only.'})
 shutil.rmtree(d)
out={'schema':'pr107-owned-private-backend-cleanup/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),
 'removed':removed,'actual_disposition_verified_first':True,'all_exported_pins_git_recovery_verified':True,
 'actual_command_journals_and_source_archives_preserved':True,'primary_cache_untouched':True,'browser_cache_untouched':True}
(A/'PRIVATE_BACKEND_CLEANUP_RECEIPT_20261006.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
