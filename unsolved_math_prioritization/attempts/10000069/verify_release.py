#!/usr/bin/env python3
"""Offline exact-byte replay and corruption controls, not a proof assistant."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

AUTHOR = set('EXACT_CONTROLS.json HISTORY_AND_SOURCE_AUDIT.md MANIFEST.sha256 MODEL_AND_STATUS.md PROOF_RECONSTRUCTION.md PUBLIC_SOURCE_MANIFEST.json README.md RESEARCH_LEDGER.json VERIFICATION_NOTES.md verify_exact_controls.py'.split())
AUDIT = set('AUDIT.md ERRATA_AND_SCOPE.md EXACT_BINDING.json INDEPENDENT_CONTROLS.json MANIFEST.sha256 NEGATIVE_CONTROLS.md PUBLIC_SOURCE_VERIFICATION.json README.md RESULTS.json SOURCE_UPDATE.md independent_controls.py verify_audit.py'.split())
TOP = set('README.md RELEASE_STATUS.json RELEASE_MANIFEST.json REPLAY_RESULTS.json verify_release.py'.split())
EXPECTED = TOP | {'author/'+s for s in AUTHOR} | {'independent_audit/'+s for s in AUDIT}
PINS = {'author/MANIFEST.sha256':'65297b9b4168ebd859dace3416a1bb01c559ad6ebd90235d52e9e82a6420f50d',
        'independent_audit/MANIFEST.sha256':'1d8243213088369561b10d10d6410856a1800ae5c0204b28904695dcf53f5675'}
RELATION = 'E(X-Y)^2 = 2(EX^2-1) <= 2(R-1).'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def read_json(p):
    return json.loads(p.read_bytes())

def safe_name(name):
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'unsafe path: '+name)

def check_record(root, name, record):
    safe_name(name)
    b = (root/name).read_bytes()
    require(len(b) == record['bytes'] and sha(b) == record['sha256'], 'byte binding: '+name)

def verify(root, replay=True):
    files, dirs = set(), set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink')
        name = p.relative_to(root).as_posix()
        if p.is_file():
            files.add(name)
        else:
            require(p.is_dir(), 'special node')
            dirs.add(name)
    require(files == EXPECTED and dirs == {'author','independent_audit'}, 'exact inventory')
    m = read_json(root/'RELEASE_MANIFEST.json')
    require(m['schema'] == 1 and m['problem_id'] == '10000069', 'manifest identity')
    rows = m['files']
    require(len(rows) == len(EXPECTED)-1 and {r['path'] for r in rows} == EXPECTED-{'RELEASE_MANIFEST.json'}, 'manifest inventory')
    for row in rows:
        check_record(root,row['path'],row)
    for name,pin in PINS.items():
        require(sha((root/name).read_bytes()) == pin, 'immutable pin: '+name)
    for folder, inventory in [('author',AUTHOR),('independent_audit',AUDIT)]:
        names = []
        for line in (root/folder/'MANIFEST.sha256').read_text().splitlines():
            digest,name = line.split('  ',1)
            safe_name(name); names.append(name)
            require(sha((root/folder/name).read_bytes()) == digest, 'frozen manifest: '+name)
        require(len(names) == len(inventory)-1 and set(names) == inventory-{'MANIFEST.sha256'}, 'frozen inventory')
    binding = read_json(root/'independent_audit/EXACT_BINDING.json')
    require(binding['problem_id'] == '10000069' and len(binding['input_files']) == 10, 'audit binding identity')
    require({r['name'] for r in binding['input_files']} == AUTHOR, 'audit target inventory')
    for row in binding['input_files']:
        check_record(root/'author',row['name'],{'bytes':row['byte_count'],'sha256':row['sha256']})
    status = read_json(root/'RELEASE_STATUS.json')
    require(status['problem_id'] == '10000069' and status['rank'] == 711, 'release identity')
    require(status['queue_status'] == 'unsolved' and status['turns'] == '1/5' and status['substantive_routes'] == 1, 'queue disposition')
    require(status['local_erratum_E1_adopted'] is True and status['corrected_relation']+'.' == RELATION, 'erratum gate')
    require(status['candidate_commit'] == 'a875da08e8bfbdb70fd8165c097ab036731b5f6f' and status['candidate_repository'] == 'DannyExperiments/random-series-parallel-distance-exponent', 'credit gate')
    require(status['expectation_exponent'] is True and status['parameter'] == 'series probability p' and status['interior_domain'] == '(1/2,1)', 'model gate')
    for key in ['full_shape_resolution','novelty_claim','five_route_exhaustion','elementary_scalar_formula','eigenprofile_uniqueness','all_normalized_laws_converge','later_almost_sure_preprint_proof_audited','literature_wide_almost_sure_openness_claim','raw_corpus_hash_certified','controls_replace_analytic_proof']:
        require(status[key] is False,'scope gate: '+key)
    for key in ['source_pdf_404_index_only','catalogue_403','frozen_originals_preserved']:
        require(status[key] is True,'limit gate: '+key)
    require(status['author_controls'] == 2158 and status['independent_controls'] == 156596 and status['independent_mathematical_negatives'] == 10, 'control counts')
    guide = (root/'README.md').read_text()
    for text in [RELATION,'arXiv:2609.23802v1','HTTP 404','HTTP 403','not a literature-wide assertion of openness','Queue: unsolved','1/5']:
        require(text in guide,'controlling guide: '+text)
    verdict = read_json(root/'independent_audit/RESULTS.json')
    require(verdict['verdict'] == 'APPROVE_QUALIFIED_CREDITED_CHARACTERIZATION_WITH_LOCAL_ERRATUM', 'audit verdict')
    result = {'integrity':'PASS','release_files':len(EXPECTED),'author_files':10,'audit_files':12,
              'qualification':'Exact-byte integrity and finite controls only; analytic proof and source limitations are separately documented.'}
    if replay:
        run = subprocess.run([sys.executable,'-I','-B',str(root/'independent_audit/verify_audit.py'),str(root/'author')],capture_output=True,check=True,cwd='/tmp')
        require(not run.stderr,'unexpected replay stderr')
        got=json.loads(run.stdout)
        require(got['status'] == 'PASS' and got['author_replay_assertions'] == 2158 and got['independent_replay_assertions'] == 156596,'exact replay counts')
        require(got['original_manifest_sha256'] == PINS['author/MANIFEST.sha256'] and got['audit_manifest_sha256'] == PINS['independent_audit/MANIFEST.sha256'],'replay target pins')
        result['replay'] = got
    return result

def corruption_controls(root):
    cases = ['changed_author','changed_audit','changed_guide','missing','extra_hidden','nested_empty','symlink','unlisted_pdf',
             'manifest_traversal','manifest_omission','manifest_duplicate','coordinated_author','coordinated_audit',
             'wrong_status','wrong_turns','removed_erratum','wrong_relation','full_shape','novelty','as_openness','preprint_audited',
             'removed_source_limit','missing_guide_erratum']
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='random-sp-corruption-') as td:
            p=Path(td)/'packet';shutil.copytree(root,p)
            outer=read_json(p/'RELEASE_MANIFEST.json')
            def rebind(name):
                b=(p/name).read_bytes()
                for row in outer['files']:
                    if row['path'] == name:
                        row.update(bytes=len(b),sha256=sha(b));return
                raise ValueError('unlisted mutation')
            if case.startswith('changed_'):
                name={'changed_author':'author/PROOF_RECONSTRUCTION.md','changed_audit':'independent_audit/AUDIT.md','changed_guide':'README.md'}[case]
                b=bytearray((p/name).read_bytes());b[0]^=1;(p/name).write_bytes(b)
            elif case == 'missing': (p/'README.md').unlink()
            elif case == 'extra_hidden': (p/'.extra').write_text('synthetic corruption')
            elif case == 'nested_empty': (p/'author/empty').mkdir()
            elif case == 'symlink': (p/'README.md').unlink();(p/'README.md').symlink_to('author/README.md')
            elif case == 'unlisted_pdf': (p/'source.pdf').write_bytes(b'%PDF synthetic corruption')
            elif case.startswith('manifest_'):
                if case == 'manifest_traversal': outer['files'][0]['path']='../README.md'
                elif case == 'manifest_omission': outer['files'].pop()
                else: outer['files'].append(dict(outer['files'][0]))
            elif case.startswith('coordinated_'):
                folder,name=('author','PROOF_RECONSTRUCTION.md') if case.endswith('author') else ('independent_audit','AUDIT.md')
                target=folder+'/'+name; manifest=folder+'/MANIFEST.sha256'
                (p/target).write_bytes((p/target).read_bytes()+b'\nsynthetic mutation\n')
                lines=(p/manifest).read_text().splitlines()
                lines=[sha((p/target).read_bytes())+'  '+name if line.split('  ',1)[1] == name else line for line in lines]
                (p/manifest).write_text('\n'.join(lines)+'\n');rebind(target);rebind(manifest)
            elif case == 'missing_guide_erratum':
                (p/'README.md').write_text((p/'README.md').read_text().replace(RELATION,'E(X-Y)^2 = 2(R-1).'));rebind('README.md')
            else:
                key,value={'wrong_status':('queue_status','solved'),'wrong_turns':('turns','5/5'),'removed_erratum':('local_erratum_E1_adopted',False),
                           'wrong_relation':('corrected_relation','E(X-Y)^2 = 2(R-1)'), 'full_shape':('full_shape_resolution',True),
                           'novelty':('novelty_claim',True),'as_openness':('literature_wide_almost_sure_openness_claim',True),
                           'preprint_audited':('later_almost_sure_preprint_proof_audited',True),'removed_source_limit':('source_pdf_404_index_only',False)}[case]
                s=read_json(p/'RELEASE_STATUS.json');s[key]=value;(p/'RELEASE_STATUS.json').write_text(json.dumps(s));rebind('RELEASE_STATUS.json')
            (p/'RELEASE_MANIFEST.json').write_text(json.dumps(outer))
            try:
                verify(p,replay=False)
            except (ValueError,KeyError,OSError):
                pass
            else:
                raise RuntimeError('Accepted actual corruption: '+case)
    return cases

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--integrity-only',action='store_true')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    result=verify(Path(__file__).resolve().parent,replay=not args.integrity_only)
    if args.self_test:
        result['actual_corruptions_rejected']=corruption_controls(Path(__file__).resolve().parent)
    print(json.dumps(result,indent=2,sort_keys=True))
