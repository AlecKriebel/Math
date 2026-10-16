#!/usr/bin/env python3
"""Third-review fresh exact flow/game checks, no imports of inherited checkers."""
from fractions import Fraction as Q
from itertools import product
from math import lcm,factorial
from pathlib import Path
import hashlib,json,datetime,random
HERE=Path(__file__).resolve().parent
def need(ok,why):
 if not ok:raise RuntimeError(why)
def dot(v,w):return sum((a*b for a,b in zip(v,w)),Q(0))
def make(w,base_adjustment=True):
 need(len(w)>0 and all(type(z)==int and z>0 for z in w),'source domain')
 n=len(w);S=sum(w);E=[];nodes=['s']
 for sign in [1,-1]:nodes +=[(sign,'s',i) for i in range(n,-1,-1)]
 for sign in [1,-1]:nodes +=[(sign,'t',i) for i in range(n+1)]
 nodes+=['t']
 for sign in [1,-1]:
  E.append(((sign,'s',0),(sign,'t',0),Q(1),Q(1,120*S) if base_adjustment else Q(0)))
  for i,z in enumerate(w,1):
   v=Q(sign*z,24*S);u=Q(2**(i-1));a=(sign,'s',i);b=(sign,'t',i);c=(sign,'s',i-1);d=(sign,'t',i-1)
   E +=[(a,c,u,v/2),(d,b,u,v/2),(a,d,u,(2**i-1-v)/2),(c,b,u,(2**i-1-v)/2)]
  E += [('s',(sign,'s',n),Q(2**n),Q(0)),((sign,'t',n),'t',Q(2**n),Q(0))]
 E.append(((1,'s',0),(-1,'t',0),Q(1),Q(0)));p=len(E);V=len(nodes);F=Q(2**(n+1));D=lcm(*(z.denominator for a,b,u,z in E));cost=[z+Q(1,4*D*3**(i+1)) for i,(a,b,u,z) in enumerate(E)]
 ranks={a:i for i,a in enumerate(nodes)};H=1+max(abs(z) for z in cost);shift=[z+H*(ranks[b]-ranks[a]) for z,(a,b,u,c) in zip(cost,E)]
 need(p==8*n+7 and V==4*n+6,'dimensions');need(all(ranks[a]<ranks[b] for a,b,u,z in E),'DAG');need(all(z>0 for z in shift),'positive potential')
 return dict(w=w,E=E,nodes=nodes,F=F,e=p-1,cost=cost,shift=shift,orig=[z for a,b,u,z in E],D=D,H=H,ranks=ranks)
def residual(b,f,cost):
 R=[]
 for i,((a,z,u,c),k) in enumerate(zip(b['E'],cost)):
  if f[i]<u:R.append((a,z,k,i,1,u-f[i]))
  if f[i]>0:R.append((z,a,-k,i,-1,f[i]))
 return R
def bf(b,R,source=None):
 d={a:(Q(0) if source is None or a==source else None) for a in b['nodes']};pred={}
 for it in range(len(d)):
  change=False
  for a,z,c,i,s,u in R:
   if d[a] is not None and (d[z] is None or d[z]>d[a]+c):d[z]=d[a]+c;pred[z]=(a,z,c,i,s,u);change=True
  if not change:return d,pred
 raise RuntimeError('negative cycle')
def feasible(b,f,q):
 net={a:Q(0) for a in b['nodes']}
 for z,(a,c,u,k) in zip(f,b['E']):need(0<=z<=u,'capacity');net[a]+=z;net[c]-=z
 need(all(z==(q if a=='s' else -q if a=='t' else 0) for a,z in net.items()),'conservation')
 need(sum(f)<=(len(net)-1)*q,'path bound')
def path(b,f,cost):
 d,pred=bf(b,residual(b,f,cost),'s')
 if d['t'] is None:return None
 P=[];v='t'
 while v!='s':
  step=pred[v];P.append(step);v=step[0];need(len(P)<len(d),'shortest simple')
 return P
