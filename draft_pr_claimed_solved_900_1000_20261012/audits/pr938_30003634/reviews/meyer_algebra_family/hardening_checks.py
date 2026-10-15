#!/usr/bin/env python3
"""Optimization-mode, read-only-default, baseline-equivalence and rejection checks."""
import argparse
import ast
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PROGRAMS = ['reproduce.py', 'compare_after.py', 'authenticate.py']
OLD_EXTERNAL_SEAL = 'fdef3b2c42f877192921622330166c2986a513cb90be927bb1b7014b78c1cf31'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def top_files():
    return {f.name: sha(f.read_bytes()) for f in HERE.iterdir() if f.is_file()}

def no_timestamp(data):
    result = dict(data)
    result.pop('utc', None)
    return result

def worker(mode):
    expected_level = {'normal': 0, 'O': 1, 'OO': 2, 'inherited2': 2}[mode]
    require(sys.flags.optimize == expected_level, 'Worker optimization differs from requested mode')
    if mode == 'inherited2':
        require(os.environ.get('PYTHONOPTIMIZE') == '2', 'Inherited2 worker is not actually inheriting environment value2')
    args = ['-O'] if mode == 'O' else ['-OO'] if mode == 'OO' else []
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    before = top_files()
    probe = subprocess.run([sys.executable, *args, '-c', 'import json,os,sys;print(json.dumps(dict(optimize=sys.flags.optimize,environment=os.environ.get("PYTHONOPTIMIZE"))))'], env=env, text=True, capture_output=True, check=True)
    observed = json.loads(probe.stdout)
    require(observed['optimize'] == expected_level, 'Child optimization level differs')
    if mode == 'inherited2':
        require(observed['environment'] == '2' and not args, 'Child did not inherit optimization2 without a flag override')
    baseline = json.loads((HERE / 'INDEPENDENT_RESULTS.json').read_text())
    passed = []
    for program in PROGRAMS:
        run = subprocess.run([sys.executable, *args, str(HERE / program)], env=env, text=True, capture_output=True)
        require(run.returncode == 0, 'Valid replay failed: ' + mode + '/' + program + '\n' + run.stderr)
        data = json.loads(run.stdout)
        if program == 'reproduce.py':
            require(no_timestamp(data) == no_timestamp(baseline), 'Mathematics differs from the independent initial baseline')
        elif program == 'compare_after.py':
            require(all(data['comparisons'].values()) and data['replay_equal_except_timestamp'] and data['child_optimization_preserved'], 'Comparison replay missing verification')
            require(data['runtime_optimization_level'] == expected_level, 'Comparison mode not reported correctly')
        else:
            require(data['count'] == 44 and data['disk_file_count'] == 44 and data['all_equal'] and data['closed_disk_inventory_equal'] and data['branch'] == 'main', 'Actual selected authentication failed')
        passed.append(dict(program=program, exit=run.returncode, stdout_sha256=sha(run.stdout.encode()), json_accepted=True))
    prefix = 'import sys,json;sys.dont_write_bytecode=True;sys.path.insert(0,' + repr(str(HERE)) + ');print("optimization="+str(sys.flags.optimize),file=sys.stderr,flush=True);'
    negative = {
        'false_expected_signature': 'import reproduce as r;r.calculate(expected_signature=0)',
        'nonsymmetric_form': 'import reproduce as r;r.inertia([[0,1],[0,0]])',
        'false_expected_Meyer_form': 'import reproduce as r;r.require(r.meyer(r.T[1],r.T[1],True)["intersection_form"]==[[-2]],"Deliberately false expected Meyer form")',
        'false_actual_authentication_pin': 'import authenticate as a;a.authenticate(expected_proof_sha256="0"*64)',
        'false_certificate_term': 'import compare_after as c;d=json.loads((c.HERE/"INDEPENDENT_RESULTS.json").read_text());p=d["power_pairs"];bad=dict(word=d["free_reduced_word"],syllables=[x for pair in zip(p["A"],p["B"]) for x in pair],pairwise_linking=[0,0,0],burau_matrix=[x for row in d["final_Burau_matrix"] for x in row],signature=-2,meyer_terms=[t["meyer"] for t in d["meyer_terms"]]);bad["meyer_terms"][0]=1;c.compare_certificate(d,bad)'
    }
    rejected = []
    for name, code in negative.items():
        run = subprocess.run([sys.executable, *args, '-c', prefix + code], env=env, text=True, capture_output=True)
        require(run.returncode != 0, 'Deliberately false check was accepted: ' + mode + '/' + name)
        require('optimization=' + str(expected_level) in run.stderr and 'VerificationError' in run.stderr, 'Rejection did not reach the explicit check at requested optimization: ' + name + '\n' + run.stderr)
        rejected.append(dict(check=name, exit=run.returncode, explicit_VerificationError=True, observed_optimize=expected_level, stderr_sha256=sha(run.stderr.encode())))
    require(top_files() == before, 'A default replay or rejection check mutated family top-level files')
    return dict(mode=mode, parent_optimize=sys.flags.optimize, child_probe=observed, valid_replays=passed, rejected_controls=rejected, default_replays_preserved_top_level_files=True, all_initial_mathematical_data_equal_except_timestamp=True)

def calculate():
    for program in PROGRAMS + ['hardening_checks.py']:
        tree = ast.parse((HERE / program).read_text())
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), 'Optimization-removable check remains: ' + program)
    def dispatch(mode):
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        flags = ['-O'] if mode == 'O' else ['-OO'] if mode == 'OO' else []
        if mode == 'inherited2':
            env['PYTHONOPTIMIZE'] = '2'
        run = subprocess.run([sys.executable, *flags, str(HERE / 'hardening_checks.py'), '--worker', mode], env=env, text=True, capture_output=True)
        require(run.returncode == 0, 'Hardening worker failed: ' + mode + '\n' + run.stderr)
        return json.loads(run.stdout)
    modes = ['normal', 'O', 'OO', 'inherited2']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(dispatch, modes))
    return dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),kind='Code hardening only, no mathematical or source change',prior_external_public_map_sha256=OLD_EXTERNAL_SEAL,prior_public_map_entry_count=13,public_programs_have_no_ast_Assert=True,current_program_sha256={name: sha((HERE / name).read_bytes()) for name in PROGRAMS + ['hardening_checks.py']},initial_independent_result_sha256=sha((HERE / 'INDEPENDENT_RESULTS.json').read_bytes()),modes=results,successful_valid_program_replays=12,rejected_deliberately_false_controls=20,mathematical_data_unchanged=True,all_default_replays_stdout_only_and_file_preserving=True)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', choices=['normal', 'O', 'OO', 'inherited2'])
    parser.add_argument('--output', type=Path, help='Explicit result destination; omitted means stdout only.')
    args = parser.parse_args(argv)
    result = worker(args.worker) if args.worker else calculate()
    payload = json.dumps(result, indent=2) + '\n'
    if args.output is not None:
        args.output.write_text(payload)
    sys.stdout.write(payload)

if __name__ == '__main__':
    main()
