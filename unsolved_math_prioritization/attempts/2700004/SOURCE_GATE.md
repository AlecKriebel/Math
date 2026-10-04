# Source gate: AMR-026-0004 / 2700004

Checked 2026-10-04 (UTC).

## 1. Exact target and primary source

The requested [catalogue page](https://www.unsolvedmath.com/problems/2700004) was attempted through the web reader and direct HTTP. The direct request returned HTTP 403. The matching record was recovered from the public [UnsolvedMath dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json), using an existing local copy whose SHA-256 matches the distribution's LFS object. Only the selected record was retained in this investigation. Numerical ID, AMR code, title, author, and source item agree.

Primary question:
- Denis Serre, *Five Open Problems in Compressible Mathematical Fluid Dynamics*, author version dated December 28, 2012, Section 4, pp.9–10: [author PDF](https://perso.ens-lyon.fr/denis.serre/DPF/Ouverts.pdf).
- Published version, *Methods and Applications of Analysis* 20(2) (2013), 197–210, Section 4, pp.204–205: [journal PDF](https://intlpress.com/site/pub/files/_fulltext/journals/maa/2013/0020/0002/MAA-2013-0020-0002-a006.pdf).

Both complete Section 4 passages were read. The journal continuation on p.205 was also rendered and visually inspected. The question allows either the isentropic pressure law \(p=\rho^\gamma\) or the non-isentropic law \(p=(\gamma-1)\rho e\), with a fixed \(\gamma>1\). It asks for all-real-time classical solutions with positive finite mass and energy in odd dimension, specifically mentioning dimension three. Compact spatial support is offered as an example, not written as a mandatory hypothesis in that passage.

**Crucial scope issue:** the surrounding discussion involves Sobolev perturbations of constant entropy and affine velocity, whereas the explicit existential wording only says classical/smooth and finite mass/energy. We do not silently identify those two classes.

## 2. Direct prior construction

K. Fellner and C. Schmeiser, *Classification of Equilibrium Solutions of the Cometary Flow Equation and Explicit Solutions of the Euler Equations for Monatomic Ideal Gases*, *Journal of Statistical Physics* 129 (2007), 493–507:
- [DOI/publisher metadata](https://doi.org/10.1007/s10955-007-9396-8), publication date September 13, 2007.
- [Author manuscript](https://homepage.univie.ac.at/christian.schmeiser/Euler.pdf).

The full relevant derivations were read: Section 1, pp.2–4 (kinetic transport, moment closure, formulas (6)–(11)); Section 5, pp.11–12 (finite-mass/energy family and exponential profile). Page 12 was rendered and inspected. Their parameters \(\lambda=0\), \(\varphi(g)=Ce^{-g}\) yield the exact \(d=3,\gamma=5/3\) example in PROOF.md. The date precedes the question.

The source also distinguishes these solutions from small, near-constant-entropy Sobolev constructions. Accordingly our attribution is to a known full-Euler example, not to a newly solved isentropic problem. The written proof independently verifies all equations and integrals; it does not invoke an abstract as a proof.

## 3. Later obstruction: why it does not invalidate the example

Denis Serre, [*Expansion of a compressible gas in vacuum*](https://arxiv.org/abs/1504.01580), arXiv:1504.01580v1, Sections 1, 2.1–2.2, especially Theorem 2.5, p.10.

The complete argument around Lemma 2.1, Theorem 2.3, and Theorem 2.5 was inspected. It uses an isentropic gas with compact support and a front smooth up to vacuum. Free boundary trajectories make the support volume a polynomial; odd dimension forces a lower degree, which contradicts a dispersive mass estimate. The inspected Theorem 2.5 additionally prints an exponent restriction, \(\gamma\le1+1/(d-1)\), for \(d>1\). No stronger interpretation is used here. The Gaussian has no compact vacuum front and is non-isentropic, so the obstruction does not apply.

The arXiv listing reports v1 submitted April 7, 2015; the downloaded PDF has a later typeset date. Its exact bytes are identified in SOURCE_MANIFEST.json. We do not infer any additional theorem revision from that date.

## 4. Prior report and duplicate checks

The selected public dataset's generated research report was read in full. Its statement inserts “isentropic” into the broader catalogue wording and reports no known construction. This is not a faithful justification for dismissing the full-Euler branch. Its status claims and informal acoustic discussion were treated as untrusted leads, not proof.

Read-only checks in AlecKriebel/Math:
- QUEUE.md: rank 561, ID 2700004 / AMR-026-0004, queued, 0/5.
- Exact-ID code, PR, commit, and branch searches: no matches.
- AMR-code PR search: no matches.
- Eternal/Euler PR search: no matches.
- Compressible code search: no matches.
- Serre PR search: inspected returned candidates; none concerns this Euler target.
- Main repository root inspected; no matching Euler target folder.
- The current attempts-directory tree (54 entries) inspected; no matching ID or Euler target.
- related_target_groups.json read; this ID is absent.

The queue alone was not used as evidence of no prior work. These bounded searches establish no located repository attempt, not a theorem about every historical branch. Tool-read provenance remains local and is not published.

## 5. Success criterion, status, and exact gap

A broad classical full-Euler existential reading is settled by one admissible example in odd dimension. PROOF.md supplies one and verifies it completely; it already appears in the 2007 primary source.

A bounded-entropy, constant-entropy Sobolev, compact-support, or isentropic variant is a different target. Our example fails those additional hypotheses. No new solution of such a variant is supplied. No claim is made that those variants are all open; some have the narrower known obstruction described above.

**Gate conclusion:** pass for the mathematical theorem and its prior-art attribution; scope-qualified pass for the literal full-Euler wording; hold against any unqualified claim that all intended regularity interpretations or the isentropic problem are solved. The independent reviewer must explicitly preserve this distinction. No novelty claim.

## 6. Publication boundary

Only original mathematical exposition, bibliographic links/locations, source hashes, the short research log, status, and exact-check scripts/results are in public/. Source PDFs, extracted source text, rendered pages, complete catalogue records/reports, raw repository reads, and dataset corpora stay outside public/. There has been no remote write, release, merge, or external outreach.

