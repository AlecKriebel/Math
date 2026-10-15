# Independent mathematical verdict: PR374 Turns 1–2

Frozen head `c683fc4b84266a6a153c087e182cf427ed502d6c`; base `efd29c05204703acca9a0860812f54b94fae54b1`. Scope: every universal assertion in Turns 1–2, exact unrestricted source problem, all multipartite part counts, complete joins with low-density internal blocks, all asymptotically triangle-minimizing sequences, and nonmultipartite ties/edit separation. This is not an audit of the separate cograph/local routes in Turns 3–5.

**Verdict: no mandatory mathematical correction found in Turns 1–2.** Their stated restricted results are supported; the original unrestricted problem remains unresolved. The claimed author status “unsolved after five turns” is consistent with these two turns but whole-package validation belongs to the integrating audit. No novelty or present global open-status certification is issued.

## Independent entry and seal

Three primary documents were freshly downloaded and inspected first; exact source metadata and failures are preserved. Before reading any candidate proof or verifier I sealed the independent formulation, proof mechanisms, and source-free exact controls in `source_first_seal.json` at 2026-10-03T07:46:10.320879Z. The independently reconstructed proof in `source_first_formulation.md` includes the full moment optimization, join identity, triangle-minimizer deduction, and explicit paw tie.

Candidate prose was then read from the exact frozen Git object and matched byte-for-byte to the clarified snapshot. The parent's A notation was a placeholder; two initial nonexistent path errors were preserved in ignored tmp and the actual snapshot path was supplied. While awaiting clarification, an agent inventory automatically exposed unrelated PR375/376 completion summaries; no PR374 sibling mathematical result was exposed, and the independent formulation was already sealed. This limited process deviation is recorded rather than silently omitted. No author verifier or historical review was read before this mathematical verdict was sealed.

## Turn 1: universal moment proof passes

The normalization `c=6 sum_(i<j) a_i^2 a_j^2` is correct for induced four-subsets. It is three times a fixed-labeled-cycle probability, and cycle count is asymptotically `c n^4/24`. The full restricted value is `F(p)=3[(1-p)^2-L(1-p)]`.

For each fixed finite dimension, compactness gives a minimizer; deleting zero coordinates correctly handles support faces. At reciprocal q the Hölder inequality `q<=S4^(1/3)` has equality only for equal positive coordinates, so all reciprocal boundary cases are settled. At nonreciprocal q constraint rank is two; the positive-coordinate cubic has at most two positive roots. The second-variation vector on two repeated smaller roots is feasible and gives `8(t-u)(2t+u)<0`, excluding the wrong stationary branch. The dimension exception is correctly avoided, because a repeated-small-root vector with an additional larger coordinate has at least three coordinates.

The unique supported form is r equal large parts and one smaller part, with `1/(r+1)<q<1/r` and r=floor(1/q). This also proves the proposed vector is feasible in every original dimension allowed by Cauchy–Schwarz. Equal roots, zero small parts, and q=1 are consistent. The candidate's formula uses r=floor(1/q), while the independent formulation uses m=ceil(1/q) off knots; these are the same indexing, and at knots the candidate's r+1 form merely includes a zero class.

The finite identity `24N/n^4=3(q^2-p4)+6(p3-q)/n+3(1-q)/n^2` is correct by expanding `binom(n_i,2)binom(n_j,2)`. Its error is independent of the number of parts. Together with continuity at every reciprocal knot and at q=0, it handles arbitrary multipartite sequences whose part counts diverge. Thus no hidden fixed-part-count restriction remains. The separate compact-closure/dust proof in the source-first formulation supplies another universal justification. Candidate equation (9), the exact quadratic-field expansion, is verified independently without approximate square roots.

Endpoints: p=0 gives c=0; p=1/2 gives 3/8; p=1 gives 0. At p=1-1/r, `F=3(r-1)/r^3`. Adjacent branches coincide as vectors after deleting a zero part. The source comparison correctly identifies the credited clique construction; no historical novelty is inferred.

## Turn 2: direct bound and full join theorem pass

The direct matching proof fully reconstructs the bound `c(W)<=3p(W)^2/2`, without needing an external low-density C4 theorem. A four-vertex C4 contains exactly two perfect matchings. Pointwise, twice its indicator is no greater than the number of present perfect matchings. Each matching consists of two edges involving disjoint independent sampled vertices, so its expected indicator is p squared, also for fractional graphons. All 64 simple four-vertex graphs satisfy the pointwise inequality. The source-first seal treated the low-density theorem as external before this direct proof was read; this audit now distinguishes the full reconstructed direct proof from the still-external triangle theorem.

