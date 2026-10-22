# PR1257 / 30005416: independent original-source, mathematics and prior-publication audit

Audit date: 22 October 2026 UTC. Immutable PR head: `e81d140d4aabfa35adb01d12a1677035fd3fa1f2`; base: `4b27092a448d53b61408355ce44ec38d103a1ce4`. All eight added files and the PR description were read. The comparison changes no QUEUE line. This review is independently authored; it executes no source-author program, changes no external service or Git state, and contacts nobody. Research-family completion: 100% for this bounded audit; overall parent sweep: 80%. Completion does not certify worldwide novelty of the separate normal converse.

## Decision

The unrestricted ADE-characterization question has a complete negative answer: the reduced crossing surface `xy=0` in affine three-space, at its origin, has exactly the ADE scheme-theoretic centered-arc Hilbert series and is not ADE. This follows directly from an already published theorem of Clemens Bruschek, Hussein Mourtada and Jan Schepers (BMS). It is not a novel result of PR1257. The original question contains no normality restriction; uncertainty about unstated historical intention does not prevent recording this literal negative answer, with its category explicit.

An existing-publication accounting row is justified for this literal negative answer alone, crediting BMS and their journal DOI **10.1007/s11139-012-9401-y**. The journal DOI, bibliographic metadata and author-authenticated preprint relationship are verified. The actual full journal PDF was not retrieved: the requested PDF endpoint returned HTML with HTTP200. The exact crossing formula and its definition of the invariant were independently read in both the full 2011 preprint and the actual published 2011 proceedings PDF, DOI **10.46298/dmtcs.2904**. Thus the result's published status does not rest on an abstract or an assumed identical journal payload. A single family row, retaining both publications as aliases, suffices; no new upload is appropriate.

The PR's further pinch-point calculation and its characteristic-zero normal finite-type surface converse are mathematically supported within their stated restrictions. The proofs below survived deliberate counterexample and infinite-limit checks. They are **not** established as prior BMS results, nor certified novel by this audit. No new publication of these additional claims is authorized by this report. The sole suggested wording repair is to state the centered-jet dimension formula `2m+1` for `m>=1`, treating `m=0` separately.

The four-cell proposal in `PROPOSED_ROW.json` is held for root adoption and a fresh immediate pre-write duplicate check. No spreadsheet row was written. Fresh full43-column numeric-gid reads at 08:45:31 and 09:02:45 UTC returned the same 191 rows, with no matching problem, DOI, author, title or mathematical result. Broad `ADE` substring leads were unrelated words, not ADE entries.

## 1. Precise original question and invariant

