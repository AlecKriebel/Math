#!/usr/bin/env python3
"""Read-only, source-free integrity and mutation controls for the frozen packet.
Usage: python3 audit_checks.py PATH_TO_FROZEN_PUBLIC [PATH_TO_CORPUS_DIRECTORY]
The optional corpus directory is read only; no dataset contents are emitted.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

EXPECTED_MANIFEST_SHA256 = '10a8affedf81c5d559356b842c6d7216f88c1fb143d66dce667f62804b4d013b'
EXPECTED_FILES = {'BRIDGE_LEMMAS.md','CHECK_RESULTS.json','PROOF.md','README.md','SOURCE_AUDIT.md','SOURCE_METADATA.json','TURN_LEDGER.json','verify.py','MANIFEST.sha256'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

root = pathlib.Path(sys.argv[1])
manifest_bytes = (root/'MANIFEST.sha256').read_bytes()
assert digest(manifest_bytes) == EXPECTED_MANIFEST_SHA256
assert {p.name for p in root.iterdir() if p.is_file()} == EXPECTED_FILES
assert not any(p.is_symlink() for p in root.iterdir())
entries = []
for line in manifest_bytes.decode().splitlines():
    sha, filename = line.split('  ',1)
    assert filename in EXPECTED_FILES - {'MANIFEST.sha256'}
    data = (root/filename).read_bytes()
    assert digest(data) == sha
    entries.append({'filename':filename,'bytes':len(data),'sha256':sha})
assert len(entries) == 8
original = (root/'verify.py').read_text()
run = subprocess.run([sys.executable,'-c',original], capture_output=True, text=True)
assert run.returncode == 0, run.stderr
result = json.loads(run.stdout)
assert result == json.loads((root/'CHECK_RESULTS.json').read_text())
assert result['all_passed'] and result['check_count'] == 20
controls = []
for label, before, after, expected_failure in [
    ('wrong stereographic scale','return (2*a/(1+r),','return (3*a/(1+r),','stereographic image lies on sphere'),
    ('reversed contraction parameter','h = Q((1-t)*u, (1-t)*v)','h = Q(t*u, t*v)','contraction start is identity in plane chart'),
    ('wrong cycle coefficient','fundamental=sp.Matrix([-1,1,-1,1])','fundamental=sp.Matrix([1,1,-1,1])','tetrahedron oriented boundary is a cycle'),
    ('coalesced quotient classes',"classes={0:{'north'},1:{'punctured_sphere'}}","classes={0:{'north'},1:{'north'}}",'all four subsets of the two-point quotient enumerated'),
]:
    assert original.count(before) == 1
    changed = original.replace(before,after)
    test = subprocess.run([sys.executable,'-c',changed],capture_output=True,text=True)
    assert test.returncode != 0 and expected_failure in test.stderr
    controls.append({'name':label,'rejected':True,'failed_check':expected_failure})
# A byte mutation is checked in memory. The frozen file is never edited.
proof_bytes = (root/'PROOF.md').read_bytes()
proof_sha = next(e['sha256'] for e in entries if e['filename']=='PROOF.md')
assert digest(proof_bytes+b'\n') != proof_sha
controls.append({'name':'single appended newline in proof','rejected':True,'failed_check':'SHA-256 comparison'})
corpus = None
if len(sys.argv)>2:
    directory=pathlib.Path(sys.argv[2])
    metadata=json.loads((root/'SOURCE_METADATA.json').read_text())
    corpus=[]
    loaded={}
    for item in metadata['public_corpus_local_byte_verification']:
        data=(directory/item['basename']).read_bytes()
        assert len(data)==item['bytes'] and digest(data)==item['sha256']
        corpus.append(dict(item,verified=True))
        loaded[item['basename']]=json.loads(data)
    matches=[p for p in loaded['problems.json'] if p.get('id')==30001405 or p.get('problem_number')=='OWR-4196-003']
    assert len(matches)==1
    assert matches[0]['id']==30001405 and matches[0]['problem_number']=='OWR-4196-003'
    research=loaded['research_results.json']
    assert 'OWR-4196-003' not in research and '30001405' not in research
print(json.dumps({
    'frozen_manifest_sha256':EXPECTED_MANIFEST_SHA256,
    'manifest_verified':True,'exact_public_allowlist_verified':True,
    'frozen_entries':entries,
    'author_diagnostics_reproduced':20,
    'diagnostic_json_matches_frozen_record':True,
    'negative_controls':controls,
    'corpus_byte_verification':corpus,
    'corpus_match_count':1 if corpus else None,
    'research_exact_code_key_present':False if corpus else None,
    'research_exact_numeric_key_present':False if corpus else None,
    'mutations_executed_in_memory_only':True,
    'formal_proof_checker_run':False,
    'limitations':'These controls test exact algebra, finite chains, enumeration, and packet integrity. They do not formalize model theory, topology, source interpretation, or the absence of later results.'
},indent=2))
