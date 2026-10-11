# Independent audit: simultaneous minimal taut foliations

Problem 10300008 / AMR-102-0008, rank 1003. Review date: 8 October 2026.

## Decision

**Accept the scoped mathematical results. Retain the disposition `unsolved`, with five substantive approaches. A harness-only reproducibility correction is required.**

No mathematical correction to `packet/PROOF.md` is required by this audit. The author packet does not supply a general obstruction classification, a universal construction, or an explicit counterexample after independent isotopies. This review does not establish the complete current literature status, mathematical novelty, human peer review, or journal acceptance.

The one detected defect is operational: the frozen test harness copies read-only payload permissions into fixtures that it subsequently tries to mutate. The authenticated bootstrap passes; the original mutation harness fails for this permission reason. The three-line correction in `HARNESS_CORRECTION.patch` changes only disposable fixture permissions, and the corrected harness passes in normal, `-O`, and `-OO` modes from a genuinely read-only relocated package. The immutable author archive and all frozen payload bytes were preserved.

## 1. Exact object and review boundary

The reviewed object is the 13-member source-free archive `MINIMAL_SURFACES_10300008_AUTHOR.zip`, 25,054 bytes, SHA-256:

`61fc41de148b8502dbc899e9eaa09e5864fabbf98869c691378b50a3001c8274`.

Its author manifest hash is:

`0c1731e5864003466319176235ee3e4feb16c0d7bc29d75a0bc6e43c1f289d89`.

Its proof hash is:

`9c06dee3bb1b609f4afd885e9e4fcbdf0608b734f4d41cc54a592001db821051`.

The archive, the receipt's complete 13-member inventory, and every corresponding frozen-layout byte were compared. They agree. The mutable public draft was not the mathematical review target. The manifest authenticates the nine packet files. Separately checked archive anchors cover the bootstrap and test harness; the manifest alone does not authenticate those outer files. This distinction matters when rerunning a downloaded package.

The proof was read in full, including all hypotheses and unproved-step statements. The independent verifier imports no author functions. Exact finite algebra supports, but does not replace, the differential-geometric and topological reasoning below. No source PDF, extracted source text, source image, raw corpus record, private coordination material, or chat link is included in this review package.

## 2. Source and scope

Calegari's Question 4.2, on printed page 10, concerns a prescribed collection of taut foliations, a metric that may be chosen, and isotopy. It imposes no explicit finite-index-set restriction there. The preceding discussion mentions C2 regularity, and the following observation is PL, not a smooth metric-gluing theorem. The wording does not formally choose between separate and common isotopies. The packet properly states its independent-isotopy interpretation rather than claiming the text resolves that ambiguity. Its smooth, oriented, cooriented results are explicitly narrower. [Primary question and surrounding remarks](https://arxiv.org/html/math/0209081v1#S4)

The reviewer rehashed the existing full local corpus copies and repeated the unique-record join. Both full-file counts, byte counts, full-file hashes, and canonical selected-record hashes match `CORPUS_BINDINGS.json`; see `CORPUS_RECHECK.json`. This is a local recheck, not a claimed fresh corpus download. The author's historical repository searches were not independently rerun. Their negative result remains a bounded recorded search, not a theorem of nonexistence of prior work.

The reviewer independently read the primary arXiv records and relevant theorem statements, and visually inspected the existing renderings of Calegari page 10, Nguyen page 3, and Marques–Neves–Sun page 25. The complete existing PDF/extraction hashes and sizes agree with the author pins. See `SOURCE_RECHECK.json`; no fresh reviewer PDF download is claimed.

## 3. Characteristic form and Route 1

For a global unit normal n, contraction with the oriented volume gives a two-form, not a three-form. Cartan's identity yields d(i_n vol) = (div n) vol. Since the normal-normal contribution to divergence is zero, div n is the tangential trace of the normal derivative. An alternative second-fundamental-form sign convention changes the sign, never the minimality equation. The characteristic form has comass one and equals the oriented leaf area form. These facts justify all later calibration uses.

The single-common-calibration warning is correct. In dimension three, a comass-one two-form corresponds to a unit vector under contraction with the volume. Equality on a unit oriented bivector forces the corresponding normal to be that vector. The two distinct coordinate plane foliations in a flat torus are simultaneously minimal but cannot share such a calibration.