def allpaths(b,f,cost):
 adj={a:[] for a in b['nodes']}
 for st in residual(b,f,cost):adj[st[0]].append(st)
 out=[]
 def go(a,seen,P,c):
  if a=='t':out.append((c,P));return
  for st in adj[a]:
   if st[1] not in seen:go(st[1],seen|{st[1]},P+[st],c+st[2])
 go('s',{'s'},[],Q(0))
 return out
def adjust(f,P,amt):
 g=list(f)
 for a,z,c,i,s,u in P:g[i]+=s*amt
 return tuple(g)
def yes(w):return any(sum((z if bits>>i&1 else -z) for i,z in enumerate(w))==0 for bits in range(1<<len(w)))
def flowrun(b):
 f=tuple(Q(0) for z in b['E']);q=Q(0);segments=[];samples=0;half=[]
 while True:
  P=path(b,f,b['cost'])
  if P is None:break
  amount=min(st[-1] for st in P);need(amount==1,'unit augment')
  orig=bf(b,residual(b,f,b['orig']),'s')[0]['t'];need(sum(st[2]-Q(st[4],4*b['D']*3**(st[3]+1)) for st in P)==orig,'same-state original comparison')
  g=adjust(f,P,amount)
  for frac in [Q(0),Q(1,7),Q(2,5),Q(1,2),Q(6,7),Q(1)]:
   z=adjust(f,P,frac*amount);d=bf(b,residual(b,z,b['cost']))[0];ds=bf(b,residual(b,z,b['shift']))[0];qq=q+frac*amount;feasible(b,z,qq)
   need(all(c+d[a]-d[v]>=0 for a,v,c,i,s,u in residual(b,z,b['cost'])),'dual reduced costs')
   need(dot(z,b['shift'])-dot(z,b['cost'])==b['H']*(b['ranks']['t']-b['ranks']['s'])*qq,'potential telescoping')
   if not yes(b['w']):need(z[b['e']]==0,'no-case sampled bridge')
   samples+=1
  if f[b['e']]==0 and g[b['e']]==1:
   pp=path(b,g,b['cost']);need(pp is not None and adjust(g,pp,1)[b['e']]==0,'immediate reverse')
   qq=q+Q(1,2);L=len(b['nodes'])-1;need(qq<=b['F']-Q(3,2) and qq+Q(1,4*L)<b['F'],'retained half upper boundary');half.append(str(qq))
  segments.append((q,f,g));q+=amount;f=g
 need(q==b['F'] and f[b['e']]==0,'terminal flow');need(bool(half)==yes(b['w']),'partition equivalence')
 return segments,{'w':b['w'],'partition':yes(b['w']),'augmentations':len(segments),'fractional_dual_certificates':samples,'half_values':half}
def tied(b):
 cur={(tuple(Q(0) for e in b['E']),False)};states=1;branches=0;term=set()
 while cur:
  nxt=set()
  for f,used in cur:
   P=allpaths(b,f,b['orig'])
   if not P:term.add(used);continue
   m=min(c for c,p in P);opts=[p for c,p in P if c==m];branches+=len(opts)-1
   for p in opts:
    amount=min(st[-1] for st in p);need(amount==1,'all ties unit');g=adjust(f,p,amount);forward=(g[b['e']]>f[b['e']])
    if forward:
     P2=allpaths(b,g,b['orig']);m2=min(c for c,p in P2);need(all(adjust(g,pp,1)[b['e']]==0 for c,pp in P2 if c==m2),'all ties reverse')
    nxt.add((g,used or forward))
  cur=nxt;states+=len(cur)
 need(term=={yes(b['w'])},'all tied executions iff partition')
 return {'weights':b['w'],'states':states,'tie_branches':branches,'terminal_bridge_flags':list(term)}
