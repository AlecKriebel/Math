"""Exact finite game controls, never advertised as models of IOpen."""
import itertools as it,json
from functools import lru_cache
N=0
def check(x):
 global N
 N+=1
 assert x

def bad(us):return any(a*b<c<2*a*b for a,b,c in it.product(us,repeat=3))
def legal(x):return range(x//2+1,x+1)
def response(x):return 1<<(x.bit_length()-1)

def wins(us,m,B):
 @lru_cache(None)
 def w(t,k):
  if bad(t):return False
  if k==0:return True
  return all(any(w(tuple(sorted(t+(u,))),k-1) for u in legal(x)) for x in range(1,B+1))
 return w(tuple(sorted(us)),m)

def main():
 check(list(legal(1))==[1]);check(list(legal(2))==[2]);check(bad((6,2)));check(not bad((3,2)));check(bad((3,2,1)))
 powers=[1,2,4,8,16,32,64];states=0
 for k in range(8):
  for us in it.combinations_with_replacement(powers,k):check(not bad(us));states+=1
 for x in range(1,10001):u=response(x);check(u<=x<2*u);check(u&(u-1)==0)
 comparisons=0
 for B in range(1,7):
  for n in range(4):
   A=wins((),n,B);Bp=wins((1,),n,B);Anext=wins((),n+1,B)
   check(not Anext or Bp);check(not Bp or A);comparisons+=1
 check(not wins((6,),1,2));check(not wins((3,),2,2))
 print(json.dumps({'problem_id':30005751,'turn':1,'status':'PASS','exact_assertions':N,'power_response_multisets_checked':states,'largest_power_responses_checked':10000,'bounded_game_sandwich_cases':comparisons,'scope':'Finite standard-integer game controls only. Compactness and the all-model sentence reductions are proved separately; no finite axiomatizability conclusion.'},indent=2))
if __name__=='__main__':main()
