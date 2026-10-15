#!/usr/bin/env python3
"""Independent affine coefficient certification in Z, with residue-group model."""
import itertools,json
N=0
def check(ok,label):
 global N
 if not ok: raise RuntimeError(label)
 N+=1
def sg(c): return (-1)**(c//2)
def plus(a,b):return(tuple(x+y for x,y in zip(a[0],b[0])),(a[1]+b[1])%4)
def minus(a,b):return plus(a,(tuple(-x for x in b[0]),-b[1]%4))
def circle(a,b):return(tuple(x+sg(a[1])*y for x,y in zip(a[0],b[0])),a[1]^b[1])
def lam(a,b):return minus(circle(a,b),a)
def star(a,b):return minus(lam(a,b),b)
V=[(1,0,0),(0,1,0),(0,0,1)];z=((0,0,0),0)
for c,d,e in itertools.product(range(4),repeat=3):
 a,b,t=(V[0],c),(V[1],d),(V[2],e)
 check((c+d+2*c*d)%4==c^d,'xor/ring agreement')
 check(circle(circle(a,b),t)==circle(a,circle(b,t)),'universal associativity')
 check(circle(a,plus(b,t))==plus(minus(circle(a,b),a),circle(a,t)),'universal left law')
 check(lam(a,b)==(tuple(sg(c)*x for x in b[0]),((-1)**c*d)%4),'universal lambda')
 check(star(a,b)==(tuple((sg(c)-1)*x for x in b[0]),2*c*d%4),'universal star')
 check(lam(circle(a,b),t)==lam(a,lam(b,t)),'universal action')
rows=[]
for c,nonzero_n in itertools.product(range(4),(False,True)):
 n=int(nonzero_n)
 H=[d for d in range(4) if 2*c*d%4==0]
 K=[d for d in H if (sg(d)-1)*n==0]
 for L in (H,K):
  check(0 in L and all((d^e) in L for d,e in itertools.product(L,repeat=2)),'residue subgroup')
 hi=4//len(H) if sg(c)==1 else 'infinite';ki=4//len(K) if sg(c)==1 else 'infinite'
 rows.append({'c':c,'n_nonzero':nonzero_n,'H_residues':H,'K_residues':K,'m_constraint':'arbitrary' if sg(c)==1 else 'zero','H_index':hi,'K_index':ki})
# All 4 characters are legitimate. Only high bit and bit sum have nonadditive kernels.
char_controls=[]
for h,l in itertools.product(range(2),repeat=2):
 f=lambda c:(-1)**(h*(c//2)+l*(c%2))
 check(all(f(c^d)==f(c)*f(d) for c,d in itertools.product(range(4),repeat=2)),'character control')
 ker=[c for c in range(4) if f(c)==1]
 additive=all((c+d)%4 in ker for c,d in itertools.product(ker,repeat=2))
 char_controls.append({'high_weight':h,'low_weight':l,'s_residues':ker,'additive_subgroup':additive})
check(char_controls[0]['s_residues']==[0,1,2,3],'trivial-action positive control')
check(char_controls[1]['s_residues']==[0,2] and char_controls[1]['additive_subgroup'],'parity-action positive control')
check(char_controls[2]['s_residues']==[0,1] and not char_controls[2]['additive_subgroup'],'high-bit negative closure')
# Removing the bilinear term loses the character identity, so cannot use this eps.
check(any(sg((c+d)%4)!=sg(c)*sg(d) for c,d in itertools.product(range(4),repeat=2)),'reject deleted diamond term')
# Overflow/finite-bound stress controls in actual Z.
for n,m in itertools.product((0,1,-1,10**100,-10**100),repeat=2):
 a=((n,0,0),2); b=((m,0,0),0)
 check(star(a,b)==((-2*m,0,0),0),'arbitrary-precision coefficient')
 check((-2*m==0)==(m==0),'torsion-free coset coefficient')
print(json.dumps({'status':'PASS_INDEPENDENT_UNIVERSAL_AFFINE_CERTIFICATE','checks':N,'all_integer_coefficient_certificate':True,'residue_case_table':rows,'meaningful_alternative_character_controls':char_controls,'infinite_index_proof':'For c=2,3 H,K require m=0. Representatives (j,0), j in Z: additive differences and circle quotients equal (j-i,0), hence same coset iff i=j. No finite bound is used.'},indent=2))
