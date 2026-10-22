# Independent audit: the imbalanced restricted-sumset rectangle question

Date: 2026-10-10 UTC. Target: AIM-COMBINATORICS-0229 / 20001104, original AIM Problem 2.4.

## Verdict

**PASS — VERIFIED PRIOR NEGATIVE, for the precise ratio-free large-rectangle assertion.**

The integer construction and analytic argument are complete. The underlying cube/basis obstruction is previously recorded by Green and Kane, with explicit attribution to Hosseini, Impagliazzo and Lovett. No novelty or priority claim is justified. No mathematical correction to the audited proof is required.

The distributed [proof](PROOF.md) has 6,240 bytes and SHA-256 `533679fdd1cc500e6a87ff1a8505cf338e3d9810a298dbf8600138a96c14c90e`. This audit binds to that exact public edition. The proof and mathematical scope were read in full; no mathematical correction was required. This AI-assisted, unrefereed audit is not external human peer review, journal acceptance or formal proof-assistant certification.

## 1. Exact source scope

[AIM's workshop problem list](https://aimath.org/WWN/additivecomb/additivecomb.pdf), Problem 2.4, printed/PDF page 6, asks about finite integer sets of cardinalities m>n, a graph of density at least δ, and a restricted sumset of size strictly less than Cm. The concrete conclusion asks for fractions c of both sets and a full sumset of size at most Km, with c,K depending only on δ,C.

The source first asks broadly what structure follows. Its subsequent concrete assertion is refuted; the proof does not show that no useful structural conclusion is possible. This distinction is explicitly preserved in the proof.

[Croot and Lev's expanded list](https://math.haifa.ac.il/seva/Papers/Montpr.pdf), §4.9, printed/PDF page 17 of the inspected author-hosted version, repeats the rectangle question and separates the bounded-imbalance case. It exchanges the letters used for the input/output size constants and permits m=n. These notational differences do not change the target for m>n.

The exact negation to prove is therefore:

For some fixed δ,C>0, for every c,K>0, there exist finite A,B⊂Z with |A|=m>|B|=n and a graph G⊂A×B, with |G|≥δmn and |A+_G B|<Cm, such that every A′⊆A and B′⊆B satisfying |A′|≥cm and |B′|≥cn has |A′+B′|>Km.

The proof establishes this statement with δ=1/2 and C=1. Refuting this one fixed pair is sufficient to refute a uniform theorem for all permissible δ,C.

## 2. Construction and integer embedding

For d≥2 the construction is

A={Σ ε_i3^i : ε∈{0,1}^d}, B={−3^i : 0≤i<d},

with (a(ε),−3^i) an edge precisely when ε_i=1.

All A elements are distinct by ordinary ternary uniqueness; all B elements are distinct because the powers are distinct. Thus m=2^d, n=d and m>n. Negative elements of B are allowed by the original integer-set hypothesis.

For each i, exactly 2^(d−1) cube points have ε_i=1, so |G|=d2^(d−1)=mn/2. An edge sum replaces its selected 1 by 0. Every Boolean vector except the all-ones vector occurs in this way, by changing any of its zero coordinates to 1 before subtracting the corresponding power. Therefore the restricted sumset is exactly A\{Σ3^i}, of cardinality m−1. The strict inequality required by the original source is met even at C=1.

On a nonedge the signed ternary vector has exactly one coordinate −1; all others are 0 or 1. For two distinct signed vectors, let r be their largest differing coordinate. The contribution there has magnitude at least 3^r, while the lower-coordinate contribution has magnitude at most 2Σ_{j<r}3^j=3^r−1. It cannot cancel. This proves injectivity on all such signed vectors, hence on nonedge pairs. It also proves disjointness of nonedge sums and edge sums.

This is a genuine sum-preserving embedding for the finite sets of sums being used. It does not assert that Z^d embeds injectively as a group into Z. Such a global assertion would be false and is not needed.

## 3. Adversarial rectangle estimate

Take any A′⊆A and any B′⊆B. Put k=|A′|, α=k/m, and let J index B′, with t=|J|. On the full cube, X(ε)=#{i∈J:ε_i=0} has mean t/2 and variance t/4. Hence

Σ_{ε∈{0,1}^d}(X(ε)−t/2)^2=mt/4.

The number of nonedges in A′×B′ is N=Σ_{a(ε)∈A′}X(ε). Direct Cauchy–Schwarz, first over A′ and then extending a nonnegative square sum to the full cube, gives

N ≥ kt/2 − √(kmt)/2 = m(αt−√(αt))/2.

The argument never treats the coordinates as independent after conditioning on A′. A′ may be chosen adversarially to favor high-weight vectors. Independence is used only under the uniform measure on the full cube, so there is no conditioning gap. The formula is uniform in J, not merely typical over coordinate sets.

Distinct nonedges yield distinct integer sums, so |A′+B′|≥N. If αt≥4, then √(αt)≤αt/2 and consequently

|A′+B′|≥αtm/4.

If |A′|≥cm and |B′|≥cd, then αt≥c²d. Therefore d≥4/c² implies

|A′+B′|≥c²dm/4.

The proof loses harmless constants but no factor depending negatively on the imbalance. There is no union bound, probabilistic exceptional set, or unproved expansion hypothesis.

## 4. Quantifiers and boundary cases

For any proposed 0<c≤1 and K>0, choose an integer d>max{2,4/c²,4K/c²}. Every eligible rectangle then has |A′+B′|>Km. This dimension may depend on c,K because those constants must be fixed before the input sets are chosen. The construction itself always has the same δ=1/2,C=1.

If c>1 no subset can meet the retained-size condition, so the existential rectangle conclusion is already impossible for nonempty A,B. Taking c=1 is handled normally. Integer rounding of cm or cd only strengthens the inequalities |A′|≥cm and |B′|≥cd. Empty sets are permitted in the intermediate inequality, where the lower bound becomes trivial; they cannot qualify for the final positive-fraction conclusion.

Because m/n=2^d/d tends to infinity, the construction does not refute the bounded-imbalance theorem. An asserted dependence on m/n would be a different conclusion.

## 5. Verified prior attribution and implication

[Green and Kane, arXiv:1703.01036v2](https://arxiv.org/pdf/1703.01036v2), §4, printed/PDF page 5, records the cube {0,1}^d with positive basis vectors in Z^d, credits the observation to Hosseini, Impagliazzo and Lovett, and states that |A′+B′|≤L|A′| forces |B′| to be bounded solely in terms of L. The [author-hosted v1](https://cseweb.ucsd.edu/~dakane/probabilisticallyclosedCounterExample.pdf), §4 on pages 4–5, contains the same statement and attribution. The final proof accurately records both versions. The arXiv landing page verifies the v1/v2 submission dates; no claim about peer review is needed for the mathematical argument.

To check the sign convention explicitly, if U={0,1}^d, E={e_i}, and 1 denotes the all-ones vector, then

(1−A′)+(−B′)=1−(A′+B′).

Thus reflecting the first summand and negating the second preserves both retained cardinalities and the full-sumset cardinality; U is preserved. The positive and negative basis examples are equivalent. Encoding the relevant signed vectors in base 3 preserves these cardinalities, as proved above.

For fixed proposed c,K, a qualifying AIM rectangle would satisfy |A′+B′|≤(K/c)|A′|. The recorded source assertion would therefore bound |B′| by a constant depending only on K/c, while the retained-size requirement gives |B′|≥cd→∞. This is the exact logical bridge from the prior stronger obstruction to the AIM conclusion. The proof also proves the necessary conclusion directly, so its correctness does not depend on accepting an unproved literature remark.

Tao and Vu's *Additive Combinatorics*, printed page 91/PDF page 111 of the inspected copy, contains a simplex example in Exercise 2.6.1 and an instruction to adapt it for the ε=0 obstruction in Exercise 2.6.2. The proof correctly treats this as related background rather than attributing the precise Boolean-cube rectangle statement directly to that exercise.

## 6. Compatibility with other structural statements

Writing S=A+_G B, an inclusion A′+B′⊆S+S−S does not imply |A′+B′|=O(m) without a size bound on that threefold container. This counterexample contradicts no such conditional inclusion. Likewise, an asymmetric BSG statement with imbalance-dependent losses is compatible with the present lower bound. Failure of a stronger approximate-group theorem alone would not settle the weaker rectangle question; the explicit count here does settle it.

The refutation does not depend on an auxiliary structural theorem or the failure of one. Its exact ratio-free rectangle assertion is settled negatively by the explicit argument, with the underlying obstruction credited to the prior literature. Other possible structural conclusions require their own hypotheses and proofs.

## 7. Supplemental audit metadata

The recorded independent exact-arithmetic checks passed: signed base-3 injection for 1≤d≤10; construction and sign-reflection identities for 2≤d≤14; all 1,050,688 rectangles for 2≤d≤4; 1,463,801 adversarial binomial-layer boundary checks for 2≤d≤128; exact-rational dimension-selection checks; and a negative control detecting signed base-2 collisions.

These aggregate totals describe supplementary historical audit work only. Programs, fixtures and detailed outputs are not distributed in this proof-only edition, which makes no claim of executable reproduction from its files. Finite checks do not establish the universal quantifier; the self-contained analytic proof in Sections 2–4 does.

## 8. Acceptance limits

No remaining mathematical gap was found in the exact rectangle refutation. The result should be represented as verification and explicit exposition of a known counterexample. It should not be represented as a new discovery, as a theorem that all structural consequences fail, or as a contradiction to balanced/bounded-imbalance BSG results.

This proof-only edition distributes authored mathematics and public citation/hash metadata. Third-party PDFs, page images, extracted source text, programs, fixtures, detailed checker output and private coordination records are excluded. The proof and the mathematical audit are self-contained.
