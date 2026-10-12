# Independent audit: modular Sidon obstruction and exact carries

Audit date: 12 October 2026 UTC. Target: row 1741 / problem 2350 / Erdős 864.

## Verdict and required wording

**ACCEPT the two finite-group theorems and their restricted consequences.** The proofs are elementary and valid for every finite abelian group under the stated strong Sidon convention, including diagonal pairs. The carry formulas are valid for an injective lift of the modular set. They do not solve the unrestricted interval problem, improve its unrestricted leading upper constant, construct an asymptotic counterexample, or establish novelty.

**Required editorial clarification before presenting Section 4 as a standalone statement:** replace its opening sentence by:

> Let q be a positive integer, and let b₁,…,bₖ be integers with pairwise distinct residues modulo q whose residue set B is a strong Sidon set of cardinality k.

The existing notation |B| = k and the subsequent word “lift” support this intended interpretation. Nevertheless, distinct integers alone need not have distinct residues. Without injectivity, equation (4) can fail: the distinct integers {3,6} reduce to the strong singleton {0} modulo 3. Their 16 ordered quadruples are all congruent solutions, whereas the singleton has R(0) = 1. The clarification makes the existing intended argument explicit; it does not modify Theorems 1 or 2.

For the alternative half-integer formulation, “half-integer lattice” should mean the single coset Z + 1/2, as in the reflected-set setting. More generally the direct integer-carry sentence requires that a+b+c−d be integer-valued. The safe instruction to scale by 2 is valid for every subset of (1/2)Z, including mixed parity.

## Artifact identity and independence

The entire supplied proof was read. Its SHA-256 matches the requested audit anchor:

- PROOF.md: 10,051 bytes; 5687edc531996d229dff371574472c398604308f85376d2a71ad52bd7af1469b
- RESULTS.json: 3,487 bytes; aaffd17d2fedc85752626ff429974ddc9541767fe3b9aa8e594e5e04616f5a46
- check.py: 2,534 bytes; 1db7c3e01ae49ce5bf510a194e83b4dd37380ebcd98e1a0562a29fdf71c4f9c2

No separate author manifest was supplied or found in the three-file source directory. SOURCE_PINS.json records independent observations, not an invented author seal. The author's checker was hashed as an opaque file but was not inspected, imported, or executed. Fresh diagnostic code was written from the mathematical statements. Author RESULTS.json was read and its numerical claims were independently reproduced.

## 1. Difference uniqueness, diagonal sums, and torsion

Take a strong Sidon set B of cardinality k in a finite abelian group G. If a−b = c−d is nonzero, then a+d = c+b. The strong Sidon property makes the unordered multisets {a,d} and {c,b} equal. One pairing gives a=c and b=d, hence identical ordered difference representations. The other forces a=b and c=d, contrary to nonzero difference. Thus D has exactly k(k−1) members.

In particular, no element of D has order two: otherwise reversing its two distinct endpoints would give a second ordered representation. No assumption that multiplication by 2 is invertible has been made. The k(k+1)/2 unordered pairs with repetition have distinct sums by the exact hypothesis, so |S| = k(k+1)/2. Diagonal pairs cannot be discarded or combined with a distinct-entry representation.

In a group of exponent two, every double is zero, so a strong Sidon set has at most one point. A singleton never avoids its triple sum because 3b=b. The avoidance theorem is therefore vacuous for nonempty sets in such a group, while the counting identity still applies. Even-order groups of larger exponent are covered without change. Independent checks included every noncyclic abelian group of order at most 16.

## 2. Theorem 1 and the exact avoidance criterion

Assume B is nonempty and avoids 3B. If a+b is a nonzero difference c−d, then c=a+b+d gives a forbidden solution. Thus S∩D is empty. If a+b=0, choose any c in B; then c=a+b+c is forbidden. Hence zero is absent from S as well as from D.

The disjoint union S∪D fits inside G\{0}. Therefore

    k(k+1)/2 + k(k−1) = (3k²−k)/2 ≤ q−1.

Solving 3k²−k−2q+2 ≤ 0 gives exactly

    k ≤ (1 + sqrt(24q−23))/6.

