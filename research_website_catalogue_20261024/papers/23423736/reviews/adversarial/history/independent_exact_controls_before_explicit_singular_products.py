"""Independent finite falsifiers for the sealed universal derivations; stdlib only.
No source imports, source writes, sampling-as-proof or native campaign replay.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json,sys

def need(ok,label):
 if not ok:raise ValueError(label)
# Symbolic Z[alpha,beta] coefficients and genuinely noncommutative free words.
def za(a,b):
 r=dict(a)
 for k,v in b.items():r[k]=r.get(k,0)+v
 return {k:v for k,v in r.items() if v}
def zm(a,b):
 r={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():r[(i+k,j+l)]=r.get((i+k,j+l),0)+v*w
 return {k:v for k,v in r.items() if v}
def zn(a):return {k:-v for k,v in a.items()}
ONE={(0,0):1};ALPHA={(1,0):1};BETA={(0,1):1}
def na(a,b):
 r={w:dict(c) for w,c in a.items()}
 for w,c in b.items():r[w]=za(r.get(w,{}),c)
 return {w:c for w,c in r.items() if c}
def nn(a):return {w:zn(c) for w,c in a.items()}
def nm(a,b):
 r={}
 for u,c in a.items():
  for v,d in b.items():r[u+v]=za(r.get(u+v,{}),zm(c,d))
 return {w:c for w,c in r.items() if c}
def ns(c,a):return {w:zm(c,d) for w,d in a.items() if zm(c,d)}
def letter(x):return {x:ONE}
def sub(a,mapping):
 r={}
 for word,c in a.items():
  out={'':c}
  for x in word:out=nm(out,mapping[x])
  r=na(r,out)
 return r
def symbolic():
 a,b,c,d=[letter(x) for x in '1234'];minus=lambda x,y:na(x,nn(y))
 fs=[na(nm(a,minus(ns(ALPHA,a),c)),nm(c,minus(a,ns(ALPHA,c)))),na(nm(a,minus(ns(ALPHA,b),d)),nm(c,minus(b,ns(ALPHA,d)))),na(nm(b,minus(ns(ALPHA,a),c)),nm(d,minus(a,ns(ALPHA,c)))),na(nm(b,minus(ns(ALPHA,b),d)),nm(d,minus(b,ns(ALPHA,d)))),na(nm(a,minus(ns(BETA,a),b)),nm(d,minus(a,ns(BETA,b)))),na(nm(a,minus(ns(BETA,c),d)),nm(d,minus(c,ns(BETA,d))))]
 X,Y=letter('X'),letter('Y');Q=na(na(ns(BETA,nm(X,X)),nn(nm(X,Y))),na(nm(Y,X),nn(ns(BETA,nm(Y,Y)))))
 images=[sub(f,{'1':X,'2':Y,'3':X,'4':Y}) for f in fs];need(images==[{},{},{},{},Q,Q],'all_six_exact_symbolic_eliminations')
 U,V=letter('U'),letter('V');transformed=sub(Q,{'X':na(U,V),'Y':V});want=na(ns(BETA,nm(U,U)),na(ns(za(BETA,zn(ONE)),nm(U,V)),ns(za(BETA,ONE),nm(V,U))));need(transformed==want,'exact_UV_relation_over_Z_alpha_beta')
 wrong=na(nm(a,minus(ns(BETA,a),b)),nm(c,minus(a,ns(BETA,b))));need(sub(wrong,{'1':X,'2':Y,'3':X,'4':Y})!=Q,'mutated_last_left_factor_detected')
 return {'symbolic_base':'Z[alpha,beta], free words retained','six_images':['0','0','0','0','Q','Q'],'transformed_relation':'beta UU+(beta-1)UV+(beta+1)VU','altered_left_factor_fault_rejected':True}
class Field:
 def __init__(self,p):self.p=p;self.name='Q' if p==0 else 'F4' if p==4 else 'F'+str(p);self.zero=self.cast(0);self.one=self.cast(1)
 def cast(self,n):return Fraction(n) if self.p==0 else n%2 if self.p==4 else n%self.p
 def add(self,a,b):return a+b if self.p==0 else a^b if self.p==4 else (a+b)%self.p
 def neg(self,a):return -a if self.p==0 else a if self.p==4 else (-a)%self.p
 def mul(self,a,b):
  if self.p==0:return a*b
  if self.p!=4:return a*b%self.p
  r=0
  while b:
   if b&1:r^=a
   b>>=1;a<<=1
   if a&4:a^=7
  return r
 def power(self,a,n):
  out=self.one
  while n:
   if n&1:out=self.mul(out,a)
   a=self.mul(a,a);n//=2
  return out
 def inv(self,a):need(a!=self.zero,'nonzero_field_inverse');return 1/a if self.p==0 else self.power(a,2 if self.p==4 else self.p-2)
def operations(F):
 def add(a,b):
  r=dict(a)
  for k,v in b.items():r[k]=F.add(r.get(k,F.zero),v)
  return {k:v for k,v in r.items() if v!=F.zero}
 def scale(c,a):return {k:F.mul(c,v) for k,v in a.items() if F.mul(c,v)!=F.zero}
 def mul(a,b):
  r={}
  for (i,j),v in a.items():
   for (k,l),w in b.items():r[(i+k,j+l)]=F.add(r.get((i+k,j+l),F.zero),F.mul(v,w))
  return {k:v for k,v in r.items() if v!=F.zero}
 def power(a,n):
  r={(0,0):F.one}
  for _ in range(n):r=mul(r,a)
  return r
 return add,scale,mul,power
def rank(columns,F):
 if not columns:return 0
 a=[list(row) for row in zip(*columns)];r=0
 for col in range(len(a[0])):
  pivot=next((i for i in range(r,len(a)) if a[i][col]!=F.zero),None)
  if pivot is None:continue
  a[r],a[pivot]=a[pivot],a[r];iv=F.inv(a[r][col]);a[r]=[F.mul(iv,v) for v in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][col]!=F.zero:
    c=a[i][col];a[i]=[F.add(x,F.neg(F.mul(c,y))) for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
def check_case(F,beta):
 add,scale,mul,power=operations(F);s={(1,0):F.one};t={(0,1):F.one};det=F.add(F.one,F.neg(F.mul(beta,beta)));need(det!=F.zero,'case_is_admissible')
 plus=F.add(F.one,beta);a=F.mul(F.add(F.one,F.neg(beta)),F.inv(plus));b=F.mul(F.neg(beta),F.inv(plus))
 @lru_cache(None)
 def linear(m):
  S,T=s,t
  for _ in range(m):S,T=add(S,scale(beta,T)),add(scale(beta,S),T)
  return S,T
 def theta(f,m):
  S,T=linear(m);r={}
  for (i,j),c in f.items():r=add(r,scale(c,mul(power(S,i),power(T,j))))
  return r
 def twist(word,mapping):
  f={(0,0):F.one}
  for n,x in enumerate(word):f=mul(f,theta(mapping[x],n))
  return f
 mapping={'X':s,'Y':t};q=add(add(scale(beta,twist('XX',mapping)),scale(F.neg(F.one),twist('XY',mapping))),add(twist('YX',mapping),scale(F.neg(beta),twist('YY',mapping))));need(not q,'quadratic_identity_actual_positive_pullback')
 U=add(s,scale(F.neg(F.one),t));normalmap={'U':U,'V':t}
 @lru_cache(None)
 def nf(word,right=False):
  positions=[i for i in range(len(word)-1) if word[i:i+2]=='VU']
  if not positions:return {word:F.one}
  i=positions[-1] if right else positions[0];r={}
  for coefficient,replacement in [(a,'UV'),(b,'UU')]:
   child=word[:i]+replacement+word[i+2:]
   need(child<word,'strict_fixed_length_lex_descent')
   for key,val in nf(child,right).items():r[key]=F.add(r.get(key,F.zero),F.mul(coefficient,val))
  return {k:v for k,v in r.items() if v!=F.zero}
 def operator_word(word):
  r={(0,0):F.one}
  for x in word[::-1]:
   out={}
   for (i,j),c in r.items():
    if x=='U':term={(i+1,j):c}
    else:
     qsum=F.zero
     for n in range(i):qsum=F.add(qsum,F.power(a,n))
     term={};dc=F.mul(c,F.mul(b,qsum));sc=F.mul(c,F.power(a,i))
     if dc!=F.zero:term[(i+1,j)]=dc
     if sc!=F.zero:term[(i,j+1)]=sc
    out=add(out,term)
   r=out
  return r
 words=0
 for n in range(7):
  for letters in product('UV',repeat=n):
   word=''.join(letters);left=nf(word);need(left==nf(word,True),'independent_reduction_orders');as_operator={(w.count('U'),w.count('V')):c for w,c in left.items()};need(as_operator==operator_word(word),'operator_faithfulness_on_actual_all_short_words');expected={}
   for w,c in left.items():expected=add(expected,scale(c,twist(w,normalmap)))
   need(expected==twist(word,normalmap),'normal_form_matches_actual_section_product');words+=1
 ranks=[]
 for n in range(9):
  columns=[]
  for i in range(n+1):
   image=twist('U'*i+'V'*(n-i),normalmap);columns.append([image.get((j,n-j),F.zero) for j in range(n+1)])
  got=rank(columns,F);need(got==n+1,'section_images_of_normal_basis_full_rank');ranks.append(got)
 # Associativity for inhomogeneous triples, where degree-specific pullback
 # must be used separately for every homogeneous summand.
 def star(f,g):
  r={}
  for (i,j),c in f.items():r=add(r,mul({(i,j):c},theta(g,i+j)))
  return r
 f=add(s,{(0,0):F.one});g=add(t,mul(s,s));h=add(mul(s,t),{(0,0):F.one});need(star(star(f,g),h)==star(f,star(g,h)),'inhomogeneous_associativity');need(star(f,g),'selected_inhomogeneous_product_nonzero')
 return {'field':F.name,'beta':str(beta),'words_through_degree6':words,'normal_section_basis_ranks_degrees0_to8':ranks,'inhomogeneous_associativity':True,'operator_vs_twist_and_two_reduction_orders':True}
def negative_controls():
 F=Field(0);add,scale,mul,power=operations(F);s={(1,0):F.one};t={(0,1):F.one};beta=Fraction(2);iv=F.inv(1-beta*beta);Ss=scale(iv,add(s,scale(-beta,t)));Tt=scale(iv,add(scale(-beta,s),t));wrongQ=add(add(scale(beta,mul(s,Ss)),scale(-1,mul(s,Tt))),add(mul(t,Ss),scale(-beta,mul(t,Tt))));need(wrongQ,'inverse_pullback_without_relabeling_fails_same_Q');rows=[{'fault':'inverse_pullback_used_with_unchanged_sigma_and_beta','actual_nonzero_residual':str(wrongQ)}]
 for p in [0,2,3,5,4]:
  F=Field(p)
  for beta in {F.one,F.neg(F.one)}:
   need(F.add(F.one,F.neg(F.mul(beta,beta)))==F.zero,'excluded_matrix_singular');rows.append({'field':F.name,'beta':str(beta),'excluded_matrix_singular':True,'linear_zero_divisors_from_exact_factorization':True,'characteristic_two_factors_coincide':p in {2,4}})
 return rows
def main():
 sym=symbolic();rows=[]
 for p in [0,2,3,4,5,7,11]:
  F=Field(p);values=[Fraction(0),Fraction(2),Fraction(-2),Fraction(1,2)] if p==0 else [0,2,3] if p==4 else [x for x in range(p) if F.mul(x,x)!=F.one]
  for beta in values:rows.append(check_case(F,beta))
 return {'literal_custom_status':'INDEPENDENT_EXACT_ALGEBRAIC_DIAGNOSTICS_AGREE_WITH_SEALED_UNIVERSAL_DERIVATIONS','optimization':sys.flags.optimize,'symbolic':sym,'cases':rows,'negative_convention_and_boundary_controls':negative_controls(),'finite_cases_prove_universal_claim':False,'universal_proof':'INITIAL_RECONSTRUCTION.md families1-8; full operator identity is proved there for arbitrary coefficients/degree','source_imports_or_source_program_execution':False,'file_writes_or_network':False}
if __name__=='__main__':print(json.dumps(main(),indent=2))