The primary source is Hussein Mourtada, *Commutative Algebra and Integer Partitions*, in Oberwolfach Report6/2023, printed pages371–373; Question2 is on printed372/PDF46 of the official [report](https://ems.press/content/serial-article-files/47000). Its setup is an affine pointed singularity over a characteristic-zero field K, with O a closed point. It defines the actual scheme of centered arcs and its natural cone grading, with coefficient dimensions taken over K. The question asks whether that invariant characterizes ADE surface singularities. The setup supplies no normality, irreducibility or isolated-singularity hypothesis; the same contribution subsequently discusses a nonreduced scheme. The negative conclusion here is expressly about this unqualified, scheme-theoretic reading. It does not assert that the writer intended every restricted normal formulation to be false.

For a K-rational point O and a hypersurface f in three variables, use centered series `x(t)=sum_{i>=1}x_i t^i`, and similarly y,z, and write `f(x(t),y(t),z(t))=sum_j F_j t^j`. The coordinate ring is

`B=K[x_i,y_i,z_i : i>=1]/(F_j : j>=1)`, with `wt(x_i)=wt(y_i)=wt(z_i)=i`.

There is no reduction, radical, normalization or restriction to K-valued arcs in this definition. The target series is

`C(q)=(1-q)^(-3) product_{i>=2}(1-q^i)^(-2)`.

Its first eleven coefficients are `1,3,8,18,38,74,139,249,434,734,1215`. These coefficients are controls, not a substitute for equality in every weight.

The author PDF dated31January2013, *Jet schemes of rational double point singularities*, Section4.1, printed13, has Proposition4.4 (forward ADE formula) and Question4.5 (characterization). The alternate author PDF *JetSchemes-ValuationTheory.pdf* has the same characterization question as Question4.4, following Proposition4.3. Its next Question4.5 is a different jet-component question. Both contexts were read; the numbering difference is preserved. The 2023 report itself cites the eventual2014 chapter. This report does not invent a normality convention from adjacent terminology.

If O is not K-rational, the centered ring has degree-zero part kappa(O). Equality with C using the report's `dim_K` convention forces `[kappa(O):K]=1`, since the point is closed of finite type and C has constant coefficient1. BMS instead defines the focused algebra over the residue field; these dimension conventions must not be silently interchanged.

## 2. Crossing: complete all-weight proof and exact prior theorem

Let X be `Spec K[x,y,z]/(xy)`, centered at its origin. It has dimension2, is reduced and reducible, and has a one-dimensional singular locus. It is not a rational double point or geometric ADE singularity.

For m>=1 let `S_m=K[x_i,y_i,z_i:1<=i<=m]` and `F_j=sum_{a+b=j,a,b>=1}x_a y_b`. The centered m-jet fiber has equations F2 through Fm. Over an algebraic closure their common zero set is the union of the m linear spaces where `ord(x)+ord(y)>=m+1`: choose `r=1,...,m`, kill x1 through x_(r-1) and y1 through y_(m-r). Each has codimension m-1 in S_m. The orders argument includes zero series and every boundary case. The same argument for every prefix gives height j-1 for F2 through Fj, in S_m for j<=m. Since polynomial rings are Cohen–Macaulay, the ordered sequence F2,...,Fm is regular; equivalently use successive prefix heights and the complete-intersection criterion. This concerns the original ideal and therefore computes its scheme-theoretic Hilbert series, even though the quotient need not be reduced.

Consequently

`H_{S_m/(F2,...,Fm)}=product_{j=2}^m(1-q^j)/product_{i=1}^m(1-q^i)^3`.

Every fixed weight N stabilizes once m>=N: variables and equations of higher positive weight cannot contribute to the ideal's Nth homogeneous piece. Taking this coefficientwise limit gives exactly C. There is no unjustified exchange of an analytic limit or of infinite dimensions.

This is already BMS Proposition3.9. In arXiv1101.4950v2, Section3, the local normal-crossing formula uses dimension d, with e components through q. Set d=e=2: on `xyz=0`, use q=(0,0,1), so the third factor is a unit and the local product is the same crossing surface. The formula is C. Adjacent Corollary3.8 is the ADE formula. More directly, the actual published FPSAC2011 paper, printed215, Proposition3.9 gives the formula for `x1...xe=0` in affine n-space. Setting n=3,e=2 is exactly our X at0, without a local-unit bridge. Its preceding Proposition3.8 gives the identical ADE series.

The original invariant's scheme structure is essential. In B the class x1*y2 is nonzero in weight3, but has square zero: F2=x1*y1 and F3=x1*y2+x2*y1 give `(x1*y2)^2=-x1*y1*x2*y2=0`. The independent checker verifies both claims exactly. On the reduced centered arc ring all x_i*y_j vanish, since in any prime quotient the product of the two formal series over a domain is zero. Thus its Hilbert series is `2H(q)^2-H(q)`, where `H=product_{i>=1}(1-q^i)^(-1)`, giving coefficient17 in weight3 rather than18. Reducing the arc ring would invalidate the comparison; this audit does not do so.

## 3. Pinch point: separate stronger-category example

The PR's second example is `f=x^2-y^2 z`. For every N choose n sufficiently large that n-1>N. The rational-double-point polynomial `f-z^(n-1)` is of type D_n after the usual permutations and nonzero scalar changes over an algebraic closure. Centering makes the added term have minimum natural weight n-1, so every coefficient equation of weight<=N is identical. The coefficientwise finite-weight stabilization argument from Section2 then identifies the pinch and D_n Hilbert series through weight N. The standard ADE formula gives C, and arbitrary N proves equality in every weight. This uses no assertion of flatness of a degenerating family.

The pinch surface is geometrically integral and formally irreducible: division by the monic equation in x gives unique expressions `a(y,z)+x b(y,z)`. Under `y=u,z=v^2,x=uv`, the first summand has even v powers and the second odd v powers. Their monomial supports cannot cancel, proving injection both for polynomial and formal power series normal forms, over any extension field in characteristic0. Its Jacobian singular locus is the line x=y=0. In its fraction field, x/y is integral by `(x/y)^2=z`, but it is not regular at the origin: if a unit denominator made x divisible by y, reduction modulo y would make nonzero x vanish in the local ring of `K[x,z]/(x^2)`, which is impossible. Thus the example is nonnormal and nonisolated. It does not disprove the normal-surface converse. Its arc ring is nonreduced already because nonzero x1 has square zero.

This argument is accepted as mathematics independently of whether it appears elsewhere. The literature search did not authenticate an earlier identical pinch-point Arc Hilbert calculation; no firstness is inferred. Motivic Poincaré series of a Whitney umbrella are a possible search lead but are a different invariant; no such lead was used to establish this result or its priority.

## 4. Infinite regular sequences: noncancellation and convergence

Let S be a nonnegatively graded algebra with finite-dimensional pieces, and let homogeneous f_i have positive degrees d_i tending to infinity, with only finitely many d_i below each bound. Put `R_i=S/(f1,...,fi)`, `K_i=Ann_{R_(i-1)}(fi)` and `P_i=product_{j<=i}(1-q^d_j)`. The exact multiplication sequence gives

`H_Ri=(1-q^di)H_R(i-1)+q^di H_Ki`.

Dividing by P_i and telescoping gives

`H_Ri/P_i=H_S+sum_{j<=i}q^dj H_Kj/P_j`.

Every summand on the right has nonnegative coefficients, since each inverse Euler factor does. This positivity, rather than an unsafe alternating unnormalized product, is the key point. For fixed weight N, later equations cannot affect R_i in weight N, P_i stabilizes, and terms with d_j>N do not contribute. Therefore the coefficientwise identity holds at infinity. The expected complete-intersection product for `H_{S/(fi)}` holds if and only if all K_i vanish, that is, the sequence is regular. If an equation is zero, its annihilator contains1 and is detected. No cancellation, Noetherian hypothesis on the infinite polynomial ring, or interchange of divergent series is hidden in the argument.

The reviewer checker also tests the nonregular sequence a²,ab,b²: after normalization its defect coefficients are nonnegative and some are positive, while the naive unnormalized Euler product has negative coefficients. This is a deliberate control for the key inference, not a proof of the general identity.

## 5. Normal-surface converse: exact category and imports

Suppose X is a normal finite-type surface in characteristic0, and its centered invariant at O equals C in the preceding dimension convention. Degree1 is the embedding dimension, so it equals3. The local ring is excellent, and its completion is a normal dimension2 local domain. A minimal equicharacteristic Cohen presentation is `K[[x,y,z]]/(f)`: the kernel is a height-one prime in a regular local UFD, hence principal. Its equation has no linear term. Being lci descends from the completion and holds after shrinking an affine neighborhood. Normality in dimension2 implies regularity in codimension1, so the singular locus can be made exactly O; the component through O is integral.

The completion comparison is a scheme-level assertion, not just a statement about field-valued arcs. A centered map to A[[t]] for an arbitrary test K-algebra A sends the maximal ideal into (t), and extends uniquely to the completion by the inverse system modulo t^r. Formal changes of coordinates induce well-defined coefficientwise homogeneous maps. This proves graded ring compatibility even for nilpotent A and permits the minimal formal hypersurface presentation.

Write the centered equations of f as F2,F3,.... The normalized criterion from Section4 and equality C force this entire ordered list to be regular in the infinite polynomial ring. Faithful flatness of the polynomial extension from S_m descends regularity of each finite prefix to S_m. For m>=1 the centered fiber has dimension `3m-(m-1)=2m+1`; at m=0 it is a point. This is the only endpoint correction recommended to the PR prose. The dimension is strictly below `2(m+1)`.

Mustaţă, *Jet Schemes of Locally Complete Intersection Canonical Singularities*, final arXivmath/0008002v5 (9April2001), Proposition1.4 applies: for an integral lci variety of dimension2, the full m-jet scheme is irreducible precisely when its fiber over the singular locus has dimension below2(m+1). Its actual proof was read: the smooth-locus preimage is one irreducible component of dimension2(m+1), and the lci equation count forces every component to have at least that dimension; the smaller singular fiber cannot support another component. The isolated-singularity reduction above supplies all its hypotheses.

The actual surface Theorem4.4 and its proof in v5 were also read. Irreducibility of all jet schemes gives rational double points. The proof imports the canonical/rational lci criterion (Theorem3.3, equivalently the main theorem and the Gorenstein rational/canonical equivalence); these are standard cited background, not newly proved here. This audit does not claim to have reproduced the entire motivic-integration argument. The deep imported result has precisely the needed hypotheses, and the PR does not transfer a new research gap to an unsupported lemma. The original PR's v4 and its v5 citation supplement remain distinct captures; this report uses the explicitly inspected v5 statements.

Over arbitrary characteristic-zero K, normal finite-type schemes are geometrically normal. This also follows from Stacks Lemma33.27.4: the purely inseparable extension needed there is trivial over a perfect field. Completion normality for excellent normal local domains is explicitly used and justified in Stacks Lemma55.8.2's proof. Base-changing graded pieces to an algebraic closure preserves their dimensions and equality with C. Take the geometric component through the lifted rational point and apply the preceding argument. The conclusion is **geometric ADE after base change**, not a split equation or a determined Dynkin type over K. Conversely a geometric ADE point has C by the established forward theorem and faithful base change. Smooth points have embedding dimension2 and cannot satisfy C. For a nonrational closed point one must either retain the degree-zero restriction or restate the invariant over its residue field.

The real positive-definite quadratic `x²+y²+z²` is a useful control: it is geometric A1 and has C although its real-valued arcs can behave very differently. Point-set reasoning cannot replace the test-algebra scheme argument.

## 6. Deliberate falsification and independent exact artifacts

`verify_readonly.py` was written for this audit, using only standard-library integer sparse row elimination to compute ideal-piece ranks exactly over Q. Monomials are generated independently, variables are interleaved by natural weight, and ideal multiples are constructed directly from coefficient equations. It neither imports nor executes any PR or source-author code. Explicit guards, rather than Python assertions, remain active under normal, -O and -OO runs. Closed-manifest membership, source receipts, eight Git blob identities, the nested PR manifest, ledger captures and proposal scope are also checked.

Through weight10, crossing, pinch, D4 and the anisotropic A1 all match C. The doubled plane first differs at weight4 (39 instead of38). More significantly, the normal isolated non-ADE candidate `x²+y³+z^6` agrees through weight9 and differs at weight10 (1216 instead of1215). In its coefficient ring before F5, y1^5 is nonzero and annihilates F5; y1^4 does not annihilate it. Exact linear algebra verifies both the actual annihilator and the rejected weaker control. Its centered5-jet fiber also has the linear subspace x1=x2=y1=0 of dimension12, exceeding the regular-sequence expectation11. Thus the theorem is not being accepted from a finite list of matching low coefficients.

Other checks verify crossing and pinch nilpotents, the changed reduced-crossing invariant, sharp finite-weight perturbation visibility and distinct pinch normal-form monomial images. The written parity proof and positive coefficientwise identity, not the finite samples, provide the universal conclusions. Normal/O/OO outputs are retained as `CHECK_NORMAL.json`, `CHECK_O.json`, `CHECK_OO.json`; the final verifier replay authenticates the closed manifest as well.

## 7. Publication identity, chronology, supporting material and deduplication

Crossref and the resolved DOI landing identify **Clemens Bruschek, Hussein Mourtada, Jan Schepers**, *Arc spaces and the Rogers–Ramanujan identities*, **The Ramanujan Journal30(1),9–38**, online18July2012, printJanuary2013, DOI10.1007/s11139-012-9401-y. The arXiv record gives v1 25January2011 and v2 7February2011; v2 is the independently read body. Mourtada's current author publication31 explicitly lists the journal volume/pages and links arXiv1101.4950. The original2023 question's references also list both the2011 proceedings and2013 journal versions. These independent primary links authenticate the family relationship; no claim of byte-for-byte journal/preprint equivalence is needed or made.

The full proceedings PDF is an actual10-page published payload, *Arc Spaces and Rogers-Ramanujan Identities*, FPSAC2011, pages211–220, DOI10.46298/dmtcs.2904. Its original family authorship and exact theorem are verified. Crossref's generic1January2011 metadata is not treated as the precise conference disclosure date. The2011/2012–13 family necessarily predates the PR's server creation on11October2026 and both inspected characterization-question versions. This establishes prior coverage of the literal negative; it does not establish that somebody explicitly advertised an answer under the exact question number at the time.

The Springer PDF URL yielded HTML despite HTTP200, and the DOI redirected to the correct article landing with a cookie-error parameter. Raw bytes and this content-type mismatch are retained. Do not describe the actual journal PDF as downloaded or independently read. The actual published proceedings body plus preprint proof and this reviewer's all-weight derivation remove any need to promote a snippet. Journal-family attribution is authenticated by the author and original problem source.

The relevant scientific support is the accessible mathematical paper/proof, preprint and conference text. No theorem in this literal result depends on author software, a certificate or dataset; no missing Zenodo source ZIP is inferred for a classical journal publication. This audit does not require a new Zenodo record for a valid existing journal DOI.

The all43-column spreadsheet has headers Original Problem, Solution Chat URL, DOI, Notes. Both read captures have SHA256 `fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1` and191rows. Aliases checked include problem30005416, OWR-12697689-012, PR1257, both BMS DOIs, arXiv1101.4950, all three names, Arc Hilbert, crossing, pinch, jet schemes and the theorem context. No relevant row appears. Semantic inspection rejected12 `ADE` substring leads belonging to unrelated words such as graded, tradeoffs and Fradelizi. The proposal leaves chat URL blank; it does not invent a solution chat, transfer BMS authorship to this project or append two rows for one family.

## 8. Priority search and exact remaining limits

The retained search index covers28 mathematical/publication queries plus two standard-background queries, current author publications, the original2023 source, both2013 author question editions, BMS2011v2 and its actual proceedings publication, Mourtada's2020 HDR relevant section, the author's2025 article and proof of its forward ADE theorem, Handbook Section1.9, and relevant introduction/Section2 of arXiv2601.12048v1. Those later sources give the forward canonical/ADE Hilbert product or partition applications in the inspected passages; they do not supply an authenticated reverse Arc Hilbert characterization there. The audit makes no statement about every page of these broader works.

Public Zenodo searches used the original problem identifier, the prose-package title, ADE AND Hilbert (all10 returned records), and pinch AND Hilbert (all12 results across both pages). None identifies this target package. DataCite searches used the numeric problem, Arc Hilbert, ADE AND Hilbert-Poincaré, and arc with creator Ferudun (four unrelated digraph arc records). The current EulerSolve index has no target match; its guessed direct target URL returns404. Searches do not rule out private unfinished deposits, an unindexed paper, or differently worded prior formulations. They are not a global novelty certificate.

The normal converse is an elementary-but-nontrivial consequence of the all-weight regular-sequence criterion and classical jet theorems. Whether this exact characterization or the pinch calculation was previously written down remains unestablished. The full literal original question is nevertheless already answered negatively by BMS; no new publication is needed to cover it. Preserve the further correct mathematics as separately scoped material without claiming a novel resolution or rejecting it merely because historical intention is unspecified.

## 9. Evidence hygiene and proposed disposition

`SOURCE_INDEX.json` lists capture receipts and actual read scopes. `SEARCH_INDEX.json` distinguishes queried metadata, inspected primary bodies and unresolved absence claims. `ALIASES.json` supplies exact DOI/arXiv/problem/PR/result-family roles. `PRIORITY_DECISION.json` and `PROPOSED_ROW.json` enforce literal-only accounting and pending root adoption. Primary bodies, ledger contents, PR bodies, search responses, extracts and two page renders are private research captures, excluded from redistribution; only authored reasoning and hash metadata are public-scope artifacts. The closed inventory includes the nested PR manifest; only the exact top-level `MANIFEST.json` is excluded from its own hash list.

Recommended parent disposition: accept full literal negative as already published; adopt one narrowly qualified existing-publication row after the immediate concurrency recheck. Do not upload a duplicate paper, do not claim that BMS proves the normal converse, and do not close the draft as mathematically invalid. Preserve or separately process its further correct claims according to the parent's publication scope and a distinct originality gate. This audit performs none of those live actions.
