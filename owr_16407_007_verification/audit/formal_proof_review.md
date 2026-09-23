# Independent formal proof review: OWR-16407-007

Audit date: 2026-09-23 UTC. Reviewer: independent adversarial agent, formal-algebra route.

## Determination

The submitted candidate is **not a complete proof of the boundary-value claim**. Its Lagrange–Bürmann calculations are correct for the series it defines, but its final identification of that series with the independently defined model quantity assumes the assertion that must be proved. This is a proof gap, not a coefficient counterexample.

There is also decisive prior work: Panzer and Wulkenhaar supplied the missing identification in their 4 November 2018 revision. Thus repairing this candidate with that argument yields an exposition of an existing result, not a new resolution. No novelty claim is justified.

Audit completion estimate: 100% for determining whether this candidate establishes a new all-orders resolution. This is not a claim to have checked every theorem of the cited 28-page paper.

## Exact target and success criterion

Write \(D=d/da\), \(\phi(a)=-\log(1+a)\), and distinguish the independently defined quantity \(I_{\mathrm{BVP}}\) from the proposed series

\[
J(a,\lambda)=\sum_{n\ge1}\frac{\lambda^n}{n!}D^{n-1}\phi(a)^n
-\lambda\sum_{n\ge1}\frac{\lambda^n}{n!}D^{n-1}\frac{\phi(a)^n}{a}.
\]

The target is \(I_{\mathrm{BVP}}=J\) as formal series on the perturbative branch, for \(a>0\), with a separately justified extension to \(a=0\). One must establish the independent equation for \(I_{\mathrm{BVP}}\), show that \(J\) satisfies it, and show uniqueness of its normalized formal solution. Merely resumming \(J\) is insufficient.

