# PR196 original-source and mathematical contract audit

Audit family C; frozen original submission HEAD a229ac722a3b1733bcb590a5f796b4a52f68cc73, supplied by parent custody. This audit performed no Git, index, ref, remote, editor, or tab operation and initiated no communication with an outside individual. It wrote only this audit directory and the expressly authorized shared private source cache.

## Verdict

**Mathematical source-contract PASS.** The exact original problem requires an interior failure of C^2 for a smooth boundary Dirichlet problem on P^1 times the disc. The turn4 candidate meets that target, and the required source hypotheses support its construction and pre-contact derivatives. I found no remaining unsupported central mathematical claim in its use of the primary sources. The covering-chart and endpoint-smoothness details are supplied in DEPENDENCY_CHECKS.md. This is a source-contract and mechanism audit, not historical novelty, priority, or publication clearance.

**Provenance correction required.** The OWR report itself announces and sketches an interior construction; it does not present a formal numbered world-open conjecture. Its tentative smoothness paragraph leaves a detail unproved in that short report. The intake's claim that the report leaves the construction unresolved overstates what can be inferred. The report's announced interior mechanism must be credited, and the imported open-status assessment must not be promoted as a source theorem.

## Independent sequence

I read source_record.json and the official OWR printed1321-1325 first, visually verifying printed1323-1324. At 2026-10-15T13:16:23.129676Z I wrote SOURCE_PROBLEM_FREEZE.md, before opening TURN_4_CANDIDATE.md or any favorable historical review. The frozen artifact hash was 9775b931c9d0993ad1898951c342b0d20e88221f0ebdb4bb575b92e938303764. I then read the candidate and checked the complete accessible primary PDFs at their relevant statements/proofs. Before other-family report access, I completed the independent dependency derivations. I have not read any other new family report or the original independent_review/README/status files. Later coordination supplied an additional primary reference and existing page renders only.

## Exact source target and scope

In the global setting, X=P^1, D={|tau|<1}, f is smooth on X x partial D and omega+dd_z^c f is semipositive on each boundary slice. The solution is continuous up to the boundary, relatively plurisubharmonic, and has zero Bedford-Taylor Monge-Ampere measure in the product interior. The required example fails to be C^2 at some interior point. The source's general setup permits semipositive data; a strictly positive example is stronger and also permits the AIF contracts.

The speaker distinguishes previously located boundary irregularities from the announced interior construction. At printed1324 the sketch uses simply connected Hele-Shaw domains, a terminal conformal map, and transport of the fiber form. Smoothness of the inverse-flow density near the terminal complement receives tentative treatment, permitting vanishing density there. The finite-time positive-density contact-arc argument in turn4 is an additional derivation from different credited inputs. The source does not provide a formal status certificate for that derivation or for the broad existence question.

## What the cited papers establish

The published AIF Proposition3.4 supplies the smooth strictly positive global form and a finite-time tangency along a chosen genuine segment. Its proof uses a smooth simply connected lifted domain and a strong flow on a covering surface. The proof of Theorem6.2 explicitly supplies nonvanishing limiting velocity. Proposition2.5 supplies the current identity across the zero-area arc. Section4 supplies both the envelope duality and the smooth twisting relation on the punctured disc. AppendixA supplies smooth Green dependence for the lifted-domain use after a fixed conformal chart and compact-time restriction.

The published AIF Theorems1.1/1.3/6.2 locate non-twice-differentiability at |tau|=1. They do not literally state the turn4 interior derivative jump. The earlier IHES paper supplies the original duality proof and harmonic-disc classification; missing regular foliation does not itself prove failure of C^2. The APDE main theorem gives a rank-zero open set, and its later discussion anticipates further regularity behavior without proving the candidate's jump. No literal exact existing theorem giving the candidate's interior conclusion was found in this required source corpus. This limited statement is not historical clearance.

## Dependency correctness

The full check is in DEPENDENCY_CHECKS.md. The candidate's decisive mechanism survives adversarial checks:

1. Filling a zero-area contact-arc piece enlarges the Greenian domain while the current identity makes psi_T relatively harmonic across the arc.
2. Negative Green-function comparison has the stated direction and is strict. A point-only contact would not support this argument.
3. The smooth lifted flow gives a'_-(T)=G_Omega_T and finite strictly negative a''_-(T). It is essential to work on the cover rather than invoke smoothness of the singular projected boundary.
4. The one-sided slope gap creates a global Legendre plateau. Strict negative left curvature produces unequal one-sided derivatives of F', proving a genuine second-derivative failure.
5. The chosen negative Green value gives an interior nonzero radius. The twisting map and correction terms are smooth there; rotation preserves strict boundary positivity.

The argument requires no post-contact strong-flow description, no quantitative rate of arc engulfment, no global foliation through degenerate points, and no curvature hypothesis from the unrelated hyperbolic-flow theorem. Its existence recipe is constructive through a credited theorem; it is not a polynomial closed form.

## Checkable artifacts and access limits

- SOURCE_PROBLEM_FREEZE.md: independently fixed claim, quantifiers, regularity, boundary cases, risks and timestamp.
- CONTRACT_MATRIX.md: theorem-by-theorem input matrix, printed/PDF page map and literal-formula cautions.
- DEPENDENCY_CHECKS.md: source applications and mathematical derivations.
- SOURCE_ACCESS.json: URLs, versions, verified byte counts/hashes, input hashes and access limitations.
- RESEARCH_LOG.md: UTC checkpoints and completion estimates.
- SAFE_ALLOWLIST.json and HASH_MANIFEST.json: exact safe authored output set; no source texts or images.

The published AIF file independently matches the expected 3,158,845 bytes and SHA256 724e742d033b3401b6938011cf07ee4faf79a7d13b14d22bb9ca1a90969cc0e2. The arXiv download is v3 dated 8Dec2017 and has different pagination/numbering; published numbering controls. The optional precursor is arXiv1212.2337v2, whose Remark7.1 corroborates two-sided modified flow; Theorem2.2 alone is forward. All six source PDFs and full text extractions live only in excluded shared private_primary_sources. Three OWR page renders and independently produced AIF page renders were inspected; extraction uncertainties about closure bars and disc bars were resolved visually.

No core source was inaccessible. Initial DOI web-reader errors were bypassed with official full PDFs. Relevant full theorem statements and proofs were inspected, rather than snippets; this was not a line-by-line reproof of every result in all papers. This audit did not conduct a broad literature/priority search and cannot conclude that an interior example is historically new or currently world-open.

Source-contract audit completion: **100%**. No unsupported source-contract gap remains. Historical novelty/priority and publication clearance remain unassessed, as required.
