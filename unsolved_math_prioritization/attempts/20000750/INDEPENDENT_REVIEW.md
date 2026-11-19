# Independent adversarial mathematical review

Review date: 2026-10-21 (UTC). This review independently rederives the finite-dimensional and Hilbert-space claims below. It makes no novelty claim, does not certify the literature search, and does not establish an asymptotic arithmetic improvement or a new prime-gap bound. Section 9 additionally verifies a strictly finite arithmetic example.

## 1. Review scope and public-artifact binding

This is an editorial public projection of the authored mathematical review dated 21 October 2026. Its derivations and mathematical conclusions are retained. Non-public provenance bindings have been removed; the projection is not a new independent mathematical review. Section 9 binds the safe authored artifacts actually checked. The package manifest binds this projected review and the other included public artifacts.

## 2. Verdict and defects

**Mathematical verdict: the exact Gram criterion, continuous radial non-eigenfunction theorem, residual gain formula, and displayed example constants are correct under their stated real-valued, continuous-profile, standard-simplex hypotheses.**

One genuine proof omission needs repair: the earlier proof restricts a radial identity to a measure-zero boundary slice. If “radial” means equality almost everywhere, as appropriate to the surrounding L² formulation, this restriction does not follow without a continuous-representative argument. Section 4 below supplies that argument. `RECOVERY_GATE.md` correctly identifies the omission and does not itself supply the full argument. The omission does not furnish a counterexample to the theorem.

Two scope/wording cautions matter:

1. When the Gram residual has zero A-norm, the proposed coefficient direction contributes no *independent normalized weight*. It can rescale the baseline divisor sum and hence its square. Thus “adds no new weight” should not be read as saying the numerical weight values cannot change.
2. An optimal combination in the span of two coefficient vectors need not remain in the original product-local family. The exact test certifies the unrestricted linear span being considered; it does not classify or optimize a nonlinear coefficient family unless closure/admissibility is separately proved. In particular, zero cross term and a smaller second diagonal entry reject this plane, not every product-local perturbation.

No incorrect displayed numerical constant or invalid algebraic identity was found in the audited claims. The signed-weight budget was also checked and is correct. The recovered claims should remain partial functional-level progress, not a complete solution of the historical alternative-weight question.

## 3. Exact Gram and two-plane criterion

Let Φ have entries φ_d(n), let Q be the diagonal matrix with nonnegative entries q(n), and work over real scalars. Then

\[
A=\Phi^{T}\Phi,\qquad B=\Phi^{T}Q\Phi.
\]

Consequently both forms are positive semidefinite and, for λ with λᵀAλ>0,

\[
\mathscr R(\lambda)=\frac{\lambda^TB\lambda}{\lambda^TA\lambda}.
\]

If zᵀAz=0, then Φz=0, hence Az=Bz=0. This last implication, which need not hold for arbitrary unrelated positive-semidefinite A and B, holds for the specified Gram pair and justifies taking the quotient by ker A.

Take a=uᵀAu>0, c=uᵀAv, z=v−(c/a)u, and b=zᵀAz. If b=0, every vector xu+yv has the same image under Φ as (x+yc/a)u. Every nonzero image therefore has the baseline quotient, although the weights may be multiplied by a square scalar.

If b>0, u/√a and z/√b are A-orthonormal. In this basis the compressed numerator matrix is

\[
C=\begin{pmatrix}q_0&s\\s&q_1\end{pmatrix},
\quad q_0=\frac{u^TBu}{a},\quad
q_1=\frac{z^TBz}{b},\quad
s=\frac{u^TBz}{\sqrt{ab}}.
\]

The maximum quotient is exactly

\[
\lambda_+=\frac{q_0+q_1+\sqrt{(q_0-q_1)^2+4s^2}}2.
\]

If s≠0, the square root is strictly greater than |q₀−q₁|, giving λ₊>q₀. If s=0, λ₊=max(q₀,q₁). This proves the advertised necessary-and-sufficient criterion, including its equality cases.

Writing d=vᵀAv, α=uᵀBu, β=uᵀBv, γ=vᵀBv gives independently

