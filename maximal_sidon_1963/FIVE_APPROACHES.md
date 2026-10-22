# Erdős 156: five approaches and rigorous limitations

Date: 2026-10-21. Queue 1856 / corpus ID 1963. Status: **NOT SOLVED**. No asymptotic improvement or priority claim is made. The elementary lemmas below are proved here for auditability, not asserted to be new. Computations are finite certificates, not extrapolation.

## Target and conventions

Write g(N) for the smallest size of an inclusion-maximal ordinary Sidon subset of [1,N]. Ordinary means unordered sums with repetition are unique: a+b=c+d implies {a,b}={c,d} as multisets. The target is g(N)=O(N^(1/3)) for every sufficiently large integer N. Existing inspected source: Ruzsa, *A Small Maximal Sidon Set*, Ramanujan J. 2 (1998), 55–58, https://doi.org/10.1023/A:1009757824153; author manuscript https://www.renyi.hu/~ruzsa/cikkek/sidmax.dvi . Its bound remains O((N log N)^(1/3)). The source gate and public-source metadata in the recovery directory specify inspection provenance.

## Approach 1: exact blockers, parity, and the counting deficit

Let A be Sidon, k=|A|, and x outside A. Then A∪{x} fails to be Sidon if and only if either

* x=a+b−c for a,b,c∈A, a≤b and c∉{a,b}; or
* 2x=a+b for distinct a,b∈A.

Proof: a new collision must contain x. If it occurs on both sides with the same multiplicity it cancels to a trivial equality. A single occurrence gives x+c=a+b, and a double occurrence on one side gives 2x=a+b. Cancellation excludes c=a or c=b when x∉A. Conversely both displayed equations give nontrivial collisions. In the second case a=b would force x=a, so it is excluded. This classification includes repeated summands a=b in the first case.

There are k(k−1)(k−2)/2 witnesses of the first type with a<b, and k(k−1) with a=b, totaling T=k²(k−1)/2. If e and o count the even and odd marks, integer midpoint witnesses number P=binom(e,2)+binom(o,2). None of the witness values is in A, by Sidonicity. Values can coincide or lie outside [1,N]. Consequently maximality gives

N≤k+T+P=(k³+k−2eo)/2.

In particular g(N)≥(2N)^(1/3)−o(1). This does not strengthen the growth exponent or remove the upper logarithm. The parity term is quadratic at most, so it cannot by itself establish an unbounded-factor improvement over N^(1/3).

An exact accounting can retain losses. Count every valid witness as a token, discarding those outside the interval. Let W_out be the discarded-token count, and m_x the number of remaining witness tokens with value x. Let C=Σ_{x:m_x>0}(m_x−1). If A is maximal, then exactly

N=k+T+P−W_out−C.

Thus any lower-bound improvement from this approach must control boundary loss or collision surplus uniformly for every saturated set. Merely counting possible witnesses does not provide such control. A= {1,3} demonstrates that omitting midpoint blockers changes the problem: 2 is blocked although 2∉A+A−A.

Result: exact criterion and parity-sensitive necessary bound, exhaustively checked for N≤16. No new asymptotic conclusion.

## Approach 2: random Singer lifts and where the logarithm enters

Ruzsa starts from a modular Sidon set B of p+1 marks modulo q=p²+p+1, takes independent lifts a_i=b_i+q d_i with 0≤d_i<M=floor(N/q), and uses disjoint modular triple witnesses. For a residue outside B there are at least p/8 disjoint triples in the inspected proof; the chance that each triple supplies the required integer lift equality is at least c/M, uniformly in the needed lift range when M is sufficiently large. Independence for this selected family yields

