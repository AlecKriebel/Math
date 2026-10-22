# Independent adversarial audit: Settled quadratic polynomials

Problem 30000492 / OWR-1274-008, rank 656. Audit date: 2026-10-04 UTC.

## Verdict

PASS as an honestly unresolved, five-approach research packet with correct stated partial results and reproducible finite evidence. No required mathematical correction to the frozen author packet was found. The general odd-characteristic problem is not solved by this work. The characteristic-two counterexample must remain a separately labeled scope correction; it must not be used to mark the intended problem solved. The Markov obstruction is prior published work, and no novelty or human peer review is certified.

This audit is independent of the packet's authoring process and concerns only the exact frozen archive bound in BINDING.json. It does not convert an unsuccessful general proof attempt into a solution. The audit was conducted by an AI reviewer, not a human referee, and includes neither a proof-assistant formalization nor a universal literature-priority search.

## 1. Frozen-object and replay checks

The author archive has SHA-256 25f0cd6997fc0d2774588030e98f902d2b16b8817eaf44b6f3c815826a7c7783, length 23,273 bytes, and 13 regular members. Its MANIFEST.json has SHA-256 e7cc4c304695dde9df2c6cf800e605d1811c4c6b10082baece7302a902fcc270. All eleven manifest payload hashes and lengths match. The two excluded manifest/checksum files are themselves covered by the archive binding, and the complete per-member audit binding includes all thirteen members.

The reviewer extracted a separate copy, inspected the proof and verification code before running it, and left the original archive and original author directory untouched. Under Python 3.12.14 and SymPy 1.14.0:

- verify.py produced byte-identical EXACT_RESULTS.json.
- test_controls.py produced byte-identical CONTROL_RESULTS.json: 162 controls, including 150 low-degree irreducibility comparisons.
- A separate program recomputed all 39 reported odd-field mass rows by factoring entire iterates at every depth. It did not import the author verifier and did not prune stable branches. Every mass row matched.
- A second, pure-Python program independently checked all 52 saved stable certificates. It verified irreducibility, membership in the stated full iterate, and nonsquare values at every postcritical-orbit point. It also verified all five polynomials in the Markov witness path and rejected four negative controls.
- The root-degree formula passed 4,064 multiplicative-order cases across 58 odd prime powers, with depths 1 through 16 and all possible nonsquare element orders for each tested field size.
- Every monic irreducible polynomial of degrees 2, 4, 6 and 8 over F2 was tested: all 43 fail stability for x^2+x+1 by their first or second composition.

The unpruned mass calculation still uses SymPy to propose and test factorizations, as the author does. That is a shared software dependency, not an independent factorization implementation. The separate certificate checker imports neither SymPy nor the author code and uses descending-coefficient polynomial arithmetic with a Rabin test. Its algebraic criterion is the same standard theorem as the author's test; implementation independence does not remove dependence on that theorem. Finite testing is supporting evidence, not an all-depth proof.

## 2. Target, normalization and source scope

Printed page 1490 of the original Oberwolfach contribution was independently read and visually checked. It supplies the degree-weighted settledness question and the Markov-model motivation. Its displayed conjecture does not explicitly exclude p=2, while its critical-point formula requires division by 2. The later primary papers inspected here explicitly use odd characteristic. The packet's separation between the literal characteristic-two obstruction and the intended odd-characteristic target is therefore appropriate. [Original report](https://ems.press/journals/owr/articles/1274).

The scalar conjugacy fixing zero was checked directly. For f(x)=Ax^2+Bx+C, A nonzero, L(x)=Ax gives F(x)=x^2+Bx+AC. Iterates obey F^[n](Ax)=A f^[n](x). For monic h of degree d, H(x)=A^d h(x/A) is monic and H(F^[k](x))=A^d h(f^[k](x/A)). Invertible changes of variable and nonzero scalar multiples preserve irreducibility, factor degrees and multiplicities. Thus the normalization does preserve the target-zero factor tree and stability. Arbitrary translation generally does not preserve that target, so the packet correctly refuses to reduce every quadratic to its fixed-critical-point family.

Types must be applied to monic factor representatives. Otherwise nonsquare scalar multiplication flips all type digits. The packet both enforces monicity computationally and states it in the theorems. The published source's Remark 1.5 explicitly records this issue and its relation to the Boston--Jones erratum. [Goksel 2026](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.1358/).

## 3. Proposition 1: finite stability certificate

The proof is valid under the stated odd-q, monic-f, irreducible-f and monic-even-degree-h hypotheses.

Squarefreeness: a repeated root of an iterate forces some forward image of that root to be the critical point gamma. A subsequent critical iterate is then zero. Its predecessor lies in the base field and is a root of f, contradicting irreducibility. This also excludes zero from the postcritical orbit.

