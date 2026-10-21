# Independent measure-class and factorization review

Review date: 2026-10-03 UTC. Reviewer: the independently assigned measure/factorization auditor. This is an audit of the frozen candidate, not an author revision, new construction, publication, or full-result certification.

## Verdict and binding

**PASS for the assigned measure-class, ordinal-factorization, and associativity obligations. No fatal or substantive repair-required gap was found in these obligations.** The original source category was independently checked and the scalar specialization is valid. This does not certify novelty, the continuous-field argument, or the entire maximal-core/generation argument, which have a separate audit. I read the entire candidate for interactions and found no measure-theoretic obstruction to those later arguments.

The reviewed file is `CANDIDATE_PROOF.md`, exactly 20,525 bytes, SHA-256:

`152881a86b39c8b8afec166842000b8b256cad2ac04c764731e23468d8877d85`.

All ten file entries in `FROZEN_MANIFEST.json` were recomputed and matched their recorded byte lengths and hashes. The supplied WIP provenance is branch `wip/free-product-generation-30001179`, commit `6d1d44e7ffee89976a50fc1f4db5a350a033247e`. This audit independently verifies the local bytes; it does not independently re-fetch or certify that remote commit. No frozen author file was changed and no remote state was written.

The exact primary source was read from its local text and the images of printed pages 529 and 530, and its official PDF URL was independently opened:

https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1

Local PDF SHA-256: `5121d8ec30d2c1346cbbdd68164915d5a24fb31e5a94a3a3215ba576954ee64d`.

The line references below refer to the frozen candidate.

## 1. Exact category and scalar specialization

On printed p.529 the source defines the reduced pointed free product as the vacuum summand plus the Hilbert direct sum of finite alternating tensor words in the orthogonal complements of the central unit reference vectors. Its algebraic free product system consists of Hilbert B–B bimodules, pointed B-bilinear unitaries from the free product of two fibres to the sum-time fibre, associativity, and canonical zero-time identifications. The source explicitly leaves continuity or measurability as additional bundle conditions and discusses continuity of the embedded tensor multiplication. It does not require that a free product system already arise from the later inductive tensor-to-free construction.

On p.530 the question concerns whether the intersection of the embedded ordered tensor products generates the given free system. The next theorem constructs a free system from an already supplied spatial tensor system; it is not a theorem that arbitrary free systems come from that construction.

For B=C, any complex Hilbert space is a Hilbert C–C correspondence, every vector commutes with the scalar left/right actions, and a complex-linear unitary is B-bilinear in the module sense. The isolated vacuum point has measure one, so its indicator is a central unit vector. The given scalar specialization therefore lies in the actual source category. A counterexample there suffices to refute the universal generation assertion. There is no coefficient-algebra mismatch or confusion with the tensor product system of an associated E0-semigroup.

## 2. Parameter recovery, Borel structure, sigma-finiteness, and separability

Candidate lines 19–37 are sound.

Both defining limits for Gamma are Borel conditions in the countable product R^N. The first limit holds gamma-almost surely by Gaussian tail bounds and Borel–Cantelli, and the second by the strong law for the independent integrable random variables z_j^2. Taking a countable sequence of positive error thresholds justifies the first convergence statement as written.

For (a,delta,z) in the stated domain, x_j=a+delta*2^(-j)z_j has limit a and recovered squared scale delta^2, so Theta is injective. Conversely, for every x in C, the displayed inverse z_j=2^j(x_j-a(x))/d(x) satisfies both Gamma conditions exactly. This is a genuine Borel bijection of the stated Borel sets, not merely a many-to-one pushforward with a hoped-for sigma-finiteness property. The functions a(x) and d(x) are Borel on C.

The set |a|<=N, 1/N<=d<=N has measure 4N log N for N>=1, with the harmless zero value at N=1. These sets exhaust C. Consequently the pushforward is sigma-finite. Finite products mu^n times Lebesgue^m are sigma-finite; the countable disjoint union over (n,m) is also sigma-finite. Standard Borel spaces have countably generated Borel sigma-algebras, and a sigma-finite measure on one gives separable L^2 by finite-measure exhaustion and approximation by a countable generating algebra. Thus the separability assertion at lines 77–81 is justified. Completion of the measures does not enlarge L^2 modulo equality almost everywhere.

