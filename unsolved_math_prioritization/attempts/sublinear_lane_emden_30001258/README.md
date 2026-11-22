# Frozen analytic package: row 1877 / problem 30001258

Status: SCOPED PARTIAL; no full-problem closure and no novelty claim.
Local only. No publication, commits, queue changes, copied scholarly sources, dataset contents, or private coordination files belong to this package.

## Exact theorem scope
On a bounded connected C^{1,1} domain, for p>1, weight one and Dirichlet boundary conditions, normalized least-nodal eigenpairs at 1<q<p sufficiently close to p obey |mu_q-lambda_2| <= C(p-q). The unnormalized resonant actual least-energy nodal solutions have a nonzero finite C1 subsequential limit along every sequence q increasing to p after extraction. Uniform bounds apply to arbitrary choices of normalized representatives. The conclusion concerns asymptotic compactness as q approaches p, not an unrelated closed parameter interval.

The unchanged RESONANT_NODAL_ANALYSIS.md supplies all five approaches. Approach 1 is the unconditional general-p sandwich; Approach 2 supplies general-p inequalities and a rigorous p=2 entropy condition; Approach 3 is conditional; Approach 4 records a variational obstruction; Approach 5 checks the exact interval case. INDEPENDENT_AUDIT.md principally audits Approach 1 and also checks the p=2 projection. It is not a machine proof or independent certification of every ancillary derivation.

Excluded conclusions: general-p unique limiting direction or amplitude, full-family convergence without selection and orientation conventions, a general-p entropy identity or derivative, nonsmooth-domain extension, and novelty. The source does not explicitly settle whether only subsequential convergence is the intended target. Consequently the original problem retains scoped-partial status.

## Evidence chronology
SOURCE_GATE.md is the unchanged earlier source inspection; its statement that the resonant gap was not yet verified is historical, not the terminal claim. The later unchanged report and its hash-anchored audit establish the specified smooth-domain subsequential consequence. PUBLIC_METADATA.json records prior source inspections and public hashes, not a fresh retrieval or fresh corpus scan. No source text, PDFs, or corpus records are included.

## Verification boundary
There is no executable mathematical certificate. verify.py checks only byte integrity, exact inventory, public metadata schema, fixed provenance anchors, and full Python AST provenance. A PASS does not verify PDE arguments, scholarly-source truth, retrieval history, or mathematical completeness. Human analysis and its stated literature inputs remain necessary. An attacker able to replace both package and external receipt defeats this local integrity trust anchor.

Run from the parent directory:

    python -B frozen_sublinear_1877_20261021/verify.py frozen_sublinear_1877_20261021 frozen_sublinear_1877_20261021_RECEIPT.json
    python -O -B frozen_sublinear_1877_20261021/verify.py frozen_sublinear_1877_20261021 frozen_sublinear_1877_20261021_RECEIPT.json
    python -B frozen_sublinear_1877_20261021/test_integrity.py frozen_sublinear_1877_20261021 frozen_sublinear_1877_20261021_RECEIPT.json

The receipt and replay/mutation results remain outside the frozen directory. The mutation harness uses temporary copies, invokes the unchanged trusted verifier, and exercises both normal and optimized modes. It never creates sockets or executes a candidate package's code. Verification does not modify package files. No Python asserts are used for security checks.