\[
b=d-\frac{c^2}{a},\quad q_0=\frac{\alpha}{a},\quad
s=\frac{\beta-c\alpha/a}{\sqrt{ab}},\quad
q_1=\frac{\gamma-2c\beta/a+c^2\alpha/a^2}{b}.
\]

These are the six-moment formulas under review. No asymptotic or arithmetic estimate is hidden in this linear-algebra step.

## 4. Operator and the continuous-representative repair

Let

\[
\mathcal R_k=\{t_i\ge0:\ S=\sum_i t_i\le1\},\qquad k\ge2,
\]

with Lebesgue measure. For fixed coordinates other than t_i, put x=Σ_{j≠i}t_j. Define T_iF by integrating F in t_i over [0,1−x]. Cauchy–Schwarz on that interval yields

\[
|T_iF|^2\le(1-x)\int_0^{1-x}|F|^2\,dt_i
\le\int_0^{1-x}|F|^2\,dt_i.
\]

After integration over the other coordinates, ||T_i||≤1. Its adjoint lifts a function of the other coordinates to a function constant in t_i along its fibre. Thus

\[
\mathcal L=\sum_iT_i^*T_i,\qquad
0\le\mathcal L\le kI,\qquad
\langle F,\mathcal LF\rangle=\sum_i\|T_iF\|^2.
\]

This verifies boundedness, self-adjointness, positivity, and the claimed quadratic-form representation.

### Continuous radial representative lemma

Suppose U is continuous on the closed simplex and U(t)=h(S) for almost every t, with h measurable. Then there is a continuous function h₀ on [0,1] for which U(t)=h₀(S) at **every** point of the closed simplex.

Proof: write t=s z, where 0<s<1 and z belongs to the probability simplex

\[
\Delta=\{z_i\ge0:\ \sum_i z_i=1\}.
\]

Using z₁,…,z_{k−1} as independent variables, the absolute Jacobian is s^{k−1}. Fubini therefore implies that for almost every s∈(0,1), U(sz)=h(s) for almost every z∈Δ. For each such s, continuity in z makes this identity valid for all z∈Δ: a continuous function which is zero almost everywhere on Δ is zero everywhere, including its boundary by density.

Let z_*=(1/k,…,1/k) and set h₀(s)=U(sz_*). This is continuous on [0,1]. The full-measure set of good s is dense in (0,1). For arbitrary fixed z, approximate any s∈[0,1] by good s and use continuity of U and h₀. One obtains U(sz)=h₀(s). At s=0 all points sz coincide, so there is no remaining exceptional case. This proves the lemma.

This lemma is the missing justification before the original proof uses the boundary slice. It applies to U=LF whenever G∈C([0,1]), since the formula in the next section makes LF continuous. It also applies to equality LF=qF, although that case is simpler: two continuous functions equal almost everywhere are equal everywhere on this simplex.

## 5. Exact radial characterization and non-eigenfunction result

Let F(t)=G(S), with G∈C([0,1]), and define

\[
H(x)=\int_x^1G(u)\,du.
\]

Directly in each fibre,

\[
\mathcal LF(t)=\sum_{i=1}^kH(S-t_i).
\]

The displayed function is continuous on the closed simplex. If it is radial almost everywhere, the preceding lemma makes it constant on each S-slice pointwise. Thus, for 0<s<1 and 0<x<s, the value at t=(x,s−x,0,…,0) is

\[
H(x)+H(s-x)+(k-2)H(s),
\]

and is constant in x. Because H is continuously differentiable, differentiation gives H′(x)=H′(s−x). Hence H′(x)=H′(y) whenever x,y>0 and x+y<1. Given any x,y∈(0,1), choose z with 0<z<min(1−x,1−y); then H′(x)=H′(z)=H′(y). Therefore G=−H′ is constant on (0,1), and continuity extends this to [0,1].

Conversely, if G=c, then H(x)=c(1−x), giving

\[
\mathcal LF(t)=c\bigl(k-(k-1)S\bigr),
\]

