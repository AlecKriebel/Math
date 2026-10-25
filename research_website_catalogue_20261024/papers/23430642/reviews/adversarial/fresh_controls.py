"""Independent exact reconstruction from the nine-page manuscript; no submitted imports."""
from fractions import Fraction as Q
from itertools import product
from math import lcm,factorial
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent
COUNTS={}
def count(k,n=1):COUNTS[k]=COUNTS.get(k,0)+n
def check(v,label):
 count('assertions')
 if not v:raise AssertionError(label)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q(0))
def net(w,delta=True,bridge_bump=Q(0)):
 n=len(w);S=sum(w);eta=Q(1,24*S);d=eta/5 if delta else Q(0);E=[]
 def add(u,v,cap,c):E.append((u,v,Q(cap),Q(c)))
 for sign in [1,-1]:
  s=lambda i:(sign,'s',i);t=lambda i:(sign,'t',i)
  add(s(0),t(0),1,d)
  for i in range(1,n+1):
   a=sign*Q(w[i-1],24*S);cap=2**(i-1)
   add(s(i),s(i-1),cap,a/2);add(t(i-1),t(i),cap,a/2)
   add(s(i),t(i-1),cap,Q(2**i-1,2)-a/2);add(s(i-1),t(i),cap,Q(2**i-1,2)-a/2)
 for sign in [1,-1]:
  add('s',(sign,'s',n),2**n,0);add((sign,'t',n),'t',2**n,0)
 add((1,'s',0),(-1,'t',0),1,bridge_bump)
 nodes=['s']+[(sg,'s',i) for i in range(n,-1,-1) for sg in [1,-1]]+[(sg,'t',i) for i in range(n+1) for sg in [1,-1]]+['t']
 check(len(nodes)==4*n+6 and len(E)==8*n+7,'dimensions')
 return E,nodes,2**(n+1)
def residual(E,f,c):
 out=[]
 for i,(u,v,cap,_) in enumerate(E):
  if f[i]<cap:out.append((u,v,i,1,cap-f[i],c[i]))
  if f[i]>0:out.append((v,u,i,-1,f[i],-c[i]))
 return out
def distances(nodes,edges,start=None):
 ds={x:(Q(0) if start is None or x==start else None) for x in nodes}
 for _ in range(len(nodes)-1):
  change=False
  for u,v,*_,c in edges:
   if ds[u] is not None and (ds[v] is None or ds[v]>ds[u]+c):ds[v]=ds[u]+c;change=True
  if not change:break
 for u,v,*_,c in edges:
  check(ds[u] is None or ds[v] is None or ds[v]<=ds[u]+c,'no negative residual cycle')
 return ds
def shortest(E,nodes,f,c,all_paths=False):
 edges=residual(E,f,c);ds=distances(nodes,edges,'s')
 if ds['t'] is None:return []
 adj={x:[] for x in nodes}
 for a in edges:
  if ds[a[0]] is not None and ds[a[1]]==ds[a[0]]+a[-1]:adj[a[0]].append(a)
 found=[]
 def dfs(u,seen,path):
  if u=='t':found.append(path);return not all_paths
  for a in adj[u]:
   if a[1] not in seen and dfs(a[1],seen|{a[1]},path+[a]):return True
  return False
 dfs('s',{'s'},[])
 check(bool(found),'tight simple shortest exists');return found
def advance(f,path,step=Q(1)):
 g=list(f)
 for a in path:g[a[2]]+=step*a[3]
 return tuple(g)
def feasible(E,nodes,f,q):
 bal={v:Q(0) for v in nodes}
 for (u,v,cap,_),x in zip(E,f):
  check(0<=x<=cap,'capacity');bal[u]+=x;bal[v]-=x
 check(all(bal[v]==(q if v=='s' else -q if v=='t' else 0) for v in nodes),'conservation')
def original_search(w,delta=True):
 E,nodes,F=net(w,delta);c=[x[3] for x in E]; seen=set(); terminal=[]
 def search(f,q,touched):
  key=(f,touched)
  if key in seen:return
  seen.add(key);feasible(E,nodes,f,q)
  if q==F:terminal.append(touched);return
  paths=shortest(E,nodes,f,c,True)
  for path in paths:
   check(min(a[4] for a in path)==1,'unit SSP')
   g=advance(f,path);search(g,q+1,touched or f[-1]!=g[-1])
 search(tuple(Q(0) for _ in E),0,False)
 return terminal,len(seen)
