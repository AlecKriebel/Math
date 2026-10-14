# Independent audit: Chebyshev–Nahm family and ordinary Bloch information loss

## Verdict

**ACCEPTED AS A SCOPED, KNOWN FAMILY-LEVEL RESULT.** The Chebyshev–Nahm family argument is mathematically sound with its stated limitations. The original AIM Problem 2.4 remains unresolved by this argument. No novelty, exact torsion order, arbitrary Bailey-pair dictionary, or general Nahm modularity equivalence is accepted or claimed.

The complete reconstruction is `STANDALONE_PROOF.md`. This audit makes the ordinary Bloch-group convention, its possible diagonal 2-torsion, and the complementary-variable convention precise. These clarifications support the conclusions rather than repair a false identity in the argument.

## Result identification and review scope

- Problem ID: 20000735; source key: AIM-ANALYTIC_NUMBER_THEORY-0099.
- Reviewed result: the concrete Chebyshev/Nahm family and its lost terminal parameters, reconstructed in full in `STANDALONE_PROOF.md`.
- The proof and cited reference inputs were independently reviewed. No source-author code was run.

## Claim-by-claim acceptance

1. **A_ij = 2min(i,j): accepted.** A=2LL^T for lower-triangular L with all entries on/below the diagonal equal to one. The ordering is important: L^TL is a different displayed matrix. The associated tadpole matrix T_r has diagonal 2,…,2,1 and neighbor entries −1; T_r A=2I, including r=1.
2. **Chebyshev coordinates: accepted.** The sine formula and recurrence are compatible; u_i²−u_{i−1}u_{i+1}=1, u_0=1, and u_{r+1}=u_r. For 1≤i≤r, (i+1)θ lies strictly between θ and π/2, so u_i>1. Consequently x_i=1−u_i^(−2) is in (0,1).
3. **Tail telescope and Nahm equations: accepted.** The unsimplified tail is u_{i−1}u_{r+1}/(u_i u_r); the terminal equality makes it u_{i−1}/u_i. Successive ratios match those of 1−x_i. x_0=0 is an auxiliary starting value, not a new Nahm coordinate.
4. **Positive-solution uniqueness: accepted.** The gradient of (1/2)t^TAt+ΣLi_2(e^(−t_i)) is At+log(1−e^(−t)), and its Hessian is A+diag(1/(e^t_i−1)). This is strictly positive on the convex positive orthant. Explicit existence is separate. The proof does not assert uniqueness of all complex solutions.
5. **Totally real field: accepted.** K=Q(cos(π/(2r+3))) is a subfield of a cyclotomic field fixed by complex conjugation, with all embeddings real. Polynomial Chebyshev expressions put all u_i and x_i in K. Only the distinguished embedding is asserted to put x_i in (0,1); other embeddings need only be real.
6. **Ordinary Bloch boundary: accepted.** In an alternating exterior square, symmetry suffices. In the integral antisymmetric tensor quotient used by Suslin/Garoufalidis, diagonal terms can be 2-torsion, but the diagonal coefficients A_ii=2i kill them. Off-diagonal terms cancel in pairs. Thus the element lies in the ordinary Bloch group without rationalizing the boundary.
7. **Torsion: accepted with established theorem dependency.** Rank B(K)=r_2(K)=0 gives torsion because tensoring an abelian group with Q kills exactly its torsion elements. The primary Borel/Suslin route and Zagier's explicit rank statement are pinned. This does not require identifying Lee's quotient with the chosen integral ordinary group and does not compute an order.
8. **Andrews–Gordon parameters and noninjectivity: accepted.** Expanding the tails gives (1/2)n^TAn+Σ_i max(0,i−a+1)n_i. For a<b≤r+1 the allowed-parts products first differ at part a. Their coefficients agree below a, and the b-series coefficient at q^a exceeds the a-series coefficient by one. These are unshifted C=0 series. All share the same A-dependent distinguished solution and class.

## Source-convention and source-equation cautions

### Lee's variables and group

