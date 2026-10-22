#!/usr/bin/env python3
"""Round 3 checks using actual captured publication receipts; no live writes.

Git commands in this file only read objects. The separate routine harness uses
a disposable toy repository, never the shared index or refs.
"""
import copy
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import zipfile
import sympy as s

sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
A = HERE.parents[1]
REPO = A.parents[2]
TMP = HERE / 'tmp'
DOI = '10.5281/zenodo.23384924'
RESULTS = []

def check(label, value):
    if not value:
        raise ValueError('failed check: ' + label)
    RESULTS.append({'label': label, 'status': 'PASS'})

def rejects(label, function):
    try:
        function()
    except (ValueError, KeyError, TypeError, OSError):
        RESULTS.append({'label': label, 'status': 'REJECTED_AS_REQUIRED'})
    else:
        raise ValueError('accepted negative control: ' + label)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

M = load(A / 'prepare_integration.py', '_round3_integration')
T = load(A / 'record_tracker.py', '_round3_tracker')

def timestamp_and_actual_inputs():
    inputs = M.publication_inputs(A / 'publication', DOI,
        A / 'ZENODO_PUBLICATION_RECEIPT.json', A / 'ZENODO_POST_PUBLICATION_INSPECTION.json')
    receipt, inspection = map(M.parse_json, inputs['receipt_bytes'])
    confirmed = receipt['verified_utc']
    check('actual receipt confirmation is exact recorded time', confirmed == '2026-10-15T05:09:10.098518+00:00')
    check('independent inspection is later and distinct',
          datetime.datetime.fromisoformat(inspection['verified_utc']) > datetime.datetime.fromisoformat(confirmed))
    now = '2099-01-02T03:04:05+00:00'  # Explicitly synthetic future preparation time.
    files = M.build_publication(inputs, DOI, now)
    info = M.parse_json(files['PUBLICATION.json'])
    check('confirmation uses actual publication receipt rather than preparation', info['publication_confirmed_utc'] == confirmed)
    check('preparation time has separate exact field', info['integration_prepared_utc'] == now)
    check('no invented publication instant remains', 'published_utc' not in info and 'publication_utc' not in info)
    check('log describes both events separately', (now + ': integration preparation').encode() in files['PUBLICATION_LOG.md']
          and ('publication confirmed at ' + confirmed).encode() in files['PUBLICATION_LOG.md'])
    check('paper and metadata calendar date unchanged', b'\\date{October 15, 2026}' in files['real_schlicht_preschwarzian.tex']
          and M.parse_json(files['zenodo-deposit.json'])['metadata']['publication_date'] == '2026-10-15')
    manifest = M.parse_json(files['PUBLICATION_MANIFEST.json'])
    check('generated manifest binds all other exact members',
          {r['path']: (r['bytes'], r['sha256']) for r in manifest['files']} ==
          {n: (len(d), sha(d)) for n, d in files.items() if n != 'PUBLICATION_MANIFEST.json'})
    # Vary preparation without changing any scientific inputs or public receipts.
    other = M.build_publication(inputs, DOI, '2099-01-03T03:04:05+00:00')
    changed = {n for n in files if files[n] != other[n]}
    check('varying preparation affects only metadata log and dependent manifest',
          changed == {'PUBLICATION.json', 'PUBLICATION_LOG.md', 'PUBLICATION_MANIFEST.json'})
    check('varying preparation never changes confirmation', M.parse_json(other['PUBLICATION.json'])['publication_confirmed_utc'] == confirmed)
    old = load(HERE / 'tmp/prepare_integration.before_timestamp_repair.py', '_round3_old_integration')
    old.A, old.REPO = A, REPO
    old_files = old.build_publication(inputs, DOI, now)
    check('old-version comparison isolates repaired artifacts', {n for n in old_files if old_files[n] != files[n]} ==
          {'PUBLICATION.json', 'PUBLICATION_LOG.md', 'PUBLICATION_MANIFEST.json'})
    check('historical defect reproduced without production mutation', M.parse_json(old_files['PUBLICATION.json'])['published_utc'] == now)
    placeholder = copy.deepcopy(inputs)
    placeholder['receipt_bytes'] = [b'{"OFFLINE_LAYOUT_FIXTURE_NOT_A_PUBLICATION":1}\n',
                                    b'{"OFFLINE_LAYOUT_FIXTURE_NOT_A_PUBLICATION":2}\n']
    rejects('old synthetic replay placeholder deliberately lacks new required field',
            lambda: M.build_publication(placeholder, DOI, now))
    # Exercise mandatory receipt fields on copied real inputs, not forged success claims.
    with tempfile.TemporaryDirectory(prefix='receipt-negative-', dir=TMP) as temporary:
        root = Path(temporary)
        names = ['SCOPE_AND_SNAPSHOT.json', 'ACCEPTED_PUBLICATION_INPUTS.json',
                 'ZENODO_PUBLICATION_RECEIPT.json', 'ZENODO_POST_PUBLICATION_INSPECTION.json']
        names += ['publication/' + n for n in M.PUB_NAMES]
        names += ['native/' + M.PREFIX + n for n in inputs['original']]
        acceptance = M.parse_json(inputs['accepted_bytes'])
        names += [r['report_path'] for r in acceptance['whole_package_review_rounds']]
        for name in names:
            target = root / name; target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((A / name).read_bytes())
        previous_a, previous_acceptance = M.A, M.ACCEPTANCE
        M.A, M.ACCEPTANCE = root, root / 'ACCEPTED_PUBLICATION_INPUTS.json'
        try:
            for filename in ('ZENODO_PUBLICATION_RECEIPT.json', 'ZENODO_POST_PUBLICATION_INSPECTION.json'):
                path = root / filename; original = path.read_bytes()
                for value in (None, '', 0, False, []):
                    altered = M.parse_json(original); altered['verified_utc'] = value
                    path.write_bytes(M.json_bytes(altered))
                    rejects(filename + ' rejects absent/empty/nonstring timestamp ' + repr(value), lambda:
                        M.publication_inputs(root / 'publication', DOI, root / 'ZENODO_PUBLICATION_RECEIPT.json',
                                             root / 'ZENODO_POST_PUBLICATION_INSPECTION.json'))
                altered = M.parse_json(original); del altered['verified_utc']
                path.write_bytes(M.json_bytes(altered))
                rejects(filename + ' rejects missing timestamp key', lambda:
                    M.publication_inputs(root / 'publication', DOI, root / 'ZENODO_PUBLICATION_RECEIPT.json',
                                         root / 'ZENODO_POST_PUBLICATION_INSPECTION.json'))
                path.write_bytes(original)
            check('all copied negative fixtures restore exact validation',
                  M.publication_inputs(root / 'publication', DOI, root / 'ZENODO_PUBLICATION_RECEIPT.json',
                                       root / 'ZENODO_POST_PUBLICATION_INSPECTION.json')['validation'] == inputs['validation'])
        finally:
            M.A, M.ACCEPTANCE = previous_a, previous_acceptance
    tracker = M.parse_json((A / 'TRACKER_RECEIPT.json').read_bytes())
    check('actual tracker receipt remains old dependency executed at append', tracker['integration_helper_sha256'] ==
          '196caa41a2ac33161bf09437642b8c7ac726364b6e7ffdd0a33c718d0b2d43dd')
    check('tracker source captures repaired helper for future operations', T.INTEGRATION_HELPER_SHA256 ==
          'ca78faf9d061262f694098e2a8588a1a1a53eb8d203c6eab28091cdb9727a61b')
    check('historical tracker receipt still binds identical accepted publication', tracker['publication_validation'] == inputs['validation'])
    check('tracker is exact four-cell unique accepted row', tracker['applied'] is True
          and tracker['read_back'] == [T.wanted_row(DOI)] and tracker['row'] == T.wanted_row(DOI)
          and tracker['updated_range'] == "'Math Puzzles'!A94:D94" and tracker['global_exact_doi_rows'] == [94])
    journal = M.parse_json((A / 'ZENODO_PUBLISH_INTENT.json').read_bytes())
    check('reconciled publication intent binds actual receipt time and hash',
          journal['outcome'] == 'confirmed_published' and journal['confirmed_utc'] == confirmed
          and journal['publication_receipt_sha256'] == sha(inputs['receipt_bytes'][0])
          and journal['automatic_publish_retry_permitted'] is False)
    return inputs

