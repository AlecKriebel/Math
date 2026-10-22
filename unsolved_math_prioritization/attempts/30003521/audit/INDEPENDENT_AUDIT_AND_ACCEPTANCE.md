# Independent adversarial audit: quadratic graph NLS partial

Problem 30003521 / OWR-15437-003, rank 867. Audit date: 6 October 2026.

## Decision

**Accept the authored mathematics as a bounded partial result. Reject the original assertion-based integrity bootstrap as optimization-safe. Accept the separately pinned corrected derivative and fail-closed replay bootstrap. The original open problem remains unsolved.**

No mathematical correction is required. The entire original `PROOF_AND_STATUS.md` is unchanged, SHA-256 `fdb8b5e806929452e089388e932593d3b26a3ab9a93b10105191f1d14ee07ed5`. The correction changes the finite identity checker's failure guard and its external integrity bootstrap. It does not expand the five-approach investigation, establish novelty, or turn the partial obstruction into a solution.

The original report's `STATUS.json` is preserved as a historical author snapshot, including its then-pending audit field. This document supplies the independent acceptance decision for the corrected release. No publication was performed during this audit.

## Pinned objects and prior-attempt gate

The original archive has 11,449 bytes and SHA-256 `439c6e19b62f6e75843b3c84955600842488aa8e49b8f4c5b91eed52ee64542a`. Its external manifest SHA-256 is `7761f7a28c02e251d926f37ddfc5d51e3bfb326a3d1eb89e4544eee507b10f66`. The audit first checked those external anchors and every member's byte count and hash without running payload code.

The complete catalog, problems, and research-results corpora independently matched the supplied hashes. The exact catalog entry is rank 867. The full problem record and inherited report, serialized by the prescribed sorted-key JSON rule, matched SHA-256 `60cb3f3a125818baf6ad22d92111951b952fffd5277c7b84d06b702d1cd867b5`. The inherited report is the empty object, not a substantive prior proof. `CORPUS_HASH_REPLAY.json` gives only verification metadata, with no dataset contents.

Fresh repository searches for the ID, problem number, default-branch occurrence, and matching branches found no indexed prior attempt. These bounded searches do not establish absence from every historical revision. Primary-source details and limitations appear in `INDEPENDENT_SOURCE_AUDIT.json`.

## Mathematical audit

### 1. Exact operator domain and multiplication

The operator is the positive Kirchhoff realization of `L = -d²/ds² + 1`. A finite periodic quotient yields finitely many positive edge-length types, hence uniform one-dimensional Sobolev constants. The edgewise H² direct-sum norm is equivalent to the graph norm: control of `u''` follows from `Lu` and `u`, and interpolation controls `u'` uniformly.

The proof that D(L) is an algebra is valid. Edgewise multiplication estimates sum in ℓ² because the sum of products of nonnegative squared edge norms is bounded by the product of their sums. Continuity of the two factors makes the vertex flux of their product equal to the common value of each factor times the other's zero flux sum. This includes complex conjugation and counts both endpoints of a loop. The result is correctly identified as already used in the literature.

For D(L²), the stated conditions are exact: edgewise H⁴, common traces of `u` and `u''`, and vanishing sums of outgoing first and third derivatives. For `u,v` in this domain, the only term in `(uv)''` that need not have common traces is `2u'v'`. The third-derivative flux automatically vanishes because the traces of `u,v,u'',v''` are common. Thus the displayed slope-product criterion is genuinely both necessary and sufficient. There is no omitted third-derivative compatibility condition.

The compactly supported endpoint construction with slopes `(1,-1,0,...)` is valid at a vertex of degree at least three. Smooth cutoffs can be supported on pairwise disjoint endpoint segments, including loop endpoints. Near the selected vertex each `L^m u` equals the same linear profile; at every other vertex all jets vanish. Therefore the function lies in every positive integer power-domain. Its square has unequal `L(u²)` traces `(-2,-2,0,...)`, so it fails D(L²). The obstruction concerns operator-domain multiplication, not lack of edgewise smoothness or failure of local quadratic evolution in D(L).

### 2. First-order reduction, divisors, and correctors

Differentiation of `z_sigma = (u - sigma i Omega^(-1)u_t)/2` gives exactly the stated quadratic coefficient `-sigma i eta Omega^(-1)/2`. For `w = z + B(z,z)`, the quadratic homological term is `i Phi b`, where `Phi` is the sum of the two signed input frequencies minus the signed output frequency. The sign and factor in `b = sigma eta c/(2 omega_j Phi)` are correct under the report's ordered bilinear convention.

