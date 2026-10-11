# Rational-caustic obstructions, inner partial results, and versioned source audits

This is an AI-assisted, unrefereed mathematical draft. Acceptance means an internal AI mathematical audit accepted the explicitly scoped arguments; it is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

Original problem 2100405 / AMR-020-0405 has two existence parts. Both remain UNRESOLVED in this edition. The complete three-part authored argument below has passed the scoped internal mathematical audit in AUDIT.md.

# Part I. Rational constant-offset outer billiards: a complete obstruction

Authored proof, 2026-10-11. This is a restricted rigidity result, not a solution of the two-rational-caustic existence question. The cyclotomic argument below does not use the sine-ratio lemma in arXiv:1103.5072v1.

## 1. Cyclotomic ingredients

Write Φ_m for the m-th cyclotomic polynomial and φ for Euler's totient. We use the standard facts that Φ_m is irreducible over Q, [Q(ζ_m):Q]=φ(m), and primitive m-th roots are Galois conjugate.

If a divides b and φ(a)=φ(b), then either a=b or b=2a with a odd. Indeed, raising the exponent of an existing prime multiplies φ by that prime; adjoining a new prime power p^e multiplies it by p^(e−1)(p−1). The only factor equal to one from a proper enlargement is adjoining a single factor 2 to an odd integer.

If s,t≥3 and Q(ζ_s)=Q(ζ_t), set m=lcm(s,t). Their compositum is Q(ζ_m): the two roots generate a primitive m-th root by Bezout's identity, since gcd(m/s,m/t)=1. Thus φ(m)=φ(s)=φ(t). The preceding observation implies either s=t, or one is twice the other and the smaller is odd.

For d>1 odd, Φ_d(1) is odd. This follows by evaluating (X^d−1)/(X−1)=∏_{e|d,e>1}Φ_e(X) at X=1: its product of integer factors is the odd integer d. Also Φ_d(−1)≡Φ_d(1) modulo 2. For d>1 odd, Φ_(2d)(X)=Φ_d(−X), so both Φ_(2d)(1) and Φ_(2d)(−1) are odd as well.

Consequently, if a root of unity w has order s>2, where s is odd or twice an odd integer, then the nonzero rational number

N_Q(w)/Q((w−1)/(w+1)) = Φ_s(1)/Φ_s(−1)

has odd numerator and denominator in reduced form. There is no sign issue because φ(s) is even. In particular its 2-adic valuation is zero. Here v_2(a/b) means the exponent of 2 in a minus that in b.

## 2. Rational tangent-slope lemma

**Lemma.** Let θ/π be rational. Let k,l be positive integers for which tan(kθ) and tan(lθ) are finite and nonzero. If

    tan(kθ)/k = tan(lθ)/l,

then k=l.

**Proof.** Put z=e^(2iθ), of order q, and

    u_k=(z^k−1)/(z^k+1)=i tan(kθ),
    u_l=(z^l−1)/(z^l+1)=i tan(lθ).

The hypothesis is u_l=(l/k)u_k. The inverse formula w=(1+u)/(1−u) for u=(w−1)/(w+1) shows

    K=Q(z^k)=Q(u_k)=Q(u_l)=Q(z^l).

All denominators are nonzero; u=1 would imply −1=1. Let s and t be the orders of z^k and z^l. Finite nonzero tangents imply s,t>2. By Section 1 either s=t, or one is twice the other with the smaller odd.

If s=t, a Galois automorphism σ of K takes z^k to z^l and therefore u_k to (l/k)u_k. If σ has finite order N, iteration gives u_k=(l/k)^N u_k. Since u_k≠0 and l/k>0, l=k.

If s=2t with t odd, write a=v_2(q). Since s=q/gcd(q,k) has exactly one factor 2, v_2(k)=a−1. Since t=q/gcd(q,l) is odd, v_2(l)≥a. Thus v_2(l/k)≥1. But Section 1 shows that both N_K/Q(u_k) and N_K/Q(u_l) have 2-adic valuation zero. Taking norms in u_l=(l/k)u_k gives

    0 = [K:Q] v_2(l/k) + 0,

