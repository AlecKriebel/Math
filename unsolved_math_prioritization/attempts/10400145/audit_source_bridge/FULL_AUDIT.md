# Independent full mathematical audit: Ohtsuki Conjecture 7.30

Problem 10400145 / AMR-103-0145; queue rank 1010. Audit completed 2026-10-08 UTC.

## Decision

**ACCEPT the negative resolution of the literal printed conjecture.** The final author argument is a complete contradiction for the stated coefficient ring and normalization, using established, explicitly cited quantum-topological inputs. No mathematical correction is required. The oriented Poincare sphere given by minus-one surgery on the left-handed trefoil supplies the counterexample.

Acceptance is an independent mathematical/source audit, not a proof-assistant certificate or a claim of human peer review. It does not establish originality. I reviewed the complete proof, the stated scope, the topology-to-algebra bridge, and the final replay package independently. I did not consult the other independent audit.

Accepted author snapshot:

- AUTHOR_MANIFEST.json SHA-256: abc975e091ff72d9b020f238ef4ff7884a4ce9c0ed755b34f45626c1ef74158c
- bootstrap.py SHA-256: 301e0c33f5eafccb1701687ae9cfbd574496b0ef1fd357bb4c4efe728c2379fa
- Nine manifest-listed author files, with complete bytes and SHA-256 values pinned by that manifest

These hashes identify the reviewed objects only when obtained through an independently trusted record. A colocated mutable hash file is not a self-authenticating trust root.

## 1. Exact target and hypotheses

Direct visual inspection of the publisher's Ohtsuki PDF, printed pages 490-492 (PDF pages 118-120), establishes the following facts. The rank interpolation ring is the inverse limit of R[t]/E_m(t), where E_m(t) is the product of t-q^j for 1 <= j <= m, and R is the cyclotomic completion of Z[q,q^-1] with the product of q^j-1 as defining ideals. The requested specialization is at t=q^n for every n >= 1, with the n=1 invariant expressly assigned value 1. The symbols sl_n refer to the matrix-size index n, not Lie rank n-1. There is no printed factor dividing the Newton kernels, no localization at q-1, and no change of quantum parameter depending on n.

The premise concerning fixed-Lie-algebra unification is not left hypothetical in the audit. Ohtsuki includes a proof update, and the later published Habiro-Le Theorem 1.1 gives the corresponding invariant in the Habiro ring. The statement's uniqueness convention identifies this invariant with the specialization target.

The polynomial and Laurent-polynomial versions of the coefficient completion agree. Let f_m(q)=product(1-q^j). Since f_m(0)=1, there is an integral polynomial g_m such that f_m(q)=1+q g_m(q). Modulo f_m, q has inverse -g_m. Thus localizing at q does not alter any finite quotient, compatibly with its transition maps. Reversing all factor signs does not alter their ideals. This justifies comparison with Habiro-Le's polynomial-ring convention without assuming that a completion commutes with an arbitrary localization.

## 2. Independent reconstruction of the algebraic contradiction

Put D=Z[x]/(x^2). The assignment q -> 1+x, q^-1 -> 1-x is a homomorphism from Z[q,q^-1] to D. The second cyclotomic product (q-1)(q^2-1) maps to zero. Composing the projection from R onto that second quotient with this homomorphism defines a first-jet map T:R -> D.

This is exactly the reduction modulo x^2 of the usual Taylor homomorphism at q=1: both maps are induced by the same polynomial substitution and agree at this finite level. Only the existence of this homomorphism is used, not its injectivity. In particular, no cancellation by q-1 and no assumption that q-1 is regular is needed. Inverting q-1 would make this map impossible, since its image x is nilpotent in a nonzero ring.

