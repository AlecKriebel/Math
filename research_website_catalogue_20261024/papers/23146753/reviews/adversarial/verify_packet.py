"""Read-only verifier: no replay, network, rendering, or filesystem writes."""
from pathlib import Path, PurePosixPath
import hashlib, json, re, stat, zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / 'sources'
def get(name):
    return json.loads((HERE / name).read_text())
def check(condition, message):
    if not condition:
        raise RuntimeError(message)
def binding(p):
    data = p.read_bytes()
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())

custody = get('CUSTODY.json')
for p, spec in custody['original_bindings'].items():
    check(binding(Path(p)) == spec, 'Original input changed: ' + p)
for p, spec in get('SOURCE_BINDINGS_BEFORE.json')['files'].items():
    check(binding(Path(p)) == spec, 'Before binding changed: ' + p)
early = get('INITIAL_SEAL.json')
check(binding(HERE/'INITIAL_RECONSTRUCTION.md')['sha256'] == early['reconstruction_sha256'], 'Initial reconstruction changed')
check(binding(HERE/'INITIAL_READ_LEDGER.json')['sha256'] == early['read_ledger_sha256'], 'Initial read ledger changed')
check(binding(HERE/'INITIAL_SEAL.json') == custody['preserved_early_seal'], 'Initial seal changed')
objects = get('ORIGINAL_SOURCE_OBJECTS.json')['originals']
for name, original in objects.items():
    check(json.loads((SOURCE/name).read_text()) == original, 'Original object drift: '+name)
ready = objects['SOURCE_READY.json']
raw = objects['record.raw.json']
check(ready['all_assets'][0]['original_api_file_object']['key'].endswith('.zip'), 'Original file order changed')
check([x['original_api_file_object'] for x in ready['all_assets']] == raw['files'], 'Actual API object mismatch')
for asset in ready['all_assets']:
    p = Path(asset['path'])
    data = p.read_bytes()
    check(len(data) == asset['bytes'] == asset['original_api_file_object']['size'], 'Asset size')
    check(hashlib.sha256(data).hexdigest() == asset['sha256'], 'Asset SHA256')
    check(hashlib.md5(data).hexdigest() == asset['md5'], 'Asset MD5')
    check(asset['original_api_file_object']['checksum'] == 'md5:'+asset['md5'], 'API checksum')
with zipfile.ZipFile(SOURCE/'mtp2-edge-closure-verification.zip') as z:
    check(len(z.infolist()) == 13, 'Member count')
    for info in z.infolist():
        name = PurePosixPath(info.filename)
        mode = info.external_attr >> 16
        check(not name.is_absolute() and '..' not in name.parts and not info.is_dir(), 'Unsafe member path')
        check(not mode or stat.S_ISREG(mode), 'Nonregular member')
        check(z.read(info) == (SOURCE/'published-source'/info.filename).read_bytes(), 'Member mismatch')
check((SOURCE/'published-source/output/pdf/mtp2_edge_closure.pdf').read_bytes() ==
      (SOURCE/'mtp2-edge-closure-note.pdf').read_bytes(), 'Embedded reader')
tex = (SOURCE/'published-source/mtp2_edge_closure.tex').read_text()
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
check(abstract == get('READ_LEDGER.json')['original_abstract'] == get('INITIAL_READ_LEDGER.json')['original_abstract'], 'Full original abstract')
results = get('CONTROL_RESULTS.json')
check(results['driver_sha256'] == binding(HERE/'independent_controls.py')['sha256'], 'Control driver binding')
check(sum(x['feasible_graph_support_pairs'] for x in results['support_geometry']) == 18067, 'Support controls')
check(sum(x['incomparable_squares'] for x in results['support_geometry']) == 18202, 'Witness controls')
check(results['residual']['networks'] == 900 and results['residual']['all_cut_equalities'] == 13176, 'Flow controls')
check(results['residual']['wrong_minus_reverse_formula_rejected'] == 520, 'Wrong-sign rejection')
check(results['examples']['naive_smoothing_ratio'] == '1/4', 'Smoothing rejection')
check(results['examples']['c4_quartic'] == ['1/6561','2/6561'], 'Prior-law obstruction')
for job in get('EXECUTION_LEDGER.json')['jobs']:
    label = job['label']
    check(job['expected_outcome_observed'], 'Execution failed: '+label)
    check(binding(HERE/(label+'.stdout.txt'))['sha256'] == job['stdout_sha256'], 'Execution stdout')
    check(binding(HERE/(label+'.stderr.txt'))['sha256'] == job['stderr_sha256'], 'Execution stderr')
