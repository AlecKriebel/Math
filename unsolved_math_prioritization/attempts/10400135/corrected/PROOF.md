# Additive Borel QHI are constant for a fixed closed pair

## Scope and normalization

Fix a compact connected closed oriented 3-manifold W, a nonempty link L in W, and an odd integer N > 1. Write K_N for the original Borel invariant of Baseilhac–Benedetti [B01], with B the upper-triangular subgroup of SL(2,C). If a is an additive complex cohomology class, let rho_a be the flat bundle with holonomy gamma -> U(a(gamma)), where

    U(x) = [[1,x],[0,1]].

The claim proved below is

    K_N(W,L,rho_a) = K_N(W,L,1)   for every a in H^1(W;C).

Thus the real-additive part of Ohtsuki Problem 7.20 has an affirmative answer, including every face of the Thurston unit sphere. The argument does not assert that all multiplicative/diagonal specializations are constant, or identify every fiber of their invariant functions.

The normalization is fixed by [B01], equation (2): if r_0 is the vertex count, N=2m+1, z has upper-right edge entries x(e), and t_Delta are its charged tetrahedron tensors, then

    K_N = (N^(-r_0) sum_states product_Delta(t_Delta)
                        product_{e outside H}(x(e)^(-2m/N)))^N.

This is the Nth power of the original state sum, not the later PSL(2,C) invariant raised to 2N, a reduced QHI, or an asymptotic volume. Multiplying this definition by a nonzero factor depending only on W,L,N would preserve the asserted constancy. A representation-dependent renormalization is outside this assertion.

## Source inputs

We use existence and gauge invariance of this invariant from [B01], Sections 3–4, especially Theorem 4.2; the charged local formulas are in Propositions 8.3 and 8.5. The source permits a distinguished triangulation with distinct edge endpoints, a branching, an integral charge, and a full cocycle. Fix the integral charge c_int once and use the actual tensor charge c = 2^(-1)c_int mod N, as in [B01], Definition 3.9; 2 is invertible because N is odd. These charge conditions are combinatorial and do not vary with the cocycle. Fullness means every upper-right edge entry is nonzero. A vertex gauge lambda acts by z(uv) -> lambda(u)^(-1) z(uv) lambda(v). Root choices do not alter K_N. These are the only imported invariant-theoretic statements. The continuity needed below is checked directly rather than inferred from the word “character.”

## Lemma 1: local continuity on the full-cocycle domain

Keep the finite triangulation, branching and integral charge fixed. The original K_N state sum is locally continuous as the full B-cocycle varies. In fact its permitted local determinations are holomorphic.

Proof. At any fixed full cocycle, every diagonal and upper-right edge entry is nonzero. On a sufficiently small neighborhood, choose local Nth roots of these finitely many entries. This can be done by taking disjoint small discs about the distinct members of the finite set of nonzero values and using one root function on each disc. Equal values receive the same determination, and every occurrence of a shared oriented edge uses its single chosen root. No multiplicativity condition is imposed on these root functions: the cocycle and Fermat equations are equations of their Nth powers. Proposition 4.3(a) of [B01] permits this local edge-root choice for K_N.

For a tetrahedron label its branched vertices 0,1,2,3 and write y_ij for a chosen Nth root of its upper-right edge entry x_ij. The nonconstant elementary expressions in its tensor can be written in terms of

    A = y_03 y_12,   B = y_01 y_23,   C = y_02 y_13.

They are nonzero. The cocycle equations give

    C^N = A^N + B^N.                                      (1)

For completeness, write the three consecutive edge matrices as (t_01,x_01), (t_12,x_12), (t_23,x_23), with multiplication

    (t,x)(u,y) = (tu, t y + x/u).

Then x_02=t_01 x_12+x_01/t_12,
 x_13=t_12 x_23+x_12/t_23, and
 x_03=t_01 t_12 x_23+t_01 x_12/t_23+x_01/(t_12 t_23).
Multiplication shows x_02 x_13 = x_03 x_12+x_01 x_23, which proves (1).

Let zeta=exp(2 pi i/N). The cyclic products occurring in the local matrices have factors B/(C-A zeta^j), with an optional zeta-shift of A in the inverse matrix. None of these denominators vanishes: C=A zeta^j would imply C^N=A^N and therefore B=0, contrary to fullness. Each numerator B is also nonzero, so reciprocal cyclic products in the inverse matrix are regular as well. Integer indices can be reduced modulo N; only finite products are involved.

