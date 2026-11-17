"""Finite passive own-lane seal. No source execution, network, Git, or writes outside this lane."""
import datetime, hashlib, json, os, stat, sys
from pathlib import Path

OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204212/reviews/scope-continuation-20261117')
TERMINALS=('FINAL_MANIFEST.json','FINAL_SEAL.json')
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def encoded(value):
    return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink()
    raw=p.read_bytes();b=p.lstat()
    fields=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    assert fields(a)==fields(b) and len(raw)==a.st_size
    return {'bytes':len(raw),'SHA256':hashlib.sha256(raw).hexdigest(),'MD5':hashlib.md5(raw).hexdigest(),'mode':oct(stat.S_IMODE(a.st_mode))}
def census():
    files={};dirs={'.':oct(stat.S_IMODE(OWN.lstat().st_mode))};todo=[OWN]
    while todo:
        here=todo.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            n=p.relative_to(OWN).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):
                dirs[n]=oct(stat.S_IMODE(s.st_mode));todo.append(p)
            elif n not in TERMINALS:
                files[n]=pin(p)
            else:
                assert stat.S_ISREG(s.st_mode)
        b=here.lstat()
        assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(b.st_dev,b.st_ino,b.st_mode,b.st_mtime_ns,b.st_ctime_ns)
    return files,dirs
for name in TERMINALS:
    assert not (OWN/name).exists()
inventory=json.loads((OWN/'PRIMARY_INVENTORY.json').read_bytes())
assert inventory['upstream_files_exact']==88 and inventory['primary_request_count']==99
assert inventory['identity_valid_primary_files']==98 and inventory['valid_classical_PDFs']==10
assert inventory['native_scientific_attempts']==1 and inventory['native_scientific_failures']==0
assert len(inventory['literal_transport_failures'])==1
assert inventory['complete_source_INITIAL_bytes_modes_hidden_empty_before_after_exact'] is True
before=json.loads((OWN/'CUSTODY_BEFORE.json').read_bytes())
after=json.loads((OWN/'CUSTODY_AFTER.json').read_bytes())
assert all(before[k]==after[k] for k in ('sources','INITIAL'))
for name in TERMINALS:
    with (OWN/name).open('xb'):
        pass
