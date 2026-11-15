"""Small new adapter/scope fixtures only. No prior control suite, Git or installer."""
import sys
sys.dont_write_bytecode = True
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import exact11_lib as L


def denied(action):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError('required rejection missing')


def main():
    results = []
    original = L.obj(L.O / 'inputs/stage-OVERLAY_MANIFEST.json')['files']
    plan = L.obj(L.O / 'inputs/stage-INSTALLATION_PLAN.json')
    rows = L.overlay_rows(original, plan)
    bad = copy.deepcopy(original)
    bad[2]['path'] = 'research/five-outgoing-centers-alpha16/assets/five_centers.tex'
    denied(lambda: L.overlay_rows(bad, plan))
    denied(lambda: L.overlay_rows(original[:2] + original[3:], plan))
    results.append({'control': 'article-root TeX mapping and exact11 coverage', 'both_losses_rejected': True})
    template = L.obj(L.O / 'ROOT_ADOPTION_TEMPLATE.json')
    denied(lambda: L.adoption_fields(template))
    denied(lambda: L.adoption_fields(L.obj(L.O / 'inputs/root-five-centers-mixed-face-stage-reading-20261115.json')))
    prior = L.obj(L.O / 'inputs/stage-ROOT_WEBSITE_GO.json')['prior_stage_adoption']
    # Held prior receipt body, not its original path and never current production authority.
    baseline = L.obj(L.O / 'inputs/stage-WEBSITE_BASELINE.json')
    old = next(r for r in baseline['files'] if r['path'] == prior['path'])
    denied(lambda: L.adoption_fields(json.loads(L.pin(L.S / old['blob'], old))))
    results.append({'control': 'false template, source-only reading and prior-pair authority', 'all_rejected': True})
    raw = L.read(L.O / 'private/retained-approved-index')
    targets = {('public/' + r['path']).encode() for r in rows}
    index = L.parse_index(raw, targets)
    L.need(index['count'] == 58554 and index['protected_record_count'] == 58552, 'new-scope retained records')
    path, record = index['protected'][0]
    offset = raw.find(record)
    L.need(offset >= 12 and raw.count(record) == 1, 'unique protected native record')
    changed = bytearray(raw); changed[offset] ^= 1
    changed[-20:] = hashlib.sha1(changed[:-20]).digest()
    altered = L.parse_index(bytes(changed), targets)
    L.need(altered['protected'] != index['protected'], 'native stat-byte preservation catches real loss')
    results.append({'control': 'new58552 native protection detects stat change', 'detected': True})
    with tempfile.TemporaryDirectory(prefix='new-scope-toy-', dir=L.O / 'private') as directory:
        root = Path(directory)
        old_w, old_run = L.W, L.subprocess.run
        calls = [0]

        def forbidden_run(*args, **kwargs):
            calls[0] += 1
            raise AssertionError('subprocess must not be reached')

        (root / 'held').write_bytes(b'owned toy')
        L.W, L.subprocess.run = root, forbidden_run
        try:
            denied(lambda: L.read(root / 'held'))
            denied(lambda: L.namespace(root))
            denied(lambda: L.git('rev-parse', 'HEAD'))
            L.need(calls[0] == 0, 'source-only gate precedes any subprocess')
        finally:
            L.W, L.subprocess.run = old_w, old_run
        results.append({'control': 'live read/list/Git gates exercised against owned toy root', 'subprocess_calls': calls[0]})
        lock = root / 'toy-lock'; fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
        L.write_complete(fd, L.LOCK_BODY)
        destination = root / 'toy-destination'; destination.write_bytes(b'old')
        alternate = root / 'toy-alternate'; alternate.write_bytes(b'validated130131')
        captured = alternate.read_bytes(); alternate.write_bytes(b'changed')
        try:
            L.publish_buffer(captured, destination, lock, fd)
            L.validate_owned_buffer(lock, fd, L.LOCK_BODY)
            L.need(destination.read_bytes() == captured, 'current compiled FD helper publishes captured whole buffer')
            results.append({'control': 'compiled current FD buffer/retained distinct lock', 'passed': True})
        finally:
            try: L.unlink_owned(lock, fd)
            finally: os.close(fd)
        target = root / 'owned'; fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
        alias = root / 'foreign-link'; alias.symlink_to(target)
        try:
            denied(lambda: L.unlink_owned(alias, fd))
            L.need(alias.is_symlink() and target.exists(), 'lstat refusal retains substituted symlink and target')
            results.append({'control': 'current cleanup refuses symlink to owned inode', 'retained': True})
        finally:
            os.close(fd)
    for name in L.CODE_FILES:
        ast.parse(L.read(L.O / name).decode())
    L.need(L.LIVE_AUTHORIZED is False, 'no authority enabled by controls')
    print(json.dumps({'status': 'PASS_NEW_BOUNDED_SOURCE_ADAPTER_AND_TOY_CONTROLS', 'controls': results,
                      'old_fault_renderer_native_scientific_campaigns_executed': False,
                      'actual_website_dot_git_or_Git_subprocess_access': False,
                      'writes_only_new_private_toy_namespace': True}, indent=2))


if __name__ == '__main__':
    main()