The quasiperiodic fiber convention adds phases under multiplication. At second order, the frequency-2ω and frequency-zero terms consequently yield the displayed equations with forcing `eta f²` and `2 eta |f|²`. The zero-frequency equation is invertible since L is at least the identity. A nonzero projection of `f²` onto the second-harmonic kernel makes the other equation unsolvable by self-adjointness.

The report does not promote pointwise nonvanishing divisors into an infinite-band operator bound. Its distinction between finite carrier-generated correctors and carrier/error interactions with every relevant sign is essential and correct. No infinite-band summability, parameter regularity, or domain-preserving normal-form theorem has been established.

### 3. Necklace graph, simple carrier, and coupling

All edge orientations and four displayed quasiperiodic vertex equations are consistent. Substitution of `cos(a)=1/3` and `sin(a)=2sqrt(2)/3` gives the claimed endpoint values and derivatives. In particular the outgoing sign at a right endpoint is properly accounted for in the displayed forward-derivative flux equations.

The exchange of the two parallel arcs is a symmetry of the full fiber operator. In the antisymmetric sector the link vanishes and the arcs have zero endpoint values, so a nonzero eigenmode at wavenumber q requires `q ell` to be an integer multiple of π. The carrier value `a=arccos(1/3)` is excluded from that set.

In the symmetric sector the forward-flux state gives the product matrix

`T2 T1 = [[-1/3, sqrt(2)/3], [-2sqrt(2)/3, -5/3]]`.

It has determinant 1, trace -2, and `T2 T1 + I` has rank one. Thus the antiperiodic eigenspace is one-dimensional. The absence of an antisymmetric mode proves simplicity in the full compact self-adjoint fiber. A nontrivial Jordan structure of the transfer matrix is not a Jordan structure of the self-adjoint differential operator; it causes no flaw in this eigenspace argument.

The periodic profile g satisfies the vertex conditions and `L(0)g=(1+pi²/ell²)g`. The exact choice `3ell²=pi²-4a²`, with positive ell, gives `1+pi²/ell²=4(1+a²/ell²)`. The chosen mass term stays +1. This is a change of graph length, not an unacknowledged conversion of the fixed π-length model.

The inner product uses both parallel arcs. Since each arc component of g is minus one half of the link sine profile, the integrand reduces to `(f0²-fplus²) sin(pi s/ell)`, with no missing factor of two. The centered-coordinate identities in the report are exact. Inside the cell `cos(2ay)>1/3` and `cos(pi y)>0`, so the integrand is strictly negative. Direct integration gives

`<g,f²> = -6 ell a² / [pi(pi²-4a²)] = -2a²/(pi ell)`,

which is nonzero. Rescaling f and g to unit norms does not change nonvanishing. Simplicity of the harmonic eigenvalue is unnecessary; one nonorthogonal kernel vector already proves incompatibility. The Fredholm contradiction is therefore valid.

This is an exact fiber obstruction on the specified rescaled graph. A Bloch eigenfunction on an infinite periodic graph is not thereby localized L² initial data. The report correctly does not claim a localized-wave-packet failure theorem, a result for the conventional fixed π-length graph, or failure for every carrier.

### 4. Conditional long-time stability

On the error bootstrap `||w-w_a|| <= epsilon`, the displayed cubic Lipschitz assumption bounds the nonlinear difference by `K(2C_a+1)² epsilon² ||w-w_a||`. Integrating an `epsilon^(p+2)` residual up to `T/epsilon²` produces `T epsilon^p`. The bounded linear group and Gronwall then give precisely the report's constant, and `p>1` improves the bootstrap for small epsilon.

This argument is valid as a conditional lemma, with local well-posedness/continuation and the variation-of-constants formulation available. The report explicitly leaves these hypotheses, the invertible quadratic transformation, the residual construction, and the choice of wave-packet-adapted norm to be proved for the graph problem. They cannot be inferred from the lemma itself. The warning that an unscaled L²-based packet norm need not be O(epsilon) is also correct.

## Source reconciliation

The complete OWR contribution on printed pp. 1856–1858 was read and visually inspected. It explicitly leaves the quadratic graph extension open and relates the obstacle to vertex regularity and normal-form analysis. It does not supply a complete quadratic Cauchy problem or a theorem covering arbitrary resonant carriers. [1]

