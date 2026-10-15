# A checkable prior-theorem implication for the unrestricted ugly-set question

Independently authored audit deduction, 12 October 2026 (America/Los_Angeles).
PR #615; problem 4200010 / AMR-041-0010. This proof is an audit artifact, not a claim of new mathematics or a claim that its exact conclusion was explicitly published in 1993.

## Exact claim and assumptions

Interpret almost periodicity in the Koopman sense: every vector in the complex L2 space of the restricted invariant Liouville measure has a relatively compact time orbit. A good region is a measurable invariant *subset*, not a discrete-spectrum factor. A bad point has a positive tangent Lyapunov exponent. The target is the existence of an autonomous smooth Hamiltonian system whose complement of good and bad has positive full phase-space Liouville measure. No Euclidean, mechanical, analytic, contact, or genericity requirement is assumed.

**Claim.** The Anzai skew shift and cosymplectic thickening give a connected smooth symplectic four-manifold with globally real Hamiltonian and complete flow, finite total Liouville volume one, every tangent Lyapunov exponent zero at every point, and no positive-measure invariant good region. Every regular energy surface is compact, ergodic, and non-almost-periodic with its Liouville conditional measure. There is also a compact ambient version with a positive-volume band having these properties.

The older inputs are independently authenticated in SOURCE_LEDGER.md. The rest of this document supplies all connecting deductions explicitly. In particular it does not infer zero Lyapunov exponents merely from zero entropy, or the absence of positive good regions merely from the existence of continuous spectrum in a direct integral.

## 1. Anzai map and the particular Fourier obstruction

Fix any irrational a, for instance a=sqrt(2), and define on R²/Z²

    F(x,y) = (x+a, y+x).

The integer lattice is respected, F is invertible, and its derivative is

    A = [[1,0],[1,1]].

Since det A=1, F preserves sigma=dx∧dy and normalized Haar measure m. For every integer n, including negative n,

    F^n(x,y) = (x+n a, y+n x+a n(n-1)/2),
    DF^n = [[1,0],[n,1]].

The forward recurrence proves the first formula, and its reversible recurrence proves it for negative n as well. For the Fourier basis e_(k,l)=exp(2πi(kx+ly)),

    U_F e_(k,l) = exp(2πik a) e_(k+l,l).

If f∈L²(m) is invariant, its coefficients have equal moduli on each orbit (k+n l,l). For l≠0 the orbit contains infinitely many distinct indices, so square summability forces every coefficient on it to vanish. For l=0, invariance forces the k coefficient to vanish unless exp(2πik a)=1, which irrationality permits only at k=0. Hence F is ergodic.

Set g(x,y)=exp(2πiy). Then

    U_F^n g = exp(2πi[y+n x+a n(n-1)/2]).

For distinct n,m, integration in x gives <U_F^n g,U_F^m g>=0. Norms are one. Thus this orbit has pairwise distance sqrt(2), and cannot be relatively compact. This is an explicit obstruction within the classical map, consistent with Anzai's theorem; no general spectral-equivalence theorem is required.

## 2. Constant-roof suspension and its volume

Let

    N=(T²×R)/((z,t)~(Fz,t-1)).

The integer action is free and properly discontinuous because it translates t by integers. It gives a compact connected smooth mapping torus. A fundamental domain T²×[0,1) has seams of zero volume. The F-invariant sigma and dt descend to closed forms beta and tau on N. The form nu=beta∧tau is a positive volume form with integral one.

The vector field R=∂t descends. Its complete volume-preserving flow is

    psi_s[z,t]=[z,t+s].

At integer times its fundamental-domain formula is

    psi_n[z,t]=[F^n z,t].

This fixes the sign convention and first-return map: [z,1]=[Fz,0]. The field satisfies i_R beta=0 and tau(R)=1, hence is the Reeb field of this cosymplectic pair.

**Ergodicity for the full real flow.** An L² function invariant under every psi_s has zero distributional t derivative in each product chart. Indeed flow invariance gives equality after all sufficiently small t translations, and integrating against compactly supported smooth test functions and differentiating in s proves that derivative is zero. It is therefore w(z), independent of t almost everywhere on (0,1). Invariance under time one, using psi_1[z,t]=[Fz,t], gives w(Fz)=w(z) almost everywhere, so Section 1 makes it constant. No matching of arbitrary L² representatives across the measure-zero seam is assumed. Conversely a constant is invariant. This argument uses all times; the time-one map alone is not ergodic, because it preserves t.

