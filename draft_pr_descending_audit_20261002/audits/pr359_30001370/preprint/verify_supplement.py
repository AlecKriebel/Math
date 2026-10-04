#!/usr/bin/env python3
"""Portable read-only supplement verification. Python3.10+, no default dependencies.

Use --full for unchanged original/SymPy controls (SymPy1.14.0 required).
No downloads, installations, external source substitution or generated files.
"""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');args=ap.parse_args()
    manifest=json.loads((ROOT/'FILE_MANIFEST.json').read_bytes())
    paths=[r['path'] for r in manifest['files']]
    assert len(paths)==len(set(paths))
    discovered=list(ROOT.rglob('*'));assert not any(p.is_symlink() for p in discovered)
    actual={str(p.relative_to(ROOT)) for p in discovered if p.is_file()}
    assert actual==set(paths)|{'FILE_MANIFEST.json'},'Unexpected or missing supplement files.'
    for row in manifest['files']:
        path=Path(row['path']);assert not path.is_absolute() and '..' not in path.parts
        b=(ROOT/path).read_bytes();assert (len(b),sha(b))==(row['bytes'],row['sha256']),str(path)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    def run(script,args=(),expected=None):
        p=subprocess.run([sys.executable,'-B',str(ROOT/script),*map(str,args)],cwd=ROOT,capture_output=True,env=env)
        assert p.returncode==0 and not p.stderr,(script,p.returncode,p.stderr.decode(errors='replace'))
        if expected:assert p.stdout==(ROOT/expected).read_bytes(),script+' entire saved output'
        out=json.loads(p.stdout);assert out['status']=='PASS';return out
    alg=run('controls/algebra/check_uniform_algebra.py',
            ['--candidate-csv',ROOT/'candidate/TURN_3_CONTRACTION.csv'],
            'controls/algebra/UNIFORM_CERTIFICATE.json')
    topology=run('controls/topology/check_topology.py',expected='controls/topology/topology_checks.json')
    backward=run('controls/backward/verify_controls.py')
    # The exact fields are exact; the two labeled floating maxima use the
    # explicitly justified comparison policy in verify_controls.py.
    full=[]
    if args.full:
        for n in (1,2,3):
            full.append(run(f'candidate/check_turn_{n}.py',expected=f'candidate/TURN_{n}_CHECKS.json'))
        full.append(run('candidate/review/check_independent.py',expected='candidate/review/INDEPENDENT_CHECKS.json'))
        full.append(run('candidate/verify_packet.py'))
        full.append(run('controls/algebra/check_symbolic_equations.py',expected='controls/algebra/SYMBOLIC_IDENTITIES.json'))
    print(json.dumps({'status':'PASS','files_verified':len(paths),
                      'continuous_exact_certificates':'sharp rank-one determinant/polynomial and separate Bernstein positivity',
                      'topology_exact_controls':topology['exact_assertions'],
                      'backward_exact_controls':backward['exact_assertions'],
                      'backward_numerical_summary_policy':backward['absolute_numeric_summary_tolerance'],
                      'original_interval_rows':alg['original_table_rows'],
                      'optional_full_program_runs':len(full),
                      'original_source_hash_check':'not performed: copyrighted primary PDFs are deliberately not redistributed',
                      'limitations':'Finite reproductions supplement the analytical proof; source and bounded literature audit results are documented, not inferred from this run.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
