# Independent source-match audit

Checkpoint: 2026-09-23 03:50 UTC. Source-match task: 100% complete. This audit verifies scope and notation; it does not certify the proposed proof or novelty. No outreach, commit, or push was performed by this auditor.

## Verdict

The current UnsolvedMath entry asks exactly whether equality can occur in

\[
D_J=M_1(J)^2-M_2(J)^2\geq\tfrac14(E_{J+1}-E_J)^2.
\]

Thus a valid proof of strictness for every finite positive integer \(J\), for the bounded Euclidean Dirichlet setting, answers that corrected equality question negatively. The original report also asks a saturation question, separately from its neighboring upper-growth-bound problem. There is, however, a real typographical inconsistency in the original report, not merely an OCR error: its displayed second mean lacks the square. Any final manuscript should disclose this and explicitly specify the corrected quantity \(D_J\).

## Primary report, visual verification

- [Publisher record](https://ems.press/journals/owr/articles/3389): *Low Eigenvalues of Laplace and Schrödinger Operators*, Oberwolfach Reports 6 (2009), 355-428, DOI [10.4171/OWR/2009/06](https://doi.org/10.4171/OWR/2009/06).
- [Publisher PDF](https://ems.press/content/serial-article-files/46205), independently also available as [MFO PDF](https://publications.mfo.de/bitstream/handle/mfo/3107/OWR_2009_06.pdf).
- Printed p. 413, PDF page 59/index 58: Section 8 specifies the Dirichlet Laplacian on bounded \(\Omega\subset\mathbb R^n\), \(n\geq2\).
- Printed p. 414 introduces item (5), attributed to Evans Harrell and Joachim Stubbe.
- Printed p. 415, PDF page 61/index 60, defines
  \[
  M_p(J)=\left(\frac{n+2p}{nJ}\sum_{j=1}^J E_j^p\right)^{1/p},\qquad
  M_0(J)=e^{2/n}\left(\prod_{j=1}^J E_j\right)^{1/J}.
  \]
- Its final question asks: “Can one find Ω and J such that the inequality” followed by \(M_1^2(J)-M_2(J)\geq(E_{J+1}-E_J)^2/4\), “is saturated?”
- Earlier on that page are separate requests for a growth upper bound and for \(E_J\leq M_p(J)\). The saturation claim alone does not answer either.

I rendered and visually inspected all of printed pp. 413 and 415. Page 415 visibly omits the square on \(M_2\) in both gap displays and the square-root bounds. This is therefore a source typo. Its neighboring growth display also has inconsistent powers; no correction or solution of that separate problem is certified here.

Local preserved report: `sources/OWR_2009_06-source-audit.pdf`, SHA-256 `a3ab668409f786c7c1783150d9f937b2d6e06471a48b76c5721b58a49bf3a683`. Visual audit renders are in `audit/source-report-p413.png` and `audit/source-report-p415.png`. The source PDF was downloaded for inspection; redistribution permissions should be checked before including it in any public release.

## Live website comparison

[UnsolvedMath OWR-3389-016](https://www.unsolvedmath.com/problems/OWR-3389-016) was successfully read in the in-app browser on 2026-09-23 UTC after direct HTTP access returned 429. Title: *Equality Cases for Universal Eigenvalue Mean Inequalities*. It is labeled Open, with literature-review date 2026-08-21. Its displayed definition agrees with the definition above, and its main inequality uses \(M_1(J)^2-M_2(J)^2\). It cites the report DOI and arXiv:0808.1133.

The site's v1.7 correction note claims that the official source itself contains the difference of squared means. That precise source-description claim is contradicted by the PDF image. Expanding the comparison panel shows the prior extraction used \(M_{1/2}(J)-M_2(J)\); the reviewed wording replaces this with the squared-means expression. The latter is the mathematically coherent correction, but it is not a literal transcription of the print source. The website's Open label and literature triage are not independent evidence of current novelty.

## Independent support for the intended corrected expression

The report's reference [3] is Harrell and Stubbe, *On trace identities and universal eigenvalue estimates for some partial differential operators*, Trans. AMS 349 (1997), 1797-1809, DOI [10.1090/S0002-9947-97-01846-1](https://doi.org/10.1090/S0002-9947-97-01846-1). The publisher PDF was access-blocked. The [CERN record](https://cds.cern.ch/record/472254/) links the author-submitted 1995 precursor, [MP-ARC 95-431 source](https://web.ma.utexas.edu/mp_arc/e/95-431.amstex), preserved locally as `sources/harrell-stubbe-1995-preprint.amstex`.

Proposition 6 of that primary preprint defines

\[
D_N=\left(\left(1+\frac{2\sigma}{d}\right)\frac1N\sum_{k=1}^N\lambda_k\right)^2
-\left(1+\frac{4\sigma}{d}\right)\frac1N\sum_{k=1}^N\lambda_k^2,
\]

and gives \(\lambda_{N+1}-\lambda_N\leq2\sqrt{D_N}\). It explicitly says \(\sigma=1\) applies to the Dirichlet Laplacian. Consequently its \(D_N\) is precisely \(M_1^2-M_2^2\) under the report's rooted-mean definitions. This is evidence beyond dimensional analysis for the correction.

Own deduction: the typo cannot harmlessly be interpreted literally. Write \(a=M_1\), \(b=M_2>0\), \(g=E_{J+1}-E_J\). The established corrected inequality gives \(A=a^2-g^2/4\geq b^2>0\). Under a spatial dilation inducing eigenvalue scaling by \(t>0\), the literal printed equality becomes \(t^2A-tb=0\), which holds for \(t=b/A\). A negative equality answer must therefore concern the corrected expression, not the literal dimensionally inconsistent print formula.

## Limited prior-strictness check

- [Harrell-Stubbe arXiv:0808.1133](https://arxiv.org/pdf/0808.1133), pp. 5-7, contains an exact commutator identity and abstract non-strict estimates. A text search for strictness/saturation did not locate the proposed finite-index Dirichlet strictness result. This is a limited check, not a novelty certificate.
- [Ashbaugh-Hermi (2004), publisher PDF](https://msp.org/pjm/2004/217-2/pjm-v217-n2-p01-p.pdf), *A unified approach to universal inequalities for eigenvalues of elliptic operators*, Pacific J. Math. 217, 201-220: the remark on printed p. 212 states strict versions of the classical inequalities under \(V\geq M>0\). Its positive-potential assumption excludes the zero-potential Dirichlet Laplacian considered here. The apparent direct strict-Yang search hit therefore does not settle this claim. Local copy and text are in `sources/ashbaugh-hermi-2004-source-audit.*`.

Remaining audit gap: a broad search for prior publication of the exact corrected strictness theorem remains necessary before claiming novelty. Independent proof verification belongs to the other audit routes.

## Distribution note

The mentioned downloaded source PDFs and source-page renders are private audit inputs and are excluded from git and both publication archives. Readers should use the original URLs above. The subsequent broad, scoped priority audit is in priority-audit-independent.md.
