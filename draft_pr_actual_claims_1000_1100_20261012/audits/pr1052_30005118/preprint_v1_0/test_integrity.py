#!/usr/bin/env python3
"""Adversarial local upload-wrapper and safe-path tests; Python stdlib only."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default='_runs/integrity.json')
    args = ap.parse_args()
    out = ROOT/args.output
    out.resolve().relative_to(ROOT)
    out.parent.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('integrity_verifier', ROOT/'verify_support.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    z = json.loads((ROOT/'.zenodo.json').read_text())
    w = json.loads((ROOT/'metadata.json').read_text())
    accepted = rejected = 0
    with tempfile.TemporaryDirectory(prefix='integrity-', dir=out.parent) as temp:
        d = Path(temp)
        module.ROOT = d
        for name in ['.zenodo.json', 'metadata.json', 'paper.pdf']:
            shutil.copyfile(ROOT/name, d/name)
        # Synthetic archive bytes allow standalone clean-extraction tests.
        (d/'pr1052_support_v1_0.zip').write_bytes(b'local wrapper binding test')
        baseline = {'metadata': z, 'files': [{'filename': name, 'bytes': (d/name).stat().st_size, 'sha256': module.sha((d/name).read_bytes())} for name in ['paper.pdf', 'pr1052_support_v1_0.zip']]}
        module.verify_upload_if_present(); accepted += 1
        (d/'zenodo-deposit.json').write_text(json.dumps(baseline))
        module.verify_upload_if_present(); accepted += 1
        cases = []
        for key, value in [('title', 'wrong title'), ('publication_type', 'article'), ('license', 'cc0-1.0'), ('version', '9'), ('creators', [])]:
            t = copy.deepcopy(baseline); t['metadata'][key] = value; cases.append(t)
        for key, value in [('bytes', -1), ('sha256', '0'*64), ('filename', '../paper.pdf')]:
            t = copy.deepcopy(baseline); t['files'][0][key] = value; cases.append(t)
        t = copy.deepcopy(baseline); t['files'].pop(); cases.append(t)
        t = copy.deepcopy(baseline); t['unexpected'] = True; cases.append(t)
        t = copy.deepcopy(baseline); t['files'][0]['unexpected'] = True; cases.append(t)
        for t in cases:
            (d/'zenodo-deposit.json').write_text(json.dumps(t))
            try:
                module.verify_upload_if_present()
            except (ValueError, KeyError):
                rejected += 1
            else:
                raise RuntimeError('bad wrapper accepted')
        # Even matching all metadata copies must retain the preprint identity.
        bad = copy.deepcopy(z); bad['publication_type'] = 'article'
        (d/'.zenodo.json').write_text(json.dumps(bad))
        badw = copy.deepcopy(w); badw['metadata'] = bad
        (d/'metadata.json').write_text(json.dumps(badw))
        badb = copy.deepcopy(baseline); badb['metadata'] = bad
        (d/'zenodo-deposit.json').write_text(json.dumps(badb))
        try:
            module.verify_upload_if_present()
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError('matching bad publication identity accepted')
        for path in ['../x', '/x', 'a//b', 'a/./b', 'a/../b', 'a\\b', '', 'C:/x', 'x\x00y']:
            try:
                module.safe(path)
            except ValueError:
                rejected += 1
            else:
                raise RuntimeError('unsafe path accepted')
    result = {'all_checks_passed': True, 'valid_wrapper_controls': accepted, 'invalid_wrapper_and_path_controls_rejected': rejected, 'external_descriptor_required_for_clean_extraction': False}
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
