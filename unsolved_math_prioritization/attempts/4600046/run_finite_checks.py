#!/usr/bin/env python3
"""Fresh isolated finite diagnostics, not a universal full-shift CA proof."""
import json,math,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
REASONS={'arbitrary_even_multiplier': 'power-of-two winding failed: m=6, k=(2, 0), order=3', 'drop_strict_exposedness': 'two co-highest permutive inputs do not give a slice permutation', 'ignore_cycle_parity': 'finite graph consistency mismatch: (0,), (1,)', 'ignore_loops': 'finite graph consistency mismatch: (0,), (1,)', 'ignore_zero_winding': 'accepted periodic routing target has no verified lift', 'nonstrict_bound': 'power-of-two winding failed: m=1, k=(1, 0), order=1', 'odd_multiplier': 'power-of-two winding failed: m=3, k=(1, 0), order=3', 'omit_target_phase': 'cycle period lost target phase', 'replace_specified_q': 'specified beta=1 target was replaced by zero background', 'thin_fibre_collar': 'crossing input is outside the proposed collar', 'uniform_inverse_radius': 'same finite input window does not determine inverse origin'}
def need(ok,message):
 if not ok:raise ValueError(message)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def unique(pairs):
 result={}
 for k,v in pairs:need(k not in result,'duplicate JSON key');result[k]=v
 return result
def nonfinite(token):raise ValueError('nonfinite JSON')
def number(token):
 x=float(token);need(math.isfinite(x),'nonfinite float');return x
def parse(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=nonfinite,parse_float=number)
def identities():
 return [('current/verify_partials.py',None),('current/verify_correction.py',None)]+[('current/verify_partials.py',m) for m in sorted(REASONS)]
def positive(index,mode):
 return {'collars': {'crossing_input_pairs_checked': 7928, 'note': 'Width 2r suffices. No optimality claim is made for Proposition 1.', 'thin_fibre_collar_counterexample': True}, 'exposed_vertex': {'absolute_phase_offsets_checked': True, 'constructed_periodic_lifts': 239, 'maximum_observed_T': 62, 'nonexposed_negative_control': True, 'singleton_permutations': 6, 'unimodular_lambda': [2, 3]}, 'finite_graphs': {'graphs': 700, 'includes': ['loops', 'reciprocal directed edges', 'merging incoming trees', 'terminals'], 'target_assignments': 10552}, 'input_integrity': {'excluded_original_input_replay': 'NOT_RUN', 'public_files_verified': 4}, 'marker_and_q': {'brute_force_unique_support_fibres': 729, 'nonuniformity_radii': [1, 2, 7, 40], 'nonzero_q_verified': True, 'two_dimensional_marker_words': 729}, 'mutant': None, 'routing': {'accepted': 425, 'interpretation': 'Conditional graph tests; no universal CA antecedent inferred.', 'lifted_targets': 6800, 'long_step_and_dimension_stress': [{'d': 2, 'm': 2, 'n': 1, 'step': [1, 0], 'vertices': 4}, {'d': 2, 'm': 4, 'n': 1, 'step': [2, 0], 'vertices': 16}, {'d': 2, 'm': 8, 'n': 1, 'step': [-4, 3], 'vertices': 64}, {'d': 3, 'm': 2, 'n': 1, 'step': [1, 0, -1], 'vertices': 8}, {'d': 3, 'm': 8, 'n': 2, 'step': [1, 0, 0], 'vertices': 4096}], 'odd_base_cycle_targets': 1632, 'patterns_including_zero_steps': 1296, 'rejected': 871, 'theorem_multiplier': 4}, 'scope': 'finite checks and public authored-input integrity; not unrestricted A/B/C', 'status': 'PASS', 'uid': 1000} if index==0 else {'contextual_patch_replay': 'EXACT_UNIQUE_CONTEXT_AFTER_EDITORIAL_EDITS_NO_WRITES', 'corrected_report_bytes': 21413, 'corrected_report_sha256': '18b5cdfa9efe0fe4b86e4cb927bc374b3dad9d7dbd502246f24579a2df9a9cce', 'empty_set_identity_targets': 274, 'empty_set_radius': 1, 'singleton_alphabet_cases': [{'T': 1, 'n': 1, 'offsets': [[0, 0], [1, 2]]}, {'T': 1, 'n': 1, 'offsets': [[3, -2]]}, {'T': 2, 'n': 2, 'offsets': [[0, 0], [1, 2]]}, {'T': 2, 'n': 2, 'offsets': [[3, -2]]}, {'T': 3, 'n': 3, 'offsets': [[0, 0], [1, 2]]}, {'T': 3, 'n': 3, 'offsets': [[3, -2]]}], 'status': 'PASS', 'superseded_full_report_replay': 'NOT_RUN'}
