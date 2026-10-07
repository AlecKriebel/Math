# Dependency ledger

| Input | Exact role | Validation basis | Status/gap |
|---|---|---|---|
| Family004 thm:main | H10(Q) undecidability for integer polynomial encoding, arbitrary n | Pinned TeX and PDF; manuscript-specific citation OpenAI2026 | Unverified; audit central proof and dependencies |
| Poonen2009 Theorems1.1(i),1.3, Lemma10.1, sections9–10 | Effective decision transfer from regular projective geometrically integral class to all varieties | Published primary proof and independent reconstruction | Verified conditional transfer; separate fresh reconstruction running |
| Perfect-field regular/smooth equivalence | Match Poonen promise over Q | Finite-type regular schemes over perfect fields; component/global-functions argument in manuscript | Promise preprocessing supplied |
| Rational-point enumeration | Semidecision and finite height search | Exact primitive integer-coordinate enumeration with self-delimiting presentation size | Elementary proof supplied; undecidability consequence conditional on arithmetic input |
| Family004 companion arithmetic | Pole parity / five-point height estimate | Source citations and proof bodies | Audit needed; no release/Lean-directory shortcut |

Checkpoint02 refinement: logic, elliptic/primes, pole-parity algebra and height geometry have independent source-body audits. Five-point height may use coefficient5 and Pan2022 Theorem1.0.4 in place of the source dyadic companion; exact assumptions and substitution are in corrected upstream_arithmetic.md. Do NOT accept the superseded vonKanel–Kret shortcut. The pivotal remaining new arithmetic input is the pointwise2-converse, specifically exclusion of the rank0/divisible-Sha2∞ alternative for the constructed E_l. Its six simultaneous arithmetic obligations remain under active reconstruction. No applicable full family004 Lean formalization identified.