The interval restriction is a countable intersection of coordinate conditions. Restriction preserves sigma-finiteness and separability. Infinite total mass on some restricted interval sectors would cause no problem: the distinguished unit vector is the separate mass-one vacuum, not the constant function on the whole word space.

## 3. Exact prefix/tail identity and Radon–Nikodym direction

Candidate Lemma 1 is valid, including its direction of density and its use with sigma-finite measures.

Write y_j=x_(j+k). Then

  (1/N) sum_(j<N) 4^j(y_j-a)^2
  = 4^(-k) (1/N) sum_(i=k)^(N+k-1) 4^i(x_i-a)^2.

The right-hand average tends to 4^(-k)d(x)^2, by removing finitely many initial summands from a Cesaro-convergent sequence. Therefore d(y)=2^(-k)d(x), with the positive square root. Conversely, prepending any finite vector v multiplies d(y) by 2^k and leaves the limit unchanged. Both operations preserve C exactly and are inverse Borel maps.

There is no need to assume a probability disintegration theorem for an infinite total measure. The density assertion follows directly by Tonelli and change of variables. Split the original Gaussian coordinates into z_0,...,z_(k-1) and the tail w_j=z_(j+k), and put delta'=2^(-k)delta. The product Gaussian measure splits into gamma_k times gamma. The set Gamma itself is stable under removal/addition of arbitrary finite prefixes, so restricting to Gamma introduces no hidden correlation between prefix and tail. The parameter measure satisfies ddelta/delta=ddelta'/delta'. For j<k, change variables

  v_j=a+2^(k-j)delta' z_j.

