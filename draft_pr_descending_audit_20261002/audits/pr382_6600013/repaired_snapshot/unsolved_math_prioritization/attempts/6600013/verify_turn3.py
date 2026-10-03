from thue_morse_language import language
from rational_linear import matmul,rank,eye
from rectangular_complex import complex as pattern_complex,forgetting
from cochain_images import transpose,nullspace,image_rank
import json
checks=0
def check(x):
 global checks
 assert x;checks+=1
V=sorted(language(2));E=sorted(language(3));vi={w:i for i,w in enumerate(V)};ei={w:i for i,w in enumerate(E)}
B=[[0]*6 for _ in range(4)];M=[[0]*6 for _ in range(6)];VM=[[0]*4 for _ in range(4)]
for j,(a,b) in enumerate(V):VM[vi[1-a,b]][j]=1
for j,(a,b,c) in enumerate(E):
 B[vi[a,b]][j]-=1;B[vi[b,c]][j]+=1
 for w in [(1-a,b,1-b),(b,1-b,c)]:check(w in ei);M[ei[w]][j]+=1
check(matmul(B,M)==matmul(VM,B));check(rank(B)==3)
# All shared-pair collared adjacencies are legal; no false vertex gluing.
legal4=language(4);gluings=set()
for a in E:
 for b in E:
  if a[1:]==b[:-1]:w=a+(b[-1],);check(w in legal4);gluings.add(w)
check(gluings==legal4);check(len(gluings)==10)
C=[[1,0,0],[1,1,-1],[0,0,1],[1,0,0],[0,1,0],[0,0,1]];J=[[1,1,0],[1,0,1],[1,1,0]]
check(matmul(B,C)==[[0]*3 for _ in range(4)]);check(rank(C)==3);check(matmul(M,C)==matmul(C,J));check(rank(J)==rank(matmul(J,J))==2)
J2=matmul(J,J);J3=matmul(J2,J);check(all(J3[i][j]-J2[i][j]-2*J[i][j]==0 for i in range(3) for j in range(3)))
for v,lam in [([-1,1,1],0),([1,1,1],2),([1,-2,1],-1)]:check([sum(a*b for a,b in zip(row,v)) for row in J]==[lam*x for x in v])
check(rank([[-1,1,1],[1,1,-2],[1,1,1]])==3)
P=eye(3)
for n in range(1,17):P=matmul(J,P);check(rank(P)==2)
records=[]
for n,m,expected in [(1,3,[4,4]),(2,4,[4,6]),(2,6,[4,4])]:
 small,ds,hs=pattern_complex(n);large,dl,hl=pattern_complex(m);maps=forgetting(n,m,small,large,hs,hl)
 check(matmul(ds[0],maps[1])==matmul(maps[0],dl[0]));check(matmul(ds[1],maps[2])==matmul(maps[1],dl[1]))
 Z1=nullspace(transpose(ds[1]));check(all(x==0 for row in matmul(transpose(ds[1]),Z1) for x in row));im1=matmul(transpose(maps[1]),Z1)
 r1=image_rank(transpose(dl[0]),im1);r2=image_rank(transpose(dl[1]),transpose(maps[2]));check([r1,r2]==expected)
 records.append(dict(from_scale=n,to_scale=m,image_H1=r1,image_H2=r2))
print(json.dumps(dict(assertions=checks,collared_homology_matrix=J,stable_rational_rank=2,pattern_cohomology_images=records,scope='Exact collared substitution and cochain-persistence controls; limiting Betti numbers(1,4,4) are proved for the special example, not for arbitrary low-complexity tilings.'),indent=2,sort_keys=True))
