"""Pinned integrity replay. This program does not certify mathematical truth."""
import argparse
import hashlib
import io
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath
import verify_source_pins as sources

NAMES = sorted(['ACCEPTANCE.json', 'AUTHOR_EXTERNAL_MANIFEST.json', 'AUTHOR_SAFE_FREEZE.zip',
    'CORRECTED_EXTERNAL_MANIFEST.json', 'CORRECTED_SAFE.zip', 'CORRECTION.patch',
    'INDEPENDENT_AUDIT.md', 'PATCH_REPLAY.json', 'README.md', 'SOURCE_INSPECTION.json',
    'SOURCE_PIN_RESULTS.json', 'verify_source_pins.py', 'verify_package.py', 'test_integrity.py',
    'ARTIFACT_TEST_RESULTS.json', 'REPLAY_RESULTS.json', 'AUTHOR_STATIC_REPLAY.json'])
AUTHOR_NAMES = ['README.md', 'approach_log.md', 'checks.json', 'proof.md', 'source_metadata.json', 'status.md']
PINS = {
 'AUTHOR_SAFE_FREEZE.zip': ('195733cfb3eea7909a667f4a1f7b71ca39abb516f89e2f4803040a31c2525c6d', 12373),
 'AUTHOR_EXTERNAL_MANIFEST.json': ('2c3077fb9ba088ef767a679036152c436e781119d805abf17908418c24a438c2', 1426),
 'CORRECTED_SAFE.zip': ('245fb3371e9ffb1397e104e75232403b16470c580850124cbd39f4243dc32cee', 12382),
 'CORRECTED_EXTERNAL_MANIFEST.json': ('219c543e554f2f9ca9eab0cad34e365fb8b692a8487a31d85ea5260c979e53b1', 1942),
 'CORRECTION.patch': ('71938f29d9b098416eda2d8fd7f3146eca3e04c73b557d4fc44015fe4b0310a6', 2029),
}
DECISION = 'ACCEPT_CORRECTED_RESTRICTED_PARTIAL'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, reason):
    if not condition:
        raise ValueError(reason)

def parse(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=unique)

def unpack(data, names):
    require(len(data) < 3000000, 'archive size limit')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        require(z.namelist() == names, 'archive inventory/order/duplicates')
        require(sum(i.file_size for i in z.infolist()) < 3000000, 'uncompressed limit')
        out = {}
        for i in z.infolist():
            p = PurePosixPath(i.filename)
            require(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename, 'unsafe path')
            mode = i.external_attr >> 16
            require(stat.S_ISREG(mode) and not mode & 0o111 and not i.flag_bits & 1, 'unsafe member type/mode/encryption')
            require(not i.is_dir(), 'directory member')
            out[i.filename] = z.read(i)
        return out

def inner(archive, manifest):
    meta = parse(manifest)
    require(meta['archive']['bytes'] == len(archive) and meta['archive']['sha256'] == sha(archive), 'inner archive metadata')
    require([x['path'] for x in meta['files']] == AUTHOR_NAMES, 'inner manifest inventory')
    data = unpack(archive, AUTHOR_NAMES)
    for x in meta['files']:
        require(len(data[x['path']]) == x['bytes'] and sha(data[x['path']]) == x['sha256'], 'inner member digest')
    require(meta['mathematical_status'] == 'stopped_partial_not_solved', 'inner mathematical status')
    require(meta['approaches_used'] == 4 and meta['approach_limit'] == 5 and meta['novelty_claimed'] is False, 'inner scope')
    require(meta['executable_files'] == [], 'original executable claim')
    return data

def check_source_evidence(result, inspection):
    require(result['status'] == 'PASS', 'source result status')
    require(result['problem_id'] == 2875 and result['rank'] == 916, 'source identity')
    require(result['complete_pair_sha256'] == sources.PAIR_SHA and result['complete_pair_bytes'] == 5695, 'source pair evidence')
    require(result['statement_sha256'] == sources.STATEMENT_SHA, 'source statement evidence')
    require(result['full_corpus_count'] == 3 and result['pdf_count'] == 5, 'source count evidence')
    require(result['exact_record_count'] == 1 and result['associated_report_empty'] is True, 'record evidence')
    rows = result['source_checks']
    require([x['source_label'] for x in rows] == list(sources.PINS), 'source inventory evidence')
    for x in rows:
        size, digest = sources.PINS[x['source_label']]
        require(x['bytes'] == size and x['sha256'] == digest and x['matches_expected'] is True, 'source evidence pin')
    pdfs = inspection['primary_sources']
    require([x['source_label'] for x in pdfs] == ['k3','fkr','bfs','long_reid','hatcher'], 'inspection inventory')
    for x in pdfs:
        size, digest = sources.PINS[x['source_label']]
        require(x['bytes'] == size and x['sha256'] == digest and x['pdf_readable'] is True, 'inspection evidence pin')
        require(x['fresh_text_matches_retained_text'] is True and x['inspection_scope'], 'inspection text evidence')
    require(len(inspection['inspection_limits']) >= 6, 'inspection limits')

