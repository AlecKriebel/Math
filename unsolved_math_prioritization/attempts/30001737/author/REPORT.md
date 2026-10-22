# Converse unitary distinction: scope correction and bounded partial audit

Problem 30001737 / OWR-4804-005. Research checked 2026-10-06.

**Disposition: not solved here.** No proof or counterexample to the unrestricted converse has been obtained. This is an authored status correction with elementary, explicitly expository deductions. No novelty is claimed for the classification, special cases, counting formula, or descent observation. In particular, the descent example below is not a counterexample to the target conjecture.

## 1. Exact mathematical target

Let n >= 1, let p,q >= 0 with p+q=n, put J=diag(I_p,-I_q), and let H=U(p,q)={g in GL_n(C): g*Jg=J}. The ambient field extension is C/R. Work with irreducible admissible smooth Frechet representations of moderate growth, and continuous complex-linear H-invariant functionals. The representation pi is the Langlands quotient of normalized induction from n smooth characters of C^times, ordered by decreasing real exponent. The superscript tau means pullback by entrywise complex conjugation; it does not mean conjugate-contragredient or complex conjugation of vector-space coefficients.

Use the usual Euclidean absolute value to write each character uniquely as

    chi_(k,s)(z) = (z/|z|)^k |z|^(2s),   k in Z, s in C.

Then chi_(k,s)^tau=chi_(-k,s). In particular, tau fixes s, rather than conjugating it. Let M be the multiset of these parameters. If M is stable under tau, let a_1,...,a_r be the multiplicities of the distinct fixed characters (k=0), and let b_1,...,b_t be the common multiplicities of the distinct nonfixed pairs {chi,chi^tau}. Set

    s_0 = b_1+...+b_t,      n = a_1+...+a_r+2s_0.

The target asks whether tau-stability and s_0 <= min(p,q) force Hom_H(pi,C) to be nonzero. Orbits must be counted with multiplicity. There is no parity restriction on n, p or q beyond integrality and p+q=n. The fixed-character count n-2s_0 automatically has the parity of n. In the quasi-split signatures, |p-q| <= 1, the inequality is automatic once M is stable.

The primary location is Erez Lapid's report, §2.3, Theorem 6 and Conjecture 2, printed p.732 in [1]. It gives necessity and the generic converse. Its p-adic §2.2 is a different setting. The supplied target record and review fingerprints match; the public target URL was also attempted, with access details in the metadata. No raw dataset or copied source text accompanies this report.

## 2. Literature scope correction

The exact-target extension in Feigon–Lapid–Offen [2] is Conjecture 6.12. Their established complex cases include generic representations (Corollary 12.3), finite-dimensional representations (Lemma 6.13), spherical representations (Lemmas 3.3 and 6.14), and unitarizable representations (Remark 13.13). Appendix B, Theorem B.1 provides an upper bound used below. The category and normalization are fixed in §1.3.

Two previously supplied citations do not establish additional cases of this complex target. Gurevich [3] treats a quadratic extension of p-adic fields and distinction by GL_n(F), with conjugate-duality; both subgroup and symmetry differ. Zou [4] treats unitary distinction for supercuspidals over nonarchimedean fields of residual characteristic different from 2, with coefficient characteristic different from that residual characteristic. Complex coefficients there do not mean the local field is C.

A more recent cross-check is Beuzart-Plessis [5], §3.5.9 and Theorem 3.22. The generic multiplicity formula there retains the nonarchimedean hypothesis imposed in §3.5.1. It cannot be transplanted to arbitrary complex nongeneric Langlands quotients. The bounded search found no full resolution applicable to the target. This is not a claim that an exhaustive literature search proves the problem remains open.

## 3. Approach 1: multiplicity-aware orbit calculation

Here is an elementary expansion of the existing Aizenbud–Lapid upper bound, rather than a new distinction theorem. Let W_2 be the involutions of n labelled occurrences, and let g(w) be the number of transpositions. Define

    B_(p,q)(M) = sum over w in W_2 with wM=M^tau
                 binom(n-2g(w), p-g(w)),

where the binomial coefficient is zero unless its lower argument is between zero and its upper argument. For standard Langlands ordering, [2, Theorem B.1] bounds the dimension of the period space of both the standard module and its Langlands quotient by this number. The equality wM=M^tau here is coordinatewise for a labelled tuple, not merely equality of unordered multisets after a permutation.

For tau-stable M the following closed expression is exact:

    B_(p,q)(M) = (product_j b_j!)
      sum_(0 <= u_i <= floor(a_i/2))
        [product_i a_i! / (2^u_i u_i! (a_i-2u_i)!)]
        binom(n-2s_0-2u, p-s_0-u),
    where u = sum_i u_i.

For a nonstable multiset the value is zero.

Proof. An occurrence of a nonfixed character must be paired with an occurrence of its conjugate. There are b_j! matchings for the j-th pair and they contribute exactly b_j transpositions. Within a fixed-character block of size a_i, choose 2u_i elements and partition them into unordered pairs. This gives a_i!/(2^u_i u_i! (a_i-2u_i)!) involutions. No different fixed-character blocks can mix. The total transposition count is s_0+u and the number of fixed labels is n-2s_0-2u. Substitution in the defining sum proves the formula.

Consequently B_(p,q)(M)>0 if and only if M is tau-stable and s_0<=min(p,q). Indeed, every nonzero term has at least s_0 transpositions, proving one implication. Conversely take every u_i=0; the remaining binomial coefficient binom(n-2s_0,p-s_0) is positive exactly when s_0<=p and s_0<=q.

