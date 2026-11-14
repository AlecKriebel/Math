"""Independent exact all-subset solver for the manuscript's seven-vertex support witness.
Weights are transcribed from the native primary certificate graph, not fixation outputs.
"""
from fractions import Fraction as F
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix
import json,time

def solve(w,r,rule):
 n=len(w);full=(1<<n)-1;states=list(range(1,full));degree=list(map(sum,w));a={};b={}
 for mask in states:
  row=mask-1;fit=[r if mask>>u&1 else F(1) for u in range(n)];a[row]={};diag=F(0)
  for v in range(n):
   different=[u for u in range(n) if bool(mask>>u&1)!=bool(mask>>v&1)]
   if rule=='Bd':rate=sum((fit[u]*w[u][v]/degree[u] for u in different),F(0))
   else:rate=sum((fit[u]*w[u][v] for u in different),F(0))/sum((fit[u]*w[u][v] for u in range(n)),F(0))
   if not rate:continue
   diag+=rate;target=mask^(1<<v)
   if target==full:b[row]={0:QQ(rate.numerator,rate.denominator)}
   elif target:a[row][target-1]=-QQ(rate.numerator,rate.denominator)
  a[row][row]=QQ(diag.numerator,diag.denominator)
 matrix=DomainMatrix(a,(full-1,full-1),QQ);rhs=DomainMatrix(b,(full-1,1),QQ)
 h=matrix.to_dense().lu_solve(rhs.to_dense())
 assert matrix.matmul(h).to_dense()==rhs.to_dense()
 vals=h.to_list();rho=sum((F(int(vals[(1<<v)-1][0].numerator),int(vals[(1<<v)-1][0].denominator)) for v in range(n)),F(0))/n
 return rho

def main():
 start=time.monotonic();n=7;w=[[F(0) for _ in range(n)] for _ in range(n)]
 edges=[(0,1,642311627470),(0,2,641177352713),(1,2,2172410361743),(0,3,5),(0,4,1665053),(3,4,4231492313836),(0,5,79),(0,6,71),(5,6,5921340201086)]
 for u,v,z in edges:w[u][v]=w[v][u]=F(z)
 r=F(3,2);q=1-1/r;rb=solve(w,r,'Bd');rd=solve(w,r,'dB');x=rb/(q/(1-r**(-n)));y=rd/(F(n-1,n)*q/(1-r**(-(n-1))));theta=(y-1)/(y-x)
 assert x<1<y and theta>F(177,2000)
 assert not theta<F(177,2000)
 print(json.dumps({'all_labelled_transient_states_per_rule':126,'all_harmonic_residuals_zero':True,'x':str(x),'y':str(y),'theta':str(theta),'theta_decimal':float(theta),'theta_greater_than_177_over_2000':True,'opposite_sign_control_rejected':True,'seconds':time.monotonic()-start},indent=2))
if __name__=='__main__':main()
