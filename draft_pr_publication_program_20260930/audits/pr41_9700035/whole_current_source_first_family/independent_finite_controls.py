#!/usr/bin/env python3
"""Independent exact finite falsification controls, authored before current exposure.
These examples are not SIRSN constructions and cannot prove the target law.
"""
from fractions import Fraction
import json

def interval_union_length(intervals):
 ordered=sorted((Fraction(a),Fraction(b)) for a,b in intervals)
 if any(b<a for a,b in ordered):raise ValueError('Reversed interval')
 total=Fraction(0);start=end=None
 for a,b in ordered:
  if start is None:start,end=a,b
  elif a>end:total+=end-start;start,end=a,b
  else:end=max(end,b)
 return total+(end-start if start is not None else Fraction(0))

def main():
 assert interval_union_length([])==0
 assert interval_union_length([(0,2),(1,3),(0,2)])==3
 assert interval_union_length([(0,1),(1,2)])==2
 assert interval_union_length([(1,1)])==0
 # The three designated edge routes of an abstract equilateral triangle each
 # meet another in just one endpoint: route compatibility is vacuous here.
 # Network edge-lengths all one; route union length3, minimal connector length2.
 triangle={'pair_routes':{'AB':['AB'],'AC':['AC'],'BC':['BC']},'edge_lengths':{'AB':1,'AC':1,'BC':1}}
 union=set(e for route in triangle['pair_routes'].values() for e in route)
 all_pair_length=sum(triangle['edge_lengths'][e] for e in union)
 selected_tree_length=sum(triangle['edge_lengths'][e] for e in ('AB','BC'))
 assert all_pair_length==3 and selected_tree_length==2
 for k,edges in triangle['pair_routes'].items():
  for m,other in triangle['pair_routes'].items():
   if k!=m:assert len(set(k)&set(m))==1
 # Rare exterior mass vanishes in probability after normalization, while
 # normalized mean stays1. This refutes unqualified UI inference from that.
 rare=[]
 for n in (2,4,16,256,65536):
  mass=n*n;p=Fraction(1,n);normal_mean=p*Fraction(mass,n)
  assert normal_mean==1 and p>0
  rare.append({'n':n,'probability':str(p),'mass_when_present':mass,'mean_divided_by_n':str(normal_mean)})
 # Dist_infinity outer-square layer areas must retain perimeter growth.
 layer=[]
 for L,a,b in ((1,0,1),(7,2,5),(32,1,2)):
  area=(L+2*b)**2-(L+2*a)**2
  primitive=lambda r:4*L*r+4*r*r
  correct=primitive(b)-primitive(a)
  wrong=4*L*(b-a)
  assert area==correct and area>wrong
  layer.append({'L':L,'a':a,'b':b,'area':area,'constant_perimeter_incorrect':wrong})
 print(json.dumps({'classification':'Exact finite controls only; no infinite-SIRSN certificate','route_union_distinct_from_minimal_connector':{'all_pair_length':all_pair_length,'selected_tree_length':selected_tree_length},'overlap_counted_once':True,'boundary_point_length_zero':True,'rare_exterior_mass_no_UI_inference':rare,'outer_square_perimeter_growth':layer},indent=2))

if __name__=='__main__':main()
