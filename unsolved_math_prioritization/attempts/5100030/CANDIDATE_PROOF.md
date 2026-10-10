# A Jacobi-addition proof of focal-pedal invariant k601

Problem 5100030 / AMR-050-0030. Author substantive turn 1, 2026-10-01. Complete candidate, awaiting separate adversarial review. No novelty or priority assertion.

## 1. Exact target and conventions

Let the outer ellipse have semiaxes a>b>0 and foci F±=(±c,0), where c²=a²−b². Fix a nondegenerate confocal elliptic caustic with semiaxes α>β>0, so α²−β²=c². For a closed billiard polygon P, let q±,i be the ordinary Euclidean perpendicular distance from F± to the supporting line of its ith side. Equivalently, this is the distance from that focus to its corresponding pedal vertex. The feet may lie on extended sides; the distance is to the line, not to a segment.

**Theorem.** For every odd primitive period N, the product

    I(P) = (Σ_i q+,i)(Σ_i q−,i)

is independent of P in the fixed confocal Poncelet family. The result includes the allowed self-intersecting winding classes. Repeating an odd primitive orbit an odd number of times multiplies I by the square of that repetition number, so constancy also holds with a nonprimitive odd indexing length.

This is the identical k601 row of arXiv:2004.12497v11, Table 7, p.9, and the published *Fifty New Invariants*, Table 7, p.349. The source's elliptic billiard is a pair of confocal ellipses, not a hyperbolic caustic. No area convention enters this theorem. The source uses signed areas for its other rows, which are not part of this claim.

## 2. Classical inputs and notation

Write

    k=c/α,    m=k²,    k′=β/α,    K=K(k).

Thus 0<k<1 and m is the elliptic *parameter*. All Jacobi functions below have modulus k; their argument is written alone. This avoids conflating the source's use of “m” for a modulus with software's use of m=k².

We use the classical addition identities, quarter-period identities, and Jacobi zeta function Z. In particular,

    Z(x+a)=Z(x)+Z(a)−m sn(x) sn(a) sn(x+a),           (2.1)
    Z(x+2K)=Z(x),
    dn(x+K)=k′/dn(x),    cn(x+K)=−k′ sn(x)/dn(x).    (2.2)

These are standard identities, recorded in NIST DLMF §§22.8, 22.4–22.5 and 22.16. Equation (2.1) is the quasi-addition law 22.16.27, also satisfied by Z as stated in §22.16(iii); its period is 22.16.34. They are credited inputs, not new identities.

We also use the standard canonical billiard parametrization, in the precise form of Stachel, *On the motion of billiards in ellipses*, European Journal of Mathematics 8 (2022), Theorem 4.3, pp.1614–1615. If the primitive winding number is τ, then gcd(τ,N)=1, 0<τ<N/2, and with

    h=2τK/N,
    a=α dn(h)/cn(h),    b=β/cn(h),

the vertices are

    P_i=(−a sn(u+2ih), b cn(u+2ih)),   i=0,…,N−1.   (2.3)

Varying u parametrizes the family. This classical parametrization is the substantive geometric input; a proof of integrability is not claimed here.

## 3. A finite odd-period Jacobi identity

**Lemma.** Let N be odd, t_i=t+4Ki/N for i modulo N, and put

    D(t)=Σ_i dn(t_i),    C(t)=Σ_i cn(t_i).

Then D(t)²−m C(t)² is independent of t.

**Proof.** For r=1,…,N−1, set a_r=4Kr/N. Since N is odd, a_r is not an integer multiple of 2K, so sn(a_r)≠0. The zeta addition identity gives

    sn(t_i) sn(t_i+a_r)
      = [Z(t_i)+Z(a_r)−Z(t_i+a_r)]/[m sn(a_r)].

The arguments t_i+a_r permute the t_i modulo 4K. Since Z has period 2K, summing telescopes exactly:

    S_r(t):=Σ_i sn(t_i) sn(t_i+a_r)
           =N Z(a_r)/[m sn(a_r)].                 (3.1)

In particular S_r is independent of t. There are no real denominator singularities: m>0 and the only real zeros of sn are integer multiples of 2K.

The difference addition formulas imply, for y=x+a and S=sn(x)sn(y),

    dn(x)dn(y) = dn(a)−m cn(a) S,
    cn(x)cn(y) = cn(a)−dn(a) S.                   (3.2)

For completeness, the ordinary difference formulas say

    dn(a) = [D_xy+m S C_xy]/[1−mS²],
    cn(a) = [C_xy+S D_xy]/[1−mS²],

where D_xy=dn(x)dn(y), C_xy=cn(x)cn(y). Inverting this two-by-two system gives (3.2). Its denominator is positive for real arguments because 0<m<1.

It follows that each cyclic cross-correlation

    Σ_i [dn(t_i)dn(t_i+a_r)−m cn(t_i)cn(t_i+a_r)]
      =N[dn(a_r)−m cn(a_r)]
        +m[dn(a_r)−cn(a_r)] S_r(t)               (3.3)

