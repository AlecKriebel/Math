"""Finite quantifier-scope controls; toy sets are not arithmetic models."""
import itertools as it,json
N=0
def check(x):
 global N
 N+=1
 assert x

def main():
 negations=0;hierarchies=0;goodsets=0
 for H in range(1,7):
  U=tuple(range(H+2));inf=H+1
  sets=[tuple(u for u in U if bits>>u&1) for bits in range(1,1<<len(U))]
  # Each finite height k survives horizon k but not k+1.
  for k in range(H+1):check(k>=k and not k>=k+1);hierarchies+=1
  for S in sets:
   if inf in S:
    for m in range(H+2):check(any(u>=m for u in S));goodsets+=1
  for S,T in it.product(sets,repeat=2):
   for m in range(H+2):
    A=all(any(u>=m for u in R) for R in (S,T))
    bad_interval=any(all(not u>=m for u in R) for R in (S,T))
    check((not A)==bad_interval);negations+=1
 print(json.dumps({'problem_id':30005751,'turn':5,'status':'PASS','exact_assertions':N,'closed_sentence_negation_controls':negations,'strict_parameter_height_examples':hierarchies,'good_response_interval_controls':goodsets,'scope':'Finite toy quantifier controls only. No IOpen model, finite axiomatization, or non-finite axiomatizability certificate is claimed.'},indent=2))
if __name__=='__main__':main()