For three everywhere independent positive tangent bivectors xi_i, the compatibility theorem is correct as stated. Set a_i = omega_i(xi_i) > 0. Necessity follows because a_i omega_i(xi_j) is the induced bivector Gram matrix. Conversely, symmetry and positive definiteness define a smooth positive inner product B on the entire rank-three bivector bundle, with B(xi_i,xi_i) = a_i^2. The prescribed omega_i are then exactly its normalized metric duals.

For a metric matrix G in a tangent frame, the matrix of its induced bivector inner product in the cyclic cofactor frame is (det G)G^(-1). In dimension three its inverse map is G = sqrt(det B)B^(-1). The determinant is positive, so the positive square root is smooth. The induced-metric map is intrinsic and injective: coordinate-wise reconstruction therefore agrees on frame overlaps. This verifies the global step rather than merely the formula in one trivialization. The independent tests also check covariance under non-unit-determinant and orientation-reversing frame changes.

Every nonzero bivector in a three-dimensional vector space is simple, so no additional decomposability restriction has been silently omitted. Coorientation together with ambient orientation supplies the positive tangent orientation used here. The assumed bivector frame is nevertheless a strong condition: the proof gives no extension to rank changes or an arbitrary collection.

The nonsymmetric constant-form example correctly disproves sufficiency of individual positivity for those chosen forms. It does not obstruct the underlying foliations, since other forms may work. Route 1 is an exact reformulation within its hypotheses, not an eliminated global existence criterion.

## 4. Route 2: relative second jets and isotopies

At a tangency between z = 0 and z = f(x,y), the two first fundamental forms and all connection terms agree at the point. The difference of second fundamental forms is f_ab g(n,partial_z). The latter scalar is nonzero and can be chosen positive because partial_z is transverse to the common plane. Contracting with the inverse induced metric C gives a strictly positive trace whenever D^2 f is nonzero positive semidefinite. This follows by conjugation with C^(1/2), including the rank-one semidefinite case. Thus both patches cannot be minimal for any smooth ambient metric.

The torus example is valid. Periodicity makes f a globally defined real-valued smooth function on T^2, both displayed circle maps are submersions, and the vertical circle is transverse and meets every fiber. At the specified point the relative Hessian is 4 pi^2 epsilon times the identity. Its sign is independent of the eventual metric.

The isotopy phi_t(x,y,z) = (x,y,z - t f(x,y)) is globally well-defined, has the displayed smooth inverse, starts at the identity, and sends the second foliation to the first at t = 1. Applying it only to that foliation produces identical flat-minimal foliations. Therefore this example is **not** an independent-isotopy counterexample. Under one common ambient diffeomorphism, metric pullback preserves the obstruction. The packet explicitly keeps those two conclusions separate.

The C^k-closeness claim is also valid for every fixed finite k: the graph distribution differs by epsilon times a fixed smooth derivative field. It refutes only an unqualified smooth fixed-representative closeness assertion, not Calegari's PL observation or a theorem allowing further independent isotopies.

## 5. Route 3: compact-leaf homology and topology

This is the main isotopy-invariant partial obstruction, and the complete proof is valid.

On a closed oriented ambient manifold, let S and T be closed connected leaves, oriented by the specified coorientations, with [T] = c[S], c > 0. The two closed characteristic forms give b >= c a and a >= b/c, where a and b are their positive areas. Hence equality holds in both calibration bounds. Nonnegative continuous calibration deficits integrate to zero, so they vanish pointwise. In dimension three the equality case identifies the oriented tangent plane of T with the first foliation and that of S with the second.

The passage from an everywhere tangent compact surface to an entire leaf deserves explicit topology checking. A compact leaf of the original foliation is embedded: its canonical injective immersion is an embedding because its domain is compact and the ambient manifold is Hausdorff. A smooth tangent inclusion of the connected surface T factors through one maximal connected integral leaf L. To see continuity into the intrinsic leaf topology, use Frobenius charts: on each sufficiently small connected surface patch the transverse coordinate is constant, and its tangential derivative has full rank. The resulting map into L is smooth and a local diffeomorphism. It is therefore open. Its image is compact in the Hausdorff manifold L, so it is also closed. Connectedness of L implies the image is all of L. The potentially non-Hausdorff *leaf space* is irrelevant: each individual leaf manifold is Hausdorff. This validates the author's compact/open/closed argument; no additional hypothesis is missing.

