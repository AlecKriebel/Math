# Independent audit of two rational caustic obstructions

This is an AI-assisted, unrefereed mathematical draft. Acceptance means an internal AI mathematical audit accepted the explicitly scoped arguments; it is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

## Disposition

**Accept the scoped arithmetic and constant-offset rigidity results. The original inner and outer existence questions both remain unresolved.** The independent review also confirms two precise counterexamples to auxiliary assertions in the inspected preprints. These are proof-level findings, not counterexamples to either main geometric theorem.

This audit concerns the three complete authored arguments now assembled in PROOF.md. Their original byte identities and exact public document bindings are recorded in ACCEPTANCE.json and VERIFICATION.json. It does not certify novelty, comprehensive literature coverage, or a universal nonexistence theorem. No source-author code was executed.

## Original target and the principal obstruction to completion

The source question is Question 3.7 on PDF21 of arXiv:1804.03737v1 and Question 4.7 on PDF17 of v2. The surrounding v2 PDF14 and PDF16 conventions concern smooth closed strictly convex planar tables and a whole periodic invariant phase circle. Period two for constant-width inner tables is expressly allowed. Merely finding two periodic orbits, two irrational invariant circles, or the two orientations of one caustic is insufficient. [Original source v2](https://arxiv.org/pdf/1804.03737v2)

The outer proof assumes, in one and the same parameter, a **constant tangent offset** and a **constant rational shift**. A general rational outer caustic has a variable offset lambda(t) and a finite-order map f(t). Conjugating f to a rigid rotation does not make lambda constant. No supplied result permits simultaneous normalization of two caustics. This is the exact unfilled logical step between the accepted obstruction and the original outer target.

For inner billiards the supplied construction establishes exactly one rational family. The second family's first-order necessary condition is satisfied, but no convergent solution of the nonlinear reflection equations is produced. Passing that filter cannot fill the inner target.

## Accepted arithmetic argument

The precise lemma is: if theta/pi is rational and k,l are positive integers, with both tan(k theta) and tan(l theta) finite and nonzero, then

    tan(k theta)/k = tan(l theta)/l  implies  k=l.

The proof is valid, with these dependencies and checks:

1. Put z=exp(2i theta), u_j=(z^j-1)/(z^j+1). The finite/nonzero hypotheses exclude root orders one and two. The equality gives u_l=(l/k)u_k. The invertible fractional-linear relation between u_j and z^j gives equal fields K=Q(z^k)=Q(z^l).
2. If a divides b and phi(a)=phi(b), prime-power factorization forces a=b or b=2a with a odd. The compositum identity Q(zeta_s,zeta_t)=Q(zeta_lcm(s,t)), together with cyclotomic degrees, therefore makes the two orders s,t equal or an odd/double-odd pair. The coprimality of lcm(s,t)/s and lcm(s,t)/t justifies the compositum assertion.
3. When s=t, a finite-order Galois automorphism sends z^k to z^l and hence u_k to (l/k)u_k. Iteration forces (l/k)^N=1. Positivity and u_k nonzero force l=k.
4. For an odd/double-odd pair, the two norms of u_j have 2-adic valuation zero: the norm is Phi_s(1)/Phi_s(-1), and both integers are odd. This follows for odd d>1 from the product of Phi_e(1) over e|d, e>1 being d, and for 2d from Phi_(2d)(X)=Phi_d(-X).
5. If s=2t with t odd, write a=v_2(ord z). Then v_2(k)=a-1 while v_2(l)>=a, so v_2(l/k)>0. Taking the norm of u_l=(l/k)u_k contradicts item 4. Interchanging k,l handles the reverse case.

The only standard algebraic dependencies are cyclotomic irreducibility/degrees, conjugacy of primitive roots, elementary field norms, and rational prime valuations. The argument does not depend on Cyr's disputed sine-ratio lemma.

The desired consequence follows with k=1, l=n: for integer n>1 and rational theta/pi in (0,1/2), the equation tan(n theta)=n tan theta has no solution where its left side is defined. A pole is not a solution. The nonzero condition matters: theta=pi/3 and indices 3,6 give equal zero normalized tangents. This exception is outside the lemma.

## Accepted Fourier and geometric argument

Assume gamma is a C1 embedding of R/(2pi Z) into R2, r>0, alpha/(2pi) rational, 0<alpha<pi, and

    gamma(t+alpha)-gamma(t)=r[gamma'(t)+gamma'(t+alpha)]

for every t. Integration by parts gives the displayed scalar Fourier multiplier in the authored proof. A nonzero coefficient at frequency j excludes exp(i j alpha)=+/-1, and therefore satisfies tan(j alpha/2)=jr. Reality pairs positive and negative frequencies. The arithmetic lemma permits only one positive frequency. Fourier uniqueness and continuity then give gamma=c+a cos(kt)+b sin(kt). Embedding excludes dependent a,b and k>1, leaving k=1 and r=tan(alpha/2). This is a complete restricted rigidity theorem; no missing analyticity or first-mode hypothesis is needed.

For a regular strictly convex table and an embedded exterior tangent-coordinate curve Gamma_r=gamma+r gamma', the identity says that Gamma_r(t) and Gamma_r(t+alpha) are midpoint reflections in the tangent point gamma(t+alpha). This checks the outer-map interpretation up to the fixed orientation convention.

Applied to the **n>1 branch** of Bialy-Mironov-Shalom's explicit construction, it proves its proposed shifts irrational. The source itself states this in PDF4 Remark 2. The original blanket wording was narrowed during review: the literal n=1 case is circular and allows rational shifts. Nonelliptic application also presupposes a nonzero perturbation and the source's smooth-convex/embedded regime. [Inspected outer preprint](https://arxiv.org/pdf/1811.04981v1)

## Accepted inner partial and exact equations

For a smooth support function h with h+h''>0, the standard positive-radius support parametrization is regular and bounds a strictly convex domain. Constant width h(theta)+h(theta+pi)=w gives the antipodal chord -w n(theta), normal at both endpoints; it supplies the full period-two phase circle. Conversely, within this positive-curvature class, such a family forces constant width.

The example h=1+epsilon cos(5 theta), 0<|epsilon|<1/24, has positive radius 1-24epsilon cos(5 theta), width two, and a nonzero odd fifth mode. Translation changes only first modes, so no translation makes h pi-periodic; hence the table is not centrally symmetric and cannot be an ellipse. This is a valid one-caustic example.

For a differentiably persisting p/q-periodic family near the circle, with coprime p,q and 0<p/q<=1/2, perimeter stationarity cancels the vertex-parameter variations. The first normal variation is 2 sin(pi p/q) times the sum of f(t+2pi jp/q). Constancy in t removes every nonzero Fourier mode divisible by q. The q=2 and q=3 filters both retain cos(5t). Differentiable persistence is an explicit hypothesis; the calculation does not assert it for arbitrary isolated caustics.

The stated exact inner equation is sufficient under a regular strictly convex parametrization, a finite-order orientation-preserving circle homeomorphism, nonzero chords, and the given rotation number. The tangent dot product is the equality of incoming and outgoing tangential components; strict convexity selects the proper normal components. The exact outer equation is likewise a valid midpoint identity for the stated positive offsets and embedded exterior graph. Neither equation has been solved for two different rational families on one nonellipse.

## Scoped source findings

### Cyr v1

In arXiv:1103.5072v1, PDF2 Lemma 3, rho=1/6, k=3, m=1 satisfies all printed hypotheses, including the nonzero denominator. Its sine ratio is exactly 2. No hidden restriction in the retained five-page text removes it. The claimed prime-power coordinate bound also fails at n=3 for the real vector 1, whose coefficient relative to Re(zeta_3)=-1/2 is -2. [Inspected preprint](https://arxiv.org/pdf/1103.5072v1)

The theorem's application uses the **ordered** indices k=n-1,m=n+1. The witness does not satisfy that relation and does not refute the tangent theorem. The accepted independent argument above establishes the relevant conclusion. The published AMS proof was not inspected; this audit makes no claim about its wording, corrections, or published validity.

### Kaloshin and Koudjinan v1

PDF6 Lemma 11 allows a complex-valued periodic analytic function bounded on a strip, and assumes zero Fourier autocorrelation at every nonzero shift. The entire function f(z)=exp(iz) is bounded on each finite-width strip and has only f_1=1, so it satisfies the complete condition while being nonconstant. The condition makes |f(t)| constant on the real circle; it does not make |f(z)| constant on the strip. The PDF7 step treating f(z)conjugate(f(z)) as a holomorphic Fourier continuation is invalid in general. [Inspected preprint](https://arxiv.org/pdf/2107.03499v1)

The PDF8 application was checked as well. It defines f_k=k p_(1,6k+1) and asserts real-valuedness. The real analytic input p_1(t)=cos(5t) has no first, even, or nonzero multiple-of-three modes, yet yields f(z)=-exp(-iz)/2. Equation (21) has possible nonzero support only at shift n=0, so it adds no exclusion of this input. These displayed constraints therefore do not justify the asserted real-valuedness or constancy. Extra reality would repair the isolated lemma, but it is not supplied by this coefficient definition.

This input is **not** a family satisfying every higher-order billiard equation. Theorem 9 is not declared false; its displayed route cannot be certified at this step. Nothing here constructs two actual caustics.

### Remaining source context

[Koudjinan-Ramirez-Ros v2](https://arxiv.org/abs/2503.07488) PDF18-19 discusses co-preservation and convergence as further problems. Its official record lists a 2026 journal reference; the inspected mathematical text is the v2 preprint. This supports a limited source-scope statement, not worldwide current openness. [Fierobe-Sorrentino v1](https://arxiv.org/abs/2407.17090) PDF1-2 treats a fixed rotation in an analytic family; its discrete-or-entire alternative does not establish an intersection for two rotations. [Genin-Tabachnikov v1](https://arxiv.org/abs/math/0604388) Section 4 constructs a period-three family subject to monodromy/convexity conditions; those conditions do not themselves impose a second rotation. Their full proofs are not certified by this audit.

## Integrity and checks

The original proof and audit inventories were authenticated against fixed manifest hashes. The public document identities are bound in ACCEPTANCE.json and VERIFICATION.json. SOURCES.json distinguishes reading from retrieval and visual checks from text checks. Source copies, page images, and local verification programs are not distributed in this prose edition.

The independent standard-library checker passed under ordinary Python, -O, and -OO. It checked 17,535 admissible tangent-slope pairs for root orders 3 through 72 and positive frequencies through 24, 320 divisor/totient cases through 256, 52 norm-parity cases, and exact finite-support source witnesses with hypothesis countercontrols. These finite checks are regression evidence only. The unbounded acceptance above rests on the mathematical argument.

Final classification: **accepted scoped result; both original existence parts unresolved; no novelty or published-paper-error claim.**
