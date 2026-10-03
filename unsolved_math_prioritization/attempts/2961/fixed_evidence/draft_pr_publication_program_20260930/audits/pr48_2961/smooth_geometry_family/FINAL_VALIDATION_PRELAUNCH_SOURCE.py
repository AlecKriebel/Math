import pathlib, json, hashlib, stat, datetime, os
assert __debug__
r=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
original=json.loads((r/'ORIGINAL_COMPLETE_INDEPENDENT_AUDIT.json').read_bytes())
def check_bound(row):
 p=pathlib.Path(row['path']);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
 assert stat.S_IMODE(s.st_mode)==row['full_mode']
 return {'path':str(p),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(s.st_mode)}
original_rechecked=[check_bound(x) for x in original['closed_original_payload_reads']]
original_rechecked.append(check_bound(original['original_manifest']))
outer_rechecked=[check_bound(x) for x in original['external_actual_original_closure_reads']]
raw_rechecked=[check_bound(x) for x in original['raw_in_place_full_reads']]
captures=[]
for p in sorted(r.rglob('CAPTURE.json')):
 c=json.loads(p.read_bytes());d=p.parent
 assert isinstance(c['pid'],int) and c['pid']>0 and isinstance(c['exit_code'],int)
 assert datetime.datetime.fromisoformat(c['started_utc'])<=datetime.datetime.fromisoformat(c['finished_utc'])
 assert sha((d/'prelaunch_operator.py').read_bytes())==c['operator_sha256']
 streams=c.get('streams',{})
 for name in ['stdout.bin','stderr.bin']:
  expected=streams.get(name,c.get(name.split('.')[0]));assert expected is not None
  b=(d/name).read_bytes();assert len(b)==expected['bytes'] and sha(b)==expected['sha256']
 captures.append({'path':str(p.relative_to(r)),'sha256':sha(p.read_bytes()),'pid':c['pid'],'exit_code':c['exit_code']})
pairs=[('fetch_primary_sources.py','FETCH_PRIMARY_PRELAUNCH_SOURCE.py'),('render_primary_pages.py','RENDER_PRELAUNCH_SOURCE.py'),('audit_original.py','ORIGINAL_AUDIT_PRELAUNCH_SOURCE.py'),('audit_original_v2.py','ORIGINAL_AUDIT_V2_PRELAUNCH_SOURCE.py'),('replay_original_helpers.py','HELPER_REPRODUCTION_PRELAUNCH_SOURCE.py'),('check_smooth_geometry.py','SMOOTH_DIAGNOSTICS_PRELAUNCH_SOURCE.py'),('fetch_additional_sources.py','ADDITIONAL_FETCH_PRELAUNCH_SOURCE.py')]
for a,b in pairs:assert (r/a).read_bytes()==(r/b).read_bytes()
v=json.loads((r/'VERDICT.json').read_bytes());assert v['mathematical_partial']=='PASS' and v['open_problem_outcome']=='unsolved'
assert v['new_substantive_turns']==v['audit_turn_charge']==0
tmp=r/'tmp';assert tmp.is_dir() and not tmp.is_symlink()
transients=[]
for p in sorted(tmp.rglob('*')):
 assert not p.is_symlink()
 if p.is_file():
  b=p.read_bytes();transients.append({'path':str(p.relative_to(r)),'bytes':len(b),'sha256':sha(b),'removed_utc':stamp()});p.unlink()
for p in sorted(tmp.rglob('*'),key=lambda x:len(x.parts),reverse=True):assert p.is_dir();p.rmdir()
tmp.rmdir()
assert not tmp.exists()
assert not any(p.suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.webp'} for p in r.rglob('*') if p.is_file())
receipt={'schema':'pr48-smooth-geometry-final-readback-and-transient-removal/v1','actual_pid':os.getpid(),'completed_utc':stamp(),'original_files_rechecked':len(original_rechecked),'outer_original_closure_files_rechecked':len(outer_rechecked),'raw_in_place_full_hashes_rechecked':raw_rechecked,'own_prior_captures':captures,'own_prelaunch_source_pairs_verified':len(pairs),'removed_foreign_transient_files':transients,'foreign_bodies_remaining':False,'no_original_changes':True,'promotion_or_root_closure_claim':False}
(r/'FINAL_READBACK_AND_TRANSIENT_REMOVAL.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','actual_pid':os.getpid(),'original_files_rechecked':len(original_rechecked),'outer_closure_files_rechecked':len(outer_rechecked),'raw_files_rechecked':len(raw_rechecked),'own_prior_captures_rechecked':len(captures),'transient_files_removed':len(transients),'foreign_bodies_remaining':False},indent=2))
