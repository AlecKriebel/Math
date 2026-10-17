# Independent priority audit of PR 1135

Audit date: 2026-10-17 UTC. Exact target: problem 30000052 / OWR-723-005. Exact PR head: `e809a9c40f4ccdaced6f45f10b1dc8b7725a2119`.

## Decision and the chronology distinction

**NO IDENTIFIED PRE-PR FULL TARGET RESOLUTION, WITH VERIFIED POST-PR FULL OVERLAP.** This is a bounded finding, not certification of novelty or first discovery. There is a substantial, directly relevant preprint that any new release must cite and discuss: Alper Ferudun's *A Negative Answer to a Question of Novak on Randomly Shifted Lattices and the Expected p-th Power of the Lp Discrepancy*, posted 14 October 2026, [DOI 10.5281/zenodo.23372668](https://doi.org/10.5281/zenodo.23372668). Its exact-target negative answer is mathematically valid. It appeared after the source PR's server-recorded creation on 10 October, so it is not evidence that this source PR's claim was already resolved when recorded.

An independently verified alternative argument uses Su's 2000 Fourier identity and a classical Dirichlet-kernel moment recorded by Anderson–Ash–Jones–Rider–Saffari in 2007. **This is a new audit application of earlier tools, not an earlier paper already treating the exact expected anchored discrepancy law.** It proves the full negative answer but does not, by itself, establish historical prior resolution. It must not be mechanically labeled an `already_solved` priority exclusion merely because its ingredients have old dates.

Root retains the process/disposition decision. This report does not recommend skipping PR 1135 on either of those two grounds. It does require accurate contemporary framing: a current note cannot present the question as still unanswered as of its own release, omit Ferudun's broader overlapping work, or claim first publication from this bounded search.

This audit performed no PR mutation, comment, merge, close, paper preparation, deposit, tracker write, Git mutation, or external communication. It is an internal AI-assisted audit, not human peer review.

## 1. Exact target, success criterion, and excluded substitutes

For independent continuous uniform vectors \(Z,\Delta\in[0,1)^d\), the indexed points are \(t_j=\{jZ+\Delta\}\), \(0\le j<n\). The source compares the expectation of

\[
\operatorname{disc}_p(t)^p=
\int_{[0,1]^d}\left|n^{-1}\sum_{j=0}^{n-1}1_{[0,x)}(t_j)-\prod_r x_r\right|^p\,dx
\]

with its iid-uniform counterpart for even \(p\). A single strict reversal under this exact law disproves the universal comparison. The source PR supplies \(n=3,d=1,p=4\), with values \(19/1620>16/1620\), and an independent no-wrap-tail proof at \(n=4\). The exact norm power, normalization, anchored boxes, full continuous generator average, independent shift, and absence of conditioning are material.

