# Independent second priority audit: all-multiplicity sparse reduction

Started and source searches performed 2026-10-07 UTC. This is an independent
literature/interface audit, not a complete-package review or a formal proof
certificate. The first source searches and exact-source reads preceded reading
the first priority agent's note. That note was consulted later to identify
additional comparison families, not used as evidence for their statements.

## Exact target and candidate inspected

For a nonzero univariate polynomial with t nonzero terms and binary exponents at
most N, over an explicitly represented K = F_p[T]/(h) with deg h = m, recover
all distinct monic irreducible factors in dense form and their binary
multiplicities. Write D for the sum of the distinct factor degrees. The claimed
cost is polynomial in t, log(N+1), m, log p and D, including arbitrary
p-divisible multiplicities. It uses a validated dense factorization algorithm as
a dependency. It does not assert polynomial cost in the sparse encoding of the
output factors or solve arbitrary sparse-output GCD.

I read `code/sparse_cartier.py`, initially 9,601 bytes with SHA-256
`33dfca735400ec29ef34e787e691b1c9f060420962c17a8cd11d2f5de17c5693`.
The executable reduction itself is not novelty evidence. Its bounded prime
oracle is a feasible reference implementation, not an implementation of the
upstream large-characteristic theorem.

## Disposition

The all-multiplicity candidate identifies a concrete additional mechanism beyond
the tame precursor: repeated retention of a sparse numerator with a dense
auxiliary denominator, and control of that denominator by the original radical
degree and the number of descent levels. None of the exact statements inspected
below supplies that combined theorem. The old Padé, logarithmic-derivative,
Cartier and multiplicity arguments must remain attributed. In particular, neither
the coefficient-section product identity nor the known-root digit recursion
should be claimed as invented here. Lecerf's Lemma 2 and dense algorithms
already give the base-p multiplicity-residue decomposition and recursion; only
the compressed rational implementation and auxiliary degree control are the
candidate additional contribution.

This audit supports continuing rigorous development of the specific repeated
quotient invariant and complexity bound. It does not support an assertion of
being first, an unconditional proof of historical nonexistence, or immediate
publication before fresh full mathematical and package reviews. Failed searches
are not priority evidence. The positive distinctions below are the basis for the
recommendation.

## Exact positive comparisons