For a complete join of blocks of masses w_i and internal densities p_i,c_i, the exact formulas are

`p=1-sum_i w_i^2(1-p_i)`;

`c=sum_i w_i^4 c_i+6 sum_(i<j) w_i^2 w_j^2(1-p_i)(1-p_j)`.

Every other occupancy pattern has a degree-three vertex and cannot induce C4. The cross term counts two nonadjacent vertices in each of two blocks; it is not an internal edge term. The formulas hold for arbitrary internal graphons. When every p_i<=1/2, split each block into two independent classes with `2u_iv_i=p_i`; this keeps global p exactly fixed and changes c by `sum_i w_i^4(3p_i^2/2-c_i)>=0`. The result is multipartite, so Turn 1 proves the desired restricted upper bound. The deficit identity has precisely two nonnegative summands. No implication is made for a block with p_i>1/2: such a split is impossible and the stated hypothesis is essential.

The countable case is valid: sums have nonnegative summands, refined part masses sum one, and their tail mass tends to zero. Merging the tail produces second/fourth-moment changes tending to zero and continuity applies. This covers zero blocks, empty interiors, balanced interiors, infinitely many positive blocks, and all global density knots. The finite graphon uses internal `p_i=2e_i/|B_i|^2`, rather than a finite binomial normalization, so Mantel gives p_i<=1/2 exactly. Sampling collisions have probability at most 6/n; candidate finite error (7) is correctly normalized and uniform.

## All triangle-minimizing sequences: external theorem used correctly

The primary Pikhurko–Razborov Theorem 1.1 is an epsilon/delta theorem uniform over the graph's actual edge density a. It permits a general triangle-free residual block, not solely a complete bipartite block. The candidate applies it to every sequence with triangle excess tending to zero, selecting n sufficiently large for each fixed epsilon. The resulting adjacency edit bound changes induced C4 density by at most six epsilon, since `binom(n,2)binom(n-2,2)/binom(n,4)=6` exactly. The H family satisfies the complete-join hypothesis by Mantel. Fixed p<1 permits continuity of the rounded construction densities, including knots; p=1 is handled by missing-edge scarcity. Letting epsilon tend to zero gives the stated limsup for ALL sequences, not only canonical hosts. The non-effective positive-triangle-excess corollary follows by a sequential contradiction and is valid.

This is a check of the exact theorem premises and a reconstructed deduction, not a reconstructed proof of PR stability or the clique density theorem. Those prior theorems remain credited external inputs. The source's unrestricted hypothesis would require an additional theorem covering C4 extremizers with positive triangle excess; no supplied premise gives it. The candidate explicitly states this gap and therefore does not substitute a restricted conclusion for the original conjecture.

## Nonmultipartite ties and edit separation pass

For every interior noncritical high-density branch, replace two source parts a,b by an internal bipartite component u,v plus isolated mass z, with uv=ab and u+v+z=a+b. The full join identities prove that edge and C4 densities agree exactly; the triangle-free internal flexibility also preserves triangles. For u in [b,a], z is nonnegative, and z>0 in the interior. A global triple has exactly one edge precisely when it selects one vertex from u,v,z, so its density is 6uvz. Complete multipartite graphons have zero one-edge triple density; coupling three edge states gives an L1 distance lower bound 2uvz. Relabeling cannot remove this invariant. The paw density is positive as an additional obstruction, `24(r-1)a uvz`. Candidate rational values at masses (4,2,2,1)/9 and its 8/729 edit lower bound are correct.

The independently constructed different rational tie in `source_first_formulation.md` is additional checkable evidence: p=16/25, c=144/625, triangle=24/125, paw=16/625, and distance >=8/1875 via four-subset counting. The endpoints do not carry the positive-separation claim: at the zero/equal-part boundaries the available isolated mass vanishes. These ties contradict a uniqueness-based reduction; they do not contradict the source value conjecture. The candidate makes that distinction explicitly.

## Strongest verified result and exact remaining gap

For every complete multipartite host, every complete join whose internal edge densities are at most one half, and every asymptotically triangle-minimizing sequence (using credited stability), the proposed construction value is an upper bound. Complete multipartite constructions attain it, and the explicitly exhibited nonmultipartite family also attains it. All part counts and endpoints are covered. What remains is an upper bound for arbitrary graphs outside these classes, especially with positive triangle excess. Treating that reduction as automatic is blocked because it simply restates the central unsupported difficulty.

Supplementary finite/exact controls are falsification and reproducibility evidence; none replaces the universal proofs above. Current priority/open status is bounded to the freshly read primary material and the mathematical scope of this candidate. No communication to an outside individual was attempted.
