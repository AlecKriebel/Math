#!/usr/bin/env python3
"""Exact current replay of fixed authored certificates and accepted diagnostics."""
import json,math,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
CASES=['author_core','author_saved_adversarial','independent','source_mutants']
FALSE_CLAIMS=['omit_subset_bounds','floor_fractional_endpoint','treat_any_fractional_tree_as_target_counterexample','require_globally_largest_endpoint_integral','require_maximum_weight_tree_integral','exclude_zero_maximum','omit_rank_zero_mass_bound','collapse_parallel_coordinate_bounds','accept_negative_remaining_mass']
SOURCE_MUTANTS=['drop_subset_facets','round_down_rational_endpoint','drop_selected_coordinate_bounds','drop_nonnegative_mass_endpoint','replace_zero_by_positive_endpoint']
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
def main():
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required');need(len(sys.argv)==1,'no optional or skip arguments')
 contract=parse((HERE/'FINITE_CONTRACT.json').read_bytes())
 need(type(contract) is dict and set(contract)=={'schema','problem_id','modes','role'} and type(contract['schema']) is int and contract['schema']==1 and type(contract['problem_id']) is int and contract['problem_id']==30001934,'contract schema')
 need(type(contract['modes']) is dict and set(contract['modes'])=={'0','1','2'},'all optimization modes')
 expected=contract['modes'][str(sys.flags.optimize)];need(type(expected) is list and len(expected)==4 and [r['case'] for r in expected]==CASES,'exact nonempty suite identities')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];rows=[]
 for row in expected:
  need(type(row) is dict and set(row)=={'program','case','expected_exit','stdout','stderr'},'case schema');need(row['program']=='run_checker.py','exact program')
  need(type(row['expected_exit']) is int and row['expected_exit']==0,'successful suite exit required');need(type(row['stdout']) is str and row['stdout'] and type(row['stderr']) is str and row['stderr']=='','raw reference fields')
  case=row['case'];p=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(HERE/'run_checker.py'),case],cwd=HERE,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=600)
  need(type(p.returncode) is int and p.returncode==0,'successful suite exit '+case);need(p.stdout==row['stdout'].encode() and p.stderr==row['stderr'].encode(),'entire raw output differs '+case)
  x=parse(p.stdout);need(same(x,parse(row['stdout'])),'recursive exact output types')
  if case=='author_core':need(same(x,dict(passed=True,tested_points=2680,all_graph_theorem=False,assert_guard_dependency=False)),'author core exact counts')
  if case=='author_saved_adversarial':
   need(type(x) is list and len(x)==3,'saved points exact count');need([r['n'] for r in x]==[5,6,7] and [r['tree_count'] for r in x]==[125,1296,16807] and [r['integer_maxima'] for r in x]==[54,623,6909],'saved exact tree counts');need(all(r['exact_fraction_crosscheck'] is True for r in x),'all saved exact checks')
  if case in ('independent','source_mutants'):need(x['uid']==x['euid']==1000 and type(x['optimization']) is int and x['optimization']==sys.flags.optimize and x['passed'] is True,'checker process mode and identity')
  if case=='independent':
   need(x['mutants_rejected']==FALSE_CLAIMS and [r['control'] for r in x['rejection_details']]==FALSE_CLAIMS and len(x['rejection_details'])==9,'false claim identities');need(all(r['rejected'] is True and r['exception']=='RuntimeError' and type(r['reason']) is str and r['reason'] for r in x['rejection_details']),'intended false claim reasons')
   need([r['trees'] for r in x['examples']]==[16,125,16] and sum(r['trees'] for r in x['examples'])==157,'endpoint coverage');need(x['small_graph_structure']=={'connected_labeled_graphs':44,'nonpath_stars':4} and x['k5_structure']=={'triple_crossing_edge_choices':60,'inside_multiplicity':3,'crossing_multiplicity':6} and x['parallel_projection']=={'all_lifted_trees':24,'parallel_classes_split':1,'loops':1},'structural counts');need(x['all_graph_resolution'] is False and x['new_research_approaches']==0,'bounded scope')
  if case=='source_mutants':
   need([r['mutant'] for r in x['source_mutants_rejected']]==SOURCE_MUTANTS and len(x['source_mutants_rejected'])==5,'actual source mutant identities');need(all(r['rejected'] is True for r in x['source_mutants_rejected']),'all actual source mutants rejected');need(x['source_files_written'] is False and x['new_research_approaches']==0,'mutation scope')
   for r in x['source_mutants_rejected']:
    need(r['exception']==('ValueError' if r['mutant']=='drop_nonnegative_mass_endpoint' else 'RuntimeError') and r['diagnostic']==('min() iterable argument is empty' if r['mutant']=='drop_nonnegative_mass_endpoint' else 'author endpoint disagreement'),'exact actual mutant rejection reason')
  rows.append(dict(script=row['program'],case=case,category='source_mutation_suite' if case=='source_mutants' else 'positive_mathematical_suite',exit_code=p.returncode,expected_exit=0,reason='five actual in-memory source mutations rejected for their intended reasons' if case=='source_mutants' else 'positive fixed mathematical diagnostics accepted',stdout=p.stdout.decode(),stderr=p.stderr.decode(),complete_output_comparison=True,recursive_exact_type_comparison=True,normalization='NONE'))
 print(json.dumps(dict(status='passed',problem_id=30001934,uid=os.getuid(),euid=os.geteuid(),python_optimize=sys.flags.optimize,positive_checker_runs=3,source_mutation_suites=1,expected_mutant_rejections=14,rejection_categories={'false_claim_controls':9,'actual_source_mutants':5},cases=rows,mathematics='Fixed exact checks only; no new discovery search. The general target remains unresolved at 5/5; partial universal theorems rely on the full mathematical report and independent audit.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as error:
  print('REJECT: fixed-certificate replay failed: '+str(error),file=sys.stderr);sys.exit(1)
