# Independent audit of the generalized Saxl graph counterexample

Audit date: 2026-10-03 UTC.
Target: problem 30006342, OWR-14299292-003.
Decision: **PASS for the explicit degree-19683 primitive affine counterexample and its implication that the original universal conjecture is false.**

All mathematical discovery credit belongs to **Aluna Rizzoli and Adam R. Thomas**, *Common neighbour conjectures for Saxl graphs fail at every base size*, [arXiv:2609.01367v1](https://arxiv.org/abs/2609.01367v1), submitted 1 September 2026. This audit is a credited verification, with no novelty claim.

## Audit boundary

This audit verifies the concrete group in Section 7, Table 2, first row, and the frozen certificate's logical route from that action to a counterexample. It independently establishes the finite group, irreducibility, primitivity, minimum base size two, and failure of the common-neighbor property. It also verifies the ancillary diameter-three claim.

It does not certify the entire preprint, the every-base-size family of Section 6, the completeness of any classification/search, the global minimality of degree 19683, or the authors' Lean development. No Lean build, GAP run, Magma run, or IRREDSOL lookup was used. Those are unnecessary for this finite counterexample. No remote state was changed during the original audit.

## Original review provenance and public projection

The independent review checked all 49 files of the original packet and reran its verifier with byte-identical JSON output. The original reviewed manifest SHA256 was:

`6064e8e6da4d87e3a94e42c3a8fd575db421e2364e914671ad66b38f52cfeb03`

That original 49-file manifest and its source PDFs, screenshot, repository snapshots and operational records are deliberately not reproduced in this public projection. The public package has its own manifest and must not be mistaken for a complete copy of the original input. Source URLs and the exact finite mathematics, generator data, executable checks, result JSON and review are retained. The original unprojected audit SHA256 was `1e5a5ff6a5a24d992d4a4841e76a8b4ff5d976219be16a5095a3146d3e43dbd4`.

The public checker preserves every mathematical computation in the audited script. It changes only its input-root location to a relative path and the original-manifest lookup to the same historical digest literal. Its resulting exact-check JSON remains byte-identical to the audited output. Run `python verify_public_packet.py --replay` to check the public manifest and both computations. Provenance digests and transformations are listed in PUBLIC_PROJECTION.json.

The original frozen replay was integrity evidence, not independent mathematical verification. Independence is supplied by the separate implementation described below.

## Original target and primary-source checks

The official [Oberwolfach report](https://publications.mfo.de/bitstream/handle/mfo/4340/OWR_2025_27.pdf?isAllowed=y&sequence=1), printed page 1406, was checked in the saved page image and in a fresh read of the official PDF. Its definition uses pairs contained in a base of **minimum cardinality**. Conjecture 1 covers **every finite primitive permutation group with base size at least two**. The sporadic, almost-simple and diagonal restrictions appear in subsequent positive results, not in that conjecture's hypotheses. Thus an affine example of base size two is squarely in scope.

The arXiv abstract/version page and [full HTML](https://arxiv.org/html/2609.01367v1) were accessible in this audit. The saved paper's Table 2 lists the degree-19683 example with stabilizer order 1152, 1152 regular vectors, 96 missing sums, and diameter three. The frozen generator file identifies commit `b2c0a8f95aa4dca76a034a0e769a8c8249f38ae2` in the authors' repository.

Fresh GitHub blob and raw-file requests returned tool errors. Consequently, this audit does not claim a successful new remote fetch of that commit. It uses the frozen literal source file, its matching manifest digest, and the packet's saved provenance. Its SHA-256 is `b53c4253db629fb22e00b6acf4ee79a8c005c85c53d7f5f0ba8e2d4a2f8278d0`. The mathematical verification does not depend on the remote file's availability.

## Independent computational method

New program: `independent_dense_fixedspace_check.py`.

The new program never imports either frozen verifier and never executes the authors' GAP code. It parses only the three literal `MonomialGen` data rows from the frozen source file, reconstructs dense 9-by-9 matrices, and enumerates their closure by ordinary integer matrix multiplication followed by reduction modulo 3.

The decisive regular-vector computation uses a different method from the packet. For each matrix A, it computes the kernel of `A^T-I` by exact Gaussian elimination over F3, enumerates that kernel, and increments the stabilizer count of every fixed vector. It therefore determines stabilizers without using orbit lengths, the packet's signed-permutation composition, its vector-action routine, or its base-3 Boolean-mask indexing. Each enumerated kernel vector is also checked against dense row multiplication. All 19683 vectors are represented as explicit coordinate tuples.

The two-fold sumset is subsequently computed by coordinate-wise tuple addition. The witness is hard-coded to the advertised value rather than selected from whatever holes the program happens to find. Comparisons to the frozen JSON occur only after the independent mathematical checks succeed.

Environment: Python 3.12.14; NumPy 2.3.5. Arithmetic is integral and exact. Matrix entries are reduced modulo 3; no floating point or probabilistic test is used. Assertions must remain enabled: run `python`, not `python -O`.

## The action and group order

Let V=F3^9, with row-vector action. The generator specified by (p,s) maps e_i to s_i e_p(i). The parsed data agree exactly with the certificate:

```text
p1 = (0,2,1,6,8,7,3,5,4), s1 = (1,1,1,1,1,1,1,1,1)
p2 = (4,5,3,6,7,8,1,2,0), s2 = (1,1,1,1,1,1,1,1,1)
p3 = (0,1,2,3,4,5,6,7,8), s3 = (1,1,1,1,1,1,2,1,2)
```

All generators are invertible. Dense closure produces exactly 1152 matrices. Every enumerated matrix has its inverse in the enumeration, and closure under both left and right multiplication by generators is checked. Finite closure of invertible matrices equals the generated group H.

The diagonal kernel D has 64 elements. The coordinate-permutation image has 18 elements and is transitive on all nine positions. As an additional identity check, the first permutation generator is an involution, the second has exact order nine, and conjugation by the first inverts the second. The resulting 18 pure permutation matrices form a complement. The diagonal subgroup is an elementary abelian 2-group of order 64. Thus the advertised structure `C2^6 semidirect D18` is also verified, although this structural name is not needed for the conclusion.

For G=V semidirect H, the affine degree is 19683 and the order is 22674816. The action is faithful: an affine transformation fixing zero has zero translation part, and a linear transformation fixing every vector is the identity matrix.

## Irreducibility and primitivity

The nine coordinate characters of D are pairwise distinct. More strongly, the independent code explicitly computes, for each i,

```text
sum over d in D of d_ii * d  (mod 3) = E_ii.
```

Here E_ii is the matrix projecting onto coordinate i. This is the character projector formula: 64 is 1 in F3 and each nonzero diagonal entry is its own inverse.

If W is an H-invariant subspace, it is D-invariant and is preserved by every F3-linear combination of D. Therefore each coordinate projection sends W into W. A nonzero vector of W has a nonzero coordinate, so W contains a coordinate axis. Transitivity of H on the nine axes then gives W=V. This proves irreducibility; it does not confuse coordinate transitivity alone with irreducibility.

For completeness, consider a block B in the affine action with 0 in B. For b in B, the translation by b takes 0 into B, hence its translate of B intersects B and must equal B. Thus B is an additive subgroup. Every element of H fixes 0, so likewise preserves B. Since the underlying field is the prime field F3, B is an H-invariant F3-subspace. Irreducibility forces B={0} or B=V. Translations make the action transitive; consequently G is primitive.

## Stabilizers and minimum base size

The exact fixed-space dimension histogram over the 1152 matrices is:

```text
dimension 1: 600 matrices
dimension 3: 443 matrices
dimension 5:  99 matrices
dimension 7:   9 matrices
dimension 9:   1 matrix
```

The total fixed-point incidence is 77184. Dividing by 1152 gives 67 orbits by Burnside's lemma, independently agreeing with the frozen orbit enumeration.

The stabilizer histogram on V is:

```text
stabilizer order : number of vectors
1:1152, 2:12096, 4:2880, 6:384, 8:2448, 12:96, 16:216,
18:128, 24:96, 32:144, 64:18, 96:24, 1152:1
```

Let R be the set of vectors with trivial H-stabilizer. Thus |R|=1152. The dense orbit of the explicit vector

```text
r = (2,1,1,1,1,1,1,1,0)
```

is exactly R, proving that there is one regular orbit. The pair {0,r} has trivial pointwise stabilizer in G and is a base. No singleton is a base because all point stabilizers are conjugate to the nontrivial H. Therefore **b(G)=2 exactly**, not merely b(G) at most two.

The sorted regular-vector-code digest is

`ad599d7fa427b77837a9304ff318e61a2a8bc579eeed9d3d66b0688f476a8eac`.

It agrees with the frozen computation.

## Graph criterion and fixed witness

Because b(G)=2, a generalized Saxl edge is precisely a two-point base. Translating one endpoint to zero shows that u and v are adjacent exactly when v-u belongs to R. This also excludes loops: 0 is not regular. Further, R=-R because H fixes v exactly when it fixes -v.

Use the fixed pair

```text
x = (0,0,0,0,0,0,0,0,0)
z = (1,1,1,1,1,1,0,0,0).
```

The endpoints are distinct. The independently computed stabilizer of z has order 24, so they are nonadjacent. Every one of the 19683 possible vertices w is tested against both exact conditions

```text
|H_w| = 1 and |H_(w-z)| = 1.
```

There are **zero** successful candidates. For the 1152 vertices satisfying the first condition, the second stabilizer orders have histogram

```text
2:768, 4:168, 6:24, 8:168, 24:24.
```

In particular, the absence of a common neighbor is not inferred merely from nonadjacency, nor from a diameter/common-neighbor equivalence that can fail at base size two.

The separate tuple sumset computation gives |R+R|=19587 and exactly 96 holes. All 96 coordinate tuples, not just the count, agree with the frozen JSON; z is one of them. The equivalence is direct: a common neighbor w would give z=w-(w-z) in R-R=R+R.

The ancillary diameter-three statement also passes. Both 0 and all of R lie in 2R. Each of the 96 missing vectors lies in 3R. The distance-shell sizes from zero are 1, 1152, 18434, and 96. Translation invariance makes the graph diameter three.

## Adversarial controls and possible failure modes

- Kernel calibration passed for identity, minus identity, a single-coordinate sign flip, a coordinate transposition, and a nonsymmetric 3-cycle. Their kernel sizes and coordinate relations were checked explicitly.
- All generated fixed vectors satisfy the original dense equations. RREF free variables enumerate the entire solution space, so this is not a sample.
- The sum of the stabilizer counts equals the sum of fixed-space cardinalities and gives the independently corroborated Burnside orbit count.
- A positive common-neighbor control gives 1152 neighbors for equal endpoints at zero; the explicit distinct pair {0,r} has 23 common neighbors. Thus an accidentally constant-empty adjacency test would fail.
- A negative irreducibility control confirms that the two permutation generators alone fix the all-ones line. The sign generator does not, and the actual full-group certificate uses nine verified projectors.
- Zero versus one-based indexing and row versus column action are handled explicitly from the authors' matrix definition. The tuple result is only converted to the packet's base-3 code for final comparison.
- The frozen verifier chooses the first hole rather than asserting the stated witness literally. This is not a defect in its executed result: its output is the advertised vector. The independent audit removes this avoidable dependence by fixing z in advance.
- The frozen replay establishes no proof of global minimum counterexample degree, and none is claimed here.

No mathematical defect or scope mismatch was found within the audited boundary.

## Conclusion and reproduction

This single primitive affine action, of minimum base size two, is a valid counterexample to the original universal OWR conjecture for base sizes at least two. It also refutes its weaker nonadjacent-pair diameter-at-most-two consequence. It does not refute the separate amended almost-simple-or-diagonal conjecture.

Run the independent check with:

```sh
python review/independent_dense_fixedspace_check.py
```

The review directory contains the portable checker, exact result JSON (including all holes), captured original run output and environment record. The original frozen-replay record is omitted along with the source-only material; the separate public verifier checks this projection and both executable results. All mathematical claims above are preserved and supported by the included checks and proofs.

**Final decision: PASS. Exact scope: credited finite counterexample verification and original universal-target refutation. No independent approval of all-base-size families, classification completeness, publication acceptance, or Lean verification is implied.**
