# Counterexample to Long Question 7.2

Problem 10900050 / AMR-108-0050. Public mathematical edition, 11 October 2026 UTC.

## Result

For the totally real field \(k=\mathbb Q(\sqrt{10})\), its full ring of integers is \(O=\mathbb Z[\sqrt{10}]\). With prime elements defined to generate nonzero prime ideals,

\[
\omega(\Gamma_{\rm unit})=\omega(\Gamma_{\rm prime})=2,
\qquad \min_{\mathfrak q\ne0\text{ prime}}|O/\mathfrak q|=2.
\]

Thus the proposed equality in Long Question 7.2 is false: its left side is 2 and its proposed right side is 4. The ideal \((2,\sqrt{10})\) has norm 2 and is nonprincipal. No unit or prime element lies in it, so reduction modulo this ideal gives a proper two-coloring of both graphs. The edge \(\{0,1\}\) attains both clique bounds.

The [complete elementary proof](PROOF.md) establishes every arithmetic and graph step. It uses no class-number table, prime search, numerical approximation, unproved conjecture, or omitted computational certificate.

## Exact source scope

The target is Question 7.2 in [Problems In Groups, Geometry, and Three-Manifolds, arXiv:1512.04620v1](https://arxiv.org/pdf/1512.04620v1). Its cited [Long–Thistlethwaite manuscript](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz.pdf), first definition and Section 3, defines the relevant prime differences as generators of prime ideals. Irreducible elements alone do not satisfy this convention. The full-ring-of-integers and total-reality hypotheses are met, and the question imposes no PID assumption.

The cited manuscript's Theorem 3.1 is printed with a minimum principal-ideal norm; the problem list's displayed question instead uses a minimum prime-ideal norm. This distinction is retained explicitly. The proof evaluates the actual quantities in the printed question directly and does not identify those two minima or rely on repairing that theorem.

The work does not answer a separately imposed PID-only question or an irreducible-difference graph question.

## Review and publication limits

The proof and separate mathematical audit are AI-assisted. The accepted verdict is a complete negative counterexample in the precise source scope above. Acceptance here is not external human peer review, journal acceptance, formal proof-assistant certification, or certification of novelty or priority.

The audit inspected the pinned 16-page manuscript. A separately hosted 17-page manuscript was checked in online text but not downloaded or fingerprinted, and its relationship to the journal version was not established. The final journal full text and the full 2018 Lopez thesis were not inspected. Bounded searches found no explicit prior statement of this exact counterexample, but cannot establish novelty or exhaustive literature status. Publication preparation did not repeat those historical scholarly-source inspections.

## Reading and verification

- [Full proof](PROOF.md)
- [Separate AI-assisted mathematical audit](ACCEPTANCE_REPORT.md)
- [Mathematical audit manifest](AUDIT_MANIFEST.json)
- [Hash-bound acceptance](ACCEPTANCE.json)
- [Public-source identities and inspection history](SOURCE_MANIFEST.json)
- [Bounded literature check and limitations](LITERATURE_CHECK.json)
- [Exact editorial transformations](EDITORIAL_MAP.json)
- [Research log](RESEARCH_LOG.md)
- [Closed public-file manifest](PUBLIC_MANIFEST.json)

Only authored mathematical prose and public verification metadata are included. Source PDFs, copied source text or images, dataset contents, raw code or certificates, and private material are excluded. The mathematical goal in the stated scope is complete; novelty remains unverified.
