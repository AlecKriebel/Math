# Independent audit: extremal modular forms modulo p

Audit date: 10 October 2026. Target: 30000160 / OWR-782-001, with duplicate 30000161 / OWR-782-002.

## Verdict and attribution

**Accept as a credited prior resolution of the intended, corrected conjecture.** Alper Ferudun's *Extremal Modular Forms Modulo p and a Conjecture of Bannai, Koike, Shinohara and Tagami*, dated 1 October 2026, Theorem 1.2 and Corollary 1.3, give the required smaller-weight extremal form and the maximal iteration. The proof is valid in its stated level-one setting. No repair to the central argument is required. This is an independent mathematical audit of an explicitly unrefereed, AI-assisted note, not a claim that the note has undergone journal peer review. The classical inputs remain credited to Swinnerton-Dyer and Serre, with the Hasse-invariant interpretation credited to Deligne; the conjecture remains credited to Bannai, Koike, Shinohara, and Tagami.

The source is [Ferudun, version 1.0](https://doi.org/10.5281/zenodo.23071924). The author expressly disclaims a proof of priority. This audit makes no new-result or first-proof claim. The reasoning below checks and explains the existing argument; it is not a new proof-search approach.

## 1. Exact question and source correction

In [OWR 1/2005](https://ems.press/content/serial-article-files/45975?nt=1), printed pp.13–14 (PDF pp.9–10), let f_k be the normalized level-one extremal form of weight k=12μ, with f_k=1+O(q^(μ+1)). The intended Case (2) requires:

- a_n is divisible by p whenever p does not divide n;
- at least one positive-index a_n is not divisible by p.

Thus the reduction is nonconstant and belongs to F_p[[q^p]]. Conjecture 4 asks first for a smaller-weight modular g with f_k(τ) congruent to g(pτ), then for a smaller-weight **extremal** g after a substitution p^rτ, r≥1.

The first divisibility sign in the printed Case (2) is wrong: it says p does not divide a_i. Replacing it by p divides a_i, while retaining p does not divide i, is necessary and is disclosed here. The literal printed case is impossible for positive μ because a_1=0, and is incompatible with the claimed three-case partition. Independently, the [2006 journal abstract](https://www.mathnet.ru/eng/mmj245) states the corrected divisibility condition. This audit accepts the intended statement, not the vacuous literal misprint.

The output g need not have weight divisible by 12. The original definition allows every even weight at least 4. This matters for iteration. The normalization a_0=1 is essential throughout. No assertion about existence of extremal lattices is used.

## 2. Integral forms and exact coefficient uniqueness

For even k≥0, let d_k=dim M_k. The usual formula is floor(k/12)+1 except in residue 2 modulo 12, where it is floor(k/12); in particular M_2=0. Odd weights vanish. Write k=12m+4a+6b with a∈{0,1,2}, b∈{0,1} and m≥0 when M_k is nonzero. The forms

    E4^(3(m-j)+a) E6^b Δ^j,  0≤j≤m,

have integral q-series and successive leading terms q^j. They form a basis, by the classical level-one structure theorem and the dimension count. Triangular elimination uses no division: it gives integral forms with initial coefficient vectors equal to the coordinate vectors through degree d_k−1. Consequently f_k is integral at **every** prime. A form with coefficients in Z_(p) is zero modulo p if its first d_k coefficients, including the constant term, are zero modulo p.

This verifies Ferudun Lemma 2.1 and avoids an unjustified use of a rational Eisenstein basis at a bad denominator. For p≥5 only, Δ=(E4^3−E6^2)/1728 is a polynomial over Z_(p). Thus every weight-k integral reduction has a homogeneous polynomial representative in E4,E6, and every F_p polynomial representative can be lifted coefficient by coefficient to an integral classical form.

The normalized E_(p−1) has coefficients in Z_(p) and reduces to 1: the von Staudt–Clausen denominator gives v_p(B_(p−1))=−1, while the normalizing numerator is a p-adic unit. No E_2, division by p, or assertion that every normalized E_k has globally integral coefficients is needed.

## 3. Classical filtration dependency, checked in the primary source

We independently retrieved [Serre, Bourbaki exposé 416](https://www.numdam.org/item/SB_1971-1972__14__319_0.pdf). The relevant scope is rational p-integral q-series of holomorphic level-one forms, p≥5, exactly the scope used here.

- Theorem 1, printed p.321, gives the kernel (A−1) of F_p[X,Y]→F_p[[q]], where A represents E_(p−1).
- Theorem 2, p.322, gives equality of weights modulo p−1 for equal nonzero reductions.
- Corollary 1 to Theorem 3, p.323, and Corollary 1 to Theorem 5, p.325, give squarefreeness of A.
- The filtration criterion is on p.326; the p-th-power argument is explicit in §2.2, p.329.

These statements and their prime/level hypotheses were read and visually checked. The audit does not need a general-level Katz lifting theorem. In particular it does not infer root existence solely from the weaker assertion that the theta kernel has filtration divisible by p.

Here is the algebraic dependency check. For a fixed weight, the triangular basis above makes the evaluation map injective. If F_1 and F_2 represent the same nonzero series in weights k_1≤k_2, the weight congruence gives t=(k_2−k_1)/(p−1)∈Z_≥0, and injectivity in weight k_2 gives F_2=A^tF_1. Thus a representative has minimal weight precisely when it is not divisible by A. If F is minimal, A cannot divide F^p: because A is squarefree, every irreducible factor of A dividing F^p would divide F, and their product would divide F. Therefore

    w(h^p)=p w(h).

This verifies Ferudun Lemma 2.3 without assuming that an arbitrary p-th root of a modular series is modular. The squarefreeness step is essential; simple comparison of q-expansions or weights alone would not establish the equality.

## 4. Small primes and the constant case

At p=2 and p=3 both E4 and E6 reduce to 1. In the integral triangular basis, f_k becomes a polynomial in Δ of degree below d_k. Its first d_k coefficients are 1,0,…,0, so triangularity forces this polynomial to be 1. This proves that Case (2) never occurs for these primes, without invoking the p≥5 polynomial presentation.

For p≥5, if p−1 divides k, E_(p−1)^(k/(p−1)) is a weight-k p-integral form reducing to 1. Coefficient uniqueness then gives f_k≡1. Conversely, a nonzero reduction equal to 1 occurs in both weights k and 0, so the classical weight congruence gives p−1 dividing k. Ferudun Lemma 3.1 therefore holds for all primes. In the target k=12μ, this excludes 2,3,5,7,13 from Case (2).

The zero-weight case, if allowed by μ=0, is vacuous because the normalized form is constant. Weight 2 does not occur. These are not omitted counterexamples.

## 5. Actual modular root and its weight

Let p be in Case (2). We have p≥5 and k≥4. The classical normalized Hecke operator preserves M_k and has Fourier coefficients

    a_n(T_p f_k)=a_(pn)(f_k)+p^(k−1)a_(n/p)(f_k),

with the second coefficient zero when p does not divide n. This includes n=0: its value is 1+p^(k−1), hence 1 modulo p. The q-series formula also proves that integral coefficients remain integral. The full-space, noncuspidal operator and its formula can also be checked in [Snowden's level-one lecture, Hecke-operator section](https://public.websites.umich.edu/~asnowden/teaching/2013/679/L13.html).

Thus G=overline(T_p f_k) is an actual element of the reduction of M_k, with coefficients a_(pn) modulo p. The support hypothesis gives

    overline(f_k)=G(q^p)=G^p.

The equality uses coefficients in F_p. G is nonconstant, since substitution q↦q^p is injective and the original reduction is nonconstant. Set k′=w(G). Since M_0 consists of constants, M_2=0, and odd-weight spaces vanish, k′ is even and at least 4. Filtration multiplication gives

    w(overline(f_k))=p k′≤k.

Also G occurs in weights k and k′, so k′≡k modulo p−1. In particular k′≤k/p<k. This proves the root, its rational/integral lift, its smaller weight, and the claimed exact formula for k′. It does not assert that f_k as a characteristic-zero form is a p-th power.

## 6. Extremality, including the exceptional residue class

Let d=d_k and L=floor((d−1)/p)+1. If 1≤n<L, then pn≤d−1 and the **integer** coefficient a_(pn)(f_k) is zero. Therefore G=1+O(q^L) modulo p. To identify G with an extremal form of weight k′, one needs d_(k′)≤L; divisibility of the filtration alone would not suffice.

When k is not 2 modulo 12,

    d_(k′)−1 ≤ floor(k′/12) ≤ floor(k/(12p))
               = floor(floor(k/12)/p)=L−1.

For k=12M+2, d−1=M−1. The same inequality works unless p divides M. In that remaining case put t=M/p, so L=t. If d_(k′)>L, the dimension formula and k′≤(12M+2)/p force floor(k′/12)=t and k′ not congruent to 2 modulo 12. The interval

    12t≤k′≤12t+2/p<12t+1

contains only the integer k′=12t. But then k=pk′+2, whereas k′≡k modulo p−1 forces p−1 to divide 2. This contradicts p≥5. Hence d_(k′)≤L in every case.

Lift a homogeneous representative of G in weight k′ to Z[X,Y] and evaluate at E4,E6. The resulting integral weight-k′ form has the same first d_(k′) coefficients modulo p as f_(k′). Coefficient uniqueness gives G=overline(f_(k′)). Consequently

    f_k(τ) ≡ f_(k′)(pτ) modulo p.

This verifies every step of Theorem 1.2. No off-by-one gap occurs: the known vanishing ends at d−1, the root vanishing ends at L−1, and precisely d_(k′) initial coefficients are required.

## 7. Iteration, nonconstancy, maximal exponent, and uniqueness

Apply the theorem whenever the next extremal reduction is in Case (2). The positive even weights satisfy 4≤k_(i+1)≤k_i/p, so the sequence terminates, with R≥1 for the starting case. Nonconstancy is preserved by the injective substitutions. The terminal reduction is neither Case (1) nor Case (2), so it is in Case (3).

The identities compose to f_k(q)≡f_(k_i)(q^(p^i)) for 0≤i≤R. Since the terminal form has a nonzero coefficient at an exponent not divisible by p, the original series belongs to F_p[[q^(p^R)]] but not F_p[[q^(p^(R+1))]]. Therefore no formal series h with p-integral coefficients can satisfy f_k(q)≡h(q^(p^r)) for r>R. For r≤R, injectivity of substitution forces h modulo p to equal f_(k_r) modulo p.

Only the reduction is unique; the characteristic-zero form and its weight need not be. This distinction is correctly made in the note. Equivalently, R is the minimum p-adic valuation of an exponent with nonzero positive coefficient in the original reduction. The proof establishes r=1, every intermediate allowed exponent, and the maximal exponent, all with smaller-weight extremal forms. It covers both parts of Conjecture 4 and the duplicate's stronger wording.

## 8. Ancillary assertions and source errors

The finite criterion in Ferudun Lemma 3.2 / Corollary 1.4 is also sound. For an admissible k′, the exponent m=(k−pk′)/(p−1) is a nonnegative integer. The weight-k form f_(k′)^p E_(p−1)^m has initial expansion 1+O(q^(pL)), and pL≥d_k. Coefficient uniqueness proves the congruence. Conversely the audited root qualifies, and any qualifying weight is at least w(G). This supplies a genuine finite test. The bounds p≤k/4 and, for k=12μ, 11≤p≤3μ with p≠13 follow immediately.

There is a **second error in the original OWR abstract**, already identified by Ferudun: its printed Theorem 3 lacks the exclusion p−1 not dividing k. For example k=12,p=13 satisfies p≥13 and p divides 2k+2=26, but f_12≡1 modulo 13, so the asserted Case (2) conclusion is false as printed. This counterexample does not affect Conjecture 4 or Ferudun's proof. The audit does not claim that adding the missing exclusion has been proved to repair that entire auxiliary theorem.

The OWR Theorem 2 remains a historical partial result. It is not promoted to a full proof. Koike's [2009 paper](https://doi.org/10.2206/kyushujm.63.123), pp.123–132, was read for scope: Theorems 1.2–1.3 concern congruences modulo powers of 2 and 3 with special theta series, while subsequent results concern integrality of roots. These are different assertions, and do not by themselves resolve the nonconstant mod-p Case (2) question. The audit does not independently reprove those unrelated higher-power results.

## 9. Inspection limits

The acceptance is based on the complete argument above and the checked classical dependencies. We did not inspect the full 2006 journal article, verify a global literature-priority assertion, or read Katz's and Swinnerton-Dyer's separate papers in full. None is needed for the claimed applicability once the primary Serre statements have been checked.

## 10. Accepted scope and exclusions

Accepted: the corrected level-one conjecture, every prime, all even weights needed by the root chain, integral extremal g, strict smaller weight, exact filtration formula, and maximal iteration. No theorem is asserted for arbitrary level, arbitrary coefficient field, a non-extremal starting form, or characteristic-zero equality. This work consumed zero new proof-search turns and makes no novelty claim.