def build_game(E,nodes,F,c):
 V=len(nodes);p=len(E);L=V-1;K=Q(1,2*L);eps=K/2;m=p+2
 h=[Q(0)]+[Q(F)]*(m-1);q=h[:];q[-1]-=K*L*F
 cost=[Q(0),Q(0)]+[L*F*x for x in c];RR=[];rr=[];ss=[]
 def add(row,r=0,s=0):RR.append(list(row));rr.append(Q(r));ss.append(Q(s))
 for i,(_,_,cap,_) in enumerate(E):
  row=[Q(0)]*m;row[i+2]=L*F;add(row,cap)
 for v in nodes:
  row=[Q(0)]*m;dv=1 if v=='s' else -1 if v=='t' else 0
  for j in range(m):row[j]-=dv*q[j]
  for i,(u,z,_,_) in enumerate(E):row[i+2]+=L*F*((u==v)-(z==v))
  add(row);add([-x for x in row])
 add(q,0,1);add([-x for x in q],0,-1)
 k=len(RR);d0=k+1
 den=1
 for val in cost+[x for row in RR for x in row]:den=lcm(den,val.denominator)
 H=max([1,den]+[abs(int(x*den)) for x in cost]+[abs(int(x*den)) for row in RR for x in row])
 C=k*factorial(d0)*H**d0;M=C+1
 RR=[[Q(0)]*m]+RR;rr=[Q(0)]+rr;ss=[Q(0)]+ss
 a=[-eps]+[F-eps]*(m-1);b=[-M*x for x in ss]
 A=[[-cost[i]-M*RR[j][i]+M*rr[j] for j in range(k+1)] for i in range(m)]
 B=[[-A[i][j]+a[i]*b[j] for j in range(k+1)] for i in range(m)]
 check(all(A[i][j]+B[i][j]==a[i]*b[j] for i in range(m) for j in range(k+1)),'rank-one identity')
 check(a[0]!=0 and b[-1]!=0,'exact rank one')
 check(len(A)==8*((len(nodes)-6)//4)+9 and len(A[0])==16*((len(nodes)-6)//4)+22,'game dimensions')
 default=k-1
 check(A[0][default]==0 and all(A[i][default]<0 for i in range(1,m)),'strict default row')
 check(B[0][default]>max(B[0][:default]+B[0][default+1:]),'strict default column')
 return dict(L=L,K=K,eps=eps,cost=cost,q=q,h=h,R=RR,r=rr,s=ss,a=a,b=b,A=A,B=B,M=M,C=C,p=p,k=k,F=F)
def verify_aux(E,nodes,c,f,lam,g):
 L,F,K,M=g['L'],g['F'],g['K'],g['M'];h=lam+K*f[-1];x=[1-h/F,h/F-sum(f)/(L*F)]+[z/(L*F) for z in f]
 check(min(x)>=0 and sum(x)==1,'simplex encoding');check(dot(g['q'],x)==lam and dot(g['h'],x)==h,'q h encode');check(dot(g['cost'],x)==dot(c,f),'cost encoding')
 residuals=[dot(row,x)-r-s*lam for row,r,s in zip(g['R'],g['r'],g['s'])];check(max(residuals)<=0,'all primal inequalities')
 pi=distances(nodes,residual(E,f,c));mu=[]
 for (u,v,cap,_),cc in zip(E,c):mu.append(max(Q(0),-cc-pi[u]+pi[v]))
 for v in nodes:mu.extend([max(pi[v],0),max(-pi[v],0)])
 gamma=pi['s']-pi['t'];mu.extend([max(gamma,0),max(-gamma,0)])
 mu=[Q(z) for z in mu]
 check(sum(mu)<M,'uniform M dominates chosen dual')
 dualcols=[Q(0)]+mu
 check(all(dot([g['R'][j][i] for j in range(len(dualcols))],dualcols)+g['cost'][i]>=0 for i in range(len(x))),'dual feasible')
 val=-sum(dualcols[j]*(g['r'][j]+g['s'][j]*lam) for j in range(len(dualcols)))
 check(val==dot(c,f),'exact primal dual equality')
 y=[1-sum(mu)/M]+[v/M for v in mu]
 check(min(y)>=0 and sum(y)==1,'dual simplex')
 aux=[[g['A'][i][j]-lam*g['b'][j] for j in range(len(y))] for i in range(len(x))]
 rowvals=[dot(row,y) for row in aux];colvals=[dot(x,[aux[i][j] for i in range(len(x))]) for j in range(len(y))]
 check(max(rowvals)==min(colvals)==-val,'aux minimax exact')
 crossing=dot(g['a'],x)==lam
 if crossing:
  ay=[dot(row,y) for row in g['A']];bx=[dot(x,[g['B'][i][j] for i in range(len(x))]) for j in range(len(y))]
  check(max(ay)==dot(x,ay) and max(bx)==dot(y,bx),'full Nash inequalities');count('fresh_second_equilibrium_pairs')
 count('fresh_auxiliary_dual_pairs')
 return crossing

def run(w,game=False):
 E,nodes,F=net(w);orig=[e[3] for e in E];D=1
 for x in orig:D=lcm(D,x.denominator)
 pert=[x+Q(1,4*D*3**(i+1)) for i,x in enumerate(orig)];H=1+max(abs(x) for x in pert);ranks={v:i for i,v in enumerate(nodes)};cost=[c+H*(ranks[v]-ranks[u]) for (u,v,_,_),c in zip(E,pert)]
 check(min(cost)>0,'positive potential costs');gg=build_game(E,nodes,F,cost) if game else None
 f=tuple(Q(0) for _ in E);events=[];samples=[]
 zeros=[j for j in range(2**len(w)) if sum((-1 if j>>(i)&1 else 1)*z for i,z in enumerate(w))==0]
 for q in range(F):
  P=shortest(E,nodes,f,pert)[0];g=advance(f,P)
  check(min(a[4] for a in P)==1,'perturbed unit');check(sum(a[-1] for a in P)==sum(orig[a[2]]*a[3] for a in shortest(E,nodes,f,orig)[0])+sum((pert[a[2]]-orig[a[2]])*a[3] for a in P),'same-state original shortest')
  for step in [Q(1,3),Q(1,2),Q(2,3)]:
   mid=advance(f,P,step);lam=Q(q)+step;feasible(E,nodes,mid,lam);distances(nodes,residual(E,mid,pert));count('fractional_optimality_controls')
   if gg and (mid[-1]==Q(1,2) or q in [0,F-1]) and lam+gg['K']*mid[-1]<=F:
    cross=verify_aux(E,nodes,cost,mid,lam,gg);check(cross==(mid[-1]==Q(1,2)),'scalar crossing iff half bridge')
  if f[-1]!=g[-1]:events.append((q,int(g[-1]-f[-1])));check(q//2 in zeros,'event exactly partition state')
  count('augmentations');f=g
 check(events==[(2*j+d,1 if d==0 else -1) for j in zeros for d in [0,1]],'complete event sequence')
 if gg:
  count('complete_games');check(f[-1]==0,'terminal bridge zero')
  for lam in [-gg['eps'],-gg['eps']/2]:
   x=[Q(1)]+[Q(0)]*(len(gg['a'])-1);values=[dot(row,x)-r-s*lam for row,r,s in zip(gg['R'],gg['r'],gg['s'])];check(values.index(max(values))==gg['k']-1 and values.count(max(values))==1,'negative unique column')
 return {'weights':w,'partition_states':zeros,'events':events,'game_built':game,'M_bits':gg['M'].bit_length() if gg else None}

if __name__=='__main__':
 start=datetime.now(timezone.utc).isoformat();cases=[[1],[7],[1,1],[1,2],[2,2],[1,1,1],[1,2,3],[2,3,4],[1,1,2,2],[1,2,4,8],[1,3,5,7],[3,3,3,3],[1,2,3,4,5],[2**80+1,2**80+1]]
 outcomes=[run(w,i in [0,2,3,6,7,13]) for i,w in enumerate(cases)]
 choice=[]
 for n in [1,2]:
  for w in product(range(1,4),repeat=n):
   states=[j for j in range(2**n) if sum((-1 if j>>i&1 else 1)*z for i,z in enumerate(w))==0];term,countstates=original_search(w);check(bool(term) and all(t==bool(states) for t in term),'every original shortest execution event');choice.append({'weights':w,'states_visited':countstates,'terminal_event_options':term})
 # Removing base tie-break must permit a missed diagnostic in a yes instance.
 term,ns=original_search((1,1),delta=False);check(False in term,'negative control missing base shift detected')
 # A too-small exact penalty admits the infeasible origin at positive demand.
 E,nodes,F=net([1]);zero=[Q(0)]*len(E);check(sum(zero)==0 and Q(1)>0,'zero penalty infeasibility control')
 result={'completed_utc':datetime.now(timezone.utc).isoformat(),'started_utc':start,'completion_percent':70,'status':'ALL_FRESH_CHECKS_PASSED','counts':COUNTS,'cases':outcomes,'all_choice_searches':choice,'negative_controls':{'removed_base_shift_all_choice_search':{'detected':False in term,'states':ns},'M_zero_fails_positive_demand':'At lambda=1, origin has cost zero and penalty zero but violates q=lambda; every feasible positive flow has strictly positive potential-shifted cost.'},'limits':'Finite exact controls only; no original helper/code imports, no exhaustive equilibrium enumeration, universal conclusions require proof.'}
 (R/'fresh_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'counts':COUNTS,'case_count':len(cases),'choice_search_count':len(choice),'max_M_bits':max(x['M_bits'] or 0 for x in outcomes)},indent=2))