In v1, equation (26) defines \(I_{\mathrm{BVP}}\) by a coupled nonlinear integral involving the angle and its Hilbert transform. The candidate calls v1 (31) its definition instead; (31) is the proposed expansion. Section 5.3 conjectures the all-orders expression after ten terms. Section 6 rewrites and resums it. [Panzer–Wulkenhaar v1](https://arxiv.org/html/1807.02945v1).

The defining system can be expressed using the renormalized integral

\[
I_{\mathrm{BVP}}(a)=\int_0^\infty\left(\frac{\tau_a(p)}{\pi}-\frac{\lambda}{1+p}\right)dp,
\qquad
\tau_a(p)=\arg\bigl(1+a+p-\lambda\log p+I_{\mathrm{BVP}}(p)+i\pi\lambda\bigr)
\tag{A}
\]

for positive real coupling, with argument in \([0,\pi]\). The perturbative normalization is \(I_{\mathrm{BVP}}=O(\lambda)\), \(\tau_a(p)=\pi\lambda/(1+a+p)+O(\lambda^2)\). The reduced system uses the choice of zero homogeneous Carleman term. This does not assert uniqueness of every nonanalytic boundary-value solution. The simplification of the v1 integral uses the finite-cutoff identity equating the integral of the angle with the integral of the corresponding exponential-Hilbert-transform expression; the subtraction and cutoff limit still have to be respected. The source is v2 Proposition 4, equations (17c), (19)–(21).

## Strongest theorem actually proved by the candidate

**Formal resummation theorem.** For each fixed \(a>0\), there is a unique series \(K\in\lambda\mathbb R[[\lambda]]\) solving

\[
K=-\lambda\log(1+a+K).
\tag{B}
\]

The proposed series satisfies

\[
J=K-\lambda\log(1+K/a).
\tag{C}
\]

Proof: the coefficients of (B) determine those of \(K\) recursively, since the right side has an explicit factor \(\lambda\). Formal Lagrange inversion yields the first sum in \(J\). Generalized inversion applied to \(H(w)=\log(1+w/a)\), whose derivative is \(1/(a+w)\), yields the second sum. Translation by \(a\) identifies differentiation in \(w\) at zero with differentiation in \(a\). This establishes (C) without invoking a physical model or any integral equation. The analytic implicit-function theorem also gives a positive convergence radius near \(\lambda=0\), since the derivative of \(K+\lambda\log(1+a+K)\) with respect to \(K\) is 1 there.

Putting \(x=1+a+K\) in (B) gives \(xe^{x/\lambda}=e^{(1+a)/\lambda}\). This recovers the candidate's Lambert expression on the branch continuous from \(K(a,0)=0\). None of these operations establishes (A).

### An explicit algebraic recursion

Let \(A=1+a\), \(\ell=\log A\), \(K=\sum c_n\lambda^n\), and \(\log(1+K/a)=\sum b_n\lambda^n\). Then

\[
c_1=-\ell,\qquad
c_n=\sum_{j=1}^{n-1}\frac{(-1)^j}{jA^j}
\sum_{r_1+\cdots+r_j=n-1\atop r_i\ge1}c_{r_1}\cdots c_{r_j},
\]

\[
b_n=\sum_{j=1}^{n}\frac{(-1)^{j+1}}{ja^j}
\sum_{r_1+\cdots+r_j=n\atop r_i\ge1}c_{r_1}\cdots c_{r_j},
\qquad [\lambda^n]J=c_n-b_{n-1},\quad b_0=0.
\]

These are the recursions that the candidate *does* establish. They produce

\[
[\lambda]J=-\ell,\qquad [\lambda^2]J=\frac{\ell}{A}+\frac{\ell}{a},
\]

\[
[\lambda^3]J=-\frac{\ell}{A^2}-\frac{\ell}{aA}
+\frac{\ell^2}{2A^2}+\frac{\ell^2}{2a^2}.
\]

## The independent recursion that must be matched

Write \(I_{\mathrm{BVP}}=\sum_{n\ge1}i_n\lambda^n\). Taking formal imaginary parts of a logarithm in (A) gives the triangular recurrence

\[
i_n(a)=\int_0^\infty\left\{
\frac{1}{\pi}\operatorname{Im}[\lambda^n]\log\left(1+\frac{\lambda(-\log p+i\pi)+\sum_{r=1}^{n-1}i_r(p)\lambda^r}{1+a+p}\right)
-\frac{\delta_{n1}}{1+p}\right\}dp.
\tag{D}
\]

The omitted term \(i_n(p)\lambda^n\) has a real contribution in the linear term of the logarithm, so it does not change the coefficient's imaginary part. Consequently, (D) determines at most one normalized formal solution when its coefficient integrals exist. Every finite coefficient of the proposed logarithmic-rational series has integrable endpoint behavior in (D); this does not by itself evaluate those integrals.

The first two consequences can be checked independently:

\[
i_1(a)=\int_0^\infty\left(\frac1{A+p}-\frac1{1+p}\right)dp=-\ell,
\]

\[
i_2(a)=\int_0^\infty\frac{\log p+\log(1+p)}{(A+p)^2}\,dp
=\frac\ell A+\frac\ell a.
\]

For the second equality, substitution \(p=At\) evaluates the \(\log p\) integral as \(\ell/A\), while integration by parts evaluates the \(\log(1+p)\) integral as \(\ell/a\). Thus the first two coefficients match; they do not imply an all-orders match. At third order the new integral contains

\[
-\frac{i_2(p)}{(A+p)^2}
+\frac{(\log p+\log(1+p))^2-\pi^2/3}{(A+p)^3}.
\]

The submitted candidate never compares (D) with its algebraic recursion. Its claim that the boundary-value calculation gives \(I_{\mathrm{BVP}}=K-\lambda L\) is precisely the missing step. Mark this candidate route **blocked by circular identification** unless an independent integral verification is supplied.

## Existing repair, and what it proves

The necessary additional work is already in v2 §5.2: Lemma 10 establishes two integral identities and Proposition 11 verifies the resummed solution. The target series is v2 (26). The revision history dates this proof to 4 November 2018. [Version history](https://arxiv.org/abs/1807.02945), [v2 full text](https://arxiv.org/html/1807.02945v2).

The mechanism can be checked transparently. Define

\[
u=p+K(p,\lambda),\quad p=u+\lambda\log(1+u),\quad
dp=\left(1+\frac{\lambda}{1+u}\right)du.
\]

For \(\lambda>0\), this is a monotone bijection of \([0,\infty)\). Substituting \(J\) into the angle reduces its denominator to \(1+a+u-\lambda\log u\). Let \(\theta_a(u)\) denote the resulting argument. The two independent integral identities needed are

\[
\int_0^\infty\left(\frac{\theta_a(u)}\pi-\frac{\lambda}{1+u}\right)du=K(a,\lambda),
\qquad
\int_0^\infty\frac{\theta_a(u)}{\pi(1+u)}du=-\log(1+K(a,\lambda)/a).
\]

They turn the transformed integral into \(J\). A cutoff at \(u=R\) corresponds to \(p=R+\lambda\log(1+R)\); the correction from the subtraction is bounded by \(\lambda\log(1+\lambda\log(1+R)/(1+R))\), which tends to zero. This checks that the change of variables does not lose a finite renormalization. The proof of those two integral identities, supplied by contour integration in the cited lemma, is mathematically additional to formal inversion.

With that independent verification and existence of coefficient integrals, triangularity of (D) gives equality to every order. This repairs the mathematics by invoking existing work, while defeating the requested priority claim.

## Adversarial boundary checks

1. **\(a=0\).** The candidate's inverse theorem with \(\phi(0)\ne0\) and its \(H(w)=\log(1+w/a)\) cannot be applied directly at \(a=0\). The fix is removable continuation. Equation (B) gives \(K(0,\lambda)=0\), and differentiation gives \(K_a(0,\lambda)=-\lambda/(1+\lambda)\). Hence \(1+K/a\to1/(1+\lambda)\), and
   \[
   J(0,\lambda)=\lambda\log(1+\lambda)
   =\sum_{n\ge2}\frac{(-1)^n}{n-1}\lambda^n.
   \]
   The derivative series gives the same result directly: \(\phi(a)^n\) vanishes to order \(n\), whereas \(\phi(a)^n/a\) has leading term \((-1)^na^{n-1}\).
2. **\(\lambda=0\).** The Lambert expression has no literal value as written at zero; it must be understood by its analytic continuation or (B). The formal coefficients themselves are unambiguous.
3. **Positive versus negative coupling.** \(W_0\) gives the real positive-coupling branch; \(W_{-1}\) gives the formal branch continued to \(-1<\lambda<0\). Analytic continuation of the final formula must not be identified with the unchanged real integral equation at negative coupling. The v2 §6.4 discussion exhibits additional terms that are flat at zero. Those terms have zero formal Taylor series and so do not falsify the formal claim.
4. **Uniqueness scope.** Formal triangularity addresses the normalized coefficient solution. It does not prove uniqueness among nonanalytic boundary-value solutions.
5. **Evidence scope.** No coefficient mismatch was found. This audit falsifies the candidate's claim to have supplied a complete proof, not the identity itself.

## Dated checkpoint log

- 2026-09-23 03:40 UTC checkpoint: inspected v1 definitions and dependency chain; diagnosed circularity; checked algebraic coefficient recursion and endpoint normalization. Candidate-proof audit: 90% complete.
- 2026-09-23 03:43 UTC checkpoint: confirmed v2 Proposition 11 and version-history priority; checked monotone substitution and cutoff correction; identified negative-coupling qualification. Candidate/novelty determination: 100% complete.

No person was contacted. No commit, push, release, or DOI registration was performed by this reviewer.
