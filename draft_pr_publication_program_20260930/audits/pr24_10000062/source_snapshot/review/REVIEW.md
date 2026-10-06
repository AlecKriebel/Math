# Independent review: metric-ball homogeneous Euclidean triangulation

## Verdict and exact boundary

**PASS for the explicitly scoped Euclidean non-cocompact example.** The reviewed construction is a locally finite face-to-face triangulation by straight triangles of diameter at most $r=\sqrt{10}$. Its vertex-centered radius-$r$ metric disks have congruent restrictions of all cells, including boundary-only traces. Its full Euclidean symmetry group is not cocompact.

**This is not a full-source solved verdict.** The example has nonzero horizontal translation symmetries, does not address the hyperbolic clause, and does not resolve the source's undefined use of “periodic.” It refutes the Euclidean conclusion only when periodicity means cocompact/crystallographic symmetry. The known layered family is correctly credited; neither historical novelty nor external peer review is certified.

- Record: **10000062 / AMR-099-0062**.
- Reviewed artifact: `CANDIDATE.md`.
- SHA-256: `3df33716dab169f07c9ff24434023d2945fc8121e03519f91a0a3fdb1ea30f84`.
- Submitted checker SHA-256: `19e8cb51992446ab768843af4dc7ed753c425ce639b51fe40ddb44183f1e5ac6`.
- Date: 2026-09-30 UTC. Separate reviewer: `gpt-6-astra`, effort `xhigh`.
- Required mathematical revisions: **none** for that scope.

## 1. Original problem and prior family