This positivity does not prove existence of a functional: a positive upper bound permits the actual dimension to be zero. The computation therefore recovers the known necessary combinatorial condition and gives an auditable diagnostic, not the converse.

Checks worth retaining:

- With no repeated characters, B=binom(n-2s_0,p-s_0).
- Two occurrences each of a nonfixed character and its conjugate give s_0=2, even though there is only one distinct pair. Signature (1,3) fails the condition; signature (2,2) has B=2.
- Two equal fixed characters and signature (1,1) have B=3. This is a count in an upper bound, not a claim that a period space has dimension 3.

## 4. Approach 2: elementary special cases and twisting

For n=1, H=U(1) for both possible signatures. Restricting chi_(k,s) to exp(i theta) gives exp(ik theta). A nonzero invariant functional on its one-dimensional space exists exactly when k=0. This is exactly tau-invariance, and proves the target in rank one. This is elementary and already covered by the known results.

A slightly broader elementary observation is useful for ruling out false new cases. For any s in C define nu_s(g)=|det(g)|^(2s), using the real logarithm of the positive modulus. Taking determinants in h*Jh=J gives |det(h)|=1 for h in H. Hence

    Hom_H(pi tensor nu_s,C) = Hom_H(pi,C)

on the same representation space, not just up to dimension. Multiplication by this common radial character also commutes with tau and preserves every equality and conjugate pairing of Langlands characters. Thus the condition and the answer are unchanged by this twist. Any case obtained from a known case by such a twist is an immediate corollary, not evidence of a solution in the genuinely remaining range.

The compact signatures and the finite-dimensional, spherical, and unitarizable classes are already accounted for in §2. Re-proving those classes would not settle the general nongeneric question, so this route was not developed into a novelty claim.

## 5. Approach 3: the precise quotient-descent issue

Let I be the standard module, q:I -> pi its continuous surjection, and K=ker(q). These are Frechet spaces and K is closed. Pullback gives the exact sequence at the first two nonzero terms

    0 -> Hom_H(pi,C) -> Hom_H(I,C) -> Hom_H(K,C),

where the last map is restriction. To prove this directly, a functional pulled back from pi vanishes on K. Conversely, an invariant continuous functional on I that vanishes on K descends uniquely to I/K. The Frechet open mapping theorem identifies the quotient topology with that of pi, so the descended functional is continuous and H-invariant.

Therefore the missing sufficiency statement requires a nonzero element of Hom_H(I,C) whose restriction to K is zero. Meromorphic continuation or the existence of a standard-module functional alone does not provide that assertion at a reducibility point.

The logical error in omitting this step is visible even for H=C^times. Take E=C e_0 direct-sum C e_1 with z acting by diag(1,z), K=C e_0, and Q=E/K. Every invariant functional on E is a multiple of the e_0-coordinate and is nonzero on K unless it is zero. Hom_H(E,C) is one-dimensional, while Hom_H(Q,C)=0. The single group element z=2 already verifies these assertions. This toy example is not a Langlands quotient for (GL_n(C),U(p,q)) and is explicitly not a counterexample to the target. It only disproves the general inference that distinction passes to every quotient.

No new vanishing argument on the actual Langlands kernel was found. This is where the attempted extension stops.

## 6. Bounded outcome and verification limits

Three substantive mathematical approaches were pursued: the orbit/multiplicity formula, elementary special-case and twist reduction, and quotient descent. Source and prior-attempt searches were preparatory checks, not extra mathematical approaches. The limit of five was not reached; work stopped because the remaining gap was identified without a route to close it.

No actual prior proof attempt was found in the bounded AlecKriebel/Math searches recorded in metadata. Empty connector search results are not a complete repository-history audit. The catalog's desk assessment is not counted as an earlier attempt.

The code independently enumerates labelled involutions in a finite test universe, compares the formula, and checks explicit adversarial examples. It cannot establish distinction for arbitrary representations or prove the cited analytic theorems. The all-size counting identity is justified by the proof in §3; finite enumeration is a regression test. Strict inventory, external manifest pinning, normal/optimized/relocated replays, and mutation tests protect the authored package. An uninvolved mathematical audit remains required before publication.

## References

[1] E. Lapid, “Unitary periods and distinction; representation-theoretic aspects,” in Automorphic Forms: New Directions, Oberwolfach Report 14/2011, especially p.732. https://doi.org/10.4171/owr/2011/14

[2] B. Feigon, E. Lapid and O. Offen, “On representations distinguished by unitary groups,” Publications Mathematiques de l'IHES 115 (2012), 185–323; Appendix B by A. Aizenbud and E. Lapid. https://doi.org/10.1007/s10240-012-0040-z

[3] M. Gurevich, “On a local conjecture of Jacquet, ladder representations and standard modules,” arXiv:1411.2420v2. https://arxiv.org/abs/1411.2420

[4] J. Zou, “Supercuspidal representations of GL_n(F) distinguished by a unitary involution,” Bulletin de la Societe Mathematique de France 150 (2022), 393–458; revised arXiv version 4, 2024. https://arxiv.org/abs/1909.10450 ; https://doi.org/10.24033/bsmf.2850

[5] R. Beuzart-Plessis, “Introduction to the relative Langlands program,” arXiv:2509.18062v1 (2025), §§3.5.1, 3.5.9, Theorem 3.22. https://arxiv.org/abs/2509.18062