is constant. The diagonal term is constant too, since dn²−m cn²=1−m. Expanding the two squares and grouping all ordered pairs by j−i modulo N expresses D²−mC² as the sum of that diagonal contribution and the N−1 quantities (3.3). This proves the lemma. ∎

Oddness is essential to this argument. For even N, the shift r=N/2 gives a_r=2K and sn(a_r)=0; the telescoping division is unavailable. We do not claim an even-period invariant.

## 4. Geometry-to-functions calculation

The side from P_i to P_{i+1} is tangent to the caustic at parameter

    v_i=u+(2i+1)h,
    Q_i=(−α sn(v_i), β cn(v_i)).

Here is a direct check, so the contact-point phase is not assumed. The tangent line at Q_i is

    −(sn(v_i)/α) X + (cn(v_i)/β) Y = 1.          (4.1)

For the vertex of parameter v_i−h, substitution from (2.3) gives the left-hand side

    [dn(h) sn(v_i−h)sn(v_i)
       +cn(v_i−h)cn(v_i)]/cn(h)=1,

by the second identity in (3.2). The same calculation with difference −h gives 1 at the vertex of parameter v_i+h. Thus (4.1) is exactly the required side line. The nondegenerate caustic and the distinct primitive vertices ensure it is a genuine chord and tangent line.

The norm of its normal vector is

    sqrt(sn(v_i)²/α²+cn(v_i)²/β²)=dn(v_i)/β.

Evaluating (4.1) at F± yields the ordinary distances

    q+,i = β[1+k sn(v_i)]/dn(v_i),
    q−,i = β[1−k sn(v_i)]/dn(v_i).               (4.2)

Both numerators are strictly positive for real v_i because k<1. No signed-distance replacement or absolute-value cancellation is hidden in this step. The pointwise product q+,i q−,i=β² is a familiar focal-tangent identity, but by itself does not establish the desired product of sums.

Since gcd(τ,N)=1, the unordered parameter set v_i modulo 4K is exactly

    {v_0+4Ki/N : i=0,…,N−1}.

This holds for every primitive winding class, and reversing orientation merely permutes the summands. Put

    A(v)=Σ_i 1/dn(v+4Ki/N),
    B(v)=Σ_i sn(v+4Ki/N)/dn(v+4Ki/N).

Equation (4.2) gives I=β²(A²−mB²). Apply the quarter-period identities (2.2) term by term at t=v+K:

    A(v)=D(t)/k′,    B(v)=−C(t)/k′.

Consequently

    I(P)=α²[D(t)²−m C(t)²],                     (4.3)

which is constant by the lemma. This proves the theorem. ∎

## 5. An explicit family constant and boundary cases

Evaluate at v=0. The points 4Ki/N pair under negation, so the odd function sn/dn has sum zero. A positive expression for the invariant is therefore

    I = β² [Σ_{i=0}^{N−1} 1/dn(4Ki/N,k)]².      (5.1)

This finite elliptic-function expression depends only on the fixed caustic and period. No elementary closed form or minimal expression is claimed.

The source assumes a>b. In the circular limiting case k=0, each side is tangent to a concentric circle of radius β, both foci coincide with the center, and every q equals β; hence I=N²β² directly. Degenerate caustics β=0 and grazing/nonperiodic limiting trajectories are outside the theorem's hypotheses. No claim for even N is made. A repeated odd orbit reduces to its odd primitive period and scales each sum by its repetition count.

## 6. Attribution and verification status

This proof combines the source's experimentally proposed invariant with Stachel's published canonical parametrization and classical Jacobi addition/zeta identities. Cyclic Jacobi identities and generalized Landen transformations have an extensive preexisting literature, including Khare–Sukhatme (2002–2004). No new special-function theorem or priority for this application is asserted. The proof above establishes the needed identity directly, rather than relying on a numerical version of a cyclic identity or a literature status label.

The checker separates exact symbolic reductions from high-precision numerical calibration. Numerical constancy is diagnostic only; the theorem rests on the telescoping argument for every odd integer N. This complete candidate requires a separate full review before promotion or a claim PR.

## Primary references

- Reznik–Garcia–Koiller, [arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), §§2,3.7 and Table 7; [published Table 7, p.349](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf)
- Stachel, [On the motion of billiards in ellipses](https://doi.org/10.1007/s40879-021-00524-2), Theorem 4.3; [arXiv preprint](https://arxiv.org/abs/2105.03624)
- NIST DLMF, [addition theorems](https://dlmf.nist.gov/22.8), [periods and zeros](https://dlmf.nist.gov/22.4), [quarter-period special values](https://dlmf.nist.gov/22.5), and [Jacobi epsilon/zeta identities](https://dlmf.nist.gov/22.16)
- Khare–Sukhatme, [Generalized Landen transformation formulas for Jacobi elliptic functions](https://arxiv.org/abs/math-ph/0312074), background and attribution only, not a required unverified lemma
