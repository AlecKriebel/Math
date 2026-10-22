"""Replay and adversarial tests; finite tests supplement, not replace, proofs."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(path, optimized=False):
    return subprocess.run([sys.executable] + (['-O'] if optimized else []) + [str(path)], capture_output=True)


def main():
    report = {'replay': [], 'mathematical_mutations': [], 'manifest_controls': []}
    source = (ROOT / 'verify_identities.py').read_text()
    mutations = {
        'wrong_square_count': ('(p ** n + p ** (n - 1)) // 2', '(p ** n + p ** (n - 1)) // 3'),
        'false_parity_identity': ("counts['nonzero_square'] == counts['nonsquare']", "counts['nonzero_square'] != counts['nonsquare']"),
        'omit_composition_sign': ('(-1) ** m * 4 ** m', '1 * 4 ** m'),
    }
    for optimized in (False, True):
        mode = '-O' if optimized else 'normal'
        replay = run(ROOT / 'verify_identities.py', optimized)
        require(replay.returncode == 0 and replay.stdout == (ROOT / 'IDENTITY_CHECKS.json').read_bytes() and replay.stderr == b'', 'Full output mismatch '+mode)
        report['replay'].append({'mode':mode,'exact_output_match':True})
        for name, (old, new) in mutations.items():
            require(source.count(old)==1, 'Mutation anchor mismatch '+name)
            with tempfile.TemporaryDirectory() as temp:
                target = Path(temp) / 'mutant.py'
                target.write_text(source.replace(old,new))
                result = run(target, optimized)
                require(result.returncode != 0 and b'AssertionError: Exact identity check failed' in result.stderr, 'Mathematical mutation survived '+name+' '+mode)
            report['mathematical_mutations'].append({'case':name,'mode':mode,'rejected':True})
        controls = ['baseline','missing','changed','extra','nested_manifest','symlink','manifest_symlink','empty_directory','duplicate_record','unsafe_path']
        for case in controls:
            with tempfile.TemporaryDirectory() as temp:
                clone=Path(temp)/'package'; shutil.copytree(ROOT,clone)
                if case=='missing': (clone/'IDENTITY_CHECKS.json').unlink()
                if case=='changed':
                    target=clone/'IDENTITY_CHECKS.json'; b=target.read_bytes(); target.write_bytes(bytes([b[0]^1])+b[1:])
                if case=='extra': (clone/'extra.txt').write_text('unexpected')
                if case=='nested_manifest':
                    (clone/'nested').mkdir(); (clone/'nested/MANIFEST.json').write_text('{}')
                if case=='symlink':
                    target=clone/'IDENTITY_CHECKS.json'; target.unlink(); target.symlink_to(ROOT/'IDENTITY_CHECKS.json')
                if case=='manifest_symlink':
                    target=clone/'MANIFEST.json'; target.unlink(); target.symlink_to(ROOT/'MANIFEST.json')
                if case=='empty_directory': (clone/'empty').mkdir()
                if case in ('duplicate_record','unsafe_path'):
                    target=clone/'MANIFEST.json'; data=json.loads(target.read_text())
                    if case=='duplicate_record': data['files'].append(data['files'][0])
                    else: data['files'][0]['path']='../escape'
                    target.write_text(json.dumps(data))
                result=run(clone/'verify_manifest.py',optimized)
                require((result.returncode==0)==(case=='baseline'), 'Manifest control failed '+case+' '+mode)
                if case!='baseline': require(b'ValueError:' in result.stderr, 'Unexpected failure '+case)
                report['manifest_controls'].append({'case':case,'mode':mode,'expected_outcome_observed':True})
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
