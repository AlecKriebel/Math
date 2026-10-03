# Publication entrypoint: 6000016

**Reviewed complete negative result.** The unrestricted positive-definite Hessian-metric stability assertion in the original item 5(b) fails, even for complete volume-preserving affine structures on a two-torus. One substantive attempt, complete early: **claimed_solved, 1/5**. Mathematical task completion estimate at this checkpoint: 100%; this is not a novelty or peer-review probability.

Read the unchanged [full proof](PROOF.md), followed by the unchanged [independent full audit](audit/AUDIT_REPORT.md). The audit returned **PASS_FULL**, requiring no mathematical repair. It reviewed all author files, the exact original source, the deformation topology, the arbitrary-metric quantifier, and the global positivity/Stokes obstruction. This is an independent AI audit, not human peer review.

## Credit and exact scope

The affine-torus deformation is already published in Baues–Goldman, arXiv:math/0401257v2, §5, p.20. The packet proves directly that none of its noncentral fibers admits any positive-definite Hessian metric, using the Codazzi equation and Stokes' theorem. The affine family is not new, and historical priority for this consequence is not established. No novelty or first-resolution claim is made.

The result applies to the printed unrestricted affine-deformation question. It does not assert a counterexample in the hyperbolic, fixed-linear-holonomy, or indefinite-metric settings. The exact live aggregator returned HTTP 403; the original item was visually checked independently by author and auditor.

## Additive clarification: smooth period coordinates

The frozen family is a smooth deformation of affine structures. Baues–Goldman's extra period coordinates parameterize this particular curve by (0, −∛t), which is continuous at zero. If smoothness in those coordinates is also desired, use t=s³. The connection family remains smooth; the period curve becomes (0, −s); and the same obstruction excludes a positive-definite Hessian metric for every s≠0. This optional clarification was already verified in the audit and requires no alteration of the frozen proof.

## Reproducibility and preservation

From this directory, with Python 3 and SymPy installed:

```sh
python check_exact.py
python audit/check_audit.py --author-dir .
```

The author script passes 41 exact identities. The independent script passes 61 controls: 22 integrity/reproduction and 39 algebraic/boundary-case controls. Both replayed byte-for-byte from a different working directory. The analytic integral contradiction is a proof, not a finite-sampling conclusion.

All seven frozen author files are retained unchanged, including the historical “audit pending” notices. This additive status records the subsequent PASS_FULL without rewriting those reviewed inputs. All five audit files are also retained unchanged. [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json) binds the selected public files; the earlier [author manifest](FROZEN_AUTHOR_MANIFEST.json) and [audit manifest](audit/AUDIT_MANIFEST.json) retain their original bindings.

The public packet excludes source PDFs, page images, full source texts, raw corpora, and private context. The repository change outside this directory is limited to this problem's existing QUEUE.md Status, Turns, and previously empty Findings cells. No merge or release is requested.