Degree powers: for f(beta)=alpha, the field generated by beta contains the field generated by alpha, and the relative degree is 1 or 2. Above an irreducible h, Frobenius makes this behavior uniform across its roots. Consequently h(f) either has one degree-2d factor or two degree-d factors. The separability argument excludes collisions. Starting from degree 2 prevents odd-degree factors.

Norm step: if P=h composed with f^[k-1] is irreducible of even degree D, and beta is its root, then P(f) is irreducible precisely when beta-delta is nonsquare in F_(q^D). For nonzero z, the quadratic character of its norm equals its extension-field quadratic character. The norm of beta-delta is (-1)^D P(delta), and D even removes the sign. Since delta=f(gamma), this is h(f^[k](gamma)). Induction over k proves the equivalence, including necessity. A zero evaluation is correctly rejected as nonsquare and would also force reducibility.

Attack outcome: no omitted sign, wrong composition index, or unsupported irreducibility induction was found. The conclusion certifies individual stable factors only; no rate of creating such factors follows.

## 4. Theorem 2: exact fixed-critical-point threshold

The all-depth proof is valid for odd prime powers, not just primes. The assumption -a nonsquare implies a is nonzero and makes f irreducible. Writing b=-a gives f^[n](x)=(x-a)^(2^n)+a.

The potentially fragile step is the common root order. Let e=ord(b), let s=v2(q-1), and let y^(2^n)=b. Since a nonsquare in the cyclic group Fq* has order with full 2-part, v2(e)=s, which is at least 1. If M=ord(y), then ord(y^(2^n))=M/gcd(M,2^n)=e. The odd part of M therefore equals the odd part of e. If t=v2(M), the equation gives t-min(t,n)=s>0. Hence t=n+s, so M=2^n e. This works for every root and is not merely an existence assertion for one selected root.

A root of multiplicative order M has degree ord_M(q). The odd part of e divides q-1 and therefore imposes no extra extension degree. The problem is exactly ord_(2^(s+n))(q). For q congruent to 1 modulo 4, v2(q^d-1)=s+v2(d), and the degree is 2^n. For q congruent to 3 modulo 4, an admissible exponent d must be even, and v2(q^d-1)=v2(q+1)+v2(d). This yields degree 2^max(1,n-r+1), with r=v2(q+1).

The conversion from degree formulas to stability is also valid. Every irreducible divisor of h composed with f^[k] divides f^[n+k] and thus has the same common degree d_(n+k). When n is at or above the stated threshold, that degree equals the entire degree 2^k d_n of the composition; multiple factors are impossible. Before the threshold, the very next level still has degree d_n, so the composition splits. Therefore S_n is exactly zero before r and one from r onward when q is 3 modulo 4; for q 1 modulo 4, all positive levels have mass one.

Attack outcome: the threshold is r, not r-1. The field size q, rather than its characteristic p, controls the congruence and valuation. The packet uses both correctly. The theorem is an explicit special family, with no reduction to general critical dynamics and no novelty certification.

## 5. The three-step Markov witness

The source's strict orbit convention and old one-step permissions were checked against the 2015 paper, including its tail-size definition and Lemma 2.9. For f=x^2+1 over F7 the strict orbit is (1,2,5), its tail size is 2, and the critical-point orbit type in the 2026 paper is (3,1). These are compatible conventions, not conflicting orbit lengths. [Goksel--Xia--Boston 2015](https://doi.org/10.1080/10586458.2014.992079).

Direct recomputation confirms that g=x^2+4x+5 is an irreducible factor of f^[4]. Its compositions at relative depths zero, one and two are irreducible, with types nns, nss and sss. At relative depth three it has two irreducible degree-eight factors, both nnn. Their complete ascending coefficient lists are recorded in INDEPENDENT_RESULTS.json and independently tested by the pure-Python checker against the author witness.

At the sss split, the product type is sss, so child types are identical. The old tail constraint forces the second and third digits to agree. Thus the permissible identical pairs are precisely nnn/nnn, nss/nss, snn/snn and sss/sss. Using tail index one would produce a different, incorrect set.

Published Theorem 1.7 and Corollary 4.3 impose an additional history-dependent equality of the first two child digits after nns -> nss -> sss. This removes exactly nss/nss and snn/snn from the old support. The theorem, monic/even-degree hypotheses, and auxiliary proof steps on pp.169-177 were inspected. In particular, the proof's square-root expressions are shown to lie in the base field through Frobenius-invariant paired root sets; a square only in an extension would not suffice. [Goksel 2026](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.1358/).