Consequently S and T are common leaves of both foliations, and they are either disjoint or identical as sets. The calibration integral also excludes the zero real homology class. Positive c is needed for the displayed inequalities and division; reversing one foliation's coorientation handles the opposite sign separately. The proof does not use compactness of arbitrary noncompact leaves and should not be extended to them without new arguments.

The independent-isotopy consequence follows correctly. If phi(F) and psi(G) share a minimal metric, then psi(T) is a leaf of phi(F). Applying phi^(-1) produces a compact leaf of F in T's oriented ambient isotopy class, because phi^(-1) psi is isotopic to the identity. The composite isotopy also preserves the homology relation and transported orientations. Thus absence of this leaf isotopy class in F is a genuine necessary obstruction, with the symmetric condition as well. The weaker disjoint-representatives conclusion follows, but it is not a sufficiency criterion.

The construction gap is real and honestly identified. Homologous norm-minimizing surfaces alone do not show that a foliation containing one excludes the other's isotopy class; one must control all compact leaves. The packet gives no explicit verified pair violating the condition. Neither nonisotopy alone nor genus minimization can replace those missing facts.

## 6. Route 4: conformal exactness

Under g = exp(2u)g0 in dimension three, the normal scales by exp(-u), the volume by exp(3u), and the trace becomes exp(-u)(h_i + 2 n_i(u)). The coefficient two and its sign match the chosen divergence convention.

When the first three normals form a frame, their directional equations determine a unique smooth one-form beta. A common conformal solution exists precisely when beta = du and every additional foliation satisfies the same evaluation equation. A potential is unique up to a constant on each connected component. Closedness alone is insufficient; the vanishing of all loop periods supplies global exactness. The path-integral proof is valid on a connected manifold, which is path-connected because manifolds are locally path-connected. For disconnected manifolds it is applied componentwise.

For the displayed torus metric, sqrt(det g0) = exp(b), so h1 = b_x, h2 = 0, h3 = 0. Thus beta = -(b_x/2) dx and d beta = (b_xy/2) dx wedge dy. The coefficient at the origin is 2 pi^2. The failure is genuinely within the chosen conformal class, while the same coordinate foliations are flat-minimal. No unrestricted obstruction follows.

## 7. Route 5: positive families, credit, and gluing

The determinant-one horizontal metric has volume dx dy dz. Each coordinate normal has zero divergence. For ker(p dx + q dy), the stated metric-dual unit normal has coefficients depending only on z and has no z component, so its divergence is zero. Reducing the pair to a primitive pair gives connected torus fibers; a coordinate integral circle with nonzero evaluation is a closed transversal meeting every fiber. The horizontal fibration has a vertical transversal. Infinitely many distinct slopes therefore give a genuine infinite simultaneously minimal taut collection.

The recent literature is accurately credited and limited. Nguyen's Theorem 1.2 concerns a determinant-normalized one-variable family of torus metrics and constructs calibrated fibrations in every primitive codimension-one class. His note identifies the overlap with Marques–Neves–Sun. It does not say arbitrary preassigned taut foliations on arbitrary three-manifolds can be simultaneously realized. The observed arXiv v2 is a preprint revised 22 September 2026; no journal status is inferred. [Nguyen, Theorem 1.2 and note](https://arxiv.org/html/2608.18428v2)