The remaining non-monomial normalization is h(C/A), where

    g(q) = product_{j=1}^{N-1}(1-q zeta^j)^(j/N),
    h(q) = q^(-m) g(q)/g(1).

Here q=C/A is nonzero and q^N != 1 by (1). Hence all radicands 1-q zeta^j are nonzero. Local holomorphic determinations exist, g(1) != 0, and h(q) is locally holomorphic and nonzero. Both h and its reciprocal are therefore harmless. The factor [q]=(1-q^N)/(N(1-q)) in the inverse tensor is a polynomial in q; moreover q != 1 here. Charged tensors add only powers of nonzero edge roots and fixed powers of zeta. The edge normalization likewise uses only powers of nonzero entries.

There are two separate root issues. The edge-root determinations just discussed are covered by Proposition 4.3(a). The fractional powers in g also admit local holomorphic choices, but a chosen global branch may jump. Any two values of g(q) obtained from these fractional powers differ by an Nth root of unity. More explicitly,

    h(q)^N = q^(-m N) product_{j=1}^{N-1}(1-q zeta^j)^j / g(1)^N,

which is a single-valued nonzero holomorphic function on the domain under consideration. The normalization g(1)^N is nonzero and independent of these branch choices.

In the tensor R of [B01], Proposition 8.3, h(q) is a scalar common to every state index; in the inverse tensor it is replaced by 1/h(q). Proposition 8.5 adds only charged monomials and state-index shifts. Consequently the full unpowered state sum has the form

    H_N = product_Delta h(q_Delta)^(epsilon_Delta) S,

where epsilon_Delta is +1 or -1 according to which tensor occurs, and S is a finite sum of locally holomorphic expressions in the chosen edge roots. A change of any fractional-power branch in g therefore multiplies the entire H_N by one state-independent Nth root of unity. Its Nth power K_N is unchanged. Equivalently, K_N is the product of the single-valued factors h(q_Delta)^(N epsilon_Delta) and S^N. This proves local holomorphy as a genuine complex-valued function, not only continuity of a phase class. Zeros of S create no problem.

Changes between the permitted edge-root determinations do not change K_N by Proposition 4.3(a), so these local functions agree. This argument does not claim that an arbitrarily selected unpowered phase of H_N is globally continuous. No assumption about generic convergence to an undefined cocycle has been used. QED.

## Lemma 2: a nonsingular additive contraction

Let a be any additive cocycle on a distinguished triangulation whose edges have distinct endpoints. Choose an injective function u from its finite vertex set to C. Put

    b(uv) = u(v)-u(u),
    x_s(uv) = b(uv)+s a(uv),
    z_s(uv) = U(x_s(uv)).

Then z_s is a cocycle, [z_s]=rho_{s a}, and z_0 is a full cocycle representing the trivial bundle. There is an epsilon > 0 such that z_s is full for every |s| < epsilon.

Proof. Both b and a are additive cocycles, and U(x)U(y)=U(x+y). The cocycle b is the coboundary of u, so z_s is obtained from U(s a) by the vertex gauge U(u(v)). Its class is therefore rho_{s a}, while z_0 is gauge equivalent to the identity cocycle. Every b(e) is nonzero by injectivity and the distinct-endpoint condition.

If a vanishes on every edge, any epsilon works. Otherwise choose

    epsilon < min_{a(e) != 0} |b(e)|/(2 |a(e)|).

Then |x_s(e)| >= |b(e)|/2 > 0 for every edge with a(e) != 0; the other entries equal b(e). QED.

## Theorem: additive constancy

For the fixed W,L,N above and every a in H^1(W;C),

    K_N(W,L,rho_a) = K_N(W,L,1).

Proof. Represent a by a cocycle on the fixed distinguished triangulation and apply Lemma 2. For s != 0, choose any r with r^2=s. Direct multiplication gives

    diag(r,r^(-1)) U(a(gamma)) diag(r^(-1),r)
      = U(s a(gamma)).

Thus rho_{s a} and rho_a are conjugate as B-representations. Gauge invariance yields

    K_N(z_s)=K_N(W,L,rho_a)  whenever 0 < |s| < epsilon.

Lemma 1 applies at the full cocycle z_0, so letting s tend to zero gives

    K_N(W,L,rho_a)=K_N(z_0)=K_N(W,L,1).

The limiting gauge on the representations need not converge: the actual state-sum inputs z_s do converge inside the full-cocycle domain. This distinction is the reason the proof works. QED.