which is radial. This proves the exact equivalence with radiality understood either pointwise or almost everywhere.

If G is nonconstant, LF cannot be any scalar multiple of F, because the latter is radial. If G=c≠0, the preceding affine expression is not constant for k≥2 and again cannot equal a scalar multiple of F. Thus no nonzero continuous radial profile is an eigenfunction of the full operator. This argument specifically uses k≥2: when k=1, nonzero constants are eigenfunctions.

## 6. Residual direction and exact gain

For any nonzero continuous radial F, set

\[
a=\|F\|^2,\quad q=\frac{\langle F,\mathcal LF\rangle}{a},\quad
r=\mathcal LF-qF,\quad b=\|r\|^2.
\]

A continuous nonzero G gives a>0. By definition, ⟨F,r⟩=0. The non-eigenfunction result proves b>0. Self-adjointness then gives

\[
\langle F,\mathcal Lr\rangle
=\langle\mathcal LF,r\rangle=b.
\]

In the orthonormal basis F/√a,r/√b, the compressed operator is exactly

\[
\begin{pmatrix}q&\sqrt{b/a}\\\sqrt{b/a}&\tau\end{pmatrix},
\qquad \tau=\frac{\langle r,\mathcal Lr\rangle}{b}.
\]

Its maximum quotient is

\[
\Lambda_+=\frac{q+\tau+\sqrt{(q-\tau)^2+4b/a}}2>q.
\]

The direct quotient expansion independently verifies the sign:

\[
\mathscr M(F+\varepsilon r)-q
=\frac{b\bigl(2\varepsilon+\varepsilon^2(\tau-q)\bigr)}{a+\varepsilon^2b}.
\]

In particular, 0≤q,τ≤k, so every 0<ε<2/k is an explicit sufficient choice for strict improvement. This is only a convenient conservative bound, not an optimal step size.

For nonconstant G, r is nonradial: if it were radial, LF=r+qF would be radial, contradicting Section 5. For constant G, r is radial, as stated above; such F is not stationary even within the radial class.

If F is stationary under all radial variations, differentiation gives ⟨h,r⟩=0 for each such h. The radial L² subspace is identified with

\[
L^2\left([0,1],\frac{s^{k-1}}{(k-1)!}\,ds\right),
\]

and continuous functions are dense there. Therefore the conclusion is orthogonality to the whole radial L² subspace even if the initially allowed variations were only continuous. Since r≠0, it cannot itself belong to that subspace. This completes the stationary-profile version without assuming that a restricted maximizer exists.

These are variational conclusions. No arithmetic transfer or admissibility in the exact historical product-local family follows from the residual formula alone.

## 7. Independent checks of example constants

The simplex identity used throughout is

\[
\int_{\mathcal R_k}f(S)\,dt
=\frac1{(k-1)!}\int_0^1s^{k-1}f(s)\,ds.
\]

It follows either by scaling the volume {S≤s}=s^k/k! or by the same simplex coordinates used in Section 4.

### 7.1 Constant profile F=1

Here a=1/k!, LF=k−(k−1)S, and under normalized simplex volume

\[
\mathbb ES=\frac{k}{k+1},\qquad
\operatorname{Var}S=\frac{k}{(k+1)^2(k+2)}.
\]

Hence

\[
q=\frac{2k}{k+1},\qquad
r=(k-1)\left(\frac{k}{k+1}-S\right),\qquad
\frac ba=\frac{k(k-1)^2}{(k+1)^2(k+2)}.
\]

To check τ independently rather than infer it from an asserted operator identity, integrate r along one coordinate. With x=Σ_{j≠i}t_j,

\[
T_ir(x)=\frac{k-1}{2(k+1)}(1-x)\bigl((k-1)-(k+1)x\bigr).
\]

For k≥2,

\[
\langle r,\mathcal Lr\rangle
=\frac{k}{(k-2)!}\int_0^1x^{k-2}|T_ir(x)|^2\,dx.
\]

The remaining integral satisfies

