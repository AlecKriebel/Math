#!/usr/bin/env python3
"""Independent exact physical tests of the Bell source's mathematical interfaces.

This program does not import any other project checker, parse/evaluate Lean,
invoke a compiler, or certify the main theorem.  Its fixtures use rational
complex matrices; comparisons have no numerical tolerance.  Linear algebra on
finite rational polytopes is exhaustive only for the explicitly recorded sets.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import random
import time
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/semantic_audit'
Q = s.Rational
I2 = s.eye(2)
Z2 = s.zeros(2)
J = s.diag(1, -1, -1, -1)
e0 = s.Matrix([1, 0, 0, 0])
u = s.Matrix([1, 1, 0, 0])
rays = [s.eye(4)[:, k] for k in range(4)] + [s.Matrix([1, 1, -1, -1])]
P0 = s.diag(1, 0)
P1 = s.diag(0, 1)
X = s.Matrix([[0, 1], [1, 0]])
Ypauli = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
records: list[dict] = []
negative_controls: list[dict] = []
fixtures: list[dict] = []


def canon(a):
    return s.cancel(s.expand(a))


def mat(A):
    return A.applyfunc(canon)


def entries(A):
    return list(A) if isinstance(A, s.MatrixBase) else [A]


def check(name, lhs, rhs, scope='exact_fixture'):
    ds = [canon(x) for x in entries(lhs-rhs)]
    if any(x != 0 for x in ds):
        raise AssertionError(f'{name}: {ds}')
    records.append({'name': name, 'scope': scope})


def require(name, condition, scope='exact_fixture'):
    if not bool(condition):
        raise AssertionError(name)
    records.append({'name': name, 'scope': scope})


def reject(name, correct, wrong, source_file, reason, kind="formula_mutation"):
    ds = [canon(x) for x in entries(correct-wrong)]
    witness = next((x for x in ds if x != 0), None)
    if witness is None:
        raise AssertionError(f'Mutation was not detected: {name}')
    negative_controls.append({'name': name, 'nonzero_exact_difference': str(witness),
        'source_file': source_file, 'reason': reason,
        'kind': kind,
        'meaning': 'Independent exact control, NOT a Lean-source mutation or compiler test.'})


def pauli(v):
    return v[0]*I2 + v[1]*X + v[2]*Ypauli + v[3]*Z


def coordinates(A):
    return mat(s.Matrix([s.re(s.trace(A))/2, s.re(A[0, 1]),
        -s.im(A[0, 1]), s.re(A[0, 0]-A[1, 1])/2]))


def su2(a, b, c):
    # Stereographic parametrization of the real unit 3-sphere.
    n = 1+a*a+b*b+c*c
    w, x, y, z = (1-a*a-b*b-c*c)/n, 2*a/n, 2*b/n, 2*c/n
    return mat(s.Matrix([[w+s.I*x, y+s.I*z], [-y+s.I*z, w-s.I*x]]))


def rot(U, M):
    return mat(U*M*U.H)


def planar_pair(t):
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def residual_measurements(t, q, U):
    pts = [(s.Integer(1), s.Integer(0)), planar_pair(t), planar_pair(q)]
    A = s.Matrix([[1, 1, 1], [p[0] for p in pts], [p[1] for p in pts]])
    weights = A.inv()*s.Matrix([1, 0, 0])
    if not all(w > 0 for w in weights):
        raise ValueError('The triangle must enclose the spatial origin strictly.')
    binary = [rot(U, P0), rot(U, P1), Z2]
    ternary = [rot(U, weights[k]*(I2+pts[k][0]*X+pts[k][1]*Ypauli)) for k in range(3)]
    return [binary, ternary]


def density(C):
    v = s.Matrix([C[i, j] for i in range(2) for j in range(2)])
    return mat(v*v.H)


def direct_born(rho, A, B):
    # Direct joint-space trace, not a steering/Pauli formula.
    return canon(s.trace(rho*s.kronecker_product(A, B)))


def table(rho, A, B):
    return {(x, y, a, b): direct_born(rho, A[x][a], B[y][b])
        for x in range(len(A)) for y in range(len(B))
        for a in range(len(A[x])) for b in range(len(B[y]))}


def matrix_repr(A):
    return [[str(x) for x in A.row(i)] for i in range(A.rows)]


def psd2(A):
    return mat(A-A.H) == Z2 and canon(s.trace(A)) >= 0 and canon(A.det()) >= 0


def verify_measurements(name, A, projective=False):
    for x, measurement in enumerate(A):
        check(f'{name}_{x}_normalization', sum(measurement, Z2), I2)
        require(f'{name}_{x}_positive', all(psd2(M) for M in measurement))
        if projective:
            for a, M in enumerate(measurement):
                for b, N in enumerate(measurement):
                    check(f'{name}_{x}_projective_{a}_{b}', M*N, M if a==b else Z2)


def physical_fixtures():
    # Different triangles, Schmidt spectra, and genuinely complex local bases.
    specs = [
        (Q(2), Q(-2), Q(3, 5), Q(4, 5), (Q(1, 3), Q(1, 2), Q(1, 4))),
        (Q(2), Q(-3), Q(5, 13), Q(12, 13), (Q(-1, 2), Q(1, 4), Q(1, 3))),
        (Q(3), Q(-2), Q(8, 17), Q(15, 17), (Q(1, 5), Q(-1, 3), Q(1, 2))),
        (Q(4), Q(-3), Q(7, 25), Q(24, 25), (Q(2, 3), Q(1, 5), Q(-1, 4))),
        (Q(3, 2), Q(-4), Q(20, 29), Q(21, 29), (Q(-1, 3), Q(-1, 2), Q(1, 7))),
        (Q(5), Q(-3, 2), Q(9, 41), Q(40, 41), (Q(1, 7), Q(2, 5), Q(1, 3))),
    ]
    result=[]
    for i,(t,q,a,b,xyz) in enumerate(specs):
        UA=su2(*xyz)
        UB=su2(xyz[2], -xyz[0], xyz[1])
        UC=su2(xyz[1], xyz[0], -xyz[2])
        VC=su2(-xyz[2], xyz[1], xyz[0])
        C=mat(UC*s.diag(a,b)*VC.T)
        A=residual_measurements(t,q,UA)
        B=residual_measurements(q.__abs__(),-t,UB)
        rho=density(C)
        E=s.Matrix.hstack(*[coordinates(M) for M in [A[0][0],A[0][1],A[1][0],A[1][1]]])
        G=mat(E.T*J*E)
        flatA=[A[0][0],A[0][1],A[1][0],A[1][1]]
        flatB=[B[0][0],B[0][1],B[1][0],B[1][1]]
        P=s.Matrix(4,4,[direct_born(rho,M,N) for M in flatA for N in flatB])
        YY=mat(G.inv()*P)
        result.append((rho,A,B,C,E,G,P,YY))
        fixtures.append({'id':f'physical_{i}', 'coefficient':matrix_repr(C),
            'alice_effects':[[matrix_repr(M) for M in block] for block in A],
            'bob_effects':[[matrix_repr(M) for M in block] for block in B],
            'coefficient_determinant':str(canon(C.det())), 'frame_determinant':str(canon(E.det()))})
    return result


def physical_suite():
    data=physical_fixtures()
    for i,(rho,A,B,C,E,G,P,YY) in enumerate(data):
        n=f'physical_{i}'
        check(n+'_density_hermitian',rho,rho.H)
        check(n+'_density_trace',s.trace(rho),s.Integer(1))
        check(n+'_density_pure',rho*rho,rho)
        require(n+'_full_schmidt_rank',C.det()!=0)
        verify_measurements(n+'_alice',A); verify_measurements(n+'_bob',B)
        require(n+'_invertible_effect_frames',E.det()!=0 and YY.det()!=0)
        check(n+'_frame_unit',E*u,e0)
        check(n+'_block_mass',(u.T*P*u)[0],s.Integer(1))
        for j,r in enumerate(rays):
            check(n+f'_null_{j}',(r.T*YY.T*G*YY*r)[0],s.Integer(0))
            require(n+f'_future_{j}',(E*YY*r)[0]>0)
        tab=table(rho,A,B)
        require(n+'_nonnegative_joint_probabilities',all(v.is_Rational and v>=0 for v in tab.values()))
        coeff=[[rays[0],rays[1],s.zeros(4,1)],[rays[2],rays[3],rays[4]]]
        for key,value in tab.items():
            x,y,a,b=key
            check(n+f'_full_table_{key}',value,(coeff[x][a].T*P*coeff[y][b])[0])
        U=su2(Q(1,5),Q(2,7),Q(1,3));V=su2(Q(-1,4),Q(2,5),Q(1,7))
        rr=rot(s.kronecker_product(U,V),rho)
        AA=[[rot(U,M) for M in m] for m in A];BB=[[rot(V,M) for M in m] for m in B]
        transformed=table(rr,AA,BB)
        require(n+'_local_unitary_invariance',transformed==tab)
        conjugated=table(rho.conjugate(),[[M.conjugate() for M in m] for m in A],
            [[M.conjugate() for M in m] for m in B])
        require(n+'_full_complex_conjugation_invariance',conjugated==tab)
        swap=s.zeros(4)
        for a,b in it.product(range(2),repeat=2):swap[2*b+a,2*a+b]=1
        swapped=table(swap*rho*swap.T,B,A)
        require(n+'_party_exchange_invariance',all(swapped[y,x,b,a]==v for (x,y,a,b),v in tab.items()))
    rho,A,B,C,*_=data[0]
    expected=direct_born(rho,A[1][1],B[1][1])
    reject('omitted_Bob_transpose',expected,s.trace(A[1][1]*C*B[1][1]*C.H),
        'Bell/Purification.lean','The physical coefficient state requires a transpose on Bob.')
    reject('transpose_instead_of_conjugate_transpose',expected,s.trace(A[1][1]*C*B[1][1].T*C.T),
        'Bell/Purification.lean','A real-only test cannot detect loss of complex conjugation.')
    return data


def filter_suite():
    # Full-rank, rational four-effect POVMs: H belongs to both real spans.
    tetra=[s.Matrix([1,Q(2,3),Q(2,3),Q(1,3)])/4,
           s.Matrix([1,Q(2,3),Q(-2,3),Q(-1,3)])/4,
           s.Matrix([1,Q(-2,3),Q(2,3),Q(-1,3)])/4,
           s.Matrix([1,Q(-2,3),Q(-2,3),Q(1,3)])/4]
    for case,r in enumerate([Q(1,100),Q(1,200),Q(1,500)]):
        U=su2(Q(1,3),Q(1,5),Q(-1,4))
        V=su2(Q(1,7),Q(-1,3),Q(1,2))
        A=[[rot(U,pauli(v)) for v in tetra], [rot(V,pauli(v)) for v in tetra]]
        B=residual_measurements(Q(2),Q(-3),su2(Q(1,3),Q(2,5),Q(1,7)))
        C=mat(su2(Q(1,4),Q(-1,5),Q(1,2))*s.diag(Q(3,5),Q(4,5)))
        rho=density(C)
        H=rot(U,Z)
        coeff=[]
        for measurement in A:
            E=s.Matrix.hstack(*[coordinates(M) for M in measurement])
            coeff.append(E.inv()*coordinates(H))
        hi=(1-r*r+2*r)/(1+r*r)
        lo=(1-r*r-2*r)/(1+r*r)
        eps=canon(hi*hi-1)
        require(f'filter_{case}_strict_epsilon',eps>0)
        branches=[]
        old=table(rho,A,B)
        for sign in (1,-1):
            K=rot(U,s.diag(hi,lo) if sign==1 else s.diag(lo,hi))
            check(f'filter_{case}_{sign}_square_root',K*K,I2+sign*eps*H)
            delta=s.kronecker_product(K,I2)
            q=canon(s.trace(delta*rho*delta.H))
            require(f'filter_{case}_{sign}_positive_branch_weight',q>0)
            state=mat(delta*rho*delta.H/q)
            invK=K.inv()
            M=[[mat((1+sign*eps*coeff[x][a])*invK.H*A[x][a]*invK)
                for a in range(4)] for x in range(2)]
            require(f'filter_{case}_{sign}_positive_scalars',
                all(1+sign*eps*coeff[x][a]>0 for x in range(2) for a in range(4)))
            verify_measurements(f'filter_{case}_{sign}',M)
            check(f'filter_{case}_{sign}_state_trace',s.trace(state),s.Integer(1))
            branch=table(state,M,B)
            for key,val in branch.items():
                x,y,a,b=key
                check(f'filter_{case}_{sign}_born_{key}',q*val,(1+sign*eps*coeff[x][a])*old[key])
            require(f'filter_{case}_{sign}_nontrivial_split',branch!=old)
            branches.append((q,branch))
        check(f'filter_{case}_weights_sum',branches[0][0]/2+branches[1][0]/2,s.Integer(1))
        require(f'filter_{case}_complete_shared_mixture',all(
            canon(branches[0][0]*branches[0][1][key]/2+branches[1][0]*branches[1][1][key]/2)==val
            for key,val in old.items()))
        key=next(k for k in old if canon((branches[0][1][k]+branches[1][1][k])/2-old[k])!=0)
        reject(f'filter_{case}_unweighted_average',old[key],(branches[0][1][key]+branches[1][1][key])/2,
            'Bell/CommonSpanFiltering.lean','The two weights are q_plus/2 and q_minus/2, not 1/2 each.')


def phi(v):
    a,b,c,d=v
    return s.Matrix([c*(a+d),d*(a+c),c*(b+d),d*(b+c)])


def variation(h):
    a,b,c,d=h;e=a+b+c+d
    return s.Matrix([[0,0,a,b],[0,0,c,d],[a,c,0,e],[b,d,e,0]])


def mass(P):return canon((u.T*P*u)[0])

def weighted(G,Y,lam):return canon(sum(lam[j]*(r.T*Y.T*G*Y*r)[0] for j,r in enumerate(rays)))

def incidence_suite():
    data=physical_fixtures()
    rng=random.Random(10621699161)
    detected=False
    for i,(_,A,B,C,E,G,P,YY) in enumerate(data):
        rows=s.Matrix.hstack(*[phi(YY*r) for r in rays])
        basis=rows.nullspace()
        require(f'incidence_{i}_nontrivial_multiplier_kernel',len(basis)>0)
        lam=basis[0]
        check(f'incidence_{i}_metric_stationarity',rows*lam,s.zeros(4,1))
        alpha=Q(i+3,7)
        def score(M):return canon(alpha*mass(M)-2*sum(lam[j]*(r.T*YY.T*M*r)[0] for j,r in enumerate(rays)))
        _,_,_,_,_,GG,PP,YN=data[(i+1)%len(data)]
        actual=score(PP)-score(P)
        target=weighted(GG,YN-YY,lam)
        check(f'incidence_{i}_finite_physical_score_gap',actual,target)
        check(f'incidence_{i}_metric_residual',weighted(GG-G,YY,lam),s.Integer(0))
        if target!=0 and not detected:
            reject('finite_gap_reversed_sign',actual,-target,'Bell/IncidenceAlgebra.lean',
                'The increasing-direction argument depends on the sign of the exact finite gap.')
            detected=True
        for trial in range(2):
            h=s.Matrix([rng.randint(-3,3) for _ in range(4)])
            H=variation(h)
            ZZ=s.Matrix(4,4,[Q(rng.randint(-3,3),5) for _ in range(16)])
            def constraints(t):
                Gt=G+t*H;Yt=YY+t*ZZ
                return s.Matrix([canon((r.T*Yt.T*Gt*Yt*r)[0]) for r in rays]+[mass(Gt*Yt)])
            # Exact derivative of a cubic from 4 exact evaluations (Richardson).
            derivative=(8*(constraints(1)-constraints(-1))-(constraints(2)-constraints(-2)))/12
            formula=s.Matrix([canon(2*(r.T*YY.T*G*ZZ*r)[0]+(r.T*YY.T*H*YY*r)[0]) for r in rays]
                +[mass(H*YY+G*ZZ)])
            check(f'incidence_{i}_{trial}_six_cubic_derivatives',derivative,formula)
            shift=-formula[5]
            corrected=ZZ+shift*YY
            check(f'incidence_{i}_{trial}_radial_normalization',mass(H*YY+G*corrected),s.Integer(0))
            for j,r in enumerate(rays):
                check(f'incidence_{i}_{trial}_radial_preserves_null_{j}',
                    2*(r.T*YY.T*G*corrected*r)[0]+(r.T*YY.T*H*YY*r)[0],formula[j])
            wrong=ZZ-mass(G*ZZ)*YY
            if mass(H*YY)!=0:
                reject(f'incidence_{i}_{trial}_dropped_metric_mass',s.Integer(0),mass(H*YY+G*wrong),
                    'Bell/IncidenceRank.lean','Normalizing only the W/frame term leaves a nonzero mass derivative.')
        # Genuine Gram right inverse with all ten symmetric entries independently populated.
        SS=s.Matrix(4,4,[Q(rng.randint(-4,4),7) for _ in range(16)])
        HH=SS+SS.T
        DD=mat(J*E.T.inv()*HH/2)
        direct=(mat((E+DD).T*J*(E+DD))-mat((E-DD).T*J*(E-DD)))/2
        check(f'incidence_{i}_gram_right_inverse',direct,HH)
        bad=mat(E.T.inv()*HH/2)
        reject(f'incidence_{i}_omitted_minkowski',HH,mat(bad.T*J*E+E.T*J*bad),
            'Bell/GramLift.lean','The right inverse must include the Minkowski matrix, not a Euclidean substitute.')
    require('finite_gap_mutation_nonvacuous',detected)


def vertices(vectors,sides):
    # Independent enumeration of every basic feasible support in this fixture.
    A=s.Matrix.hstack(*[s.Matrix([(-1 if side else 1)*x for x in v[:3]]+[v[0]])
        for v,side in zip(vectors,sides)])
    b=s.Matrix([0,0,0,1]);rank=A.rank();out={}
    for size in range(1,rank+1):
        for supp in it.combinations(range(len(vectors)),size):
            C=A[:,list(supp)]
            if C.rank()!=size or C.row_join(b).rank()!=size:continue
            w=list(C.gauss_jordan_solve(b)[0])
            if not all(t>0 for t in w):continue
            full=tuple(w[supp.index(i)] if i in supp else s.Integer(0) for i in range(len(vectors)))
            out[full]=supp
    return A,b,out


def circuit_suite():
    directions=[(1,0),(0,1),(-1,0),(0,-1),planar_pair(Q(2)),planar_pair(Q(-2))]
    scenarios={
      'ellipse_with_duplicate_labels':([0,1,2,3,4,0,1,2,3,5],[0]*5+[1]*5),
      'same_ray_duplicates':([4,4,4,4,4],[0,0,1,1,1]),
      'parallel_axes_interval':([0,2,0,2,0,2],[0,0,0,1,1,1]),
      'rank_one_repeated':([1,1,1,1],[0,0,1,1]),
    }
    catalogue=[]
    for name,(ids,sides) in scenarios.items():
        vectors=[s.Matrix([Q((i%3)+1,2),Q((i%3)+1,2)*directions[k][0],
            Q((i%3)+1,2)*directions[k][1],0]) for i,k in enumerate(ids)]
        A,b,vs=vertices(vectors,sides)
        require(name+'_nonempty_vertices',len(vs)>0,'finite_polytope_enumeration')
        counts={};timelike=0;null=0
        for vi,(w,supp) in enumerate(vs.items()):
            check(f'{name}_{vi}_balance_and_mass',A*s.Matrix(w),b,'finite_polytope_enumeration')
            sidecounts=tuple(sum(sides[i]==side for i in supp) for side in (0,1))
            require(f'{name}_{vi}_two_sided_support',1<=min(sidecounts) and max(sidecounts)<=2,
                'finite_polytope_enumeration')
            counts[str(sidecounts)]=counts.get(str(sidecounts),0)+1
            sums=[sum([w[i]*vectors[i] for i in supp if sides[i]==side],s.zeros(4,1)) for side in (0,1)]
            check(f'{name}_{vi}_same_sum',sums[0],sums[1],'finite_polytope_enumeration')
            Omega=pauli(sums[0]);det=canon(Omega.det())
            check(f'{name}_{vi}_trace_one',s.trace(Omega),s.Integer(1),'finite_polytope_enumeration')
            require(f'{name}_{vi}_Omega_positive',psd2(Omega),'finite_polytope_enumeration')
            if det>0:
                timelike+=1;inv=Omega.inv()
                # Algebraically equivalent to projector multiplication after any
                # whitening C with C C* = Omega, with no square-root numerics.
                for side in (0,1):
                    selected=[i for i in supp if sides[i]==side]
                    for i,j in it.product(selected,repeat=2):
                        R=w[i]*pauli(vectors[i]);S=w[j]*pauli(vectors[j])
                        check(f'{name}_{vi}_whitened_projector_{i}_{j}',R*inv*S,R if i==j else Z2,
                            'finite_polytope_enumeration')
            else:
                null+=1
                for i in supp:
                    R=w[i]*pauli(vectors[i])
                    check(f'{name}_{vi}_singular_collinearity_{i}',R,s.trace(R)*Omega,'finite_polytope_enumeration')
        catalogue.append({'id':name,'rays':[matrix_repr(v) for v in vectors],'side':sides,
            'constraint_rank':A.rank(),'number_of_vertices':len(vs),'support_patterns':counts,
            'timelike_common_sums':timelike,'singular_common_sums':null,
            'weights':[[str(x) for x in w] for w in vs]})
    (OUT/'circuit_catalogue.json').write_text(json.dumps(catalogue,indent=2)+'\n')


def maps_suite():
    # A genuinely nonlocal PVM strategy, with exact CHSH score 14/5.
    rho=s.zeros(4);rho[0,0]=rho[3,3]=Q(1,2);rho[0,3]=rho[3,0]=Q(1,2)
    U=su2(Q(1,3),Q(1,5),Q(1,7));V=su2(Q(-1,5),Q(1,4),Q(2,7))
    A0=[[P0,P1],[(I2+X)/2,(I2-X)/2]]
    B0=[[(I2+(3*Z+4*X)/5)/2,(I2-(3*Z+4*X)/5)/2],
        [(I2+(3*Z-4*X)/5)/2,(I2-(3*Z-4*X)/5)/2]]
    rho=rot(s.kronecker_product(U,V),rho)
    A=[[rot(U,M) for M in block] for block in A0]
    B=[[rot(V,M) for M in block] for block in B0]
    verify_measurements('map_alice',A,True);verify_measurements('map_bob',B,True)
    base=table(rho,A,B)
    def chsh(T):return canon(sum((1 if (x,y)!=(1,1) else -1)*(-1)**(a+b)*T[x,y,a,b]
        for x,y,a,b in it.product(range(2),repeat=4)))
    check('nonlocal_PVM_CHSH',chsh(base),Q(14,5))
    # Different output sets per input; collapsing maps create deterministic branches.
    sizesA=[3,4];sizesB=[4,2]
    mapA=[[(0,2),(1,1)],[(3,0),(2,3)]]
    mapB=[[(1,3),(0,0)],[(1,0),(0,1)]]
    rates=[Q(1,3),Q(2,5),Q(3,7),Q(4,9)]
    for boundary in (False,True):
        rr=rates[:] if not boundary else [Q(0),rates[1],Q(1),rates[3]]
        channelA=[s.zeros(m,2) for m in sizesA];channelB=[s.zeros(m,2) for m in sizesB]
        for x in range(2):
            for k in range(2):
                w=rr[x] if k==0 else 1-rr[x]
                z=rr[x+2] if k==0 else 1-rr[x+2]
                for a in range(2):channelA[x][mapA[x][k][a],a]+=w
                for b in range(2):channelB[x][mapB[x][k][b],b]+=z
        target={(x,y,a,b):canon(sum(channelA[x][a,c]*channelB[y][b,d]*base[x,y,c,d]
            for c,d in it.product(range(2),repeat=2)))
            for x,y in it.product(range(2),repeat=2) for a in range(sizesA[x]) for b in range(sizesB[y])}
        mixture={key:Q(0) for key in target};total=Q(0)
        for bits in it.product(range(2),repeat=4):
            w=s.prod(rr[j] if bits[j]==0 else 1-rr[j] for j in range(4));total+=w
            AA=[[sum([A[x][c] for c in range(2) if mapA[x][bits[x]][c]==a],Z2)
                for a in range(sizesA[x])] for x in range(2)]
            BB=[[sum([B[y][d] for d in range(2) if mapB[y][bits[y+2]][d]==b],Z2)
                for b in range(sizesB[y])] for y in range(2)]
            # Each label is positive, and all pairwise projector identities hold.
            # Count a complete branch as one certificate, not every matrix entry.
            require(f'map_{boundary}_{bits}_physical_PVM_branch',all(
                sum(M,Z2)==I2 and all(psd2(P) for P in M) and
                all(mat(P*Q)==(P if a==b else Z2) for a,P in enumerate(M) for b,Q in enumerate(M))
                for M in [*AA,*BB]))
            branch=table(rho,AA,BB)
            for key in target:mixture[key]+=w*branch[key]
        check(f'map_{boundary}_common_weights_sum',total,Q(1))
        require(f'map_{boundary}_complete_shared_selector',all(canon(mixture[k]-target[k])==0 for k in target))
        for x,y in it.product(range(2),repeat=2):
            check(f'map_{boundary}_{x}_{y}_normalization',sum(v for (xx,yy,_,_),v in target.items() if xx==x and yy==y),Q(1))
    local_scores=[]
    for aa in it.product(range(2),repeat=2):
        for bb in it.product(range(2),repeat=2):
            T={(x,y,a,b):Q(int(a==aa[x] and b==bb[y])) for x,y,a,b in it.product(range(2),repeat=4)}
            local_scores.append(chsh(T))
    require('complete_local_branches_CHSH_bound',max(local_scores)==2,'exhaustive_16_local_assignments')
    PR={(x,y,a,b):Q(1,2) if a^b==x*y else Q(0) for x,y,a,b in it.product(range(2),repeat=4)}
    check('pairwise_local_but_not_common_local_PR_score',chsh(PR),Q(4))
    reject('separate_mixtures_are_not_a_common_mixture',max(local_scores),chsh(PR),
        'Bell/ClassicalProduct.lean','Separate input-pair decompositions cannot replace one whole-strategy random variable.',
        kind='scope_control')
    # Padding an unused label by a zero COEFFICIENT, rather than pulling back
    # through the deterministic coarsening, changes the maximum of a Bell test.
    original_max=Q(-1);naive_padded_max=Q(0);correct_padded_max=Q(-1)
    check('Bell_coefficient_coarsening_padding',correct_padded_max,original_max)
    reject('naive_zero_coefficient_padding',original_max,naive_padded_max,
        'Bell/SmallOutputEncoding.lean','Unused effects may be zero; the extended functional must still use the coarsening map.',
        kind='interface_mutation')


def saddle_suite():
    """An exact high-rank coupled uphill path; NOT a POVM/PVM separation."""
    t=s.symbols('t',real=True)
    rho=s.zeros(4);rho[1,1]=rho[2,2]=Q(1,2);rho[1,2]=rho[2,1]=-Q(1,2)
    U=Q(3,5)*I2+4*s.I*X/5
    A=residual_measurements(Q(2),Q(-2),I2)
    # Actual heterogeneous (2,3)-by-(2,3) outputs, not a zero-coefficient third binary label.
    A[0]=A[0][:2];B=[[rot(U,M) for M in block] for block in A]
    v0=s.Matrix([0,1,-1,0])
    check('saddle_base_density_Gram',rho,v0*v0.H/2)
    check('saddle_base_density_trace',s.trace(rho),Q(1))
    check('saddle_base_density_purity',rho*rho,rho)
    check('saddle_Bob_base_unitary',U.H*U,I2)
    verify_measurements('saddle_base_Alice',A)
    verify_measurements('saddle_base_Bob',B)
    AA=[A[0][0],A[0][1],A[1][0],A[1][1]];BB=[B[0][0],B[0][1],B[1][0],B[1][1]]
    F=s.Matrix([[-Q(9,10),-2,Q(6,5),Q(2,5)],[-Q(2,25),-Q(9,10),Q(6,25),-Q(38,25)],
        [Q(6,25),Q(6,5),-Q(68,25),Q(14,25)],[-Q(38,25),Q(2,5),Q(14,25),Q(28,25)]])
    E=s.Matrix.hstack(*[coordinates(M) for M in AA]);G=mat(E.T*J*E)
    P=s.Matrix(4,4,[direct_born(rho,M,N) for M in AA for N in BB]);YY=mat(G.inv()*P)
    R=s.Matrix.hstack(*[phi(YY*r) for r in rays]);lam=s.Matrix([Q(1,4),Q(1,4),1,1,1])
    check('saddle_base_normalization',(u.T*P*u)[0],Q(1))
    require('saddle_base_invertible_frames',E.det()!=0 and YY.det()!=0)
    for j,r in enumerate(rays):
        check(f'saddle_base_null_constraint_{j}',(r.T*YY.T*G*YY*r)[0],Q(0))
        require(f'saddle_base_future_pairing_{j}',canon((r.T*YY.T*G*YY*u)[0])>0)
    require('saddle_metric_row_rank_is_three',R.rank()==3)
    check('saddle_strict_multiplier_kernel',R*lam,s.zeros(4,1))
    require('saddle_all_five_multipliers_positive',all(x>0 for x in lam))
    Lambda=sum([lam[j]*r*r.T for j,r in enumerate(rays)],s.zeros(4))
    check('saddle_stationary_score_coefficients',F,-2*YY*Lambda)
    Bell=mat(sum([F[i,j]*s.kronecker_product(AA[i],BB[j]) for i,j in it.product(range(4),repeat=2)],s.zeros(4)))
    v1=s.Matrix([1,0,0,-1]);v2=s.Matrix([1,-1,-1,1]);v3=s.Matrix([1,1,1,1])
    check('saddle_negative_Bell_operator_Gram',-Bell,v1*v1.T/2+Q(5,16)*v2*v2.T+Q(23,64)*v3*v3.T)
    check('saddle_base_state_globally_optimal_with_fixed_measurements',s.trace(rho*Bell),Q(0))
    duals=[]
    K_A=[mat(sum([F[i,j]*(s.trace(BB[j])*I2-BB[j])/2 for j in range(4)],Z2)) for i in range(4)]
    K_B=[mat(sum([F[i,j]*(s.trace(AA[i])*I2-AA[i])/2 for i in range(4)],Z2)) for j in range(4)]
    for side,MM,KK in [('Alice',A,K_A),('Bob',B,K_B)]:
        for x in (0,1):
            Ks=KK[2*x:2*x+2]+([Z2] if x==1 else [])
            Gamma=mat(sum([K*M for K,M in zip(Ks,MM[x])],Z2))
            for j,(K,M) in enumerate(zip(Ks,MM[x])):
                slack=mat(Gamma-K)
                require(f'saddle_{side}_{x}_{j}_dual_feasible',psd2(slack))
                check(f'saddle_{side}_{x}_{j}_complementary_slackness',slack*M,Z2)
            duals.append({'party':side,'input':x,'Gamma':matrix_repr(Gamma),
                'scores':[matrix_repr(K) for K in Ks]})
    # Exact rational physical path discovered using a floating-point Hessian,
    # then reconstructed/checked here with NO floating-point arithmetic.
    S=I2-3*s.I*t*Ypauli/10
    W=s.kronecker_product(S,I2)
    Rho=mat(W*rho*W.H/(1+9*t*t/100))
    UA=su2(s.Integer(0),-t/10,s.Integer(0))
    Ap=[A[0],[rot(UA,M) for M in A[1]]]
    p,q=2-t,-2-t;pts=[(1,0),planar_pair(p),planar_pair(q)]
    coeff=s.Matrix([[1,1,1],[z[0] for z in pts],[z[1] for z in pts]])
    ww=mat(coeff.inv()*s.Matrix([1,0,0]))
    Bp=[B[0],[rot(U,ww[j]*(I2+pts[j][0]*X+pts[j][1]*Ypauli)) for j in range(3)]]
    check('saddle_path_state_norm',s.trace(Rho),Q(1),'symbolic_rational_identity')
    check('saddle_path_filter_norm',S.H*S,(1+9*t*t/100)*I2,'symbolic_rational_identity')
    check('saddle_path_Alice_unitary',UA.H*UA,I2,'symbolic_rational_identity')
    check('saddle_path_Alice_normalization',sum(Ap[1],Z2),I2,'symbolic_rational_identity')
    check('saddle_path_Bob_normalization',sum(Bp[1],Z2),I2,'symbolic_rational_identity')
    expected_weights=s.Matrix([(3-t*t)/(2*(4-t*t)),((t-2)**2+1)/(8*(2-t)),((t+2)**2+1)/(8*(2+t))])
    check('saddle_path_positive_weight_form',ww,expected_weights,'symbolic_rational_identity')
    for j,(xx,yy) in enumerate(pts):
        check(f'saddle_path_unit_planar_direction_{j}',xx*xx+yy*yy,Q(1),'symbolic_rational_identity')
    # Exact positivity certificates under -1/2 <= t <= 1/2.  Every remainder
    # below is nonnegative on that interval.  These identities plus their
    # listed elementary sign conditions are independently inspectable.
    interval_certificates=[
        ('weight0_numerator',3-t*t,Q(11,4),Q(1,4)-t*t),
        ('weight0_denominator_factor',4-t*t,Q(15,4),Q(1,4)-t*t),
        ('weight1_denominator_factor',2-t,Q(3,2),Q(1,2)-t),
        ('weight2_denominator_factor',2+t,Q(3,2),Q(1,2)+t),
        ('Alice_unitary_denominator',100+t*t,Q(100),t*t),
        ('state_normalization_denominator',100+9*t*t,Q(100),9*t*t),
        ('weight1_numerator',(t-2)**2+1,Q(1),(t-2)**2),
        ('weight2_numerator',(t+2)**2+1,Q(1),(t+2)**2),
    ]
    for name,term,lower_bound,remainder in interval_certificates:
        check('saddle_interval_'+name,term,lower_bound+remainder,'symbolic_polynomial_identity')
        require('saddle_interval_'+name+'_positive_lower_bound',lower_bound>0)
    for k in range(3):
        check(f'saddle_path_Bob_rank_one_{k}',Bp[1][k].det(),Q(0),'symbolic_rational_identity')
    AA2=[Ap[0][0],Ap[0][1],Ap[1][0],Ap[1][1]];BB2=[Bp[0][0],Bp[0][1],Bp[1][0],Bp[1][1]]
    f=canon(sum(F[i,j]*s.trace(Rho*s.kronecker_product(AA2[i],BB2[j])) for i,j in it.product(range(4),repeat=2)))
    N=850000-955000*t*t-58595*t**4+252*t**6
    denominator=40*(4-t*t)*(t*t+100)**2*(9*t*t+100)
    target=t*t*N/denominator
    check('saddle_entire_physical_path_score',f,target,'symbolic_rational_identity')
    lower=Q(9721405,16)
    check('saddle_interval_positivity_certificate',N,
        lower+(Q(1,4)-t*t)*(955000+58595*(Q(1,4)+t*t))+252*t**6,'symbolic_polynomial_identity')
    require('saddle_positive_numerator_lower_bound',lower>0)
    numerator_upper=Q(850000)+Q(252,64)
    denominator_lower=40*Q(15,4)*100**2*100
    path_score_upper=Q(1,4)*numerator_upper/denominator_lower
    check('saddle_interval_numerator_upper_certificate',numerator_upper-N,
        955000*t*t+58595*t**4+252*(Q(1,64)-t**6),'symbolic_polynomial_identity')
    require('saddle_entire_interval_below_deterministic_PVM',0<path_score_upper<Q(3,10))
    check('saddle_stationary_path_first_derivative',s.diff(f,t).subs(t,0),Q(0),'symbolic_rational_identity')
    check('saddle_positive_path_second_derivative',s.diff(f,t,2).subs(t,0),Q(17,1600),'symbolic_rational_identity')
    values=[]
    for tt in [Q(-1,2),Q(-1,10),Q(-1,100),Q(1,100),Q(1,10),Q(1,2)]:
        RR=mat(Rho.subs(t,tt));AM=[[mat(M.subs(t,tt)) for M in block] for block in Ap];BM=[[mat(M.subs(t,tt)) for M in block] for block in Bp]
        verify_measurements(f'saddle_at_{tt}_Alice',AM);verify_measurements(f'saddle_at_{tt}_Bob',BM)
        check(f'saddle_at_{tt}_state_purity',RR*RR,RR)
        direct=canon(sum(F[i,j]*direct_born(RR,M,Qm)
            for i,M in enumerate([AM[0][0],AM[0][1],AM[1][0],AM[1][1]])
            for j,Qm in enumerate([BM[0][0],BM[0][1],BM[1][0],BM[1][1]])))
        check(f'saddle_at_{tt}_direct_score',direct,f.subs(t,tt))
        require(f'saddle_at_{tt}_strict_improvement',direct>0)
        EA=s.Matrix.hstack(*[coordinates(M) for M in [AM[0][0],AM[0][1],AM[1][0],AM[1][1]]])
        GT=mat(EA.T*J*EA)
        PP=s.Matrix(4,4,[direct_born(RR,M,N)
            for M in [AM[0][0],AM[0][1],AM[1][0],AM[1][1]]
            for N in [BM[0][0],BM[0][1],BM[1][0],BM[1][1]]])
        YT=mat(GT.inv()*PP)
        gap=canon(sum(lam[j]*((YT-YY)*r).dot(GT*((YT-YY)*r)) for j,r in enumerate(rays)))
        check(f'saddle_at_{tt}_finite_incidence_gap',gap,direct)
        values.append({'t':str(tt),'direct_born_score':str(direct)})
    reject('high_rank_test_requires_coupled_moves',Q(0),f.subs(t,Q(1,2)),
        'Bell/IncidenceRank.lean','Separate state/measurement optimization is not a test for absence of coupled uphill curves.',
        kind='scope_control')
    # A positive saddle path is NOT evidence of a POVM/PVM separation: a
    # deterministic PVM strategy already scores 3/10 on this same functional.
    label_indices=[[0,1],[2,3,None]]
    def deterministic_score(aa,bb):
        return sum(F[label_indices[x][aa[x]],label_indices[y][bb[y]]]
            for x,y in it.product(range(2),repeat=2)
            if label_indices[x][aa[x]] is not None and label_indices[y][bb[y]] is not None)
    local_scores=[(aa,bb,deterministic_score(aa,bb))
        for aa in it.product(range(2),range(3)) for bb in it.product(range(2),range(3))]
    witness_score=deterministic_score((0,0),(0,1))
    check('saddle_deterministic_PVM_witness_score',witness_score,Q(3,10))
    require('saddle_exact_36_local_assignments_maximum',max(z for _,_,z in local_scores)==Q(3,10),
        'exhaustive_36_local_assignments')
    require('saddle_no_separation_in_test_values',all(canon(f.subs(t,tt))<witness_score
        for tt in [Q(-1,2),Q(-1,10),Q(-1,100),Q(1,100),Q(1,10),Q(1,2)]))
    cert={'status':'exact_symbolic_and_rational_checks_passed','architecture':[[2,3],[2,3]],
        'Bell_first_four_effect_coefficients':matrix_repr(F),'base_density':matrix_repr(rho),
        'base_alice':[[matrix_repr(M) for M in block] for block in A],
        'base_bob':[[matrix_repr(M) for M in block] for block in B],
        'metric':matrix_repr(G),'frame_Y':matrix_repr(YY),'metric_row_rank':3,
        'positive_multipliers':[str(x) for x in lam],'fixed_measurement_Bell_operator':matrix_repr(Bell),
        'measurement_duals':duals,'path_state_filter':matrix_repr(S),'path_Alice_unitary':matrix_repr(UA),
        'path_Bob_planar_parameters':['2-t','-2-t'],
        'path_score':str(target),'score_numerator_positive_lower_bound':str(lower),
        'valid_interval':'-1/2 <= t <= 1/2','strict_improvement_interval':'0 < |t| <= 1/2',
        'first_derivative_at_zero':'0','second_derivative_at_zero':'17/1600',
        'positive_interval_factor_certificates':[{'factor':name,'expression':str(term),
            'positive_lower_bound':str(lb),'nonnegative_remainder':str(rem)}
            for name,term,lb,rem in interval_certificates],
        'interval_sign_assumptions':['1/4-t^2 >= 0','1/2-t >= 0','1/2+t >= 0','all real squares >= 0'],
        'deterministic_PVM_comparison':{'Alice_outputs':[0,0],'Bob_outputs':[0,1],
            'score':'3/10','local_assignments_enumerated':36,
            'entire_interval_score_upper_bound':str(path_score_upper),
            'numerator_upper_bound':str(numerator_upper),'denominator_lower_bound':str(denominator_lower),
            'meaning':'Exceeds the path score on the entire certified interval; this is not a separation certificate.'},
        'exact_finite_values':values,'discovery':'Floating-point Hessian exploration; all claimed identities independently recomputed exactly.',
        'kernel_checked':False,'does_not_claim':'No POVM/PVM separation or arbitrary-point saddle theorem.'}
    (OUT/'rank_three_saddle_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite',choices=['physical','filter','incidence','circuit','maps','saddle','all'],default='all')
    args=parser.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    started=time.time()
    report={'status':'in_progress','suite':args.suite,'lean_invoked':False,'kernel_checked':False,
        'scope':'Exact rational/algebraic fixtures; no analytic, arbitrary-input or Lean proof certification.'}
    path=OUT/f'{args.suite}.json';path.write_text(json.dumps(report,indent=2)+'\n')
    try:
        for name,fn in [('physical',physical_suite),('filter',filter_suite),('incidence',incidence_suite),('circuit',circuit_suite),('maps',maps_suite),('saddle',saddle_suite)]:
            if args.suite in (name,'all'):
                before=len(records);fn();print(f'{name}: {len(records)-before} exact checks passed',flush=True)
        report.update(status='passed',checks=records,exact_check_count=len(records),
            negative_controls=negative_controls,negative_control_count=len(negative_controls),
            negative_controls_by_kind={kind:sum(c['kind']==kind for c in negative_controls)
                for kind in sorted({c['kind'] for c in negative_controls})},
            fixture_count=len({f['id'] for f in fixtures}),source_module_sha256={p.relative_to(ROOT).as_posix():
                hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'Bell').glob('*.lean')) if p.name!='Audit.lean'},
            checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            tolerance_used=False)
        unique_fixtures=list({f['id']:f for f in fixtures}.values())
        (OUT/f'{args.suite}_fixtures.json').write_text(json.dumps(unique_fixtures,indent=2)+'\n')
    except BaseException as exc:
        report.update(status='failed',error=str(exc),completed_exact_checks=len(records))
        raise
    finally:
        report['elapsed_seconds']=time.time()-started;path.write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS: {len(records)} exact checks; {len(negative_controls)} exact controls distinguished. NOT Lean verification.')

if __name__=='__main__':main()
