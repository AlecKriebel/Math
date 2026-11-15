#!/usr/bin/env python3
"""Read-only packet closure and native-custody verifier. Never writes to any input."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import sys
import zipfile

R = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((R/name).read_bytes())


def check_entry(entry, relative=False):
    p = R/entry['path'] if relative else Path(entry['path'])
    require(p.is_file() and not p.is_symlink(), 'missing/nonregular input '+str(p))
    require(p.stat().st_size == entry['bytes'], 'size mismatch '+str(p))
    require(sha(p) == entry['sha256'], 'SHA-256 mismatch '+str(p))


def main():
    manifest=read('ARTIFACT_MANIFEST.json')
    seal=read('FINAL_SEAL.json')
    inputs=read('INPUT_MANIFEST.json')
    custody=read('ORIGINAL_PAYLOAD_CUSTODY.json')
    require(sha(R/'ARTIFACT_MANIFEST.json') == seal['artifact_manifest_sha256'], 'owned-manifest binding')
    require(sha(R/'INPUT_MANIFEST.json') == seal['input_manifest_sha256'], 'input-manifest binding')
    require(sha(R/'INITIAL_SEAL.json') == seal['initial_seal_sha256'], 'initial seal binding')
    require(sha(R/'INITIAL_RECONSTRUCTION.md') == seal['initial_reconstruction_sha256'], 'initial reconstruction binding')
    require(seal['completion_percent']==100, 'packet incomplete')
    for entry in manifest['entries']:
        require(not PurePosixPath(entry['path']).is_absolute() and '..' not in PurePosixPath(entry['path']).parts,
                'unsafe relative owned path')
        check_entry(entry, True)
    actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file()}
    expected={e['path'] for e in manifest['entries']} | {'ARTIFACT_MANIFEST.json','FINAL_SEAL.json'}
    require(actual==expected, 'owned file inventory differs from sealed inventory')
    for entry in inputs['source_files']+inputs['foreign_primary_objects']:
        check_entry(entry)
    source_root=Path(seal['source_root'])
    require({str(p.resolve()) for p in source_root.rglob('*') if p.is_file()} ==
            {e['path'] for e in inputs['source_files']}, 'native source tree inventory changed')
    require(sha(source_root/'SOURCE_READY.json') == seal['source_ready_sha256'], 'SOURCE_READY binding')
    require(sha(source_root/'spherical_fibonacci_separation.pdf') == seal['published_pdf_sha256'], 'published PDF binding')
    require(sha(source_root/'published-source/spherical_fibonacci_separation.tex') == seal['controlling_tex_sha256'], 'controlling TeX binding')
    require(sha(source_root/'spherical_fibonacci_verification.zip') == seal['original_zip_sha256'], 'ZIP binding')
    check_entry(custody['original_archive'])
    members=[]
    with zipfile.ZipFile(custody['original_archive']['path']) as z:
        for ordinal,info in enumerate(z.infolist()):
            if info.is_dir():
                continue
            name=PurePosixPath(info.filename)
            require(not name.is_absolute() and '..' not in name.parts, 'unsafe native member')
            data=z.read(info)
            recorded=custody['members'][len(members)]
            require(recorded['original_member_name']==info.filename and recorded['ordinal_zero_based']==ordinal,
                    'native member identity/order')
            require(recorded['bytes']==len(data) and recorded['sha256']==hashlib.sha256(data).hexdigest(),
                    'native member original bytes')
            require(Path(recorded['extracted_path']).read_bytes()==data, 'native extracted bytes changed')
            members.append(info.filename)
    require(len(members)==13 and len(set(members))==13, 'native payload count/uniqueness')
    run=read('supplied_replay/RESULT.json')
    require(run['successful_controls']==4 and run['expected_mathematical_rejections']==5, 'supplied route count')
    require(all(x['reaped'] and not x['timed_out'] and x['error'] is None for x in run['full_process_results']),
            'supplied execution failed/deadline/cleanup')
    require(all(x['exit']==x['expected_exit'] for x in run['full_process_results']), 'supplied exit mismatch')
    require(not run['infinite_theorem_proved_by_computation'] and not run['novelty_certified'],
            'finite controls overstated')
    result=subprocess.run([sys.executable,'-E','-B',str(R/'independent_verifier.py')],
                          cwd=R,stdin=subprocess.DEVNULL,capture_output=True,timeout=20,check=True)
    require(not result.stderr, 'independent diagnostic stderr')
    require(json.loads(result.stdout)==read('INDEPENDENT_RESULT.json'), 'independent diagnostic changed')
    require(read('INDEPENDENT_RESULT.json')==read('INDEPENDENT_OPTIMIZED_RESULT.json'), 'optimization diagnostic mismatch')
    print(json.dumps({'closure_status':'READ_ONLY_CLOSURE_VERIFIED','owned_files':len(actual),
                      'manifested_owned_files':len(manifest['entries']),
                      'bound_source_files':len(inputs['source_files']),
                      'bound_foreign_primary_objects':len(inputs['foreign_primary_objects']),
                      'native_payloads':len(members),'file_writes':False,
                      'final_seal_sha256':sha(R/'FINAL_SEAL.json'),
                      'artifact_manifest_sha256':sha(R/'ARTIFACT_MANIFEST.json'),
                      'input_manifest_sha256':sha(R/'INPUT_MANIFEST.json')},sort_keys=True))


if __name__=='__main__':
    main()
