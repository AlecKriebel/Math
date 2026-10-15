# PR384 independent quaternion/abstract-ring audit

Frozen head: `682f6fd29dce0c9ca5625d14461d0e6e1eb2e6d6`. Audited family: Turn 3 quaternion syzygy/restriction obstruction, Turn 4 finite abstract representation-ring obstruction, and the precise source and structural inputs they use. Scoped review complete. No mandatory repair was found in this family. This report does not approve the unaudited remainder of PR384, authorize a merge, or bypass the required acceptance of PR385 first.

The original question remains unresolved at 5/5 substantive author turns. Neither the Q8 element nor the abstract family solves the universal finite-group symmetry problem. No novelty or priority certification is made.

## Controlling primary sources

The exact problem OWR-16776-002 is Benson's contribution on printed pp. 847–849 of [OWR 2019/14](https://ems.press/content/serial-article-files/46794?nt=1), bound to [the official EMS record 16776](https://ems.press/journals/owr/articles/16776). The visual page check confirms both conjugation bars in the bounded-species statement. It asks symmetry of the full complex Banach completion of the split Green ring in the dimension-weighted norm, for every element. Positive module growth, stable quotients, maximal quotients, and further C*-completions are separate targets.

[Benson's accepted 2022 manuscript](https://arxiv.org/pdf/2008.13155v2) controls Definition 1.1.1, (ii'), the character/symmetry criterion, the actual-module detection theorems, and Schanuel. The older author-hosted manuscript was independently obtained but is not relabeled as the later published edition. [Langer's primary paper](https://arxiv.org/pdf/0803.0252v1), §1.2 and Proposition 2.2, supplies self-injectivity and the credited four-periodic Q8 resolution. Its right-module, left-matrix-multiplication convention was checked visually. Independently downloaded bytes match every relevant frozen source SHA-256. No new author/novelty search was conducted.

## Claim-by-claim disposition

| Claim | Status | Independently checkable evidence / exact limitation |
|---|---|---|
| Langer maps form a minimal Q8 resolution in characteristic two | Verified | Hamilton-unit matrices, four zero compositions, exact ranks 7/9/7/1, independent unit minors, radical-power calculation; literal four-periodicity proves all degrees. |
| The four syzygy cores have exact stable order four over every characteristic-two field | Verified | Dimensions 1/7/9/7/1; norm image is trivial; cover kernels have no projective summand; tensor presentations and Schanuel; projective-free cancellation excludes orders one/two, all proper divisors. |
| Signed Q8 element is self-adjoint and has full spectrum `{0,-2,-4}` | Verified | Nonzero Fourier idempotents force ambient stable spectral persistence; explicit inverses exclude other values; regular-projective idempotent splitting lifts with correction `(3/2)P` and zero scalar factor. |
| All elementary-abelian restrictions vanish in the full split ring | Verified | Unique involution gives only E=C2 and the trivial subgroup; direct invariant-image action ranks give `Omega^1|E=Omega^3|E=k+3kE`; `P|E=4kE`; zero total dimension handles the trivial subgroup. |
| This defeats a signed/complex restriction inequality | Verified | Radius four versus restricted radius zero for any finite multiplicative constant. It does not defeat positive-module gamma detection or symmetry; its spectrum is real. |
| Abstract family satisfies all five axioms and (ii') | Verified | Generic P-twisted multiplication proof, cubic coefficients, star/dimension compatibility, regular element; independent exact coordinate checks include cyclic and noncyclic H. |
| Abstract completion is radical zero yet nonsymmetric | Verified | Generic invertible Fourier transform to `C^(m+1)` and nonreal fixed-basis character. Exact C3 polynomial control confirms spectrum `{0,4,zeta,zeta^2}`. |
| Every positive-element gamma duality identity still holds | Verified | All real positive combinations are self-adjoint in every representation-ideal quotient; spectral mapping for squares proves the statement for the entire family, not only finite samples. |
| Abstract family cannot be a based finite-group split Green ring over any field | Verified | Semisimple case has a split trivial summand in `M tensor M*`; modular case has an indecomposable projective cover of dimension d and indecomposable projective-free syzygy of missing dimension d-1. Stable equivalence is derived from self-injectivity and Schanuel. Scope explicitly preserves the whole basis, dimensions, and duality. |

All generic and infinite-dimensional deductions are expanded in `PRE_REPLAY_PROOF.md`; the finite computations supplement those proofs. No general spectral statement is inferred merely from gamma field-extension invariance. For the Q8 construction, every characteristic-two field is treated directly by F2 identities and nonzero unit minors, minimality over its local group algebra, and the same coordinate/Fourier proof. Algebraic closure is unnecessary in the nonrealizability proof.

## Materially distinct controls

`independent_controls.py` imports no author or old-review code. Its quaternion model uses Hamilton multiplication of signed units instead of the snapshot's exponent-normal-form rule. It computes the syzygy images and actual restriction action, not merely their dimensions. It checks GF4 scalar extension and the augmentation radical dimensions `8,7,5,3,1,0`. The characteristic-two restriction is essential: the displayed third/fourth composite would contain `2N` in odd characteristic.

The abstract controls use exact rational matrices for multiplication by P, checking determinant `d*c^(m-1)`. They include H=C3,C4,C5,C3xC2 and the boundary groups C2,C2xC2. The order>2 hypothesis distinguishes the nonsymmetric cases from exponent-two symmetric controls. At q=1, semisimplicity fails: the nontrivial Fourier directions yield a square-zero radical. These boundary controls corroborate the exact roles of the hypotheses.

An extra exact field control directly separates all-element symmetry from positive identities. In the C3,q=2 example let `y=(x1-x2)/sqrt(3)` and `a=1+i*y`. The complete species values of y are `0,0,i,-i`; those of a are `1,1,0,2`, while those of `a* a` are `1,1,0,0`. Thus `rho(a)^2=4` but `rho(a* a)=1`. This computation is exact in `Q(sqrt(3),i)` and uses no floating-point eigensolver. It strengthens the check that the original all-element criterion is being distinguished from the always-valid positive radius identities.

## Reproduction, independence, and preservation

Primary reads and the independent proof/control checkpoint preceded the old review and old-code reads. The first checkpoint was recorded at 65% completion. Only afterward were exact private copies of `verify_turn3.py`, `verify_turn4.py`, and the old reviewer `independent_check.py` executed with Python `-B`. All three exit successfully, with zero stderr and stdout byte-identical to their frozen receipts. The new controls also exit successfully with standard-library dependencies only.

`SOURCE_ACQUISITION.json`, `VISUAL_SOURCE_CHECKS.json`, `OLD_REPLAY_RECEIPT.json`, `INDEPENDENT_CONTROLS.json`, and `INPUT_HASH_VERIFICATION.json` preserve source, execution, and input bindings. All 52 frozen input hashes and lengths are unchanged. The independent-check source/output hashes are recorded in `OUTPUT_MANIFEST.json`. Raw PDFs, extracted primary text, rendered page images, and private historical execution copies remain ignored. No Git/index/queue/PR/service state or external communication was changed.

Strongest verified result: the scoped obstructions in Turns 3–4 are correct, including their explicit limits. Exact remaining mathematical gap: an argument controlling bounded species on other actual finite-group indecomposable directions, or an actual finite-group non-Hermitian species. The abstract nonrealizability proof prevents promoting its nonsymmetry to an actual-group counterexample. No repair to these two turns is required; maintain the original unresolved 5/5 disposition.
