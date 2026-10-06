# Audited partial: monodromy exactness for isocrystals

Problem 30002618 / OWR-13102-007; queue rank 843. Canonical status: **unsolved**, **5/5** disclosed approaches.

The accepted [corrected proof](corrected/PROOF.md) establishes the cohomological defect identity ker(N)/im(i) ≅ im(A) ∩ ker(D), of dimension rank(A) − rank(DA), under its stated semistable/no-log coefficient hypotheses. Under additional cycle and componentwise trivial-connection assumptions, the defect is ker(T−I) ∩ im(T−I); exactness holds precisely when ker((T−I)^2)=ker(T−I).

The general coefficient classification and geometric-origin expectation remain unresolved. Arbitrary matrix diagnostics are not isocrystal realizations. No untwisted Frobenius-equivariance or novelty claim is made. This is the cohomological invariant-cycle question, not a Tannakian homotopy-sequence question.

## Correction and evidence

- [Independent audit](audit/AUDIT_REPORT.md) and [acceptance report](audit/ACCEPTANCE_REPORT.json)
- [Actual correction patch](audit/CORRECTION.patch): eigenvalue-1 semisimplicity terminology, Gysin hypotheses, and status precision
- Original six-file author freeze, corrected six-file freeze, and 15-member audit archive are retained unchanged, alongside external inventories and the original audit receipt/bootstrap
- All extracted members are byte-bound to those immutable archives. Exact patch replay uses zero fuzz and compares all six corrected files
- [Fresh retained-source bindings](PUBLICATION_SOURCE_BINDINGS.json): three complete corpus hashes and six retained source-PDF hashes. No corpus or third-party source contents are distributed

## Reproduction and limits

The original and corrected proof archives contain only text; there was no executable mathematical checker in them. Publication adds a standard-library-only auxiliary verifier and exact-rational matrix diagnostic runner. These are integrity and finite-example checks, not a formal proof of the imported comparison or Gysin theorems.

First authenticate publication_bootstrap.py and PUBLICATION_MANIFEST.json against the hashes in the acceptance comment. Run the verifier with Python -I -S -B, supplying the package directory and externally authenticated manifest SHA-256, optionally adding --replay. Use -O as an additional test, not a substitute for isolation. The external manifest and immutable pins bind every file before helper execution. The verifier rejects unexpected files, caches, symlinks, wrong entrypoints and malformed inventories. Publication controls exercise hostile working-directory/import environments separately from the original text-only proof package.

Five approaches are disclosed. The historical chronology is not independently certified. Historical statements that publication had not yet occurred are preserved as historical facts. No full-solution or exhaustive current-open-status certification is supplied.
