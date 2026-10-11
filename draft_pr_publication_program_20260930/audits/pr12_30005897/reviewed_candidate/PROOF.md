# Shadowing without bounded distortion for dissipative composition operators

**Status:** mathematically checked proof and credited known-method reformulation;
final acceptance review pending. This repository audit is not a preprint, human
peer review, or formal certification. The full result follows from earlier scalar
spectral machinery; see [PRIORITY_AUDIT.md](PRIORITY_AUDIT.md). The original
AI review and its reviewed proof snapshots are preserved in `review/`.

**Target:** UnsolvedMath 30005897 / OWR-14298367-003: the second sentence
of Open Problem (1) in Oberwolfach Report 19/2024, p. 1080, asking for the
shadowing/generalized-hyperbolicity equivalence without bounded distortion.
The first sentence asks a distinct aggregate-mass question, already refuted
in the literature and credited in Section 7.

## 1. Statement and scope

Let \((X,\mathcal B,\mu)\) be a sigma-finite measure space. Suppose that
\(f:X\to X\) is a bijective bimeasurable transformation and that there
are finite constants \(c_+,c_-\) for which
\[
 \mu(fA)\le c_+\mu(A),\qquad
 \mu(f^{-1}A)\le c_-\mu(A)\qquad(A\in\mathcal B).
\tag{1.1}
\]
Thus \(T\varphi=\varphi\circ f\) is a bounded invertible operator on
\(L^p(X,\mu)\), for each fixed \(1\le p<\infty\). Assume dissipativity in
the source's sense: there is a measurable \(W\) with
\(0<\mu(W)<\infty\) such that
\[
 X=\mathop{\dot\bigcup}_{n\in\mathbb Z}f^nW
\tag{1.2}
\]
up to a null set. All operators and spaces may be real or complex.

We use two-sided shadowing. Generalized hyperbolicity means a topological
direct sum \(L^p=M\oplus N\) of closed subspaces satisfying
\[
 TM\subset M,\qquad T^{-1}N\subset N,\qquad
 r(T|_M)<1,\qquad r(T^{-1}|_N)<1.
\tag{1.3}
\]
Equivalently, the two restrictions have uniform exponential norm decay.
This is the spectral-radius convention used in the 2024 source; strict
one-step contractions can be obtained by an equivalent norm. For real spaces,
spectral radius means the radius after complexification; the equivalent
uniform exponential power bounds avoid dependence on a scalar convention.

**Theorem.** Under (1.1)--(1.2), \(T\) has the shadowing property if and
only if it is generalized hyperbolic. No bounded-distortion assumption is
needed. In the implication from shadowing, \(M\) and \(N\) can be chosen
as complementary measurable support bands.

There is also a pointwise density criterion. Put \(\nu=\mu|_W\), and let
\[
 \rho_n=\frac{d\nu_n}{d\nu},\qquad
 \nu_n(A)=\mu(f^nA),\quad A\subset W.
\tag{1.4}
\]
Each \(\rho_n\) is positive and finite almost everywhere; \(\rho_0=1\).
The theorem's two conditions are equivalent to the following:

**Density condition.** There are an integer \(d\ge1\) and \(0<\eta<1\) such that,
for almost every \(w\in W\) and every \(n\in\mathbb Z\),
\[
 \min\{\rho_{n-d}(w),\rho_{n+d}(w)\}\le\eta\rho_n(w).
\tag{1.5}
\]
The exceptional set is common to all integers \(n\). Its existence causes
no issue because there are only countably many coordinates.

The proof below is self-contained apart from standard \(L^p\) duality,
Radon--Nikodym theory, and elementary Banach-space facts. In particular it
does not assume the recent general spectral characterization of shadowing.

## 2. A necessary dual estimate for shadowing

We first give an elementary Banach-space lemma, including its quantitative
form to expose the uniformity needed later.