\[
\int_0^1x^{k-2}(1-x)^2\bigl((k-1)-(k+1)x\bigr)^2\,dx
=\frac{8}{(k+1)(k+2)(k+3)}.
\]

For example, this follows by expanding the squared affine factor and using

\[
\int_0^1x^{m}(1-x)^2\,dx
=\frac{2}{(m+1)(m+2)(m+3)}.
\]

Division by b gives exactly

\[
\tau=\frac{2k(k-1)}{(k+1)(k+3)}.
\]

All three displayed constant-profile formulas are correct.

### 7.2 Linear radial profile F=S

For x=S−t_i,

\[
T_iS=\int_0^{1-x}(x+u)\,du=\frac{1-x^2}{2}.
\]

Summing these expressions yields

\[
\mathcal LS
=\frac{k}{2}-\frac12\sum_i(S-t_i)^2
=\frac{k}{2}-\frac{k-2}{2}S^2-\frac12\sum_it_i^2.
\]

This is genuinely nonradial for every k≥2: on the same slice S=s>0, the values of Σt_i² at (s,0,…,0) and (s/2,s/2,0,…,0) are s² and s²/2. Continuity ensures this is also a failure of almost-everywhere radiality, not merely a boundary anomaly.

Furthermore,

\[
I(S)=\frac1{(k-1)!(k+2)},
\]

and

\[
\sum_iJ_i(S)
=\frac{k}{4(k-2)!}
\left(\frac1{k-1}-\frac2{k+1}+\frac1{k+3}\right)
=\frac{2k}{(k-1)!(k+1)(k+3)}.
\]

Therefore

\[
\mathscr M(S)=\frac{2k(k+2)}{(k+1)(k+3)},
\]

which verifies the stated linear-profile quotient.

### 7.3 Exact arithmetic spot checks

In addition to the symbolic derivations, Python's standard-library `Fraction` arithmetic was used to integrate the explicit polynomials, with no floating-point quadrature and no optional symbolic package. All checks passed at k=2,3,4,5,10,50,100. Representative output:

| k | b/a for F=1 | τ for F=1 | M(S) |
| ---: | ---: | ---: | ---: |
| 2 | 1/18 | 4/15 | 16/15 |
| 3 | 3/20 | 1/2 | 5/4 |
| 4 | 6/25 | 24/35 | 48/35 |
| 5 | 20/63 | 5/6 | 35/24 |
| 10 | 135/242 | 180/143 | 240/143 |

The all-k proofs above, not these finitely many checks, establish the identities.

## 8. Signed-weight check and final scope

For any nonnegative W₊,W₋ with W=W₊−W₋,

\[
\sum_xg(x)W(x)
\le\sum_xg(x)_+W_+(x)+\sum_x(-g(x))_+W_-(x).
\]

Thus strict excess over the second term forces the first term positive and yields a point where g>0 and W₊>0. A point with W<0 and g=−1, with g zero elsewhere, proves that positive signed surplus alone is insufficient. The proposition is valid even if W₊,W₋ were not required to be disjoint Jordan parts.

Acceptance is limited to the audited finite Gram geometry and continuous-profile variational statements, with the explicit representative repair above. The audit does not verify current bibliographic status, novelty, asymptotic arithmetic moment estimates, an optimum over the original nonlinear product-local family, or a new prime-gap theorem. No such claim should be inferred from this report.

## 9. Additional independent audit of the new residual package

The following safe authored artifacts were read and checked. The hashes below incorporate the cutoff-regularity clarification and bind the mathematical acceptance to the included artifacts.

