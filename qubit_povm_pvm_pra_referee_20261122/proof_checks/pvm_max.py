import numpy as np
from scipy.optimize import minimize
I2=np.eye(2); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1.,-1.]).astype(complex); Y=np.array([[0,-1j],[1j,0]])
def obs(th,ph): return np.sin(th)*np.cos(ph)*X+np.sin(th)*np.sin(ph)*Y+np.cos(th)*Z
def B02(p, sgnB0=1):
    A=[np.kron(obs(p[0],p[1]),I2),np.kron(obs(p[2],p[3]),I2),np.kron(obs(p[4],p[5]),I2)]
    B=[np.kron(I2,obs(p[6],p[7])),np.kron(I2,obs(p[8],p[9]))]
    Id=np.eye(4)
    S=A[0]@(B[0]+B[1])+A[1]@(B[0]-B[1])
    M0=(Id+A[2])/2; M2=(Id-A[2])/2
    if sgnB0==1:
        T=0.6*M0@(Id+B[0])/2+0.8*M2@(Id+B[1])/2   # support {0,2}
    else:
        T=0.6*M0@(Id-B[0])/2+0.8*M2@(Id+B[1])/2   # support {1,2}
    return 10*S+T
rng=np.random.default_rng(1)
best=[-1,-1]
for s_i,sg in enumerate([1,-1]):
    for trial in range(200):
        p0=rng.uniform(0,2*np.pi,10)
        r=minimize(lambda p:-np.linalg.eigvalsh(B02(p,sg)).max(),p0,method='BFGS')
        best[s_i]=max(best[s_i],-r.fun)
print("max qubit PVM values support {0,2},{1,2}:",best, " vs 28.9, U=28.917242, 20sqrt2+0.6=",20*np.sqrt(2)+.6)
