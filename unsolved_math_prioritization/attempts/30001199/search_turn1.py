import numpy as np, random,json,time
p=1009;rng=random.Random(1199);calls=0

def rr(M):
 M=np.array(M,dtype=np.int64,copy=True)%p;row=0;piv=[]
 for j in range(M.shape[1]):
  ks=np.flatnonzero(M[row:,j])
  if not len(ks):continue
  k=row+int(ks[0]);M[[row,k]]=M[[k,row]];M[row]=(M[row]*pow(int(M[row,j]),-1,p))%p
  for k in range(M.shape[0]):
   if k!=row and M[k,j]:M[k]=(M[k]-M[k,j]*M[row])%p
  piv.append(j);row+=1
  if row==M.shape[0]:break
 return M,piv

def null(M):
 M,piv=rr(M);n=M.shape[1];free=[i for i in range(n) if i not in piv];Z=np.zeros((n,len(free)),dtype=np.int64)
 for k,j in enumerate(free):
  Z[j,k]=1
  for i,c in enumerate(piv):Z[c,k]=-M[i,j]%p
 return Z

def rank(M):return len(rr(M)[1])
def bd(A,B):
 out=np.zeros((len(A)+len(B),A.shape[1]+B.shape[1]),dtype=np.int64);out[:len(A),:A.shape[1]]=A;out[len(A):,A.shape[1]:]=B;return out

def comp(x,y):
 A,B,L,C=x;D,E,M,F=y
 return (np.block([[A,-B@F],[E@C,D]]),bd(L,M),bd(C,F))

def sim(src,tgt):
 global calls
 calls+=1
 A,L,C=src;D,M,F=tgt;ns=len(A);nt=len(D);AA=bd(A,D)
 E=np.hstack((C,-F));W=null(E);V=np.vstack((np.zeros((ns,M.shape[1]),dtype=np.int64),M))
 for k in range(ns+nt+1):
  WV=np.hstack((W,V));ann=null(WV.T).T;WW=null(np.vstack((E,(ann@AA)%p)))
  if WW.shape[1]==W.shape[1]:W=WW;break
  W=WW
 if rank(W[:ns,:])<ns:return False
 U=np.vstack((L,np.zeros((nt,L.shape[1]),dtype=np.int64)));WV=np.hstack((W,V))
 return rank(np.hstack((WV,U)))==rank(WV)

def rand_sys(n=2):
 A=np.array([[rng.choice([-1,0,0,1]) for _ in range(n)] for _ in range(n)],dtype=np.int64)
 B=np.array([[rng.choice([-1,0,1])] for _ in range(n)],dtype=np.int64)
 L=np.array([[0] for _ in range(n)],dtype=np.int64)
 if rng.random()<.7:L[rng.randrange(n),0]=1
 C=np.array([[1]+[0]*(n-1)],dtype=np.int64)
 return A,B,L,C

def ser(x):return [m.tolist() for m in x]
start=time.time();eligible=0;trials=0;stats=[]
for qtrial in range(80):
 q1=rand_sys();q2=rand_sys();target=comp(q1,q2);p1s=[q1];p2s=[q2]
 assert sim(target,target)
 for i in range(90):
  pp=rand_sys(rng.choice([1,2,2]))
  if sim(comp(pp,q2),target):p1s.append(pp)
  if sim(comp(q1,pp),target):p2s.append(pp)
 eligible+=len(p1s)*len(p2s)
 for x in p1s:
  for y in p2s:
   trials+=1
   if not sim(comp(x,y),target):
    print(json.dumps({'status':'finite_field_candidate_requires_rational_verification','prime':p,'Q1':ser(q1),'Q2':ser(q2),'P1':ser(x),'P2':ser(y),'simulation_calls':calls,'pair_tests':trials,'elapsed_seconds':time.time()-start},indent=2));raise SystemExit
 stats.append([len(p1s),len(p2s)])
print(json.dumps({'status':'no_finite_field_witness_found','prime':p,'simulation_calls':calls,'pair_tests':trials,'reference_pairs':len(stats),'eligible_sizes':stats,'scope':'Proposal filter over a finite field only, not proof of the real linear-system theorem.'},indent=2))
