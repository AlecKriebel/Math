# Final exact-candidate priority and attribution wording audit

Reviewer: independent priority/attribution subagent. Completed 2026-10-06 PDT
(2026-10-07 04:24 UTC). This is a bounded attribution and public-source audit,
not a new proof audit or conventional human peer review.

## Exact candidate reviewed

The candidate identity in `publication/CANDIDATE_MANIFEST.json` is
`1e2d272246398abd2ff4186ea9857a756fdc829e0e9d164c56e376c7ff1a77c3`.
I reread the entire current manuscript, publication README, text abstract and
Zenodo manifest and independently recomputed these file hashes. The candidate
files and the original priority report were not modified.

| File | Bytes | SHA-256 |
|---|---:|---|
| publication/main.tex | 17096 | 1dd9b9a88304d580bede386f12acacf55a803063d3cfca7d7d0de0cfa453b698 |
| publication/README.md | 3168 | 32996ceed173c6673a49c6da3595946d42822b718947f23f460e02e9bcc248d1 |
| publication/abstract.txt | 728 | 812904cfe244275108990f92d1846ebcb916a0652a2aa997bd089257d51a9b59 |
| zenodo-deposit.json | 3140 | c62abfe8db3da9e3dd3833002a115a2248f5c64164a76bd07a1df97ea93bad01 |
| publication/paper.pdf | 87034 | 79d21f3d716c983abaff4078e9243eb43a58cdcc0fc23502d768c3d9bd8b27a3 |
| publication/CANDIDATE_MANIFEST.json | 10071 | 0abae5901150450a83359fd0d2195cba131cf00976c837bf4a4b918f2d9dd137 |
| agent_notes/priority_audit.md (preserved) | 17886 | 71bc5ed53aa9307a9f62e4abbc661355d3daa53559c973dd3c86b09fd80e2da0 |

The PDF hash is recorded as candidate identity evidence; this pass did not
repeat the independent PDF rendering audit or inspect the archive byte by byte.

## Attribution and scope findings

No substantive priority, attribution or metadata wording concern remains in
the four requested publication files at these exact hashes.

1. The title says the result comes *from* triangular-lattice universal
   optimality. The abstract calls the universal-optimality breakthrough,
   finite-to-infinite reduction and manifold theorem inherited results. It
   identifies the contribution as an explicit self-contained account and
   planar surface consequence. The README and deposit description use the
   same consequence framing and expressly disclaim an independent base
   breakthrough and first-public-priority claim.
2. The manuscript gives the correct historical normalization: Kuijlaars--Saff
   Conjecture 1 uses unordered pairs, hence its sphere coefficient is doubled
   here. It limits the resolved Brauchart--Hardin--Saff Conjecture 2 claim to
   dimension two and real s>2. The wrappers retain ordered pairs,
   covolume-one lattice, area scaling and ambient Euclidean distance.
3. The established finite reduction is now credited precisely to
   Hardin--Saff--Simanek Theorem 3.2 and Hardin--Leble--Saff--Serfaty Proposition
   3.1, with centered-ball periodic averaging credited to Cohn--Kumar Lemma
   9.1. The paragraph records the published analogous dimension-8/24
   implication. It no longer misattributes a finite equivalence theorem to
   the CKMRV universal-optimality paper.
4. The substantive planar input is explicitly OpenAI's main and atomic
   Theorem 1.1 at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a, with
   corporate author and manuscript-specific identifiers. The inherited
   theorem is cited, not disguised as a hypothesis or an independent
   discovery. Neither the strong per-potential sharp-auxiliary-function
   formulation of Cohn--Kumar Conjecture 9.4 nor uniqueness is claimed.
5. The Hardin--Saff citation points to the version including the addendum,
   distinguishes the retrieved PDF's November 23, 2018 heading from archive
   version chronology, and calls the theorem corrected. Smooth boundary and
   ambient distance are explicit in manuscript and wrappers. Exact theorem
   applicability remains the subject of the separate mathematical audit.