P(m unblocked by triples)≤exp(−c' p³/N).

This is an upper bound, not an asymptotic equality or a lower bound on failure probability. Summing over m outside the seed residue classes gives an expected number of exceptions at most N exp(−c' p³/N). A direct extension can pay one mark per exception, plus the controlled seed-residue completion cost. The resulting certified objective has the form

p+1+floor((N−1)/q)+N exp(−c' p³/N).

For this *particular upper estimate* to certify O(N^(1/3)) by the trivial one-point-per-exception repair, its last term would need to be O(N^(1/3)), requiring p³/N≥(2/(3c'))log N−O(1). Thus this estimate retains the logarithmic scale. At p=C N^(1/3), the estimate on residual count is only a fixed fraction of N, not O(N^(1/3)). This does not prove that the random model cannot achieve a better realization.

Conditional expectation could select lift variables so that the final exception count is at most its expectation, if one computes the exact conditional objective. Such derandomization alone preserves the same estimate and is not a logarithm removal. No efficient conditional-expectation oracle is claimed. Likewise the witnesses for one fixed m being disjoint does not make the bad events for different m independent: their supports can overlap throughout the seed. A local-lemma invocation needs an actually verified dependency or lopsided-dependency bound, which is absent here.

Result: exact proof bottleneck isolated. Missing ingredient: structured repair of a large exceptional set, or a genuinely stronger all-points coverage theorem at p≈N^(1/3).

## Approach 3: difference-budget completion instead of pointwise repair

For an integer Sidon set S, let Δ(S) be its positive difference set. The ordinary Sidon property is equivalent to all positive differences of distinct unordered pairs being distinct. This follows by rearranging a repeated positive difference into a pair-sum collision, and conversely orienting a nontrivial pair-sum collision.

**Completion lemma.** Let S⊂[1,N] be Sidon. Suppose all points currently addable to S lie in (S+D)∪(S−D)∪H, where D is a finite set of positive integers and H⊂[1,N]. Then any Sidon extension A⊃S has

|A\S|≤|D\Δ(S)|+|H|.

Proof: every x∈A\S is individually addable to S. Separate those in H, at most |H|. For each other x choose an anchor a_x∈S and d_x=|x−a_x|∈D. The pairs {x,a_x} are distinct as x varies because x lies outside S whereas its anchor lies inside S. Their positive differences in A are therefore distinct and do not belong to Δ(S). This is an injection into D\Δ(S). A maximal extension exists by finite greedy addition.

**Modular corollary.** If S contains exactly one representative of each residue in B modulo q, and every currently addable point has a residue in B, then any extension adds at most floor((N−1)/q) marks. Match each new point to the seed representative of its residue and use D={q,2q,…,floor((N−1)/q)q}. No seed difference is divisible by q. This sharpens the elementary 1+2N/q directed-difference estimate printed in the inspected manuscript, only by a constant; no novelty is asserted.

The completion lemma is a genuine alternative target: construct seeds S with |S|=O(N^(1/3)) whose uncovered set is covered by seed translates by only O(N^(1/3)) absolute distances, plus O(N^(1/3)) free exceptions. That would settle the problem even if the number of uncovered points were much larger than N^(1/3). It does not assert the existence of those seeds. Selecting D to cover an arbitrary residual set is an auxiliary covering problem with the seed fixed; relaxing Sidonicity or ignoring the forbidden existing differences is not valid.

Result: rigorous sufficient condition and improved completion constant; construction satisfying the sufficient condition remains missing.

## Approach 4: group constructions, carries, and product obstructions

A modular ordinary Sidon set lifted with one representative per residue is automatically integer Sidon: equality of integer sums implies congruence, which identifies the residue multiset, and unique representatives then identify the integer multiset. Maximality does **not** transfer. A modular equation x≡a+b−c can have a nonzero multiple of q discrepancy in the integers; the integer midpoint may likewise fail.

The independent reviewer supplied the transparent example: {0,1} is maximal ordinary Sidon modulo 5 (every other residue creates a modular repeated sum), while its canonical representatives in {0,…,4} are not maximal: 3 and 4 can each be added. Our separate lift guard uses B={0,1,3} modulo 7 and S={1,9,18} in [1,21]; the residues of S are B+1, and S has fifteen addable points. Modular saturation alone therefore supplies no interval saturation certificate.

Repeating a modular construction in several q-blocks does not automatically repair carries: the union of two translates of any two-mark subset repeats a positive difference. For example {1,3,11,13} is not Sidon. Cartesian products likewise have rectangle collisions (a,b)+(a',b')=(a,b')+(a',b) when both factors have two distinct points. Embedding these rectangles by a base expansion does not remove their additive equality. One must construct a graph-like selection with controlled difference uniqueness rather than take the full product.

Characteristic-two analogues require a different Sidon convention: 2a=2b for every a,b, so any ordinary repeated-summand Sidon set in such a group has at most one mark. Results using only distinct summands cannot be directly imported. See Redman–Rose–Walker, https://arxiv.org/abs/2109.00292, which also retains a logarithmic factor in group-order notation.

Result: valid Sidon-lifting direction identified; maximality, carry repair, product, and convention shortcuts explicitly falsified. No all-N construction obtained.

## Approach 5: finite certificates and the all-N interpolation obligation

The independently checkable example A={8,48,68,69,71,75,104,120} is saturated in [1,144]. It is the translate by 1 of the example associated with Huber's preprint, https://oeis.org/A399118/a399118.pdf . The source gate previously inspected the preprint; fresh retrieval in this pass failed. We verified the integer example itself from scratch: all 36 unordered pair sums are distinct and each of the 136 omitted points has an explicit triple or midpoint collision. The JSON certificate contains these witnesses; a separate pair-sum oracle verifies every augmentation is non-Sidon. This certifies existence at N=144 only, not the preprint's optimality assertion max E_8=144. Its computational archive has not been independently replayed.

Our exhaustive enumeration of all subsets for every N≤16 independently checks the exact blocker criterion, parity bound, completion-distance injection, and the minimal sizes. These values are 1,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4. They are a regression test, not a claim to new finite records. No inference from these values to a uniform constant is valid.

**Interpolation lemma.** Suppose A is maximal in [1,n] and m≥n. Extend A greedily to a maximal Sidon set in [1,m]. All new points lie in {n+1,…,m}, because every old omitted point was already blocked by A and remains blocked. With L=m−n≥1 and t the number of new marks, unique positive differences among the new marks give binom(t,2)≤L−1. Hence

g(m)≤|A|+floor((1+sqrt(1+8(L−1)))/2).

For L=0 no extension is necessary. In particular a family at an increasing unbounded sequence n_j, with |A_j|≤C n_j^(1/3) and gaps n_{j+1}−n_j≤K n_j^(2/3), would suffice for the all-N target. Proof: for n_j≤m<n_{j+1}, the added term is O(sqrt(K)n_j^(1/3)), hence O(m^(1/3)). Bounded successive ratios alone do not guarantee this sufficient gap condition; the displayed interpolation estimate can then cost O(sqrt(m)). Cubic-scale mesh n_j=j³ would meet it, but no saturated O(j) construction on that mesh is supplied.

Truncating a saturated set is not a valid replacement: the reviewer's example {0,3,4} is saturated in {0,…,6}, but its restriction to {0,1,2} is {0}, which is not maximal. Translation and reflection do preserve saturation when the ambient interval is moved correspondingly; dilation does not fill the intervening integer holes.

Result: finite existence certificate and a rigorous sparse-to-all-N sufficient condition. Missing ingredient: a uniform constructive family with suitably controlled gaps.

## Source and priority limits

The original source is Erdős–Sárközy–Sós, *On Sum Sets of Sidon Sets, I* (1994), Problem 7, https://doi.org/10.1006/jnth.1994.1040; the recovery inspected its repeated-summand convention and exact question. Fresh official problem-page retrieval again returned HTTP 403. The prior gate's indexed OPEN status is not live certification. No matching asymptotic resolution was found in the follow-on search; this is not an exhaustive nonexistence assertion.

A primary author page indexed at https://robin.riblet.go.yj.fr/ lists a forthcoming Riblet–Schehr work titled *Difference Sets of maximal Sidon sets have large intersection*. Direct page retrieval returned HTTP 403 and no theorem text or accessible manuscript was located in the exact-title search. Its title alone cannot establish applicability, a lower bound, or priority over any lemma here. We make no novelty claim that would depend on excluding it.

The 2026 publication of Riblet–Schehr's distinct-distance-constant work is confirmed by https://doi.org/10.1007/s10474-026-01604-z . Its optimization is a different target. Search snippets and secondary automated research pages were discovery aids only, not authority for mathematical conclusions.

## Deliverables and stopping point

Run `python checks.py` from any working directory. It writes `checks_results.json` and `certificate_N144.json`. `independent_audit.py` and the review report belong to the independent reviewer. All proofs are elementary and explicitly scoped. This packet does not remove log N, establish a stronger unbounded-factor lower bound, or justify changing the problem's status from open.
