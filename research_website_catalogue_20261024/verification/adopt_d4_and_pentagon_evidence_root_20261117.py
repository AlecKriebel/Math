from pathlib import Path
import datetime, hashlib, json, stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V = P/'verification'
def digest(b): return hashlib.sha256(b).hexdigest()
def snapshot(root):
    out = {}
    for p in [root, *sorted(root.rglob('*'))]:
        s = p.lstat()
        assert not p.is_symlink(), str(p)
        kind = 'directory' if stat.S_ISDIR(s.st_mode) else 'file'
        assert kind == 'directory' or stat.S_ISREG(s.st_mode)
        x = {'kind': kind, 'mode': stat.S_IMODE(s.st_mode), 'mtime_ns': s.st_mtime_ns}
        if kind == 'file':
            b = p.read_bytes()
            x.update(bytes=len(b), SHA256=digest(b), MD5=hashlib.md5(b).hexdigest(), empty=not b)
        else:
            x['empty'] = not any(p.iterdir())
        out[str(p.relative_to(root))] = x
    return out
def checked(root, manifest_name, pins, nfiles, ndirs):
    a = snapshot(root)
    for name, value in pins.items():
        assert a[name]['SHA256'] == value, (str(root), name, 'external pin')
    if manifest_name.endswith('.sha256'):
        rows = {}
        for line in (root/manifest_name).read_text().splitlines():
            h, path = line.split('  ', 1)
            rel = str(Path(path).relative_to(root))
            assert len(h) == 64 and rel not in rows
            rows[rel] = h
        assert set(a) == {'.', *rows, manifest_name, 'FINAL.md'}
        for name, h in rows.items(): assert a[name]['SHA256'] == h
    else:
        m = json.loads((root/manifest_name).read_text())
        if 'entries' in m:
            rows = {x['path']: x for x in m['entries']}
            assert set(a) == set(rows)
            terminals = set(m['terminal_content_hash_exclusions_exact'])
            for name, x in rows.items():
                y = a[name]
                assert y['kind'] == x['kind'] and y['mode'] == int(x['mode_octal'], 8)
                for k in ['bytes', 'mtime_ns', 'empty']:
                    if k in x: assert y[k] == x[k], (str(root), name, k)
                if x.get('sha256') is not None:
                    assert y['SHA256'] == x['sha256']
                elif x['kind'] == 'file':
                    assert name in terminals and name in pins
        else:
            assert a['.']['mode'] == int(m['root_mode'], 8)
            payload = m['payload_files']
            if isinstance(payload, dict):
                rows = payload
                dirs = m['directories']
                controls = {x['path']: x for x in m['terminal_pair']}
                assert set(a) == {'.', *rows, *dirs, *controls}
                for name, mode in dirs.items():
                    assert a[name]['kind'] == 'directory' and a[name]['mode'] == int(mode, 8)
                for name, x in controls.items():
                    assert name in pins and a[name]['bytes'] == x['bytes'] and a[name]['mode'] == int(x['mode'], 8)
            else:
                rows = {x['path']: x for x in payload}
                dirs = {x['path']: x for x in m['directories']}
                controls = m['terminal_modes']
                assert set(a) == {'.', *rows, *dirs, *controls}
                for name, x in dirs.items():
                    assert a[name]['kind'] == 'directory' and a[name]['mode'] == int(x['mode'], 8)
                    if 'empty' in x: assert a[name]['empty'] == x['empty']
                for name, mode in controls.items():
                    assert name in pins and a[name]['mode'] == int(mode, 8)
            for name, x in rows.items():
                y = a[name]
                assert y['kind'] == 'file' and y['mode'] == int(x['mode'], 8)
                for k in ['bytes', 'SHA256', 'MD5', 'empty']:
                    if k in x: assert y[k] == x[k], (str(root), name, k)
    assert sum(x['kind'] == 'file' for x in a.values()) == nfiles
    assert sum(x['kind'] == 'directory' for x in a.values()) - 1 == ndirs
    assert snapshot(root) == a
    return {'path': str(root.relative_to(P)), 'files': nfiles, 'child_directories': ndirs,
            'external_controls': pins, 'all_payloads_and_individually_declared_modes_exact': True,
            'whole_observed_bytes_modes_mtime_topology_before_after_exact': True}