1. **Kaltofen (1988), rational reconstruction.** In *Greatest Common Divisors
   of Polynomials Given by Straight-Line Programs*, JACM 35(1), 231–264,
   §8, Algorithm Rational Numerator and Denominator and Theorem 8.1 give
   randomized reconstruction with complexity polynomial in the program length
   and reduced numerator/denominator degree bounds. The univariate Padé
   specialization at a known regular point is classical exact linear algebra.
   Adaptive doubling and verification are also present in Corollary 8.1. This
   positively covers the recovery of U'/U; it does not supply the later
   pth-root descent or its representation bound. I read the actual algorithm,
   theorem and corollary in the author-hosted primary PDF, not only its abstract.
   [Primary PDF](https://kaltofen.math.ncsu.edu/bibliography/88/Ka88_jacm.pdf).

2. **Mattarei (2005/2006), sparse multiplicities.** *Root multiplicities and
   number of nonzero coefficients of a polynomial*, arXiv:math/0512239,
   Theorem 2 bounds the weight by the product of one plus each base-p digit of
   the exact nonzero-root multiplicity. Its proof groups exponent residues and
   reduces to lower digits. In particular, the lowest multiplicity residue is
   at most t−1. The known-root recursion is a constructive development of that
   proof and the distinct-residue linear algebra. This paper contains no
   complete sparse factoring algorithm or auxiliary quotient invariant.
   First public arXiv submission: 12 December 2005; exact inspected PDF v2:
   20 January 2006. [Version record](https://arxiv.org/abs/math/0512239),
   [inspected primary version](https://arxiv.org/pdf/math/0512239v2).

3. **Dutta–Saxena–Sinhababu (2017 onward), small radical and prime
   characteristic.** *Discovering the roots: Uniform closure results for
   algebraic classes under factoring* first appeared publicly on arXiv on
   9 October 2017. Theorem 1 gives a small-radical circuit-size conclusion
   under the paper's characteristic-zero/algebraically-closed default. The
   full author JACM version §6.3, Theorem 28 treats only rad_p, whose factors
   have multiplicities not divisible by p. It explicitly separates the
   high-degree pth-power obstruction; its dense interpolation root descent
   retains numeric degree dependence. These are strong positive antecedents
   of visible-radical extraction, but not the all-multiplicity sparse theorem.
   I read §§1.2, 6.2–6.3 and the exact Theorems 1, 27 and 28.
   [Version record](https://arxiv.org/abs/1710.03214),
   [inspected author PDF](https://www.cse.iitk.ac.in/users/nitin/papers/factor-closure-jacm.pdf).

4. **Rowland–Yassawi (2013/2014/2015), Cartier sections.** *Automatic
   congruences for diagonals of rational functions*, Definition 1.7 and
   Proposition 1.9 supply the coefficient-section operation and pull-out
   identity. Theorem 2.1 concerns automatic coefficient sequences and a fixed
   rational denominator; it is not a factoring theorem. These results directly
   antecede the candidate's individual equation C_0(A H^p)=C_0(A)H, after
   inverse coefficient Frobenius over a perfect finite field. First public
   arXiv submission: 31 October 2013; inspected v2: 23 April 2014; journal
   DOI 10.5802/jtnb.901, 2015. I read the exact definition, proposition and
   theorem proof. [Primary text](https://arxiv.org/html/1310.8635),
   [version record](https://arxiv.org/abs/1310.8635).

5. **Bostan–Christol–Dumas (2016), rational section closure.** *Fast
   Computation of the Nth Term of an Algebraic Series over a Finite Prime
   Field*, §2.3, equation (7), gives the section product identity; §3.2
   maintains rational functions through S_r(a/b)=S_r(a b^(p−1))/b.
   Theorem 9 has preprocessing cost proportional to numeric p, alongside
   logarithmic dependence on the desired coefficient index. Thus even this
   refined exact rational-section algorithm cannot be cited as a log-p sparse
   factorization bound. First submission: 1 February 2016; inspected v2:
   18 May 2016. [Primary version](https://arxiv.org/html/1602.00545v2),
   [version record](https://arxiv.org/abs/1602.00545).

6. **Demin–van der Hoeven (2023/2025), general sparse factoring.**
   *Factoring sparse polynomials fast*, §§1.1, 1.4 and 2.1 explicitly permit
   polynomial dependence on numeric total input degree d and use randomized
   sparse evaluation/interpolation. Section 5.3 assumes characteristic zero
   or greater than d² for the stated squarefree algorithm; §7.7, Theorem 7.6
   has O~(d³ s-bar+d^10) arithmetic cost plus a dense factorization of degree
   O(d²). This does not become poly(log N,D) by replacing the dense oracle.
   First public arXiv version: 28 December 2023; inspected final author PDF:
   23 February 2025; journal DOI 10.1016/j.jco.2025.101934. I inspected the
   exact sections and theorem, including their complexity-model definitions.
   [Author PDF](https://www.texmacs.org/joris/sparsefact/sparsefact.pdf),
   [public version record](https://arxiv.org/abs/2312.17380).

7. **Bhattacharjee–Kothary–Rai–Saraf (2026), low individual degree
   factors.** arXiv:2606.27293v1, submitted 25 June 2026, covers bounded
   individual input degree or bounded-degree factors of general sparse input.
   Theorems 1.7 and 5.1 give the exact general-case bound
   poly(s^(d² log n), binom(N,≤d)^(log s), n) T(F,N), and permit spurious
   candidates. Here N is the input individual degree, d is the desired factor
   degree, s is input sparsity, and T is the dense univariate factoring cost.
   Theorem 2.13 supplies T(F_(p^m),N)=poly(N,m,p), with numeric-p dependence.
   Consequently it does not imply the desired binary-N/all-multiplicity
   full-factorization statement, even with the new dense factoring oracle.
   I inspected §1.1, the displayed bounds, §2.3 and the later proof's
   characteristic assumptions. [Primary version](https://arxiv.org/html/2606.27293v1),
   [version record](https://arxiv.org/abs/2606.27293).

8. **Lecerf (2007/2008), established residue descent and dense squarefree
   factoring.** *Fast separable factorization and applications*, author PDF
   dated preliminary 6 June 2007 / revised 9 October 2007; AAECC 19(2)
   (2008), 135–160, DOI 10.1007/s00200-008-0062-4. Section 2.1, p.5,
   explicitly represents a degree-d polynomial by its d+1 coefficient vector
   in a computation-tree arithmetic model. Lemma 2, p.6, gives
   F(y)=S_0(y) S_1(y^p), with separable multiplicity residues at most p−1.
   Algorithm 1, pp.6–7, begins with dense gcd(F,F'), computes dense F/S_0
   and deflates it. Algorithm 3, p.10, recurses and merges; Proposition 5
   gives O(M(d) log d) field operations. Corollary 2, p.17, gives finite-field
   squarefree decomposition in O(M(d) log d+d log(q/p)) field operations.
   The parameter d is numeric total input degree. Thus this is a direct
   positive antecedent for the residue decomposition and full recursion, but
   does not state the compressed sparse/dense representation or its D bound.
   I read the introduction, computational model, Lemma 2, Algorithms 1–3,
   Proposition 5 and §4.1 through Corollary 2 in the actual author PDF.
   [Author PDF](https://www.lix.polytechnique.fr/~lecerf/publications/Lecerf:2007:fsfa.pdf),
   [journal DOI](https://doi.org/10.1007/s00200-008-0062-4).

9. **Further recent exact-root and sparse factoring comparisons.** The
   independently delegated primary-source check is complete; its exact scope,
   statement locations and versions are saved in
   [sparse_priority_second_recent.md](sparse_priority_second_recent.md).
   Huang–Cao–Qiu–Gao, arXiv:2607.02364v1 (2 July 2026), Theorem 5.2,
   extracts roots for a supplied exponent at numerical input-degree-dependent
   cost plus scalar-root cost. Chuyoon–Shpilka, arXiv:2603.07589v1
   (8 March 2026), Theorems 1.9 and 1.12 bound input individual degree;
   Theorem 1.10 counts repeated factors in its parameter ell. Its finite-field
   oracle in Theorem 2.7 costs poly(p,log q,d), with numeric p.
   Giesbrecht–Roche, arXiv:0901.1848v2 (3 December 2010), finite-field
   Theorem 2.12 requires characteristic greater than input degree and is
   Monte Carlo; root extraction Theorem 3.5 uses Conjecture 3.3 and numerical
   supplied root exponent. The delegated note records a four-term family
   (x−1)^(p^k)(x+1)^(p^k+1), with D=2 and arbitrarily large coprime
   multiplicities, to distinguish complete multiplicity recovery from an
   exact-power task. These positive scope distinctions are not proof of
   nonexistence of an equivalent composition in other literature.

## Why the specific invariant matters

This paragraph is my own algebraic comparison, not a theorem attributed to any
source. Suppose the current polynomial is F=U/V, V divides U, U is sparse,
U(0)V(0) is nonzero, and rad(F) has degree at most the original D. Put E=deg V.
Then rad(U) has degree at most E+D, including temporary factors introduced by
the denominator. If A_U records the base-p multiplicity residues of U,
U=A_U H_U^p, all exponents in A_U are at most p−1. The zero section yields
H_U=C_0(U)/C_0(A_U), and deg C_0(A_U) is at most deg(A_U)/p.
For the analogous residue decomposition V=A_V H_V^p, deg H_V≤E/p.
The new auxiliary denominator therefore obeys

    deg V_new ≤ ((p−1)(E+D))/p + E/p
              = E + (1−1/p)D ≤ E+D.

For construction cost, use the separate Mattarei bound on every visible residue:
deg A_U≤(t−1)(E+D). No algorithm may loop to p merely because the degree
analysis uses p−1. The section keeps at most t numerator terms and shrinks
its exponent bound by p. In combination these observations give a potentially
non-immediate representation/complexity result across all descent levels.
The old rational-section algorithms keep a fixed denominator and compute its
(p−1)st power; that operation is precisely what the present candidate avoids.

The argument must still be checked for polynomiality of F_new, signed
multiplicity telescoping, exact Padé rejection of accidental truncated matches,
binary coefficient/exponent work, all boundary cases and final completeness.
Those are mathematics-review duties, not settled by this priority audit.

## Hardness boundaries and scope limits

Qiu–Cao–Huang–Feng–Gao, arXiv:2606.12144v1, first submitted 10 June 2026,
Theorems 3 and 4 concern sparse-output GCD and roots-of-unity detection.
Their complexity parameters are input/output term counts and log input degree.
They do not impose a small dense degree on the entire radical of each input.
Thus a radical-degree-sensitive full factoring algorithm would not directly
contradict them: their squarefree X^M−1 input already has radical degree M.
I read the exact theorems and input model.
[Primary version](https://arxiv.org/html/2606.12144v1),
[submission record](https://arxiv.org/abs/2606.12144).

Gianni–Trager's *Square-free algorithms in positive characteristic*, AAECC 7(1)
(January 1996), 1–14, DOI 10.1007/BF01613611, remains classical attribution.
The primary publisher and IBM records were consulted, and Gianni's author
publication list was searched. The Pisa institutional record explicitly lists
no associated file; the publisher PDF endpoint redirects to subscription
content. No accessible complete primary manuscript was obtained in this audit.
I do not exclude a mechanism from that paper based on its abstract, and do not
claim to have checked its proof.

The exact primary citation chain in Lecerf supplies a bounded comparison:
the introduction, p.2, says Gianni–Trager is derived from Musser and has
inherent quadratic cost; §4.1, p.16, cites Gianni–Trager §4, Proposition 13,
Proposition 16, Corollary 4 and its theorem on p.13 for the relationship
between separable and squarefree decomposition and constructive hypotheses.
Lecerf then explicitly analyzes a dense coefficient-vector implementation.
This justifies attribution of established perfect-field residue descent and
the positive dense-model comparison; it does not substitute for inspection
of every Gianni–Trager algorithm or certify historical nonexistence of the
compressed invariant. Any firstness assertion would remain unjustified.
[Publisher record](https://link.springer.com/article/10.1007/BF01613611),
[IBM record](https://research.ibm.com/publications/square-free-algorithms-in-positive-characteristic),
[author list](https://people.dm.unipi.it/gianni/listapap.htm),
[Pisa institutional record](https://arpi.unipi.it/handle/11568/47744).

I also checked current primary source chains through Kaltofen's 1987
single-factor Hensel lifting paper and the 2025/2026 factoring survey. They
distinguish circuit-size conclusions from uniformly constructible algorithms
and retain inseparability qualifications. No equivalence to the candidate's
repeated quotient theorem was established. Searches in the pinned upstream
family142 TeX/Markdown sources found no sparse/lacunary/Cartier theorem. A
later keyword search across all pinned upstream preprints' TeX/Markdown for
Cartier near factor/root, sparse near factoring, and lacunary found only
unrelated papers using Cartier divisors; no relevant sparse finite-field
statement was identified. These searches are bounded by their terms and
formats; absence of those words is not itself novelty evidence.

## What was and was not reviewed

Primary exact-source comparisons above; a read of the current reduction; the
elementary auxiliary denominator estimate. No full code test campaign, Lean
formalization, proof of the upstream analytic theorem, whole-package license
review, Zenodo metadata review or production publication operation occurred.
No person was contacted. Research-only PDF material is excluded from authored
publication files and is not redistribution authorization.

The independent recent-paper check's completed note was read and reconciled
above. It used a further independent exact Giesbrecht–Roche check. This closes
the assigned bounded source audit, with the explicit Gianni–Trager direct
access limitation. Original exact-source bytes, versions and read scopes are
recorded in `sources/sparse_priority_second_manifest.json`; hashes pin material,
not public priority.

Final checkpoint: 2026-10-07 UTC. Assigned bounded priority audit completion
100%; best-guess mathematical resolution of the new candidate 55% on this
limited audit basis; publication package eligibility 0% on the same basis.
These estimates are not mathematical or priority evidence. No whole-package
approval or publication recommendation is given by this limited audit.
