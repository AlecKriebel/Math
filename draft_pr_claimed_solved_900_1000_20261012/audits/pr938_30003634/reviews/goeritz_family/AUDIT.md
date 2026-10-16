# Independent Goeritz/diagram adversary — PR938 / 30003634

## Finding and scope

**The Goeritz signature calculation passes.** In Erle's convention, whose positive trefoil has signature -2, the downward-oriented standard closure of the specified braid has signature **-2**. The 48-by-48 matrix is the actual reduced checkerboard matrix of that closure, not just a matrix with the advertised inertia. Exact independent arithmetic gives inertia (23,25,0), determinant -7154819319988224 and correction mu=0. Mirroring gives signature +2.

This family verifies the geometric/signature step and its braid/link prerequisites. The implication that an algebraically split 1-solvable link has zero signature is **conditional here**, assigned to the separate topology family. No Meyer calculation, historical acceptance, sibling conclusion, priority claim or current-open claim is used. This is a verification of the submitted mechanism, with zero new positive proof-search turns; it introduces no substantively new route.

The complete charter, private source record and original proof were read first. `INDEPENDENT_RECONSTRUCTION.md` and a first independent exact result were written before reading any author executable, historical audit verdict or current sibling report. After that reconstruction, only the author's certificate data were compared: the word, all matrix entries, all 48 rational pivots and reported invariants match. No author executable or historical audit verdict was read at all.

## Primary source and actual pixels