The converse uses no Sidon property: a+b+c=d implies a+b=d−c, which is either zero or in D. Therefore S∩D=∅ together with 0∉S is equivalent to triple avoidance. Nonemptiness is used in the forward proof to select c; the empty case also satisfies the equivalence directly and causes no hidden exception. The trivial group has no nonempty triple-free subset. Singleton avoidance is exactly 2b≠0.

The bound is genuinely attainable at small parameters: B={1,2} in Z/6 is strong Sidon and triple-free, and (3k²−k)/2=5=q−1. This is an audit diagnostic, not an asymptotic construction claim.

## 3. Theorem 2, translations, and perfect difference sets

Translation preserves both the strong Sidon property and the difference multiset. It does not require division by 2: adding 2t to all pair sums is a bijection of G even when G has 2-torsion.

For any translate, ordered difference multiplicity is k at zero, 1 on D, and 0 on H=(G\{0})\D. Counting the equation a+b=d−c by its common value gives

    R(t) = sum_{u∈D} r_t(u) + k r_t(0).

There are k² ordered pairs in total. Subtracting the contributions from H and zero and then restoring k copies at zero yields

    R(t) = k² − sum_{u∈H} r_t(u) + (k−1)r_t(0).

A diagonal unordered pair contributes 1 to its ordered multiplicity, a pair with distinct entries contributes 2, and no two unordered pairs share a sum. Thus r_t(u)≤2. Since k≥1, the zero correction is nonnegative. Consequently

    R(t) ≥ k²−2h = 3k²−2k−2q+2.

The bound may be negative; nonnegativity then supplies the useful bound. No equidistribution, average over t, cyclicity, or odd-order restriction enters the identity or inequality.

Along any sequence with q→∞ and k/sqrt(q)→1, the difference capacity gives h=q−1−k(k−1)=o(q), and the displayed lower bound is (1−o(1))q uniformly in t. The error depends only on q and k, making the uniformity explicit. This statement counts ordered quadruples and allows repetitions; it is not a claim about that many disjoint or distinct-entry solutions.

When h=0, the formula becomes R(t)=k²+(k−1)r_t(0). Because r_t(0) belongs to {0,1,2}, the listed three possible numerical values are correct. “One of” does not assert that all three are realized. Small k can make the displayed values coincide. No translate of a nonempty perfect difference set can have R(t)=0.

## 4. Integer carries and interval endpoints

For pairwise distinct residues, reduction maps the k chosen integers bijectively onto B. The lift is also strong Sidon over the integers: an exact pair-sum equality reduces to a modular equality, and injectivity recovers the same unordered pair of lifted elements. Reduction maps ordered quadruples bijectively onto B⁴. A modular solution has one uniquely determined integer j with a+b+c−d=jq. Partitioning the finite solution set by this integer gives sum_j C_j=R(0). Integer triple avoidance is exactly C₀=0, so the nonzero carries bear all R(0) coincidences and satisfy the asserted lower bound.

If every representative lies in [1,L], then each quadruple satisfies

    3−L ≤ a+b+c−d ≤ 3L−1.

Dividing by the positive q gives precisely (6). If L≤q, the lower endpoint is strictly greater than −q and the upper endpoint is strictly less than 3q. Thus the only possible integral carry indices are 0,1,2. With C₀=0 the necessary bound on C₁+C₂ follows. This includes q=1 and endpoint cases. General lifts outside [1,q] may have negative or larger positive carry indices, which is why the unrestricted identity sums over all integers.

For {2,3}, the ordinary unordered sums are 4,5,6 and the smallest triple sum is 6>3, so the integer set is strong Sidon and triple-free. Modulo 3 the sums are 1,2,0 and D={1,2}; hence h=0 and r(0)=1, giving R=4+1=5. Direct ordered enumeration gives C₁=1 and C₂=4, exactly as claimed. This explicitly defeats the proposed inference from integer avoidance to modular avoidance.

## 5. Half-integer reduction

Multiplication by 2 is an injective map from (1/2)Z into Z, preserving all exact pair-sum equalities and the triple-to-single equation. The numerical upper endpoint changes from L to 2L, so a sharp coefficient against sqrt(L) cannot simply be copied from a statement against sqrt(2L).