Attack outcome: the packet uses the corrected tail index and the published theorem numbering. One observed allowed transition alone is not a statistical refutation; the theorem supplies the all-degree missing support. This does not refute settledness or prove every possible refined Markov law.

## 6. Stable mass and conditional absorption

Proposition 3 is correct. A stable h at depth n contributes h composed with f at depth n+1, twice the degree and the same normalized mass. Distinct factors remain coprime after composition by composing a Bezout identity. Existing stable mass therefore persists without double counting. Since total normalized degree is one, the nondecreasing sequence has a limit.

Proposition 4 is also correct as a conditional statement. A descendant of h has degree at least deg(h), because its root generates a field containing a root of h. A stable descendant reached at depth k<=L contributes at least 2^(-k), and hence at least 2^(-L), of h's original mass. Its stable mass persists through the remaining L-k levels. Summing over disjoint unstable branches yields exactly the claimed residual-mass contraction.

The indispensable unproved hypothesis is one uniform L for every unstable factor at every level. A merely possible path in a type graph does not prove a realized descendant. Nor does eventual access from each individual factor yield a uniform depth or measure-one absorption. Dense access and full measure are different properties.

Independent full-iterate calculations give the terminal masses 85/128 at F7 depth 9, 11/32 at F5 depth 8, 13/16 at F3 depth 8, 1/8 at F11 depth 7 and 3/16 at F13 depth 7. All intermediate rows match. These are rigorous lower bounds for the limit, with no certified residual error and no positive lower bound on the limiting complement.

The 2026 Ejder--Kocak manuscript concerns dense settledness of certain arithmetic iterated monodromy groups. Its version, main theorem and specialization corollary were checked. Density does not force a specified Frobenius element to be settled: the identity has no growing stable cycles even in an ambient group with a dense settled subset. Thus this source does not supply the missing pointwise finite-field assertion. Refereed publication was not established. [Manuscript v2](https://arxiv.org/abs/2604.04524v2).

## 7. Characteristic-two scope counterexample

Proposition 5 is correct and proves more than the failure of f itself to be stable. Every root alpha of a factor of f^[n] maps to a root of the irreducible quadratic f. Consequently F2(alpha) contains F4 and the factor degree d is even.

For any such monic irreducible h, if h(f) already splits, stability fails. Otherwise P=h(f) is irreducible of degree 2d. Only the leading term f^d contributes to its coefficient of x^(2d-1), giving d=0 in F2. The trace of a root beta of P is therefore zero. The trace of 1 is also zero because the field degree 2d is even. The Artin--Schreier equation z^2+z=beta+1 is soluble in the same field, so f(z)=beta does not create a quadratic extension. The composition P(f) is reducible. This rules out stability of every factor, and establishes S_n=0 at all depths.

The trace-zero solvability claim follows from the additive map z -> z^2+z having kernel {0,1}; its image is the trace-zero subspace by equal cardinality. The trace functional is nonzero for a finite separable field extension, or directly because its defining polynomial has degree below the field size and is not the zero polynomial.

The prior Ahmadi paper was read through its complete finite-field trace proof. Its non-stability result for the quadratic itself is relevant prior work, but the every-factor step is needed for settledness and is explicitly supplied by the packet. [Ahmadi](https://arxiv.org/abs/0910.4556v1). No priority claim for that specialization is validated here.

## 8. Sources, limitations and disposition

All six PDF objects listed by the author were freshly downloaded during the audit; every byte count and SHA-256 matched. Only public retrieval/inspection metadata is included here. No source PDFs, extracted source text, catalogue corpus, private coordination files or credentials are redistributed.

The original 2012 Boston--Jones article and 2020 erratum were not fully inspected. A fresh attempt to open the search-indexed 2012 copy failed with HTTP 403. The packet's disclosure is accurate; its stability criterion is independently proved, and the type-normalization warning is confirmed in the inspected published follow-up. The original report, 2015 model definition, published 2026 restrictions and the relevant recent manuscript were sufficient for the claims actually made.

A limited current-literature check found no verified general resolution that changes the audit disposition. A secondary search result's apparent relation to arXiv:2510.19417 was checked against the primary abstract; that paper concerns escape of mass for Laurent series, not this factorization limit. arXiv:2608.14524 concerns fixed-point proportions and does not, at abstract level, assert the target theorem. Neither was used as evidence of a general solution. These limited checks cannot prove universal absence of other results.

Recommended final status: unsolved, five distinct approach families completed, with audited partial results. No mandatory patch or refreeze is needed. Preserve the original archive hash, keep this audit bound separately, and retain all scope, novelty and finite-versus-asymptotic caveats.