6. The HSS DOI is 10.1063/1.4903975; the HLSS DOI is the verified
   10.1007/s00365-018-9431-9. Deposit related identifiers match these sources
   and the pinned OpenAI paper. Title, sole author Alec Kriebel, ORCID,
   date, preprint type and license agree across the requested files.
7. The formal-verification limitation, extensive AI-use disclosure and lack
   of conventional human peer review are clear and consistent. The metadata
   makes no broader dimension, subleading-term, s<=2, microscopic
   crystallization or finite-minimizer uniqueness claim.

Minor editorial observation, not a substantive issue: `Lebl'e` in the TeX
prose and bibliography is an ASCII apostrophe spelling rather than the usual
accented `Lebl\'e`. The identity, author attribution and cited work are
unambiguous. It does not alter this audit's conclusion.

## Final current-source and duplicate check

Searches and read-only version checks were performed on 2026-10-06 PDT
(2026-10-07 UTC), extending the detailed primary-source and citation-chain
audit in `agent_notes/priority_audit.md`. No external individual was contacted.

The following current primary archive version pages were reread:

- [HSS arXiv:1403.7505](https://arxiv.org/abs/1403.7505): latest v2,
  December 11, 2014; v1 March 28, 2014.
- [HLSS arXiv:1702.02894](https://arxiv.org/abs/1702.02894): latest v2,
  November 7, 2017; v1 February 9, 2017.
- [Hardin--Saff arXiv:math-ph/0311024](https://arxiv.org/abs/math-ph/0311024):
  latest v3 December 15, 2004; current page describes the paper plus addendum.
- [Hardin--Tenpas arXiv:2307.15822](https://arxiv.org/abs/2307.15822): latest
  v4 October 15, 2025. The current abstract still restricts its planar
  results to specified four- and six-representative periodic problems,
  rather than the unrestricted planar constant.
- [Leble arXiv:2511.03353](https://arxiv.org/abs/2511.03353): v1 November 5,
  2025 remains the current listed version; the exact local theorem was
  examined in the original audit and is not an unrestricted global result.

Read-only `git ls-remote` on https://github.com/openai/math.git returned
`adc7f1241b42e322a6451854ab7e4b4c146bf78a` for main at 04:24 UTC. Thus no later
upstream commit or silently changed version was observed. The public upstream
[overview](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/overview.tex)
continues to state the infinite centered-disk energy theorem and its separate
renormalized/Coulomb consequences; the original whole-corpus inspection did
not locate this explicit finite hypersingular surface note.

The final exact and equivalent-formulation searches used these queries:

- `"Hypersingular Riesz-energy constants on surfaces"`, restricted to
  arxiv.org, github.com and zenodo.org;
- `"triangular lattice" "C_{s,2}"`, restricted to arxiv.org and github.com;
- `"Universal optimality of the triangular lattice" correction`, restricted
  to github.com and openai.com;
- `hypersingular "OpenAI" "Riesz"`, restricted to arxiv.org, github.com and
  zenodo.org.

Returned relevant primary hits were the upstream repository overview,
verification README and formalization inventory. No exact counterpart to
this explicit finite/surface note or later source correction was located in
this search. Unrelated search results and third-party commentary were not
used to certify a theorem or priority.

This is bounded negative-search evidence, not proof that no equivalent result
exists, not a certification of firstness, and not evidence of a novel
finite-to-infinite mechanism. HSS and HLSS already establish the general
reduction, and the upstream planar theorem makes the target an immediate
newly available inherited consequence. The exact candidate's explicit
consequence framing is justified by the evidence; no stronger originality
claim is justified or present.

## Verdict and limits

Clean bounded verdict for priority, attribution and requested metadata wording
at candidate identity
`1e2d272246398abd2ff4186ea9857a756fdc829e0e9d164c56e376c7ff1a77c3`:
**no substantive issue found**. The paper should remain an explicit
consequence note. This review does not certify the central upstream proof,
finite-transfer proof, manifold applicability, package reproduction,
publication outcome or tracker action; those have separate required checks.

The original report and candidate publication bytes were preserved. No git,
Zenodo, spreadsheet or other service mutation was performed by this reviewer.