| Included authored artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `RESIDUAL_REPORT.md` | 10442 | `a3007895c78780bb198abe89a78def742edaa9ff41022b91bc07b2adcc68dd80` |
| `verify_exact.py` | 2453 | `92d10513ebc3022d8104afc299e28574476d922ef56f538b1cd36468fa602e0d` |
| `EXACT_CHECKS.json` | 679 | `31918c030c22b6f74c7fab705cf671fda6d832087d4f54de55b5d472a22c1f5e` |
| `EXACT_CHECKS_OPTIMIZED.json` | 679 | `31918c030c22b6f74c7fab705cf671fda6d832087d4f54de55b5d472a22c1f5e` |
| `FINITE_PRODUCT_EXAMPLE.md` | 1276 | `de845f1964cb820a0193ab935a752184cf5643d189535f5adb64b80395ecf25f` |
| `verify_finite_product.py` | 941 | `abe7b239b945e1cc666bfa1f008a19c4a6c0f711bd761387741337c85b75abea` |
| `FINITE_PRODUCT_CHECK.json` | 341 | `2cec69204f85b35b5138a520f3ccdbed854413fac82aec9e43b9e75b87f4f528` |
| `FINITE_PRODUCT_CHECK_OPTIMIZED.json` | 341 | `2cec69204f85b35b5138a520f3ccdbed854413fac82aec9e43b9e75b87f4f528` |

### 9.1 Prime-local gauge and finite interpolation

For squarefree d, Σ_{p|d}log p=log d, and log d/log R=1−y_d/log R. Therefore the simultaneous changes

\[
f(x)\mapsto e^{cx}f(x),\qquad
Q(y)\mapsto e^{-c+cy/\log R}Q(y)
\]

have multiplying factors whose product is identically one at every allowed divisor. The sign in the report is correct. Changing f alone is instead equivalent to changing the cutoff by the *opposite* factor e^{c−cy/log R}. This latter observation does not claim simultaneous gauge invariance with that opposite sign.

The nodes y_d=log(R/d), d∈D, are distinct and positive. Lagrange interpolation prescribes Q(y_d)=μ(d)c_d and optionally Q(0)=0. Since μ(d)²=1 on squarefree D, f=1 gives λ_d=c_d exactly. The assertion is correct for each fixed finite D, with no uniform bound on degree or derivatives; it does not imply a useful asymptotic family as R varies. If a smooth zero extension is required, Q(0)=0 alone is insufficient. The revised report correctly requires flatness at zero and explains the alternative of disjoint smooth bumps supported away from zero. Such bumps can prescribe all finitely many positive-node values while remaining identically zero near zero.

### 9.2 Actual product-curve Hessian

Let λ(ε)=u+εv+ε²z/2+O(ε³), with v_d=u_dH_d and z_d=u_dH_d². Set D(ε)=λ(ε)ᵀAλ(ε), and C(ε)=λ(ε)ᵀKλ(ε), where K=B−ρA and ρ=uᵀBu/a. Then C(0)=0, D(0)=a,

\[
C'(0)=2u^TKv,\quad
C''(0)=2v^TKv+2u^TKz,\quad
D'(0)=2u^TAv.
\]

Since R(ε)−ρ=C(ε)/D(ε), direct quotient differentiation gives

\[
R'(0)=\frac{2u^TKv}{a},\qquad
R''(0)=\frac{2(v^TKv+u^TKz)}a
-\frac{8(u^TAv)(u^TKv)}{a^2}.
\]

Both formulas and the local-improvement criteria are correct. The term uᵀKz is genuinely necessary at first-order stationarity along the actual nonlinear curve. Its absence from a straight-line test cannot be excused by uᵀKv=0.

### 9.3 Exact counterexample to replacing the curve by its tangent plane

For the stated u,r,w, the independent expansion is

\[
K=\begin{pmatrix}
5/12&-1/3&11/12\\
-1/3&-4/3&-1/3\\
11/12&-1/3&5/12
\end{pmatrix}.
\]

The vectors u,r,w are pairwise orthogonal. K has eigenvalues √2,−√2 on span{u,r} and −1/2 on span{w}; hence B=5I+K is positive definite, with eigenvalues 5+√2,5−√2,9/2. Its leading principal minors are indeed 65/12,79/4,207/2.

As v=u+w, the tangent plane span{u,v} has compressed quotient values 5 and 9/2, with zero cross entry. Its maximum is exactly 5. On the genuine exponential curve, put x=e^ε>0; then λ=(1,x,x²), and direct factorization gives

