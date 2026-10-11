# Acceptance: established finite-generator characterization

Decision: AUDITED_PRIOR_RESULT_WITH_SOURCE_SCOPE_QUALIFICATION.

For every finite family of L2(R) generators and fixed positive integer n, its norm-closed integer-shift span S satisfies T_(1/n)S = S if and only if rank G equals the sum of the n residue-cutoff Gramian ranks almost everywhere on [0,1). PROOF.md gives the complete independent reconstruction; AUDIT.md preserves the full integrated mathematical and source audit.

This is the established Theorem 5.2 of Aldroubi, Cabrelli, Heil, Kornelson and Molter, *Invariance of a Shift-Invariant Space*, J. Fourier Anal. Appl. 16 (2010), 60–75, https://doi.org/10.1007/s00041-009-9068-y , arXiv:0804.1597v3 (2008). It is not a new theorem or first resolution. The source's 2018 PDF typesetting date is not a theorem-priority date.

## Included conclusions

The reconstruction proves fiber membership through Fourier-coefficient uniqueness and measurable finite Gram–Schmidt, then reduces fractional translation to cyclic residue projections and finite-dimensional rank equality. It does not assume a general range-function theorem. Plancherel, elementary measure theory, Fourier uniqueness and finite-dimensional Hilbert-space facts are explicit imported standard dependencies.

The identity-Gramian specialization includes orthogonal residue Gramian projections and cross-residue frequency-vector orthogonality. For normalized principal generators exactly one residue is active almost everywhere; for unnormalized principal generators at most one may be active, allowing zero fibers. No nonzero-fiber, independence, Riesz-basis or frame-bound hypothesis is added to the main theorem.

The proof uses W_k = closure(P_k S) = S(P_k Phi) until invariance proves the image P_k S closed. A normalized counterexample shows that a pre-invariance cutoff image need not be closed and need not equal its supported intersection. This is a repair to a proof presentation, not a counterexample to the rank theorem.

## Original-source and practical limits

- The original OWR 2004 question sought a useful qualitative support-style analogue in its identity-Gramian setting. Its unspecified qualitative standard is not certified by simply presenting the general theorem.
- The printed scalar support-set display requires Fourier interpretation. Its literal time-domain reading fails for sinc, without invalidating the established theorem.
- Chui–Sun (2003) already contains a related vector-orthogonality criterion in an affine-frame setting. No novelty is claimed for the normalized reformulation, and those affine-frame hypotheses are not imported into the general theorem.
- Identical componentwise support sets can yield opposite answers in rank two. Values and relative directions matter.
- Infinite cardinal ranks do not extend the finite-dimensional test; an explicit countable-generator counterexample is retained.
- The exact a.e. criterion, infinite alias sums and rank discontinuity do not supply a finite algorithm for arbitrary L2 inputs. No impossibility theorem for every restricted algorithm is claimed.
- The separate positive-error approximate-invariance question is not resolved.
- No unqualified all-interpretations original resolution, novelty, formal verification or external human review is claimed.

The original-source, prior-theorem and Chui–Sun inspection boundaries are recorded exactly in SOURCES.json. Imported oversampling results in Chui–Sun were not independently audited and are not dependencies of this reconstruction. Finite matrix checks do not prove the analytic argument.

This AI-assisted, unrefereed edition records an internal AI audit of an established prior theorem. Acceptance here is an internal mathematical assessment, not human peer review or formal proof-assistant certification. Finite checks are corroboration only. This is a full written proof and audit edition, not a computational reproduction package. Source retrieval and inspection occurred during the preceding audit on 11 October 2026; this editorial preparation performed no fresh scholarly-source retrieval or inspection.
