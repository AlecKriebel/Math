#!/usr/bin/env python3
"""Independent deterministic verifier for Phase IV finite claims."""
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
MODULES=[
 'phase4_critical_lamperti.src.xi_certificate',
 'phase4_critical_lamperti.src.poisson_corrector',
 'phase4_critical_lamperti.src.kernel_expansion',
 'phase4_critical_lamperti.src.exact_absorption',
 'phase4_critical_lamperti.src.macrochain_builder',
 'phase4_critical_lamperti.src.lamperti_verifier',
 'phase4_critical_lamperti.src.rate_monomial_audit',
 'phase4_critical_lamperti.src.tier_assembler',
 'phase4_critical_lamperti.src.corrected_variance',
 'phase2_trigger_drain.src.phase2_verifier',
 'phase3_defect_credit.src.cone_lemma',
 'phase3_defect_credit.src.conservation_or_drain',
 'phase3_defect_credit.src.buffered_word',
 'phase3_defect_credit.src.fast_automaton',
 'phase3_defect_credit.src.fast_scc_analysis',
 'phase3_defect_credit.src.reward_cycle',
 'phase3_defect_credit.src.bellman_certificate',
 'phase3_defect_credit.src.foster_trace_chain',
]

def run()->dict:
 results={}
 for mod in MODULES:
  cp=subprocess.run([sys.executable,'-m',mod],cwd=ROOT,text=True,capture_output=True)
  results[mod]={'returncode':cp.returncode,'stdout':cp.stdout.strip(),'stderr':cp.stderr.strip()}
  if cp.returncode:raise RuntimeError(f'{mod} failed: {cp.stderr}')
 cp=subprocess.run([sys.executable,str(HERE/'critical_network_search.py')],cwd=ROOT,text=True,capture_output=True)
 if cp.returncode:raise RuntimeError(cp.stdout+cp.stderr)
 results['critical_network_search']=json.loads(cp.stdout)
 return results

def main()->None:print(json.dumps(run(),indent=2,sort_keys=True))
if __name__=='__main__':main()