a contradiction. The case t=2s is identical after interchanging k,l. These exhaust the cases. ∎

**Corollary (the tangent equation used in the explicit outer construction).** If θ/π is rational, 0<θ<π/2, and n>1 is an integer, then tan(nθ)=n tan θ is impossible when tan(nθ) is defined. If tan(nθ) is undefined it does not solve the equation. Apply the lemma with k=1 and l=n.

This recovers the relevant result attributed to Cyr by an independent argument. It does not assert that Cyr's theorem is false; the separate source audit only refutes a more general intermediate lemma in the retained preprint.

## 3. Fourier rigidity of the constant-offset ansatz

**Theorem.** Let γ:R/2πZ→R² be a C¹ embedding. Suppose r>0 and α/(2π) is rational, with 0<α<π, and

    γ(t+α)−γ(t)=r[γ′(t)+γ′(t+α)]                 (1)

for every t. Then the image of γ is an ellipse, γ(t)=c+a cos t+b sin t with a,b linearly independent, and r=tan(α/2).

**Proof.** Let c_j be its vector-valued Fourier coefficients. Integration by parts is valid for C¹ periodic γ. Equation (1) gives

    [(e^(ijα)−1)−ijr(1+e^(ijα))] c_j=0.          (2)

If j≠0 and c_j≠0, then e^(ijα) can be neither 1 nor −1: substituting either value into (2) gives a nonzero scalar multiplier. Therefore

    tan(jα/2)=jr.

Reality gives c_(−j)=conjugate(c_j). Any two positive frequencies with nonzero coefficients satisfy the lemma in Section 2 and must agree. There is at least one such frequency since an embedding is not constant. Fourier uniqueness in L², followed by continuity, now gives γ(t)=c+a cos(kt)+b sin(kt) for one positive integer k. If a,b were dependent this would not be an embedding. If k>1 the parametrization would repeat after 2π/k, also contradicting embedding. Thus k=1, the image is an ellipse, and equation (2) gives r=tan(α/2). ∎

No first-Fourier-mode assumption, analyticity, smallness condition, or finite Fourier cutoff is used.

## 4. Exact outer-billiard application and its limit

For a positively oriented, smooth strictly convex boundary γ, a common explicit ansatz is Γ_r(t)=γ(t)+rγ′(t). Equation (1) is exactly

    Γ_r(t)=γ(t+α)−rγ′(t+α).

Thus Γ_r(t) and Γ_r(t+α) are symmetric about γ(t+α) on its supporting line. Whenever Γ_r is an embedded exterior curve and the orientation is chosen accordingly, the outer billiard acts on it by t↦t+α. For the opposite convention the inverse map acts; rationality and periodicity are unchanged.

The theorem proves: a nonelliptic smooth strictly convex table cannot have even one rational invariant curve represented by this *constant tangent-offset and constant parameter-shift* ansatz.

In particular, for the nontrivial n>1 construction in Bialy–Mironov–Shalom, arXiv:1811.04981v1, Theorem 2.1, the stated curves are not rational periodic invariant circles. The literal n=1 case is a circle and permits arbitrary shifts; it is excluded from this claim. The nonelliptic application also requires a nonzero perturbation. Their parameters satisfy the tangent equation, and the corollary proves the shift irrational. The paper itself states the irrationality on PDF4, Remark 2.

This does not exclude general rational outer caustics. For them both the tangent offset λ(t) and the induced map f(t) may vary. No argument here makes either constant, and no argument here makes two distinct induced maps commute. Conjugating one finite-order circle map to a rotation does not make its tangent offset constant or simultaneously normalize a second map.

# Part II. Inner partial result and exact remaining systems

Authored mathematics, 2026-10-11. Neither original existence question is resolved.

## 1. Constant width and the allowed period-two caustic