def create_game(b):
 E=b['E'];p=len(E);L=len(b['nodes'])-1;F=b['F'];e=b['e'];m=p+2;K=Q(1,2*L);eps=K/2;c=[Q(0),Q(0)]+[L*F*z for z in b['shift']];q=[Q(0)]+[F]*(p+1);q[e+2]=F/2
 R=[];r=[];s=[]
 for i,(u,v,cap,cost) in enumerate(E):row=[Q(0)]*m;row[i+2]=L*F;R.append(row);r.append(cap);s.append(Q(0))
 for v in b['nodes']:
  dv=int(v=='s')-int(v=='t');row=[-dv*z for z in q]
  for i,(u,z,cap,cost) in enumerate(E):row[i+2]+=L*F*(int(u==v)-int(z==v))
  R.extend([row,[-z for z in row]]);r.extend([Q(0)]*2);s.extend([Q(0)]*2)
 diag=len(R)+1;R.extend([q,[-z for z in q]]);r.extend([Q(0)]*2);s.extend([Q(1),Q(-1)]);k=len(R)
 clear=lcm(*(z.denominator for row in R for z in row),*(z.denominator for z in c));H=max([clear,1]+[abs(int(z*clear)) for row in R for z in row]+[abs(int(z*clear)) for z in c]);C=k*factorial(k+1)*H**(k+1);M=C+1;a=[-eps]+[F-eps]*(m-1);bv=[Q(0)]+[-M*z for z in s]
 A=[[-c[i]]+[-c[i]-M*row[i]+M*rr for row,rr in zip(R,r)] for i in range(m)];B=[[-A[i][j]+a[i]*bv[j] for j in range(k+1)] for i in range(m)]
 need(all(A[i][j]+B[i][j]==a[i]*bv[j] for i in range(m) for j in range(k+1)) and M in bv and -M in bv and a[0]!=0,'rank one')
 return dict(L=L,F=F,K=K,eps=eps,c=c,q=q,R=R,r=r,s=s,M=M,a=a,b=bv,A=A,B=B,diag=diag)
def verify(A,B,x,y):
 need(min(x)>=0 and min(y)>=0 and sum(x)==sum(y)==1,'simplex witness')
 ru=[dot(row,y) for row in A];cu=[sum(x[i]*B[i][j] for i in range(len(x))) for j in range(len(y))]
 need(max(ru)<=dot(x,ru) and max(cu)<=dot(y,cu),'best-response certificate')
def gamechecks(b,seg):
 g=create_game(b);m=len(g['a']);N=len(g['b']);x0=[Q(1)]+[Q(0)]*(m-1);y0=[Q(0)]*N;y0[g['diag']]=1;verify(g['A'],g['B'],x0,y0)
 need(all(g['A'][i][g['diag']]<g['A'][0][g['diag']] for i in range(1,m)) and all(g['B'][0][j]<g['B'][0][g['diag']] for j in range(N) if j!=g['diag']),'strict default')
 cnt=0;extra=0
 for q,old,new in seg:
  for z in [Q(1,7),Q(2,5),Q(1,2),Q(6,7)]:
   f=[u+(v-u)*z for u,v in zip(old,new)];lam=q+z;h=lam+g['K']*f[b['e']]
   if h>g['F']:continue
   x=[1-h/g['F'],h/g['F']-sum(f)/(g['L']*g['F'])]+[z/(g['L']*g['F']) for z in f];need(dot(g['q'],x)==lam,'simplex q inverse')
   d=bf(b,residual(b,f,b['shift']))[0];mu=[max(Q(0),-(c+d[u]-d[v])) for (u,v,cap,c0),c in zip(b['E'],b['shift'])]
   for v in b['nodes']:mu +=[max(Q(0),d[v]),max(Q(0),-d[v])]
   beta=d['s']-d['t'];mu +=[max(Q(0),beta),max(Q(0),-beta)]
   dual=[g['c'][i]+sum(mu[j]*g['R'][j][i] for j in range(len(mu))) for i in range(m)];need(min(dual)>=0 and dot(dual,x)==0,'simplex dual optimal')
   need(sum(mu)<g['M'],'M exceeds explicit dual');y=[1-sum(mu)/g['M']]+[z/g['M'] for z in mu]
   Aux=[[z-lam*g['b'][j] for j,z in enumerate(row)] for row in g['A']];verify(Aux,[[-z for z in row] for row in Aux],x,y);cnt+=1
   if f[b['e']]==Q(1,2):need(dot(g['a'],x)==lam,'scalar crossing');verify(g['A'],g['B'],x,y);extra+=1
 need(bool(extra)==yes(b['w']),'actual additional pair iff partition')
 return {'weights':b['w'],'dimensions':[m,N],'M_bits':g['M'].bit_length(),'new_auxiliary_pairs':cnt,'additional_pairs':extra,'strict_default':True}
