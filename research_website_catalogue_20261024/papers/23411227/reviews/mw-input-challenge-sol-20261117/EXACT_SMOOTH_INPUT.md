# Exact smooth-curve MW input check

This is a bounded check of the MW input required by the native fivefold note, not a new theorem for the full note. General weighted Abban–Zhuang and valuative polystability machinery are accepted inputs. All calculations below are written deductions; no scientific program was executed.

## Geometry, filtration and canonical sign

Write H=Q∩{u=0}. The two diagonal forms on P3 have distinct eigenvalues. A dependent pair of gradients on their common zero locus forces at most one coordinate to be nonzero, contradicting sum x_i²=0. Thus C is smooth. On the smooth quadric H, C has class (2,2), is connected, and has genus one. This is precisely MW family 2.23(a), which §3.1 states for any such smooth C, without an additional genericity condition.

MW pp.10–11 gives the point action t·u=t^(−1)u and the ord_E degeneration to Z=Bl_C Q0. In the explicit diagonal example its inverse pullback produces t²u²+sum x_i², exactly the native family. The exponent two in the equation does not multiply the primitive divisorial valuation: locally u=s_loc*q with E={s_loc=0}, and ord_E(s_loc)=1.

The raw anticanonical section order k can also be checked without the degree-one Okounkov-body assertion. In the central associated grading, write the ideal of C as (u,q). For 0≤k≤m, its k-th piece has a factor u^k*q^(m−k) and moving restriction O_H(m+k,m+k). After substituting u=s_loc*q and removing the exceptional factor q^m this becomes s_loc^k times that complete moving series. For m≤k≤3m the moving restriction is O_H(3m−k,3m−k), with fixed factor q^(k−m). Thus the refined normalized series, writing z=k/m−1, is

    z∈[−1,0]: O_H(2+z,2+z);
    z∈[0,2]:  O_H(2−z,2−z)+z*C.

These are precisely MW p.14. Their dimensions have leading coefficient d(z)², where d(z)=2−|z|. Consequently the unnormalized DH density is d(z)² dz, not a density depending on a selected tangent flag. Its total mass is 7/3+8/3=5. Since A_V(E)=1, the canonical coordinate is z=k/m−1. The canonical weight function is g(z)=exp(−a*z), with no sign or scale change.

The exact moment is M(a)=∫_[−1,2] z*g(z)*d(z)² dz. One has M(0)=5/12, M'(a)=−∫z²*g*d²<0, and a fixed negative subinterval makes M(a)<0 for sufficiently large a. Hence the positive solution a is unique. The raw expected E-order is

    S^g(R;E)=v_g^(−1)∫(z+1)*g(z)*d(z)² dz=1,

where v_g=∫g*d². This checks the plt-divisor equality needed in MW Theorem 3.2. If the integration variable α in the final p.12 display denotes the shifted canonical coordinate, the raw-order function there is α+1, not α. The literal shifted first moment is zero; this notational issue is not silently used as a valid identity.

## An exact scalar replacing the printed decimals

Put

    q=(2*v_g)^(−1)∫g(z)*d(z)³ dz,
    r=v_g^(−1)∫_[0,2] z*g(z)*d(z)² dz.

The zero moment gives equal positive and negative first moments, so q=1−r. Positivity gives 0<q<1. The independent read-only local challenge supplied the following useful strengthening, which was then checked directly here:

    (2q−1)*v_g=∫_[−1,2] g*d²*(d−1).

On [−1,0], g≥1 and the integrand without g is nonnegative, so that part is at least ∫_1^2 d²(d−1) dd=17/12. The part on [0,1] is nonnegative. On [1,2], g≤1 and d−1≤0, so that part is at least −∫_0^1 d²(1−d) dd=−1/12. Hence the whole expression is positive, and

    1/2<q<1.

No approximation to a, q, or a local delta is used below.

## Complete local smooth cases

For every slice, write L=d(z). The moving series is the full monomial square 0≤i,j≤L. Positive z additionally contributes the fixed divisor z*C. A ruling has discrepancy one and expected moving order L/2. The ordinary point blowup has discrepancy two and expected moving order L; the (2,1) weighted point blowup has discrepancy three and expected moving order 3L/2.

If p is outside C, refine by either ruling through p. Both the ruling expected order and the subsequent curve-point expected order are q. The flag bound is therefore 1/q>1.

If p lies on smooth C and neither ruling is tangent, use the ordinary blowup. Its expected order is 2q+r=1+q. On the exceptional P1 all point discrepancies are one. Its induced curve expected orders are

    ruling points: q, q;
    strict-curve point: 2q/3+r=1−q/3;
    general point: 2q/3.