The official [Oberwolfach PDF](https://ems.press/content/serial-article-files/45858), printed pp. 696–699, was read in context; physical PDF pages 25–26, printed 697–698, were also rendered and visually inspected. The source supplies the definition and comparison just described. Its final star-discrepancy existence question is separate. Results for a selected good generator, a fixed generator with only a random shift, a rational rank-one generator from a finite nonzero grid, jittered points, extreme boxes, \(p=2\) alone, or the expectation of the norm itself are not full answers to this target.

## 2. What the current overlapping paper actually proves

Primary materials were downloaded from [the author's publication page](https://eulersolve.org/papers/owr-723-005/): the 15-page PDF, source archive, verification report, and metadata. The reading-copy PDF has 182,528 bytes and SHA-256 `edb268431856eef5d6eb00e730d1a27a7e91a15d76186b506168f259dbbb174c`. Its entire text was read. The exact three-point proof and no-wrap-tail proof were also visually checked in the typeset pages. This audit independently verifies the analytic portion sufficient for the full target; it does not certify all of that paper's thousands of computer-assisted cases or adopt its reported verification runs as our own.

The paper's Theorem 1.2 states the same strict three-point values in dimension one and a positive difference in every dimension. The proof uses a circular-gap integral, rather than the source PR's direct three-inclusion area calculation. For the three circular points \(0,z,2z\) with \(0<z<1/2\), the gaps are \(z,z,1-2z\). Reflection treats the upper half. Direct integration gives

\[
\int_0^1\sum_i g_i^2\,dz=\frac12,
\qquad
\int_0^1\sum_i g_i^3\,dz=\frac5{16}.
\]

Uniform shift integration consequently gives the second-power maximum functional \(\phi_2=1/2-(5/16)/3=19/48\), while \(\phi_1=1/4\). Grouping the three-index terms in the elementary fourth-moment expansion yields, at \(d=1\),

\[
E_{\rm lat}-E_{\rm iid}
=\frac49\left(\frac25-\frac{19}{48}\right)=\frac1{540}.
\]

Together with the independently checked iid value \(4/405\), this recovers \(19/1620\). These steps have no unavailable lemma or computer-assisted dependency. The 129-control program accompanying this audit recomputes the gap integrals and strict margin exactly, without importing a source-PR or external-paper program.

The later paper's progression-event argument extends the source PR's second mechanism to all even exponents and fixed dimensions. Its two disjoint no-wrap generator regions and the two outer empty intervals give the one-dimensional lower bound \(4/[(p+1)(p+2)(p+3)(n-1)]\). Conditional expectation and Jensen add the factor \((p+1)^{1-d}\). The iid centered-moment bound then gives failure for sufficiently large \(n\). This analytic argument is valid and is more than enough to settle the original universal question. The paper explicitly distinguishes the moment from the expected norm, chosen generators, and high-dimensional regimes; those distinctions are correct.

The mathematical overlap is extensive: exact three-point values, equality at \(n\le2\) and \(p=2\), and the same rare no-wrap progression mechanism. The three-point derivations use different representations. Neither similarity nor chronology proves copying, dependence, awareness, or independent discovery. This audit makes no such causal attribution.

## 3. Verified dated records

Fresh read-only GitHub API evidence records:

| Record | Exact fact |
|---|---|
| [PR 1135](https://github.com/AlecKriebel/Math/pull/1135) | Created and last updated `2026-10-10T11:34:20Z`; currently open draft; exact unchanged head above. |
| Sole PR commit | Author and committer dates `2026-10-10T11:33:05Z`; commit message identifies the counterexample. |
| PR body | Already explicitly states \(19/1620>16/1620\), the \(n=4\) tail comparison, and the full negative outcome. |
| Repository | Currently public. This audit did not obtain a historical visibility archive; it does not infer first public availability solely from Git author dates. |
| [Zenodo record 23372668](https://zenodo.org/records/23372668) | API `created=2026-10-14T14:58:42.560423+00:00`, `updated=2026-10-14T14:58:43.020327+00:00`; version `1.0`; preprint, not a journal article. |
| Author metadata | Manuscript date and stated first public online release date both 14 October 2026. |

The site-hosted PDF, ZIP and verification-report bytes match every size and MD5 checksum in the retrieved Zenodo record; their SHA-256 values also match the site's metadata. Direct Zenodo file/version-list requests were refused, so no successful direct-file download is claimed. The successfully retrieved canonical record metadata authenticates the file-list comparison. The paper is explicitly AI-assisted and unrefereed; a DOI is not peer review. No earlier version was identified in the successful metadata, but a failed version-list request is not proof that no other release exists.

Chronology supports the narrow statement that the dated PR record precedes the identified dated preprint record by four days. It does not alone prove first discovery, first publication, or all possible earlier availability. The PR claim predates the later record; a current publication should transparently cite the later paper and preserve this distinction.

## 4. The Fourier/Dirichlet route: full new audit proof, old ingredients

The root supplied a candidate mechanism from a materially distinct priority family. I independently fetched and read the relevant primary bodies and reconstructed the entire bridge, including constants and boundary cases.

Su's [author-hosted reprint](https://math.hmc.edu/su/wp-content/uploads/sites/10/2019/06/A-LeVeque-type.pdf), *A LeVeque-type lower bound for discrepancy*, published in the 2000 MCQMC proceedings, printed pp. 448–458, has 236,076 bytes, SHA-256 `0cbb07f38ab5e30700208c66831c6917497bea453a963d9a7db6bedd422003bf`. The proof of Lemma 4 on printed 450–451, physical PDF pages 3–4, gives the nonzero Fourier coefficients of a cumulative-distribution discrepancy. Its constant \(K\) makes that function mean zero. Changing \(K\) affects only the zeroth coefficient. The result concerns a general probability measure; it does not analyze the continuous-generator expected \(L_4\) law in the target. One must use the coefficient identity itself, not incorrectly infer an \(L_4\) lower bound from a bound on the supremum.

Anderson, Ash, Jones, Rider and Saffari's [2007 AIF article](https://aif.centre-mersenne.org/articles/10.5802/aif.2298/), *Exponential sums with coefficients 0 or 1 and concentrated Lp norms*, defines the \(n\)-term kernel in Eq. (1.1) and gives its \(p\)-moment growth in Lemma 2.1, printed 1383–1384, physical PDF pages 8–9. The PDF has 540,419 bytes, SHA-256 `35b5354d153b430ba9dc3c2043a0729385b2a67469064548fb6c113e80b588f9`. This is a generic kernel norm theorem, with \(p>1\); it does not state Novak's comparison. Its leading constant is positive because the displayed sinc-power integral is positive near zero. At \(p=4\), elementary orthogonality gives an exact formula, so no asymptotic error estimate is needed below.

Here is the complete target-specific application, newly checked in this audit. For an arbitrary indexed one-dimensional configuration set

\[
F(x)=n^{-1}\sum_j1_{[0,x)}(t_j)-x,
\qquad e(x)=\exp(2\pi i x).
\]

Direct integration, valid even with repeated points or a point at zero, gives

\[
\int_0^1 F(x)e(-x)\,dx
=\frac{1}{2\pi i n}\sum_j e(-t_j).
\]

For example, each indicator integrates from \(t_j\) to 1, giving \((e(-t_j)-1)/(2\pi i)\); the integral of \(x e(-x)\) is \(-1/(2\pi i)\). Thus no endpoint boundary term is being discarded. Hölder on a probability interval gives

\[
\operatorname{disc}_4(t)^4=\|F\|_4^4
\ \ge\ \frac{\left|\sum_j e(-t_j)\right|^4}{16\pi^4 n^4}.
\]

For \(t_j=\{jz+\Delta\}\), the shift is a factor of modulus one. The remaining sum is exactly the source's \(n\)-term Dirichlet kernel. Its fourth moment is the additive-energy count

\[
\int_0^1\left|\sum_{j=0}^{n-1}e(jz)\right|^4dz
=\#\{(a,b,c,d)\in\{0,\ldots,n-1\}^4:a+b=c+d\}
=n^2+2\sum_{k=1}^{n-1}k^2
=\frac{2n^3+n}{3}.
\]

Integrating the preceding inequality over the actual full generator and shift cube proves

\[
E_{\rm lat}(n,1,4)\ge\frac{2n^2+1}{48\pi^4n^3},
\qquad
E_{\rm iid}(n,1,4)=\frac{3n-1}{30n^3}.
\]

The lower bound is of order \(1/n\), and the iid moment is of order \(1/n^2\); hence this is a complete negative answer. For a fully explicit coarse instance, use only \(\pi<4\) and \(n=1000\): the rational lower-bound excess is \(3858053/61440000000000>0\). Using the standard sharper \(\pi<22/7\), \(n=234\) already has certified rational excess \(5893/4262484695040>0\). After clearing denominators, the comparison for every \(n\ge234\) reduces to a quadratic whose coefficients after \(n=234+t\) are

\[
5975502/2401,\quad33687216/2401,\quad60,
\]

all positive. No claim of an optimal threshold is made. This coarse bound does not prove the exact \(n=3\) result, and the program explicitly rejects that misuse.

The exact checker uses standard-library rational arithmetic, enumerates the energy independently in two ways, reconstructs iid moments by integrating the complete binomial expansion, verifies both explicit thresholds, and reproduces the later preprint's relevant gap integrals. It has 129 checks including five adverse controls; normal and optimized Python outputs agree byte for byte. It imports neither the PR's verifier nor any external author's program. The analytic proof, rather than finite checks, establishes the identity for every positive integer n.

**Epistemic assessment.** The central application is choosing a nonzero Fourier coefficient of the *anchored* discrepancy, recognizing the shift cancellation and shared continuous-generator Dirichlet law, then averaging its fourth moment and comparing the iid normalization. That is a target-specific new audit argument. The source theorems supply its ingredients but do not state this application or already cover the exact averaged anchored-(L_p) comparison. Every proof uses earlier mathematical tools; the existence of this short proof therefore cannot alone certify an earlier published answer. Accurate old-tool credit is required if this route is used, with the new application labeled as such. There is no unsupported central lemma left in this route, but there is also no dated earlier target-resolution document supplied by it.

## 5. Broad earlier-source coverage and exclusions

The actual query ledger contains 52 queries in 13 batches, including exact and semantic formulations, quoted fractions, `generalized/generalised lattices`, random rotations, random Weyl sampling, higher moments, `Open Problem 41`, original authors and titles, and current literature through the audit date. Some broad/German variants returned unrelated results; those failures are recorded and provide no novelty evidence.

Forward-citation discovery included the exact report title, inspected bibliography references, and a fresh OpenAlex query for the report DOI. The index returned three citing works, all screened below; it omits other known citers already found from their primary reference lists, so its three is not an exhaustive count. Crossref rate limits and unavailable full bodies are retained in receipts. Abstracts/index metadata are discovery aids; they are not substituted for a theorem-level exclusion when a body was unavailable.

| Primary work and inspection | Relevance and precise limit |
|---|---|
| Novak/Hinrichs, OWR 13/2004, pp. 696–699 | Full source contribution read, original target rechecked visually. It poses the comparison and develops iid formulas, not a negative answer. Original references identify star-discrepancy existence/bounds and Banach-space probability; no target answer is asserted there. |
| Novak/Woźniakowski, author-hosted prepublication PDF of *Tractability of Multivariate Problems*, Vol. II (2010), §9.8.1, physical and printed p. 69 | Exact law and moment comparison reappear as Open Problem 41. The [668-page author PDF](https://web.maths.unsw.edu.au/~josefdick/preprints/Novak_Wozniakowski_book_2.pdf) is 4,724,291 bytes, SHA-256 `941c51b4aa6271abca9ff8ed800b1b341452aaace2ad36c64b8d608324c2b84a`. This is affirmative evidence of the same question's formulation at that time, not evidence of present openness. Final-book pagination/body was not conflated with this preprint. |
| Gnewuch (2005), *Bounds for the average Lp-extreme and the L∞-extreme discrepancy* | Publisher full PDF obtained; introduction, symmetrization framework, results and source reference read, full text screened. The random variables are iid; the object is principally extreme discrepancy. It corrects/suspects an iid symmetrization error in the 2004 note. It does not analyze the shared continuous generator. |
| Steinerberger (2010), *The asymptotic behavior of the average Lp-discrepancies and a randomized discrepancy* | Publisher full PDF obtained; target definitions, principal theorems and references inspected, full body screened. Its average is over iid uniform point tuples, and its separate randomized discrepancy has a different definition. No exact target answer is supplied. |
| Hinrichs/Weyhausen (2012), *Asymptotic behavior of average Lp-discrepancies* | Primary publisher abstract and primary 20-page talk slides obtained; actual VoR full body requests failed. The inspected material is about independent-point asymptotics. A complete journal-body exclusion is not claimed. |
| Hinrichs (2013), *Discrepancy, Integration and Tractability* | The [author-hosted proceedings preprint](https://web.maths.unsw.edu.au/~josefdick/MCQMC_Proceedings/MCQMC_Proceedings_2012_Preprints/133_hinrichs_plenary.pdf), 282,173 bytes, SHA-256 `4a9fe355f90eda51b587e932234b38f273ea54a1c8d44d8831b7ac5a1a5f4015`, was retrieved. Sections 3–4 and all source-reference context read; full text screened. §3 explicitly assumes iid points. §4 concerns a different structured deterministic construction on lower-dimensional diagonal subspaces and Open Problem 42. This closes the previous preprint-access gap, without claiming comparison to the final typeset edition. |
| Novak/Pillichshammer, arXiv:2512.08364v1 (9 Dec. 2025), *Generalized Discrepancy of Random Points* | Full arXiv PDF obtained, definitions/background, both importance-sampling regimes, discrepancy/moment sections and references inspected; full body screened. It changes iid sampling densities and weights; it does not replace independence with the shared-generator law. Current arXiv metadata lists only v1. |
| Same authors, *Upper bounds for generalized Lp-discrepancy of random points*, J. Complexity 95 (Aug. 2026), 102028 | Primary publisher/institution metadata and indexed body excerpts checked, Crossref confirms journal title/date. Direct VoR HTML/PDF/API requests did not deliver a full body. The arXiv v1 is not silently treated as the final journal text. No complete final-body exclusion is claimed. |
| Sinescu (2009), shifted lattice weighted discrepancy | Publisher indexed §3 and an institutional full thesis, Chapter 7, inspected. The generator is a rational rank-one vector with nonzero components coprime to \(n\); rational shifts and weighted star-discrepancy construction/existence are used. This is a different ensemble and functional. The thesis is not claimed to be byte-identical to the journal article; the actual publisher VoR body was unavailable. |
| Wnuk/Gnewuch/Hebbinghaus, arXiv:1904.10796v3 (2020 chapter) | Actual §4.2, Theorem 4.6 and surrounding definitions read. It uses a finite nonzero grid generator, prime point count, random permutation, finite shift and independent jitter. Its pairwise negative-dependence conclusion is not the target's continuous unjittered high-moment comparison. |
| Sugita (2016), *Random Weyl sampling—A secure Monte Carlo integration method* | Primary full PDF retrieved, §3.2/Theorems 4 and 6 read, whole text screened. It supplies pairwise independence and variance equality for a finite-resolution Weyl scheme; it does not compare the target fourth moments. Original Sugita/Takanobu (2000) and Sugita (2002) full bodies were not obtained; no claim that all their content was excluded is made. |
| Dolgopyat/Fayad, *Deviations of ergodic sums for toral translations II. Boxes*, arXiv v3 (2020) | Primary full PDF obtained, introduction and main law inspected. The discrepancy is unnormalized visit count for random boxes and a Cauchy weak limit under logarithmic normalization. Such weak convergence does not itself give the required fourth-moment comparison: the tail/moment bridge would need justification. It is not counted as an earlier target resolution. |
| Dick/Hinrichs/Pillichshammer (2020), periodic L2-discrepancy of Korobov p-sets | Actual arXiv body and relevant remarks inspected. Periodic L2 and finite Korobov constructions differ; the referenced polynomial construction problem is Open Problem 40, not the target. |
| Cesaratto/Vallée (2012, 2016) and Cesaratto/Plagne/Vallée (2006) | Primary landing pages/abstracts for the later two were obtained, but full-paper URLs returned HTML, not PDFs; this is recorded. The 2006 author full PDF's model and main theorem were read. Arnold's circular gap statistic, rational inputs and convergent-dependent truncations differ from the fixed-\(n\) continuous shifted anchored moment. These are contextual sources; a complete exclusion of the inaccessible 2012/2016 bodies is not asserted. |
| Su (2000), Anderson–Ash–Jones–Rider–Saffari (2007) | Exact relevant bodies/normalizations and proofs checked as above. Classical ingredients for a new complete audit proof, not a documented old solution to Novak's comparison. |

## 6. Release implications and remaining bounds

The current mathematical result is sound. The priority evidence supports transparent publication of the dated source-PR result with the later broader preprint prominently cited, subject to root's own decision and the required new whole-package reviews. A prospective paper must distinguish the date of the source PR, the date of the external preprint, and its own new release; call all unrefereed work accurately; preserve the original proof pin; and avoid asserting an exclusively new negative answer as of today. The later author's exact overlapping values and broader scope must be fairly acknowledged. No finding in this report establishes authors' awareness or intellectual dependence.

No earlier *explicit full-target answer* was identified in the inspected literature. Several source bodies/final editions remain unavailable, forward-citation coverage is incomplete, and an unindexed or unpublished prior answer is possible. A dated open-problem label and unsuccessful queries cannot settle those gaps. These limits must survive in global research notes and any package description; they are not mathematical gaps in either the PR proof or the newly checked Fourier proof.

The report and metadata are the authored audit artifacts. All downloaded third-party bodies, extracted texts, HTML, ZIPs and rendered images remain under ignored `sources/private/`; temporary files remain ignored. `INPUT_PINS.json` ties this audit to every frozen PR input. `ARTIFACT_RECEIPT.json` pins all authored deliverables and excludes itself.
