# Rationality below four: research and proof audit

Date: 2026-10-21 UTC. Queue row 1854, ID 30005762, source OWR-14298158-007.

## Verdict and priority

**Not solved.** No proof or counterexample to the general conjecture was obtained. The verified exact partials below are applications or elementary derivations, not claimed new theorems of research significance. The target remains every finitely based hereditary classical permutation class C with limsup |C_n|^(1/n)<4; no sum-closure or well-quasi-order hypothesis is added.

A fresh search on 21 October 2026 checked Brignall–Opler/rationality/below-four queries, Opler's publication list, the official PP2025 abstract and Brignall slides. No complete Brignall–Opler manuscript was located. The author's /research/ URL failed, so it contributes no negative evidence. Search failure is not a proof of nonexistence.

Established literature already covers all sub-kappa classes (kappa approximately 2.20557), all separable below-four classes, and proper finitely based subclasses of Av(321) or Av(123). The 2025 conference theorem announces the general finite-basis result below Phi=(3+sqrt(5))/2. It must remain labelled **announced, complete proof not recovered**, rather than independently audited. Its public outline uses concentrated cell classes, special grid components, insertion encodings, and monadic second-order definitions. The slides state concentration fails at Phi; a simple extension of that same concentration argument to 4 is therefore unavailable. This is a method barrier, not a disproof of the conjecture.

A correction to the inherited source gate: Av(132) is not sum-closed, since 1 direct-sum 21 equals 132. The Catalan boundary example Av(132) itself remains correct; for a sum-closed Catalan example use Av(231), since the pattern 231 is sum-indecomposable. No other claim here relies on that incorrect adjective.

The present target and row 1848's separable converse have disjoint unresolved growth domains. Nothing here settles that converse.

## Approach 1: structural exclusion and a finite six-witness filter

Use the established separable theorem and proper-subclass theorem, rather than assume that small growth forces separability.

**Exact corollary.** If a finitely based class C of upper growth <4 avoids any permutation of length three, then its generating function is rational.

Proof. For monotone patterns use the proper-subclass theorem for Av(321), or reversal for Av(123). Properness follows because the whole class has Catalan growth 4. For a nonmonotone length-three pattern tau, both 2413 and 3142 contain tau (this can be checked for each of 132,213,231,312). Thus Av(tau) is separable. Each of the four nonmonotone length-three avoidance classes has growth 4, so none can be contained in C. The established separable theorem gives strong rationality of C. Finite basing is needed for the monotone branch; it is not silently imposed on the separable theorem.

Consequently any counterexample must contain all six length-three permutations, and its minimal basis has no member of length at most three.

**Necessary finite certificate.** If C=Av(B) has upper growth <4, then for each tau in S_3 there is beta in B avoiding tau. Indeed, failure means B is disjoint from Av(tau), and heredity gives Av(tau) subset Av(B), contradicting growth <4. Conversely, a witness beta in B intersect Av(tau) proves that inclusion fails. This is an exact inclusion test, not a sufficient test for growth <4 or rationality. One beta may witness more than one tau.

Outcome: a rigorous pruning rule and a solved structural region, but no structural theorem covering all classes with all of S_3 present.

## Approach 2: explicit rational families approaching the boundary

This elementary derivation makes the strict threshold concrete and prevents an unjustified uniform finite-state bound.

Let i_k=12...k and C_k=Av(132,i_k), for fixed integer k>=2. Let F_k(x) count C_k, including the empty permutation, and set F_1=1. Decompose a nonempty 132-avoider uniquely at its maximum as L n R. Every value in L exceeds every value in R, or an entry from L, then n, then an entry from R would form 132. The longest increasing subsequence therefore has length max(LIS(L)+1,LIS(R)). Hence

F_k=1+x F_{k-1} F_k, so F_k=1/(1-x F_{k-1}).

Put P_0=P_1=1 and P_k=P_{k-1}-xP_{k-2}. Induction gives F_k=P_{k-1}/P_k, with

P_k(x)=sum_{j=0}^{floor(k/2)} (-1)^j binom(k-j,j)x^j.

Adjacent P's have no common root: their constant terms are 1, and a nonzero common root propagates by the recurrence down to P_0=1. Thus the displayed fraction is reduced and its denominator degree is floor(k/2).

