# Independent original-source and prior-theorem review: PR1233 / 30000035

**Verdict: accept the full exact finite-generator characterization, with an explicit qualification about the original qualitative request.** Theorem 5.2 of Aldroubi–Cabrelli–Heil–Kornelson–Molter gives the required necessary and sufficient condition for every finite family in (L^2(\mathbb R)) and every fixed positive integer (n). It includes the original identity-Gramian setting and the scalar Fourier-support partition. I independently reconstructed the analytic proof, including the measurable-fiber and closure issues, and found no remaining formal mathematical gap. This is an existing result, not a new theorem of this project.

The 2004 abstract already acknowledges earlier characterizations. Its additional wish for a “similar characterization” that is not an “easy or direct consequence” is qualitative; I do not certify that preference, the author's intended degree of practicality, or independence from earlier methods. These qualifications do not remove any generators or values of (n) from the exact criterion. The separate approximate-invariance question is outside the exact target reviewed here. No claim of a component-support-only characterization, finite numerical decision procedure, global priority, or current openness is made.

This review is AI-assisted internal research, unrefereed, without external human peer review or proof-assistant certification. This statement concerns this review only; I make no assertion about the source authors' use of AI. No people were contacted, no author program was run, and no service or Git state was written. Root must read and adopt this review before any downstream action. Overall program completion remains **79%**; this independent review family is **100%** on closure.

## 1. Exact object and source custody