def actual_prepared_tree(inputs):
    raw = (A / 'INTEGRATION_PREPARED_RECEIPT.json').read_bytes()
    check('parent corrected prepared receipt matches announced identity', sha(raw) ==
          '2d1ce4beb1d50f00f1917502408550d7a8c2cfd688a5095c9bcdb0290c363264')
    prepared = M.parse_json(raw)
    check('prepared corrected tree is unpushed', prepared['pushed'] is False and prepared['helper_sha256'] ==
          'ca78faf9d061262f694098e2a8588a1a1a53eb8d203c6eab28091cdb9727a61b')
    files = M.build_publication(inputs, DOI, prepared['prepared_utc'])
    check('prepared commit and tree match recorded objects', git('rev-parse', prepared['integration_commit'] + '^{tree}').decode().strip() == prepared['tree'])
    check('prepared commit has only main and original candidate parents', git('show', '-s', '--format=%P', prepared['integration_commit']).decode().split() ==
          [prepared['main_base'], M.ORIGINAL])
    check('actual proposed directory matches every freshly constructed byte', all(
          git('show', prepared['tree'] + ':' + M.PUB_PREFIX + n) == d for n, d in files.items()))
    check('actual proposed manifest/pins match prepared receipt',
          {n: sha(d) for n, d in files.items()} == prepared['publication_sha256'])
    original_queue = git('show', M.ORIGINAL + ':' + M.QPATH)
    _, _, candidate_line, cells = M.queue_row(original_queue)
    check('immutable candidate queue exact claimed_solved 5/5 selected row',
          cells[8].strip() == b'claimed_solved' and cells[9].strip() == b'5/5'
          and candidate_line.rstrip(b'\r\n').decode() == inputs['snapshot']['queue_row'])
    main_queue = git('show', prepared['main_base'] + ':' + M.QPATH)
    changed_queue, queue_record = M.patch_queue(main_queue, DOI, inputs['snapshot']['queue_row'])
    check('actual queue patch equals independently reconstructed selected three cells',
          git('show', prepared['tree'] + ':' + M.QPATH) == changed_queue and queue_record == prepared['queue_patch'])
    expected = {M.QPATH} | {M.PREFIX + n for n in inputs['original']} | {M.PUB_PREFIX + n for n in files}
    actual = {n.decode() for n in git('diff', '--name-only', '-z', prepared['main_base'], prepared['tree']).split(b'\0') if n}
    check('exact45 selected target paths and no other PR processing', actual == expected and len(actual) == 45)
    native_git_entries = git('ls-tree', '-r', '-z', M.ORIGINAL, '--', M.PREFIX)
    proposed_git_entries = git('ls-tree', '-r', '-z', prepared['tree'], '--', M.PREFIX)
    check('all native24 Git blob modes and identities exact', native_git_entries == proposed_git_entries)
    for name, data in inputs['original'].items():
        check('actual tree preserves original bytes ' + name,
              git('show', prepared['tree'] + ':' + M.PREFIX + name) == data)
    check('actual prepared replay has two successful real verifiers',
          prepared['proposed_tree_replay']['native_proposed_tree']['status'] == 'PASS'
          and prepared['proposed_tree_replay']['accepted_archive']['status'] == 'PASS')
    check('no branch push marker exists', not (A / 'INTEGRATION_PUSH_INTENT.json').exists()
          and not (A / 'INTEGRATION_PUSHED_RECEIPT.json').exists())
    (HERE / 'ACTUAL_PREPARED_TREE_CHECK.json').write_bytes(M.json_bytes({
        'status': 'PASS', 'prepared_receipt_sha256': sha(raw), 'integration_commit': prepared['integration_commit'],
        'tree': prepared['tree'], 'prepared_utc': prepared['prepared_utc'], 'changed_paths': sorted(actual),
        'read_only_git_objects_only': True, 'no_push_or_shared_git_mutations': True}))
    return files

