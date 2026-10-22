# Exact elimination and dominance audit — PR212 / 30005310

**Algebraic verdict: verified for both stated K4,4 colorings. No mandatory mathematical repair found in the elimination/dominance portion.** This is a scoped mathematical audit, not blanket clearance of historical priority, the complete statistical argument, source interpretation, or publication readiness.

## Strongest independently established claims

For the source's exact real polynomial elimination ideal, with all rank minors of the full symmetric covariance matrix and with the stated color-sum statistics, both the singleton-colored K4,4 and the variant whose only nontrivial color class is the vertex pair {1,2} satisfy

    I(G,3) != (0),    I(G,4) = (0),    pi_G(I_8) in V_R(I(G,3)).

The graph's concentration model and the statistic map match Definition 1 and the preceding model definition in the official report. In particular, a color equality on concentration diagonals merges their covariance statistics by addition; it does not impose a covariance-diagonal equality. Both vertex-color partitions and the 16 singleton edge classes meet the report's declared class, and I_8 is a feasible concentration matrix. No additional group-symmetry or edge-regularity requirement appears in that definition. The projection sums each edge once. A factor 2 from an alternate trace-pairing coordinate convention is invertible; a common positive sample-covariance normalization is a simultaneous scaling. Neither changes the checked claims, and neither is silently inserted into the source's coordinates.

The four-by-four cross determinant is a nonzero statistic polynomial, remains available after the vertex-color merge, and is exactly a permitted nonprincipal four-minor. The independent derivation gives its ideal-membership certificate as the sum of that minor and a telescoping combination of the linear statistic relations. Thus the argument proves membership in J intersect R[t], not merely vanishing on a finite collection of rank-three examples.

## Independent derivative and exact-ideal proofs

Before inspecting any inherited reviewer or checker, I reconstructed a linear right inverse for the full derivative at U=I_4 and V_j=e_j+e_(j+1), cyclic indices. Given arbitrary target left diagonals a, right diagonals c, and cross block H, set

    D_ii = a_i/2,
    D_(j,j+1) = (VH)_jj − (a_j+a_(j+1)+c_j)/2,
    all other off-diagonal entries of D = 0,
    E = H^T − V D^T.

Then the cross differential is DV^T+E^T=H, the left differentials are a, and each right differential is

    2(VH)_jj − 2 v_j D v_j^T = c_j.

The four cyclic ordered entries have different unordered supports. This checks the wraparound pair (4,1), both mixed transposes, and every cross and diagonal output. It is not a dimension-count argument. The singleton derivative has shape 24 by 32, rank 24, and kernel dimension 8. Merging the first two diagonal statistics gives a projection P with an explicit section L, so P dPhi R L=identity_23 and the tied derivative has rank 23 and kernel dimension 9.

The submitted real-open-image argument is sufficient even if one makes no radicality assumption: every member of the actual elimination ideal evaluates to zero on every Gram image, since the substitution kills every generator of J. A polynomial vanishing on a nonempty real open set is zero. Complex coefficients cause no issue because real and imaginary parts vanish separately.

I also supplied a second proof avoiding any image/variety equality or topology. The exact linear lift gives

    Phi(X0+R(Y)) = t0 + Y + Q(Y),

with Q homogeneous quadratic. For any nonzero f, the lowest nonzero homogeneous component of f(t0+Z) survives substitution Z=Y+Q(Y). Hence the statistic polynomial pullback is injective. Since the pullback kills every elimination-ideal element, I(G,4) must be exactly zero. The tied model admits the same argument through L. This is an argument about the ideal itself; it does not replace the ideal by its radical.

No equality between real images and Zariski closures, no positivity of every real zero, and no identity between generic completion rank and maximum likelihood threshold is needed. The formulas are rational and also prove the corresponding coefficient-extended claims over C. A rank-four PSD Gram submersion is sufficient even though the source determinantal locus additionally includes indefinite matrices: it provides a subset on which each elimination-ideal member must vanish.

## Falsification probes and boundaries

