# Acceptance of prior interval matching bounds

Audit date: October 10, 2026.

## Edition and review statement

This AI-assisted authored audit is unrefereed. “Accepted” means a prose proof
check in an independent internal AI audit of the identified prior results,
conditional on the explicitly cited established inputs. It does not mean
external human peer review, journal acceptance, or formal proof-assistant
certification. The underlying van Doorn result is published; Kominers v1 and
Chen--Korsky v2 are arXiv manuscripts whose journal acceptance was not verified.
The results belong to their credited authors. No novelty, priority, exhaustive
literature survey, or current-best-bound certification is claimed.

This edition preserves the complete authored general derivations and substantive
mathematical qualifications. Historical source retrieval, visual inspection,
version checks and finite diagnostics below refer to the October 10, 2026
audit. Edition preparation performed only byte-integrity and publication-
structure checks, with no new scholarly-source retrieval or inspection and
no new mathematical computation. Standard analytic inputs are dependencies,
not reproved here. The minor auxiliary-constant correction in Kominers's
Proposition 4.1 is retained; it is not a main-theorem failure.

Executable code, copied source documents or text, images, raw certificates,
numerical witnesses, datasets and private coordination material are omitted.
Aggregate counts, hashes, match results, public citations and inspection
history are verification metadata. Finite diagnostics are not asymptotic
proof certificates. This is not a formal or executable replay package.

## Accepted results

- Van Doorn, published Integers 26 (2026), A7: F(n)-f(n,n)>0.36 n log n/log log n for all sufficiently large n. The entire proof is checked, with the published Erdős--Pomerance diagonal estimates treated as explicit inputs.
- Kominers, arXiv:2607.10431v1: liminf [F(n)-f(n,n)]/(n log n)>=1/e. The full main proof chain is checked and the two analytic input theorems were matched to the primary corrected Hildebrand--Tenenbaum source. The small auxiliary-constant issue described in the audit does not affect the main theorem.
- Chen--Korsky, arXiv:2607.26450v2: F(n)<=n^(4/3) exp(O(log n/log log n)), h_P(n)<<n^(4/3)/(log n)^(1/3), and F(n)>=h_P(n)>=n exp(((log 2)/2-o(1))log n/log log n). The complete proof chains of the three main theorems are checked. The weaker projection appendix is not a dependency and is not included in the acceptance claim.

The last lower bound implies [F(n)-f(n,n)]/(n log n)->infinity after applying the known diagonal upper bound. This consequence is attributed to the prior bounds, not claimed as a new theorem.

## Residual questions

The uniform exponent-one upper-bound conjecture F(n)<=n^(1+o(1)) is not resolved. The separate fixed-start asymptotic in Problem 710 is not resolved. No finite threshold for the eventual asymptotic inequalities has been established here.

Kominers and Chen--Korsky are described as arXiv manuscripts; their journal acceptance was not verified. Chen--Korsky v2 supersedes v1 and is the adopted source. The original absolute endpoint is n+f(n,n), while the open-right integer convention adds exactly one to every length and cancels exactly in the difference of maxima and diagonal lengths.

## Finite diagnostics

The historical independent standard-library checker passed, with byte-identical result files in Python normal, -O, and -OO modes. These are recorded audit outcomes, not mathematical checks rerun for this edition:

- All 3,921 residue starts for n=1,...,9, including translated positive and negative starts
- 72 transfer constructions for 1<=n<=12 and 1<=k<=6
- 160 progression families and 1,962 oriented paths, including even moduli and negative starts
- 1,278 quadratic-residue image checks across four modulus families
- 36 CRT endpoint constructions, checking the exact complete list of multiples

These finite checks are not asymptotic proof certificates. In particular, the endpoint constructions do not assert a Hall deficit at the tested finite sizes.

## Sources and verification boundaries

SOURCES.json records seven primary PDF identities, including the superseded historical version and the corrected analytic dependency. It preserves public titles, URLs, sizes, hashes, manuscript status, and recorded visual-inspection pages. The PDFs and their extracted text are not distributed. Historical source inspection is distinct from edition-preparation integrity checking.

The complete accepted general argument is in AUDIT.md. Its standard analytic inputs are explicitly cited dependencies, not independently reproved from first principles. Public verification metadata and editorial provenance are in VERIFICATION.json and EDITORIAL_RECORD.json. The original sealed audit is unchanged.
