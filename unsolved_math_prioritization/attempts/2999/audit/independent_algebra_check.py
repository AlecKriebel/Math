#!/usr/bin/env python3
"""Independent tensor-coefficient calculation; no imports from the author checker.
The grid test is exact polynomial interpolation, not a numerical sampling claim:
each coordinate degree of every tested identity is at most 2, and {-1,0,1}^6 is
unisolvent for that polynomial space. Topology is reviewed in AUDIT_REPORT.md.
"""
import itertools,json

def require(value, message):
    if not value:
        raise ValueError(message)

# a_i=A[i,j]p_j and e_i=B[i,j]p_j are alpha and eta components.
A=[[0]*6 for _ in range(6)]
B=[[0]*6 for _ in range(6)]
for i,j in [(0,1),(2,3)]:
    A[i][j]=-1;A[j][i]=1
B[4][5]=-1;B[5][4]=1

def tensor(p):
    a=[sum(A[i][j]*p[j] for j in range(6)) for i in range(6)]
    e=[sum(B[i][j]*p[j] for j in range(6)) for i in range(6)]
    def dwedge(k,i,j):
        return A[i][k]*e[j]+a[i]*B[j][k]-A[j][k]*e[i]-a[j]*B[i][k]
    d=[[[dwedge(i,j,k)-dwedge(j,i,k)+dwedge(k,i,j)
         for k in range(6)] for j in range(6)] for i in range(6)]
    return a,e,d

def main():
    points=0;components=0
    for p in itertools.product((-1,0,1),repeat=6):
        a,e,d=tensor(p);R=a;T=e
        q=sum(t*t for t in p[:4]);r=sum(t*t for t in p[4:])
        require(sum(a[i]*R[i] for i in range(6))==q,'alpha(R)')
        require(sum(e[i]*T[i] for i in range(6))==r,'eta(T)')
        require(sum(a[i]*T[i] for i in range(6))==0,'alpha(T)')
        require(sum(e[i]*R[i] for i in range(6))==0,'eta(R)')
        for k in range(6):
            got=sum(R[i]*T[j]*d[i][j][k] for i in range(6) for j in range(6))
            wanted=2*(r if k<4 else q)*p[k]
            require(got==wanted,'ambient contraction identity')
            components+=1
        points+=1
    p=(1,0,0,0,1,0);a,e,d=tensor(p)
    require(d[2][3][5]==2,'nonclosedness witness')
    # Both sphere constraints have zero derivative on coordinate directions 2,3,5.
    for k in (2,3,5):
        require((2*p[k] if k<4 else 0)==0,'S3 tangency')
        require((2*p[k] if k>=4 else 0)==0,'S1 tangency')
    print(json.dumps({'independent_tensor_calculation':'PASS','unisolvent_grid_points':points,
        'contracted_components_checked':components,'max_coordinate_degree':2,
        'nonclosedness_value':d[2][3][5],
        'meaning':'exact polynomial identity check; does not mechanize topology'},indent=2))
if __name__=='__main__':main()
