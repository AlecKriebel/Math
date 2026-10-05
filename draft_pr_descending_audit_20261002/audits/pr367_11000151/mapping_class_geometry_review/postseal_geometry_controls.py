"""Additional bounded false-positive and boundary-word controls."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
J=[[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]]
V=[[1,0,0,0],[0,1,0,0],[1,0,-1,0],[0,0,0,1],[0,0,1,0]]
G=[]
for v in V:
 cov=[sum(v[k]*J[k][j] for k in range(4)) for j in range(4)]
 G.append([[int(i==j)+v[i]*cov[j] for j in range(4)] for i in range(4)])
def matrix(w):
 r=eye(4)
 for i in w:r=mm(r,G[i-1])
 return r
def perm(w):
 r=list(range(6))
 for i in w:r[i-1],r[i]=r[i],r[i-1]
 return r
target=(1,2,3,4)*10
false=(1,)*40
checks={'equal_lengths40':len(target)==len(false)==40,
 'same_abelianization_class_Q':len(target)%10==len(false)%10,
 'same_S6_image':perm(target)==perm(false),
 'same_Sp4_F2_image':[[x%2 for x in r] for r in matrix(target)]==[[x%2 for x in r] for r in matrix(false)],
 'unequal_integral_homology_so_unequal_Q':matrix(target)!=matrix(false)}
def red(w):
 s=[]
 for a in w:
  if s and s[-1]==-a:s.pop()
  else:s.append(a)
 return tuple(s)
def inverse(w):return tuple(-a for a in w[::-1])
def subst(w,A):
 r=()
 for x in w:r=red(r+(A[x-1] if x>0 else inverse(A[-x-1])))
 return r
A=[((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),
   ((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),
   ((1,),(2,),(3,),(3,-2,1,4))]
b=(1,-2,3,-4,-1,2,-3,4)
for i,a in enumerate(A,1):checks[f'F4_generator_{i}_preserves_boundary_word']=subst(b,a)==b
I=((1,),(2,),(3,),(4,))
def action(w):
 r=I
 for i in w:r=tuple(subst(x,A[i-1]) for x in r)
 return r
checks['F4_boundary_twist_target_is_conjugation_by_boundary_word']=action(target)==tuple(red(b+(i,)+inverse(b)) for i in range(1,5))
report={'all_checks_pass':all(checks.values()),'checks':checks,
        'false_word':'a1^40','target':'(a1a2a3a4)^10','false_word_integral_homology':matrix(false),
        'boundary_word':b,
        'meaning':'Even within length40, abelianization and S6 x Sp4(F2) acceptance do not suffice for Q equality. Candidate does not use that invalid criterion.'}
(P/'postseal_geometry_controls.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert all(checks.values())