Its finite-dimensional Jacobian gives the factor

  phi((v_j-a)/(2^(k-j)delta')) / (2^(k-j)delta').

The tail is Theta(a,delta',w), and its recovered parameters are precisely (a,delta'). Thus for every nonnegative Borel F on C,

  integral F(x) mu(dx)
  = integral_C integral_R^k F(p_k(v,y)) q_k(v;y) dv mu(dy).

This proves the candidate's formula as an equality of sigma-finite measures. In addition, integral q_k(v;y) dv=1 for every y in C, so its stated tail marginal really is mu. Every q_k is finite and strictly positive, giving equivalence in both directions.

Let eta=dv*mu(dy) and p=p_k. The equality is mu=p_*(q_k eta), and therefore

  d(p_*eta)/dmu at p(v,y) = 1/q_k(v;y).

Consequently the canonical L^2 multiplier is q_k^(-1/2), exactly as at line 103. In particular,

  integral_C |f(p^(-1)x)|^2 / q_k(p^(-1)x) mu(dx)
  = integral |f(v,y)|^2 dv mu(dy).

The reciprocal is essential and is correctly chosen. Unboundedness of q_k^(-1/2) is not an obstruction: this norm identity defines a unitary between the different measured L^2 spaces.

The displayed chain rule is also exact, not just an almost-everywhere heuristic. Prepending l values leaves a unchanged and replaces d by 2^l d. Hence the first k Gaussian scales in q_k(v;p_l(w,y)) are 2^(k+l-j)d(y), and q_l(w;y) supplies exactly the remaining l scales. Their product is q_(k+l)(v,w;y).

## 4. Why Gaussian singularity theorems do not obstruct the construction

The construction does not require equivalence of Gaussian product laws at different fixed a or delta. Indeed, those laws live on disjoint level sets of the recoverable parameters and are singular when the corresponding parameters differ. Treating them as equivalent would be wrong, but the candidate does not do so.

Translation changes the Lebesgue parameter a; deletion changes delta to 2^(-k)delta; positive dilation changes (a,delta) to (ra,rdelta). All of these are handled on the mixing-parameter space. The Gaussian coordinate sequence z remains unchanged under translation/dilation, and deleting its first k entries has exactly the original product law on the remaining entries. No infinite product of likelihood ratios is asserted. The only likelihood ratios used for prefix absorption have finitely many factors with the explicit finite-dimensional Jacobian above.

Thus neither Kakutani equivalence criteria nor an unverified Cameron–Martin shift hypothesis is missing here. The Haar factor ddelta/delta is what makes finite-tail rescaling preserve the marginal measure. Translation preserves mu, while dilation carries mu(A) to mu(rA)=r*mu(A), because only da contributes a factor r. These claims are correct.

For each fixed c, the level set a=c is null and each event x_j=c is null by integration of the conditional Gaussian density against the sigma-finite parameter measure. Countable unions preserve nullity. Convergence to a!=c makes the side of c eventually constant. Finite products of these null statements remain null because all factor measures are sigma-finite. Restricting to interval supports does not turn null sets into positive-measure sets.

## 5. Fixed ordinal concatenation is actually bijective

Candidate Lemma 4 is correct. Ordinal absorption does not delete coordinate values: it reindexes a finite suffix as the finite prefix of the next infinite sequence.

For alpha=omega*n+m and beta=omega*p+q with p>0, write the inputs as

  (x^1,...,x^n; v_0,...,v_(m-1))
  (y^1,...,y^p; w_0,...,w_(q-1)).

The output coordinates are

  (x^1,...,x^n,p_m(v,y^1),y^2,...,y^p; w).

From an arbitrary output one recovers the first n blocks, removes the first m entries from the next block, and recovers all remaining blocks/suffix coordinates unchanged. Tail stability makes this an inverse on every point of the stated spaces. If p=0, it is ordinary finite suffix concatenation. This also covers m=0 and zero-length words via the singleton mass-one factor.

For any fixed finite list of lengths, iteration gives a Borel bijection. Although different input grade lists can have the same total ordinal, Lemma 4 claims bijectivity for a fixed list only, and that claim is sufficient. No cancellation law for ordinal addition is being incorrectly invoked.

For an arbitrary parenthesization, the flattened ordered coordinate word is the same. A useful check is to track each original infinite block and the finite coordinate string immediately preceding it: that finite string becomes its prefix, while the final finite string remains the final suffix. Regrouping changes only how those finite strings are assembled. The q chain identity covers sequential absorption into the same block; absorptions into distinct blocks act on distinct product factors. This independently confirms the nontrivial density compatibility in Lemma 4.

## 6. Maximal color-run charts, including limit-ordinal boundaries

Candidate Lemma 5 is valid. The issue of crossing an omega-block boundary is real, but is handled by the stated prefix/tail mechanism.

Fix the two open subintervals separated by c. On a sector omega*n+m, remove the countable collection of coordinate-equality events x_beta=c and the finitely many block-limit equalities a_i=c. The remaining set is conull. Each of its n infinite blocks has an eventually constant binary color string and thus finitely many runs. There are only finitely many boundaries between the infinite blocks and finitely many final letters. The entire ordinal color word has finitely many maximal monochromatic convex subsets. A change at a limit position omega*i contributes at most one extra boundary; it does not create an infinite run count or require a predecessor at that position.

To check that a convex run remains in the defined word category, suppose it begins at omega*i+k. If it ends in the same block it is finite. If it reaches a later block, its first infinite constituent is the tail beginning at k of block i, its subsequent infinite constituents are the full intervening original blocks, and any final portion of its end block is a finite prefix. The infinite tail lies in C by Lemma 1; the full blocks already lie in C. The same description applies to a run terminating in the final finite suffix. Its order type is below omega^2. In particular, runs crossing several block boundaries do not have to be represented by an inappropriate single sequence: they retain the corresponding finite number of omega-blocks.

Conversely, an alternating finite list of nonempty one-color words concatenates to a word with exactly those runs. The fixed-length concatenation map is injective, and maximal-run decomposition is unique. Distinct choices of run count, color pattern, or ordinal run lengths consequently have disjoint images, even though some distinct grade lists have the same total ordinal. Allowing empty runs would break this uniqueness, but the free-word factors are explicitly nonvacuum.

The charts are indexed by finite lists drawn from a countable set of ordinal lengths and two colors, so there are countably many. On each fixed chart, its domain is a Borel product of interval-support sets. Its image is Borel because the unrestricted fixed-grade concatenation is a Borel isomorphism. The color restrictions are countable coordinate inequalities. Lemma 1's strictly positive densities ensure the restricted product measure and restricted output measure are equivalent on that image. Conditioning on colors need not preserve independence; independence is not claimed or needed, since the RN factors account for the dependence.

Each centered Hilbert tensor summand is L^2 of the corresponding product of nonempty one-color word spaces. Splitting by its countably many ordinal grade tuples and applying these chart unitaries gives exactly the reduced pointed free-product decomposition. The mutually disjoint conull chart images prove surjectivity, not merely an isometric embedding.

## 7. Null sets and all finite associativity diagrams

For a fixed finite set D of cuts, remove all events that a coordinate or original infinite-block limit belongs to D. This is conull simultaneously in every sector. Every resulting infinite block is eventually in a single component interval of R minus D, so the full word has finitely many maximal runs for the finite color set.

This finite-cut good set is stable under the operations used in the proof: finite-prefix insertion does not change the limit of the affected infinite block, finite-tail deletion does not change its limit, and regrouping preserves the coordinate values. For translations in the product-system maps, translate the cut values with the corresponding word. On the domain side the corresponding excluded sets are null by the fixed-chart measure-class equivalence, or directly by the product null-set argument. Thus a common conull set is available for every fixed finite associativity diagram. There is no need for a conull set working for every real cut at once.

For three factors, the canonical pointed-Hilbert-space free-product associator identifies both parenthesizations with the same direct sum of finite words in the three centered factor spaces, with neighboring factor labels different. For example, grouping the first two factors means grouping every maximal string that avoids the third factor. This is exactly the word regrouping used by the candidate. The same applies to any finite number of factors.

For a measure-class Borel isomorphism c:X->Y and d:Y->Z, set rho_c=d(c_*eta)/dzeta and rho_d=d(d_*zeta)/dxi. The chain rule is

  rho_(d o c)(z) = rho_c(d^(-1)z) rho_d(z)

almost everywhere. Positive square roots therefore give U_d U_c=U_(d o c) exactly as L^2 operators. Tensor products and disjoint sums respect this identity. It is enough to check each countable fixed-grade chart and then use density/direct sums; simultaneous pointwise choices of all RN versions are unnecessary.

The time translations also agree. Both parenthesizations shift the three original factors by s+t, t, and 0, respectively. Common translation commutes with concatenation, and q_k(v+h;y+h)=q_k(v;y), since a shifts by h and d is unchanged. Hence no additional translation-dependent cocycle occurs. The vacuum factors and zero-time cases are identities. This proves the required associativity obligation for the constructed pointed unitaries; the same coordinate/RN argument gives coherence for every finite regrouping.

## 8. Interaction checks with the later proof

These are limited cross-checks, not a replacement for the continuity/core audit.

- The pair differences in Lemma 3 depend on disjoint Gaussian pairs, are symmetric and nondegenerate, and have independent signs. Infinite rises and falls thus occur almost surely, uniformly in the parameter values, and remain almost-everywhere properties after interval restriction. There is no invalid normalization or conditional-probability step here.
- The sigma-finite parameter model supports the translation/dilation strong-continuity argument used later: on parameters these transformations act only on the finite-dimensional a and log(delta) variables and fix the Gaussian coordinate variable.
- Nonzero infinite interval sectors are justified. For a in [t/3,2t/3] and delta in [t/100,t/50], the success thresholds t*2^j/(3delta) are uniformly at least (50/3)*2^j. The independent Gaussian success probabilities have a strictly positive infinite product because the failure probabilities are summable and each success probability is positive. The parameter region has measure (t/3)log 2, finite and positive. Thus the proposed grade-omega support really has a finite-positive-measure subset.
- Positive RN multipliers preserve support projections. Nothing in the measure-class construction prevents the later rational-cut support calculation or the finite-sector free-hull computation.

## 9. Optional precision improvements, not proof gaps

No author repair is required by this audit. For a polished exposition, two points could be made more explicit without changing the construction:

1. Interpret line 43 as `(p_k)^*mu = q_k (lambda^k x mu)`, or state the nonnegative-integral identity above. The current differential notation is standard shorthand, but the integral identity makes the sigma-finite argument and reciprocal RN direction especially easy to audit.
2. A general Borel bijection that is nonsingular in only one direction need not induce a surjective L^2 unitary. The formula at lines 99–103 should be understood under the two-way measure-class equivalence already proved for every map actually used. Its application here has that stronger property and is correct.

The converse sentence in Lemma 5 is also understood after deleting the corresponding null sets on both sides: some one-color sequences can have their limit at the cut, but that set is null. This is already covered by the phrase “off the exceptional null set” and by chart nonsingularity.

## Final scoped assessment

The measure construction, finite-prefix equivalence, fixed ordinal concatenation, finite color-run factorization, and canonical associativity survive the requested adversarial checks. No counterexample to an asserted lemma in this assigned half was found. The packet's finite arithmetic check was not treated as evidence for the infinite-dimensional claims; the reasoning above supplies the independent audit of those claims. This result alone is not a declaration that the whole mathematical problem is solved or that the construction is new.
