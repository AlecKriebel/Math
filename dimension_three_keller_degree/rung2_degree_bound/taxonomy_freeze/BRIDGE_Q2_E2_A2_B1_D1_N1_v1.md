# Certified post-freeze bridge for `Q2-E2-A2-B1-D1-N1`

**Candidate recorded (UTC):** 2026-07-26T00:01:30Z.

**Certified (UTC):** 2026-07-26T00:31:14Z.

**Coverage verdict:** **PASS.**  The clean-room hostile replay is
`audit_bridge_q2_e2_v1/REPORT.md`; its dependency-free exact checker ends
with `AUDIT_BRIDGE_Q2_E2_STRICT_PASS_D9347B`.  The row is promoted in
`CERTIFIED_EXCLUSION_STATUS.md`.

This bridge supersedes the no-go verdict in
`READINESS_Q2_E2_A2_B1_D1_N1.md`.  That audit correctly found that the old
lower theorem covered only the marked-equal locus \(h=s\).  The missing
marked-distinct quotient has since been frozen as thirteen stable strata,
and exact lower calculations now route all thirteen.

This work was produced with substantial AI assistance and is not peer
reviewed.  Exact checks verify encoded algebra and coverage assertions;
they are evidence, not review by the mathematical community.

## 1. Frozen scope and target normalization

The inclusive frozen row has tuple
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)
=(2,2,2,1,1,1).
\]
The canonical-pencil factorization is
\[
H_4=hA(p,q),
\]
where \(h\) is quadratic, \(p,q\) are coprime quadratic generators of a
minimal pencil, and \(A\) is a basepoint-free binary triple of degree one.
Writing
\[
A(u,v)=\mathbf a u+\mathbf b v,
\qquad \mathbf a,\mathbf b\in\mathbb C^3,
\]
basepoint freeness makes \(\mathbf a,\mathbf b\) independent.  Completing
them to a target basis gives, pointwise,
\[
\boxed{H_4=(hp,hq,0).}                               \tag{1}
\]

This target normalization depends only on a nonzero rank-two target minor.
It imposes no condition on \(H_3,H_2,L\), and source and target linear
changes preserve the Keller property and invertibility of the linear part.

For frozen coefficient pivots `C00`--`C29`, choose the lexicographically
first nonzero \(2\times2\) target-rank minor and apply (1).  For
`C30`--`C44`, the first two target components are zero, so
\(\operatorname{rank}JH_4\le1\); these fifteen strata are empty in this
rank-two row.  Thus every nonempty frozen coefficient-pivot stratum reaches
(1), without division by its first nonzero coefficient.

## 2. Horizontal components and the all-vertical frontier

Factor \(h\) into prime components.  If a component is horizontal for the
minimal pencil, the hostile-audited fixed-divisor verticality theorem gives
\[
4v_f(G)=3v_f(h),\qquad G=(H_3)_3,
\]
and forces \(G=0\).  The third target component then has degree at most two,
so the unconditional quadratic-component exit makes the map an
automorphism.

If every component of \(h\) is vertical, the hostile-audited all-vertical
top theorem excludes the genuine square-times-line and split-member shapes.
Its exact remaining frontier is
\[
\boxed{
H_4=(h^2,hs,0),\qquad
s=\ell^2\text{ is the unique double member},\qquad
G=\ell r,\quad [r]\in\mathbb P\langle h,s\rangle .
}                                                     \tag{2}
\]
If \(G=0\), the quadratic-component exit again applies.  It remains only to
route the nonzero companion in (2).

The ordered configuration
\[
\bigl(\langle h,s\rangle;[s],[h],[r]\bigr)
\]
has two disjoint intrinsic loci: \(h=s\) and \(h\ne s\).

## 3. Marked-equal locus \(h=s\)

