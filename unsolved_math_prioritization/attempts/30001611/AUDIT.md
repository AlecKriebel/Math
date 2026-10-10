# Audit of the bicyclic endpoint growth partial result

## Decision

This is an AI-assisted independent internal mathematical audit. Its acceptance is limited to the rigorous partial result stated below. The proof and audit are unrefereed; no external human peer review or formal proof-assistant certification is claimed.

Accepted as a rigorous partial result for problem 30001611 / OWR-4531-003. No substantive mathematical correction is required in the audited manuscript. The original counterexample or universal cyclicity problem is not solved by this result.

The acceptance covers the complete arguments in Sections 1–7 of the submitted mathematics: the weighted Hilbert shift, the augmentation-ideal Banach operator, the bounded analytic coefficient functionals, their annihilation of the complete cutoff classes, the quantitative separation, infinite-dimensional quotients, localization, and cyclicity of the Banach defect quotient. It does not rely on finite computations to establish any infinite-dimensional assertion.

In particular, the following distinctions are essential to this acceptance:

- The vector `z−1` is bicyclic and is not cyclic for the operator on the augmentation ideal. Failure of that particular vector does not decide whether another vector is cyclic.
- The cutoff ideal is a proper subspace of infinite codimension in that ideal. This proves a failure of the density identification used in the subendpoint argument.
- The induced operator on the defect quotient is itself cyclic. That quotient cannot supply the claimed noncyclic counterexample.
- Cyclicity of the full augmentation-ideal operator and of the critical Hilbert shift remains undetermined by the submitted argument.
- The endpoint ideal phenomenon is classical. No novelty, priority, exhaustive search, or present global-open-status conclusion is accepted or asserted.

## 1. Exact target and source comparison

The target concerns a bounded invertible operator T on a complex separable Banach space X. There must exist a vector with dense linear span under all integer powers of T. For some integer k≥0 the operator norms must satisfy

\[
\|T^n\|=O(n^k),\qquad \log\|T^{-n}\|=O(\sqrt n),
\]

and the unit circle must not be contained in the point spectrum of the Banach adjoint T*. The requested counterexample would also have to lack every cyclic vector, where cyclic uses only nonnegative powers. The alternative is a cyclicity theorem covering all these hypotheses.