**Lemma 2.1.** Let \(A\) be a bounded invertible operator on a Banach
space \(E\). If \(A\) has two-sided shadowing, there is \(K>0\) such
that every bounded sequence \((b_j)_{j\in\mathbb Z}\) admits a bounded
solution of
\[
 y_{j+1}-Ay_j=b_j,\qquad
 \sup_j\|y_j\|\le K\sup_j\|b_j\|.
\tag{2.1}
\]
For this \(K\), any integer \(d>4K^2+1\) satisfies
\[
 \max\{\|(A^*)^du\|,\|(A^*)^{-d}u\|\}>2\|u\|
 \quad(0\ne u\in E^*).
\tag{2.2}
\]

**Proof.** For (2.1), fix a shadowing accuracy, say one, and an associated
positive error tolerance. Scale any bounded forcing into that tolerance,
construct a bi-infinite pseudotrajectory recursively using invertibility,
and subtract a shadowing exact orbit. Scaling back gives (2.1), with a
constant independent of the forcing. Explicitly, if \(\delta_0>0\) is
a tolerance for shadowing accuracy one and \(L=\sup_j\|b_j\|>0\),
scale the forcing by \(\delta_0/(2L)\), set \(x_0=0\), and define
\(x_{j+1}=Ax_j+\delta_0 b_j/(2L)\) in both directions, using
\(A^{-1}\) backwards. Subtract the shadowing orbit and scale back;
\(K=2/\delta_0\) works. For zero forcing choose the zero solution.

Write \(S=A^*\). Every finitely supported sequence \((u_j)\) in \(E^*\)
satisfies
\[
 \sum_j\|u_j\|\le K\sum_j\|u_{j-1}-Su_j\|.
\tag{2.3}
\]
Indeed, choose \(b_j\) in the unit ball so that the real parts of
\(u_j(b_j)\) approach \(\|u_j\|\), simultaneously on the finite support.
Use (2.1), sum the identities
\(u_j(b_j)=u_j(y_{j+1}-Ay_j)\), and shift the index. This gives
\[
 \operatorname{Re}\sum_j u_j(b_j)
 =\operatorname{Re}\sum_j(u_{j-1}-Su_j)(y_j)
 \le K\sum_j\|u_{j-1}-Su_j\|.
\]
Letting the finite approximation errors tend to zero proves (2.3).
No norm-attainment assumption is used.

Fix nonzero \(u\in E^*\), and write \(a_j=\|S^ju\|\). In (2.3), take
\(u_j=S^{-j}u\) for \(-b\le j\le-a\) and zero otherwise. Interior
terms cancel, leaving, for every pair of integers \(a\le b\),
\[
 \sum_{j=a}^{b}a_j\le K(a_a+a_{b+1}).
\tag{2.4}
\]
In particular, using the interval \([-j,j-1]\), for each \(j\ge1\),
\[
 a_0\le K(a_{-j}+a_j).
\tag{2.5}
\]
If both \(a_{-d}\) and \(a_d\) were at most \(2a_0\), (2.4) on
\([-d,d-1]\) would give
\[
 \sum_{j=-d}^{d-1}a_j\le4Ka_0.
\]
Summing (2.5) for \(1\le j\le d-1\) then gives
\[
 \frac{d-1}{K}a_0
 \le\sum_{j=1}^{d-1}(a_{-j}+a_j)
 \le4Ka_0.
\]
This contradicts \(d>4K^2+1\), proving (2.2). \(\square\)

The implication in this lemma is consistent with the more recent full
duality theorem of Dragičević--Pituk. Only the elementary necessary
direction proved here is used.

## 3. Orbit coordinates and localization

The realization of dissipative composition operators as shifts on
density-weighted sequence spaces is prior work: see
Carvalho--Darji--Varandas [7, Theorem 2.4]. We give the normalization
explicitly because the adjoint coefficients are essential to the argument.