The corrected theorem
`../fixed_divisor_e2_quadratic_pencils/NOTE.md` has exactly this scope.
There are two canonical pencil types,
\[
\langle x^2,yz\rangle,\qquad
\langle x^2,y^2+xz\rangle,
\]
and the marked-pair stabilizer leaves two nonzero companion orbits:
\[
G=xq,\qquad G=x^3.
\]
The mixed-companion verifier and the two triple-companion packages exclude
all four combinations.  Their SymPy calculations, independent PARI/GP
reconstructions, hostile reports, and fail-closed tests were retained before
the global freeze.  No statement from that package is used on \(h\ne s\).

## 4. Marked-distinct locus \(h\ne s\)

The immutable internal taxonomy
`FROZEN_Q2_E2_MARKED_COMPANION_v1.md` and its freeze certificate give
exactly thirteen stable strata:
\[
\boxed{4+5+4=13}.
\]
The middle family contains a genuine projective modulus; it is not replaced
by a finite list.

### 4.1 Frozen route table

| Marked pair | Companion suffix | Lower route |
|---|---|---|
| `MD-P21-HR2` | `C0` | quadratic-component exit |
| `MD-P21-HR2` | `CH` | endpoint closure, RT-reducible/H |
| `MD-P21-HR2` | `CS` | endpoint closure, RT-reducible/S |
| `MD-P21-HR2` | `CO` | discrete CO closure, HR2_CO |
| `MD-P21-HSM` | `C0` | quadratic-component exit |
| `MD-P21-HSM` | `CH` | endpoint closure, RT-smooth/H |
| `MD-P21-HSM` | `CT` | finite nonzero uniform obstruction, \(k=-1\) |
| `MD-P21-HSM` | `CS` | endpoint closure, RT-smooth/S |
| `MD-P21-HSM` | `CTAU` | finite nonzero uniform obstruction, \(k\ne0,-1\) |
| `MD-P3-HSM` | `C0` | quadratic-component exit |
| `MD-P3-HSM` | `CH` | endpoint closure, RO-smooth/H |
| `MD-P3-HSM` | `CS` | endpoint closure, RO-smooth/S |
| `MD-P3-HSM` | `CO` | discrete CO closure, P3_CO |

The three `C0` routes are immediate because \(H_{4,3}=H_{3,3}=0\).
The other ten routes are described next.

### 4.2 The projective middle family

Put
\[
h=x^2+yz,\qquad s=x^2,\qquad
r_{[u:v]}=uh+vs.
\]
On the finite chart \(u=1\), write \(k=v/u\).  The released complete
\(E_7\) quotient for every \(k\ne0\) is
\[
H_3=(Ax^3,Bx^3,x(h+ks)),\qquad (H_2)_3=Tx^2.
\]
Two coprime pivot charts cover every \(k\ne0\); the lower proof itself uses
only the divisor \(k=0\).

The division-free \(E_6\) chain forces
\[
a_1=a_2=a_3=a_5=b_1=b_2=b_3=b_5=\ell_7=\ell_8=0.
\]
Six literal \(E_5\) coefficients then force
\[
\ell_1=\ell_2=\ell_4=\ell_5=0.
\]
Hence \(L\) has only its first column and \(\det L=0\).  This excludes the
entire punctured `CTAU` family and its finite `CT` boundary \(k=-1\).
The omitted chart \(u=0\) is exactly `CS`, and \(v=0\) is exactly `CH`;
both are rebuilt from their endpoint normal forms below.

The exact SymPy and independent PARI/GP reconstructions are in
`../fixed_divisor_e2_quadratic_pencils/marked_h_distinct/quartic_survivor_search/`.

### 4.3 The six endpoint strata

The released endpoint package proves that its six \(E_7\) normal forms are
complete modulo two target shears and three source translations.  Its exact
\(E_6\) compatibility ideals first reduce the normal parameters.

