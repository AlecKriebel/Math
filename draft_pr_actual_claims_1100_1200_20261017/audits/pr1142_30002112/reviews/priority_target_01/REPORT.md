# Exact-target priority audit: PR1142 / problem30002112

Audit date: 2026-10-17 UTC. Scope: whether a recorded earlier full resolution exists for Colbois's additive Euclidean boundary-spectrum question, not whether individual construction tools are old. This is an independent primary-source priority review, not a certificate of earliest authorship or a new mathematical result.

## Finding

**An earlier full negative resolution is recorded.** Luc Pétiard's 2017 preprint proves a stronger impossibility statement for every fixed hypersurface dimension at least three. His 2019 doctoral thesis explicitly includes dimension two, with the complete construction in Chapter 2. Both precede the 2026-10-10 PR date and the 2026-10-17 audit date. Colbois's 2017 survey already attributes a negative answer to Pétiard; Colbois and Provenzano's 2021 journal paper explicitly acknowledges the failure of decoupling and cites the thesis.

The strongest verified priority conclusion is therefore positive and specific: the original target had a recorded full negative resolution before this candidate, for every fixed dimension under consideration, including a subfamily with connected boundary. It is unnecessary to infer priority from the absence of search hits.

The candidate's nested cavity, prescribed area in a small ball, exact spherical multiplicity count, and explicit divergent quotient differ from Pétiard's presentation. This audit has not established whether any of those specialized formulations first appeared in the candidate. They cannot support a claim that the original additive question is newly resolved. The central high-gap component plus round-sphere spectral-union mechanism itself is already explicit in Pétiard's proof.

## Exact question and an important source discrepancy

The complete Colbois contribution in Oberwolfach Report 33/2012, printed pp. 2034–2036, first presents the multiplicative Euclidean boundary-spectrum estimate and then asks on p. 2036 for dimension-only constants in

\[
\lambda_j(\partial\Omega)|\partial\Omega|^{2/m}
\leq A_m I(\Omega)^{1+2/m}+B_m j^{2/m},
\qquad I(\Omega)=\frac{|\partial\Omega|}{|\Omega|^{m/(m+1)}}.
\]

The problem-session restatement on printed p. 2064 has the first power of the isoperimetric ratio instead. Both formulas were checked in rendered pages. The question tested here is the survey contribution's exponent \(1+2/m\); the other version is retained as a distinct recorded variant. The spectrum in the preceding theorem is the intrinsic Laplace–Beltrami spectrum of the induced boundary metric. The source's problem-session label should not be used to reclassify this as an interior Dirichlet problem.

Both exponent variants are ruled out by Pétiard's result. Its arbitrary continuous geometric term, or the thesis's bounded-ratio formulation, applies directly to either power. No assumption that the ratio tends to infinity is needed for that implication.

## The earlier theorem and the hypothesis bridge

Pétiard, arXiv:1706.09189v1, Theorem 2 (p. 2), treats smooth compact Euclidean hypersurfaces with the induced metric. For each fixed \(n\geq3\), each continuous function \(f:(0,\infty)\to\mathbb R\), and each \(A>0\), it asserts violation of

\[
\mu_k(\Sigma)|\Sigma|^{2/n}\leq f(I(\Sigma))+A k^{2/n}
\]

by a connected embedded hypersurface for every sufficiently large index. It permits a prescribed diffeomorphism type. All six preprint pages, including the proofs and bibliography, were read; this classification does not rest on its abstract.

Pétiard's 2019 thesis, Theorem 2.1.2 on printed p. 24, strengthens the dimensional scope: for every fixed \(n\geq2\) and every \(A>0\), there are \(J>0\) and \(k_0\) such that for every \(k\geq k_0\) a connected smooth embedded hypersurface \(\Sigma\subset\mathbb R^{n+1}\) satisfies

\[
I(\Sigma)\leq J,
\qquad \mu_k(\Sigma)|\Sigma|^{2/n}>2A k^{2/n}.
\]

The fixed-topology strengthening is restricted to \(n\geq3\), as it should be. The whole relevant thesis discussion, printed pp. 15–18 and Chapter 2, printed pp. 23–30, was inspected. In particular, \(n=2\) is present in the proof, not merely in a headline.

