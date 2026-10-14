#!/usr/bin/env python3
"""Replay the finite proof components and supplementary diagnostics in a temporary copy.
The analytic arguments and scope limitations in the Markdown files remain essential.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile

if not __debug__ or sys.flags.optimize:
    raise SystemExit('Refusing optimized Python: run python run_checks.py without -O or -OO.')
ROOT=Path(__file__).resolve().parent
RUNS=(
 'pass1_devil/check_restricted_obstructions.py',
 'pass1_fixed_time/verify_bounds.py',
 'pass1_game_audit/finite_game_reference.py',
 'pass1_survival/certify_terminal_1d.py',
 'pass1_game_audit/replay_1d_certificate_independent.py',
 'pass2_audit/check_profile_recursion_independent.py',
 'pass2_deadlines/verify_three_deadlines.py',
 'pass2_devil/check_three_deadline_constants.py',
 'pass2_invariant/profile_certificate.py',
 'pass2_survival/verify_exact_bounds.py',
 'pass3_deadlines/verify_four_deadlines.py',
 'pass3_devil/replay_four_deadlines_independent.py',
 'pass3_independent/check_tracking_constants.py',
 'pass3_survival/verify_bridge_bounds.py',
 'pass4_multiscale/verify_examples.py',
 'pass5_coupling/verify_mass_family.py',
 'pass5_devil/replay_periodic_history.py',
 'pass5_multiscale/verify_periodic_schedule.py',
 'pass5_survival/verify_adaptive_threshold_example.py',
)

def require(ok,message):
    if not ok: raise RuntimeError(message)

def run():
    before={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob('*') if p.is_file()}
    records=[]
    with tempfile.TemporaryDirectory(prefix='timebomb-public-replay-') as temp:
        work=Path(temp)/'public'
        shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('__pycache__'))
        env=dict(os.environ)
        env.pop('PYTHONOPTIMIZE',None)
        for rel in RUNS:
            # -I ignores Python environment settings; no optimization option is used.
            cp=subprocess.run([sys.executable,'-I','-B',str(work/rel)],cwd=work,
                              env=env,text=True,capture_output=True,timeout=180)
            require(cp.returncode==0,'Checker failed: '+rel+'\n'+cp.stderr)
            require(not cp.stderr.strip(),'Unexpected checker stderr: '+rel+'\n'+cp.stderr)
            try: result=json.loads(cp.stdout)
            except json.JSONDecodeError: result=cp.stdout.strip()
            records.append({'script':rel,'sha256':hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),
                            'returncode':cp.returncode,'assertions_enabled':True,'result':result})
        results={r['script']:r['result'] for r in records}
        four=results['pass3_devil/replay_four_deadlines_independent.py']
        require(four['case_count']==180 and four['maximum_cost']=='34777/50976'
                and four['all_producer_costs_and_divisors_match'] is True,'Four-time replay summary')
        cert=json.loads((work/'pass1_survival/terminal_1d_horizon6_certificate.json').read_text())
        verifier=runpy.run_path(str(work/'pass1_survival/certify_terminal_1d.py'))['verify']
        require(verifier(cert)['verified'] is True,'Valid 1D certificate rejected')
        mutations=[]
        bad=copy.deepcopy(cert);bad['horizon']=7;mutations.append(('wrong_horizon',bad))
        bad=copy.deepcopy(cert);bad['dimension']=2;mutations.append(('wrong_dimension',bad))
        bad=copy.deepcopy(cert);bad['first_bomb_relative_to_first_angel_position']=1;mutations.append(('wrong_first_announcement',bad))
        bad=copy.deepcopy(cert);bad['states'][bad['root']]['responses'].pop();mutations.append(('missing_response',bad))
        bad=copy.deepcopy(cert);bad['states'][bad['root']]['bombs']=[100];mutations.append(('wrong_root_state',bad))
        bad=copy.deepcopy(cert)
        leaf=next(row for row in bad['states'].values() if row['remaining_moves']==1)
        leaf['bombs']=[];mutations.append(('nonlethal_leaf',bad))
        rejected=[]
        for label,bad in mutations:
            try: verifier(bad)
            except (RuntimeError,KeyError,ValueError,TypeError): rejected.append(label)
            else: raise RuntimeError('Malformed certificate accepted: '+label)
        require(len(rejected)==6,'Incomplete malformed-certificate controls')
        adaptive=results['pass5_survival/verify_adaptive_threshold_example.py']
        require(adaptive['words']==729 and adaptive['history_rounds']==24
                and adaptive['maximum_lead']==24,'Adaptive-preload diagnostic summary')
        profile=results['pass2_invariant/profile_certificate.py']
        require(profile['three_times']['terminal_bound']=='52/103'
                and profile['three_times']['certified'] is True
                and profile['consecutive_gap_recursion_failure']['smoothing_step']==27,
                'Profile diagnostic summary')
        smoke=results['pass1_game_audit/finite_game_reference.py']
        require([r['horizon'] for r in smoke['finite_horizons']]==[1,2,3,4]
                and all(r['angel_wins'] is True for r in smoke['finite_horizons'])
                and smoke['geometry']['nonempty_center_subsets_verified']==511,'Finite smoke summary')
    after={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
           for p in ROOT.rglob('*') if p.is_file()}
    require(before==after,'Public source tree changed during replay')
    return {'status':'PASS','python_version':sys.version.split()[0],
            'script_count':len(records),'assertions_enabled':True,
            'source_tree_modified':False,'malformed_1d_certificates_rejected':rejected,
            'scope':'Four-time finite certificate and 1D certificate replay are proof components. Other finite checks are supplementary diagnostics, not general-game proofs.',
            'checks':records}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