For x>0, P_k(x)=x^(k/2) U_k(1/(2 sqrt(x))), where U_k is the Chebyshev polynomial of the second kind; this identity also follows directly from the recurrence. Its smallest positive zero is r_k=1/(4 cos^2(pi/(k+1))). No cancellation occurs. The nonnegative counting series has radius r_k; equivalently its upper growth is

lambda_k=4 cos^2(pi/(k+1))<4.

For k>=2 the smallest positive pole is unique in modulus (all roots of P_k are positive real), so the ordinary growth limit also exists and equals lambda_k. As k increases lambda_k tends to 4, while every fixed k gives a finitely based rational class. The union over all k is Av(132), whose Catalan generating function is nonrational with growth 4. Taking a union is not a rationality-preserving operation.

This proves that there is no uniform bound on reduced rational denominator degree across all finitely based sub-four classes. In particular no common bound on states of unweighted length-preserving finite automata can enumerate every such class bijectively: a d-state transfer matrix gives denominator degree at most d. It does not rule out bounds depending on basis length or a fixed growth gap.

Outcome: exact near-boundary examples, not a counterexample. The formulas are classical in substance and no novelty is asserted.

## Approach 3: sum/skew decomposition and exact growth certificates

For an actually sum-closed class, let I(x) count its nonempty sum-indecomposable members. Unique decomposition into direct-sum components gives F=1/(1-I), as a formal identity. Therefore F is rational if and only if I is rational. This reduces rather than solves the problem when I is infinite.

If the set of indecomposables is finite and nonempty, I is a polynomial with nonnegative coefficients and zero constant term. There is a unique positive root r of I(r)=1. Positivity shows that no singularity has modulus less than r; the denominator vanishes at r without cancellation. Thus upper growth is 1/r, and strict sub-four growth is equivalent to the exact rational inequality I(1/4)<1. The empty-only class is a trivial separate case. For an infinite indecomposable set, a finite partial sum I_N(1/4)>=1 is a valid obstruction to strict sub-four growth of its sum closure; no finite partial sum <1 is by itself an upper certificate.

This is a computable certificate for a proven finite-indecomposable sum-closed specification. It is not valid to replace an arbitrary C by its sum closure while preserving the growth hypothesis. For an explicit counterexample to that reduction, set m=12, form pi as the direct sum (in lexicographic order) of all length-m permutations whose first entry is m, and let C=Sub(pi). This is a finite hereditary class, hence finitely based: every minimal nonmember has size at most |pi|+1. It has growth zero. Its sum closure contains at least (m-1)! distinct sum-indecomposables of length m: each selected permutation starts with its maximum, so no proper initial segment can be the set of smallest entries. Their weighted sum at 1/4 is 11!/4^12>1. The sum closure of these finitely many indecomposables already has growth >4, by the preceding polynomial criterion. This provides an explicit finite counterexample to growth preservation under sum closure, not to the original conjecture.

The skew-sum version follows by reversal. Outcome: exact closure certificates and an obstruction to an otherwise tempting reduction; no rationality proof for the general finite-basis indecomposable language.

## Approach 4: finite-state/MSO encodings with verifiable bounds

A sufficient rationality certificate consists of a finite alphabet, a regular language, a length-preserving bijection from its accepted words to C, and a proved interpretation of avoidance. For a deterministic automaton with transition-count matrix A, initial row u, and accepting column v, the exact count is u(I-xA)^(-1)v. Epsilon conventions and inclusion of the empty permutation must be stated. A regular superlanguage or an injection proves only an upper bound, not rationality of C.

For finite B, if the two coordinate orders of encoded permutation points are definable in MSO on words, occurrence of any fixed beta in B is expressible by finitely many existentially chosen positions and their required order comparisons. Its negation and a finite conjunction express avoidance. The missing work is not this finite logical expression: it is a uniform correct encoding for all of the class, including canonical treatment of multiple griddings. Merely having regular encodings of gridded objects can overcount ungridded permutations.

**Exact upper-growth certificate.** Suppose a length-preserving injection of C into a weighted finite automaton has been proved. Let M(x) be its polynomial transition matrix with nonnegative integer coefficients counting paths, assume no problematic zero-weight cycles, and let boundary weights also have nonnegative integer polynomial coefficients counting boundary choices. Supply a rational q>1/4 and a rational positive vector w with M(q)w<w coordinatewise. In the norm max_i |z_i|/w_i, M(q) has norm at most max_i (M(q)w)_i/w_i<1. Its Neumann series converges; the dominating language series is finite at q. Coefficient domination then gives upper growth(C)<=1/q<4. All vector inequalities are exact rational arithmetic. For zero-weight transitions, the same strict contraction certificate suffices directly, so the extra no-cycle convention can be replaced by verified convergence.

