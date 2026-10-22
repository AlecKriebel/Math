#!/usr/bin/env python3
"""Read-only closed-custody validation. Requires independent caller-held pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

HEAD = '34f21454986a28ca49f24999be3a0fd1b42755f8'
PLAN = '3216c59ccf06e7bcdb940a221f14bc54eb7522a19e79726616fc6380b5989725'
REPORT = 'c85ae98cf29c46d2a3c0b399486edfa1b8c21309da388bfb884b9a2c0b338a47'
POSITION = '09755bf50d7e9d25e22d21bde0b3d471843ec9a671aaae91754c159b8174c2d5'
ORIGINAL_PREFIX = 'intake/original/'
REQUIRED = {
 'INDEPENDENT_PLAN.json','INPUTS.json','REPORT_PRE_PEER.md','POSITION_PRE_PEER.json',
 'SOURCE_LEDGER.json','QUERY_LEDGER.json','PRIMARY_BODY_COMPARISON.json',
 'EXACT_COMPARISON.md','PEER_CHALLENGE.md','PEER_EXPOSURE.json',
 'PEER_PROVISIONAL_INPUT.json','POST_FREEZE_BODY_RECEIPT.json',
 'POST_FREEZE_SOURCE_NOTE.md','VERDICT.json','BODIES.json',
 'comparison_check.py','COMPARISON_RESULTS.json','custody_check.py','RESEARCH_LOG.md'
}

class CustodyError(Exception):
    pass

def need(condition, message):
    if not condition:
        raise CustodyError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def valid_hash(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None

def pairs(items):
    d = {}
    for k,v in items:
        need(k not in d, 'Duplicate JSON key: '+str(k))
        d[k] = v
    return d

def nonfinite(value):
    raise CustodyError('Non-finite JSON value: '+value)

def parse(raw):
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)
    except (ValueError, UnicodeError) as e:
        raise CustodyError('Invalid JSON: '+str(e)) from e

def child(root, relative):
    need(isinstance(relative,str) and bool(relative), 'Empty/nonstring path')
    path = PurePosixPath(relative)
    need(not path.is_absolute() and all(x not in ('','.','..') for x in relative.split('/')),
         'Unsafe relative path: '+relative)
    current = root
    for i, component in enumerate(path.parts):
        current = current/component
        try:
            st = current.lstat()
        except OSError as e:
            raise CustodyError('Missing/inaccessible: '+str(current)) from e
        need(not stat.S_ISLNK(st.st_mode), 'Symlink forbidden: '+str(current))
        if i < len(path.parts)-1:
            need(stat.S_ISDIR(st.st_mode), 'Non-directory path component')
        else:
            need(stat.S_ISREG(st.st_mode), 'Non-regular file: '+str(current))
    return current

def checked(root, relative, row):
    need(isinstance(row,dict), 'Bad file record')
    need(type(row.get('bytes')) is int and row['bytes'] >= 0, 'Invalid byte count')
    need(valid_hash(row.get('sha256')), 'Invalid SHA256')
    f = child(root, relative)
    raw = f.read_bytes()
    need(len(raw) == row['bytes'], 'Length mismatch: '+str(f))
    need(sha(raw) == row['sha256'], 'Hash mismatch: '+str(f))
    return raw

def run(args):
    need(valid_hash(args.expected_manifest_sha), 'External manifest pin must be 64 lowercase hex')
    need(valid_hash(args.expected_checker_sha), 'External checker pin must be 64 lowercase hex')
    packet = Path(args.packet).resolve(strict=True)
    input_root = Path(args.inputs_root).resolve(strict=True)
    body_root = Path(args.bodies_root).resolve(strict=True)
    own = Path(__file__).resolve(strict=True)
    need(own == packet/'custody_check.py', 'Run the checker in the checked packet')
    need(sha(own.read_bytes()) == args.expected_checker_sha, 'External checker pin mismatch')
    raw = child(packet,'MANIFEST.json').read_bytes()
    need(sha(raw) == args.expected_manifest_sha, 'External manifest pin mismatch')
    m = parse(raw)
    need(m.get('schema') == 1 and m.get('pr') == 786 and m.get('head') == HEAD, 'Wrong target manifest')
    need(m.get('excluded') == {'MANIFEST.json':'Self-hash exception only; exact bytes require caller-held external SHA256.'},
         'Manifest exception list differs')
    need(m.get('external_pin_required') is True, 'External pin requirement missing')
    files = m.get('files')
    need(isinstance(files,dict) and REQUIRED <= set(files), 'Missing required authored files')
    need('MANIFEST.json' not in files, 'Circular manifest entry')
    actual = set()
    for e in os.scandir(packet):
        need(not e.is_symlink() and e.is_file(follow_symlinks=False), 'Flat regular-files-only packet required')
        actual.add(e.name)
    need(actual == set(files)|{'MANIFEST.json'}, 'Unlisted/missing packet path')
    for name,row in files.items():
        need(re.fullmatch('[A-Za-z0-9_.-]+', name) is not None, 'Unsafe flat filename')
        checked(packet,name,row)
    need(sha((packet/'INDEPENDENT_PLAN.json').read_bytes()) == PLAN, 'Frozen plan changed')
    need(sha((packet/'REPORT_PRE_PEER.md').read_bytes()) == REPORT, 'Frozen report changed')
    need(sha((packet/'POSITION_PRE_PEER.json').read_bytes()) == POSITION, 'Frozen position changed')
    pos = parse((packet/'POSITION_PRE_PEER.json').read_bytes())
    need(pos.get('head') == HEAD and pos.get('independent_pre_peer') is True, 'Initial position target/independence')
    for name,key in [('INDEPENDENT_PLAN.json','plan_sha256'),('REPORT_PRE_PEER.md','report_sha256'),
                     ('EXACT_COMPARISON.md','comparison_sha256'),('SOURCE_LEDGER.json','source_ledger_sha256'),
                     ('QUERY_LEDGER.json','query_ledger_sha256')]:
        need(sha((packet/name).read_bytes()) == pos.get(key), 'Pre-peer bound file changed: '+name)
    inputs = parse((packet/'INPUTS.json').read_bytes())
    need(inputs.get('target_head') == HEAD, 'Full-source target mismatch')
    sourcefiles = inputs.get('files')
    need(isinstance(sourcefiles,dict) and len(sourcefiles) == 47, 'Full input inventory must contain 47 files')
    original = {n for n in sourcefiles if n.startswith(ORIGINAL_PREFIX)}
    need(len(original) == 41, 'All 41 original files are required')
    for name,row in sourcefiles.items():
        checked(input_root,name,row)
    actual_original = set()
    origroot = input_root/'intake'/'original'
    for directory, dirs, names in os.walk(origroot, followlinks=False):
        for name in dirs:
            need(not (Path(directory)/name).is_symlink(), 'Symlink in original tree')
        for name in names:
            rel = (Path(directory)/name).relative_to(input_root).as_posix()
            child(input_root,rel)
            actual_original.add(rel)
    need(actual_original == original, 'Original source inventory is not complete/exact')
    identity = parse((input_root/'intake/ROOT_SOURCE_IDENTITY.json').read_bytes())
    need(identity.get('reviewed_head') == HEAD and identity.get('pr') == 786, 'Root identity mismatch')
    need(identity.get('original_file_count') == 41 and len(identity.get('original_files',[])) == 41,
         'Identity does not bind full source')
    for row in identity['original_files']:
        name = ORIGINAL_PREFIX+row['path']
        need(name in original, 'Identity lists unbound original')
        need(row['sha256'] == sourcefiles[name]['sha256'] and row['bytes'] == sourcefiles[name]['bytes'],
             'Identity/source inventory disagree')
    gate = parse((input_root/'root-receipts/MATH_GATE.json').read_bytes())
    need(gate.get('reviewed_head') == HEAD and gate.get('pr') == 786, 'Math-gate target mismatch')
    need(str(gate.get('result','')).startswith('PASS_COMPLETE_NEGATIVE'), 'Required closed math gate absent')
    bodies = parse((packet/'BODIES.json').read_bytes())
    need(bodies.get('included_in_packet') is False, 'Third-party full bodies must remain outside flat packet')
    bodyfiles = bodies.get('files')
    need(isinstance(bodyfiles,dict) and len(bodyfiles) == 24, 'Unexpected received body inventory')
    for name,row in bodyfiles.items():
        need('/' not in name and name.endswith(('.pdf','.txt','.png')), 'Unsafe body filename')
        checked(body_root,name,row)
    sources = parse((packet/'SOURCE_LEDGER.json').read_bytes())['sources']
    need(len(sources) == 10, 'Initial source ledger count')
    for row in sources:
        if row.get('status') == 'full_body':
            need(bodyfiles.get(row['id']+'.pdf',{}).get('sha256') == row['sha256'], 'Primary body receipt mismatch')
    post = parse((packet/'POST_FREEZE_BODY_RECEIPT.json').read_bytes())
    need(post.get('status') == 'full_body' and post.get('sha256') ==
         bodyfiles['fang_koenig_author.pdf']['sha256'], 'Post-freeze author body receipt mismatch')
    queries = parse((packet/'QUERY_LEDGER.json').read_bytes())['queries']
    need(len(queries) == 49 and [x['id'] for x in queries] == [f'Q{i:03d}' for i in range(1,50)],
         'Query inventory mismatch')
    need(all(isinstance(x.get('query'),str) and x['query'] for x in queries), 'Empty query')
    peer = parse((packet/'PEER_PROVISIONAL_INPUT.json').read_bytes())
    exposure = parse((packet/'PEER_EXPOSURE.json').read_bytes())
    need(sha((packet/'PEER_PROVISIONAL_INPUT.json').read_bytes()) ==
         exposure['files_at_read']['PROVISIONAL_FINDING.json']['sha256'], 'Peer frozen-input mismatch')
    need(peer['target']['head'] == HEAD, 'Wrong peer target')
    v = parse((packet/'VERDICT.json').read_bytes())
    need(v.get('head') == HEAD and v.get('priority_status') == 'PRIORITY_UNRESOLVED', 'Verdict target/status')
    for key in ['novelty_certified','firstness_certified','current_global_openness_certified',
                'complete_literature_coverage','new_component_theory_claimed','source_proof_changes',
                'git_mutations','queue_mutations','external_account_changes','external_contacts']:
        need(v.get(key) is False, 'Prohibited unsupported verdict flag: '+key)
    for key in ['initial_report_unchanged','initial_position_unchanged','peer_challenge_complete',
                'post_freeze_public_author_body_checked']:
        need(v.get(key) is True, 'Required completion flag: '+key)
    opts = ['-B'] + (['-O'] if sys.flags.optimize else [])
    proc = subprocess.run([sys.executable]+opts+[str(packet/'comparison_check.py')],
                          capture_output=True, text=True)
    need(proc.returncode == 0, 'Comparison check failed: '+proc.stderr[:200])
    need(parse(proc.stdout) == parse((packet/'COMPARISON_RESULTS.json').read_bytes()),
         'Comparison replay differs from checked record')
    return {'status':'PASS','manifest_sha256':args.expected_manifest_sha,
            'checker_sha256':args.expected_checker_sha,'optimization':sys.flags.optimize,
            'authored_files':len(files),'full_input_files':len(sourcefiles),'original_files':len(original),
            'outside_packet_body_files':len(bodyfiles),'query_count':len(queries),
            'scope':'Closed byte custody and finite comparison replay; not a novelty/absence certificate.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('packet','inputs-root','bodies-root','expected-manifest-sha','expected-checker-sha'):
        parser.add_argument('--'+name, required=True)
    try:
        print(json.dumps(run(parser.parse_args()),indent=2,sort_keys=True))
    except (CustodyError,OSError,KeyError,TypeError,ValueError) as error:
        print('CUSTODY_FAIL: '+str(error),file=sys.stderr)
        sys.exit(1)