Here is an explicit indexing and constants bridge to the original target. Pétiard uses \(\mu_0=0\); let the original one-based numbering be \(\lambda_j=\mu_{j-1}\), and put \(p=2/m\). Suppose a proposed bound had positive constants \(C,D\) and exponent \(\alpha\), where either \(\alpha=1+2/m\) or \(\alpha=1\). Choose

\[
A=2^pD+1.
\]

Apply the thesis theorem and obtain its \(J\). For sufficiently large \(k\), \(A k^p>CJ^\alpha\). Since \((k+1)^p\leq2^p k^p\) for \(k\geq1\), the theorem's example gives

\[
\lambda_{k+1}(\Sigma)|\Sigma|^p
>2Ak^p
>CJ^\alpha+D(k+1)^p
\geq C I(\Sigma)^\alpha+D(k+1)^p.
\]

Thus the difference in numbering does not leave a gap. Constants of other signs could be enlarged to positive constants, so positivity loses nothing.

Each final hypersurface is compact, connected, smooth, and embedded. Its bounded complementary component is a bounded connected smooth Euclidean domain with that hypersurface as its boundary. Therefore the prior result applies within the original domain class, and even within its connected-boundary subfamily. Allowing two boundary components does not restore a universal statement already false in the one-component subfamily.

The thesis also implies existence of examples whose quotient by the sum of the two unweighted target terms tends to infinity: apply the established failure successively to constants \(C=D=r\), for positive integers \(r\), and choose each index sufficiently large. This implication does not reproduce the candidate's exact two-component geometry or explicit index formula.

## Proof-body inspection, especially dimension two

The proof mechanism was checked independently of the candidate proof before reading the candidate:

1. CDE Theorem 1.4 supplies smooth embedded hypersurfaces with unbounded normalized first positive eigenvalue. The thesis explicitly separates the surface case, in which topology varies, from dimensions at least three, in which topology can be fixed.
2. Homothety fixes a sufficiently large area depending on the proposed spectral coefficient, while the first positive eigenvalue is pushed above the relevant part of the unit sphere's spectrum.
3. The disjoint union with the unit sphere has two zero eigenvalues and then a shifted initial segment of the sphere spectrum. This is proved in the thesis's Lemma 2.2.2, including multiplicities. Its use of Weyl asymptotics is only for the fixed round sphere, and requires no uniform asymptotic law across changing metrics.
4. The enclosed union contains the unit ball. Its boundary area is fixed at this stage, so the isoperimetric ratio has a bound independent of the growing index. This is Lemma 2.2.4. This step is already the geometric bridge that distinguishes an exact additive counterexample from bare high-gap existence.
5. Proposition 2.3.1 connects the components by a thin tube and preserves any prescribed finite spectral segment and the isoperimetric ratio to arbitrary accuracy. The thesis explicitly addresses smoothing through metric comparison. Area and enclosed volume converge as well. Any needed strict margin can be obtained by starting with a larger value of the arbitrary coefficient \(A\).

For the last step I also read Anné's entire 1987 article, printed pp. 271–280. Its setting allows a one-dimensional collapsed segment within a hypersurface of dimension two: \(q=1<n=2\). The endpoint set has codimension two in the surface, which is included in the capacity-zero puncture result. The connected-fibre requirement used in the collapse argument is also satisfied by the circular neck cross section in dimension two. The source supplies the finite-spectrum convergence used by the thesis; shrinking the segment length puts its additional Dirichlet spectrum beyond the desired finite segment. This is established older surgery input, not a missing new mechanism in the candidate.

A minor printed algebra slip in the thesis was checked explicitly rather than silently accepted. At the end of the proof of Lemma 2.2.4 on p. 28, write x=4A/W(n). The final displayed equality changes x^(n/2)+1 into (x+1)^(n/2). For n>2 this is generally an inequality, with the latter expression larger; for n=2 it is an equality. The immediately preceding fraction already gives the finite bound stated in the lemma, so dropping the last equality leaves the required bounded-ratio argument intact. Equivalently its final equality sign can be weakened to a less-than-or-equal sign for n>=2. This typography/algebra slip does not reopen the exact-target proof gap. A parent coordination message flagged this point after my own full-chapter read; I then independently rechecked the rendered page.