Theorem 1.3 of arXiv:1109.3667v3 concerns C(X)⊗C(X′)^(-1) for ADET diagrams, and the present matrix is C(A_1)⊗C(T_r)^(-1). Lee writes y=(1−y)^A, so his coordinate is y_i=1−x_i=u_i^(−2). His Definition 2.1 rationalizes the exterior-square target and imposes complementary-symbol and inverse-symbol relations. In his quotient, complementary sums are negatives. In the ordinary group one has instead [z]+[1−z]=c_K with 6c_K=0, so the two sums differ from negatives by r c_K. Neither equality of integral groups nor equality of exact orders is inferred.

### Ordinary versus extended Bloch groups

Garoufalidis Definition 3.1 retains logarithm-branch parameters in [z;p,q]. The present proof constructs an ordinary symbol sum and no choice of an extended lift. The demonstrated information loss therefore concerns only this ordinary A-dependent assignment. It does not prove that all extended, cyclic, or root-of-unity refinements lose the same information.

### No broad modularity equivalence

The 2010 AIM discussion is historical context. Lee's 2011 introduction explicitly notes counterexamples to the original broad Nahm conjecture. The accepted argument uses no torsion-implies-modularity theorem. The original problem's Bailey and general orthogonal-polynomial program is not settled by this family.

## Independent exact diagnostics

The independent diagnostic checker uses rational/integer arithmetic and SymPy's exact polynomial operations. It executes no downloaded code. All tests use explicit exceptions rather than assertions, so optimization cannot remove them.

- Ranks 1–12: algebraic identities are checked in Q[z]/(Φ_(2M)(z)), with z a primitive 2M-th root of unity and u_i represented by the Laurent sum z^i+z^(i−2)+⋯+z^(−i). Modular inverses give exact rational functions, without floating-point trigonometry.
- For each rank: the terminal condition, sine identity, complementary x expression, every tail telescope, every Nahm equation, A=2LL^T, and T_r A=2I are checked exactly.
- Every endpoint for these ranks: expansion of quadratic and linear exponents is verified symbolically.
- Ranks 1–8: all 44 companions are independently computed from the multisum and allowed-parts product through degree 48. The multisum enumeration uses 7,721 admissible terms across all cases; terms omitted by the quadratic lower bound cannot affect the truncation.
- All 120 pairs a<b in those ranks pass the exact first-difference test.
- Three negative controls reject complementary-variable substitution in the original rank-one equation, collapsing distinct terminal products, and reversing the Cholesky factor order.
- Normal Python, `-O`, and `-OO` all pass with identical mathematical output. The initial checker construction raised a SymPy Boolean-to-int implementation error; that error was corrected before all three successful runs and changed no mathematical claim.

These finite diagnostics are not proofs for arbitrary rank and do not test a torsion order or a modularity criterion. The arbitrary-r proofs are provided separately. `CHECK_SUMMARY.json` records the bounded scope and aggregate outcomes. Exact coefficients, per-case computational output, and checker code are excluded from this packet.

## Source capture and inspection

`SOURCE_PINS.json` records public URLs, document sizes, SHA-256 hashes, version information, and the actual reading/rendering scope. The AIM, Kirillov, Lee, and Garoufalidis reference PDFs were checked as byte-identical copies of previously retrieved public captures. Suslin, Borel, and Zagier were additionally retrieved and the relevant theorem pages inspected.

The Kirillov dependency is specifically Theorem C, equation (2.1.a), printed/PDF p.34, with N_i defined on p.35.

The Borel download initially timed out after 2,847,726 of 3,872,332 bytes; an ordinary HTTP range resume completed the same public document. The attempted original Andrews PDF open through PMC returned a browser/reCAPTCHA page; no CAPTCHA was solved and the PDF is not counted as inspected. The required identity is supported by the inspected Kirillov equation (2.1.a). These limitations are retained rather than silently reported as successful source reading.

This packet contains the authored proof, complete mathematical audit, acceptance report, public-source metadata, and aggregate verification summaries. It excludes copied source documents, page images, extraction text, raw computational output, and checker code.

## Acceptance boundary

The argument is accepted for this explicit positive solution, its ordinary torsion class, and terminal-choice noninjectivity. The source problem stays open at its original breadth. Established results are credited; no claim of firstness is attached to the packaging or coefficient observation.