\[
R(\varepsilon)-5
=\frac{(x-1)^2(5x^2+2x+5)}{12(1+x^2+x^4)}.
\]

Thus every ε≠0 improves the ratio, and its second derivative at zero is 2/3. This verifies the report more strongly than a second-order check. The report correctly labels this an abstract example, not an arithmetic GPY realization.

### 9.4 CRT, exceptional primes, and certified intervals

For m=[d,e], squarefreeness makes the root condition P(n)≡0 mod m equivalent, by CRT, to one root condition at each p|m. Root counts therefore multiply. In an interval of N consecutive integers each individual residue class has count differing from N/m by at most one. Summing over ν(m) root classes proves the stated entrywise A bound, and the bilinear bound follows by the triangle inequality.

For each prime-score summand indexed by i, the substitution p=n+h_i is a bijection between counted pairs and the prime-residue counts displayed in the report. The residue a of n is uniquely determined modulo m, so there is no hidden duplicate root-class count. If gcd(a+h_i,m)>1 and p is prime in that class, then p divides m. Those exceptional primes must indeed be retained separately rather than assigned a coprime progression main term.

Finally,

\[
\left|c^T\bigl((B-TA)-(B_0-TA_0)\bigr)c\right|
\le\sum_{d,e}|c_dc_e|(E^B_{de}+|T|E^A_{de}),
\]

so the report's strict margin, together with a separately certified positive denominator, implies R(c)>T. This is valid for either sign of T. It is a finite sufficient certificate, not evidence that available asymptotic error estimates meet the margin.

### 9.5 Mixtures and sharp signed threshold

For a nonnegative mixture of squares, discard terms of zero total square weight. The resulting ratio is a convex combination of the component ratios, with coefficients proportional to α_jΣ_nL_j(n)². It cannot exceed their maximum. Allowing cross terms in a square is a different optimization; the report distinguishes these correctly.

For the prime count q∈{0,…,k}, g=q−(m−1) has (−g)_+≤m−1. The contamination bound and sufficient strict threshold follow immediately. The one-point choice q=0, W₊=0, W₋=1 attains the threshold while containing no point with q≥m, including the endpoint m=1. It establishes sharpness given only that range information. The implication g>0⇒q≥m uses that q is an integer prime count, as intended in the report, not merely a real number between zero and k.

### 9.6 Independent finite arithmetic example

The two supplied scripts were read, then rerun with ordinary Python and `python -O`. All four results passed, and the output bytes matched the corresponding saved JSON logs. Their explicit conditional exceptions remain active under optimization; their checks do not depend on Python `assert` statements.

Separately, an independent enumeration used a sieve-generated set of primes up to 51, rather than the supplied trial-division primality function. For R=8, D={1,2,3,5,6,7}, X={10,…,49}, and the specified u,v, it gave the exact moments

\[
(u^TAu,u^TAv,v^TAv,u^TBu,u^TBv,v^TBv)=(35,4,6,15,0,0).
\]

One direct check is that L_v is −1 precisely at n=14,20,26,32,38,44 and zero elsewhere in X. At those six points the prime score is zero, and L_u has values −1,−1,−1,0,−1,0. This independently explains uᵀAv=4, vᵀAv=6, and both zero v-containing numerator moments.

Consequently,

\[
\rho=\frac{15}{35}=\frac37,\qquad
R'(0)=\frac{2(0-(3/7)4)}{35}=-\frac{24}{245}.
\]

For c=u−v/2, the denominator is 35−4+6/4=65/2, its numerator is 15, and its ratio is 6/13>3/7. Because each squarefree divisor in D has H_d=1 exactly when 2|d, ε=−log 2 yields precisely these coefficients in the genuine prime-local exponential family. The cutoff and h interpolation claims are valid at this fixed R. The finite example is correct and genuinely arithmetic, but does not establish uniformity or an asymptotic prime-gap improvement.

**Final package verdict:** accept the mathematical statements at the final hashes above, with the continuous-representative repair and the revised cutoff-regularity explanation. No novelty or asymptotic improvement is certified. No fatal error remains in the audited claims.
