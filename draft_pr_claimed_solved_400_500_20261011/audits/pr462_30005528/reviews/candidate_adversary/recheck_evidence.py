#!/usr/bin/env python3
"""Read-only whole-candidate evidence replay, with all writes in owned temp dirs.

No acceptance assert is used. Original and peer sources are copied, never run in
place. This does not repair history or certify universal mathematical claims.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
from math import gcd, isqrt
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

OWN = Path(__file__).resolve().parent
CASE = OWN.parent.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run_script(path, cwd, optimized, args=()):
    env = dict(os.environ)
    env['PYTHONOPTIMIZE'] = '1' if optimized else '0'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    flags = ['-B', '-O'] if optimized else ['-B']
    return subprocess.run([sys.executable, *flags, str(path), *map(str,args)],
                          cwd=cwd, env=env, capture_output=True, timeout=45)


def summarized(proc, label, optimized):
    return {'label': label, 'optimized': optimized, 'exit_code': proc.returncode,
            'stdout_bytes': len(proc.stdout), 'stdout_sha256': sha(proc.stdout),
            'stderr_last_line': proc.stderr.decode(errors='replace').splitlines()[-1:][0:1]}


def main():
    receipt = json.loads((CASE/'SOURCE_RECEIPT.json').read_text())
    before = {}
    for item in receipt['files']:
        data = (CASE/'source_snapshot'/item['path']).read_bytes()
        require(len(data)==item['bytes'] and sha(data)==item['sha256'], 'source receipt mismatch')
        before[item['path']] = sha(data)
    origin = CASE/'source_snapshot/unsolved_math_prioritization/attempts/30005528'
    author_text = (origin/'release/checks/verify_rotation_family.py').read_text()
    author_asserts = sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(author_text)))
    require(author_asserts==20, 'author assertion count changed')
    expected_author = (origin/'release/checks/verification_results.json').read_bytes()
    expected_audit = (origin/'audit/audit_controls.json').read_bytes()
    fresh_origin = CASE/'reviews/reproduction/integer_pell_controls.py'
    expected_fresh = (CASE/'reviews/reproduction/integer_pell_results.json').read_bytes()
    fresh_text = fresh_origin.read_text()
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(fresh_text))), 'fresh assert guard')
    wrong_messages = {
        'periodic_minimizer':'false periodic minimizer',
        'unreduced_period':'false least period',
        'drop_initial_cost':'false prefix normalization',
        'rationalization_plus':'false rationalization sign',
        'rationalization_missing_denominator':'false rationalization denominator',
        'reversed_gap':'false gap direction',
    }
    mutations = {
        'unreduced_period': ('q = n // gcd(m, n)', 'q = n'),
        'approximation_below': ('m = isqrt(2 * n * n) + 1', 'm = isqrt(2 * n * n)'),
        'drop_initial_cost': ('range(N + 1)', 'range(N)'),
        'wrong_height_sign': ('t = Qsqrt2(angle, Q(-1))', 't = Qsqrt2(angle, Q(1))'),
        'wrong_rationalization': ('Q(p*p - 2*q*q, q*q)', 'Q(p*p + 2*q*q, q*q)'),
        'inverted_sign': ('delta = a * a - 2 * b * b', 'delta = 2 * b * b - a * a'),
    }
    runs, mutated, fresh_wrong = [], [], []
    with tempfile.TemporaryDirectory(prefix='owned-evidence-', dir=OWN) as tmpstr:
        tmp = Path(tmpstr)
        shutil.copytree(origin/'release',tmp/'release')
        (tmp/'audit').mkdir()
        for name in ['audit_controls.py','FROZEN_INPUTS.json']:
            shutil.copyfile(origin/'audit'/name,tmp/'audit'/name)
        (tmp/'fresh.py').write_text(fresh_text)
        for optimized in (False,True):
            proc=run_script(tmp/'release/checks/verify_rotation_family.py',tmp,optimized)
            require(proc.returncode==0 and proc.stdout==expected_author, 'author baseline replay')
            runs.append(summarized(proc,'frozen_author_baseline',optimized))
            proc=run_script(tmp/'audit/audit_controls.py',tmp,optimized,('--release',tmp/'release'))
            if optimized:
                require(proc.returncode!=0 and b'invalid_mutations_rejected' in proc.stderr and not proc.stdout,
                        'optimized historical audit must retain its actual failure')
            else:
                require(proc.returncode==0 and proc.stdout==expected_audit,'normal audit byte replay')
            runs.append(summarized(proc,'frozen_historical_audit',optimized))
            proc=run_script(tmp/'fresh.py',tmp,optimized)
            require(proc.returncode==0 and proc.stdout==expected_fresh, 'fresh Pell byte replay')
            data=json.loads(proc.stdout)
            require(data['checks_total']==51532 and data['finite_coverage']['pell_instances']==30,
                    'fresh coverage count')
            runs.append(summarized(proc,'fresh_explicit_guard_Pell_51532',optimized))
            for name,message in wrong_messages.items():
                proc=run_script(tmp/'fresh.py',tmp,optimized,('--wrong-claim',name))
                require(proc.returncode!=0 and ('ValueError: '+message).encode() in proc.stderr,
                        'wrong claim must fail at its actual predicate')
                require(b'wrong claim unexpectedly reached end' not in proc.stderr,
                        'unconditional fallback cannot certify predicate rejection')
                fresh_wrong.append({'claim':name,'optimized':optimized,'exit_code':proc.returncode,
                                    'predicate_failure_confirmed':True})
            for name,(old,new) in mutations.items():
                require(author_text.count(old)==1,'mutation source anchor')
                path=tmp/(name+'.py'); path.write_text(author_text.replace(old,new))
                proc=run_script(path,tmp,optimized)
                require(proc.returncode==0 if optimized else proc.returncode!=0,'historical mutation behavior changed')
                mutated.append({'claim':name,'optimized':optimized,'exit_code':proc.returncode,
                                'stdout_matches_original_passed_json':proc.stdout==expected_author})
    # Independently calculate a Pell family via direct coefficient multiplication.
    pell=[]
    numerator,denominator=1,0
    for j in range(1,41):
        numerator,denominator=3*numerator+4*denominator,2*numerator+3*denominator
        require(numerator*numerator-2*denominator*denominator==1, 'independent Pell norm')
        require(gcd(numerator,denominator)==1, 'independent Pell reduction')
        require(isqrt(2*denominator*denominator)+1==numerator,'independent Pell ceil')
        require((numerator-denominator)**2<2*denominator*denominator,'independent Pell height <=1')
        if j in (1,10,30,40):
            pell.append({'j':j,'p':numerator,'q':denominator,'norm':1})
    after={item['path']:sha((CASE/'source_snapshot'/item['path']).read_bytes()) for item in receipt['files']}
    require(after==before,'source changed during replay')
    result={'reviewer':'/root/pr462_candidate_adversary','pr':462,'problem_id':'30005528',
            'frozen_head':receipt['head_sha'],'utc':datetime.now(timezone.utc).isoformat(),
            'status':'expected_successes_and_historical_failures_reproduced',
            'source_files_checked_and_unchanged':len(before),'author_static_assert_count':author_asserts,
            'runs':runs,'historical_author_mutations':mutated,'fresh_wrong_predicates':fresh_wrong,
            'independent_Pell_instances':40,'independent_Pell_samples':pell,
            'retained_V1':True,'historical_optimized_audit_pass':False,
            'finite_checks_prove_infinite_theorem_or_priority':False}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
