import numpy as np, sympy as sp
from scipy.optimize import minimize
I2=np.eye(2); X=np.array([[0,1],[1,0]],float); Z=np.diag([1.,-1.]); Y=np.array([[0,-1j],[1j,0]])
alpha=[1,-1,1]; beta=[1,-1]
def bell(rho, M, N):
    # M[x][a], N[y][b]
    val=0
    def p(a,b,x,y): return np.real(np.trace(rho@np.kron(M[x][a],N[y][b])))
    for (x,y,s) in [(0,0,1),(0,1,1),(1,0,1),(1,1,-1)]:
        for a in range(3):
            for b in range(2):
                val+=10*s*alpha[a]*beta[b]*p(a,b,x,y)
    val+=0.6*p(0,0,2,0)+0.6*p(1,1,2,0)+0.8*p(2,0,2,1)
    return val
# simple strategy
phi=np.array([1,0,0,1])/np.sqrt(2); rho=np.outer(phi,phi)
A0=(Z+X)/np.sqrt(2); A1=(Z-X)/np.sqrt(2)
M=[[ (I2+A0)/2,(I2-A0)/2,0*I2],[(I2+A1)/2,(I2-A1)/2,0*I2],[(17*I2-8*X+15*Z)/50,(17*I2-8*X-15*Z)/50,(16*I2+16*X)/50]]
N=[[(I2+Z)/2,(I2-Z)/2],[(I2+X)/2,(I2-X)/2]]
print("L0 strategy:", bell(rho,M,N), 20*np.sqrt(2)+16/25)
print("M2 eigs", [np.linalg.eigvalsh(m) for m in M[2]], "sum", sum(M[2]))
# strengthened
q=np.sqrt(7813); eta=1/q
psi=np.array([np.sqrt((1+eta)/2),0,0,np.sqrt((1-eta)/2)]); rho=np.outer(psi,psi)
A0=(6*np.sqrt(217)*X+q*Z)/125; A1=(6*np.sqrt(217)*X-q*Z)/125
k=0.6*np.sqrt((q-1)/(q+1))
M2=[0.5*np.array([[k*k,k],[k,1]]),0.5*np.array([[k*k,-k],[-k,1]]),np.array([[1-k*k,0],[0,0]])]
M=[[ (I2+A0)/2,(I2-A0)/2,0*I2],[(I2+A1)/2,(I2-A1)/2,0*I2],M2]
N=[[(I2+X)/2,(I2-X)/2],[(I2+Z)/2,(I2-Z)/2]]
print("L1 strategy:", bell(rho,M,N), (16+8*q)/25, "A0^2", np.allclose(A0@A0,I2), "sumM2", sum(M2), [np.linalg.eigvalsh(m) for m in M2])
print("gap L1-28.9:", (16+8*q)/25-28.9, (16*q-1413)/50)
qq=sp.sqrt(7813)
print("exact gap > 0.02517:", sp.N((16*qq-1413)/50,20), (16*qq-1413)/50 > sp.Rational(2517,100000))
U=20*sp.sqrt(2)+sp.Rational(3,5)+(4+3*sp.sqrt(2))/250
print("U",sp.N(U,15),"L0",sp.N(20*sp.sqrt(2)+sp.Rational(16,25),15),"L1",sp.N((16+8*qq)/25,15))
print("L0-U", sp.simplify(20*sp.sqrt(2)+sp.Rational(16,25)-U - 3*(2-sp.sqrt(2))/250))
print((6+80*qq)**2-2*5003**2, sp.expand((6+80*qq)**2-2*5003**2), 960**2*7813-56782**2)

# random-matrix test of operator identity in dims
G=np.array([
[5127,-24,1,7,-9,-19,-1810,-1809,-1788,1788,-23,30],
[-24,1670,1,-2,-1190,-1191,8,-8,20,-13,-3,-3],
[1,1,1718,11,-1212,1212,-20,13,-39,-39,2,-2],
[7,-2,11,27,-22,30,3,3,-2,2,-5,6],
[-9,-1190,-1212,-22,1712,-18,3,-2,26,17,3,0],
[-19,-1191,1212,30,-18,1723,2,21,-17,-27,0,5],
[-1810,8,-20,3,3,2,1283,644,628,0,18,0],
[-1809,-8,13,3,-2,21,644,1277,0,-629,0,-16],
[-1788,20,-39,-2,26,-17,628,0,1273,-625,-8,0],
[1788,-13,-39,2,17,-27,0,-629,-625,1269,0,-3],
[-23,-3,2,-5,3,0,18,0,-8,0,25,-1],
[30,-3,-2,6,0,5,0,-16,0,-3,-1,26]],float)
rng=np.random.default_rng(0)
def rand_inv(d):
    Hh=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); Hh=Hh+Hh.conj().T
    w,v=np.linalg.eigh(Hh)
    s=rng.choice([-1,1],size=d)
    return v@np.diag(s)@v.conj().T
for (dA,dB) in [(2,2),(3,2),(3,4),(5,5)]:
    A=[np.kron(rand_inv(dA),np.eye(dB)) for _ in range(3)]
    B=[np.kron(np.eye(dA),rand_inv(dB)) for _ in range(2)]
    Id=np.eye(dA*dB)
    W=[Id,A[0],A[1],A[2],B[0],B[1],A[0]@B[0],A[0]@B[1],A[1]@B[0],A[1]@B[1],A[2]@B[0],A[2]@B[1]]
    rhs=sum(G[i,j]*W[i].conj().T@W[j] for i in range(12) for j in range(12))/600
    S=A[0]@(B[0]+B[1])+A[1]@(B[0]-B[1])
    B02=10*S+0.35*Id+0.15*B[0]+0.2*B[1]-0.05*A[2]+0.15*A[2]@B[0]-0.2*A[2]@B[1]
    # compare with direct expansion from functional
    M0=(Id+A[2])/2; M2_=(Id-A[2])/2
    direct=10*S+0.6*M0@(Id+B[0])/2+0.8*M2_@(Id+B[1])/2
    print(dA,dB,"identity err",np.abs(28.9*Id-B02-rhs).max(),"expansion err",np.abs(direct-B02).max(),"max eig B02",np.linalg.eigvalsh(B02).max())