def wanted(index,mutation,mode):
 if mutation is None:return positive(index,mode)
 return dict(status='FAIL',error_type='AuditFailure',reason=REASONS[mutation],mutant=mutation,uid=1000)

def main():
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required');need(len(sys.argv)==1,'no optional or skip arguments')
 contract=parse((HERE/'FINITE_CONTRACT.json').read_bytes())
 need(type(contract) is dict and set(contract)=={'schema','problem_id','modes','role'} and type(contract['schema']) is int and contract['schema']==1 and type(contract['problem_id']) is int and contract['problem_id']==4600046,'contract schema')
 need(type(contract['modes']) is dict and set(contract['modes'])=={'0','1','2'},'all optimization modes')
 expected=contract['modes'][str(sys.flags.optimize)]
 need(type(expected) is list and len(expected)==13,'exact nonempty suite size');need([(r['program'],r['mutation']) for r in expected]==identities(),'exact identities and order')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];rows=[]
 for index,row in enumerate(expected):
  need(type(row) is dict and set(row)=={'program','mutation','expected_exit','stdout','stderr'},'case schema')
  script,mutation=row['program'],row['mutation'];code=1 if mutation else 0
  need(type(row['expected_exit']) is int and row['expected_exit']==code,'case exit schema');need(type(row['stdout']) is str and row['stdout'] and type(row['stderr']) is str and row['stderr']=='','raw reference fields')
  args=[script]+(['--mutant',mutation] if mutation else [])
  p=subprocess.run([sys.executable,'-I','-S','-B',*mode,*args],cwd=HERE,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=300)
  need(type(p.returncode) is int and p.returncode==code,'exact intended exit');need(p.stdout==row['stdout'].encode() and p.stderr==row['stderr'].encode(),'entire raw output differs '+script+' '+str(mutation))
  parsed=parse(p.stdout);need(same(parsed,parse(row['stdout'])),'recursive exact output types');need(same(parsed,wanted(index,mutation,sys.flags.optimize)),'exact identities counts and rejection reason')
  category='positive_checker' if mutation is None else 'mathematical_algorithm_hypothesis_mutant'
  reason='positive finite diagnostics accepted' if mutation is None else REASONS[mutation]
  rows.append(dict(script=script,mutation=mutation,category=category,exit_code=p.returncode,expected_exit=code,rejected=mutation is not None,reason=reason,stdout=p.stdout.decode(),stderr=p.stderr.decode(),complete_output_comparison=True,recursive_exact_type_comparison=True,normalization='NONE'))
 need(len(rows)==13 and sum(r['rejected'] is False for r in rows)==2 and sum(r['rejected'] is True for r in rows)==11,'exact totals')
 print(json.dumps(dict(status='passed',problem_id=4600046,uid=os.getuid(),euid=os.geteuid(),python_optimize=sys.flags.optimize,positive_checker_runs=2,expected_mutant_rejections=11,rejection_categories={'mathematical_algorithm_hypothesis_mutants':11},cases=rows,mathematics='Finite authored examples only. Eleven actual algorithm/hypothesis mutations per mode are separate from publication-integrity and schema controls. Infinite-graph existence, full-shift antecedents and universal conclusions rely on the written proofs. Repeated hostile and integrity replays add no mathematical coverage.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as error:
  print('REJECT: finite-interface replay failed: '+str(error),file=sys.stderr);sys.exit(1)
