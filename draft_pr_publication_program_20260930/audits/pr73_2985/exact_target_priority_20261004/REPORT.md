# Exact-target historical priority audit: PR73 / 2985 / K3 4.109

Assigned immutable head: `6f82e81631fd43abc0140a831acfb43c150f4210`. This audit verified the restricted candidate/target file hashes, not Git HEAD. Mathematical validity had already passed its separate gate; this report does not reopen proof search or authorize promotion.

## Verdict

**`LITERAL_PRIOR_EXISTS__CONNECTED_4D_PRIORITY_NOT_DEFEATED_IN_BOUNDED_SEARCH`.**

Auroux's disconnected four-dimensional counterexample, proved in Giroux's Proposition 9, already defeats the literal formulation if “surface” permits disconnected surfaces. It can also be expressed at degree one after rescaling the symplectic form. An unqualified claim to the first negative answer to K3 Problem 4.109 would therefore be historically misleading.

In the bounded search documented here, no earlier connected four-dimensional counterexample or theorem implying the candidate's exact strengthened conclusion was found. The candidate's potential additional contribution is the explicit free quotient yielding a connected genus-three surface at degree one and the obstruction visible in a double cover. This is a cautious priority assessment, not proof of firstness. A defensible description should credit Auroux/Giroux for the ingredients and distinguish the connected four-dimensional extension.

The independent FIRST conclusion was sealed at **2026-10-04T18:17:43.686645+00:00**, 6100 bytes, SHA-256 `54d01b63bb68eb80acc86a832630124328bb80449ebdb1155b777ddc54c5f39a`. Later literature and permitted legacy exposure did not change that verdict.

## Exact scope of the original question