Suppose F is in the proposed rank completion. Its third coordinate is a class in R[t]/E_3. Monic polynomial division, valid over any commutative coefficient ring, supplies a representative P of degree at most two. For each n in {1,2,3}, E_3(q^n)=0 exactly. Consequently P(q^n) is independent of representative. For all later coordinates, compatibility gives the same value, because E_m(q^n)=0. Evaluation therefore stabilizes algebraically, rather than requiring analytic convergence or interchange of limits.

For a separate derivation of the crucial relation, use F(q)=1. Then P(q)=1, so polynomial division by t-q gives P(t)=1+(t-q)B(t) with B in R[t]. Let b be the constant coefficient of T(B(1)) in D. In D, q^n-q=(n-1)x. Moreover T(B(q^n)) has constant term b, independent of n. It follows that

T(F(q^n)) = 1 + (n-1)b x, for n=1,2,3.

Thus the first coefficients must be 0,b,2b. Equivalently v_3-2v_2+v_1=0. This independently verifies the author's expansion P=a+bt+ct^2 and its six coefficient variables.

There is no hidden infinite differentiation: only the second quotient in q, the third quotient in t, and finite polynomial operations occur. Nor does the argument presume that tensor products commute with inverse limits. It never forms such a tensor product.

As a boundary check, dropping the n=1 condition alone does not repair the printed ring. Applying the same first-jet calculation to a representative in the fourth quotient forces an affine first coefficient at n=2,3,4 as well.

## 3. Source bridge and normalization audit

The mathematical dependence on published topology is essential and explicitly retained. The finite checker does not prove these inputs.

### 3.1 Unified invariant versus the projective invariant

I directly inspected the published Habiro-Le PDF at printed pages 2690, 2691, 2693 and 2726 (PDF pages 4, 5, 7 and 40), as well as the corresponding arXiv v2 pages. Theorem 1.1 gives the unique unified invariant. Proposition 1.2 identifies its root-of-unity evaluations with the projective invariant for integral homology spheres. The comparison is specific to integral homology spheres; the extra factor possible for general manifolds is explicitly 1 in this case.

Published Proposition 1.9 identifies its Taylor expansion with the Ohtsuki series. The preceding paragraph characterizes that series through prime congruences and cites Le's perturbative papers. The bibliography's Le3 entry in the inspected manuscript is the published PSU(n) paper used by the author. These facts remove a possible SU(n)/PSU(n) normalization gap.

### 3.2 Quantum variable and root lengths

Le's published PSU(n) paper, page 815, uses the type-A Cartan inner product, so every root has squared length 2, and explicitly fixes q=1+x. Pages 818-820 define the projective theory by root-lattice summation and specify the perturbative expansion. The shifted weight notation denotes a highest weight after subtraction of rho; it is not a different rank or a different quantum parameter.

Habiro-Le's published section 3A1 fixes short-root squared length 2; section 3A2 sets v=exp(h/2) and q=v^2. All type-A roots are short, so the parameter is uniform in n. The corresponding manuscript locator is section 3.1.2, page 36. Thus h=log q and q-1 have the same linear coefficient. A common square/inverse convention change would rescale all first coefficients by the same nonzero scalar; the nonzero second difference would persist. An n-dependent change would alter the problem and is not supplied by these sources.

### 3.3 First perturbative coefficient

Direct visual inspection of Le's published page 821, immediately after Conjecture 1.9, confirms

c_1^(n)(M) = |H_1(M;Z)|^(-n(n-1)/2) n(n^2-1) lambda_C(M),

where the Casson-Walker convention is the Lescop one. The coefficient formula is a stated result in the prose following the integrality conjecture, not part of that conjecture. This audit relies on that published result; it does not present a new proof of the surgery-theoretic formula.

For integral homology spheres, the order of H_1 is 1, even though the group is trivial. The power of its order is consequently 1. The Legendre-symbol normalization used in defining the rational-homology series is also 1 here. Therefore c_1^(n)=n(n^2-1)lambda_C applies to the exact specialization target.