This was a source-level mathematical inspection, not a formal verification of every auxiliary theorem cited by Anné, CDE, or the thesis. No unsupported new theorem is required merely to recognize that the full target and its counterexample proof were recorded earlier.

## Chronology and corroboration

- OWR 33/2012: original workshop report and survey question. Workshop dates are 2012-07-01 through 2012-07-07; the report is in the 2012 volume. No more precise first-publication timestamp is inferred.
- Colbois's later survey: repository metadata says 2017, Contemporary Mathematics 700, pp. 1–40, DOI 10.1090/conm/700/14181. The inspected author PDF is dated 2017-01-31. Its Remark 49 on p. 35 restates the exact exponent \(1+2/m\) question and attributes its negative answer to Pétiard. Its lecture context is 2015, but I do not backdate the written negative-answer assertion to the lecture.
- Pétiard preprint: arXiv metadata records v1 at 2017-06-28 09:53:24 UTC, with only v1 displayed at retrieval. The downloaded PDF is visibly labelled v1. Its PDF creation timestamp is in 2022, which is a compilation/encoding timestamp and is not substituted for the arXiv submission record.
- Pétiard thesis: title page records successful defence on 2019-02-05; current repository metadata identifies the work as a 2019 doctoral thesis, DOI 10.35662/unine-thesis-2749, current handle 20.500.14713/31635. The present repository accession/availability fields are 2025-09-12, and its modification field is 2025-10-30. Those current-system fields are not evidence of the original 2019 upload date. Even those current-record dates precede both 2026 cutoffs.
- Colbois–Provenzano: first publication is recorded by the publisher as 2021-07-02. The complete Appendix A, printed pp. 2143–2145, was inspected in the journal-format repository PDF. Remark 4 on p. 2145 explicitly recognizes that the isoperimetric and index terms cannot in general be separated when \(p=2\), and bibliography item 37 identifies Pétiard's 2019 thesis. This supplies an independent dated pre-2026 primary-literature acknowledgement.

I did not identify or inspect a final journal version of Pétiard's 2017 preprint. None is needed for the narrower conclusion that an earlier recorded full proof exists, and no absence-of-publication claim is made.

## Classification of other material and limits

CEG arXiv:1007.0826v2, Theorem 1.1, is the multiplicative Euclidean estimate. Its Examples 3.1–3.2 were read in full: the first uses changing product ambient manifolds with two boundary components; the second uses complements of shrinking balls in a compact ambient manifold. They are related ambient counterexamples, not the exact Euclidean additive answer. CDE arXiv:0909.5346v1, Theorem 1.4 and complete §5, provides generic high-gap embedding and smoothing tools; by itself it does not state the target answer. Pétiard goes beyond these ingredients and records the needed spectral-union, ratio-control, and connectedness bridge.

The 2023/2024 Steklov survey and 2026 Steklov leads appeared in search results. Their returned metadata/snippets concern another operator; they were not used as theorem-level evidence and were not comprehensively inspected. The audit did not pursue an exhaustive global citation graph after the exact prior theorem and later journal acknowledgement were secured. It does not certify the earliest version of the result, the absence of still earlier work, independent rediscovery, or novelty of a specialized cavity formulation.

Final journal bodies of CDE and CEG were not compared line by line with their arXiv versions. This limits claims about version equivalence, not the direct priority finding based on Pétiard's complete preprint and thesis. Query and read receipts list those limits explicitly. All third-party PDFs, extracted text, HTML, JSON raw returns, and rendered pages remain under ignored private directories.

## Candidate and independence pin

The initial independent classification was sealed before reading any root proof, old audit, or concurrent review. It correctly classified CDE and CEG as insufficient by themselves; it was superseded by the later direct Pétiard discovery. Its SHA-256 is 19d1bee38976c0640dcadb5995e998dcd797aa7d222eb1258106b95944aed142.

Only after that seal was the supplied candidate read at `../../inputs/PROOF.md` relative to this review folder. The exact absolute path and start/end SHA-256 appear in RECEIPT.json. Both hashes were c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658, with 10412 bytes reported by the parent and independently byte-counted in the receipt. No old audit or concurrent review file was read; parent coordination messages were received, including the minor equality slip just described. No outreach, external messaging, git mutation, PR edit, release, tracker edit, or Zenodo operation was performed.