For verification, at fixed L the ordinary slice length is min(t,2L−t), 0≤t≤2L. Integrating half its square gives L³/3; dividing by v_g produces 2q/3. A ruling-point fixed term adds L³/6 before normalization, producing q. The curve point receives the fixed contribution r. Thus weighted AZ gives the exact sufficient lower bound

    min{2/(1+q), 1/q, 1/(1−q/3), 3/(2q)}>1.

At a smooth ruling tangency the ordinary flag would merge the curve and ruling points, producing expected order q+r=1; that flag alone does not supply the strict margin. The weighted blowup is essential in this case.

Let l1={x=0} be the tangent ruling, l2={y=0} the other ruling, and ord_F(x)=2, ord_F(y)=1. Smoothness and C·l1=2 force a local leading equation x+κ*y² with κ≠0. The fixed curve multiplicity is exactly two. Hence S^g(W;F)=3q+2r=2+q, while A_H(F)=3.

The moving slice is 2i+j=t. Its coarse exceptional-curve moving degree is

    ell(t)=t/2                 for 0≤t≤L,
           L/2                 for L≤t≤2L,
           (3L−t)/2            for 2L≤t≤3L.

The two coordinate fixed parts are (t−L)_+/2 at p1 and (t−2L)_+/2 at p2. Direct elementary integrations give

    (1/2)∫ell² dt=5L³/24;
    ∫((t−L)_+/2)*ell dt=7L³/24;
    ∫((t−2L)_+/2)*ell dt=L³/24;
    ∫ell dt=L².

Therefore the exact induced expected orders are q at p1, q/2 at p2, 5q/12+r=1−7q/12 at the strict-curve point p3, and 5q/12 at a general point.

The weighted-blowup charts are x=v*y² and (x,y)=(z²,z*w)/{±1}. The unique surface quotient point on F is p2=tilde(l2)∩F. Thus Diff_F(0)=(1/2)*p2; p1, p3 and general points have discrepancy one, while p2 has discrepancy 1/2. The actual weighted AZ ratios are

    3/(2+q),  1/q,  (1/2)/(q/2)=1/q,
    1/(1−7q/12),  12/(5q),

all strictly greater than one. In particular the printed extra point p0 must not be treated as distinct from p2.

Each smooth C has no ruling component. Each ruling intersects C in degree two, so a smooth ruling tangency has contact exactly two. A smooth tangent direction cannot be both transverse ruling directions. Thus the cases above cover every point of H for every smooth (2,2) C.

## Uniform strict bound and the polystability input

Using 1/2<q<1, every ratio just listed, including the nontangent and outside-C ratios, is at least 3/(2+q). For example:

    2/(1+q)≥3/(2+q)  iff q≤1;
    1/q≥3/(2+q)      iff q≤1;
    1/(1−q/3)≥3/(2+q) iff q≥1/2;
    1/(1−7q/12)≥3/(2+q) iff q≥4/11.

The remaining general-point inequalities are weaker consequences of 0<q<1. Hence

    delta^g(H;W) ≥ 3/(2+q) > 1.

For the actual use of weighted AZ, E=H is a smooth divisor away from the cone vertex, with discrepancy one; (Z,H) is plt because Z is klt elsewhere. The ordinary and weighted extractions used above are plt-type over the smooth surface H; the weighted different is included explicitly. The central torus fixes H pointwise, so these refinements and filtrations are invariant. Their degree ranges are bounded, and their full moving series and fixed parts were checked explicitly.

MW Theorem 3.2 uses this strict threshold, S^g(R;H)=A(H)=1, and its cited valuative/torus reduction: equality valuations outside the one-dimensional torus would descend to the refined surface series, where strict delta forbids equality. Smooth C has finite automorphism stabilizer on H (an elliptic curve preserving the degree-four polarization has finite such automorphisms), so no generic-C hypothesis hides in the torus rank. Under that established reduction and weighted AZ machinery, the required weighted K-polystability input is supported. This paragraph is not a fresh proof of the external general reduction, the upstream analytic existence theorem, or the native product/global chain.

## Precisely retained primary limitations

Theorem 3.2 on the actual p.12 PDF correctly prints the fraction 3/2.782066. A separated numerator in extracted text is not a primary error. Remark 3.6 does print the nontangent local delta as approximately 1/q. That is inconsistent with the ordinary exceptional divisor's upper bound delta_p≤2/(1+q)<1/q, for all q<1. The needed strict bound is nevertheless supplied by the explicit ratios above.

The actual p.19 PDF explicitly treats p0 as separate from p2, but its own weighted intersection data and the displayed quotient chart force p0=p2. The correct combined pair is (A,S)=(1/2,q/2), still giving 1/q>1. No source or primary was altered. These imprecisions do not leave an unresolved strict-margin defect in the smooth input. No assertion is made that every printed quantitative estimate, singular-C statement, or unrelated upstream theorem has been independently verified.