For odd q, φ(b)=(2b)·2⁻¹ mod q is well-defined. On the coset Z+1/2, δ=a+b+c−d is an integer because its numerator has even parity. Then φ(a)+φ(b)+φ(c)−φ(d)≡δ mod q, so modular solutions correspond exactly to integer multiples δ=jq. Pairwise distinct modular images are still required. For mixed integer and half-integer elements, δ need not be integer; one must use the scaled formulation or state a correspondingly half-integral carry convention instead of silently invoking ordinary integer carries.

## 6. Literature applicability check

The official journal PDF was inspected on 12 October 2026: [Miquel Ortega and Sean Prendiville, “Extremal Sidon Sets are Fourier Uniform, with Applications to Partition Regularity,” Journal de Théorie des Nombres de Bordeaux 35 (2023), 115–134](https://jtnb.centre-mersenne.org/item/10.5802/jtnb.1239.pdf), DOI [10.5802/jtnb.1239](https://doi.org/10.5802/jtnb.1239).

Theorem 1.2 is the Fourier-uniformity theorem, on printed page 116. Theorem 1.15 begins on printed page 118 and requires at least five nonzero-coefficient variables, together with a nonempty zero-sum coefficient subset. Therefore its direct conclusion does not cover a+b+c=d, which has four variables. The document's applicability statement is accurate. This check does not rule out other Fourier arguments, and the audited proofs have no dependency on that paper.

## 7. Fresh exact diagnostics

The new independent_diagnostics.py uses finite direct-product addition tables, unordered-pair sum injectivity, and direct four-index enumeration for R. It neither imports nor executes the author's checker. Explicit exception checks remain active under Python optimization.

- All subsets of cyclic groups Z/q for 1≤q≤19 were enumerated.
- All subsets of every noncyclic abelian group of order at most 16 were enumerated: C₂², C₂³, C₂×C₄, C₃², C₂×C₆, C₂⁴, C₂²×C₄, C₄², and C₂×C₈.
- Total: 28 groups and 1,315,854 subsets, including empty sets.
- 8,332 subsets passed the strong Sidon definition.
- Every translation was tested explicitly: 135,001 translated instances.
- 17,437,811 ordered quadruples were directly examined across these instances.
- For cyclic groups, 21,762 integer lifts were checked, including canonical positive representatives and two noncanonical choices with negative or enlarged representatives.
- For odd cyclic moduli, 4,759 single-coset half-integer lifts were checked.
- The avoidance/disjointness equivalence was separately checked on every subset, without a Sidon filter, for q=1,…,11: 4,094 cases.
- Every applicable author RESULTS.json count for q=1,…,17, including all 3,990 strong Sidon subsets and each ordered-coincidence total, was reproduced exactly.
- The {2,3} carry example was checked separately.

All checks passed in normal Python, Python -O, and Python -OO, with identical totals. Source hashes were rechecked after the replay and were unchanged. DIAGNOSTICS.json gives exact per-group data. These finite diagnostics support implementation correctness; the universal conclusions rest on the preceding algebraic proofs.

## 8. Scope boundary and disposition

If modular avoidance is actually proved and representatives lie in (0,L] with q≤(1+o(1))L, Theorem 1 implies the claimed coefficient sqrt(2/3) for this restricted strategy. It does not justify replacing q by L otherwise. The possibility q≫L remains open, as does a dense modular seed whose integer representatives eliminate all exact equalities by nonzero carries.

The supersaturation identity obstructs certifying near-perfect seeds merely by modular translation. It does not obstruct all integer lifts: the nonzero carries are an allowed mechanism, not a contradiction. The proof correctly keeps these distinctions. No unrestricted interval resolution or new asymptotic example is accepted or suggested here.

This audit does not re-audit the earlier continuum relaxation mentioned in passing in Section 6, and no conclusion here relies on that earlier work. It also does not certify the author's checker implementation; its numerical output was reproduced by different code. No repository changes, publication, or queue edit were made as part of this audit.

## Public-edition notice

This complete substantive independent audit is reproduced as a historical report. Its references to checker programs, diagnostic outputs, manifests, or source documents identify separately retained evidence; those materials are not distributed here. The original report digest and this edition digest are distinct and recorded in INPUT_PINS.json and MANIFEST.json. Acceptance means internal independent AI review, not external human peer review, journal acceptance, or formal proof-assistant certification.