Define the measurable fundamental-domain function

    G([x,y,t])=exp(2πiy), 0≤t<1.

It need not agree at the seam, because it is an L² observable, not a proposed smooth function. The integer-time formulas and integration over t give

    <G∘psi_n,G∘psi_m>_(L²(N,nu)) = delta_(n,m).

Consequently every energy fiber below will already fail almost periodicity. This is not an artifact of varying integrable frequencies over different energies.

## 3. Finite-total-volume real Hamiltonian thickening

First apply the old cosymplectic thickening on N×R, then restrict to the invariant open submanifold

    M=N×(0,1),
    omega=beta+tau∧dE,
    H(q,E)=E.

The coordinate E is now globally real, so H has no circle-coordinate defect. M is a connected smooth manifold without boundary. It is noncompact, but its Liouville measure is finite:

    omega²/2 = beta∧tau∧dE = nu∧dE,
    mu(M)=1.

The form omega is closed and its displayed volume is nonzero, so omega is symplectic. Use i_(X_H) omega=dH. Direct contraction gives i_R omega=dE, hence X_H=R and

    Phi_s(q,E)=(psi_s q,E).

The flow is complete for every real s; it never moves E toward either omitted endpoint, and R is complete on compact N. Noncompactness therefore creates neither an escape issue nor an infinite-measure normalization issue.

Every e∈(0,1) is a regular value, because dH=dE≠0. The full level is the compact connected hypersurface N×{e}. Disintegration of mu=nu∧dE by the real H coordinate has conditional measure exactly nu. Equivalently, contraction of the volume with ∂E gives -nu; the induced positive measure is nu. No arbitrary Riemannian surface-area measure is being substituted for a Hamiltonian conditional measure. The conditional system is psi, so Section 2 gives ergodicity and failure of almost periodicity on every such level.

## 4. All tangent exponents, including energy, are zero

The following frame on the covering space descends to M:

    V1=∂x-t∂y, V2=∂y, V3=∂t, V4=∂E.

For the gluing map D(x,y,t,E)=(x+a,y+x,t-1,E), its derivative sends V1(t) to ∂x+(1-t)∂y=V1(t-1) and fixes V2,V3,V4. Integer x,y translations also preserve the frame. Equip M with the smooth metric making this frame orthonormal. It is independent of E.

In this frame, the exact derivative for every real s is

    D Phi_s V1 = V1+s V2,
    D Phi_s Vj = Vj, j=2,3,4,

where the right frame is at the image point. Thus D Phi_s=I+sL, where L(V1)=V2 and L vanishes on the other frame vectors; L²=0 and ||L||=1. The inverse is I-sL. For all v≠0,

    ||v||/(1+|s|) ≤ ||D Phi_s v|| ≤ (1+|s|)||v||.

After logarithms and division by positive s→∞, both bounds tend to zero. Every vector exponent exists and equals zero at every point. Singular-value exponents have the same bounds; there is no positive Pesin exponent. The derivative and inverse bounds also supply the needed integrability in the chosen normalized finite-measure system.

This is metric independent despite the noncompact ambient: each orbit lies in the compact set N×{e}, on whose full tangent bundle any two smooth metrics are uniformly equivalent. In particular this controls transverse energy vectors evaluated along the orbit, not just tangent vectors to that hypersurface.

## 5. Every positive-measure invariant region fails almost periodicity

Let C⊂M be measurable and invariant modulo mu-null sets under all Phi_s, with mu(C)>0. Its indicator is L² because mu(M)=1. For each rational s, invariance and Fubini show that the section 1_(C_e)∈L²(N,nu) is psi_s-invariant for almost every e. Intersect these full-measure sets over rational s.

The compact smooth volume-preserving flow gives a strongly continuous Koopman group on L²(N,nu): it is continuous first on continuous functions, by uniform continuity on compact N, and then on all L² by density and unitarity. Rational invariance therefore extends to all real times for almost every e. Ergodicity of psi makes 1_(C_e) either zero or one almost everywhere. The function e↦nu(C_e) is measurable, so for a measurable J⊂(0,1),

    C=N×J modulo null sets,
    mu(C)=Leb(J)>0.