Let \(\Omega=W\times\mathbb Z\), with measure \(\nu\times\#\), and
write \(E=L^p(\Omega)\). Define
\[
 (U\varphi)_n(w)=\rho_n(w)^{1/p}\varphi(f^nw).
\tag{3.1}
\]
The change-of-variables formula defining \(\nu_n\), together with the
disjoint decomposition (1.2), shows that \(U\) is an isometric
isomorphism from \(L^p(X,\mu)\) onto \(E\). Surjectivity follows by
defining \(\varphi\) separately on each \(f^nW\); both the definition
and its inverse are measurable.

The conjugate \(B=UTU^{-1}\) is the positive weighted backward shift
\[
 (Bg)_n(w)=a_n(w)g_{n+1}(w),\qquad
 a_n(w)=\left(\frac{\rho_n(w)}{\rho_{n+1}(w)}\right)^{1/p}.
\tag{3.2}
\]
Both \(B\) and \(B^{-1}\) are bounded. They preserve disjoint supports
and send every measurable support band onto another such band.

Let \(q\) be conjugate to \(p\), including \(q=\infty\) when \(p=1\).
The Banach dual is the scalar \(L^q(\Omega)\), and \(S=B^*\) satisfies
\[
 (Sh)_{n+1}=a_nh_n.
\tag{3.3}
\]
If \(h\) is supported in coordinate \(n\), then \(S^dh\) and
\(S^{-d}h\) are supported in coordinates \(n+d\) and \(n-d\), with
respective multiplication factors
\[
 \left(\frac{\rho_n}{\rho_{n+d}}\right)^{1/p},\qquad
 \left(\frac{\rho_n}{\rho_{n-d}}\right)^{1/p}.
\tag{3.4}
\]

**Lemma 3.1.** If \(B\) has shadowing, condition (1.5) holds for some
\(d\), with \(\eta=2^{-p}\).

**Proof.** Apply Lemma 2.1 to \(B\). Fix a coordinate \(n\). If both
factors in (3.4) were strictly less than two on a set of positive
\(\nu\)-measure, then on a subset \(F\) of positive measure they would
both be at most \(2-\epsilon\) for some \(\epsilon>0\). Use
\(h=\mathbf1_F\) in coordinate \(n\). It belongs to \(L^q(\Omega)\):
\(\nu(W)<\infty\), and for \(q=\infty\) it has norm one. Both norms
in (2.2) would be at most \((2-\epsilon)\|h\|\), a contradiction.
Thus at least one of the factors in (3.4) is at least two almost
everywhere. Rearrangement gives (1.5). Take the union of the exceptional
null sets over \(n\in\mathbb Z\). \(\square\)

This is the place where an operator-level uniform estimate becomes a
pointwise estimate uniform over every fiber. Merely knowing that each
individual fiber has shadowing would not suffice.

## 4. A support-band splitting for a power

Assume (1.5) for some \(d\) and \(\eta\in(0,1)\). Define
\[
 A_0=\{(w,n):\rho_{n-d}(w)\le\eta\rho_n(w)\},\qquad
 C_0=\Omega\setminus A_0.
\tag{4.1}
\]
These sets are measurable. All statements about them are modulo the
common null set already removed. Put
\(M_0=L^p(A_0)\), \(N_0=L^p(C_0)\), as support bands in \(E\).

If \((w,n)\in A_0\), then \((w,n-d)\in A_0\). In fact, applying
(1.5) at \(n-d\), the alternative
\(\rho_n\le\eta\rho_{n-d}\) is impossible, because it would imply
\(\rho_n\le\eta^2\rho_n\). Therefore
\(\rho_{n-2d}\le\eta\rho_{n-d}\). Iteration yields
\[
 \rho_{n-md}(w)\le\eta^m\rho_n(w)
 \quad((w,n)\in A_0,\ m\ge0).
\tag{4.2}
\]

If \((w,n)\in C_0\), condition (1.5) forces
\(\rho_{n+d}\le\eta\rho_n\). Moreover, \((w,n+d)\in C_0\), because
membership in \(A_0\) at \(n+d\) would give the contradictory opposite
inequality \(\rho_n\le\eta\rho_{n+d}\). Hence
\[
 \rho_{n+md}(w)\le\eta^m\rho_n(w)
 \quad((w,n)\in C_0,\ m\ge0).
\tag{4.3}
\]
At a point where both drops hold, (4.1) assigns the point to \(A_0\);
the two propagation arguments remain valid at this boundary.

Equations (3.2), (4.2), and (4.3) now give
\[
 B^dM_0\subset M_0,\quad B^{-d}N_0\subset N_0,
\quad
 \|B^{md}|_{M_0}\|\le\eta^{m/p},\quad
 \|B^{-md}|_{N_0}\|\le\eta^{m/p}.
\tag{4.4}
\]
For example, changing the summation index in the \(L^p\) norm of
\(B^{md}g\) expresses it as the integral of
\(\sum_n(\rho_{n-md}/\rho_n)|g_n|^p\), and (4.2) applies on the support
of \(g\). The inverse estimate is identical with (4.3).

## 5. Passing from a power to the original operator

It is important not to assume that an arbitrary generalized-hyperbolic
splitting for a power automatically gives the required splitting for the
operator. Here a finite intersection of support bands supplies it.

Define the closed support band
\[
 M=\bigcap_{j=0}^{d-1}B^jM_0,
\tag{5.1}
\]
and let \(N\) be its complementary support band. Then \(E=M\oplus N\),
with norm-one coordinate projections when the bands are nonzero. Because
\(B\) is an invertible weighted coordinate permutation,
\[
 BM=\bigcap_{j=1}^{d}B^jM_0
 \subset\bigcap_{j=0}^{d-1}B^jM_0=M;
\tag{5.2}
\]
the inclusion uses \(B^dM_0\subset M_0\).

Support complementation commutes with this weighted permutation. Thus
\[
 N=\sum_{j=0}^{d-1}B^jN_0
\tag{5.3}
\]
is the support band on the finite union of the corresponding supports.
Equation (5.2) also gives \(B^{-1}N\subset N\). More explicitly, if
\(\tau(w,n)=(w,n-1)\) is the support map of \(B\), and \(A\) is the
support of \(M\), then \(\tau A\subset A\) implies
\(\tau^{-1}(A^c)\subset A^c\).

The contraction bound for \(M\) follows immediately from \(M\subset M_0\):
\[
 \|B^{md}|_M\|\le\eta^{m/p}.
\tag{5.4}
\]
For the complementary band, set
\[
 D=\max_{0\le j<d}\|B^j\|\,\|B^{-j}\|<\infty.
\]
If \(g\in B^jN_0\), then \(B^{-j}g\in N_0\), so (4.4) gives
\[
 \|B^{-md}g\|
 \le\|B^j\|\eta^{m/p}\|B^{-j}g\|
 \le D\eta^{m/p}\|g\|.
\tag{5.5}
\]
For general \(g\in N\), partition the finite union in (5.3) into
disjoint measurable sets, the \(j\)-th contained in the support of
\(B^jN_0\). This writes \(g=\sum_{j=0}^{d-1}g_j\) with disjoint
supports and \(g_j\in B^jN_0\). Their images under \(B^{-md}\) still
have disjoint supports. Therefore
\[
 \|B^{-md}g\|^p
 =\sum_j\|B^{-md}g_j\|^p
 \le D^p\eta^m\sum_j\|g_j\|^p
 =D^p\eta^m\|g\|^p.
\tag{5.6}
\]
This argument includes \(p=1\).

Writing an arbitrary \(k\ge0\) as \(md+r\), \(0\le r<d\), and using
the finite bounds for \(B^r\) and \(B^{-r}\), proves uniform exponential
decay on \(M\) forward and on \(N\) backward. In particular,
\[
 r(B|_M),\ r(B^{-1}|_N)\le\eta^{1/(pd)}<1.
\tag{5.7}
\]
Transporting the bands by \(U^{-1}\) gives (1.3) for \(T\).

Thus shadowing implies (1.5), and (1.5) implies generalized hyperbolicity.

## 6. Converse and completion

For completeness, suppose (1.3) holds for a bounded invertible operator
on a Banach space, and let \(P,Q\) be the complementary projections onto
\(M,N\). There are \(C<\infty\) and \(0<\alpha<1\) such that
\(\|T^j|_M\|,\|T^{-j}|_N\|\le C\alpha^j\) for all \(j\ge0\).
For any bounded forcing \((b_n)\), the series
\[
 y_n=\sum_{j=0}^{\infty}T^jPb_{n-1-j}
     -\sum_{j=0}^{\infty}T^{-j-1}Qb_{n+j}
\tag{6.1}
\]
converge absolutely and uniformly in \(n\). Their sums are uniformly
bounded by \(K_G\sup_n\|b_n\|\), where
\(K_G=C(\|P\|+\alpha\|Q\|)/(1-\alpha)\). If both sums are
truncated at \(j=J\), the recurrence error is
\(b_n-T^{J+1}Pb_{n-1-J}-T^{-J-1}Qb_{n+J+1}\); the two tails
vanish uniformly as \(J\to\infty\). Directly shifting each
series gives \(y_{n+1}-Ty_n=b_n\); commutation of \(P,Q\) with \(T\)
is neither assumed nor needed.

For a pseudotrajectory \((x_n)\), use its errors as \(b_n\), and put
\(z_n=x_n-y_n\). Then \(z_{n+1}=Tz_n\), so invertibility implies
\(z_n=T^nz_0\) for all integers \(n\). The uniform bound on \(y_n\)
gives shadowing after choosing the error tolerance small enough.
This proves the converse and the full equivalence. \(\square\)

## 7. Distinguishing the two questions in the original source

The original 2024 problem also asks whether the earlier characterization
using only the scalar sequence \(\mu(f^nW)\) survives removal of bounded
distortion. That is a different assertion from the theorem proved above.

The answer to that older scalar-characterization question was already
negative before this attempt: Bernardes--D'Aniello--Maiuriello,
arXiv:2607.15831v1, Example 6.2, construct a dissipative two-orbit system
whose level masses are \(2^n\), so the condition labelled HC holds, but
whose composition operator has no shadowing. Their obstruction is a
constant-mass positive tail on one orbit, which permits unbounded
accumulation of pseudotrajectory errors. We claim no novelty for that
negative answer.

Condition (1.5) retains the pointwise orbit densities and is not the old
aggregate-mass criterion. In the cited example the constant-mass tail
violates (1.5) for every \(d\) and \(\eta<1\), as it must.

## 8. Earlier equivalent machinery and current disposition

Kitover--Orhon, arXiv:2009.09303v2 (19 December 2020), Theorem 2.26,
states and attributes to Kitover (2011), Theorem 3.29, a scalar weighted
composition decomposition on a Stonean compact space with an aperiodic
homeomorphism. The closed invariant limiting sets and clopen wandering
transition set have **global** positive and negative tail conditions.
Those conditions yield complementary clopen support sets with uniform
forward and inverse product decay.

[PRIORITY_AUDIT.md](PRIORITY_AUDIT.md) supplies the complete translation to
the present arbitrary measurable fibers. Shadowing makes `I-B*` bounded
below. A directly verified coordinate cutoff transfers the necessary
approximate-spectrum exclusion to the central `L^infinity=C(K)` operator.
The old scalar decomposition gives one-step complementary measurable
bands; the primal norm identities give generalized hyperbolicity. The
resolvent case uses the coordinate gauge and ordinary Riesz projections.
Choosing a common sufficiently large power also gives density condition
(1.5). This covers real scalars, nonseparable fibers, and `p=1`.

The audit found a false algebraic identity in equation (33) of the broader
2020 full-spectrum proof. The sufficient route imports neither that
identity nor the full spectral-equality assertion: its needed transfer
and resolvent splitting are proved independently. The original 2011 proof
was inaccessible; the inspected input is the theorem explicitly stated
and attributed in the primary-author 2020 text. That provenance boundary
is retained, rather than claiming to have inspected the earlier proof.

The result is therefore accepted in principle as a **credited corollary
of earlier equivalent machinery**, subject to the final complete audit.
No first resolution, new theorem priority, or new preprint is claimed.
The elementary density proof in Sections 2--6 remains useful independent
verification. A different proof or display format alone does not establish
novelty. The exact-question search's lack of a literal earlier all-p
statement does not override this positive equivalent-method certificate.

Other verified boundaries remain: D'Aniello--Darji--Maiuriello's 2021
Corollary GH assumes bounded distortion; Carvalho--Darji--Varandas supply
the orbit-density coordinates and conditional finite-dimensional-fiber
result; Bernardes--D'Aniello--Maiuriello's Example 6.2 refutes the aggregate
criterion; Pituk's August 2026 Theorem B covers separable complex Hilbert
spaces. General Banach counterexamples are not identified as scalar
dissipative composition operators. Current bounded fulltext search gaps
are recorded in the audit and are not used as negative priority evidence.

## References

1. E. D'Aniello, U. B. Darji, M. Maiuriello, *Generalized hyperbolicity
   and shadowing in Lp spaces*, Journal of Differential Equations 298
   (2021), 68--94. DOI: https://doi.org/10.1016/j.jde.2021.06.038.
   Open preprint: https://arxiv.org/abs/2009.11526.
2. M. Maiuriello, *Preserved dynamics: visualizing the connection between
   composition operators and weighted shifts*, in Oberwolfach Report
   19/2024, pp. 1078--1081. DOI: https://doi.org/10.4171/owr/2024/19.
3. N. C. Bernardes Jr., E. D'Aniello, M. Maiuriello, *The specification
   property for composition operators*, arXiv:2607.15831v1 (17 July 2026),
   especially Theorem 6.1 and Example 6.2.
   https://arxiv.org/abs/2607.15831.
4. M. Pituk, *Resolving the generalized hyperbolicity conjecture for
   shadowing*, arXiv:2608.19499v1 (19 August 2026), Theorems A--C.
   https://arxiv.org/abs/2608.19499.
5. A. Messaoudi, J. Tofanin Neto, M. Saavedra, I. Tsokanos, *On
   Generalized Hyperbolicity, Stability, and Shadowing for Linear
   Operators*, arXiv:2608.17021v1 (17 August 2026).
   https://arxiv.org/abs/2608.17021.
6. D. Dragičević, M. Pituk, *Duality between shadowing and uniform
   expansivity in linear dynamics*, Transactions of the American
   Mathematical Society (2026), DOI: https://doi.org/10.1090/tran/9879.
   Bibliographic details checked through [4]; the publisher PDF was
   inaccessible during this attempt. None of its uninspected proof is
   used as a premise here.
7. M. Carvalho, U. B. Darji, P. Varandas, *Shift operators and their
   classification*, arXiv:2407.20890v1 (30 July 2024), Theorem 2.4 and
   Corollary 2.16. https://arxiv.org/abs/2407.20890.
8. A. K. Kitover, M. Orhon, *Spectrum of Weighted Composition Operators
   Part VI: Essential spectra of d-endomorphisms of Banach C(K)-modules*,
   arXiv:2009.09303v2 (19 December 2020), especially Theorem 2.26 and
   Section 5. https://arxiv.org/abs/2009.09303v2.
9. A. K. Kitover, *Spectrum of weighted composition operators: part 1.
   Weighted composition operators on C(K) and uniform algebras*, Positivity
   15 (2011), 639--659. DOI: https://doi.org/10.1007/s11117-010-0106-4.
   Theorem 3.29 is attributed in [8]; its original proof was not inspected.

**Source-proof precision update:** the plain-shift cocycle countercheck in the historical falsifier report alone distinguishes operators, not their global norms. A broader allowed weighted-module example does falsify the printed norm identity, and a corrected operator relation can repair the growth estimate; the old spectral theorem is not refuted. See [the exact correction](https://github.com/AlecKriebel/Math/blob/main/draft_pr_publication_program_20260930/audits/pr12_30005897/ROOT_EQ33_PRECISION.md). The sufficient priority route remains independent of that identity.
