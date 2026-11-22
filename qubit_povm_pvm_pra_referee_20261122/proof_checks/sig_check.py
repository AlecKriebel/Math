import numpy as np
rng=np.random.default_rng(0)
cnt={}
ex=None
for _ in range(200000):
    a,b,c,d=rng.uniform(0,.5,4); e=a+b+c+d-.5
    if e>0 and a+b<.5 and c+d<.5 and a+c<.5 and b+d<.5:
        g=np.array([[0,.5,a,b],[.5,0,c,d],[a,c,0,e],[b,d,e,0.]])
        ev=np.linalg.eigvalsh(g); s=((ev>1e-12).sum(),(ev<-1e-12).sum())
        cnt[s]=cnt.get(s,0)+1
        if s!=(1,3) and ex is None: ex=(a,b,c,d,e,ev)
print(cnt); print(ex)