The restriction of G to C has norm sqrt(mu(C)), and its integer-time translates are orthogonal there:

    <G∘Phi_n,G∘Phi_m>_(L²(C,mu|C)) = mu(C) delta_(n,m).

Normalize by mu(C)^(-1/2). These are norm-one vectors with pairwise distance sqrt(2), disproving relative compactness. Thus C is not a good region.

Every measurable invariant good region has zero measure; the bad set is empty. With the source's measurable, modulo-null convention for a maximal good set, the ugly set consequently has mu measure one. The nonconstant clock eigenfunctions exp(2πit) do not change this conclusion: a pure-point factor is not a positive invariant subset on which every L² orbit is precompact.

For completeness, on the old unrestricted thickening N×R the same band N×(0,1) already has finite positive full four-dimensional Liouville measure. If an ambient good region intersected that band in positive measure, its intersection would be good: restriction to an invariant subset is a bounded intertwining projection and carries precompact orbits to precompact orbits. This contradicts the argument above. Hence even infinite ambient volume would not defeat positive ugly measure, but the restricted ambient M avoids that issue altogether.

## 6. Compactness alone changes no conclusion

If an additional compact-ambient condition were imposed, set

    M_c=N×S¹, omega_c=beta+tau∧dE.

Here dE denotes the global length form on R/Z, not the differential of a globally real circle coordinate. The older paper already remarks on an S¹ thickening; closedness and omega_c²/2=nu∧dE verify it directly. Total volume is one.

A global real H must not be written H=E on all of S¹. Construct it as follows. Choose a nonnegative smooth symmetric single-bump function b supported inside (1/3,2/3), strictly increasing then decreasing on its support, and normalize its integral to one. Such a b is obtained by normalizing

    exp(-1/[(E-1/3)(2/3-E)]) for 1/3<E<2/3,
    0 otherwise.

Let f(E)=1-b(E) and h(E)=∫_0^E f(u)du on [0,1]. Since ∫_0^1 f=0 and f is periodic and smooth, h extends to a globally smooth real function on S¹. Near 0 it is E, and near 1 it is E-1, so the values and every derivative match across the seam. Put H_c(q,E)=h(E).

The flow is Phi_s^c(q,E)=(psi_(s h'(E))q,E). On J=(0,1/4), h(E)=E, h'=1, and h''=0. Thus B=N×J has Liouville volume 1/4, and all preceding arguments apply without alteration on B.

These band energies can be taken to be globally regular values as well. The bump is unimodal; f crosses zero twice. The maximum of h occurs after E=1/3 and is greater than h(1/3)=1/3. Its minimum occurs before E=2/3 and is below h(2/3)=-1/3. They are the only critical values, so every e∈(0,1/4) is a globally regular value. The connected component E=e has conditional measure nu after normalization. Extra components elsewhere do not affect it.

Even away from the band, the full derivative in the global frame is

    D Phi_s^c = I+s h'(E)L+s h''(E)K,

where L(V1)=V2, K(V4)=V3 and both kill all other frame vectors. The products L²,K²,LK,KL vanish. Because h',h'' are bounded on S¹, both derivative and inverse are bounded by 1+C|s| uniformly. Hence every tangent exponent is zero on the compact ambient too. The band alone already supplies the required positive ugly measure, because any ambient good region meeting it in positive measure would restrict to a forbidden good region in B.

## 7. Precise limits of the priority inference

The deductions above leave no mathematical gap for the exact unrestricted question under the stated Koopman interpretation. Compactness, finite total volume, full tangent exponents, positive invariant subregions, and correct energy disintegration all survive.

This proves that the requested example is an elementary consequence of specific pre-2000 published mechanisms. It does **not** prove that Anzai or de León–Saralegi explicitly formulated the later Knill ugly-set question or published this exact combination as its answer. An earlier explicit resolution is a bibliographic claim requiring an earlier explicit source. No such source is established by this review.

If novelty is defined as the first explicit observation of this connection, that narrow historical proposition remains unverified. It cannot support framing the PR as a new original resolution of a mathematically still-unsolved unrestricted existence problem. A carefully attributed expository note remains mathematically repairable. A new solution under Euclidean, analytic, mechanical, contact, robust, or weak-mixing restrictions would require a materially different theorem and a new scope; none is supplied here.
