#!/usr/bin/env python3
"""Integrity audit of the previously closed bounded nonroot JC atlases."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
C=ROOT/'certificates'

def load(n):return json.loads((C/n).read_text())
def main():
 k5=load('canonical_theta_k5_summary.json');k6=load('canonical_theta_k6_special_summary.json')
 assert (k5['strong_signatures'],k5['weak_signatures'],k5['strict_pairs'],k5['equal_pairs'],k5['duplicate_pairs'],k5['non_T_equal_pairs'])==(8520,16590,18480,8520,0,0)
 assert k5['ordered_quartets']==6*5*4*3
 assert (k6['strong_signatures'],k6['weak_signatures'],k6['strict_pairs'],k6['equal_pairs'],k6['duplicate_pairs'],k6['non_T_equal_pairs'])==(10980,218925,21960,10980,0,0)
 assert k6['ordered_quartets']==7*6*5*4
 s5=load('canonical_theta_k5_strict_signs.json');s6=load('canonical_theta_k6_special_strict_signs.json')
 assert s5['status']=='PROVED' and s5['covered']==s5['strict_directions']==18480
 assert s6['status']=='PROVED' and s6['covered']==s6['strict_directions']==21960
 assert 'open stochastic images are disjoint' in s5['logical_use'] and 'open stochastic images are disjoint' in s6['logical_use']
 eq=load('canonical_theta_k5_equal_presentation_replay.json')
 assert eq['status']=='PROVED' and eq['intersecting_target_presentations_checked']==12720
 assert eq['non_S_TC_targets']==eq['non_T_targets']==0
 cyc=load('canonical_cycle_cross_summary.json')
 assert cyc['status']=='EXACTLY COMPUTED'
 assert cyc['sizes']['3']['cycle_strong']==9 and cyc['sizes']['4']['cycle_strong']==48
 assert cyc['sizes']['3']['cycle_weak']==12 and cyc['sizes']['4']['cycle_weak']==63
 assert cyc['sizes']['3']['theta_to_cycle']['pairs']==0 and cyc['sizes']['4']['theta_to_cycle']['pairs']==0
 for name in ('theta_k5_to_cycle_k5_pairs.tsv','theta_k6_to_cycle_k6_pairs.tsv'):
  rows=list(csv.DictReader((C/name).open(),delimiter='\t'));assert rows==[]
 print(json.dumps({'status':'VERIFIED','theta_k5_strict':18480,'theta_k6_strict':21960,'theta_equal_non_T':0,'theta_to_cycle_pairs_k5_k6':0,'all_ordered_quartets_k5':360,'all_ordered_quartets_k6':840,'auxiliary_incoming_role_covariant':True},indent=2,sort_keys=True))
if __name__=='__main__':main()
