#!/usr/bin/env python3
"""Final held namespace: native complete payload capture plus two external pins.

Only the manifest and its native capture are excluded from their own inventory.
Their actual native hashes/modes/full streams are emitted in the final stdout;
the canonical footer covers all files and directory modes with no exclusions.
No namespace write occurs after manifest creation. ROOT must close externally.
"""
from pathlib import Path
import hashlib,json,re,stat,subprocess,sys,time
if not __debug__:raise SystemExit('Assertions must remain enabled.')
N=Path(__file__).resolve().parent.parent
MAN=N/'FULL_REVIEW_FREEZE.json'
CAP=N/'phase3/FINAL_NATIVE_CAPTURE.json'
CLOCK=['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ']
sha=lambda b:hashlib.sha256(b).hexdigest()
def utc():
    p=subprocess.run(CLOCK,capture_output=True,check=True)
    return p.stdout.decode().strip()
def native(argv):
    start=utc();tm=time.monotonic_ns()
    p=subprocess.run(argv,cwd=N,capture_output=True,check=False)
    rec={'argv':argv,'cwd':str(N),'utc_start':start,'utc_end':utc(),'clock_argv':CLOCK,
         'elapsed_monotonic_ns':time.monotonic_ns()-tm,'exit_status':p.returncode,
         'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),
         'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),
         'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    if p.returncode or p.stderr:
        print(json.dumps({'actual_failed_native_receipt':rec},indent=2));raise SystemExit(p.returncode or 1)
    return rec
def paths():
    p=sorted([N]+list(N.rglob('*')),key=lambda p:str(p.relative_to(N)))
    assert all(not q.is_symlink() and (q.is_dir() or q.is_file()) for q in p)
    assert all('\n' not in str(q) and '|' not in str(q) for q in p)
    return p
def rel(p):return '.' if p==N else str(p.relative_to(N))
def inventory(p):
    result=[]
    for q in p:
        s=q.stat();o={'path':rel(q),'type':'directory' if q.is_dir() else 'file',
                     'mode_octal':format(stat.S_IMODE(s.st_mode),'04o')}
        if q.is_file():o.update(bytes=s.st_size,sha256=sha(q.read_bytes()))
        result.append(o)
    return result
def validate_native(rows,hashes,modes):
    hs={}
    for line in hashes['stdout'].splitlines():
        m=re.fullmatch(r'([0-9a-f]{64})  (.*)',line);assert m,line
        hs[m.group(2)]=m.group(1)
    assert hs=={o['path']:o['sha256'] for o in rows if o['type']=='file'}
    ms={}
    for line in modes['stdout'].splitlines():
        name,kind,mode,size=line.rsplit('|',3)
        ms[name]={'mode_octal':format(int(mode,8),'04o'),'kind':kind,'bytes':int(size)}
    assert set(ms)=={o['path'] for o in rows}
    for o in rows:
        v=ms[o['path']];assert v['mode_octal']==o['mode_octal']
        assert v['kind']==('Directory' if o['type']=='directory' else 'Regular File')
        if o['type']=='file':assert v['bytes']==o['bytes']
assert not MAN.exists() and not CAP.exists()
assert sha((N/'phase3/WHOLE_PREPRINT_REVIEW.md').read_bytes())=='b57dccf88075f88ac1eb235c17eba9f2d83bf2d50548bdff057ee6f8b7fdf331'
ledger=json.loads((N/'phase3/CLAIM_STATUS.json').read_text())
assert len(ledger['claims'])==74 and all(r['exact_mathematical_gap'] is None for r in ledger['claims'])
assert ledger['publication_approval'] is False
script_sha=sha(Path(__file__).read_bytes());checkpoint=utc()
with (N/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+checkpoint+': Final whole-review namespace freeze initiated. Mathematical audit100%; reviewer artifact preparation100%; external ROOT closure remains pending. All74 original IDs closed in the exact manuscript scope, no candidate repair requested. Universal proof and all-specialization source applicability are distinguished from finite tests; the plane-image collision and historical priority/provenance limits remain attached. Original source/first-candidate bodies and modes were verified unchanged, the log only appended, and both family namespaces exactly held. Final native hash/mode receipt and manifest have only their own two explicit exclusions; a final native stdout supplies their exact pins and a self-inclusive whole-tree canonical digest for ROOT external validation. No publication/self-seal is granted. HOLD unchanged after the final manifest write.\n')
payload_paths=paths();payload_rows=inventory(payload_paths)
hash_receipt=native(['/usr/bin/shasum','-a','256']+[rel(p) for p in payload_paths if p.is_file()])
mode_receipt=native(['/usr/bin/stat','-f','%N|%HT|%OLp|%z']+[rel(p) for p in payload_paths])
validate_native(payload_rows,hash_receipt,mode_receipt)
assert inventory(payload_paths)==payload_rows
capture={'stage':'whole-preprint-final-native-payload-capture','namespace':str(N),
         'freeze_checkpoint_utc':checkpoint,'execution_argv_literal':['/opt/homebrew/bin/python3','-B',str(Path(__file__).resolve())],
         'observed_sys_executable':sys.executable,
         'executed_body_sha256_before':script_sha,'executed_body_sha256_after':sha(Path(__file__).read_bytes()),
         'explicit_only_self_reference_exclusions':['FULL_REVIEW_FREEZE.json','phase3/FINAL_NATIVE_CAPTURE.json'],
         'complete_native_file_hash_receipt':hash_receipt,'complete_native_modes_receipt':mode_receipt,
         'publication_approval':False}
CAP.write_text(json.dumps(capture,indent=2)+'\n')
manifest={'stage':'whole-preprint-review-complete-held-for-external-ROOT-closure','namespace':str(N),
          'freeze_checkpoint_utc':checkpoint,'mathematical_audit_percent':100,'reviewer_artifact_preparation_percent':100,
          'stable_claim_ids':74,'remaining_mathematical_gaps':0,'candidate_repair_requested':False,
          'publication_approval':False,'self_certification':False,
          'only_inventory_exclusions':['FULL_REVIEW_FREEZE.json','phase3/FINAL_NATIVE_CAPTURE.json'],
          'self_reference_boundary':'Only these two final-created bodies cannot hash themselves. The final actual native stdout contains both hashes/modes/full streams and the self-inclusive canonical digest. All other files, modes and every directory mode are in objects. ROOT must pin every object independently; this is not release approval.',
          'native_full_stream_capture':'phase3/FINAL_NATIVE_CAPTURE.json','objects':payload_rows,
          'whole_review':'phase3/WHOLE_PREPRINT_REVIEW.md','claim_ledger':'phase3/CLAIM_STATUS.json',
          'remaining_operational_gap':'External ROOT complete namespace closure and any separately authorized downstream publication.',
          'historical_limit_report':'phase3/SOURCE_PUBLIC_PACKET_REPORT.md','hold':'UNCHANGED after this manifest write until explicit ROOT release.'}
MAN.write_text(json.dumps(manifest,indent=2)+'\n')
# Final write completed. Nothing below writes any namespace object.
excluded=sorted([MAN,CAP],key=rel)
excluded_rows=inventory(excluded)
excluded_hash=native(['/usr/bin/shasum','-a','256']+[rel(p) for p in excluded])
excluded_modes=native(['/usr/bin/stat','-f','%N|%HT|%OLp|%z']+[rel(p) for p in excluded])
validate_native(excluded_rows,excluded_hash,excluded_modes)
all_paths=paths();all_rows=inventory(all_paths)
assert [o for o in all_rows if o['path'] not in manifest['only_inventory_exclusions']]==payload_rows
assert [o for o in all_rows if o['path'] in manifest['only_inventory_exclusions']]==excluded_rows
canonical=(json.dumps(all_rows,sort_keys=True,separators=(',',':'))+'\n').encode()
footer={'namespace':str(N),'hold_utc':utc(),'all_namespace_files_and_directory_modes_included':True,
        'files':sum(o['type']=='file' for o in all_rows),'directories':sum(o['type']=='directory' for o in all_rows),
        'canonical_inventory_encoding':"json.dumps(sorted object rows,sort_keys=True,separators=(',',':')) plus LF, UTF-8",
        'canonical_inventory_sha256':sha(canonical),'only_on_disk_inventory_exclusions':excluded_rows,
        'actual_native_excluded_hash_receipt':excluded_hash,'actual_native_excluded_modes_receipt':excluded_modes,
        'native_payload_capture_sha256':sha(CAP.read_bytes()),'manifest_sha256':sha(MAN.read_bytes()),
        'executed_body_sha256_before':script_sha,'executed_body_sha256_after':sha(Path(__file__).read_bytes()),
        'stable_claim_ids':74,'remaining_mathematical_gaps':0,'publication_approval':False,
        'self_certification':False,'hold':'UNCHANGED, external ROOT closure required.'}
print('FINAL_SELF_INCLUSIVE_NATIVE_FOOTER_BEGIN')
print(json.dumps(footer,indent=2))
print('FINAL_SELF_INCLUSIVE_NATIVE_FOOTER_END')