The 2016 publisher abstract concerns an original NLS evolution. [2] The graphene paper's actual domains, local-existence argument, and complete NLS-justification argument were inspected in the saved author preprint. Publisher Theorem 7.1 has carrier simplicity and third-harmonic conditions (7.7)–(7.8); Remark 7.2(c) retains the quadratic case as open. Its use of an L¹-based Bloch control norm alongside the L²-based error norm supports the report's scaling warning. These are not quadratic normal-form estimates. [3]

The 2026 paper explicitly sets its original evolution to focusing cubic graph NLS, equation (1.3), and studies traveling pulses by spatial dynamics. It does not settle this quadratic graph-wave question. [4] Bounded fresh searches located no resolving result, but no exhaustive literature-absence claim is accepted.

The previously cancelled retrieval session was not retried. The already-complete saved preprint was rehashed and inspected locally. Source PDFs, extracted text, rendered images, and datasets are excluded from this audit release.

## Integrity defect, actual patch, and acceptance

The original external bootstrap uses `assert` for its manifest hash, archive hash/size, member validation, and checker-result guards. Python optimization strips all those assertions. In a temporary copy, replacing only the archive's checker with a harmless script returning an unmistakable JSON sentinel, while retaining the original external manifest, produced:

- Normal isolated interpreter: rejection before the sentinel ran
- Optimized isolated interpreter: sentinel ran and the bootstrap returned success

Thus the original bootstrap's broad pre-execution integrity claim is not optimization-safe. This is an execution-integrity defect, not a mathematical counterexample. The original finite checker also used an assertion for its all-identities guard.

`FAIL_CLOSED_CORRECTION.patch` is an actual unified patch. The corrected checker raises explicitly on a false identity. The corrected external bootstrap uses explicit runtime checks, fixed allowed names, duplicate and symlink rejection, declared and actual sizes, member hashes, and strict returned-checker validation. It parses the already-hashed archive bytes rather than reopening a mutable path. The release still depends on a separately trusted bootstrap and is invoked with Python `-I -S`, optionally `-O`.

The corrected archive is 11,483 bytes, SHA-256 `dbf1da376f6f7cb0a0df9dee55c43986b6a6911905b65fe30518c8cfa6d51a67`. Its manifest SHA-256 is `05386fd90e97e008c580fe90fc1fbffe7cf037a20bde7541085eedadbc6fabfc`; bootstrap SHA-256 is `3ec6ce36e3e69d6aefb9221cea0f801c57520ccd8f8bbfe810f1b304cf880706`.

The final independent replay has 46 expected outcomes across normal and optimized interpreters: intact relocated baselines, poisoned working-directory/import environment, stale pins, same-size and changed-size archive modifications, duplicate/missing/extra members, bad member sizes/hashes, symlink members, invalid manifest names, and false checker results. The corrected checker also rejects a deliberately false identity under both modes. To test inner validation layers, diagnostic copies explicitly reanchor only the outer layers; none of those copies is an accepted release. All fixed-pin corrected release mutations were rejected. See `ADVERSARIAL_REPLAY.json` and its reproducer.

**Explicit acceptance:** the separately pinned corrected derivative is accepted for the bounded mathematical and finite-verification claims above. The unchanged original mathematical report is accepted as a partial. The original assertion-only replay bootstrap is not accepted as optimization-safe. The 11 finite rational identities are supplementary checks, not a PDE verifier. The open approximation theorem, its infinite-band analytic estimates, and any localized-data failure result remain unproved.

## Public references

1. Guido Schneider, “The NLS approximation for dispersive systems on graphs,” Oberwolfach Report 29/2017, pp. 1856–1858. https://doi.org/10.4171/owr/2017/29 ; publisher PDF https://ems.press/content/serial-article-files/46690
2. Steffen Gilg, Dmitry Pelinovsky, Guido Schneider, “Validity of the NLS approximation for periodic quantum graphs,” NoDEA 23 (2016), article 63. https://link.springer.com/article/10.1007/s00030-016-0417-7
3. Steffen Gilg, Guido Schneider, Hannes Uecker, “Nonlinear dynamics of modulated waves on graphene like quantum graphs,” Mathematische Nachrichten 295 (2022), 2147–2170. https://onlinelibrary.wiley.com/doi/10.1002/mana.202100009 ; author preprint https://pde2path.uol.de/hu/pre/070-graphene.pdf
4. Stefan Le Coz, Dmitry E. Pelinovsky, Guido Schneider, “Traveling Waves in Periodic Metric Graphs Via Spatial Dynamics,” Journal of Dynamics and Differential Equations (2026). https://link.springer.com/article/10.1007/s10884-026-10490-6