terminal_modes={n:oct(stat.S_IMODE((OWN/n).lstat().st_mode)) for n in TERMINALS}
files,dirs=census()
allpaths=set(files)|set(dirs)|set(TERMINALS)
hidden=sorted(n for n in allpaths if n!='.' and any(c.startswith('.') for c in n.split('/')))
emptydirs=sorted(n for n in dirs if n!='.' and not any(v.startswith(n+'/') for v in allpaths))
manifest={
    'schema':'finite-independent-review-complete-namespace-manifest-v1',
    'created_UTC':started,
    'namespace':str(OWN),
    'root_mode':dirs['.'],
    'file_count_including_terminal_pair':len(files)+2,
    'payload_file_count':len(files),
    'child_directory_count':len(dirs)-1,
    'payload_files':[dict(path=n,**p) for n,p in sorted(files.items())],
    'directories':[{'path':n,'mode':m} for n,m in sorted(dirs.items()) if n!='.'],
    'hidden_paths':hidden,
    'empty_files':sorted(n for n,p in files.items() if p['bytes']==0),
    'empty_directories':emptydirs,
    'terminal_control_files':[{'path':n,'bytes':0,'mode':terminal_modes[n],'SHA256_excluded_only_for_exact_terminal_pair':True} for n in TERMINALS],
    'exclusion_rule':'Only the SHA256/MD5 of the exact two terminal files FINAL_MANIFEST.json and FINAL_SEAL.json are excluded to avoid self-reference. Their final byte lengths and actual modes are included. No path, hidden, empty or directory exclusion applies.',
}
seal={
    'schema':'finite-independent-scope-review-seal-v1',
    'status':'FROZEN_COMPLETE_SCIENTIFIC_FAMILY_REVIEW',
    'record':'23204212','row':192,
    'completion_percent_assigned_bounded_review':100,
    'follow_up':None,
    'started_UTC':started,
    'immutable_initial_checkpoint':'a4267dc5366bb693dd565421271276677a060320',
    'upstream_commit':'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
    'manifest_identity':{'path':'FINAL_MANIFEST.json','bytes':0,'SHA256':'0'*64,'mode':terminal_modes['FINAL_MANIFEST.json']},
    'own_terminal_identity':{'path':'FINAL_SEAL.json','bytes':0,'mode':terminal_modes['FINAL_SEAL.json'],'self_hash_delivered_externally':True},
    'report_and_evidence_identities':{n:files[n] for n in ('FINAL_REPORT.md','SCIENTIFIC_REVIEW.md','DERIVATIONS.md','READING_LEDGER.md','WORKING_PROOF_CHECKS.md','RESEARCH_LOG.md','PRIMARY_INVENTORY.json','CUSTODY_BEFORE.json','CUSTODY_AFTER.json','NATIVE_RUN.json','NATIVE.stdout.txt','NATIVE.stderr.txt')},
    'source_files_child_directories':[55,14],
    'INITIAL_files_child_directories':[37,1],
    'complete_source_INITIAL_before_after_exact':True,
    'native_scientific_attempts':1,'native_scientific_failures':0,
    'literal_transport_content_failures_retained':1,
    'expected_data_diff_exit_one':'BCR_V3_V4_TEXT.diff retains actual frontmatter differences; both original editions retained.',
    'primary_request_count':99,'identity_valid_original_primary_files':98,
    'exact_upstream_files':88,'valid_classical_PDFs':10,
    'exposure_limit':'Original author assertions, later BUILD assertions and incidental unopen community/exposition search snippets disclosed in ledger. No current peer/root continuation findings read.',
    'scientific_limits':'Ordinary bounded proof and theorem-interface review. Finite native corroboration only. No fresh Lean build or semantic audit of all retrieved Lean files; no human peer-review guarantee or firstness claim. Actual mechanisms/disposition are in the private reports.',
    'action_limits':'Own-lane data/review writes only. No source/INITIAL/native Git/website/tracker/release/outreach mutation or publication authority.',
    'finalization_argv':[sys.executable,*sys.argv],
    'terminal_protocol':'Manifest lists all payload hashes and complete topology; both exact terminal lengths/modes are solved to a finite byte-length fixed point. Seal hashes manifest. External recipient receives seal hash. No writes after final verification.',
}
for unused in range(20):
    lengths=(len(encoded(manifest)),len(encoded(seal)))
    for row in manifest['terminal_control_files']:
        row['bytes']=lengths[TERMINALS.index(row['path'])]
    seal['manifest_identity']['bytes']=lengths[0]
    seal['own_terminal_identity']['bytes']=lengths[1]
    if lengths==(len(encoded(manifest)),len(encoded(seal))):
        break
else:
    raise AssertionError('terminal byte-length fixed point not reached')
mraw=encoded(manifest)
seal['manifest_identity']['SHA256']=hashlib.sha256(mraw).hexdigest()
sraw=encoded(seal)
assert (len(mraw),len(sraw))==lengths
for name,raw in zip(TERMINALS,(mraw,sraw)):
    with (OWN/name).open('wb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
assert census()==(files,dirs)
for name,raw in zip(TERMINALS,(mraw,sraw)):
    actual=pin(OWN/name)
    row=next(r for r in manifest['terminal_control_files'] if r['path']==name)
    assert actual['bytes']==row['bytes'] and actual['mode']==row['mode']
    assert actual['SHA256']==hashlib.sha256(raw).hexdigest()
assert pin(OWN/'FINAL_MANIFEST.json')['SHA256']==seal['manifest_identity']['SHA256']
assert json.loads((OWN/'FINAL_MANIFEST.json').read_bytes())==manifest
assert json.loads((OWN/'FINAL_SEAL.json').read_bytes())==seal
print(json.dumps({'status':seal['status'],'file_count':manifest['file_count_including_terminal_pair'],'child_directory_count':manifest['child_directory_count'],'hidden_paths':manifest['hidden_paths'],'empty_file_count':len(manifest['empty_files']),'empty_directories':manifest['empty_directories'],'FINAL_MANIFEST':pin(OWN/'FINAL_MANIFEST.json'),'FINAL_SEAL':pin(OWN/'FINAL_SEAL.json'),'FINAL_REPORT':pin(OWN/'FINAL_REPORT.md'),'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()},ensure_ascii=False))