The binding is the open draft [PR1233](https://github.com/AlecKriebel/Math/pull/1233), head `e026f83da374407d6a020949feb738460b76aea3`, base `4b27092a448d53b61408355ce44ec38d103a1ce4`. All eight added blobs are confined to `unsolved_math_prioritization/attempts/30000035/`; no QUEUE path is changed. I read the complete fresh PR body and all eight blobs, including the separate 16,599-byte PROOF, 19,598-byte AUDIT, 2,163-byte ACCEPTANCE.json and the remaining five documents. Their exact Git blob SHAs, lengths and SHA256 values are in PR_BINDING.json, independently checked against the fetched bytes. A second live PR read retained the identical head, base, body, open state and draft flag. The public nested MANIFEST.json is checked as a payload as well as against its seven other payload entries. Historical checks and an earlier 33-member audit are historical claims, not fresh evidence replayed by this reviewer.

Before reading mathematics I made my own read-only GWS CLI fetch at **2026-10-22 07:13:15 UTC**, using numeric gid **1254632077**, columns **A:AQ (43 columns)** of spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`. The response contains 191 populated rows including the header, requested range `'Math Puzzles'!A1:AQ1178`. Body SHA256 is `fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1`. Full-width review and target/source/title/author/semantic scans found no equivalent record. Generic hits at rows 25 (observation Gramian), 160 (random lattice discrepancy) and 164 (triangle-count Weber precedent) are explicitly cleared in GWS_CLEARANCE.json. Bare `0804.1597`, its DOI aliases, all five authors, the original identifier and EMS aliases were checked; unresolved leads: **zero**. This is clearance of this fetched tracker, not worldwide novelty certification. B in the four-cell proposal is literally empty.

Primary sources were freshly fetched, authenticated and read independently of the PR's source descriptions:

| Source | Actual inspection | SHA256 of private PDF |
|---|---|---|
| [Aldroubi, Almost Translation Invariant Spaces, OWR10/2004](https://ems.press/content/serial-article-files/45879#page=9) | Complete original abstract and references, PDF pp.9–10, printed pp.487–488; p.9 visually checked | `061421de9750f944d51a8e99f8b85b5f902d997cba873aca38c59bdd582a0d11` |
| [Invariance of a Shift-Invariant Space, arXiv0804.1597v3](https://arxiv.org/pdf/0804.1597v3) | Identity page; relevant definitions and actual proof chain on pp.2–11, including 4.1–4.4, 4.7, 4.9–4.14 and 5.1–5.2; p.11 visually checked; public TeX source authenticated | `20339edf56c1e0581f20c5fd64b982b849ba1882bf45d75c42b7750e86bdb3f0` |
| [Chui–Sun, Tight frame oversampling and its equivalence to shift-invariance of affine frame operators](https://sciences.ucf.edu/math/qsun/wp-content/uploads/sites/10/2016/09/cs03.pdf) | Definitions and Theorem1 on pp.1–4; projection Lemmas1–2 and complete relevant theorem proof on pp.6–11 | `91e6f13f4ffaef11d1e1cb4dd506113bfffb4be96f5c92ba5b64f0a3f9d24b01` |

I do not claim to have read every page of these three PDFs. Unrelated support consequences, Bownik decomposition applications, higher-dimensional extensions, oversampling results imported by Chui–Sun and the approximate problem are not premises of the reconstructed proof.

The current [arXiv landing page](https://arxiv.org/abs/0804.1597) lists v1 on 10 April 2008, v2 on 15 October 2008 and latest v3 on 21 December 2008; no v4 was listed. The v3 PDF's 2018 typesetting date does not represent a later arXiv version or a new publication date. The same paper's journal identity is **Akram Aldroubi, Carlos Cabrelli, Christopher Heil, Keri Kornelson, Ursula Molter**, *Journal of Fourier Analysis and Applications* **16(1) (2010), 60–75**, [DOI10.1007/s00041-009-9068-y](https://doi.org/10.1007/s00041-009-9068-y). Fresh Crossref metadata gives online publication 1 April 2009 and print issue February 2010. The DOI returned HTTP200 and the correct Springer article HTML. The requested publisher PDF endpoint also returned article HTML: **no final journal-PDF proof-body comparison is claimed**. The operative primary proof read is v3, corroborated by its public TeX source; its journal association is authenticated metadata. Molter's current [publication page](https://mate.dm.uba.ar/~umolter/publications.htm), read in the web tool, links this journal entry to arXiv. A direct local fetch of that page failed DNS; no response-body receipt is invented.

SOURCE_ALIASES.json treats `0804.1597`, all its versions, [arXiv DOI10.48550/arXiv.0804.1597](https://doi.org/10.48550/arXiv.0804.1597), the journal DOI and publisher URLs as aliases of one paper, not different solutions. The original report is [EMS article720](https://ems.press/journals/owr/articles/720), [DOI10.4171/OWR/2004/10](https://doi.org/10.4171/OWR/2004/10), pp.479–544 overall. Chui–Sun is a separate older paper, *Proc. AMS*131(5) (2003),1527–1538, [DOI10.1090/S0002-9939-02-06703-5](https://doi.org/10.1090/S0002-9939-02-06703-5), electronically published 19 September 2002. No new upload or DOI reservation is proposed.

## 2. Original statement and its exact scope

The original author is Akram Aldroubi. On printed p.487 he fixes finite (\Phi=(\phi_1,\ldots,\phi_r)^T\in (L^2)^r), the space of integer-translate expansions with (\ell^2) coefficient vectors, and the identity Gramian (G_\Phi=I_r) almost everywhere. He asks to recognize (T_{1/n}V=V), then explicitly credits Weber for a special case and Chui–Sun for the general case. He presents the scalar (r=1,n=2) support partition and asks for a similar useful general characterization; p.488 contains the cited references. The next paragraph is a separate question about uniform projection error bounded by (\varepsilon).

The scalar display literally uses (\phi(\xi+2j)) and (\phi(\xi+2j+1)), without Fourier hats. Visual inspection confirms this is not text-extraction loss. The surrounding paragraph defines (\phi(x)=\sin(\pi x)/(\pi x)) in time and uses hats in the Gramian; no local change of convention was found. A literal time-support interpretation is false: for sinc, at every (\xi\in(0,1)) both residue classes have nonzero values, yet its bandlimited span is invariant under all real translations. With Fourier hats, the normalized scalar partition is correct. All such equalities and disjointness statements for (L^2) data must be read modulo null sets. The report and proposed row disclose this interpretation instead of silently asserting the literal printed formula.

Normalization also resolves a possible topology mismatch. (G=I_r) makes the integer translates of all (\phi_i) orthonormal, by Plancherel and the Fourier coefficients of the Gramian. Their synthesis from (\ell^2(\mathbb Z)^r) is an isometry onto a closed range; hence the original coefficient-defined (V) equals the norm-closed integer-shift span (S(\Phi)). Thus the rank theorem actually covers every original normalized generator family. No unjustified assertion about arbitrary unnormalized (\ell^2) synthesis is needed.

## 3. Independent analytic proof of the full criterion

Fix (r<\infty), (n\ge1), (\phi_i\in L^2(\mathbb R)), (S=\overline{\mathrm{span}}\{T_j\phi_i:j\in\mathbb Z,1\le i\le r\}). Fourier normalization is (\widehat f(\omega)=\int f(x)e^{-2\pi ix\omega}\,dx), extended by Plancherel. For (\omega\in[0,1)), put

\[
v_i(\omega)=(\widehat\phi_i(\omega+\ell))_{\ell\in\mathbb Z},\quad
J(\omega)=\mathrm{span}\{v_i(\omega):1\le i\le r\}.
\]

Let (Q_k) retain coordinates (\ell\equiv k\pmod n), and let (G_{ij}=\sum_\ell\widehat\phi_i(\omega+\ell)\overline{\widehat\phi_j(\omega+\ell)}); define (G_k) by summing over that residue class. The complete result is

\[
 T_{1/n}S=S\quad\Longleftrightarrow\quad
 \operatorname{rank}G(\omega)=\sum_{k=0}^{n-1}\operatorname{rank}G_k(\omega)
 \quad\text{for a.e. }\omega\in[0,1).
\]

**Fibers and measurability.** Tonelli gives (v_i\in\ell^2) a.e. and the unitary fiber map (\mathcal T:L^2(\mathbb R)\to L^2([0,1);\ell^2(\mathbb Z))). Its surjectivity follows by assembling the frequency function on the disjoint half-open cells (\omega+\ell). Gramian entries converge absolutely a.e. by Cauchy–Schwarz; they are measurable. Finite matrix ranks are measurable through their minors, allowing variable ranks and zero fibers. Endpoints are a null set; there is no hidden continuity or pointwise-everywhere premise.

Here is a direct finite-generator membership argument, avoiding any ambiguity about evaluating uncountably many (L^2) representatives at one point. Apply Gram–Schmidt measurably to the finite list (v_i(\omega)), setting a normalized residual equal to zero where that residual is zero. This constructs a measurable orthogonal projection (P_J(\omega)) with operator norm at most one, hence a bounded projection on the section space. Its range is exactly the square-integrable fields in (J(\omega)). For any field (h\), each scalar (b_i(\omega)=\langle h(\omega),v_i(\omega)\rangle\) is in (L^1[0,1)). Orthogonality to every integer translate of (v_i) means all Fourier coefficients of (b_i) vanish. Fourier uniqueness for (L^1), for example via Fejér approximation in (L^1), gives (b_i=0) a.e. Consequently the orthogonal complement of (\mathcal T S) equals the kernel of the pointwise projection, and

\[
 f\in S\ \Longleftrightarrow\ (\mathcal T f)(\omega)\in J(\omega)\text{ a.e.}
\]

**Translation and finite spectral projections.** (T_{1/n}) becomes the scalar (e^{-2\pi i\omega/n}) times (D\), where (D e_\ell=e^{-2\pi i\ell/n}e_\ell). Necessity (DJ\subseteq J) follows by applying invariance to the finite generators on one common full-measure set; sufficiency follows by the membership statement for arbitrary sections. Since (D^n=I), inclusion implies equality. The spectral projections are

\[
 Q_k=\frac1n\sum_{s=0}^{n-1}e^{2\pi i k s/n}D^s.
\]

Thus (DJ=J) iff (Q_kJ\subseteq J) for every (k). Always

\[
 J\subseteq\bigoplus_{k=0}^{n-1}Q_kJ,
\]

and the sum is orthogonal. These spaces are finite-dimensional, of dimension at most (nr). Inclusion plus equality of finite dimensions is equivalent to equality of spaces, hence to stability under every (Q_k). Finally (\dim J=\operatorname{rank}G) and (\dim Q_kJ=\operatorname{rank}G_k), yielding the criterion. For the original spaces, one-sided (T_{1/n}S\subseteq S) also gives equality since (T_{-1/n}=T_{-1}(T_{1/n})^{n-1}). The (n=1), zero-space, dependent-generator and rank-changing cases all remain valid. No frame lower bound, Riesz basis, full rank, bounded multiplier coefficient or nonvanishing assumption was introduced.

These deductions use standard Plancherel theory, Tonelli/Fubini, Cauchy–Schwarz, (L^1) Fourier uniqueness, Hilbert-space orthogonal-complement identities and finite-dimensional spectral algebra. Those foundations are named imports; this review is not a recursive reproof of their foundations. The finite-generator fiber membership statement itself is reconstructed above. Helson/Bownik range-function theory and the periodic-multiplier propositions explain the original proof route, but their full external proofs are not needed as unexamined additional hypotheses here.

## 4. Closure defect and its repair

In the authenticated v3, (U_k=P_kS) is the cutoff image. Lemma4.3 proves it closed under the hypothesis (U_k\subseteq S). Theorem4.4 validly characterizes invariance by that inclusion. However, Remark4.6 writes an unqualified equality of the image with (S\cap\operatorname{ran}P_k), and the later dimension/Gramian discussion speaks of the image as an SIS before establishing invariance. Read unconditionally these statements fail. If the preceding invariance hypothesis is retained, they are true. I do not infer that an uninspected final journal PDF has identical wording.

An explicit normalized scalar counterexample shows why this matters. Let (n=2), and, for (0<\omega<1), define

\[
 \widehat\phi(\omega)=\sqrt\omega,\qquad
 \widehat\phi(\omega+1)=\sqrt{1-\omega},
\]

with zero values elsewhere. Then (G=1); (S) consists of fibers (a(\omega)(\sqrt\omega,\sqrt{1-\omega})) for (a\in L^2(0,1)). The even-cutoff image has first components (\sqrt\omega L^2(0,1)), which is not closed. Indeed (g_N=\mathbf1_{[1/N,1)}) lies in that image since its coefficient has squared norm (\log N<\infty); (g_N\to1) with squared error (1/N), but coefficient (1/\sqrt\omega) is not in (L^2). The intersection (S\cap\operatorname{ran}P_0) is zero, whereas the image is nonzero.

The safe objects before invariance are

\[
 W_k=\overline{P_kS}=S(P_k\Phi).
\]

The equality follows because bounded (P_k) commutes with integer translations: images of finite translate combinations are dense in (P_kS), and each cutoff generator already lies in the image. The preceding fiber argument applied to (P_k\Phi) gives fibers (Q_kJ). After the rank test implies (Q_kJ\subseteq J), it follows that (P_kS\subseteq S); the image then equals (S\cap\operatorname{ran}P_k), a closed space. This repairs the dependency ordering without assuming the desired invariance. The PR's PROOF and AUDIT make the same necessary qualification. Theorem5.2's exact statement survives; no unresolved mathematical obstruction remains.

## 5. Normalization, scalar reduction and older work

If (G=I_r), the matrices (G_k) are positive semidefinite contractions and sum to (I_r). Their traces sum to (r), with each trace at most its rank. Thus the rank sum equals (r) iff every nonzero eigenvalue of every (G_k) is one, i.e. each is an orthogonal projection. Their sum being identity then makes their ranges mutually orthogonal: for (x\in\operatorname{ran}G_k), positivity and (\sum_j\langle G_jx,x\rangle=\|x\|^2) force all the other summands to vanish. If (a_\ell=(\widehat\phi_i(\omega+\ell))_{i=1}^r), the quadratic-form kernel identity for (G_k=\sum_{\ell\equiv k}a_\ell a_\ell^*) gives

\[
 \operatorname{ran}G_k=\operatorname{span}\{a_\ell:\ell\equiv k\pmod n\}.
\]

Hence normalized invariance is equivalent to orthogonality between frequency columns in different residue classes. This step depends essentially on (G=I); it is not a valid test for arbitrary unnormalized generators.

For (r=1), rank additivity says at most one residue class has any nonzero Fourier fiber entry. Under (G=1), exactly one does a.e.; for (n=2) this is precisely the corrected Fourier-support partition of the original abstract. Zero fibers in the unnormalized case need the phrase at most one.

The older Chui–Sun source is substantively relevant, not a bibliography token. Its Theorem1 states, in a finite tight affine-frame/dilation setting, equivalence between cross-frequency orthogonality and a measurable periodic unitary multiplier describing the extra shift. I read the proof using measurable projections onto the spans of residue-class frequency columns, including their measurable selection/Gram–Schmidt construction. Its Fourier convention has period (2\pi), which rescales to period one here. The written theorem includes tight affine-frame and oversampling hypotheses; I have not silently imposed those on arbitrary finite generators or used its unrelated imported oversampling results to prove the rank theorem. Its projection mechanism is earlier precedent, and the original author expressly credited its general characterization. Therefore neither the normalized orthogonality criterion nor its underlying mechanism is presented as a new contribution.

## 6. Adversarial controls and independent finite checks

The read-only independent_checker.py was written for this audit from the reconstructed proof, without executing or importing any author program. It uses exact rational Gaussian elimination and explicit `require` guards, which survive Python `-O` and `-OO`.

It exhausts all **729** real (2\times3) ternary matrices and **4096** real (3\times4) binary matrices. For each of these **4825** constant fiber models it compares Gramian rank additivity with a separate row-space test under the actual half-translation multiplier (D=\operatorname{diag}((-1)^\ell)), and independently checks the Gramian/row-rank identity. Each model can be realized by (L^2) generators constant on finitely many frequency cells. A further **320** scalar support patterns test (n=1,\ldots,5), including zero fibers, against direct spectral-projection stability. These are finite falsification checks supplementing the analytic proof; they are not a substitute for measurable-field reasoning or an exhaustive complex-analytic verification.

Specific controls reject the main tempting overclaims:

* Let (A) have rows ((1,1,1,1)/2,(1,-1,1,-1)/2), and (B) have rows ((1,1,1,1)/2,(1,1,-1,-1)/2), with columns indexed by frequencies0,1,2,3. Both have (G=I_2), and both components have the identical support ([0,4)). For (n=2), (A) has two orthogonal rank-one cutoff projections and is invariant; (B) has (G_0=G_1=I_2/2), rank sum4 and is not invariant. Thus componentwise supports alone and replacing ranks by traces both fail.
* The unnormalized matrix with rows ((1,1),(0,1)) spans the whole two-coordinate fiber and is invariant, although its two columns have nonzero inner product. This rejects using normalized orthogonality without normalization. Zero and dependent matrices reject an unstated full-rank assumption.
* An exact Gaussian-rational unitary rotation (U=\bigl(\begin{smallmatrix}3/5&4i/5\\4i/5&3/5\end{smallmatrix}\bigr)) preserves the normalized control's Hermitian Gramian; omitting conjugation does not. This explicitly guards the complex Gram convention, while the exhaustive runs themselves are real-rational.
* Finite generation matters. The closed span of (e_{2j}+e_{2j+1}), (j\in\mathbb Z), is not stable under the even/odd sign multiplier. Its own and both cutoff dimensions are countably infinite, so cardinal dimension equality would give a false test. No infinite-generator extension by infinite cardinal arithmetic is accepted.
* Exact rank is discontinuous. A normalized scalar fiber ((\sqrt{1-\varepsilon^2},\varepsilon)) approaches the invariant fiber ((1,0)) in (L^2), but fails half-shift invariance for every (0<\varepsilon<1). Finite samples can also miss a positive-measure failure set. The theorem is an exact a.e. condition, not a universal finite-precision algorithm. No impossibility theorem for all restricted representations or algorithms is asserted.

Normal, `-O`, and `-OO` runs pass with byte-identical JSON outputs. The checker also verifies exact PR and source pins, public nested manifest entries, the numeric43-column tracker fetch, same-paper alias clearance, the private-body seal and the exact recursive review closure. It refuses to call the publisher HTML a PDF. Actual private source/ledger bodies and page renders are not proposed as public materials.

## 7. Disposition and boundaries

CELL_PROPOSAL.json and CELL_PROPOSAL.tsv contain one concrete A:D literal row, with **B empty** and **C the existing journal DOI**. The notes credit all five authors, the older Chui–Sun mechanism, the original normalized and scalar scope, the closure repair, source-access limitations, review status and qualitative-interpretation limits. No new paper, new DOI, upload, service write, Git operation, queue action, publication or complete global accounting is claimed. Source aliases and semantic duplicate clearance are explicit rather than implied by a URL search alone.

The remaining boundary is interpretive: a formal exact necessary-and-sufficient generator criterion is fully established, while the original's unformalized presentation preference and separate approximate-invariance program are not certified. There is **no remaining formal mathematical gap in the finite-generator exact criterion**. Promotion is contingent on the parent's full read and adoption, and any changed head, body or payload requires a new binding and review. All closure members, including nested manifests and private bodies, are sealed; the only file excluded from REVIEW_SEAL.json is that exact seal file itself. Previous PR1219 and PR1230 review artifacts were preserved unchanged.