V itself is singular of rank 3, and its observed cross determinant at the chosen point is zero. U=I still gives rank(X0)=4. No step divides by V, its determinant, an output, or a row norm. As a separate control, U=V=I gives a rank-four PSD Gram matrix with cross determinant 1, so the rank-three obstruction is not an identity on the rank-four image. At X=0 the derivative is zero, and at U=V=I its rank is only 20. These are handled boundary points, rather than evidence that an arbitrary Gram point is a submersion.

I checked all 3,136 five-by-five minors at the exhibited Gram point, including all 56 principal ones. The universal proof remains the four-column factorization/Cauchy–Binet argument. Principal-only replacement would be materially different for arbitrary real symmetric matrices: the eight-by-eight matrix with diagonal 1 and every off-diagonal entry −1/(k−1) has rank 8 and all principal k-minors zero, for k=4 or 5. Its indicated nonprincipal minors are −64/81 and −625/1024. These exact negative controls ensure the audit did not silently replace full minors by principal minors or restrict the source ideal to PSD matrices.

The positive-definite intersection uses the explicit PSD preimage diag(J_4,J_4), of rank 2, with the same statistics as I_8. Therefore every member of I(G,3) vanishes at pi_G(I_8), including for the tied model. The inference uses an actual preimage, not a general assertion about real points of an elimination variety. Consequently no ideal member can be nonvanishing everywhere on the positive-diagonal Cholesky domain, because I_8 belongs to that domain.

## Computation and binding

The independent derivation was frozen at 2026-10-15T09:41:12.568672Z with SHA-256 `0ad18897f6d400c3e0e99a2204a3745a2a8b1ed4425d4a7fd4992ea6f085a722`. The fresh control program was written and its results completed before opening inherited reviewer/checker material. Its 3,333 exact checks passed under SymPy 1.14.0. They include a symbolic right inverse for arbitrary output variables, identity products for both colorings, exact Jacobian minors (256 and 128), the determinant-relation telescope, all five-minors at the Gram point, and the negative principal-only and degenerate-point controls. They corroborate the written universal proof; the finite checks are not its foundation.

I then read the author checker, its receipt, the inherited independent checker, its receipt, and the entire inherited FINAL_REVIEW.md. Neither prior PASS was used as a premise. Both programs ran only from isolated private copies with bytecode writes disabled. The author replay produced the submitted verification.json byte-for-byte, including 188 assertions and the dynamically computed frozen PROOF.md hash. The inherited replay produced INDEPENDENT_CHECKS.json byte-for-byte, including 1,808 assertions.

**Reproducibility limitation:** the inherited checker's `proof_sha256` value is hardcoded. It labels the intended proof and does not itself bind the current proof file. This does not invalidate its algebraic controls, but a future audit should dynamically hash its supplied proof or explicitly call the value a provenance label. My separate binding check verified all 20 frozen native files by byte count, SHA-256, and Git object SHA-1 without invoking Git: all 55,337 bytes matched the intake. No original or root output was changed.

## Reading/provenance coverage and remaining scope

Read in full: submitted PROOF.md; the official Homs–Kuznetsova contribution printed pp. 3146–3149, including rendered PDF pages 26–29; both checkers and their result receipts; inherited FINAL_REVIEW.md after freezing the independent derivation; intake and root retrieval metadata. The official 600,619-byte PDF matches SHA-256 `56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65`. A private copy, extracted full text, rendered pages, copied replay inputs and raw outputs remain under private/. Other frozen native files were read as bytes for binding, not all interpreted as substantive evidence. The source-record statement was inspected for context but supplies no algebraic premise beyond the official report.

The strongest verified result is the exact algebraic triple stated at the start for both colorings. The exact remaining gap **within this algebraic task is none**. I did not independently audit the complete-bipartite MLT literature theorem, the full probability/likelihood argument, or whether refuting a numerical conclusion of Proposition 3 is the right resolution of a separately repaired Boolean Conjecture 4. Those questions require the other audit families. In particular, algebraic validity alone does not resolve the source-scope decision. No publication, tracker, PR, Git, queue, cache, or database mutation was performed, and no other individual was contacted.
