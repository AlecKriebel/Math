## Attributed prior bounds; uniform exponent-one upper question unresolved

This prose-only edition preserves the complete authored derivations and acceptance of three prior works on distinct multiples in intervals. Define f(n,m) as the least length H for which (m,m+H] contains distinct multiples of 1,...,n; F(n)=max_m f(n,m); h_P(n) is the prime-only maximum. All logarithms are natural.

- Wouter van Doorn's published theorem gives F(n)-f(n,n)>0.36 n log n/log log n eventually.
- Scott Duke Kominers's arXiv:2607.10431v1 gives liminf [F(n)-f(n,n)]/(n log n)>=1/e.
- Kaizhe Chen and Samuel Korsky's arXiv:2607.26450v2 gives F(n)<=n^(4/3) exp(O(log n/log log n)), h_P(n)<<n^(4/3)/(log n)^(1/3), and F(n)>=h_P(n)>=n exp(((log 2)/2-o(1))log n/log log n).

The last lower bound and the known diagonal upper estimate imply [F(n)-f(n,n)]/(n log n)->infinity. This is a consequence of the credited prior results, not a new theorem. The uniform upper question F(n)<=n^(1+o(1)) remains unresolved by these results. The fixed-start asymptotic in Erdos Problem 710 is separate and is not settled here. A 4/3 upper exponent does not approach 1.

## Complete authored argument and exact scope

The accepted original audit is 21,040 bytes, SHA-256 43c210e38a0dc03080c955812c025cd269a260855a793a56f972f3195b8670f5. AUDIT.md preserves the complete general derivation: normalization between absolute endpoints and lengths; exact cancellation of the open-right one-unit shift; van Doorn's transfer construction; Kominers's smooth Hall obstruction, relative error control and fixed-parameter optimization; the Chen--Korsky progression-union path argument; both upper bounds; and the quadratic-residue/CRT lower construction, including endpoint completeness and order of limits.

The minor auxiliary-constant issue in Kominers's Proposition 4.1 is retained. For small d, use c2=max(1,2b) instead of c2=2b to satisfy the cited lemma's common-constant hypotheses. The main theorem chooses d arbitrarily large and is unaffected. This is not a main-theorem failure. Chen--Korsky v2 supersedes v1; the weaker projection appendix is not a dependency of the accepted bounds.

This AI-assisted authored audit is unrefereed. Acceptance means a prose proof check in an independent internal AI audit under the explicitly cited standard inputs. No external human peer review, journal acceptance of the preprints, formal proof-assistant certification, novelty, priority, exhaustive literature survey, or current-best-bound certification is claimed. No explicit asymptotic thresholds are established.

## Attribution and source dependencies

- Erdos and Pomerance, [Matching the natural numbers up to n with distinct multiples in another interval](https://math.dartmouth.edu/~carlp/PDF/matching.pdf), 1980: original absolute-endpoint convention and published diagonal lower/upper estimates. Those estimates are explicit dependencies; their complete analytic proofs are not recertified from first principles here.
- Erdos, [Some of my forgotten problems in number theory](https://hrj.episciences.org/125/pdf), 1992: open-right interval convention and original question.
- Wouter van Doorn, [On the length of an interval that contains distinct multiples of the first n positive integers](https://math.colgate.edu/~integers/aa7/aa7.pdf), Integers 26 (2026), A7, DOI 10.5281/zenodo.18154085: published January 5, 2026.
- Scott Duke Kominers, [Long Intervals Without Distinct Multiples of the First n Positive Integers](https://arxiv.org/abs/2607.10431v1), arXiv:2607.10431v1, submitted July 11, 2026. Journal acceptance was not verified.
- Kaizhe Chen and Samuel Korsky, [Improved Bounds for Distinct Multiples in Intervals](https://arxiv.org/abs/2607.26450v2), arXiv:2607.26450v2, revised August 13, 2026; title-page date August 4, 2026. Journal acceptance was not verified. The one-author v1 is historical only.
- Adolf Hildebrand and Gerald Tenenbaum, [On integers free of large prime factors](https://tenenb.perso.math.cnrs.fr/PPP/Psi%2B.pdf), Transactions of the AMS 296 (1986), 265--290, corrected author-hosted copy: Theorems 2(i) and 3 were source-checked, not independently reproved.

Hall's theorem, CRT, unique factorization, the prime number theorem and Mertens' estimate are also explicit standard inputs. The original source/version checks were recorded on October 10, 2026. Public source metadata retains all seven PDF hashes and byte counts, public URLs, manuscript status and visual-inspection pages. Edition preparation performed no new scholarly-source retrieval or inspection.

## Verification and editorial boundaries

Historical diagnostics passed with byte-identical normal/-O/-OO output records: 3,921 residue starts, 72 transfer constructions, 160 progression families and 1,962 oriented paths, 1,278 quadratic-residue checks over four modulus families, and 36 CRT endpoint constructions. The endpoint tests do not assert Hall deficits at the tested finite sizes. These are aggregate verification metadata; finite checks do not certify asymptotic theorems.

The original sealed audit is unchanged. Editorial changes add review and attribution framing, clarify historical inspection/check language, remove an illustrative numerical example and finite modulus list, and replace workflow-only prose. Every substantive general mathematical argument and qualification is retained. EDITORIAL_RECORD.json records the exact authored-input identities and scope of changes.

Exactly eight authored mathematical prose, acceptance, editorial and public citation/verification metadata files are proposed as additions. Copied source PDFs/text/images, code, detailed test outputs, raw certificates, numerical witnesses, datasets, private sources, private personal data and private coordination material are excluded. This is not an executable or formal replay package. QUEUE.md and unrelated paths remain unchanged. The proposed PR is draft only; no release or DOI is requested.

## Exact public-file identities

- `ACCEPTANCE.md`: 4,887 bytes; SHA-256 `8ae57e0a79d9f60f37c4da9715c07496c3eadc577ecf4823904c3711ba5694c7`.
- `AUDIT.md`: 22,736 bytes; SHA-256 `45853f002cd267903a6b572fb6e71dd5d5d2b0a71af63528fd857ca25a215f35`.
- `EDITORIAL_RECORD.json`: 1,811 bytes; SHA-256 `fbf65587fa7a074d8802080f4b23dfd929bc491700b8d94419d552daa09b86a9`.
- `MANIFEST.json`: 1,681 bytes; SHA-256 `c0e3ffca23593f7b38383f7abf885f07291e9ff457d2fb29fc1fcdc04a3b4a87`.
- `README.md`: 3,911 bytes; SHA-256 `7309052be5e90be08803ac656ed441e667125347812b977478b343063e3767f2`.
- `SOURCES.json`: 4,188 bytes; SHA-256 `48d5266004f56c38c98f8561af3f83ffd79b71aa8e9fce563f9e03ee0396758f`.
- `STATUS.md`: 1,887 bytes; SHA-256 `558f9f63c73fa70c16a447424c556585d2a1530b7fc5ae8bfa1307e3269076f4`.
- `VERIFICATION.json`: 2,941 bytes; SHA-256 `1b9e26960ad9cd9bf15b86248e178e286edd37f61c16465c075e6fd97480f3fc`.

MANIFEST.json lists all eight members and hashes the other seven; its own digest is separately pinned above.