The source is Dieter Erle, *Calculation of the signature of a 3-braid link*, Kobe Journal of Mathematics 16(2) (1999), 161–175, [version of record](https://da.lib.kobe-u.ac.jp/da/kernel/E0003685/E0003685.pdf), DOI 10.24546/E0003685. The actual downloaded PDF is 421860 bytes, SHA256 `6a97f27686bad303ea5cc7ec8db0ad0943599d3fcc6192b0bc65c1cc7c6f218a`. Its repository cover says **PDF issue 2026-10-15**. The web tool's cached wrapper says 2026-10-12; the actual download, not that cache, is pinned here. The wrapper date does not change the journal's 1999 publication date.

The actual cover and every relevant printed page 161–165 were rendered and inspected. Checks covered the exterior closing arcs in Figure 1; local theta pictures and definition on p.163; the complete formula, proof and block picture on p.164; and the oriented exceptional/nonexceptional pictures, signature formula and correction on p.165. Raw PDF, extraction and rendered pages remain private. `SOURCE_PINS.json` records their hashes and the inspection map.

## Independent standard diagram reconstruction

Fix three horizontal positions and orient every braid segment from top to bottom. At crossing vertex v, list the four ports in clockwise order NW, NE, SE, SW. The strands run NW–SE and NE–SW. Join the bottom port at each horizontal position to the next top port at that position; join the final bottom to the first top at the same position by the usual nested exterior closing arcs. Those exterior arcs are embedded and pairwise disjoint, and have no crossings. This is exactly the standard braid closure, with no extra braid-axis component.

The independent program constructs these edge pairings before constructing any Goeritz matrix. Its face successor crosses an edge and then takes the clockwise-next port at its endpoint. The resulting cycles are the oriented face boundaries. The west sector of a sigma1 crossing identifies the unbounded face O. A breadth-first coloring across diagram edges makes O an alpha face. The program checks planarity by V-E+F=2, consistency of the coloring, and every stated local incidence, raising an explicit exception on failure. This is a combinatorial embedding certificate, independent of the candidate's cyclic matrix formula.

For the actual word there are 104 crossing vertices, 208 edges, and 106 faces. Exactly 49 are alpha faces: O plus 48 bounded faces. `INDEPENDENT_RESULTS.json` records all 104 crossings' four adjacent faces, both alpha incidences, theta and exceptional status. It also records the explicit permutation from the computed face order to the cyclic order below. `STANDARD_CLOSURE.svg` is generated from the nested word and these exact face boundaries, with undercrossings, the complete exterior arcs and all 104 crossing labels. `SOURCE_EXAMPLE_RECONSTRUCTION.svg` independently draws Erle's example word; comparison with the source pixels checks the drawing convention. Both its full view and the witness's top and bottom were visually inspected, including the final-to-first face seam.

Here is the symbolic incidence argument, which supplies the universal local derivation rather than inferring it from sampled tests. The region on the west side of every sigma1 crossing connects along the left side of position one to O. Its east alpha sector is the region extending between positions two and three immediately before the following sigma2 block. Consecutive sigma1 crossings introduce beta bigons, so their east alpha region does not change. At a sigma2 crossing the alpha sectors are north and south; it advances from one bounded alpha region to the next. Consecutive sigma2 crossings therefore create one new alpha region per crossing, with beta regions on the sides. Intervening sigma1 blocks keep the current alpha region between positions two and three connected. The top and bottom closing arcs connect the alpha sector after the final sigma2 crossing to the sector before the first one; they neither create a crossing nor a further bounded alpha face. This proves the cyclic sequence and its attachment to O.

Thus, for a word with nonzero alternating powers sigma1^(A_j) sigma2^(B_j), set N=sum|B_j|, t_1=0 and t_(j+1)=t_j+|B_j|. Its bounded alpha vertices are R_0,...,R_(N-1), and the sigma1 block A_j joins O to R_(t_j). The kth sigma2 crossing in block j joins R_(t_j+k) to R_(t_j+k+1), indices modulo N. The program checks all these individual incidences and the wraparound for the witness, rather than accepting their aggregate counts.

## Local crossing contributions, orientation and correction

Use Erle's actual theta picture: with alpha sectors west and east, the positive crossing (NE–SW overstrand in this projection) has theta=+1; changing the overstrand changes theta's sign. Rotating the checkerboard sectors to north and south changes that sign. Consequently:

| Crossing | Alpha sectors | theta | Exceptional? |
|---|---|---:|---|
| sigma1 | west/east | +1 | yes |
| sigma1 inverse | west/east | -1 | yes |
| sigma2 | north/south | -1 | no |
| sigma2 inverse | north/south | +1 | no |

This classification of exceptional crossings follows from the actual downward arrows, independently of crossing handedness: at the west/east sectors there is an incoming and an outgoing boundary branch, whereas the north sector has two incoming branches and the south sector two outgoing branches. These are exactly the two local types in Erle's Figure 2. Exterior arcs are upward outside the braid and have no crossings; they contribute nothing to mu.

For two distinct alpha regions, a theta crossing contributes theta to each diagonal and -theta to each off-diagonal. Deleting O removes its row and column. A sigma1 block therefore adds A_j to the diagonal of R_(t_j). A sigma2 crossing with s=sgn(B_j) contributes

    -s (e_i-e_h)(e_i-e_h)^T,

which is the displayed block [[-s,s],[s,-s]]. Hence the full reduced matrix is

    G = sum_j A_j e_(t_j)e_(t_j)^T
        - sum_(all sigma2 crossings) s_j (e_i-e_h)(e_i-e_h)^T.

All crossings are accounted for. There are 56 sigma1 crossings (28 of each sign), and 48 sigma2 crossings (24 of each sign). The actual theta counts are 52 positive and 52 negative. Only the 56 sigma1 crossings are exceptional, so mu=sum A_j=0. Erle's formula then gives sigma(L)=sign(G)-mu.

These formulas apply to links with multiple components, not only knots. The orientation is the canonical braid orientation throughout. Reversing all components reverses both local arrows at each crossing and leaves the exceptional classification unchanged. Reorienting only selected components would require recomputing the correction; that operation is not used. Mirroring changes every theta and mu sign, so G changes to -G and signature changes sign. No unmentioned component orientation choice is needed to obtain -2.

## The source-index discrepancy is real, and numerical agreement alone misses it

On printed p.164 the off-diagonal formula uses s_(2p) on the interval belonging to the block n_(2p+2). The corresponding proof sentence repeats that index. This is not merely OCR damage. The block picture on the same page uses the current sign s_2 along its first block, then s_4 along its second block. The local crossing derivation above proves that **s_(2p+2)** is the geometric sign for that interval. Thus the candidate's stated correction is justified, but citing the literal off-diagonal line without explanation would not be.

A control with A=(1,1), B=(2,-1) makes the distinction checkable:

    geometric G = [[ 1, 1,-1],      literal prior-block G = [[ 1,-1, 1],
                   [ 1,-2, 1],                               [-1,-2,-1],
                   [-1, 1, 1]]                               [ 1,-1, 1]]

The respective inertias are (2,1,0) and (1,1,1). The literal line can change even the nullity.

There is a subtle limitation of using the actual witness to test the indexing: every |B_j| is even. If one replaces each correct current-block edge sign by the printed preceding-block sign, the product of the edge-sign ratios around the cycle is +1. Starting d_0=1 and setting d_(i+1)=d_i times that ratio gives a closed diagonal matrix D with entries +/-1, and G_literal=D G D. The witness therefore gives the same inertia even with that incorrect index. `INDEPENDENT_RESULTS.json` records the explicit switching vector. This is why the source pixels and crossing geometry, not just the observed signature, are necessary evidence for the correction.

## Word, membership and linking prerequisites

Independently construct a=(1,1), b=(2,2), c=[a,b], d=a^-1 c a, e=b^-1 c b, u=[c,d], v=[d,e] and beta=[u,v], where 1 and 2 denote the positive Artin generators. Free cancellation gives 104 letters. The result already begins with a sigma1 block and ends with a sigma2 block; there is no cyclic conjugation hidden in the computation. Grouping equal adjacent generators gives exactly the 23 A and B pairs printed in the candidate. Both sums are zero; N=48.

Membership follows algebraically before any signature calculation: a,b lie in P3; c lies in its first ordinary derived subgroup; characteristicity and normality put d,e there; u,v lie in the second derived subgroup; beta lies in P3^(3). All reconstructed powers are even, so every individual block is pure. Independently following the strand labels through all letters gives the identity permutation and signed pair-crossing sums (0,0,0), hence all pairwise linking numbers are zero. Equivalently, every pure commutator has zero linking by additivity. Deleting all other strands gives a one-strand braid, so each individual closure component is an unknot. These statements do not import any assertion about a higher solvable filtration.

## Exact arithmetic, controls and degeneracies

The independent implementation uses Python standard-library integers and rational fractions. At a nonzero scalar pivot p, it replaces the remaining block H by H-rr^T/p, an explicit rational congruence. When all diagonal entries vanish but an off-diagonal entry b is nonzero, it uses the nonsingular block [[0,b],[b,0]], of inertia (1,1,0), and its exact Schur complement. A remaining zero matrix contributes its full dimension to nullity. These cases were tested independently on zero, empty and off-diagonal-only matrices.

The witness needs 48 scalar pivots with no swaps. All values are recorded, not just their signs. The signs are

    +--++-++-++---++++-----++--+--++-++----+++----++

They give 23 positive, 25 negative and no zero pivots. Their product is -7154819319988224. A separate fraction-free Bareiss determinant calculation gives the same integer. Its exact divisibility checks pass. Therefore sign(G)=-2 and mu=0 imply sigma(L)=-2.

Fourteen named diagram controls pass: both stabilized unknot signs, positive/negative Hopf, positive/negative trefoil, connected diagrams of two- and three-component unlinks, Borromean rings and mirror, positive/negative T(3,3), and one-block cases with two and three cyclic vertices. In particular the positive trefoil yields [3], mu=3, signature -2; its mirror yields [-3], mu=-3, signature +2. The three-component unlink gives a zero 2-by-2 matrix and nullity two, while Borromean rings give signature zero with nonzero determinant 16. Thus zero signature, zero determinant and multiple components are not being conflated.

The 256 two-pair controls range all four exponents independently over {-2,-1,1,2}; the planar face matrix agrees with the cyclic construction and exact determinant/inertia checks pass. These are sampled controls, not a substitute for the symbolic incidence derivation.

The additive edge formulation also handles N=1: the sigma2 crossing meets the same alpha face twice and its contribution is zero, as required by Erle. For N=2, two parallel cycle edges add and produce the factor two in the off-diagonal entry. Zero block exponents should first be removed and adjacent powers combined; they do not belong to the source's reduced alternating-word hypothesis. A word with no sigma2 crossings is outside this cyclic description and can be treated separately as a two-braid closure plus a trivial strand; it is not used here. The actual witness has q=23 and every |B_j|>=2, so these boundary cases do not affect its application.

## Authentication, reproducibility and remaining gap

`AUTH_START.json` and `AUTH_END.json` authenticate all 44 selected disk files byte-for-byte against actual Git commit `2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b`, prefix `unsolved_math_prioritization/attempts/30003634`. The proof pin is `0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b`; the outer publication manifest pin is `149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30`. The shared branch remains main. No Git/index/branch, original-file, service, publication or tracker mutation was performed by this family. Only its own review folder was written. No person, outside agent or sibling family was contacted; communications were to the parent only.

Run `python3 independent_goeritz.py` in this folder to emit the complete independent data to stdout. Writing requires an explicit option, for example `python3 independent_goeritz.py --output INDEPENDENT_RESULTS.json`. Run `python3 draw_independent_diagram.py --output-dir .` to regenerate both SVGs. These need no installation. Regeneration changes the result timestamp and thus requires repinning a publication manifest. The original certificate comparison is informational and was done after reconstruction; the independent checker does not import it.

The mathematical checker uses explicit fail-closed conditions, with zero Python `assert` nodes. `test_replay_modes.py` runs normal, `-O`, `-OO`, and a genuine no-flag child inheriting `PYTHONOPTIMIZE=2`; the observed optimization levels are 0,1,2,2. All return the same mathematical results. In every mode `--expect-signature -1` is rejected with nonzero exit for the wrong numerical expectation, before any successful result is emitted. Default replay leaves the review files unchanged. `REPLAY_MODES.json` records these positive and negative checks. The test harness also uses explicit exceptions and is stdout-only unless `--output` is supplied.

**Strongest verified result:** the explicitly nested beta lies in P3^(3), its canonical closure is a three-component algebraically split link with unknotted components, and its ordinary signature in the stated convention is -2, by a complete standard-diagram Goeritz calculation and exact checkable arithmetic. **Exact remaining gap outside this family:** independently validate the universal 1-solvability/signature-vanishing bridge and the target's source definitions before promoting the counterexample. No unresolved geometric or finite-arithmetic gap remains within this family.

Required fixes within this family: none. Preserve the source-index explanation and convention calibration in any promoted proof. Optional improvement: publish the planar-face certificate and explicit sign-switching caveat alongside the matrix so future replay cannot mistake matching inertia for validation of the printed source index.
