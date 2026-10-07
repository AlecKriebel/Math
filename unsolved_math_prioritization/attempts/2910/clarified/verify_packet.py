#!/usr/bin/env python3
"""Fail-closed integrity/scope replay. It does not check the geometric proofs."""
import hashlib, json, stat, subprocess, sys, zipfile
from pathlib import Path

EXPECTED = {'README.md','REPORT.md','PROOF.md','status.json','sources.json',
            'verification_metadata.json','research_log.json','diagnostics.py',
            'diagnostic_results.json','verify_packet.py'}
INPUTS = {
 'catalog.json':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 'problems.json':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'research_results.json':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
SOURCES = {
 'K3':(6578041,'ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f'),
 'LAR':(605334,'5fb0bc92edf2729070f25276e1ed8d32a4bdf84716afe32f6cea8d2032521d62'),
 'LM':(451614,'b20627fd97de37a1231bec40230bb4c81d34f2f5e757092a69eb5b0a11b8f5b4'),
 'BS':(250737,'6de2ef88203a17bb1a175569e26583163ce7233349dfffa70caccd49c7cc14a5')}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def pairs(items):
    d = {}
    for k, v in items:
        require(k not in d, 'Duplicate JSON key: '+k)
        d[k] = v
    return d

def read_json(path):
    require(path.is_file() and not path.is_symlink(), 'Missing or unsafe JSON')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    require(len(sys.argv) == 4, 'Usage: verify_packet.py PACKET_DIR EXTERNAL_MANIFEST ZIP')
    root, mp, zp = map(Path, sys.argv[1:])
    require(root.is_dir() and not root.is_symlink(), 'Unsafe packet root')
    manifest = read_json(mp)
    require(manifest['schema'] == 'authored-packet-v1' and manifest['problem_id'] == 2910, 'Manifest identity')
    inventory = manifest['files']
    require(type(inventory) is list, 'Manifest inventory type')
    names = [x['path'] for x in inventory]
    require(len(names) == len(set(names)) and set(names) == EXPECTED, 'Manifest inventory mismatch')
    actual = set()
    for path in root.rglob('*'):
        require(path.is_file() and not path.is_symlink(), 'Non-file or symlink in packet')
        actual.add(path.relative_to(root).as_posix())
    require(actual == EXPECTED, 'Packet inventory mismatch')
    for entry in inventory:
        data = (root/entry['path']).read_bytes()
        require(type(entry['bytes']) is int and entry['bytes'] == len(data), 'Byte count mismatch: '+entry['path'])
        require(entry['sha256'] == sha(data), 'Digest mismatch: '+entry['path'])
    s = read_json(root/'status.json')
    require(s['problem_id'] == 2910 and s['problem_number'] == 'KP-4.34', 'Problem identity')
    require(s['disposition'] == 'unsolved' and s['result_class'] == 'stalled_with_scoped_partial_audit', 'Status mismatch')
    require(s['full_problem_solved'] is False and s['new_solution_claimed'] is False and s['novelty_claimed'] is False, 'Unsupported solution or novelty claim')
    require(type(s['turns_used']) is int and s['turns_used'] == 3 and s['turn_limit'] == 5, 'Approach count')
    v = read_json(root/'verification_metadata.json')
    require(v['problem_id'] == 2910 and v['primary_statement_match'] is True, 'Statement identity')
    require(v['prior_work_gate'] == 'passed_literature_triage_only' and v['exact_report_empty'] is True, 'Inherited-work gate')
    require(v['complete_record_and_report_inspected'] is True, 'Incomplete gate')
    require(v['statement_sha256'] == 'fd75cc9ba9ad9e919960a0d2e05a139e751ebc24cb1f9e0cc599ce8094eb5dd4', 'Statement digest')
    require(v['complete_record_report_pair_sha256'] == '56eb2b6965848c89fd7f16e3433f3dafb39fb9bf861d801378dfed904b6dcbbd', 'Record-report digest')
    ins = v['input_files']
    require(len(ins) == 3 and {x['logical_name'] for x in ins} == set(INPUTS), 'Input inventory')
    for x in ins:
        require((x['bytes'],x['sha256']) == INPUTS[x['logical_name']] and x['match'] is True, 'Input binding')
    ss = read_json(root/'sources.json')['sources']
    require(len(ss) == 4 and {x['key'] for x in ss} == set(SOURCES), 'Source inventory')
    for x in ss:
        require((x['bytes'],x['sha256']) == SOURCES[x['key']], 'Source binding')
        require(x['url'].startswith('https://') and bool(x['manuscript_status']), 'Source attribution')
    log = read_json(root/'research_log.json')
    require(log['problem_id'] == 2910 and log['stop'] == 'stalled_partial', 'Log identity')
    require([x['number'] for x in log['approaches']] == [1,2,3], 'Log approach count')
    require(log['no_search_hit_used_as_novelty_evidence'] is True, 'Search scope')
    expected_output = (root/'diagnostic_results.json').read_bytes()
    for flags in ([], ['-O']):
        result = subprocess.run([sys.executable, *flags, str(root/'diagnostics.py')], capture_output=True, timeout=30)
        require(result.returncode == 0 and result.stdout == expected_output and not result.stderr, 'Diagnostic replay failed')
    dr = read_json(root/'diagnostic_results.json')
    require(dr['matrix_cases'] == 2401 and dr['negative_controls_rejected'] == 3, 'Diagnostic count')
    require(dr['certifies_topology'] is False and dr['certifies_general_solution'] is False, 'Diagnostic scope')
    require(zp.is_file() and not zp.is_symlink(), 'Unsafe archive')
    zb = zp.read_bytes()
    require(len(zb) == manifest['zip']['bytes'] and sha(zb) == manifest['zip']['sha256'], 'ZIP binding')
    with zipfile.ZipFile(zp) as archive:
        entries = archive.infolist()
        zn = [x.filename for x in entries]
        require(len(zn) == len(set(zn)) and set(zn) == EXPECTED, 'ZIP inventory')
        for item in entries:
            require(not item.is_dir() and not stat.S_ISLNK(item.external_attr >> 16), 'ZIP link/directory')
            require(not item.flag_bits & 1, 'Encrypted ZIP entry')
            require(archive.read(item.filename) == (root/item.filename).read_bytes(), 'ZIP payload mismatch')
    print(json.dumps({'result':'pass','problem_id':2910,'files_verified':len(EXPECTED),
                      'zip_verified':True,'normal_and_optimized_diagnostics_reproduced':True,
                      'geometric_theorems_verified_by_code':False}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'result':'fail','error':str(exc)},sort_keys=True),file=sys.stderr)
        sys.exit(1)