For the three `H` endpoints, field-valued \(E_6\) solutions have
\[
E=F=0,\qquad AC=AD=0.
\]
On \(A=0\), global polynomial \(E_5\) syzygies force \(C=D=0\);
on \(A\ne0\), this already follows at \(E_6\).  The rank-two-pencil
endpoints then force \(\det L=0\) at \(E_5\), including the fresh \(A=0\)
boundary.

For the rank-one-pencil `H` endpoint, all \(A\ne0\) and \(T=0\) branches
again end at \(E_5\).  The unique sharp branch
\[
A=C=D=E=F=0,\qquad T\ne0
\]
survives through \(E_5\).  After the complete \(E_6/E_5\) solve, two
literal \(E_4\) coefficients are
\[
-8\ell_8^2,\qquad 4\ell_7^2\quad\text{after }\ell_8=0.
\]
Thus \(\ell_8=\ell_7=0\), while the displayed determinant is divisible by
\(\ell_7\).  This closes the sharp branch without assuming a lower
coefficient nonzero.

For the two rank-two-pencil `S` endpoints, \(E_6\) gives \(C=D=0\) and
\(E_5\) forces a singular \(L\).  For the rank-one-pencil `S` endpoint,
\(E_6\) gives \(D=0\), a global \(E_5\) syzygy gives \(C^3=0\), and fresh
\(A\ne0\) and \(A=0\) solves both force \(\det L=0\).

The exact exhaustive branch verifier is
`../fixed_divisor_e2_quadratic_pencils/marked_h_distinct/endpoint_closure/verify_endpoint_closure_sympy.py`.
The independent PARI/GP endpoint replay is in
`../fixed_divisor_e2_quadratic_pencils/marked_h_distinct/quartic_survivor_search/`
and is attached by the clean-room bridge report.

### 4.4 The two discrete `CO` strata

For
\[
(h,r)=(yz,x^2+yz)
\]
the raw \(E_7\) matrix has rank \(18\), and a complete three-dimensional
normal complement is
\[
(x^3,0,0),\quad(0,x^3,0),\quad(0,0,x^2).
\]
The \(E_6\) and \(E_5\) matrices have constant ranks \(10\) and \(4\);
the complete solves force \(\det L=0\).

For
\[
(h,r)=(y^2+xz,x^2+y^2+xz)
\]
the complete normal complement is
\[
(x^3,0,0),\quad(0,x^3,0),\quad
(2z(y^2+xz),x^2z,xz).
\]
The last normal parameter \(\rho\) gives an \(E_5\) pivot proportional to
\(\rho^2\).  The \(\rho\ne0\) solve forces the second column of \(L\) to
vanish; a fresh \(\rho=0\) solve forces both remaining off-axis columns to
vanish.  Thus both charts have \(\det L=0\).

The complete raw-\(E_7\) quotient and lower solves are reconstructed in
`../fixed_divisor_e2_quadratic_pencils/marked_h_distinct/co_closure/verify_co_closure_sympy.py`.
The clean-room replay independently reconstructs both quotients and lower
exits with a separate dependency-free exact engine.

## 5. Exhaustiveness

Every point of `C00`--`C29` reaches (1).  The horizontal/all-vertical split
is exhaustive.  The all-vertical theorem leaves exactly (2).  The zero
companion exits.  For a nonzero companion:

1. \(h=s\) is covered by the corrected marked-equal theorem;
2. \(h\ne s\) is one of the thirteen frozen internal strata, each appearing
   exactly once in the route table.

The projective boundaries \(u=0,v=0,u+v=0\) are respectively `CS`, `CH`,
and `CT`; none is obtained by specializing a localized solve.  All newly
encountered lower pivots have either been covered by a second coprime pivot
or rebuilt as a fresh boundary solve.

Therefore the certified bridge has no uncovered leading shape,
incidence leaf, companion orbit, projective boundary, or lower pivot
divisor in its declared scope.  The hostile replay also enforces the
distinction between the three zero-companion automorphism exits and the
ten nonzero marked-distinct determinant contradictions.
