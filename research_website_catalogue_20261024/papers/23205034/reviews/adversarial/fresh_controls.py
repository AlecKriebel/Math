"""Independent adversarial controls of sparse reduction; no upstream PF claim.
Exact Hasse-coefficient valuation reference and binary-large characteristic
cases use separate verification mechanisms from the exponent-digit trie.
"""
from pathlib import Path
import sys,json,hashlib,datetime
from collections import Counter
from math import comb
sys.dont_write_bytecode=True
source=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23205034/sources/published-source/code')
sys.path.insert(0,str(source))
import finite_fields as ff
import sparse_cartier as sc
counts=Counter(); examples=[]
def ck(value,key):
 if not value: raise RuntimeError(key)
 counts[key]+=1
# Independent Hasse coefficient sum, not recursive descent or repeated division.
for p in (2,3,5,7,11):
 K=ff.FiniteField(p,(0,1))
 for n in range(1,25):
  for pattern in range(4):
   coeff=[(j*j+pattern*j+pattern+1)%p for j in range(n)]+[1]
   U={j:K.element(c) for j,c in enumerate(coeff) if c}
   for alpha in range(1,p):
    expected=next(k for k in range(n+1) if sum(coeff[j]*comb(j,k)*pow(alpha,j-k,p) for j in range(k,n+1))%p)
    audit=[]; actual=sc.quotient_multiplicity(K,U,K.poly((-alpha,1)),audit)
    ck(actual==expected,'Hasse_known_root_valuation')
    ck(actual%p<=len(U)-1,'residue_sparsity_bound')
    ck(audit[0]['nodes']<=len(U)*(n.bit_length()+1),'trie_node_dimension')
    # Independent logarithmic derivative denominator from dense gcd, low degree only.
   if 0 in U:
    pade=[]; G=sc.logarithmic_denominator(K,U,pade)
    dense=K.poly(coeff); want=ff.monic(K,ff.exact_div(K,dense,ff.gcd(K,dense,ff.derivative(K,dense))))
    ck(G==want,'visible_denominator_dense_control')
    ck(pade[-1]['B']<=2*max(1,len(G)-1),'adaptive_pade_stop_bound')
# A strict oracle guard refuses every nonlinear or field enumeration request.
queries=[]
def linear_only(p,f):
 queries.append({'characteristic_bits':p.bit_length(),'degree':len(f)-1})
 if len(f)!=2: raise RuntimeError('linear-only oracle received unsupported polynomial')
 return [(-f[0]*pow(f[1],-1,p))%p]
for bits,k,r in ((61,7,3),(127,4,5),(521,3,2)):
 p=2**bits-1; K=ff.FiniteField(p,(0,1)); high=p**k
 # (X-1)^(p^k+r) written by multiplying a binomial and degree-r factor.
 small={j:(comb(r,j)*(-1)**(r-j))%p for j in range(r+1)}
 U={}
 for j,c in small.items(): U[j]=(-c)%p;U[high+j]=c
 terms=[(n,c) for n,c in U.items() if c]
 got,audit=sc.factor_sparse(K,terms,prime_oracle=linear_only)
 ck(got.factors==((K.poly((-1,1)),high+r),),'binary_large_characteristic_complete_factorization')
 ck(len(audit['levels'])<=max(U).bit_length(),'binary_large_level_bound')
 ck(all(v['residue_product_degree']<=r for v in audit['levels']),'binary_large_residue_product_degree')
 examples.append({'p_bits':bits,'input_terms':len(terms),'exponent_bits':(high+r).bit_length(),'dense_output_degree':1,'levels':len(audit['levels']),'prime_oracle_max_degree':max((q['degree'] for q in queries),default=0)})
# Product of distinct extension-field factors, huge repeated Frobenius powers,
# nontrivial unit, and a shifted X factor; compare with supplied algebraic product.
for p,h,k in ((2,(1,1,0,1),83),(3,(1,0,1),47)):
 K=ff.FiniteField(p,h);a=K.basis()[1];b=K.add(a,K.one); scalar=K.add(a,K.element(2))
 if scalar==K.zero:scalar=a
 high=p**k; U={0:K.one}
 expected={}
 for root,e in ((a,high+1),(b,2*high+p+1)):
  # Binary exponent made from a small low exponent and a small high coefficient.
  hi=e//high;low=e%high; g=(K.neg(root),K.one)
  lowpoly=sc.dense_power(K,g,low); highpoly=sc.dense_power(K,g,hi)
  compressed={j*high:K.pow(c,high) for j,c in enumerate(highpoly) if c!=K.zero}
  factor=sc.sparse_dense_product(K,compressed,lowpoly)
  product={}
  for i,x in U.items():
   for j,y in factor.items():product[i+j]=K.add(product.get(i+j,K.zero),K.mul(x,y))
  U={i:c for i,c in product.items() if c!=K.zero};expected[g]=e
 shift=19; terms=[(n+shift,K.mul(c,scalar)) for n,c in U.items()];expected[K.poly((0,1))]=shift
 result,audit=sc.factor_sparse(K,terms)
 ck(dict(result.factors)==expected and result.unit==scalar,'extension_two_factor_binary_multiplicities')
 D=sum(len(g)-1 for g in expected);t=len(terms);bits=max(n for n,c in terms).bit_length()
 for level,item in enumerate(audit['levels']):
  ck(item['denominator_degree']<=level*D,'denominator_growth_invariant')
  ck(item['visible_degree']<=(level+1)*D,'visible_degree_invariant')
  ck(item['residue_product_degree']<=(t-1)*(level+1)*D,'binary_safe_residue_product')
 ck(len(audit['levels'])<=bits,'binary_level_bound')
 examples.append({'p':p,'extension_degree':len(h)-1,'exponent_bits':bits,'input_terms':t,'dense_output_degree':D,'levels':len(audit['levels'])})
# Negative controls: finite Taylor prefix cannot certify a logarithmic derivative;
# alpha exponents must not be reduced modulo multiplicative order.
K=ff.FiniteField(3,(0,1));U={0:K.one,81:K.one,82:K.one};audit=[]
G=sc.logarithmic_denominator(K,U,audit)
ck(audit[0]['accepted'] is False and len(G)>1,'false_zero_prefix_rejected')
U={0:K.element(-1),3**20:K.one};g=K.poly((-1,1))
ck(sc.quotient_multiplicity(K,U,g)==3**20,'exponent_reduction_would_destroy_valuation')
# p-th root coefficients must be twisted in extension fields.
K=ff.FiniteField(2,(1,1,1));a=K.basis()[1]
root=ff.polynomial_pth_root(K,(a,K.zero,K.one))
ck(root[0]!=a and ff.mul(K,root,root)==(a,K.zero,K.one),'inverse_coefficient_frobenius_essential')
print(json.dumps({'status':'PASS','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':sum(counts.values()),'families':dict(counts),'large_examples':examples,'linear_only_oracle_queries':queries,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite reduction controls; no implementation or verification of upstream polynomial-time factorization theorem.'},indent=2))