## Thurston-norm consequence, including degenerate cases

Identify H^1(W;R) with H_2(W;R) by Poincare duality and let x_W be the Thurston seminorm. Its unit sphere means {a : x_W(a)=1}. On that entire set the invariant above has a single value, not merely one value per face. Therefore it is constant on open or closed faces, fibered or nonfibered faces, and their boundaries whenever those sets exist.

No irreducibility, hyperbolicity, fibration, positive first Betti number, nondegeneracy of the seminorm, or positive-dimensional face is needed for the theorem. If x_W is identically zero, this unit sphere is empty and the face question is vacuous; the cohomological constancy statement still has content. If the seminorm has a kernel, its unit ball can be unbounded. One can work directly with its faces or pass to H^1(W;R)/ker(x_W): the invariant descends because it is constant on all of H^1(W;R). The case b_1=0 is also covered.

No model tetrahedron or finite computation is being used as a counterexample or as proof of a global state-sum value.

## Supplement: what the same argument says about general B-bundles

Let z(e)=(t(e),x(e)) be any B-cocycle and let z_diag(e)=(t(e),0). The t entries form a C*-cocycle. Pick vertex numbers u(v) so that

    d(e) = t(e)u(v)-u(u)/t(e) != 0

for each oriented edge e=uv. Such a choice exists: each forbidden equation is a proper linear hyperplane in the finite-dimensional space of vertex assignments, and a finite union of proper hyperplanes cannot cover that space over C. The edges must have distinct endpoints, as before.

Scaling x(e) by s preserves the B-cocycle equations. After applying the fixed vertex gauge U(u(v)), its upper-right entry is

    d(e)+s x(e).

This is full near s=0. For s != 0 the scaled original cocycle has the same bundle class as z by constant diagonal conjugation. The limit is a full representative of the diagonal bundle. Lemma 1 therefore proves

    K_N(W,L,[z]) = K_N(W,L,[z_diag]).

In particular, the original invariant cannot distinguish B-extensions with the same diagonal C*-representation. This is a consequence of the proved continuity and gauge invariance, not an unproved identification of the non-Hausdorff orbit space with a GIT quotient.

Define F_N(chi)=K_N(W,L,diag(chi,chi^(-1))) on Hom(H_1(W;Z),C*). Locally choose edge cocycles for chi using a fixed spanning tree and generators. Their entries vary holomorphically with chi. A fixed vertex gauge can make the representative at any selected chi full, hence also all nearby representatives. Lemma 1 proves local holomorphic dependence of F_N.

For an additive class a, the other specialization in Problem 7.20 is F_N(exp(a)); it is generally a different construction from rho_a. Classes with coefficients Z/pZ give evaluations at characters chi(gamma)=exp(2 pi i eta(gamma)/p). The contraction proof gives no equality between different chi, no classification of these multiplicative fibers, and no transfer to a boundary-decorated or reduced invariant. Those broader questions are not claimed solved here.

## Attribution and status

This is an authored deduction from the original Baseilhac–Benedetti definition and invariant theorem, with its needed local regularity verified above. No claim of novelty or of a newly accepted theorem is made. A targeted search did not locate a prior publication stating this exact additive conclusion. That negative search is not a proof of priority or of an open literature status. This manuscript is AI-assisted and unrefereed; independent review remains necessary before its mathematical claims should be relied upon.

## References

- [B01] S. Baseilhac and R. Benedetti, *Quantum Hyperbolic State Sum Invariants of 3-Manifolds*, arXiv:math/0101234v2, 28 February 2001. https://arxiv.org/pdf/math/0101234v2 . Definition and gauge convention: Section 3.2, PDF p.10; state sum and invariance: Section 4, PDF pp.16–19; tensor factors: Section 8, PDF pp.29–32.
- [O] T. Ohtsuki, ed., *Problems on invariants of knots and 3-manifolds*, Geometry & Topology Monographs 4 (2002), 377–572, published 2004. https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf . Problem 7.20 and its surrounding definitions: printed pp.485–486, PDF pages 113–114 (one-based).
- [B03] S. Baseilhac and R. Benedetti, *Quantum Hyperbolic Invariants Of 3-Manifolds With PSL(2,C)-Characters*, arXiv:math/0306280; Topology 43 (2004), 1373–1423. https://arxiv.org/pdf/math/0306280 . Remark 4.31 records the different Borel symmetrization and phase convention; no identification of the two normalizations is needed in this proof.