Let n(θ)=(cos θ,sin θ), τ(θ)=(-sin θ,cos θ), and let h be a smooth support function with h+h″>0. The positively curved boundary is

    γ(θ)=h(θ)n(θ)+h′(θ)τ(θ).

If h(θ)+h(θ+π)=w is constant, differentiation yields h′(θ)+h′(θ+π)=0, and hence

    γ(θ+π)−γ(θ)=−w n(θ).

This chord is normal at both endpoints. It therefore gives a two-periodic inner billiard trajectory through every boundary point. The family is a periodic invariant phase circle with rotation 1/2.

Conversely, if every boundary point belongs to such a two-periodic invariant graph, the chord must be normal at both endpoints. Positive curvature makes the two normal angles antipodal. Its τ(θ) component is therefore −[h′(θ)+h′(θ+π)]=0. The width is constant. This converse is only stated in the positive-curvature class used in these coordinates.

For example h_ε(θ)=1+ε cos(5θ), 0<|ε|<1/24, gives

    h_ε+h_ε″=1−24ε cos(5θ)>0,
    h_ε(θ)+h_ε(θ+π)=2.

Thus it is an analytic nonelliptic table with the allowed period-two caustic. To check nonellipticity, any ellipse is centrally symmetric about some center c; in support coordinates this means h(θ)−c·n(θ) is π-periodic. Translation removes only frequency one, whereas the nonzero frequency-five term is π-antiperiodic, so this table is not an ellipse. This constructs only ONE rational caustic.

## 2. Necessary first-order condition for a second caustic

Consider a differentiable deformation of the unit circle whose first normal variation is f(θ), and assume a differentiably varying p/q-periodic invariant family converging to regular star polygons exists. Here 0<p/q≤1/2 and gcd(p,q)=1. Put α=2πp/q. At ε=0 its vertices are n(t+jα), j=0,...,q−1.

The polygon perimeter is stationary in each vertex parameter for a billiard orbit. Consequently, its first variation from the motion of vertex parameters cancels; its first variation from the boundary is

    2 sin(α/2) Σ_(j=0)^(q−1) f(t+jα).           (1)

Indeed, for an edge between n(a),n(b) with b−a=α, the scalar products of the edge's unit vector with n(b) and with −n(a) are both sin(α/2). Tangential terms cancel on summing adjacent edges by stationarity. The perimeter is constant as t traverses an entire periodic billiard family: its t-derivative is the sum of the vertex stationarity equations. Thus (1) must be independent of t.

Writing Fourier coefficients as f̂_m, the root-of-unity sum in (1) gives the necessary condition

    f̂_(kq)=0 for every nonzero integer k.        (2)

The proof assumes differentiable persistence of the periodic family; it does not assert a differentiable normal form for every isolated rational caustic.

For two denominators q_1,q_2, (2) merely removes the nonzero multiples of either denominator. Infinitely many Fourier directions remain; for example any cos(mθ) with m congruent to 1 modulo q_1 q_2. In particular cos(5θ) passes both q=2 and q=3 filters. The explicit constant-width family above therefore has the exact period-two family and passes the first-order necessary test for period three. It has NOT been proved to have a period-three caustic. This is a rigorous demonstration of why the linear test cannot certify existence or nonexistence.

## 3. Exact equations that a genuine construction must solve

### Inner billiards

For a regular C¹ embedding γ of a strictly convex closed boundary (so γ′ never vanishes) and an orientation-preserving finite-order circle homeomorphism f on its parameter circle, set

    V_+(t)=[γ(f(t))−γ(t)]/|γ(f(t))−γ(t)|,
    V_−(t)=[γ(f^(-1)(t))−γ(t)]/|γ(f^(-1)(t))−γ(t)|.

Assume nonzero chords. The exact reflection condition is

    γ′(t)·[V_+(t)+V_−(t)]=0                    (3)