def check_core(files):
    for name, (digest, size) in PINS.items():
        require(name in files and len(files[name]) == size and sha(files[name]) == digest, 'exact nested pin: ' + name)
    old = inner(files['AUTHOR_SAFE_FREEZE.zip'], files['AUTHOR_EXTERNAL_MANIFEST.json'])
    new = inner(files['CORRECTED_SAFE.zip'], files['CORRECTED_EXTERNAL_MANIFEST.json'])
    expected = old['proof.md'].decode().replace('in a closed orientable hyperbolic 4-manifold.',
        'in a closed connected orientable hyperbolic 4-manifold.', 1).replace(
        'Conversely, a separating embedded orientable hypersurface in an orientable manifold is two-sided.',
        'Conversely, a connected separating embedded hypersurface in a connected orientable manifold is two-sided and hence orientable. Its complement has exactly two components.', 1).encode()
    require(new['proof.md'] == expected and expected != old['proof.md'], 'exact proof correction')
    require(all(new[n] == old[n] for n in AUTHOR_NAMES if n != 'proof.md'), 'unrelated correction')
    a = parse(files['ACCEPTANCE.json'])
    expected_fields = {'decision':DECISION, 'problem_id':2875, 'problem_number':'KP-3.77','rank':916,
        'status':'unsolved','turns_used':4,'turn_limit':5,'full_problem_solved':False,'full_problem_refuted':False,
        'novelty_claim':False,'worldwide_open_status_certified':False,'analytical_mathematical_audit_completed':True,
        'mathematical_proof_machine_certified':False,'source_inspection_completed_with_stated_limits':True,
        'original_preserved':True,'substantive_mathematical_error_found':False,'publication_performed':False,
        'raw_sources_or_dataset_contents_included':False}
    for key, value in expected_fields.items():
        require(type(a.get(key)) is type(value) and a[key] == value, 'acceptance field: ' + key)
    require(a['accepted_archive'] == {'filename':'CORRECTED_SAFE.zip','bytes':12382,'sha256':PINS['CORRECTED_SAFE.zip'][0]}, 'accepted archive target')
    for field, name in [('accepted_external_manifest_sha256','CORRECTED_EXTERNAL_MANIFEST.json'),
        ('original_archive_sha256','AUTHOR_SAFE_FREEZE.zip'),('original_external_manifest_sha256','AUTHOR_EXTERNAL_MANIFEST.json'),
        ('correction_patch_sha256','CORRECTION.patch')]:
        require(a[field] == PINS[name][0], 'acceptance exact target: '+field)
    patch = parse(files['PATCH_REPLAY.json'])
    require(patch['status'] == 'pass' and patch['changed_members'] == ['proof.md'] and patch['original_preserved'] is True,
        'patch replay status')
    require(patch['all_six_replayed_member_bytes_equal'] is True and patch['patch_sha256'] == PINS['CORRECTION.patch'][0], 'patch replay evidence')
    check_source_evidence(parse(files['SOURCE_PIN_RESULTS.json']), parse(files['SOURCE_INSPECTION.json']))
    for name, data in {**files, **{'author/'+n:b for n,b in old.items()}, **{'corrected/'+n:b for n,b in new.items()}}.items():
        if not name.endswith('.zip'):
            data.decode('utf-8')
            require(not any(marker in data for marker in (b'/work'+b'space/', b'private_'+b'sources/', b'transcript_'+b'evidence', b'dream_'+b'notes', b'scratch'+b'pad')), 'private marker')
            if name.endswith('.json'):
                parse(data)
    return {'status':'PASS','decision':DECISION,'original_members':6,'corrected_members':6,'changed_members':['proof.md'],
        'original_preserved':True,'full_problem_solved':False,'full_problem_refuted':False,'turns_used':4,'turn_limit':5,
        'machine_mathematical_proof':False}

def verify_archive(archive, manifest, expected_manifest_sha):
    require(len(expected_manifest_sha) == 64 and sha(manifest) == expected_manifest_sha, 'outer manifest digest')
    meta = parse(manifest)
    require(meta['archive']['bytes'] == len(archive) and meta['archive']['sha256'] == sha(archive), 'outer archive digest/bytes')
    require([x['path'] for x in meta['files']] == NAMES, 'outer manifest inventory')
    require(meta['decision'] == DECISION and meta['problem_id'] == 2875, 'outer decision/identity')
    data = unpack(archive, NAMES)
    for x in meta['files']:
        require(len(data[x['path']]) == x['bytes'] and sha(data[x['path']]) == x['sha256'], 'outer member digest')
    result = check_core(data)
    require(parse(data['ARTIFACT_TEST_RESULTS.json'])['status'] == 'PASS', 'artifact control report status')
    author_static = parse(data['AUTHOR_STATIC_REPLAY.json'])
    require(author_static['normal_optimized_equal'] is True and author_static['result']['status'] == 'pass' and len(author_static['result']['negative_controls_rejected']) == 5, 'author static replay report')
    replay = parse(data['REPLAY_RESULTS.json'])
    require(replay['status'] == 'PASS' and replay['normal_optimized_source_results_equal'] is True and replay['patch_replay_pass'] is True, 'replay report status')
    result['audit_members'] = len(data)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--external-manifest', required=True)
    parser.add_argument('--expected-external-manifest-sha256', required=True)
    for name in sources.PINS:
        parser.add_argument('--'+name.replace('_','-'))
    args = parser.parse_args()
    result = verify_archive(Path(args.archive).read_bytes(), Path(args.external_manifest).read_bytes(), args.expected_external_manifest_sha256)
    paths = {n:getattr(args,n) for n in sources.PINS}
    require(all(paths.values()) or not any(paths.values()), 'supply all eight sources or none')
    if all(paths.values()):
        result['source_replay'] = sources.verify(paths)
        result['scope'] = 'FULL_STATIC_SOURCE_AND_ARTIFACT_REPLAY; mathematical acceptance is an analytical audit, not executable proof.'
    else:
        result['source_replay'] = 'NOT_REHASHED_THIS_RUN'
        result['scope'] = 'ARTIFACT_ONLY; saved source evidence checked, external source bytes not rehashed.'
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
