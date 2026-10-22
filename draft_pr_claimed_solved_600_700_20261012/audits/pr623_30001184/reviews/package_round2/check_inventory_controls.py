from pathlib import Path
import copy, hashlib, json, os, shutil, subprocess, sys

R = Path(__file__).resolve().parent
BASE = R / 'tmp/extracted'
TMP = R / 'tmp'
env = dict(os.environ, TMPDIR=str(TMP))
results = []

def run_control(label, mutation):
    for flags in ([], ['-O']):
        root = TMP / ('control_' + label + ('_optimized' if flags else '_normal'))
        if root.exists(): shutil.rmtree(root)
        shutil.copytree(BASE, root)
        manifest = root / 'PACKAGE_MANIFEST.json'
        doc = json.loads(manifest.read_text())
        mutation(root, doc)
        if label != 'duplicate_json_key': manifest.write_text(json.dumps(doc))
        proc = subprocess.run([sys.executable, *flags, str(root / 'verify_package.py'), '--integrity-only'], capture_output=True, text=True, env=env)
        results.append({'control':label,'flags':flags,'returncode':proc.returncode,'rejected':proc.returncode != 0,'stdout':proc.stdout,'stderr':proc.stderr})

def field(field, value):
    return lambda root, doc: doc['files'][0].__setitem__(field, value)
controls = {
    'tampered': lambda root, doc: (root / doc['files'][0]['path']).write_bytes(b'changed'),
    'missing': lambda root, doc: (root / doc['files'][0]['path']).unlink(),
    'extra_file': lambda root, doc: (root / 'unlisted.txt').write_text('unexpected'),
    'empty_directory': lambda root, doc: (root / 'unlisted_empty_dir').mkdir(),
    'symlink': lambda root, doc: ((root / doc['files'][0]['path']).unlink(), (root / doc['files'][0]['path']).symlink_to(root / 'requirements.txt')),
    'wrong_count': lambda root, doc: doc.__setitem__('file_count', doc['file_count'] + 1),
    'bool_count': lambda root, doc: doc.__setitem__('file_count', True),
    'duplicate_path': lambda root, doc: doc['files'].append(copy.deepcopy(doc['files'][0])),
    'absolute_path': field('path', '/tmp/forbidden'),
    'traversal': field('path', '../forbidden'),
    'noncanonical_path': field('path', './README.md'),
    'backslash_path': field('path', 'x\\README.md'),
    'empty_path': field('path', ''),
    'bool_bytes': field('bytes', True),
    'float_bytes': field('bytes', 1.0),
    'negative_bytes': field('bytes', -1),
    'bad_hash': field('sha256', 'g'*64),
    'unsupported_schema': lambda root, doc: doc.__setitem__('schema', 2),
    'bool_schema': lambda root, doc: doc.__setitem__('schema', True),
    'float_schema': lambda root, doc: doc.__setitem__('schema', 1.0),
    'duplicate_json_key': lambda root, doc: (root/'PACKAGE_MANIFEST.json').write_text((root/'PACKAGE_MANIFEST.json').read_text().replace('"schema":', '"schema": 999, "schema":', 1)),
}
for label, mutation in controls.items(): run_control(label, mutation)
proc = subprocess.run([sys.executable, str(BASE/'verify_package.py')], capture_output=True, text=True, env=dict(env, PYTHONOPTIMIZE='2'))
inherited={'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'optimization':'PYTHONOPTIMIZE=2'}
(R/'INVENTORY_CONTROL_RESULTS.json').write_text(json.dumps({'cases':results,'inherited_optimization_full_replay':inherited},indent=2)+'\n')
print(json.dumps({'controls':len(results),'unexpected_acceptances':[{'control':x['control'],'flags':x['flags']} for x in results if not x['rejected']],'inherited_optimization_replay_passed':proc.returncode==0},indent=2))