for every t. Strict convexity places both adjacent vertices on the interior side of the tangent, so tangential equality together with unit speed is the elastic reflection law. If f has exact rotation p/q and f^q=id, (3) gives a full q-periodic phase graph. Two different rational caustics require two such maps f_1,f_2 for the SAME γ, with different rotation numbers and genuinely different geometric caustics. Satisfying (3) only to finite order in ε is not enough.

### Outer billiards

Let γ be a positively oriented regular smooth parametrization of a strictly convex closed boundary, λ(t)>0, and define Γ(t)=γ(t)+λ(t)γ′(t). Suppose Γ is an embedded exterior curve winding once around γ. An orientation-preserving finite-order map f represents the outer billiard on Γ exactly when, with an appropriate fixed orientation convention,

    γ(f(t))−γ(t)=λ(t)γ′(t)+λ(f(t))γ′(f(t)).    (4)

Indeed, (4) rewrites Γ(t)=γ(f(t))−λ(f(t))γ′(f(t)), so midpoint reflection at γ(f(t)) sends Γ(t) to Γ(f(t)). The positive factors select the two opposite tangent half-lines. Conversely, a smooth invariant exterior graph in these tangent coordinates gives (4) from the midpoint rule.

For two caustics one needs two pairs (λ_i,f_i) solving (4) for the same γ. The obstruction proved in Part I excludes λ_i constant and f_i a rational rigid shift in the same parameter. It does not solve (4) for variable λ_i and f_i.

No simultaneous-conjugacy assumption, commutation assumption, or relation between the two λ_i is licensed by the original problem. Establishing such a condition would require an additional theorem, not a coordinate choice.

## 4. Remaining full target

Both original questions remain unresolved in this attempt:

- I: exhibit an admissible smooth strictly convex nonelliptic INNER table and two full rational periodic phase circles with distinct geometric rotation values, or prove universal nonexistence;
- O: do the same for the OUTER midpoint-reflection map.

The first-order kernel, individual periodic orbits, one-caustic families, finite-order formal persistence, and multiple irrational invariant curves settle neither question. A complete construction needs convergent exact solutions with verified regularity, convexity, global closure, and two distinct rational rotations.

# Part III. Scoped source-audit appendices

These checks concern precise intermediate statements in the retained versions. They neither refute the papers' main conclusions nor resolve the original two-caustic question. No priority claim, comprehensive erratum search, external contact, or review of inaccessible versions is implied.

## A. Cyr's retained preprint: a false general sine-ratio lemma

Source: Van Cyr, *A number theoretic question arising in the geometry of plane curves and in billiard dynamics*, arXiv:1103.5072v1, https://arxiv.org/abs/1103.5072v1. Retained PDF SHA-256: 4d518695297fed8518065714b000de86aa313af010597b01a4e122a92a9cfcbe. All five pages were text-read; PDF2 was visually inspected.

Lemma 3 on PDF2 assumes only a rational ρ in (0,1), excluding 1/2; integers k,m; and sin(mπρ)≠0. It asserts that a rational sine ratio under these hypotheses is 0 or ±1. There are no additional standing restrictions on k,m or the denominator of ρ in the retained paper.

The exact values ρ=1/6, k=3, m=1 obey every stated hypothesis, but

    sin(kπρ)/sin(mπρ)=sin(π/2)/sin(π/6)=2.

Thus this general intermediate statement is false as written. The application in Theorem 1 specifically uses k=n−1 and m=n+1. This counterexample does NOT fit that ordered relationship, so it does not refute the application's specialized assertion. It also does not refute the tangent theorem. The independent cyclotomic proof in Part I establishes the required tangent theorem without this lemma.

The proof's prime-power basis claim also cannot hold in its stated generality: for n=3, the real basis part is {Re(ζ_3)}={−1/2}, and expressing 1 requires coefficient −2. This observation is supplementary; the explicit sine ratio already suffices.

