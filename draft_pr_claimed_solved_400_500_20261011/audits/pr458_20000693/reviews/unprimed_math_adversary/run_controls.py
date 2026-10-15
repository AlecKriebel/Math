#!/usr/bin/env python3
"""Actually execute guarded mathematical mutants and private packet controls."""
import ast
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


OWN = Path(__file__).resolve().parent
CASE = OWN.parents[1]
FROZEN = CASE/'source_snapshot/unsolved_math_prioritization/attempts/20000693'
PRIVATE = OWN/'private_cases'


def require(condition, label):
    if not condition:
        raise ValueError(label)


def run_mutant(pair):
    mode, mutant = pair
    cmd = [sys.executable] + (['-O'] if mode == 'optimized' else [])
    cmd += [str(OWN/'verify_adversarial.py'), '--mutant', mutant]
    run = subprocess.run(cmd, cwd=OWN, capture_output=True)
    require(run.returncode == 1, f'{mode}/{mutant}: wrong exit')
    require(run.stdout == b'', f'{mode}/{mutant}: success output on rejection')
    diagnostic = run.stderr.decode().strip()
    require(diagnostic.startswith('REJECT: '), f'{mode}/{mutant}: wrong rejection cause')
    return {'mode':mode, 'mutant':mutant, 'exit_code':run.returncode,
            'stdout_bytes':len(run.stdout), 'diagnostic':diagnostic}


def packet_run(root, mode):
    cmd = [sys.executable] + (['-O'] if mode == 'optimized' else [])
    cmd += [str(root/'verify_publication.py')]
    return subprocess.run(cmd, cwd=root, capture_output=True)


def main():
    PRIVATE.mkdir(exist_ok=True)
    script = OWN/'verify_adversarial.py'
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(script.read_text()))),
            'fresh verifier may not contain assert guards')
    positives = [(OWN/name).read_bytes() for name in ['CHECKS_NORMAL.json','CHECKS_OPTIMIZED.json']]
    require(positives[0] == positives[1], 'positive outputs differ by mode')
    positive_report = json.loads(positives[0])
    require(positive_report['status'] == 'PASS' and positive_report['asymptotic_proved'] is False,
            'positive output overclaims scope')
    mutants = ['negative_weight','deletion_sign','finite_equals_full',
               'independent_local_phases','ignore_deletion','modulus_grouping',
               'conjugate_grouping','regularizer_sign','extra_gamma','declare_theorem']
    pairs = [(mode,mutant) for mode in ['normal','optimized'] for mutant in mutants]
    with ThreadPoolExecutor(max_workers=4) as executor:
        math_results = list(executor.map(run_mutant,pairs))
    packet_results=[]
    baseline_results=[]
    receipt=json.loads((CASE/'SOURCE_RECEIPT.json').read_text())
    for record in receipt['files']:
        path=CASE/'source_snapshot'/record['path']
        data=path.read_bytes()
        require(len(data)==record['bytes'] and sha256(data).hexdigest()==record['sha256'],
                'frozen source differs before private control')
    # The original frozen verifier is executed only in copies of its public packet.
    with tempfile.TemporaryDirectory(prefix='packet-',dir=PRIVATE) as temp:
        root=Path(temp)/'packet'
        shutil.copytree(FROZEN,root)
        for mode in ['normal','optimized']:
            run=packet_run(root,mode)
            require(run.returncode==0 and json.loads(run.stdout)['status']=='PASS',
                    f'packet {mode} baseline failed')
            baseline_results.append({'mode':mode,'exit_code':run.returncode,
                                     'stdout_sha256':sha256(run.stdout).hexdigest(),
                                     'status':json.loads(run.stdout)['status']})
        probes=[('unlisted_sentinel','Unexpected or missing public file'),
                ('same_size_hash_mutation','author/HEURISTIC.md: SHA-256 mismatch')]
        target=root/'author/HEURISTIC.md'
        original=target.read_bytes()
        for mechanism, expected_diagnostic in probes:
            if mechanism=='unlisted_sentinel':
                (root/'AUTHORED_NEGATIVE_SENTINEL.txt').write_text('private authored sentinel\n')
            else:
                target.write_bytes(bytes([original[0]^1])+original[1:])
                require(target.stat().st_size==len(original),'mutation changed byte size')
            for mode in ['normal','optimized']:
                run=packet_run(root,mode)
                stderr=run.stderr.decode()
                if mode=='normal':
                    require(run.returncode==1 and run.stdout==b'', f'{mechanism}: normal false acceptance')
                    require(expected_diagnostic in stderr,f'{mechanism}: did not reach intended guard')
                    status='REJECT'
                else:
                    require(run.returncode==0 and json.loads(run.stdout)['status']=='PASS',
                            f'{mechanism}: optimized falsePASS not reproduced')
                    status='FALSE_PASS'
                packet_results.append({'mechanism':mechanism,'mode':mode,
                    'exit_code':run.returncode,'status':status,'stdout_bytes':len(run.stdout),
                    'stdout_sha256':sha256(run.stdout).hexdigest(),
                    'intended_normal_guard':expected_diagnostic,
                    'intended_guard_reached_normally':expected_diagnostic in stderr if mode=='normal' else None})
            if mechanism=='unlisted_sentinel':
                (root/'AUTHORED_NEGATIVE_SENTINEL.txt').unlink()
            else:
                target.write_bytes(original)
    for record in receipt['files']:
        data=(CASE/'source_snapshot'/record['path']).read_bytes()
        require(len(data)==record['bytes'] and sha256(data).hexdigest()==record['sha256'],
                'frozen source differs after private control')
    report={'status':'PASS_SCOPED_FRESH_GUARDS_AND_REPRODUCED_FROZEN_BLOCKER',
            'fresh_guard_assert_nodes':0,
            'fresh_positive_checks_per_mode':positive_report['checks'],
            'fresh_positive_outputs_byte_identical':True,
            'fresh_positive_output_bytes':len(positives[0]),
            'fresh_positive_sha256':sha256(positives[0]).hexdigest(),
            'fresh_actual_negative_rejections_per_mode':len(mutants),
            'fresh_controls':math_results,
            'historical_packet_baselines':baseline_results,
            'historical_packet_controls':packet_results,
            'historical_packet_negative_probes_per_mode':len(probes),
            'historical_normal_negative_rejections':len(probes),
            'historical_optimized_false_acceptances':len(probes),
            'all_27_frozen_bindings_preserved':True,
            'publication_entrypoints_repaired':False,
            'actual_L_function_asymptotic_proved':False}
    (OWN/'CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':report['status'],'fresh_checks_per_mode':positive_report['checks'],
                      'fresh_negative_rejections_per_mode':len(mutants),
                      'historical_optimized_false_acceptances':len(probes)},sort_keys=True))


if __name__=='__main__':
    main()
