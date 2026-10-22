"""Independent stable-rank labeling and multiplication/polarization controls."""
from math import comb
import json
def need(x,m):
 if not x:raise ValueError(m)
def compositions(r,n):
 if n==1:yield (r,);return
 for a in range(r+1):
  for b in compositions(r-a,n-1):yield (a,)+b
def main():
 rows=[]
 for p,n in [(3,2),(3,3),(3,5),(5,2),(5,3)]:
  r=2*p-1;mon=list(compositions(r,n));h=list(compositions(r-1,n));checked=0
  for a in mon:
   # delta sends x^a to sum_j a_j x^(a-e_j) tensor e_j;
   # multiplication sends each summand back to x^a.
   total=0
   for j,v in enumerate(a):
    if v:
     b=list(a);b[j]-=1;need(tuple(b) in h,'polarization basis');total+=v
   need(total%p==r%p and r%p!=0,'split section requires invertible r')
   checked+=1
  # Frobenius products with exactly one exponent >=p are disjoint.
  image={tuple(b[i]+(p if i==j else 0) for i in range(n)) for j in range(n) for b in compositions(p-1,n)}
  need(len(image)==n*comb(n+p-2,p-1),'Frobenius support injective')
  if n==2:need(len(image)==len(mon),'rank2 row is full Frobenius product')
  else:need(len(image)<len(mon),'higher rank row proper invariant submodule danger')
  rec={'p':p,'n':n,'r':r,'polarization_monomials_checked':checked,'Sym_r_dimension':len(mon),'Sym_rminus1_tensor_E_dimension':len(h)*n,'multiplication_kernel_dimension':len(h)*n-len(mon),'Frobenius_row_submodule_dimension':len(image),'stable_rank':n>=r}
  if n>=r:
   # Multilinear degree-r H has one vector for each distinguished variable j.
   basis=[(tuple(int(i<r and i!=j) for i in range(n)),j) for j in range(r)]
   need(len(set(basis))==r,'multilinear basis')
   need(all(tuple(b[i]+int(i==j) for i in range(n))==tuple(int(i<r) for i in range(n)) for b,j in basis),'all basis vectors have same product')
   rec['Schur_multilinear_H_dimension']=r;rec['Schur_kernel_dimension']=r-1
  rows.append(rec)
 print(json.dumps({'result':'PASS','cases':rows,'source_logic':'DD symmetric-power injective decomposition plus dominance permits only labels(r),(r-1,1); each multiplicity1. Split multiplication kernel is I_N(r-1,1); its stable multilinear weight is the augmentation module. No higher-rank simplicity of Sym^r is assumed.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
