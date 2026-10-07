# Rational-point undecidability for smooth projective varieties over the rational numbers

Alec Kriebel — ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

This note proves that no algorithm decides rational-point existence on the valid-input promise of smooth projective geometrically integral varieties over Q, presented by finitely many homogeneous integer equations. Ambient dimension, dimension, degree, equation count and coefficient size may vary. It also rules out a computable uniform bound on the height of one rational point in terms of the explicit presentation size. The theorem is a consequence of OpenAI's audited rational Hilbert's tenth theorem and Poonen's existing effective geometric transfer. It is not an independent solution of the base problem or a new geometric reduction; no first-priority claim is made.

## Mathematical and publication status

The mathematical candidate has a completed dependency integration audit. The arithmetic route uses two explicit substitutions: published Pan modularity at coefficient prime 5 with compatible coefficient 2 for the conductor at 5, and a universal integral group-ring correction reconciling the inverse/direct Euler conventions. The pointwise-converse audit is restricted to the non-CM full-rational-two-torsion branch actually needed by the constructed curves E_l. The broader companion's other branches are not certified here.

Publication requires complete-package adversarial review and a current priority audit in addition to the mathematical integration audit. This immutable payload records the research and validation artifacts; the public repository retains subsequent complete-package reviews, publication receipts and current service status in PUBLICATION_STATUS.json. A reserved draft DOI alone is not publication.

## Contents and reproduction

- `manuscript/main.tex` is the self-contained main source; `manuscript/paper.pdf` is its exported publication PDF.
- `manuscript/height-repair.tex` and its PDF give the coefficient-prime substitution conditional on the three explicitly stated, separately audited geometric inputs. The configuration is the five fixed discriminant-210 branch values, never arbitrary five rational points.
- `VERIFIED_CORRECTIONS.md` and the current theorem/dependency/approach ledgers specify the accepted route.
- `agent_notes/` contains checkable source-body derivations and scoped adversarial audits. `reviews/dependency_integration.md` matches their joint hypotheses.
- `sources/PINNED_INPUT.json` and `sources/PINNED_COMPANIONS.json` identify exact upstream source bytes at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. The upstream clone remains read-only.
- `reproducibility/README.md` documents clean compilation and exact finite checks. Those checks support interfaces and do not prove undecidability alone.

The production upload kit is `publication/zenodo-upload-kit/`. Its separately downloadable payloads are `paper.pdf`, `height-repair.pdf`, `source.zip`, and `verification.zip`; the outer kit is not the intended sole upload. Extract the two archives into the same fresh folder to reconstruct the source and verification tree. Third-party papers, caches and upstream manuscript bodies are not redistributed; exact references, URLs and hashes are supplied instead. `publication/CANDIDATE_INVENTORY.json` records the bytes submitted for complete-package review. Complete publication reviews are retained in the public repository separately from the payload, so later operational receipts do not change reviewed archive bytes.

## Attribution, limits and disclosure

Poonen's Theorems 1.1(i), 1.3 and Lemma 10.1 supply the entire geometric transfer; his Remark 1.2(c) also credits an earlier Q-case route to R. Robinson. OpenAI's manuscript-specific citation supplies the new arithmetic input. Public-source dates are distinguished from manuscript dates in the priority audit. A negative search is not evidence of being first.

The reduction makes finitely many valid nonadaptive disjunctive oracle queries. No fixed-dimension, curve, surface, Fano, general-type, finite-point-promise, Turing-degree, quantitative reduction or single-query many-one claim is made. No no-point-certificate extension is included.

AI tools were used extensively in research, drafting and adversarial verification. Automated reviews are not conventional human peer review. At publication this preprint has not undergone conventional human peer review or refereeing. No formal verification of the complete theorem is claimed.

Original prose and proofs are licensed CC BY 4.0; the original verification code is MIT-licensed, as specified in LICENSES.md. External sources retain their own rights.