The [K3 author PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed p.281, asks about the complement of an arbitrary prescribed symplectic surface in a closed symplectic four-manifold, where its homology class equals the Poincaré dual of an integer multiple of the symplectic class. The two remarks concern, respectively, standard symplectic projective plane and symplectic isotopy, and the existence of suitable representatives at sufficiently large degree, with effective bounds desired. Scribes are L. Starkston and J. Van Horn-Morris. The complete statement and both remarks were read in the source; copyright extracts and page pixels remain private.

No explicit connectedness restriction appears there, and no general connectedness convention was located in the global/chapter material actually inspected. The §4.9 definitions, printed p.263, describe closed nondegenerate symplectic forms, Weinstein domains through exact forms and gradient-like Liouville fields, and Stein domains through strictly plurisubharmonic functions. The book's surface convention in Chapter 2 is chapter-local. It does not settle connectedness for this question. Consequently both the literal disconnected reading and the connected interpretation must be reported.

For a nonempty surface with the stated class, positivity of its symplectic area forces a positive integer degree. Its square is positive. The candidate's degree-one connected surface therefore falls within the principal prescribed-surface question. Its topological obstruction excludes any Weinstein structure, including the requested one compatible with the specified form.

The quantifiers matter:

| Claim | Consequence of candidate, given the passed mathematical gate |
|---|---|
| Every prescribed representative in every closed symplectic four-manifold has Weinstein complement | False, including the connected interpretation |
| A given manifold/form has some good representative of degree one | Not decided; another representative may work |
| Standard symplectic \\(\\mathbb{CP}^2\\) specialization | Not decided |
| Effective degree guaranteeing existence of some good representative | Not decided |
| First disconnected four-dimensional negative example | Already prior |
| Earlier connected six-dimensional negative example | Already prior; does not itself defeat connected four-dimensional priority |

The open complement and the interior of a compact exterior have the same homotopy type. The finite-cover homology obstruction is independent of choices in this compactification.

## Decisive earlier result and its exact implication

[Giroux, arXiv:1803.05929v1](https://arxiv.org/pdf/1803.05929v1), Proposition 9 and its complete proof on manuscript pp.8–10, attributes the counterexample to Auroux. The journal proof on pp.376–377 was also read in the [official publisher PDF](https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806164162696916994-1806164162696916994-81adc96e8c20b5a15ee58b5d30edbc95.pdf). It constructs disconnected symplectic hyperplane sections of \\(T^4\\), with non-Weinstein complement; parallel copies give arbitrarily large even degrees. The ingredients include two integral symplectic forms \\(\\omega_1,\\omega_2\\), the standard form \\(\\omega=(\\omega_1+\\omega_2)/2\\), and disjoint genus-three surfaces \\(W_1,W_2\\) whose union represents \\(\\operatorname{PD}(2[\\omega])\\).

Here is a checkable implication to the original literal target, rather than a keyword comparison. Let \\(M=T^4\\setminus\\operatorname{int}\\nu(W_1\\sqcup W_2)\\). Excision and the Thom isomorphism give
\\[
H_4(T^4,M;\\mathbb Z)\\cong H_2(W_1\\sqcup W_2;\\mathbb Z)\\cong\\mathbb Z^2.
\\]
The fundamental class maps \\(1\\mapsto(1,1)\\). Exactness of the pair sequence therefore injects
\\[
\\mathbb Z^2/\\langle(1,1)\\rangle\\cong\\mathbb Z
\\quad\\text{into }H_3(M;\\mathbb Z).
\\]
A Weinstein four-manifold has the homotopy type of a CW complex of dimension at most two. Thus this complement cannot be Weinstein. This supplies a negative answer for the prescribed disconnected surface. With ambient form \\(2\\omega\\), the same union has class \\(\\operatorname{PD}([2\\omega])\\), hence degree one. It still has two components.

The printed proof's broad assertion that distinct parameter vectors automatically give disjoint cross-pair tori is stronger than required and is not valid for every distinct pair. Choosing
\\[
a=(0,0,1/4,1/4),\\qquad b=(1/2,1/4,0,3/4)
\\]
satisfies the four required cross-pair inequalities. Small local smoothings then preserve disjointness. This repair preserves the existence of the prior example; it does not erase its historical priority.

Giroux's Theorem 2 is an existence result for suitable high-degree sections, not a theorem that every representative is good. Proposition 10 imposes connectedness in dimensions at least six. Neither statement produces the candidate's connected four-dimensional result.

## Candidate's additional step

The restricted candidate uses these torus ingredients with the free symplectic involution
\\[
\\tau(x_1,x_2,x_3,x_4)=(x_1+1/2,x_2,-x_3,-x_4),
\\]
exchanging the two disjoint genus-three surfaces. In the quotient \\(X=T^4/\\langle\\tau\\rangle\\), their image is a single connected surface \\(\\Sigma\\) of genus three. Its class is \\(\\operatorname{PD}([\\Omega])\\) for \\(\\Omega=2\\bar\\omega\\), with square four. The complement has a double cover with the nonzero \\(H_3\\) just discussed. Covers of a CW complex of dimension at most two retain that dimension bound, so a Weinstein complement downstairs would contradict the upstairs homology.

This precise quotient/descent step was not found in the primary sources actually read. It is mathematically close to Auroux/Giroux's construction. That closeness requires explicit attribution, even if the connected extension is eventually established as new.

## Connected prior examples and potentially implying literature

The primary [Roux divisors post and complete Auroux comment](https://symplectosaurus.wordpress.com/2020/03/06/roux-divisors/) were read. The post is dated March 6, 2020 (modified March 9); Auroux's comment bears March 6, 2020 at 4:10 pm, with no verified site time zone. It describes a smooth connected hypersurface in \\(T^6\\) by smoothing the intersections of product divisors using a normal-bundle section. Its complement has a nonzero four-dimensional cycle, detected by a relative dual cycle. This is a genuine smooth connected counterexample in dimension six. The post's separate four-dimensional singular-divisor discussion is a question, not a proof of the exact target.

[Tonkonog–Varolgunes, arXiv:2003.07486v2](https://arxiv.org/pdf/2003.07486v2), pp.7–9, Remark 1.27 and footnote 4, explicitly connect Giroux Proposition 9 with the blog's smooth connected \\(T^6\\) construction. Their primary body corroborates the distinction; it supplies no dimension reduction to four or free quotient of the four-torus example in that passage.

[Diogo–Lisi, arXiv:1804.08014v2](https://arxiv.org/pdf/1804.08014), pp.1–7, define smooth symplectic hyperplane sections by the cohomology condition. Definition 2.1 explicitly distinguishes the optional Weinstein assumption, while Lemma 2.2 proves a Liouville compactification. The actual lemma proof was read. Exactness and a contact boundary do not imply a Weinstein handle decomposition.

[Acu et al., arXiv:2012.08666v2](https://arxiv.org/pdf/2012.08666), intro and §6 pp.42–45, include obstructions for complements of smoothed toric divisors. Their nonexact cases violate the target cohomology condition, which makes the complement form exact. For a full toric divisor representing the anticanonical class, proportionality to the symplectic class places it in the monotone setting where the inspected Weinstein theorem applies. Torus examples of nonpositive square after many blow-ups also cannot satisfy the positive-square target. This excludes those specific apparent matches, not every theorem in the lengthy memoir.

[Oba, arXiv:2404.14028v1](https://arxiv.org/pdf/2404.14028), pp.1–3, proves a non-Stein-fillability obstruction for circle bundles over symplectic bases of dimension at least four. The paper explicitly explains that the result fails in general for surface bases. A normal circle bundle over the candidate surface has a two-dimensional base. The inspected theorem therefore gives no earlier connected four-dimensional implication.

OpenAlex was used only as a discovery index: all 16 indexed citing records for the Giroux DOI were retrieved and their titles inspected. The dates in that index are not treated as evidence of dissemination; one obvious date anomaly illustrates the limitation. The relevant primary bodies above were then checked. The other cited papers' full proofs were not read and cannot be claimed excluded.

## Dating and problem-list provenance

Giroux's nominal journal citation is *Pure and Applied Mathematics Quarterly* 13(3) (2017), 369–388, DOI [10.4310/PAMQ.2017.v13.n3.a1](https://doi.org/10.4310/PAMQ.2017.v13.n3.a1). The actual publisher title page says received January 9, 2018. The manuscript's internal date is December 2017; that is not itself verified public dissemination. The arXiv record establishes public v1 submission on **March 15, 2018, 18:11:56 UTC**. Crossref gives print year 2017 and a creation timestamp in November 2018; neither resolves the actual journal public-release date. Accordingly the safe public-priority anchor used here is arXiv v1 in March 2018, with Auroux credited by the primary proposition.

Auroux's thesis title page records defense January 22, 1999; this is a manuscript/defense date, not measured public availability. Printed p.7/PDF p.11 retains the existence assertion of two disjoint components, each genus 2k²+1, in class PD(2k[ω₀]) for ω=4πω₀. It sketches splitting the symplectic form into orthogonal forms and desingularizing flat tori, while not displaying Giroux's explicit four affine equations. Rescaling to Ω₀=ω/(2π)=2ω₀ puts the assertion in degree k; at k=1 the components each have genus three. The same Thom-sequence argument above then gives the literal disconnected obstruction, conditional only on the asserted existence, whose explicit proof is in Giroux. Thus the numerical existence assertion/sketch is already in the thesis, rather than wholly missing.

My initial FIRST discussion interpreted the blog's “cut” remark too broadly and did not recognize this retained assertion. FIRST remains immutable. After a post-FIRST ROOT/sibling source lead, I re-read the relevant page in my independently cached pre-FIRST thesis and rendered/visually checked it. This corrects the chronology without changing the typed priority verdict or establishing an earlier connected example. The distinction is between the retained assertion/sketch and omitted explicit details. The author's current Harvard PDF was also independently fetched after the lead; its bytes differ from the Polytechnique copy, so byte identity is not claimed. Server Last-Modified headers are not treated as independently measured historical public availability. There was no external communication; Giroux's private-communication reference remains unavailable.

K3 is the 2026 AMS volume 295 edited by R. İnanç Baykur, Robion Kirby and Daniel Ruberman. The [AIM workshop report](https://aimath.org/pastworkshops/kirbylistrep.pdf), all four pages read, documents the October 30–November 3, 2023 collecting/editing workshop. K3's introduction was read for compilation conventions and chronology. The [editor's current page](https://sites.google.com/brandeis.edu/ruberman/home) points to the book and future updates; the [AMS supplemental-material page](https://www.ams.org/publications/authors/books/postpub/surv-295) displayed book metadata and author contact information, without an errata or problem-resolution link in its inspected body. No contact was attempted. Berkeley and UMass author PDFs were independently retrieved and byte-identical.

Searches of current “open” datasets were used as locators only. Such labels are not evidence of novelty. The older K2 problem numbered 4.109 concerns a different question and cannot be substituted for this target.

## Independence, custody and residual limits

Before FIRST, project exposure consisted solely of the two specified pristine inputs plus applicable instructions and the read-only PDF skill. No original source_record/background, legacy audit, ROOT/sibling opinions, old review/checker, Git state or audit logs were read. Genuine public primary sources and independent web searches supplied the historical evidence.

After FIRST and explicit ROOT permission, one legacy SOURCE_AUDIT.md was read at 18:19:29 UTC. Its hash and exact path appear in EXPOSURE_LEDGER.json. It agrees about scope and Auroux/Giroux ingredients; it does not establish earlier connected priority. No earlier full exact-priority report was invented. ROOT's subsequent publisher URL was a custody lead; this audit had already independently retrieved/read that PDF before FIRST. A later ROOT message relayed a sibling's factual thesis-page reading and Harvard locator; this was post-FIRST cross-family source-lead exposure, explicitly recorded. I then re-read my own primary copy. No full ROOT/sibling mathematical or priority report was read.

The search is bounded: 48 independent pre-FIRST textual queries, 3 post-FIRST queries, primary source bodies as recorded, bibliographic forward/backward chains, and 16 indexed citing records. It is not an exhaustive review of every symplectic-topology paper, every dissertation, nonindexed literature, or unpublished work. No author contact is permitted. DOI/old publisher routes failed but the actual publisher PDF was recovered. A toric version-specific URL failed but the unversioned PDF returned v2. The editor-linked Google Drive copy and all full bodies of the remaining indexed citers were not obtained/read. General non-Weinstein Liouville examples mentioned in Giroux's bibliography were not all separately inspected; no qualifying compactification theorem from them was found in the searches. The earliest journal public-release date remains unresolved.

All source PDFs, HTML, extracts, rendered pages, web-result streams and literal command stdout/stderr remain in the private cache outside Git. Public files contain this audit's prose/code, small receipts and hashes. Actual child argv/cwd/PID/UTC/exit and prelaunch pins are preserved by run_child.py. Web observations have observation times and returned result payloads, with no invented child process metadata. The final manifests and readback report state their closure-tail boundaries explicitly. No shared Git, native task, PR, editor, paper, upload or tracker mutation was performed.