This restores both the forward polynomial bound and the adjoint condition from Theorem 2 of the original report. The report first states the little-o theorem, then asks about replacing its inverse-growth condition by the displayed big-O bound. The condition on the point spectrum is noncontainment of the whole circle, not disjointness. The original source pages were checked in text and in rendered images. The 2007 note states the corresponding operator theorem and identifies the Hilbert square-root-weight model in Conjecture 3.3. [Original report](https://ems.press/content/serial-article-files/46308), [2007 primary note](https://www.numdam.org/item/10.1016/j.crma.2007.02.008.pdf).

Every constructed operator asserted to meet the target hypotheses does so with k=0. The endpoint rate is genuine: the normalized inverse logarithmic growth tends to 1, rather than to 0. No use of the little-o theorem at its excluded endpoint occurs.

## 2. Weighted spaces and operator norms

Let w(j)=exp(sqrt(max(−j,0))) for j∈Z. For integers j,l,

\[
\max(-j-l,0)\leq\max(-j,0)+\max(-l,0),
\]

and the square root of a sum is at most the sum of the square roots. These inequalities give w(j+l)≤w(j)w(l). Consequently convolution of coefficient sequences is bounded on the weighted ℓ¹ space, and absolute Fourier convergence identifies that space with a unital Banach algebra A of continuous functions. Density of finite sequences gives separability. The weighted ℓ² space H is a complex separable Hilbert space continuously embedded in ordinary L², since w≥1. There is also a continuous embedding A⊆H because the ℓ² norm of a sequence is no larger than its ℓ¹ norm.

Multiplication by z sends the coefficient at j to j+1. For either weighted sequence norm and any integer q,

\[
\|S^q\|=\sup_{j\in\mathbb Z}\frac{w(j+q)}{w(j)}.
\]

The upper bound follows termwise, and individual coordinate vectors establish the reverse inequality. For q=n≥0 every ratio is at most 1, with equality for j≥0. For q=−n,

\[
\sqrt{\max(n-j,0)}-\sqrt{\max(-j,0)}\leq\sqrt n,
\]

and j=0 attains equality. Thus the exact norms are 1 and exp(√n), respectively. Invertibility is immediate from bounded multiplication by z⁻¹. Applying the spectral-radius formula to S and S⁻¹, with the standard inverse-spectrum identity, puts the spectrum inside the unit circle. This is not an inference that a spectrum of a restriction is automatically contained in its ambient spectrum; the restriction is separately treated below.

The constant vector 1 has all Laurent monomials in its two-sided orbit, so it is bicyclic on H. For a continuous complex-linear functional φ on H, put b_j=φ(z^j). Continuity is equivalent to square summability of b_j/w(j). If S*φ=λφ, invertibility gives λ≠0 and b_j=λ^j b_0 for all j. The spectral bounds force |λ|=1. Since w(j)=1 on every j≥0, a nonzero b_0 would make the positive part of this dual sequence nonsummable. If b_0=0 all b_j vanish and density forces φ=0. Hence the adjoint point spectrum is empty. The duality convention in the manuscript is consistent; no complex conjugation is missing from its complex-linear Fourier pairing.

Verdict: the Hilbert model satisfies every required structural, norm-growth, and spectral hypothesis. No cyclicity decision for this model follows.

## 3. The augmentation ideal and its adjoint spectrum

Evaluation at 1 is continuous on A. Its kernel I is a closed complex separable Banach space invariant under both multiplication operators z and z⁻¹. The resulting restriction T is invertible.

For density of the principal ideal, any φ∈A* annihilating (z−1)A satisfies φ(z^{j+1})=φ(z^j) for every integer j. It is therefore a constant multiple of evaluation at 1 on the dense Laurent polynomials and hence on A. The annihilator characterization of closed subspaces, or Hahn–Banach separation, gives

\[
\overline{(z-1)A}=I.
\]

Approximating each multiplier in A by Laurent polynomials proves that v=z−1 is bicyclic on I. There is no assumption that the unclosed range (z−1)A already equals I.

The restricted positive powers are contractions; every z^n v, n≥0, has A-norm 2. Thus ||T^n||=1. For n≥1 the test vector v gives

\[
\frac{e^{\sqrt{n-1}}+e^{\sqrt n}}2
\leq\|T^{-n}\|\leq e^{\sqrt n}.
\]

The lower expression is at least e^{√n}/2. After logarithms and division by √n this proves the claimed limit 1. The same upper growth estimates independently place the spectrum of T inside the unit circle.

For each ζ on the unit circle other than 1, evaluation at ζ is a continuous nonzero eigenfunctional on I, with eigenvalue ζ. To exclude 1, the Cesàro averages C_N=N⁻¹Σ_{j=0}^{N−1}T^j have norms at most 1. On the dense subset (z−1)A their values are (z^N−1)g/N, whose norm is at most 2||g||/N. Uniform boundedness of the averages extends convergence to zero to all of I. An eigenfunctional at 1 would be fixed under all these averages and must therefore vanish. There are no eigenvalues off the circle by the previously established spectral inclusion.

Verdict: σ_p(T*)=T\{1}, exactly as stated. This meets the source hypothesis despite having many adjoint eigenvalues. The displayed bicyclic vector fails to be cyclic because all its forward translates have no negative Fourier coefficients; the nonnegative-coefficient subspace is closed and does not exhaust I. No inference about all other vectors is justified or made.

## 4. Analytic coefficient estimates and continuity of the functionals

For 0<a<1/8, write V_a(z)=exp(a(1+z)/(1−z)) and U_a(z)=exp(−a(1+z)/(1−z)). Their coefficients are v_m(a) and u_m(a). Since the Cayley transform has positive real part in the disk, |U_a|≤1. Parseval on circles of radius r<1 gives Σ|u_m|²r^{2m}≤1. Monotone convergence establishes Σ|u_m|²≤1, so in particular |u_m|≤1 and u_m→0.

For V_a, Cauchy's bound on |z|=e⁻ˢ gives

\[
|v_m|\leq\exp\left(ms+a\frac{1+e^{-s}}{1-e^{-s}}\right)
\leq\exp(a+ms+2a/s).
\]

Here the real-part bound on the Cayley transform and eˢ−1≥s justify both inequalities. Choosing s=√(2a/m), for m≥1, yields

\[
|v_m|\leq e^a e^{2\sqrt{2am}}.
\]

Thus c=2√(2a)<1. The strict parameter inequality is important: the submitted summability argument is not being extended to a=1/8. The series Σexp(−2(1−c)√m) converges, for example by grouping m between consecutive squares. It follows that (v_m e⁻√m)_{m≥1}∈ℓ².

For f=Σa_jz^j, the functional

\[
L_a(f)=\sum_{m\geq0}v_m a_{-m}-\sum_{m\geq0}u_m a_m
\]

is consequently absolutely convergent and continuous on H by two applications of Cauchy–Schwarz. Its coefficient at index zero is v_0−u_0=e^a−e⁻ᵃ, not v_0 alone. On weighted ℓ¹, the dual norm is the supremum of coefficient magnitude divided by weight. For negative indices that ratio is at most e^a exp(−(1−c)√m)≤e^a; for positive indices it is at most 1; the constant coefficient has magnitude less than e^a. Therefore ||L_a||_{A*}≤e^a.

Verdict: all stated coefficient, norm, and convergence estimates hold on the full spaces, including the constant coefficient and both tails. No formal-series-only argument is used.

## 5. Annihilation on the entire cutoff classes

Let f∈H vanish almost everywhere on an open arc containing 1. For each r<1, ordinary L² Fourier pairing with the smooth functions V_a(rz) and U_a(r\bar z) gives

\[
\int f(z)V_a(rz)\,dm=\sum_{m\geq0}v_m r^m a_{-m},\qquad
\int f(z)U_a(r\bar z)\,dm=\sum_{m\geq0}u_m r^m a_m.
\]

These are bilinear integrals with no inserted conjugation. Both series tend to their r=1 sums by the established absolute convergence. Outside the fixed arc, both analytic factors converge uniformly as r→1, since their singularity is confined to 1. An L² function on the finite-measure circle belongs to L¹, so uniform convergence suffices to pass to the integrals on that complement. For z on the unit circle different from 1,

\[
\frac{1+\bar z}{1-\bar z}=-\frac{1+z}{1-z},
\]

hence V_a(z)=U_a(\bar z). The two limiting integrals are equal, proving L_a(f)=0. The proof applies to every such H function, not just smooth examples. Continuity extends it to J_H, the H-closure of that class. The embedding A⊆H and A-continuity give the corresponding conclusion for J_A.

The raw cutoff classes are linear: the intersection of two arcs containing 1 is again a neighborhood of 1. They are invariant under z and z⁻¹; in A the class is also an ideal. Taking the respective closures preserves these properties. Since evaluation at 1 is continuous on A, J_A⊆I.

Using v_0=e^a, u_0=e⁻ᵃ, and u_1=−2ae⁻ᵃ gives

\[
L_a(z-1)=(1+2a)e^{-a}-e^a
=e^{-a}(1+2a-e^{2a})<0.
\]

The strict sign follows from e^{2a}>1+2a. The functional therefore separates z−1 from J_A and also separates that vector from J_H. For every h∈J_A,

\[
\|z-1-h\|_A\geq\frac{|L_a(z-1)|}{e^a}
=1-(1+2a)e^{-2a}.
\]

At a=1/32, using e^{2a}−1−2a≥2a² and e⁻²ᵃ≥1−2a gives

\[
\operatorname{dist}_A(z-1,J_A)\geq2a^2(1-2a)=\frac{15}{8192}.
\]

Every inequality has the required direction, and the bound is positive. It is a lower bound, not an asserted exact distance.

Verdict: the annihilation and separation claims are accepted in their infinite-dimensional form.

## 6. Infinite codimension

Suppose a finite linear combination L=Σγ_jL_{a_j}, with distinct parameters, vanishes on I. Since I is the kernel of evaluation at 1, there is a scalar C with L=C ev_1 on A. Evaluating at z^n for n≥1 gives −Σγ_j u_n(a_j)=C. As n→∞ every term on the left tends to zero, so C=0.

The analytic function Σγ_jU_{a_j} then has all positive Taylor coefficients zero and is constant. Along real z→1⁻, each U_{a_j}(z) tends to zero, so that constant is zero. Substituting t=(1+z)/(1−z), and taking real z∈(0,1), gives \(\sum_j\gamma_j e^{-a_jt}=0\) for t>1. Order the parameters increasingly; multiply by e^{a_min t} and let t→∞ to eliminate its coefficient. Induction eliminates all coefficients.

Thus the restrictions to I are linearly independent. They all annihilate J_A, so the continuous dual of I/J_A has arbitrarily large finite independent subsets. A finite-dimensional quotient could not have this property. The argument on H is the same, starting with a combination that vanishes on H and hence omitting C ev_1. It proves infinite dimensionality of H/J_H.

Verdict: the quotient dimension conclusions follow analytically for arbitrarily many distinct parameters. A finite numerical rank observation is neither needed nor substituted.

## 7. Nonzero cutoff functions and the singleton hull

The elementary localization argument is sound. With 1<p<2 and widths εj⁻ᵖ, the sum of widths L is finite. The random series of independent variables supported in [−εj⁻ᵖ,εj⁻ᵖ] converges absolutely, or equivalently the convolution measures converge weakly, to a probability measure supported in [−L,L]. Its integer Fourier coefficients are the products of the corresponding sinc factors.

If N=floor((ε|n|/2)^{1/p}), each factor with j≤N has argument magnitude at least 2 and hence modulus at most 1/2. All other factors have modulus at most 1. Therefore the product is bounded by 2⁻ᴺ. For large |n| this is at most C exp(−d|n|^{1/p}) for positive C,d. The exponent 1/p exceeds 1/2. This bound makes all polynomially weighted Fourier series summable, so the periodized measure has a smooth density. Fourier uniqueness identifies this density with the periodized measure; positivity and total mass one are preserved. The same estimate dominates the asymmetric square-root weight in both the ℓ¹ and ℓ² norms, proving membership in A and H.

Shrinking ε makes the support arbitrarily small. Some point has positive density, and rotation can put that point at any prescribed point of the circle. After rotation the support may move off its old center, but its diameter still tends to zero with ε. For any ζ≠1 it can therefore be kept away from 1 while the density is nonzero at ζ. This produces nonzero cutoff elements and proves that the common zero set of J_A is exactly {1}.

Verdict: the construction proves actual support, smoothness, weighted membership, and nonvanishing at every specified ζ≠1. The proof does not infer support from decay alone.

## 8. Why the defect quotient is cyclic

Every character χ of the unital commutative Banach algebra A is continuous. Put λ=χ(z), which is nonzero because z is invertible. Applying the character norm bound to z^n and z⁻ⁿ gives |λ|≤1 and |λ|≥1 in the limit. Laurent-polynomial density then identifies χ with evaluation at λ. Thus A's character space is the unit circle.

Characters of A/J_A correspond to those of A annihilating J_A. The singleton hull just proved identifies these with evaluation at 1 alone. By the standard spectrum–character relation for a unital commutative complex Banach algebra, the element z+J_A has spectrum {1}. This relation remains valid for a quotient with a nonzero radical; semisimplicity of A/J_A is not being assumed.

The subspace I/J_A is a closed ideal of A/J_A. If λ≠1, the inverse of (z+J_A)−λ exists in the unital quotient. Multiplication by it preserves I/J_A, and supplies a two-sided inverse to R−λ on that ideal, where R is multiplication by z there. Hence σ(R)⊆{1}. The quotient is nonzero by separation, and its bounded operator has nonempty complex spectrum, so σ(R)={1}. Its two-sided orbit of v+J_A is dense by the continuous quotient map and bicyclicity in I.

Let Q=Id−R. Spectral mapping gives r(Q)=0. For any q∈(0,1), the spectral-radius formula gives ||Q^n||≤q^n for all sufficiently large n. The finite initial segment does not affect convergence, so ΣQ^n converges in operator norm. Telescoping its partial sums proves that its sum is R⁻¹. Thus R⁻¹ belongs to the norm closure of the polynomial algebra generated by R; all negative powers do as well. Applying these approximants to v+J_A proves that its forward polynomial orbit has the same closure as its two-sided orbit. It is cyclic.

Verdict: the cyclic quotient argument is correct. It closes, rather than leaves ambiguous, the tempting but invalid step from a localized defect to operator noncyclicity. It uses no unsupported preservation of cyclicity under arbitrary extensions.

## 9. Attribution and limits of the source audit

The 2007 paper's Section 2 explicitly uses the cutoff ideal and, under its little-o assumptions, identifies it with a closed ideal generated by a power of z−1. At k=0 this is the identification contradicted by the endpoint separation above. The comparison is therefore precise. The six-page note was read in full; it announces results and describes the method, and should not be represented as containing all proofs of the longer article. [2007 note](https://www.numdam.org/item/10.1016/j.crma.2007.02.008.pdf).

Atzmon's 1980 Section 7, especially the example spanning printed pages 54–55, gives the same one-sided square-root-weight Fourier algebra and discusses its nontrivial primary ideals with singular-inner-function generators. The relevant pages and displayed weight were inspected. The submitted credit is appropriate. The present audit verifies the manuscript's self-contained calculations; it does not certify that any formula or observation is new. [Atzmon primary paper](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6271-11511_2006_Article_BF02392120.pdf).

The publisher's page confirms the longer article's title, authors, journal volume, pages, and DOI. It is an abstract/metadata preview. Its full text was not obtained or inspected in this audit, and no proof from it is needed for the accepted partial. This limitation does not invalidate the self-contained argument, but it prevents a full comparison with that article. [Publisher record](https://link.springer.com/article/10.1007/s00208-007-0191-2).

No search for a new solution was performed in this audit, and no conclusion about whether the original conjecture has subsequently been resolved is drawn.

## 10. Verification and final scope

The accepted original mathematical manuscript was authenticated before the audit. It has 15,375 bytes and SHA-256 9454aa2fa26759ac1d85dc20f82a801f324b11f4fcef599cace059d473ada381. This prose edition adds only an explicit internal AI-review statement to that manuscript; its mathematical body, citations, and scope limitations are unchanged. ACCEPTANCE.json distinguishes the accepted originals from the distributed editorial versions.

Independent exact finite controls use a different coefficient recurrence derived from the exponential differential equation. They check normalized coefficients and inverse products through degree 96 for five rational parameters, integer inputs underlying the weight inequalities, the boundary reflection sign, and the rational distance constant. An alternating Taylor interval independently confirms that the stated distance bound is conservative. Seven deliberately wrong finite identities or parameter claims are rejected. Normal, optimized, and double-optimized Python runs produce identical results. These tests are consistency checks; the acceptance of annihilation, dimension, spectra, and cyclicity follows from the proofs above.

The only unresolved mathematical obligation is the original one: prove absence of every possible cyclic vector in a qualifying endpoint operator, or prove universal cyclicity under all endpoint hypotheses. Neither has been supplied. No corrective patch is required for the partial theorem as stated, and no full-resolution acceptance is granted.