The original is Benjamini–Tessera Question 5.7 in *Euclidean vs. Graph Metric*. The [author's original URL](https://www.wisdom.weizmann.ac.il/~itai/erd100.pdf) did not furnish an accessible PDF during this review. The full question on printed p. 7 was read and visually checked in the [dated archived original](https://arquivo.pt/noFrame/replay/20201231041538id_/http://www.wisdom.weizmann.ac.il/~itai/erd100.pdf), using the locally recovered source file.

The source permits ambient isometries without an orientation restriction and states a non-strict triangle-diameter bound. It mentions both Euclidean and hyperbolic geometry and supplies no definition of periodicity. These facts agree with the candidate's qualifications. The proof interprets respecting the triangulation as preserving the cell restrictions to the disk. It does not assert that every entire triangle merely meeting the disk is carried to an entire triangle outside the disk as well.

[Frettlöh–Garber, *Symmetries of Monocoronal Tilings*](https://arxiv.org/pdf/1402.4658), Definitions 1.3–1.4, Theorem 2.2, Section 2.3/Figure 8, and Appendix A.1.2/Figure 17, were checked. They already describe the independently chosen chiral triangle layers alternating with isosceles layers and their non-crystallographic members. Their theorem ensures at least one translational period for planar monocoronal tilings when reflections are allowed. The candidate credits this construction and separately proves the stronger metric-disk property for its chosen parameters. It does not infer the metric-disk hypothesis from monocoronality alone.

## 2. The underlying triangulation

Each strip is partitioned by parallelograms between two equally spaced horizontal rows. Splitting each parallelogram along the prescribed diagonal gives exactly the two triangle families in the candidate. Neighboring strips share their row edges, so the result is face-to-face, without crossings or gaps. The positive lower bound on row spacing and fixed horizontal spacing imply local finiteness. Every triangle is nondegenerate.

The two squared-side triples are exactly

$$\{5/4,13/4,4\},\qquad \{4,10,10\},$$

with areas $1$ and $3$. For a triangle, its Euclidean diameter is its longest side. Thus $r=\sqrt{10}$ is a valid diameter bound and is attained. The argument requires the stated non-strict inequality; it does not claim an example with every diameter strictly below the comparison radius.

## 3. Full metric-disk locality

After placing a lower-row vertex at the origin, the only possible dependence on the preceding chirality occurs in the cap below $y=-3$. The rows at $y=\pm4$ lie outside the radius-$\sqrt{10}$ disk. All remaining potentially visible strips are determined by the central short-band choice.

The line $y=-3$ intersects the closed disk in the segment between $(-1,-3)$ and $(1,-3)$. At either endpoint, every edge descending into the remote short strip has direction $(h,-1)$ with $|h|\le3/2$. Its scalar product with the endpoint is at least $3/2$. Consequently the squared distance along the edge increases strictly from $10$, and its only disk intersection is the endpoint. An edge descending from any farther row vertex has $|x|\ge3/2$ and $|y|\ge3$ throughout; its squared distance is therefore at least $45/4>10$.

These inequalities rule out all additional cap edges, rather than only their far endpoints. The cap belongs to the single triangle whose upper base is the fixed segment from $(-1,-3)$ to $(1,-3)$. Its clipped shape is independent of the remote apex. This addresses the main way in which a metric disk can contain information outside the vertex corona.

### Boundary-only traces

At each of those two circle vertices there are six incident edges and six incident triangles. Exactly three incident edges have positive-length traces, and three have only the singleton trace. Exactly four incident triangles have positive-area traces, and two have only the singleton trace. The outside directions retain their cyclic incidence pattern under either remote chirality. Thus the local cell restrictions agree even if identical singleton traces retain their distinct parent-cell labels and incidences.

All other traces occur in the fixed strips. In the open disk, the complete embedded edge set partitions the disk into its face pieces. A clipped triangle is convex, hence connected, and its boundary and choice of side determine that piece. Equality of the relevant edge geometry therefore gives equality of positive-area face pieces, while the preceding cap and singleton analysis covers the closed-circle boundary. No unverified inference from an incident vertex star is used.

## 4. Congruence for every vertex

Reflection in the vertical axis exchanges the two central shifts $1/2$ and $3/2$ modulo horizontal period $2$ and preserves the isosceles tall-strip geometry. Although it can change remote choices, those choices have just been proved invisible inside the disk.

The stated half-turn about $(\delta_0/2,1/2)$ takes an upper-row root to the lower-row origin. The whole-family reindexing can be checked explicitly: if the original offsets are $a_j$, the new lower-row offsets are

$$a'_i=\delta_0-a_{-i}-\delta_{-i},\qquad \delta'_i=\delta_{-i}.$$

Then $a'_0=0$ and $a'_{i+1}-a'_i=\delta'_i+1$. Thus the image really is another member of the same strip family, with the same central chirality and reversed surrounding choices. Root translations and these two isometries handle all vertices. Their use is permitted by the original problem, which does not require orientation-preserving maps.

## 5. Translation and full symmetry groups

Length-$2$ edges are exactly the horizontal row edges. Any symmetry must preserve their supporting-line direction. A translation must preserve the alternating strip heights, so it moves a lower row to another lower row and has vertical component $4m$ for an integer $m$.

The chirality of a short strip is detected by the sign of its shortest cross-edge's horizontal displacement when read upward. A translation preserves this sign. For the sequence with exactly one exceptional short strip, invariance under the vertical shift $4m$ forces $m=0$. Preserving a horizontal row's vertex set then forces the horizontal component to belong to $2\mathbb Z$. Conversely those translations do preserve the tiling. The translation subgroup is exactly $2\mathbb Z\times\{0\}$.

Every full symmetry has linear part preserving the horizontal direction, hence one of four diagonal orthogonal matrices. The translation subgroup therefore has finite index at most four. If the full group acted cocompactly, a finite union of images of a compact fundamental set would give a compact fundamental set for the translation subgroup. Horizontal translations cannot cover points of arbitrarily large height from such a set. This proves non-cocompactness without assuming that lack of rank-two translations alone excludes some unexamined infinite collection of rotations or glides.

The same calculation confirms the limitation: the tiling still has the translation $(2,0)$ and is not strongly aperiodic.

## 6. Independent reproduction

The submitted checker was copied to the review directory and run there, without modifying the author's files. Its **16 rooted cases passed**, including the oriented-face tests and boundary-only multiplicities.

A separately written standard-library checker imports none of the submitted code. It constructs strip parallelograms, splits them into triangles, and classifies segment/triangle intersections with the circle using exact rational squared distances. It checks **64 rooted cases**, varying five neighboring short-band choices rather than three. All **212 assertions passed**. In every case it obtains:

- eight vertices in the closed disk;
- 28 edges with positive-length traces;
- 23 faces with positive-area traces;
- two boundary-only locations, each with three singleton edge traces and two singleton face traces;
- at each such location, the complementary incidence of three positive-length edge traces and four positive-area face traces.

For edges with positive-length intersections, equality is checked using their entire endpoint pairs, a stronger finite comparison than equality of their clipped subsegments. The complete face conclusion is supported by the analytic partition argument above and by the submitted oriented-half-plane checks, not by face counts alone.

The independent checker also verifies the outward cap inequalities, the side lengths and areas, and the half-turn strip identity. At squared radius $1001/100$, the canonical comparison distinguishes two different preceding-layer choices. This is a negative control for the fixed-radius shielding calculation. It is **not** a proof that no other ambient isometry could match those larger disks, nor is any such assertion needed.

From the directory containing this review:

```sh
python3 submitted_verify.py
python3 independent_checks.py
```

Outputs are `verification.json` and `independent_results.json`. Both scripts use only the Python standard library. The finite checks supplement the infinite-family locality and symmetry proofs; they do not establish those conclusions by sampling.

## Final disposition

The frozen candidate is suitable for a draft PR presenting a **partial, explicitly scoped Euclidean cocompact counterexample**, with the existing prior-family attribution and novelty disclaimer. No mandatory mathematical correction was found. Do not promote the full record to an unconditional solved status, suppress its translational period, reinterpret “periodic” without disclosure, or claim that the hyperbolic clause has been settled.