One can further check the first-jet identification without an analytic interpretation of the Ohtsuki series. At every sufficiently large odd prime p, evaluate the unified invariant at a primitive p-th root. A representative from a cyclotomic quotient of index at least p has the same first jet. In F_p[x]/x^2, the relation Phi_p(1+x)=0 holds, since its constant and linear terms are p and p(p-1)/2. Thus the first jet reduces to the prime-congruence coefficients used by Le. Le's uniqueness lemma implies equality of the rational coefficients, since a nonzero rational difference cannot vanish modulo all sufficiently large primes. This is consistent with, and not a replacement for, Proposition 1.9.

## 4. Counterexample, orientation and all tail terms

Ohtsuki printed page 492 and Le's published Quantum Invariants paper page 133 both specify the Poincare sphere by minus-one surgery on the left-handed trefoil. They give the series with k-th term

q^k (1-q^(k+1))...(1-q^(2k+1))/(1-q).

Habiro's inspected unified-invariant preprint, section 16.1, equation (16.1), page 61, gives the same expression as an element of the Habiro ring. This also avoids relying on a purely root-of-unity formula to define a Taylor series.

There is no illicit division by a nonunit in this calculation. Cancel the factor 1-q from 1-q^(k+1) within the polynomial identity, obtaining the integral geometric sum 1+q+...+q^k. The remaining k factors are each divisible by x=q-1. Every term with k>=2 is therefore in x^2 Z[q]. This is a proof for every tail term, not an inference from the eight examples tested by the author's program. The resulting series is x-adically convergent for this coefficient calculation.

The k=0 term is 1. The k=1 term becomes q(1+q)(1-q^3), with first coefficient -6. At n=2 the published coefficient formula is 6 lambda_C, hence lambda_C(P)=-1 in exactly this orientation and convention. At n=3 it is 24 lambda_C=-24. The assigned rank-one value contributes coefficient 0. The second difference is

-24 - 2(-6) + 0 = -12,

contradicting the necessary value zero. For an arbitrary integral homology sphere, the same comparison gives 12 lambda_C=0. Thus every sphere with nonzero lambda_C is excluded. For n=2,3,4 the second difference is 18 lambda_C, confirming the author's supplementary observation about omitting rank one.

Reversing orientation would change both nonzero coefficients' signs and preserve the obstruction; the actual orientation has nevertheless been fixed rather than silently absorbed into a sign convention.

## 5. Provenance, literature status and corrected detail

All nine retained PDFs' SHA-256 hashes and byte counts were recomputed independently and matched the final source metadata. SOURCE_INSPECTION.json distinguishes direct visual inspection of the central pages, supporting text inspection and record-only checks. No PDF, source extraction or source image is included in this audit packet.

One nonmathematical correction was requested: the arXiv record for Habiro-Le comments that the manuscript has 125 pages, while the actual retained v2 PDF contains 123 physical pages. The author preserved the earlier frozen bytes, supplied BIBLIOGRAPHIC_CORRECTION.patch, and produced the accepted corrected snapshot. The patch changes that one sentence; it does not change the proof. The published PDF now provides the controlling locators as well. A second metadata-only patch updates the inspection timestamp to include the later publisher-PDF inspection; the accepted final snapshot includes both corrections. Earlier snapshots remain preserved. Neither patch changes the mathematical argument.

A suspected title mismatch for Beliakova-Gorsky was resolved without a change: its arXiv record uses “knot invariants”, while the separately retained repository PDF uses “link invariants”. The reference and metadata identify their respective sources. Its fixed-N result and HOMFLY interpolation stability do not furnish the literal R-valued rank completion in this conjecture.

A bounded independent web search on 2026-10-08 for the exact conjecture number, Habiro, Casson, counterexample and erratum did not locate an erratum or an earlier literal disproof. Ohtsuki's arXiv record lists one version. These negative searches do not prove absence of prior knowledge.

