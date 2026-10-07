# Dependency ledger: verified inputs and exact scope

## Mathematical chain

| Dependency | Exact statement/assumptions | Validation and remaining limitation |
|---|---|---|
| OpenAI family332, pinned adc7f124 | Real ell1 metric Markov cotype2, N2<=12sqrt21; finite cuts, cubic/quartic martingale, killed stationary chain, geometric-to-Cesaro bound | Independent line-by-line cut audit; constant 108*28=3024; all-L1 adaptation reproduced in main.tex; supplied PDF matched. Original pdfTeX-specific source fails under Tectonic at pdfglyphtounicode, an engine mismatch. No formalization found or claimed. |
| Measurable cut reconstruction | Every finite tuple in arbitrary real L1 has positive cut weights, exact binary pair distances and an ambient affine contraction | Self-contained proof in main.tex section2, independent agent reconstruction; integrability and zero weights checked; no measure regularity assumed |
| Mendel–Naor2013 Thm1.11 | Source Markov type2; target metric Markov cotype2 and W2-barycenter constant Gamma; each finite-domain extension bounded by kappa Gamma M2 N2 | Exact primary theorem checked. Banach mean has Gamma1 by coupling triangle/Jensen. No 2-barycentric convexity required. kappa is unspecified absolute constant; no numerical overall C claimed. |
| HWW1993 IV.1.1(a), p158 and IV.1.5(b), pp161–162 | Real/complex L1 spaces are L-embedded; arbitrary l1 sums retain property | Primary Banach lattice argument inspected. main.tex reduces arbitrary positive countably additive measures to finite pieces and explicitly constructs needed contractive projection. No L1 duality assertion. |
| Fine-ultrafilter/ultrapower bidual passage | All finite extensions plus contractive Y**->Y projection yield full arbitrary-subset extension | Anchored scalar ultralimits give bounded coordinates on nonseparable/unbounded domains, preserve all finite tails; Q:Y_U->Y** contractive. Proof independently reconstructed. No arbitrary-free-ultrafilter shortcut. |
| NPSS2006 Thm1.2/2.3 | M2(Lp)<=4sqrt(p-1) for 2<=p<infinity | Primary author PDF checked; common finite simple-function approximation transfers to arbitrary source measures. Correct DOI: 10.1215/S0012-7094-06-13415-4 (primary Princeton publication record). |

## Priority chain and publication decision

Naor 2609.07564v1 (submitted Sept7, 2026) contains a full proof of Hilbert→standard L1 and O(sqrt(p log p)) estimates. Version2 (submitted Sept10, 15:15:29 UTC) publicly announces Mendel–Naor, *Metric invariants from de-Höldering factorization*, proving N2(L1[0,1])<infinity and O(sqrt(p)) extension. The full forthcoming proof was not located in documented primary searches. This is verified public disclosure, not a checked full proof.

The announced standard-target cotype transfers by contractive interval-averaging projections to all finite weighted ell1, then by finite cuts to every L1(mu). MN2013 and HWW1993 already supply all-Markov-source/full-subset scope. The requested quantifiers do not identify a substantively unresolved new theorem. Independent audits agree; production publication and tracker update are withheld under the original novelty condition.

Cuts are classical (Deza–Laurent); cubic smoothing is also in Cheng–Wang–Xiang2609.08749v2, which proves torus metric cotype, a different invariant. The killed-chain proof/constant is attributed to OpenAI's later released manuscript-specific source. No invention, firstness, or human peer review is claimed.

## Source custody

Pinned source hashes are in receipts/initial_source_hashes.json. Exact source references/hashes are in agent_notes/cut_audit.md, full_extension_audit.md and priority_audit.md. Research-only reference PDFs and caches are excluded from archives and git. No Lean proof for this target was located; comparator sorry files and unrelated Cotype/MarkovType modules do not verify it.