Marques–Neves–Sun's Theorem 5.1 uses the cofactor tensor G = det(g)g^(-1) and a one-variable block ansatz. Its primitive-class conclusion likewise supplies suitably constructed torus foliations. The packet's reference to an overlapping cofactor formulation is correct; it does not confuse this G with an arbitrary prescribed original metric. The observed v1 is a preprint submitted 15 August 2026. [Marques–Neves–Sun, Section 5](https://arxiv.org/html/2608.15376v1#S5)

The arithmetic-average counterexample checks out exactly. Both input metrics make the horizontal tori minimal. Their average has horizontal area density A = (a + a^(-1))/2 and unit normal partial_z, giving h = A'/A. At the stated point, A = 5/4 and A' = 3 pi/4, hence h = 3 pi/5. Averaging can therefore destroy even one common minimality constraint. This defeats naive convex metric gluing, not every possible structured gluing construction. Partition-of-unity closed-form gluing also has derivative terms, as stated.

Bibliographic corrections were separately checked: Sullivan's 1979 minimal-surface characterization is distinct from his 1976 cycles article, and Hass's 1986 paper is sole-authored. [Sullivan's publication list](https://www.math.stonybrook.edu/~dennis/publications/), [Hass's publication list](https://www.math.ucdavis.edu/~hass/Research/HassPublicationsGrouped.pdf)

Barbot–Fenley–Potrie explicitly use minimality to mean density of leaves, so that source cannot silently supply a mean-curvature-zero result. Only this terminology distinction was checked, not all of its proofs. [Primary terminology](https://arxiv.org/html/2501.14489v2)

## 8. Reproducibility defect and correction

The archive records regular files with Unix mode 0444. A frozen-layout execution of the original `test_bootstrap.py` fails in every Python optimization mode at the first attempted mutation. `copy2` and `copytree` preserve those nonwritable modes; the test then appends a byte to the first copied payload. This is a fixture-construction defect. It does not invalidate the authenticated mathematical payload or the direct bootstrap's positive runs. The stored original `REPLAY.json` is not a reproducible claim about that exact read-only extracted layout without the correction.

`HARNESS_CORRECTION.patch` adds one comment and a two-line loop immediately after fixture creation. The loop sets only newly created private fixture directories to 0755 and files to 0644. The harness subsequently imposes 0555/0444 itself for the dedicated read-only test. It never changes the author source layout. The corrected outer harness hash is:

`53d2f1cc91ba3b77d5b350efc66ef6c71a0632f7c5db5339f7a595260509dc85`.

The original outer harness hash remains:

`582fd716a9b52d2b81a19acab2d01b9135c3004b2f37ed9cae95c2deb48a0cd7`.

Because this is an outer harness change, it does not change the authenticated nine-file author payload or its manifest. A newly distributed corrected archive would nevertheless need its own fresh archive receipt. This audit supplies a sidecar patch and full corrected harness, not a silently replaced author archive.

## 9. Independent controls and limits

`independent_verify.py` accepts the immutable author ZIP and performs these checks without importing the author's verifier:

- Exact archive/member trust anchors, safe unique member paths, no archive symlinks, manifest inventory and payload hashes.
- 917 exact-rational finite cases: cofactor reconstruction and frame covariance (125), scaled characteristic-form compatibility (27), positive trace pairings (600), calibration squeezes (25), conformal frame solves (125), and averaged area/divergence identities (15).
- Twelve explicit algebraic boundary checks, including nonsymmetric/indefinite compatibility matrices, dependent frames, sign restrictions, saddle Hessian trace cancellation, and the closed-versus-zero-period distinction. These are deliberately finite illustrations, not executable topology or PDE proofs.
- Direct authenticated bootstrap execution in normal, `-O`, and `-OO` modes on a relocated, genuinely read-only package; an attempted write is denied and byte snapshots stay unchanged.
- Reproduction of the original frozen-harness permission failure in all three modes.
- Corrected-harness execution in all three modes from a read-only package. Each run supplies six positive layout/mode runs and 78 rejected integrity mutations, with identical output. The authenticated author diagnostics separately report 916 finite algebra cases and 50 wrong-claim/malformed controls.
- Thirty independently selected hostile/malformed bootstrap runs: ten cases in three modes. These include malformed manifests, missing/symlinked proof files, extra payload, replaced executable code, malformed/duplicate-key/truncated claims, wrong isotopy claims, and a self-consistent manifest forgery. All are rejected before unauthenticated code runs. Integrity rejection does not claim that every case reached a JSON schema parser.

The independent outer harness is itself run under normal, `-O`, and `-OO`; results and byte-identical-output checks are recorded in `INDEPENDENT_REPLAY.json`. No `assert` statement is needed for rejection behavior. Test success is local replay, not GitHub CI, a proof assistant certificate, or human peer review.

## Final acceptance scope

The original `PROOF.md` is accepted unchanged as a careful five-route partial investigation under its stated assumptions. Route 3 survives independent isotopy; Routes 1 and 4 are restricted exact reductions; Route 2 supplies only a fixed-representative obstruction; Route 5 supplies special positive families and a concrete gluing failure. The source question remains unresolved by this work. Operational acceptance of a frozen-layout mutation replay requires the supplied harness correction or an equivalently verified fixture-permission fix.