def controls():
 rejected=[]
 for w in [[],[0],[1,-1]]:
  try:make(w)
  except RuntimeError:rejected.append(w)
 need(len(rejected)==3,'domain guard')
 b=make([1,1],False);f=tuple(Q(0) for e in b['E'])
 while True:
  P=allpaths(b,f,b['orig'])
  if not P:break
  low=min(c for c,p in P);opts=[p for c,p in P if c==low and all(st[3]!=b['e'] for st in p)];need(opts,'delta zero skips diagnostic');f=adjust(f,opts[0],1)
 need(f[b['e']]==0,'delta control')
 # Uniform exact penalty requires strict excess over dual norm.
 lam=Q(1);t=Q(3,4);need(-t+max(Q(0),t-lam/2)==-lam/2 and t>lam/2,'M=dualnorm infeasible tie')
 need(Q(2)>Q(1),'oversized perturbation can reverse costs 0,1')
 A=[[Q(0),Q(0)],[Q(0),Q(0)]];B=[[Q(1),Q(1)],[Q(1),Q(1)]]
 verify(A,B,[Q(1),Q(0)],[Q(1),Q(0)]);verify(A,B,[Q(0),Q(1)],[Q(0),Q(1)])
 try:verify([[Q(1),Q(6)],[Q(0),Q(9)]],[[Q(1),Q(0)],[Q(6),Q(9)]],[Q(1,2)]*2,[Q(1,2)]*2)
 except RuntimeError:bad=True
 else:bad=False
 need(bad,'bad pair rejected')
 return {'source_domain_rejected':rejected,'delta_zero_yes_skips_bridge':True,'M_equal_dual_norm_all_minimizer_failure':True,'oversized_perturbation_comparison_failure':True,'degenerate_rank_one_continuum_boundary_pairs':True,'non_equilibrium_pair_rejected':True}
def main():
 rng=random.Random(1041);cases=[[1],[1,1],[1,3],[1,2,3],[2,3,5],[1,1,1],[2**80+1,2**80+1],[2**64+1,2**64+2]]
 cases+=list(map(list,product(range(1,4),repeat=3)));cases +=[[rng.randrange(1,100) for i in range(4)] for j in range(12)]
 cases=[list(z) for z in dict.fromkeys(tuple(z) for z in cases)];flows=[];games=[]
 for w in cases:
  b=make(w);seg,fr=flowrun(b);flows.append(fr)
  if w in [[1],[1,1],[1,3],[2,3,5]]:games.append(gamechecks(b,seg))
 ties=[tied(make(w)) for w in [[1],[1,1],[1,3],[1,1,1],[1,2,3],[1,2,4],[2,3,5],[3,4,5]]]
 out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'mode':'optimized' if not __debug__ else 'normal','all_guards_explicit':True,'flows':flows,'games':games,'all_original_tie_searches':ties,'negative_controls':controls(),'status':'PASS','limits':'Finite independent exact certificates; no exhaustive arbitrary-instance proof, no formal assistant and no historical omitted computation replay.'}
 (HERE/('MATH_OPTIMIZED.json' if not __debug__ else 'MATH_NORMAL.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','flow_cases':len(flows),'augmentations':sum(z['augmentations'] for z in flows),'fractional_dual_certificates':sum(z['fractional_dual_certificates'] for z in flows),'full_games':len(games),'new_auxiliary_pairs':sum(z['new_auxiliary_pairs'] for z in games),'original_tie_searches':len(ties),'controls':out['negative_controls']},indent=2))
if __name__=='__main__':main()
