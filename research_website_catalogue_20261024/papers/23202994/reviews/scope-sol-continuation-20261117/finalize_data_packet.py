"""Passive full final guards and finite packet seal; no scientific/Git execution."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'papers/23202994/reviews/scope-sol-continuation-20261117'
SOURCE = P / 'papers/23202994/sources'
INITIAL = P / 'papers/23202994/reviews/scope-sol'
TERMINALS = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json'}

def row(path):
    first = path.lstat()
    assert stat.S_ISREG(first.st_mode) and not path.is_symlink()
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(fd)
        assert (opened.st_dev, opened.st_ino) == (first.st_dev, first.st_ino)
        chunks = []
        while True:
            part = os.read(fd, 1048576)
            if not part:
                break
            chunks.append(part)
        last = os.fstat(fd)
        assert (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mode, opened.st_mtime_ns, opened.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_size, last.st_mode, last.st_mtime_ns, last.st_ctime_ns)
        assert (path.lstat().st_dev, path.lstat().st_ino) == (last.st_dev, last.st_ino)
        raw = b''.join(chunks)
        assert len(raw) == last.st_size
        return dict(bytes=len(raw), SHA256=hashlib.sha256(raw).hexdigest(), mode=format(stat.S_IMODE(last.st_mode), '04o'))
    finally:
        os.close(fd)

def census(root):
    files, directories = {}, {}
    stack = [root]
    while stack:
        here = stack.pop()
        first = here.lstat()
        assert stat.S_ISDIR(first.st_mode) and not here.is_symlink()
        for path in sorted(here.iterdir()):
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISDIR(info.st_mode):
                assert not path.is_symlink()
                directories[rel] = format(stat.S_IMODE(info.st_mode), '04o')
                stack.append(path)
            else:
                files[rel] = row(path)
        last = here.lstat()
        assert (first.st_dev, first.st_ino, first.st_mode, first.st_mtime_ns, first.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_mode, last.st_mtime_ns, last.st_ctime_ns)
    return dict(root=str(root), root_mode=format(stat.S_IMODE(root.lstat().st_mode), '04o'), files=files, directories=directories)

def write_json(name, value):
    with (OWN / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')

started = datetime.datetime.now(datetime.timezone.utc).isoformat()
before = json.loads((OWN / 'GUARDS_BEFORE.json').read_bytes())
source, initial = census(SOURCE), census(INITIAL)
assert source == before['source'] and initial == before['immutable_INITIAL']
assert (len(source['files']), len(source['directories']), len(initial['files']), len(initial['directories'])) == (39, 15, 38, 3)
write_json('GUARDS_AFTER.json', dict(schema='row190-continuation-full-after-guards-v1', UTC=started, source=source, immutable_INITIAL=initial, exact_before_after=True))
primary = census(OWN / 'primary')
assert len(primary['files']) == 29
receipt = json.loads((OWN / 'ATOMIC_RUN_RECEIPT.json').read_bytes())
assert receipt['exit_code'] == 0 and receipt['stdout_bytes'] == receipt['stderr_bytes'] == 0
assert receipt['input_namespace_unchanged'] and receipt['before'] == receipt['after']
copies = census(OWN / 'run-atomic')
assert {k:copies[k] for k in ('root_mode','files','directories')} == receipt['after']
for item in json.loads((OWN / 'PRIMARY_FETCH_RECEIPTS.json').read_bytes())['files']:
    actual = primary['files'][item['path']]
    assert actual['bytes'] == item['bytes'] and actual['SHA256'] == item['sha256']
for item in json.loads((OWN / 'PDF_FETCH_RECEIPTS.json').read_bytes()):
    actual = primary['files'][item['name']]
    assert actual['bytes'] == item['bytes'] and actual['SHA256'] == item['SHA256'] and item['exact_native_match']
script_reads = {name: dict(**row(OWN/name), personally_read_full_before_its_execution=True) for name in ('guard_before.py','fetch_primary_pdfs.py','run_selected_once.py','finalize_data_packet.py')}
write_json('UTILITY_READ_ATTESTATION.json', dict(schema='row190-saved-read-utility-pins-v1', UTC=started, scripts=script_reads, scientific_entrypoint=receipt['before']['files']['verification/check_certificate.py'], scientific_entrypoint_full_read_before_run=True, imports='Only standard-library modules in owned custody wrappers and the atomic checker; no source producer imported'))
finished = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (OWN/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n'+finished+' — Fullsource39/15 andimmutableINITIAL38/3 exactly unchanged includingallbytes/modes/root/topology;29primaryfiles and6atomicruninputs authenticated. Allscopedreports/readlimits complete. Finalfinitepacket sealed; completion100% of thisfamilycontinuation. No productionauthority or furtherwork; quiescentstop.\n')
write_json('FINALIZATION_RECEIPT.json', dict(schema='row190-passive-seal-execution-v1', argv=['python3','-B',str(OWN/'finalize_data_packet.py')], started_UTC=started, finished_UTC=finished, source_and_INITIAL_exact=True, primary_files=29, scientific_route_attempts=1, scientific_exit=0, mutation_scope='Only own continuation sibling', no_Git_or_scientific_call_in_finalizer=True))
write_json('FINAL.json', dict(schema='row190-scope-family-continuation-FINAL-v1', status='COMPLETE_SCOPED_ANALYTIC_REVIEW', completed_UTC=finished, completion_percent=100, completion_scope='Bounded independent scope-family review, not overall research/publication', owned_root=str(OWN), immutable_INITIAL_seal=row(INITIAL/'INITIAL_SEAL.json'), immutable_INITIAL_manifest=row(INITIAL/'INITIAL_MANIFEST.json'), source_files_dirs=[39,15], INITIAL_files_dirs=[38,3], source_INITIAL_exact_before_after=True, primary_pin='adc7f1241b42e322a6451854ab7e4b4c146bf78a', primary_fetched_files=29, primary_changed_copies=[], scientific_attempts=1, scientific_route='ATOMIC documented ordinary inner route only', scientific_exit_code=receipt['exit_code'], scientific_stdout_stderr_bytes=[0,0], fresh_MAIN_comparisons=0, fresh_atomic_Bernstein_row_minima=659, evidence_scope='Primary full analytic core/atomic proof checked by hand separately from finite arithmetic; exact interfaces and corrected classical application recorded', precise_chain_material_gap_identified=None, known_qualified_issue='Unrestricted addendumLemma1 neighborhood wording false; actual compact regular thickening application checked explicitly', follow_up=None, findings_report='CONTINUATION_REPORT.md', proof_artifacts=['PRIMARY_PROOF_CHECKS.md','THEOREM_INTERFACE.md','CHECK_PLAN_RESULTS.json'], limits=['No fresh MAIN37,310+10 execution in this family','No formal kernel/Lean/Mathlib/Comparator build or axiom audit','No human refereeing or exhaustive current priority survey','No fresh primary retrieval of BHS/KS/HSS/HLSS in this family','No certification of excluded jellium/critical-s/uniqueness/second-order claims','Other current families and root mathematical findings not read','No Git/native/index/config/W/Sheet/deploy/release or outreach authority exercised'], source_guards_file='GUARDS_AFTER.json', terminal_self_hash_exclusions=sorted(TERMINALS), final_state='Frozen finite namespace; stop after read-only terminal verification'))
extent = census(OWN)
assert not (set(extent['files']) & TERMINALS)
rows = [dict(path=name, **data) for name,data in sorted(extent['files'].items())]
rows += [dict(path=name, terminal_control=True, mode='0644', self_hash_excluded=True, exclusion_reason='Exact terminal circular/self-hash exclusion only') for name in sorted(TERMINALS)]
directories = [dict(path=name, mode=mode) for name,mode in sorted(extent['directories'].items())]
manifest = dict(schema='row190-finite-FINAL-manifest-v1', owned_root=str(OWN), root_mode=extent['root_mode'], completed_UTC=finished, files=rows, directories=directories, counts=dict(files=len(rows), directories=len(directories)), terminal_controls=sorted(TERMINALS), no_hidden_empty_exclusions=True)
write_json('FINAL_MANIFEST.json', manifest)
nonterminal_hashes = {name:data for name,data in extent['files'].items()}
seal = dict(schema='row190-finite-FINAL-seal-v1', status='FROZEN', completed_UTC=finished, manifest=row(OWN/'FINAL_MANIFEST.json'), FINAL=row(OWN/'FINAL.json'), guards_after=row(OWN/'GUARDS_AFTER.json'), namespace_files=sorted(set(nonterminal_hashes)|TERMINALS), directories=directories, root_mode=extent['root_mode'], counts=manifest['counts'], exact_terminal_self_hash_exclusions=sorted(TERMINALS), hidden_paths=[p for p in sorted(set(nonterminal_hashes)|set(extent['directories'])) if any(c.startswith('.') for c in p.split('/'))], empty_files=[p for p,v in sorted(nonterminal_hashes.items()) if v['bytes']==0], empty_directories=[p for p in sorted(extent['directories']) if not any(q.startswith(p+'/') for q in set(nonterminal_hashes)|set(extent['directories']))], no_further_writes=True)
write_json('FINAL_SEAL.json', seal)
actual = census(OWN)
assert set(actual['files']) == set(seal['namespace_files']) and actual['directories'] == extent['directories'] and actual['root_mode'] == extent['root_mode']
for name,data in nonterminal_hashes.items():
    assert actual['files'][name] == data
for name in TERMINALS:
    assert actual['files'][name]['mode'] == '0644'
assert actual['files']['FINAL_MANIFEST.json'] == seal['manifest']
assert census(SOURCE) == source and census(INITIAL) == initial
print(json.dumps(dict(status='FROZEN', counts=manifest['counts'], FINAL=actual['files']['FINAL.json'], manifest=actual['files']['FINAL_MANIFEST.json'], seal=actual['files']['FINAL_SEAL.json'], source_and_INITIAL_exact=True)))
