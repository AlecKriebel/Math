"""Mutate ONLY review-directory copies to test the actual archived verifier."""
import json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / 'extracted/verification/check_bosonization.py').read_text()
mutations = {
    'omit_bosonization_coproduct_parity': ('(parity(b) + i) % 2', 'i'),
    'omit_bosonization_product_sign': ('(-1) ** (i * parity(a))', '1'),
    'omit_super_coproduct_sign': ('(-1) ** (parity(b) * PARITY[c])', '1'),
    'omit_antipode_group_factor': ('(i + parity(h)) % 2', 'i'),
    'invert_super_antipode_coefficient': ('(-1) ** (n + crossings)', '-((-1) ** (n + crossings))'),
}
results = {}
for name, (before, after) in mutations.items():
    assert raw.count(before) == 1, (name, raw.count(before))
    path = HERE / ('negative_' + name + '.py')
    path.write_text(raw.replace(before, after))
    run = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
    results[name] = {'rejected': run.returncode != 0, 'returncode': run.returncode,
                     'last_error': run.stderr.strip().splitlines()[-1] if run.stderr else '',
                     'false_PASS': '"PASS"' in run.stdout}
    assert run.returncode != 0 and 'AssertionError' in run.stderr and '"PASS"' not in run.stdout
(HERE / 'negative_control_results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
