"""Independent stored-matrix arithmetic check, explicitly not graph-to-Jacobian regeneration."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,tarfile,time
from datetime import datetime,timezone
D=Path(__file__).resolve().parent;P=D.parents[3]
A=P/'papers/22178672/sources/K3P_Level2_Full_Reproducibility_v1.0.0.tar.gz'
NAME='k3p_level2_reproducibility/sharpness/K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json'
def req(c,m):
    if not c:raise RuntimeError(m)
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[1],-a[0])
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    v=[x*y for x in a for y in b];return(min(v),max(v))
def I(a):return tuple(map(Q,a))
def maxabs(a):return max(abs(a[0]),abs(a[1]))
def err(Y,J):
    return [[sub((Q(i==j),Q(i==j)),sumI(mul((Y[i][k],Y[i][k]),J[k][j]) for k in range(15))) for j in range(15)] for i in range(15)]
def sumI(v):
    out=(Q(0),Q(0))
    for x in v:out=add(out,x)
    return out
def norm(E):return max(sum(maxabs(z) for z in row) for row in E)
start=datetime.now(timezone.utc).isoformat();t=time.monotonic()
with tarfile.open(A,'r:gz') as archive:
    member=archive.getmember(NAME);req(member.isfile(),'regular member')
    blob=archive.extractfile(member).read();req(hashlib.sha256(blob).hexdigest()=='8187174b3e0c0b3a0a55fa32595c211811c357dc223ada7a74b3033f7cae3941','bound exact certificate')
C=json.loads(blob);E=C['equality_system'];K=C['krawczyk'];B=C['parameterization']
Y=[list(map(Q,row)) for row in K['preconditioner_exact_inverse_of_point_jacobian']]
J0=[list(map(Q,row)) for row in E['point_jacobian']]
req(all(sum(Y[i][k]*J0[k][j] for k in range(15))==int(i==j) for i in range(15) for j in range(15)),'exact inverse')
J=[[I(v) for v in row] for row in E['interval_jacobian']]
error=err(Y,J);req(error==[[I(v) for v in row] for row in K['error_matrix_I_minus_Y_J_box']],'interval error matrix')
q=norm(error);req(q==Q(K['preconditioned_interval_jacobian_infinity_bound']) and q<1,'contraction norm')
center=list(map(Q,B['scaled_variable_center']));radius=Q(B['box_radius']);f0=list(map(Q,E['exact_center_residual']))
correction=[center[i]-sum(Y[i][j]*f0[j] for j in range(15)) for i in range(15)]
operator=[add((correction[i],correction[i]),sumI(mul(z,(-radius,radius)) for z in error[i])) for i in range(15)]
req(operator==list(map(I,K['operator_intervals'])),'Krawczyk operator')
req(all(center[i]-radius<lo<=hi<center[i]+radius for i,(lo,hi) in enumerate(operator)),'strict inclusion')
normalized=max(max(abs(lo-center[i]),abs(hi-center[i]))/radius for i,(lo,hi) in enumerate(operator))
req(normalized==Q(K['max_normalized_distance_from_box_center']),'normalized strict inclusion')
rankbounds={}
for name,R in C['rank_15_minors'].items():
    YR=[list(map(Q,row)) for row in R['point_inverse_preconditioner']]
    JR=[[I(v) for v in row] for row in R['minor_interval_matrix']]
    errorR=err(YR,JR);req(errorR==[[I(v) for v in row] for row in R['neumann_error_matrix']],name+' rank error')
    qr=norm(errorR);req(qr==Q(R['neumann_infinity_bound']) and qr<1,name+' rank norm')
    rankbounds[name]=f'{float(qr):.10e}'
values=list(map(I,B['direct_parameter_box']));mins=[]
for offset in (0,32):
    v=values[offset:offset+32]
    for j in range(10):
        c,g,tv=v[3*j:3*j+3]
        for z in(c,g,tv):mins.extend([z[0],1-z[1]])
        for x,y,z in[(c,g,tv),(g,c,tv),(tv,c,g)]:
            mins.extend([sub(add((Q(1),Q(1)),x),add(y,z))[0]/4,sub(x,mul(y,z))[0]])
    for z in v[30:]:mins.extend([z[0],1-z[1]])
req(min(mins)>0,'all exact direct-box physical and CT inequalities')
# A reversed claimed inclusion is rejected by the same strict comparison.
req(not all(center[i]-radius<lo<=hi<center[i]+radius for i,(lo,hi) in enumerate([(-Q(2)*radius+center[0],Q(2)*radius+center[0])]+operator[1:])),'expanded-box-output negative control')
result={'start_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'archive_path':str(A),'member':NAME,'member_sha256':hashlib.sha256(blob).hexdigest(),'exact_inverse_and_interval_error_recomputed':True,'strict_krawczyk_inclusion_recomputed':True,'normalized_distance_approx':f'{float(normalized):.10e}','contraction_norm_approx':f'{float(q):.10e}','both_rank_neumann_bounds_recomputed':rankbounds,'direct_box_strict_physics_recomputed':True,'expanded_output_interval_rejected':True,'limit':'Matrices/boxes are read from the bound exact certificate. Literal graph-to-polynomial, polynomial-to-Jacobian and full suite regeneration were not performed by this check.'}
(D/'INTERVAL_ARITHMETIC_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
