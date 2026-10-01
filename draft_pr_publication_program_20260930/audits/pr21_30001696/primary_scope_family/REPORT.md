# PR21 exact target and classical input audit

This family **passes the exact-target and primary-input gates** for head `096aacd71a1dc6dd3a73bea3c1055877dc8c0451`, proof SHA256 `58809f3edaa2930f1111ba823b1ce50c8e328dd8388b2e19323600ede3d04305`. No missing hypothesis was found in the strict variation or compact semialgebraic-to-PL adapters. This is a family verdict, conditional on the separately audited new construction; it is not a complete proof certificate, historical-priority determination, or assertion that the problem remains open in 2026.

The first independence seal is dated `2026-10-01T18:32:48Z`; the independently reconstructed primary findings were sealed at `18:37:51Z`, before reading the author's source record, source audit, provenance, attempt metadata, or research log. I never read historical review files, root reconstruction, or sibling conclusions. Author/reviewer pass declarations were not evidence. All 14 snapshot files are bound by raw byte hashes in `first_pass_seal.json`.

## Exact scope and endpoint adapter

[OWR Report 08/2011](https://ems.press/content/serial-article-files/46323), Klee's complete contribution and reference tail, printed pp.370–373 / PDF pp.22–25, was read. Question 4 is on printed p.372 / PDF p.24. It asks about the entire complex as a combinatorial sphere–ball triangulation. On p.371 its switch set uses adjacent positions `j=1,...,d-1`; it does not count a final-to-first edge. The contextual construction covers `0<=i<=d-1`, while Theorem 2's manifold, homology, and boundary claims use `0<=i<d-1`. The submitted theorem covers this full nontrivial range and explicitly handles the full-sphere endpoint.

| Parameter | Actual complex / candidate interpretation | Audit |
|---|---|---|
| `d>=2, 0<=i<=d-2` | Entire compact `(d-1)`-complex, product `S^i x D^(d-i-1)` | Exact question, no narrowing |
| `i=0` | Two disjoint `(d-1)`-simplices; `S^0 x D^(d-1)` | Disconnected base allowed |
| `i=1, d>=3` | Known sphere–ball product | Correctly credited |
| `i=d-2` | Cross-polytope boundary with two alternating facets omitted; one-dimensional ball factor | Included, including disconnected orbit cross-section |
| `i=d-1` | Full boundary sphere; `S^(d-1) x D^0` | Separate trivial endpoint |
| `d=1, i=0` | Two points, `S^0 x D^0` | Explicit separate endpoint |
| `i=-1` | Empty complex in Klee–Novik's auxiliary definition | Not the sphere-product question |

The original source record's `original_statement` and `clean_statement` preserve the entire sphere–ball question. Their omission of explicit bounds is resolved by the original contextual definition; their dated `status=open` and 2026-08-21 literature assessment are metadata, not evidence of present mathematical status.

[Klee–Novik's author-final PDF dated 2011-07-27](https://sites.math.washington.edu/~novik/publications/sphere-products.pdf) explicitly defines combinatorial manifolds using PL ball/sphere links on p.4; Definition 3.1 on p.5 is the same noncyclic complex. Theorem 1.2(d,e), pp.2–3, proves the manifold and integral (co)homology statements and states the **boundary** product homeomorphism. The `i=0,1` full-space cases occur on pp.3,5,11. Importantly, Remark 3.7, p.9, additionally records collapse to an i-sphere and a **disk bundle** over that sphere. This prior structure should be credited in the candidate's prior-work discussion. A disk-bundle assertion does not by itself establish that the bundle is trivial. No theorem in these inspected passages was substituted for the submitted full PL product. The isolated boundary exponent printed after the `i=1` argument on p.11 is dimensionally inconsistent; use Theorem 1.2(e), not that typographical slip.

## Strict zero-sensitive total positivity

The actual [published Margaliot–Sontag 2019 PDF](https://sontaglab.org/FTPDIR/margaliot_sontag_totally_positive_automatica2019.pdf), p.4, Theorem 3, equation (10), supplies precisely

\[
A\in\mathbb R^{d\times d},\quad\text{all square minors positive},\quad x\ne0
\quad\Longrightarrow\quad s^+(Ax)\le s^-(x).
\]

Its definitions on p.2 delete zeros for `s^-` and independently fill them for `s^+`. The first assertion has **no** no-zero restriction. The following weaker TN assertion has extra restrictions and is not the input being used. The Appendix, pp.11–13, gives the determinant argument through Proposition 1 and the SSR characterization; its strict forward implication was read.

The adapter is exact: `e^(tJ)` is square real and invertible; adjacent entries of J are positive, all other off-diagonal entries vanish, and `t>0`. Normalization divides by a positive scalar, so it changes neither sign count. Thus a point with `s^-<=i` acquires `s^+<=i`, which is the submitted ambient-sphere interior criterion. No theorem assumes an integer or positive diagonal, nor requires all coordinates of x to be nonzero.

The [Schwarz 1970 original](https://msp.org/pjm/1970/32-1/pjm-v32-n1-p20-s.pdf) uses older nomenclature: TP means nonnegative minors, STP means strictly positive minors. Theorem 3, printed pp.213–214 / PDF pp.12–13, covers continuous tridiagonal coefficients with nonnegative adjacent entries, none identically zero on any subinterval. Constant positive adjacent entries meet this condition. Its compound proof agrees with the submitted wedge-path mechanism. Theorem 4, pp.214–215 / PDF pp.13–14, supplies the same zero-sensitive inequality for every nontrivial solution and every earlier/later time pair. Its forward proof invokes Karlin's classical matrix result; the accessible Margaliot–Sontag Appendix supplies a separate displayed determinant proof of the needed implication.

For a checkable boundary witness, `x=(1,0,1)` has `s^-=0` and `s^+=2`. The identity matrix is nonsingular TN and leaves this witness unchanged, so replacing strict TP by nonsingular TN would fail. The candidate does not make that replacement.

## Compact semialgebraic-to-PL passage

[Hardt–Lambrechts–Turchin–Volić's published 2011 PDF](https://msp.org/agt/2011/11-5/agt-v11-n5-p01-s.pdf), printed p.2485 / PDF p.9, Theorem 2.6, states uniqueness up to PL homeomorphism of polyhedra semialgebraically homeomorphic to one compact semialgebraic set. Its cited [Shiota–Yokoi 1984 original PDF](https://www.ams.org/journals/tran/1984-286-02/S0002-9947-1984-0760983-2/S0002-9947-1984-0760983-2.pdf) is directly accessible: Corollary 4.3 and Theorem 4.1 are on printed p.737 / PDF p.11. The published proof reduction and Theorem 4.4 proof, pp.738–745, and graph-semialgebraic definition 6.1, p.746, were inspected. Corollary 4.3 explicitly includes the semialgebraic version. There is no dimensional, smoothness, orientability, or simple-connectivity restriction in this PL input. The constant-local-dimension condition belongs to an intermediate theorem, not an additional condition on Corollary 4.3 or the cited compact result.

Here the common compact semialgebraic set can be `C_i`. Its two polyhedral models are the actual finite cross-polytope realization `P=|B(i,d)|` and a finite triangulation `Q` of the standard PL product. Radial normalization gives `P->C_i`; the submitted hitting-graph map, product map, and radial polyhedral models give `Q->C_i`. Compositions and inverses have semialgebraic graphs. Round models need not themselves be polyhedra. A positive cutoff constant is permitted because semialgebraic maps use real polynomial coefficients; rationality of that constant is not a hidden hypothesis. Applying Theorem 2.6 gives a PL homeomorphism between **these polyhedral structures**, and the established Klee–Novik PL links support the requested combinatorial-triangulation wording.

This audit accepts the classical theorem after inspecting its original statement and relevant published proof; it does not claim to rederive every cited triangulation or tube-system result. The earlier attempted AMS `/tran/` URL returned unrelated HTML and was rejected. The correct `/journals/tran/` PDF removes any inaccessible-original-statement qualification.

## Related-space consistency

[Machacek's published 2022 paper](https://ems.press/content/serial-article-files/39446), Definition 2.1, printed p.546 / PDF p.4, uses minimum sign variation with zeros ignored. With `k=1,n=d,m=i`, its space is exactly `C_i/{x~-x}`: sign variation is invariant under all nonzero scalar multiples and each real line has two unit representatives. Theorem 3.4, p.554 / PDF p.12, gives a PL manifold; Theorem 3.6, p.556 / PDF p.14, gives collapse to `RP^i`. Both cover all `0<=i<=d-1`; parity restrictions occur in subsequent Cohen–Macaulay/network results. These claims are consistent with the submitted cover, but neither proves an ordinary full product nor identifies a product action for the antipodal involution. The candidate claims no equivariant product.

[Galashin–Karp–Lam, arXiv:1707.02010v3](https://arxiv.org/abs/1707.02010v3), Definition 2.1 p.4 and Lemma 2.3 with full proof pp.5–6, use a norm-contracting flow on `R^N` and a bounded smoothly embedded Q satisfying `f(t,closure(Q)) subset Q` for every positive t. The conclusion is a closed ball; its attractor is a single point. The submitted core is instead a sphere, and the proof does not apply that lemma to it. Citation as related flow technique is mathematically accurate and proves no priority claim.

## Reproducibility and correction record

`primary_sources.json` retains retrieval UTC, requested/resolved URLs, byte counts and SHA256 hashes. `page_ledger.json` records one-based PDF and printed locators, version distinctions, and inspection limits. Foreign PDFs, extracted text and page images are solely in `/tmp/pr21_primary_scope_096aacd`; none are deliverable artifacts.

All **seven** previously recorded PDF captures reproduced their exact byte counts and hashes. The publisher OWR PDF has a different binary hash from the old MFO file, but normalized text on the entire Klee contribution/reference-tail PDF pp.22–25 is identical. The published HLT V theorem is on PDF p.9 / printed p.2485; the old arXiv capture's same theorem is on PDF p.8. The author-final Klee–Novik and newly inspected Shiota–Yokoi originals have additional independently recorded hashes. These are source-version/access clarifications, not substantive corrections to the theorem being audited.

The substantive documentation improvement is to include Klee–Novik Remark 3.7's disk-bundle/collapse result in prior work. No candidate artifact was edited by this family. `attempt.json` and the author's log both record **1/5** substantive attempts; that is preserved as author-recorded history. This independent audit is not a new central attempt and cannot reconstruct unrecorded proof-search activity.

`scope_checks.py` independently passed **93,508 exact assertions** through `d=8`, binding all 14 snapshot files, checking noncyclic facet counts, minimum zero-completion variation, and antipodal invariance. The general zero-completion derivation is simple: deleting zeros yields a lower bound; fill between equal nonzero signs constantly and between opposite signs with one transition, then fill initial/final zeros constantly. This realizes that lower bound and identifies every face with its correct minimum-variation stratum. These finite tests and deductions support the domain adapter; they do not certify the new homeomorphism or global novelty.

Strongest verified result: the submitted full-range **entire-space PL claim** matches the original question, and both external classical theorem hypotheses apply exactly as stated. Remaining gates: independently validate the new construction in the other families and then evaluate priority through the parent's separate later families. No 2026-open or global-originality conclusion follows from this audit.
