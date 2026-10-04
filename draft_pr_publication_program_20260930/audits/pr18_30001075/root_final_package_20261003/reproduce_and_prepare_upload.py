"""ROOT: reproduce the frozen portable inputs without changing their originals."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

if sys.flags.optimize or sys.argv[1:]:
    raise RuntimeError('Nonoptimized no-argument execution required')
own = Path(__file__).resolve().parent
a18 = own.parent
package = a18 / 'preprint_v1'
pins = {
    'paper.tex': '2522ac0138de5e21067af8c16e6749b3a9d3cd01f12bdb929cca87cb6baeabb6',
    'common_tangent_nullness.pdf': '80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327',
    'common_tangents_null_locus_v1.zip': '1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5',
    'ARCHIVE_MANIFEST.json': '595bf1903377f68b6836f345bdfa252d6e65342c4d5cce0c67f02fc9f2b333b2',
    'ZENODO_UPLOAD_MANIFEST.json': '5d45d5b3ba4137ddfa19efd2b2a8c63055cb308942b8cc9a6c01019d4f0ed119',
    'zenodo_metadata.json': '2f3c90fbfefeb1fc7564399ed1d1b7287e534baf043275f6060a665e3ebd7b5f',
}
def digest(b):
    return hashlib.sha256(b).hexdigest()
def require(value, message):
    if not value:
        raise RuntimeError(message)
originals = {}
for name, expected in pins.items():
    p = package / name
    require(stat.S_ISREG(p.lstat().st_mode), 'Nonregular frozen input: '+name)
    body = p.read_bytes()
    require(digest(body) == expected, 'Frozen input changed: '+name)
    originals[name] = body
manifest = json.loads(originals['ARCHIVE_MANIFEST.json'])
extract = own / 'extracted_fixed_package'
extract.mkdir(exist_ok=False)
with zipfile.ZipFile(package / 'common_tangents_null_locus_v1.zip') as z:
    names = manifest['payload_domain'] + ['ARCHIVE_MANIFEST.json']
    require(z.namelist() == sorted(names), 'Unexpected archive domain/order')
    for entry in z.infolist():
        name = entry.filename
        require(not name.startswith('/') and '..' not in Path(name).parts,
                'Unsafe archive name')
        require(entry.external_attr >> 16 == 0o100644 and
                entry.date_time == (2026,10,3,0,0,0), 'Archive metadata mismatch')
        body = z.read(entry)
        require(body == (package / name).read_bytes(), 'ZIP/local mismatch: '+name)
        if name != 'ARCHIVE_MANIFEST.json':
            item = manifest['entries'][name]
            require(digest(body) == item['sha256'] and len(body) == item['bytes'],
                    'Manifest mismatch: '+name)
        dest = extract / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        dest.chmod(0o644)
captures = []
for label, mode in [('root-identical-build', 'build'), ('root-positive', 'verify')]:
    argv = [sys.executable, '-E', '-B', str(extract/'run_capture.py'), label, mode]
    out = own / (label+'.stdout.bin')
    err = own / (label+'.stderr.bin')
    with out.open('xb') as stdout, err.open('xb') as stderr:
        child = subprocess.Popen(argv, cwd=extract, stdout=stdout, stderr=stderr)
        code = child.wait()
    captures.append({'argv':argv, 'controller_pid':child.pid, 'returncode':code,
                     'stdout_sha256':digest(out.read_bytes()),
                     'stderr_sha256':digest(err.read_bytes())})
    require(code == 0, 'Unexpected child failure; full streams retained')
    if mode == 'build':
        require(digest((extract/'common_tangents_null_locus_v1.zip').read_bytes()) ==
                pins['common_tangents_null_locus_v1.zip'], 'Identical inputs not reproducible')
receipt = json.loads((extract/'verification.json').read_bytes())
require(receipt['status'] == 'PASS_FINITE_CONTROLS' and receipt['optimization'] == 0,
        'Finite controls did not pass')
for name, body in originals.items():
    require((package/name).read_bytes() == body, 'Original package mutated: '+name)
metadata = json.loads(originals['zenodo_metadata.json'])['metadata']
production_manifest = {'metadata':metadata, 'files':[
    {'path':'../preprint_v1/common_tangent_nullness.pdf'},
    {'path':'../preprint_v1/common_tangents_null_locus_v1.zip'},
]}
(own/'zenodo-deposit.json').write_text(json.dumps(production_manifest,indent=2)+'\n')
record = {'schema':'root-fixed-package-reproduction/v1',
    'UTC':dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_author_pid':os.getpid(),
    'pins':pins, 'ZIP_exact_domain_mode_timestamp_bytes':True,
    'same_frozen_inputs_rebuild_byte_identical':True, 'captures':captures,
    'finite_controls':receipt, 'original_preparation_package_unchanged':True,
    'ROOT_visual_QA':{'pages':list(range(1,9)), 'observed_all_complete':True,
                     'findings':'No clipped formulas, overlap or missing content observed',
                     'basis':'ROOT image-tool page readings; human/AI observation, not a hash inference'},
    'production_manifest':'zenodo-deposit.json',
    'production_manifest_sha256':digest((own/'zenodo-deposit.json').read_bytes()),
    'review_loop_complete':False, 'published':False, 'workflow_estimate_percent':75,
    'limits':'Finite reproduction and byte/layout consistency; the independent universal-proof reviews remain separate'}
(own/'ROOT_REPRODUCTION.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS_ROOT_FIXED_PACKAGE_REPRODUCTION',
    'record':'ROOT_REPRODUCTION.json','actual_pid':os.getpid(),
    'archive_sha256':pins['common_tangents_null_locus_v1.zip'],
    'UTC':record['UTC']},indent=2))