def independent_math():
    # Independently reconstruct the key identities from elementary derivatives.
    z, w, t, r = s.symbols('z w t r')
    x, y = s.symbols('x y', real=True)
    kp = z / (1-z)**2; km = z / (1+z)**2; h = z / (1-z*z)
    P = lambda f: s.cancel(s.diff(f,z,2)/s.diff(f,z))
    B = lambda f: s.cancel((1-x*x-y*y)*P(f).subs(z,x+s.I*y)-2*(x-s.I*y))
    den = (1-(x+s.I*y)**2)*(1-(x-s.I*y)**2)
    for label, f in [('k_plus', kp), ('k_minus', km)]:
        b = B(f)
        check(label + ' exact full complex deficit', s.cancel(b*s.conjugate(b)-16+48*y*y/den) == 0)
        check(label + ' direct normalization', f.subs(z,0) == 0 and s.diff(f,z).subs(z,0) == 1)
    check('opposite real endpoints', s.cancel(B(kp).subs(y,0)-4) == 0 and s.cancel(B(km).subs(y,0)+4) == 0)
    check('h is injective by exact factorization', s.cancel(h-h.subs(z,w)-(z-w)*(1+z*w)/((1-z*z)*(1-w*w))) == 0)
    check('h imaginary centered derivative', s.cancel(B(h).subs({x:0,y:t})-8*s.I*t/(1+t*t)) == 0)
    check('denominator and delta strict interior identity', s.expand(den-(1-x*x-y*y)**2-4*y*y) == 0)
    check('growth log integral', s.cancel(s.diff((1+r)/(1-r)**3,r)/((1+r)/(1-r)**3)-(4+2*r)/(1-r*r)) == 0)
    check('growth function integral', s.cancel(s.diff(r/(1-r)**2,r)-(1+r)/(1-r)**3) == 0)
    check('non-Koebe lower value at i/2 strictly larger', s.cancel((8*s.Rational(2,5))**2) == s.Rational(256,25)
          and 16*(1-3*s.Rational(2,5)**2) == s.Rational(208,25))
    check('lower branch crossing', s.cancel(16*(1-3/s.Integer(7))-64/s.Integer(7)) == 0)
    check('zero source expression differs from auxiliary value', (z*P(kp)).subs(z,0) == 0 and B(kp).subs({x:0,y:0}) == 4)
    check('convex combination shortcut really has interior critical point',
          s.simplify(s.diff((kp+km)/2,z).subs(z,s.I*(s.sqrt(2)-1))) == 0)
    e = s.symbols('e', positive=True)
    check('vanishing Euclidean imaginary part need not give delta zero',
          s.limit(s.cancel((y*y/den).subs({x:1-e,y:e})),e,0,dir='+') == s.Rational(1,8))

