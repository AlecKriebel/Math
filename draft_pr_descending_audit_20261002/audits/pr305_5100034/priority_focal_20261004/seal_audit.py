from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os

ROOT=Path(__file__).resolve().parent
def measure(p):
    b=p.read_bytes()
    return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
            'mode':oct(p.stat().st_mode&0o777)}
utc=datetime.now(timezone.utc).isoformat()
closure={
 'UTC_seal_operation_started':utc,'audit_root':str(ROOT),
 'bounded_audit_completed':True,'global_priority_resolved':False,
 'no_more_writes_after_final_seal_is_written':True,
 'criteria_sha256':hashlib.sha256((ROOT/'FROZEN_ACCEPTANCE_CRITERIA.md').read_bytes()).hexdigest(),
 'report':measure(ROOT/'FOCAL_PRIORITY_COMPARISON.md'),
 'custody':measure(ROOT/'SOURCE_CUSTODY.json'),
 'claim_comparison':measure(ROOT/'CLAIM_COMPARISON.json'),
 'self_check':measure(ROOT/'FINAL_SELF_CHECK.md'),
 'verdict':{'E':'Exact statement prior in April2020; primitive-even proof prior; full-domain proof priority unresolved.',
            'M':'No complete equivalent identified in audited sections; priority unresolved.',
            'C':'False by ROOT mathematical gate; correction firstness not certified.'},
 'remaining_gaps':['N3 circle-center specialization','Even-period scalar-trace bridge comparison',
  'Six unavailable journal editions, individually classified in report/custody',
  'Finite literature coverage and ROOT independent wider-family adjudication'],
 'authorization_to_merge_or_publish':False,
 'final_mode_policy':'All regular files0o444, all directories0o555; recorded measurements in FINAL_SEAL.json.',
 'seal_self_hash_policy':'FINAL_SEAL.json excludes its own file to avoid circular hashing. Its measured full-file hash is returned in the final native tool output and handoff.'}
(ROOT/'CLOSURE.json').write_text(json.dumps(closure,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+utc+': Bounded audit completed; completion estimate100% of this defined audit, while global historical priority remains unresolved. Final artifact seal and no-more-writes covenant entered. Exact remaining substantive gaps are preserved in CLOSURE.json and the report. No merge/publication authorization.\n')
seal=ROOT/'FINAL_SEAL.json'
# Keep one already-open descriptor for the manifest while measuring the final read-only tree.
with seal.open('w') as output:
    paths=list(ROOT.rglob('*'))
    if any(p.is_symlink() for p in paths):raise RuntimeError('Unexpected symlink')
    for p in paths:
        if p.is_file():p.chmod(0o444)
    for p in sorted([x for x in paths if x.is_dir()],key=lambda x:len(x.parts),reverse=True):p.chmod(0o555)
    ROOT.chmod(0o555)
    files=[measure(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p!=seal]
    dirs=[{'path':'.','mode':oct(ROOT.stat().st_mode&0o777)}]
    dirs += [{'path':str(p.relative_to(ROOT)),'mode':oct(p.stat().st_mode&0o777)} for p in sorted(ROOT.rglob('*')) if p.is_dir()]
    manifest={'UTC_manifest_before_final_write':datetime.now(timezone.utc).isoformat(),
      'audit_root':str(ROOT),'hash_algorithm':'SHA256','files':files,'directories':dirs,
      'self_file_excluded':'FINAL_SEAL.json','all_measured_files_read_only':all(x['mode']=='0o444' for x in files),
      'all_measured_directories_read_only':all(x['mode']=='0o555' for x in dirs),
      'no_more_writes_after_manifest_descriptor_closed':True}
    json.dump(manifest,output,ensure_ascii=False,indent=2);output.write('\n');output.flush();os.fsync(output.fileno())
# From this point onward the audit tree must receive no further writes.
print(json.dumps({'UTC_closure_confirmed':datetime.now(timezone.utc).isoformat(),
  'manifest':measure(seal),'closure':measure(ROOT/'CLOSURE.json'),
  'report':measure(ROOT/'FOCAL_PRIORITY_COMPARISON.md'),
  'custody':measure(ROOT/'SOURCE_CUSTODY.json'),
  'claim_comparison':measure(ROOT/'CLAIM_COMPARISON.json'),
  'measured_file_count_excluding_self':len(files),'measured_directory_count':len(dirs),
  'all_files_mode444':all(x['mode']=='0o444' for x in files) and measure(seal)['mode']=='0o444',
  'all_directories_mode555':all(x['mode']=='0o555' for x in dirs)},indent=2))
