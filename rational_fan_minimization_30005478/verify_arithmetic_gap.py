"""Exact finite checks, not a substitute for the universal proofs."""
import json, hashlib
from pathlib import Path

def check(condition, label):
    if not condition:
        raise RuntimeError("FAIL: " + label)

import sympy as s
from itertools import combinations
I=s.eye(7)
e=[I[:,j] for j in range(7)]
mat=lambda cols:s.Matrix.hstack(*cols)
H=mat(e[:4]); E=mat(e[4:6]); F=mat(e[6:])
pairs=[(e[0],e[1]),(e[2],e[3]),(e[0]+e[2],e[1]+e[3]),(e[0]+e[3],e[1]+2*e[2])]
Ps=[mat(pq) for pq in pairs]
Ss=[P.row_join(F) for P in Ps]
Vs=[H,E]+Ss
rank=lambda A:A.rank()
intersection=lambda A,B:rank(A)+rank(B)-rank(A.row_join(B))
objective=lambda U:max(2*rank(U.row_join(V))-rank(U) for V in Vs)
A=mat([s.sqrt(2)*e[0]+e[1],s.sqrt(2)*e[2]+e[3]])
check([intersection(A,P) for P in Ps]==[1]*4, "exact check 01")
check(objective(A)==6, "exact check 02")
check(objective(I)==7, "exact check 03")
T=s.Matrix([[0,2],[1,0]])
x=s.Symbol('x')
check(T.charpoly(x).as_expr()==x*x-2, "exact check 04")
check(s.Poly(x*x-2,x,domain=s.QQ).is_irreducible, "exact check 05")
cones=[mat([p+e[6],q+e[6],p+q+e[6]]) for p,q in pairs]
check(all(rank(C)==3 for C in cones), "exact check 06")
check(all(intersection(P,Q)==0 for P,Q in combinations(Ps,2)), "exact check 07")
check(all(intersection(S,R)==1 for S,R in combinations(Ss,2)), "exact check 08")
check(all(intersection(C,H)==2 for C in cones), "exact check 09")
w=e[0]+e[2]+e[3]
HC=mat([4*w+e[j] for j in range(4)])
check(rank(HC)==4, "exact check 10")
# Nonnegative cone separation is established by inequalities in the report,
# not by vector-space intersection tests.
print('PASS: exact ranks, quadratic irreducibility, real objective6, rational ambient objective7, and all cone-generator ranks.')
print('Input-space dimensions:',[rank(V) for V in Vs])
print('Real witness objective terms:',[2*rank(A.row_join(V))-rank(A) for V in Vs])
print('The universal lower bound and exclusion of all rational threshold6 witnesses are proved symbolically in arithmetic_gap.md.')

# Verify the graph basis really uses the displayed T, not an unrelated matrix.
check(Ps[3][:4,:] == s.eye(2).col_join(T), "graph agrees with T")
# Exact generator inequalities used in the cone-separation proof.
check(all(HC[0,j]>=4 and HC[1,j]<=1 and HC[2,j]>=4 and HC[3,j]>=4 for j in range(4)), "H cone inequalities")
check(all(C[6,j]>0 for C in cones for j in range(3)), "positive F padding")
check(all(C == P * s.Matrix([[1,0,1],[0,1,1]]) + F*s.ones(1,3) for C,P in zip(cones,Ps)), "padded cone formula")
print("PASS: explicit guards remain enabled under python -O; graph and cone checks passed.")

def verify_manifest(root):
    root=Path(root)
    manifest=json.loads((root/"MANIFEST.json").read_text())
    expected={row["path"] for row in manifest["files"]}
    check(len(expected)==len(manifest["files"]), "manifest duplicate paths")
    actual={p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p != root/"MANIFEST.json" and "__pycache__" not in p.parts}
    check(expected==actual, "manifest file inventory")
    for row in manifest["files"]:
        rel=Path(row["path"])
        check(not rel.is_absolute() and ".." not in rel.parts, "manifest safe relative path")
        data=(root/rel).read_bytes()
        check(len(data)==row["bytes"], "manifest byte count: "+str(rel))
        check(hashlib.sha256(data).hexdigest()==row["sha256"], "manifest sha256: "+str(rel))
    print("PASS: complete manifest inventory, bytes and SHA-256.")

if __name__ == "__main__":
    import sys
    if "--manifest" in sys.argv:
        verify_manifest(Path(__file__).resolve().parent)