check(not (HERE/'SHOULD_NOT_EXIST.json').exists(), 'Assertion guard wrote output')
replay = HERE/'cache/source-replay'
check(json.loads((replay/'boundary.stdout').read_text()) ==
      json.loads((SOURCE/'published-source/expected/boundary.json').read_text()), 'Published boundary replay')
check((replay/'priority_laws.json').read_bytes() ==
      (SOURCE/'published-source/expected/priority_laws.json').read_bytes(), 'Published priority replay')
verdict = get('VERDICT.json')
check(verdict['status']=='COMPLETE' and verdict['central_mathematical_gap'] is None, 'Verdict inconsistency')
for field in ['publication_authority','public','rendered','browser_verified','native_verified']:
    check(verdict[field] is False, 'Publication gate changed')
for field in ['canonical','AA','root_adoption','final_followup']:
    check(verdict[field] is None, 'Null authority changed')
check((HERE/'.gitignore').read_text() == 'cache/\n', 'Private cache ignore')
expected_prior = {
 'papers/23333353/reviews/editorial/SEAL.json':'710eb0204715bd7301b38cf411469b97990b4f8002d00bc4a4c8f54627247505',
 'papers/23416806/reviews/editorial/SEAL.json':'5163f1cb9b06f3d902fe89544137b3153d43a119b24398b21ece3542158c41dc',
 'papers/23441617/reviews/editorial/SEAL.json':'7634ac812df4357ab80a245a4e710047e640a0cc553ffb3c13d4e9fef085f898',
 'papers/23217863/reviews/scope/FINAL_SEAL.json':'57d85decc1a851cd9c9d245521e9e0c17c002c1a3e98a2d1d606f26703b0780b',
 'verification/ambient-block-modulus-navigation-correction-sol-20261025/SEAL.json':'49326baa81bbc183e1c3e81a96f2ec31393a0e8d9bb3100d96da07cb5b6aadde',
 'verification/checkpoint-subtree-diagnostic-sol-20261025/SEAL.json':'84343c587e15941e389d1aec31077a047f0b556735e116660d1a077770a8a6ec',
}
P = HERE.parents[3]
for name, digest in expected_prior.items():
    check(binding(P/name)['sha256'] == digest, 'Earlier immutable seal changed: '+name)
manifest_path = HERE/'FINAL_MANIFEST.json'
if manifest_path.exists():
    manifest = get('FINAL_MANIFEST.json')
    for name, spec in manifest['owned_bindings'].items():
        check(binding(HERE/name) == spec, 'Owned binding changed: '+name)
    current = {str(x.relative_to(HERE)) for x in HERE.rglob('*') if x.is_file()}
    check(current == set(manifest['owned_bindings']) | {'FINAL_MANIFEST.json','FINAL_SEAL.json'}, 'Unexpected/missing owned file')
    if (HERE/'FINAL_SEAL.json').exists():
        seal = get('FINAL_SEAL.json')
        check(binding(manifest_path) == seal['manifest_binding'], 'Manifest seal mismatch')
print(json.dumps(dict(status='PASS_READ_ONLY_PACKET_VERIFICATION', original_bindings=len(custody['original_bindings']),
                     before_source_bindings=25, current_source_bindings=27, archive_members=13,
                     sealed=manifest_path.exists(), writes=False, program_replays=False),indent=2))