The same search found Fang-Zhou, arXiv:2608.29585v1 (2026-08-30). Its abstract, introduction, rank-coefficient-ring definition and conclusion concern symmetric-color knot/HOMFLY invariants and an integer-valued coefficient ring inside Q(q)[A^(+/-1)]. They do not assert the printed three-manifold S-valued statement. I did not audit that preprint's proofs or infer that its claims are established. It is a useful scope comparison, not an input to this counterexample or evidence of priority.

A separate attempted re-download did not complete; no independent byte-for-byte fresh-download claim is made. Hash checks concern the retained files; direct public web records and accessible public PDF views were also inspected. This limitation does not affect the mathematical page inspection.

## 6. Exact replay and adversarial controls

The author bootstrap and manifest were checked against the independent pins before execution. The complete final payload remained byte-for-byte unchanged throughout this audit. The bootstrap validates file inventory, types, sizes and hashes before invoking the author checker. I also read the author checker and its explicit scope limits.

REPLAY_RECEIPT.json records:

- Identical successful author bootstrap output under isolated normal Python, -O and -OO
- Identical independent-algebra output under those three modes
- Three successful author runs and three successful independent-algebra runs against a whole-filesystem read-only bind mount, as uid 1000, plus a separate attempted-write probe that failed as required
- 45 direct-checker rejections covering twelve altered semantic certificates and three malformed JSON cases, each in all three optimization modes
- 24 bootstrap rejections covering stale proof bytes, changed source metadata, altered checker, missing/extra payload, a nested directory, a symlink and a malformed manifest, each in all three modes
- Three positive hostile-environment controls: shadow modules and hostile PYTHONPATH did not affect the isolated runs

The total control count is 72. Direct semantic tests intentionally bypass the manifest in disposable copies, so their failures genuinely exercise the checker rather than stopping only at stale hashes. Original author files were never changed by the audit.

The independent algebra program uses a separate ordered-pair implementation of dual numbers. It checks all six Z-basis vectors of D[t] of degree at most two. Since evaluation and second difference are linear, this is an exact universal identity check rather than random coefficient sampling. It also checks the q inverse, annihilation of the second cyclotomic product, failure at the first quotient, the Poincare linear term, the actual nonzero residual, a compatible affine control and the rank-2/3/4 obstruction.

These checks do not mechanically certify the prose, references or topological inputs; that work is the mathematical audit above. Cryptographic integrity also assumes independently trusted initial pins and no concurrent replacement of checked files. No stronger security claim is made.

## 7. Acceptance boundary

The literal statement is disproved for its full universal quantifier by one correctly normalized integral homology sphere. One mathematical approach suffices; source retrieval, normalization checking and replay controls are not additional mathematical approaches.

No acceptance is given to rank-renormalized variants, coefficient rings with poles at q=1, divided Newton completions, or any intended but unprinted correction. Nor is this a refutation of the proved fixed-Lie-algebra invariant. No novelty claim is warranted by the bounded searches. The final packet accurately limits itself on all these points.

## Public references

- Ohtsuki problem collection, publisher PDF: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- Le's published PSU(n) paper, author-hosted PDF: https://people.math.gatech.edu/~letu/Papers/PERT_NEW01.pdf ; DOI https://doi.org/10.1016/S0040-9383(99)00037-3
- Habiro-Le published article: https://msp.org/gt/2016/20-5/gt-v20-n5-p04-s.pdf ; DOI https://doi.org/10.2140/gt.2016.20.2687 ; manuscript record https://arxiv.org/abs/1503.03549
- Le's Quantum Invariants article: https://people.math.gatech.edu/~letu/Papers/QUANTUM.pdf
- Habiro's unified-invariant preprint: https://arxiv.org/pdf/math/0605314v1
- Beliakova-Gorsky record: https://arxiv.org/abs/2101.08243
- Fang-Zhou scope comparison: https://arxiv.org/abs/2608.29585 ; https://arxiv.org/html/2608.29585v1