d4 = [
    checked(V/'d4-canonical-potential-editorial-v2-sol-20261117', 'FINAL_MANIFEST.json', {
        'FINAL.json': '36eb02cf832f6734d40610a199f523b866e16505ee5e5d1ed252b63f2d27db4a',
        'FINAL_MANIFEST.json': '37b95cdf70d9cd8a4c7f521b6961bcbc52d4ff9726d2c5df7f2528bbda307a72'}, 30, 1),
    checked(V/'d4-canonical-potential-editorial-fact-sol-20261117', 'FINAL_MANIFEST.json', {
        'FINAL.json': '908da1a80c28ebaa1520d93e412c5b8be710df42c329329995a55051000e9bbc',
        'FINAL_MANIFEST.json': '2d522fc01a515f3cca5d136cfbc739d88fe6f676e7dfe56043ef94c3d179985d',
        'FINAL_SEAL.json': '32177f20a9e9822189a5345e863c17195cc3133e73437d09de9e198c91d95bef'}, 16, 0),
    checked(V/'d4-canonical-potential-legacy-sol-20261117', 'MANIFEST.json', {
        'FINAL.json': '969b0e5633d356a231b7e8f9660805676711680d1bda95b2cd8f72ffc3642ac6',
        'MANIFEST.json': '8d587be7279be17244b63666ae898d869fa953fd9115bfeb6cdba04ac97cccad'}, 21, 0)
]
custody = checked(V/'pentagon-root-custody-sol-20261117', 'MANIFEST.json', {
    'FINAL.json': '956ecbede9184ad062e7ed5c0d1344e0f4ae8ddc3f8e5865fa76411f8872f43f',
    'MANIFEST.json': '398874e6650d7d04c1062904be1791729be5ecfa17dc4210ed664b014417e89f'}, 10, 0)
challenge = checked(P/'papers/23137834/reviews/verdure-convention-challenge-sol-20261117', 'MANIFEST.sha256', {
    'FINAL.md': '919415f18b97c8767d556fad796bf326654bd736beb95fab1cc1dfda6004f119',
    'MANIFEST.sha256': 'b12a62abe384b99e54d184f8b8f336c64e53a035e5513939110f6acde5dfc8c2'}, 23, 0)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(name, obj):
    p = V/name
    with p.open('x') as f: f.write(json.dumps(obj, indent=2) + '\n')
    b = p.read_bytes()
    return {'path': str(p.relative_to(P)), 'bytes': len(b), 'SHA256': digest(b)}
one = put('root-d4-canonical-potential-editorial-adoption-20261117.json', {
    'UTC': now, 'status': 'ACCEPTED_PRIVATE_EDITORIAL_ONLY', 'record': '23439776',
    'authenticated_files': 67, 'child_directories': 1, 'packets': d4,
    'actual_complete_HTML_HEAD_MAIN_MODEL_Bib_and_all_reports_FINALs_read': True,
    'page_SHA256': '24bff5057a9f09fdfbc85020bb48c676c7940bf622cac8728dfb0dcb0f47ea0a',
    'scope': 'Historical canonical-X necessary converse only; exact later-coordinate/coefficient/KS-conclusion exclusions',
    'Mironov_complete_earlier_support_credited': True, 'follow_up': None,
    'legacy_correspondence': 'No genuine match in three fixed views; bounded absence only',
    'canonical': None, 'publication_or_AA_or_redirect_certificate': False, 'private_copy_percent': 100})
two = put('root-pentagon-final-evidence-adoption-20261117.json', {
    'UTC': now, 'status': 'ACCEPTED_FINITE_DATA_CUSTODY_AND_PRIMARY_PRECISION_NOTE',
    'record': '23137834', 'custody': custody, 'challenge': challenge,
    'protected_original_source_INITIAL_two_families_files': 242, 'protected_child_directories': 15,
    'actual_complete_custody_REPORT_FINAL_and_challenge_NOTE_FINAL_read': True,
    'actual_magnified_printed87_pixels_personally_viewed': True,
    'literal_printed87_B5': '3-5*z5-3*z5^4',
    'actual_theorem84_beta5': '3-5*zeta5-5*zeta5^4',
    'giant_Verdure_polynomial_identity_recomputed': False,
    'no_silent_primary_repair': True,
    'Fisher_independent_all_smooth_fiber_interface_checked': True,
    'scope_native_route': 'Direct-source geometry.py, no isolated copy',
    'adversarial_native_route': 'Isolated arithmetic.py byte-identical to source',
    'native_attempts_exits': [[1, 0], [1, 0]], 'root_scientific_runs': 0,
    'follow_up': None, 'scientific_PASS_or_publication_from_this_reader': False})
print(json.dumps({'D4': one, 'pentagon': two, 'authenticated_owned_files': 100}))