Version boundary: the arXiv abstract page inspected on 2026-10-11 lists only v1. The published article is recorded as Proc. Amer. Math. Soc. 140 (2012), 3035–3040, DOI https://doi.org/10.1090/S0002-9939-2012-11258-4. The correct official AMS article endpoint returned HTTP403. It was not bypassed or retried through another route. The published proof was not inspected here, and no claim about its exact wording is made. Bounded searches did not establish whether a correction already exists.

## B. Kaloshin–Koudjinan v1: autocorrelation does not imply constancy

Source: V. Kaloshin and C. E. Koudjinan, *Non co-preservation of the 1/2 & 1/(2l+1)-rational caustics along deformations of circles*, arXiv:2107.03499v1, https://arxiv.org/abs/2107.03499v1. The arXiv abstract page inspected on 2026-10-11 lists only v1. The retained PDF and extracted-text identities are recorded in SOURCES.json. Pages 1–8 were text-read; pages 6–7 were visually inspected.

Lemma 11 (PDF6) concerns a complex-valued, 2π-periodic analytic function f on a strip |Im z|<ρ, bounded there. Its condition is

    Σ_k f_k conjugate(f_(k−n))=0 for all nonzero n∈Z.

Its conclusion that f is constant is false as stated. Take f(z)=e^(iz). This is periodic, entire, and bounded on every such strip. Its only nonzero Fourier coefficient is f_1=1, so the displayed sum vanishes for EVERY nonzero n. Nevertheless f is nonconstant.

The condition implies only that |f(t)| is constant on the REAL circle. It does not imply that |f(z)| is constant throughout the complex strip. In the example, |f(x+iy)|=e^(−y). The PDF7 proof treats f(z)conjugate(f(z)) as though its real-axis Fourier expansion analytically represented the same expression throughout the strip. That expression is generally not holomorphic. The holomorphic continuation from the real circle is f(z)conjugate(f(conjugate(z))), which equals 1 for the counterexample and does not force f to be constant.

A real-valued f on the real circle would be a valid additional hypothesis: a continuous real-valued function with constant square has constant sign unless it vanishes, hence is constant. However, the PDF8 application does not automatically yield a real-valued auxiliary function. There f_k=k p_(1,6k+1). For the real analytic input p_1(t)=cos(5t), one obtains exactly

    f_(−1)=−1/2, all other f_k=0,
    f(z)=−e^(−iz)/2.

This is not real-valued on the real circle. Moreover p_1 has zero modes at ±1, at all even frequencies, and at all nonzero multiples of 3. Its finite support also satisfies equation (21) on PDF8 for every nonzero n: the only possible nonzero product uses k=−1 and n=0. Thus the displayed constraints at that step do not justify either real-valuedness or constancy of f.

This is a counterexample to the auxiliary-function inference, NOT a billiard with two actual caustics. The input p_1 alone is not a complete family solving all billiard equations. Theorem 9 is therefore not declared false. Its displayed proof cannot be certified using these steps alone, and the exact original existence question remains independent of this issue.

## C. Current-source boundary

Koudjinan–Ramírez-Ros, arXiv:2503.07488v2, https://arxiv.org/abs/2503.07488v2, PDF18 §6.1, discusses copreservation with different rotations as a remaining problem; PDF18–19 §6.2 distinguishes finite-order corrections from their convergence. The arXiv record gives a 2026 journal reference. This is evidence about that source's stated scope, not a proof of worldwide current openness. The source does not prove that any finite-order or formal calculation supplies two exact rational caustics.

Fierobe–Sorrentino, arXiv:2407.17090v1, https://arxiv.org/abs/2407.17090v1, PDF1–2, concerns the parameter set for a periodic invariant curve in an analytic family. The stated discrete-or-entire alternative for a SINGLE rotation does not establish a common parameter for TWO rotations. Its full proof was not audited here.

Genin–Tabachnikov, arXiv:math/0604388v1, https://arxiv.org/abs/math/0604388v1, provides one-period outer families. Its Section 4 construction for triangles has one-period monodromy constraints; it does not, on the inspected pages, impose a second rational invariant circle. One-period abundance does not prove an intersection of two such families away from ellipses.