def actual_layout_replay(inputs, files):
    with tempfile.TemporaryDirectory(prefix='real-receipts-layout-', dir=TMP) as temporary:
        report = M.capture_replay(inputs, temporary, files)
    check('new helper real-receipt proposed layout replay', report['native_proposed_tree']['status'] == 'PASS'
          and report['accepted_archive']['status'] == 'PASS' and report['temporary_copies_only'] is True)
    (HERE / 'ACTUAL_LAYOUT_REPLAY.json').write_bytes(M.json_bytes(report))

def main():
    inputs = timestamp_and_actual_inputs()
    files = actual_prepared_tree(inputs)
    independent_math()
    if not sys.flags.optimize:
        actual_layout_replay(inputs, files)
    output = {'status': 'PASS', 'utc': M.utc(), 'optimized': bool(sys.flags.optimize),
              'checks': len(RESULTS), 'results': RESULTS,
              'all_receipts_actual_except_explicit_synthetic_future_preparation_time': True,
              'shared_git_commands_read_only': True, 'no_live_service_writes': True,
              'independent_math_controls': True, 'scope_qualitative_only': True}
    target = HERE / ('INDEPENDENT_CHECKS.optimized.json' if sys.flags.optimize else 'INDEPENDENT_CHECKS.normal.json')
    target.write_bytes(M.json_bytes(output))
    print(json.dumps({'status': 'PASS', 'checks': len(RESULTS), 'optimized': bool(sys.flags.optimize)}))

if __name__ == '__main__':
    main()
