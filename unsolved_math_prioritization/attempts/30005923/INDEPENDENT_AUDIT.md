# Independent acceptance audit: row-ball moments and determinant covariance

Date: 8 October 2026. Targets: 30005923 and 30005922.

## Verdict

**Accept the authored fixed-parameter proof reconstruction, with the seven disclosed source repairs. Keep target 30005923 on HOLD for tuple-count uniformity. Credit prior-result coverage of target 30005922 in the exact fixed finite-parameter domain.**

No mathematical correction to `original/FIXED_G_PROOF.md` is needed for these conclusions. `PROOF_INTERFACE_ADDENDUM.md` makes several compressed interfaces explicit, especially the pure-power case of the Gaussian input. A reproducibility correction is supplied separately: `verify_audit.py` reads and reports to stdout without rewriting any packet file. The original verifier is preserved unchanged.

This is a zero-new-research-turn verification. It does not solve the all-g bound, search for a new proof of it, claim novelty, certify the entire three-author manuscript, or alter a repository or queue.

## Material inspected and source identity

Both authored mathematical files were read in full. All six entries in their manifest matched their declared SHA-256 hashes and byte counts. All seven public-source metadata entries matched the retained primary PDF or TeX archive bytes. The relevant primary proof chain was inspected:

- OWR 22/2024, Jury's contribution pp. 1270–1272; Lemma 9, Conjectures 10 and 12, and the displayed conjugations and quantifiers. Printed p. 1272 was visually inspected. [Official report](https://ems.press/content/serial-article-files/49482).
- Jury–van Rensburg–Roman, *Free versions of the strong Szegő limit theorem*, arXiv:2607.25980v1, the relevant notation, concentration and coefficient arguments, Sections 5 and 6, and the source of the missing determinant. The proof of Proposition 6.1 on printed p. 24 was visually inspected and checked against the TeX. [Version-pinned manuscript](https://arxiv.org/pdf/2607.25980v1).
- Parraud, arXiv:2005.13834v2, Theorem 1.1 and the coefficient-uniformity remark after Theorem 4.1. [Primary paper](https://arxiv.org/pdf/2005.13834v2).
- Meckes–Meckes, arXiv:1210.2681v3, Corollary 17 and its product Hilbert–Schmidt metric. [Primary paper](https://arxiv.org/pdf/1210.2681v3).
- Mingo–Śniady–Speicher, arXiv:math/0405258v2, Theorem 3.13, Corollary 3.14, and Remark 3.8 for pure powers. [Primary paper](https://arxiv.org/pdf/math/0405258v2).
- Jury–Roman, arXiv:2506.04400v1, Proposition 3.5 and its explicit normal-family uniqueness argument. [Primary paper](https://arxiv.org/pdf/2506.04400v1).
- Pisier, *Introduction to Operator Space Theory*, Theorem 9.7.4, printed pp. 187–189, including direct visual inspection of printed p. 188 (PDF page 197). The exact operator-valued inequality and the split-matrix definition agree with the reconstructed input. [Book copy hosted by Northeastern](https://bpb-us-e1.wpmucdn.com/sites.northeastern.edu/dist/4/7815/files/2024/07/Pisier.pdf).

The arXiv abstract page inspected on the audit date lists only v1 of the three-author manuscript and no journal reference. This verifies the narrow public-status statement, not an exhaustive assertion about unpublished acceptance. The two-author paper's separate JFA record is confirmed by the publisher's result: volume 291, issue 6, article 111555, 15 September 2026. It is not publication evidence for the three-author manuscript. [Three-author version record](https://arxiv.org/abs/2607.25980v1); [two-author publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0022123626002193).

The original Buchholz paper was not retrieved in full. Its operator-valued input was checked directly in the cited Pisier theorem, rather than relying on a title, search snippet, or the three-author paper's attribution. Historical input theorems are used as established results; their full proofs are not certified here.

## Literal target scope

OWR's Haar measure is probability measure. Its abbreviation A tensor U is a sum over the tuple coordinates, and its row norm is the square root of the norm of sum A_j A_j*. Matrix sizes of the two companion representations may differ.

OWR Lemma 9 requires the representations used to define a stable polynomial to have coefficient row norm strictly below one and to give determinant equality for every finite matrix tuple. Thus substituting Haar unitaries into those representations is legitimate; no unstated assertion of arbitrary determinantal representations is needed. Conjugation of the second determinant and coefficient tuple is indispensable.

OWR Conjecture 12 writes C(r,k) and quantifies over all d-tuples. The accepted reconstruction explicitly fixes g and produces C(g,k,r,m). It does not bound those constants as g changes. Renaming d or suppressing g in a constant's notation does not change the quantifiers. The optional proposed constant and monotonicity are not accepted.

## Audit of the seven source repairs

1. **Pointwise ceiling.** The exact scalar witness g=4, X_j=3/8, r=3/4, U_j=1 gives row square 9/16 and pencil square 25/4. It refutes the ceiling 4, not the averaged theorem. The row-column factorization gives the correct fixed-g ceiling (1+r sqrt(g))^2. The cutoff in C covers that entire interval.
2. **Tail integration.** The zero random variable disproves a tail formula lacking the additive one. The corrected exponential tail identity is valid; m=0 is handled separately, and negative m would require |m|. Only nonnegative row-ball moments are accepted here.
3. **Logarithm signs.** The coefficient of log(I+T) is (-1)^(n+1)/n. The positive sum of Tr(S^n)/n is -Tr log(I-S), producing the reciprocal determinant. The reconstruction uses both corrected signs consistently.
4. **Normal-family convergence.** Montel alone gives subsequences. The repaired joint holomorphic product-domain argument supplies local boundedness, identification on an open set, the identity theorem, and uniqueness of every subsequential limit. The final contradiction proves whole-sequence local uniform convergence.
5. **Missing determinant.** The printed Theorem 1.6 integrand is malformed. The second determinant appears in the scalar quotient formula of Theorem 6.2. The audited result uses the latter's unambiguous zero-denominator specialization, reconstructed directly.
6. **Trace normalization.** With normalized tau_k, the FK logarithmic identity has unnormalized factor 2k. The reconstructed derivative argument confirms the relevant value is zero, so this typo does not invalidate the corrected conclusion.
7. **Exact centering.** A Haar commutator has unnormalized expected trace 1/N. Therefore the general mixed-word exact-centering assertion cannot be imported. Positive words and their inverse words are exactly centered by common phase invariance. Those are exactly the words used by the pencil proof.

All seven repairs survive independent derivation. The acceptance does not extend to the manuscript's unrestricted mixed-word coefficient theorem or the complete quotient/rational-function generalization.

## Verification of the full analytic chain

A1/B: The free homogeneous norm bound applies to matrix-valued coefficients. Its split matrices factor with the column first and row second. Iterated completely positive maps identify both row/column power sums. Hilbert–Schmidt adjointness and finite-dimensional vectorization identify their common spectral radius. The epsilon-exponential envelope absorbs all split indices, and nth roots remove n+1. This proves the needed free spectral-radius equality, not merely an upper bound guessed from row norm.

B/C: Strict row norm gives invertibility in the free model. Compactness is valid only in the fixed-dimensional closed coefficient ball. Continuity of inverse gives a common positive spectral gap. The trace logarithm is zero because every positive free word has zero trace. The tracial derivative proof avoids an invalid identity between noncommuting matrix logarithms.

C: A common smooth majorant exists; the addendum gives an explicit cutoff construction. Its Hilbert–Schmidt Lipschitz constant is O(sqrt(N)), with all dimension factors accounted for. Parraud's estimate is applied to a single fixed polynomial with bounded deterministic coefficient variables. The normalized error must be multiplied by kN; the resulting O(log(N)^2/N) mean is uniformly bounded. Concentration applies to F-EF, and the bounded mean is removed only after accounting for t>M. Exponential tail integration then yields every nonnegative moment. Singular finite pencils cause no difficulty for positive moments, and r=0, m=0, N=1 are treated directly.

D: In the small neighborhood q<1/g, the trace-log expansions converge absolutely at each fixed N and their weighted coefficient masses are summable. The signs, complex conjugations, trace sizes, cyclic invariance, and periodic multiplicities are correct. Pure powers use MSS Remark 3.8. Centered concentration gives the required exponential uniform integrability; finite-dimensional Gaussian convergence alone would not suffice. The remainder estimate tends to zero uniformly in N by a valid integrable Gaussian majorant. The limiting covariance series expands the mixed tensor power and has the required reciprocal-determinant sign.

E: H_N is holomorphic in independent A,Z on the product row balls. Compact-local Cauchy–Schwarz uses only the proven fixed-dimensional moment bounds. The mixed-tensor spectral-radius estimate is valid even when its norm is not below one. This ensures the prospective limit is holomorphic everywhere on the domain. The identity theorem is used on a connected product domain, not on an antiholomorphic diagonal.

F: The positive-map series P converges for strict outer radius, solves the Lyapunov identity, and produces a strict row contraction after simultaneous similarity. Every determinant is similarity-invariant; the mixed tensor matrix is conjugated by the tensor-product similarity. This extends the pointwise result to fixed strict-outer-radius tuples. No stronger uniformity is smuggled through the similarities.

## Reproducibility and negative tests

The original 13-check verifier passed normally, under -O, and under -OO on separate writable staging copies, reproducing the recorded result hash. It uses explicit exceptions rather than Python assert statements, so optimization does not disable its checks. However, running that preserved verifier in an actual non-root read-only copy failed at its unconditional output write. This is a tooling defect, not a mathematical defect.

The supplemental checker is read-only by design and uses standard-library exact rational matrix calculations. It checks row/column iterates, positive-map adjointness, noncommuting mixed tensor trace expansions, direct double covariance sums, every binary word orbit through length five, scalar counterexamples/signs, conjugation, and a nonnormal strict-outer-radius similarity example. It also enforces the agreed scope and source-free file set. Scope mutation tests and an explicit failing guard are required to reject; optimization cannot disable them.

The runner tests and final file integrity results are recorded separately. A read-only test is meaningful only when the executing UID is nonzero and real write attempts fail; both conditions are checked. The checker is an interface and integrity test, not a formal proof assistant. Its finite examples cannot establish a universal analytic theorem. Mathematical acceptance rests on the audited derivation and the stated external inputs.

## Final disposition and publication boundary

- 30005923: HOLD_VARIABLE_COUNT_UNIFORMITY. A repaired fixed-g prior theorem is verified; the literal all-g target remains unresolved by this packet.
- 30005922: CREDITED_PRIOR_RESULT_WITH_EXPLICIT_REPAIRS. The exact OWR stable-polynomial convention is covered, and the reconstructed pointwise theorem holds for each fixed pair of strict-outer-radius tuples. Local uniformity is accepted only on each fixed-dimensional product row ball.
- No all-g constant, optional sharp bound, monotonicity in N, full general mixed-word theorem, full quotient theorem, or publication/acceptance of the three-author preprint is certified.
- Original authored files remain unchanged. The frozen packet contains authored mathematical documents, tests, hashes and public-source metadata only. Copied primary PDFs, TeX, extracted source text, screenshots, datasets, private sources and coordination records are excluded.

No further research is needed to complete this bounded acceptance audit. Closing the all-g gap would require separately authorized work or authoritative clarification of the intended target scope.