This certificate establishes strict growth even for an injective non-surjective code. Rationality additionally needs a regular exact cross-section, not just the injection. With such a bijection, transfer-matrix algebra proves the rational function for every coefficient, without extrapolation.

Outcome: a complete acceptance standard for individual automaton-based successes. The announced sub-Phi method motivates it, but no below-four global encoding or concentration replacement has been proved here.

## Approach 5: algebraic grammars, finite enumeration, and counterexample search

A nonlinear positive algebraic specification does not by itself force growth >=4. For instance H(x)=1+x^2 H(x)^2 has the unique nonnegative solution H(x)=C(x^2), where C is Catalan. It is nonrational and has upper growth 2. But this is not a permutation-class counterexample: it has objects of length two and no object of length one, contradicting heredity. Reinterpreting x^2 as a block size does not fix closure under deleting individual entries. Any proposed grammar counterexample must prove both that its objects are all and only Av(B) for an explicit finite B and that its size is permutation length.

Finite coefficient agreement is also insufficient. For every N, the finite class D_N of 132-avoiders of length at most N has finite basis {132} union {all 132-avoiders of length N+1}; this union need not be a minimal basis, which is irrelevant to finite basing. Its polynomial generating function agrees with the nonrational Catalan series through x^N. Thus finite enumerations cannot distinguish even a finite rational class from a nonrational hereditary finitely based class unless additional structural information is used. The latter has growth exactly 4, so this example audits inference, not the strict target.

A genuine finite-basis candidate search can use the six-witness test, symmetry reduction, exact enumeration, and guesses of recurrences to prioritize candidates. It cannot accept a guessed rational function, numerical growth estimate, or apparent singularity as proof. For a counterexample one needs an exact nonrational generating function or another rigorous nonrationality argument, and a rigorous strict upper-growth certificate, all for the same actual class. For a positive result one needs an exact decomposition or language proof, not just a recurrence fit.

Outcome: two explicit failure mechanisms for seductive purported proofs and a proof-carrying search standard. No candidate satisfying all counterexample obligations was found or asserted.

## Source pointers and status boundaries

- Brignall, open problem 6, Mini-Workshop: Permutation Patterns, OWR 6/2024, printed p.286: https://doi.org/10.4171/owr/2024/6 . Exact source already visually inspected in recovery.
- Albert–Atkinson–Vatter, Subclasses of the separable permutations, Theorem 4.1: https://arxiv.org/abs/1007.1014 . Established input for Approach 1.
- Albert–Brignall–Ruskuc–Vatter, Rationality for subclasses of 321-avoiding permutations, Theorem 1.1: https://arxiv.org/abs/1602.00672 . Properness is essential.
- Albert–Ruskuc–Vatter, Inflations of geometric grid classes of permutations, Theorem 8.5: https://arxiv.org/abs/1202.1833 . Established sub-kappa result, not sub-four.
- Brignall–Opler, PP2025 abstract, printed p.35: https://sites.cs.st-andrews.ac.uk/pp25/program/booklet-pp25.pdf ; slides https://www.rbrignall.org.uk/talks/2025-07-07-PP25.pdf . Announcement and outline only, not a recovered complete proof.
- Opler publication list checked anew: https://oplermic.pages.fit/publications.html . No corresponding full manuscript identified in this bounded search.
- Brignall–Vatter, Uncountably many enumerations of well-quasi-ordered permutation classes: https://arxiv.org/abs/2211.12397 ; 2026 publication https://doi.org/10.5070/C66165703 . Wqo alone is not a general enumerative cure.

The mathematical analysis is authored work. No copied third-party source documents or dataset contents are included in this package.

## Reproducibility

check_partials.py independently enumerates actual permutations through length 8 for C_k (k=2 through 7), checks the polynomial recurrence against its binomial formula through k=20, verifies the nonmonotone length-three containments, and checks 11!/4^12>1 using exact fractions. CHECK_RESULTS.json records the successful run. These computations are finite sanity checks; the proofs above, not the computed prefixes, support the infinite claims.
