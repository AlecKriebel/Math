# NEW second independent adversarial whole-package review

Review date: 12 October 2026 PDT / 13 October 2026 UTC. PR #1024, catalogue problem 30001113 / OWR-2492-004. Independent AI review; no conventional human peer-review certificate. Reviewer reconstructed the theorem from the candidate TeX before consulting historical material for source/provenance comparisons. Earlier PASS verdicts and mathematical conclusions were not adopted as evidence of correctness.

**Verdict: PASS_ZERO_ACTIONABLE. Actionable issue count: 0, including P3.** The reviewed deterministic archive has SHA-256 9ce7e691379f1eee0b17171e10873d8c93c983ff2377be94f7a9a90bac6b304b and 127 entries. This verdict is tied to the exact input pins in INPUT_PINS.json. The candidate, submitted snapshot, metadata and unrelated workspace material were not edited. Every output of this review is within reviews/package_02. No outreach, service write, publication, merge or closure occurred.

## 1. Exact hypothesis and success criterion

The candidate claims a negative instance of the *unrestricted* restriction–induction question. Let k be F4, let G be its additive group, and let N be the subgroup F2. The residual local action is

\[
\rho(a)(t)=\frac{t}{1+at}.
\]

The category consists of local Artinian W(k)-algebras with their identified residue field k. Coordinate equivalence consists of all A-algebra coordinate changes reducing to the identity. Nilpotent constant terms are allowed. Q=G/N acts on the actual set-valued deformation functor D_N, and D_N^Q is its fixed subfunctor, not the fixed points of a selected hull.

The exact claim is: no functor h_R prorepresented by a complete Noetherian local W(k)-algebra R, and no natural transformations f:D_N^Q→h_R and g:D_Q→h_R, can make the actual restriction–induction map factor formally smoothly through D_N^Q×_{h_R}D_Q. No tangent dimension, linearity of f or g, component prorepresentability, or extension of f to D_N is required. Thus the one-dimensional prescribed recipient is excluded as a special case.

The success criterion for this audit was a reconstruction of every full-series and functor step, a fresh comparison with the primary scope and prior-credit passages, exact computational reproduction, negative contract testing, and package/PDF/metadata integrity. A mere finite rank calculation, numerical test, hull noninjectivity, assertion of historical acceptance, or lack of a search hit would not satisfy it.

## 2. Independent mathematical reconstruction

### 2.1 The action and both complete fixed rings and fields

Ordinary rational substitution gives rho(a)rho(b)=rho(a+b): the composite denominator is 1+(a+b)t. The t² coefficient is a, so the action is faithful. Every a≠0 has rho(a)(t)−t beginning with a t², hence conductor one. These assertions require no finite truncation or lifting theorem.

Set y=t²/(1+t). It is invariant under n=rho(1), and

\[
t^2+yt+y=0,\qquad n(t)=t+y.
\]

The elements y^m and ty^m have leading t-orders 2m and 2m+1, respectively, with leading coefficient one. Given any h in k[[t]], subtract its current leading term using the corresponding basis element. The orders strictly increase, the resulting coefficients define A,B in k[[y]], and the subtraction converges in the complete t-adic topology. Thus h=A(y)+tB(y). Uniqueness follows because nonzero A and tB have even and odd leading orders, which cannot cancel. Acting by n gives A+(t+y)B, so invariance is exactly yB=0. In this domain it implies B=0. Consequently k[[t]]^N=k[[y]].

For a Laurent series the same leading-order argument starts at its finite lowest order, including negative even and odd orders. It gives the basis 1,t over k((y)); invariance again forces B=0. Hence k((t))^N=k((y)). Intersecting with k[[t]] is consistent: the t-order of a Laurent series in y is twice its y-order.

Writing u²+u+1=0, the denominator of rho(u)(y) is

\[
(1+ut)(1+(u+1)t)=1+t+u(u+1)t^2=1+t+t^2.
\]

Therefore the nontrivial quotient element acts by sigma(y)=y/(1+y). In particular D_Q is the conductor-one involution functor for this actual quotient action. Applying the same complete basis argument with z=y²/(1+y) gives

\[
k[[y]]^Q=k[[z]],\qquad k((y))^Q=k((z)).
\]

Every nonzero invariant Laurent series has even y-valuation. This last fact is crucial; finite quotients do not retain it faithfully.

### 2.2 Algebraic derivations and the exact invariant lattice

There is no omitted discontinuous algebraic derivation here. For every h in k[[t]], perfectness of k provides unique series a,b with

\[
h=a(t)^2+t b(t)^2.
\]

Split h's coefficients into even and odd degrees and take their square roots in k. For any algebraic k-derivation d, Leibniz's rule in characteristic two gives d(a²)=d(b²)=0, without any use of infinite-term differentiation. Hence

\[
d(h)=d(t)b(t)^2=d(t)h'(t).
\]

Thus all algebraic derivations are exactly k[[t]]∂_t, and are continuous. The same coefficient calculation applies to Laurent series. A coordinate automorphism reducing to the identity over k[epsilon]/epsilon² is likewise id+epsilon d, so the tangent description includes every allowed algebraic coordinate change. Moreover A[[t]]'s maximal-ideal topology is equivalent to its t-adic topology when A is Artinian: nilpotence of m_A gives (m_A,t)^{n+s}⊆(t)^n for a fixed s. Algebra automorphisms preserve the unique maximal ideal and are continuous in this topology. A hidden noncontinuous conjugator cannot evade the argument.

Any N-invariant derivation restricts to a derivation b(y)∂_y of k[[y]]. The polynomial t²+yt+y has derivative y with respect to t, nonzero in k((y)), so k((t))/k((y)) is separable. A derivation of the latter extends uniquely to the former. Differentiating the polynomial directly yields

\[
y\,d(t)+(t+1)b(y)=0,
\quad
d(t)=b(y)\frac{1+t}{y}=b(y)\frac{(1+t)^2}{t^2}.
\]

This independently agrees with b/(dy/dt), since dy/dt=t²/(1+t)². Uniqueness makes the extension N-invariant. If b≠0 has y-valuation m, its extended t-coefficient has exact t-valuation 2m−2; the factor (1+t)² is a unit, so no cancellation changes this threshold. It preserves k[[t]] precisely when m≥1. The zero coefficient is harmless. The exact module is therefore

\[
\Theta^N \cong M=y k[[y]]\partial_y.
\]

In particular b=1 produces a pole of order two and is excluded, whereas b=y produces coefficient 1+t and is allowed. Replacing M by all of Theta-sharp would change the kernel computation and is invalid.

### 2.3 The quotient action and full cohomology calculation

Conjugating coefficient derivations by sigma gives

\[
T(f)(y)=(1+y)^2 f\left(\frac{y}{1+y}\right).
\]

Indeed sigma'=1/(1+y)². The inverse-conjugation convention gives the same expression because sigma is an involution. Restriction of invariant derivations is equivariant: their field extension is unique, so transporting by the quotient action commutes with extension and restriction. There is no further ramification factor. T preserves M and T²=1.

For f in yk[[y]], the relation Tf=f is equivalent to invariance of F=f/y², because sigma(y)²=y²/(1+y)². We have ord_y F≥−1. By the complete fixed-field result F lies in k((z)) and, if nonzero, has even valuation. Its valuation is therefore at least zero, so F lies in k[[z]]. Conversely every such F gives an invariant f. It follows exactly, on complete series, that

\[
M^Q=y^2 k[[z]]\partial_y.
\]

Since z is fixed,

\[
(T-1)(y h(z))=y^2h(z)
\]

for every full series h in k[[z]]. This proves that every invariant is a coboundary, with an explicit integral preimage. The opposite inclusion holds because (T−1)²=0 in characteristic two. The cyclic cocycle formula then gives

\[
H^1(Q,M)=\ker(1+T)/(T-1)M=0.
\]

This is an equality of full formal-series modules, not a conclusion drawn from monomials or from ranks at increasing finite cutoffs.

### 2.4 Actual tangent classes and restriction injectivity

For A=k[epsilon]/epsilon², any lift can be written (id+epsilon c(g))rho(g). Composition gives a group one-cocycle, and an arbitrary identity-reducing coordinate conjugation changes it by a coboundary. The derivation result above identifies the complete permitted tangent module, including constant terms. Therefore TD_H=H¹(H,Theta) for the actual equivalence classes, and restriction agrees with cocycle restriction.

Here is a direct proof of the kernel statement, without accepting inflation–restriction as an unexplained black box. Start with a G-cocycle whose N-restriction is zero in H¹(N,Theta). Subtract a Theta-coboundary to make it vanish on N as a cocycle. For n∈N, commutativity gives

\[
c(n+u)=n\cdot c(u)=c(u+n)=c(u),
\]

so c(u) lies in Theta^N. The order-two relation gives (1+T)c(u)=0. The explicit calculation above writes c(u)=(T−1)m with m∈Theta^N. Subtract the corresponding coboundary. It does not alter the zero values on N and kills c(u), hence kills the cocycle on both generators and on all of G. Thus

\[
\ker(TD_G\longrightarrow TD_N)=0.
\]

The actual fixed subfunctor injects into D_N(A) at each A, so the same zero-kernel assertion holds for restriction into TD_N^Q. There is no hull replacement at this step.

For comparison with the originally prescribed recipient, Theta-sharp=k[[y]]∂_y and Theta-sharp/M is the constant coefficient k. T preserves that coefficient and acts trivially on this quotient. Since Q is cyclic of order two and char(k)=2, H¹(Q,k)=k. The prescribed space is indeed one-dimensional, but this value is not used to restrict possible recipients.

### 2.5 A nonzero actual quotient tangent fixed under a cubic-ring symmetry

Let B=k[epsilon]/epsilon³ and A=k[epsilon]/epsilon², with their W(k)-structures obtained through W(k)→k. Define j(epsilon)=epsilon+epsilon², fixing k. This is a genuine local W(k)-algebra automorphism of B and j²=id.

The matrix

\[
M_\epsilon=\begin{pmatrix}1&\epsilon\\1&1\end{pmatrix}
\]

gives sigma_epsilon(y)=(y+epsilon)/(1+y). Its constant term is nilpotent, its linear coefficient 1+epsilon is a unit, its determinant is 1+epsilon, and M_epsilon²=(1+epsilon)I. Thus it is an allowed continuous involution and defines an actual class x∈D_Q(B).

For the identity-reducing affine coordinate change chi(y)=(1+epsilon)y+epsilon, let

\[
C=\begin{pmatrix}1+\epsilon&\epsilon\\0&1\end{pmatrix}.
\]

Direct multiplication in B gives both sides of

\[
M_{\epsilon+\epsilon^2}C=(1+\epsilon)CM_\epsilon
\]

equal to

\[
\begin{pmatrix}1+\epsilon&\epsilon^2\\1+\epsilon&1+\epsilon\end{pmatrix}.
\]

The scalar is a unit. In ordinary function composition this is an affine conjugacy; ring-substitution composition reverses the order and exchanges the conjugator with its inverse. Both are allowed identity-reducing changes, so the conclusion concerns the actual class: j_*x=x. Noninjectivity of a chosen hull parameter alone would not imply this; the displayed actual conjugacy does.

The reduction v∈D_Q(A) is nonzero against *all* permitted conjugators. Every such conjugator is y+epsilon h(y), h∈k[[y]], with no restriction on h(0). At first order, conjugating sigma changes it by h(sigma(y))−sigma'(y)h(y), up to conjugating direction and sign. At y=0 this is h(0)−h(0)=0. The perturbation of sigma_epsilon is epsilon/(1+y), whose constant coefficient is one. It cannot equal any such coboundary. Characteristic two removes any sign issue. This checks nilpotent translations rather than quietly disallowing them.

### 2.6 Every natural transformation to every prorepresentable recipient kills v

Let eta:D_Q→h_R be any natural transformation, and write eta_B(x)=psi:R→B. Naturality at the endomorphism j, combined with actual j-fixity of x, gives j∘psi=psi. On an arbitrary element c0+c1 epsilon+c2 epsilon² of B, j adds c1 epsilon², so

\[
B^j=k+k\epsilon^2.
\]

The reduction B→A sends this fixed subring into the constants k. Consequently the reduction of psi lands in k⊂A. Since psi is local and respects the identified residue field, this reduction is precisely R→k→A, the residue basepoint of h_R(A). Naturality at B→A therefore gives eta_A(v)=0.

This argument tests a set-valued natural transformation at two specific objects and one endomorphism. It assumes neither a linear tangent map nor any tangent dimension. If R has mixed characteristic, the map to B simply kills 2; the residue composite remains the same. No coefficient-field embedding k→R is assumed. The argument only uses k→A and k→B, which are present in these equicharacteristic target rings. It applies even to a more general local represented Hom-functor; Noetherianness and completeness do not hide an exception.

### 2.7 The actual invariant-subfunctor basepoint and the smoothness quantifier

D_N^Q(k) contains the unique residual N-action. In this example the exact lift of rho(u) over any equicharacteristic target commutes with the exact lift of rho(1), so its pullback 0_N lies in the genuine fixed subfunctor. Equivalently, naturality of the fixed subfunctor pulls back its k-point. It is not a basepoint chosen inside a hull.

Suppose f and g as in the target claim exist. Naturality for k→A gives f_A(0_N) equal to the unique residue basepoint of h_R(A). The result above gives g_A(v) equal to the same point. Thus (0_N,v) is an actual point of the fibre product at A, with reduction its unique residual point.

The map A→k is small: the kernel (epsilon) is annihilated by the maximal ideal (epsilon). Formal smoothness would require surjectivity of

\[
D_G(A)\to D_G(k)\times_{(D_N^Q\times_{h_R}D_Q)(k)}
                         (D_N^Q\times_{h_R}D_Q)(A).
\]

Apply it to the unique element of D_G(k) and the pair (0_N,v). It produces w with res(w)=0_N and ind(w)=v. Restriction injectivity forces w=0_G. Induction is natural, so the pullback of the residual G-class induces the pullback of the residual quotient class: ind(0_G)=0_Q. This contradicts v≠0.

Only one small extension is needed to falsify smoothness, whose quantifier ranges over all surjections. The cubic ring constrains natural detection; it is not the extension at which smoothness is assumed to fail. No extension of f to D_N, exact induction tangent formula, Klein-four hull universality, or component prorepresentability is used. All central assertions are supported by explicit derivations, and no route transfers the central difficulty to an unsupported equivalent claim.

## 3. Fresh primary-source comparison and attribution

Fresh official-host bodies were retrieved into the gitignored sources/raw directory and are not to be redistributed. The URL/byte hashes appear in sources/RETRIEVAL.json. The initially found research-portal thesis PDF returned HTTP403; the official Utrecht bitstream successfully returned the thesis, with hash 1b8a9f23b13631a777b0c203062e93299cdcfe9a3facbfcd99d6883ed7ba26fb. This is a retrieval-channel limitation, not a broken mathematical reference. Both Numdam and the AIF publisher versions of the published BC paper were retrieved; their distinct container hashes agree with the package's separately recorded versions.

The [OWR primary report](https://ems.press/content/serial-article-files/46200), printed pp.3038–3040, first poses the general question and then its prescribed-tangent formulation on p.3039. The component prorepresentability hypotheses are imposed in the subsequent Theorem 3 on p.3040. They are not part of the question. The report also defines equivalence through identity-reducing coordinate conjugacy. I inspected the entire Byszewski contribution and cover, rather than inferring the question from a secondary summary.

The [Utrecht thesis bitstream](https://dspace.library.uu.nl/bitstream/handle/1874/33749/byszewski.pdf?sequence=1&isAllowed=y), Question 6.4.4, poses the same unrestricted prescribed-tangent question. Remark 6.4.5 and Theorem 6.4.7 separately add component prorepresentability. The candidate cites the correct question and does not promote that conditional theorem to an unrestricted existence theorem. The title, author and 2009 date were checked against the primary thesis.

The [arXiv v1 primary body](https://arxiv.org/pdf/1112.0352v1), Definitions 1.1–1.2, Lemma 1.3, Proposition 2.4 and Question 4.4, supports the category, first-order cocycle calculation, restriction map and scope used above. Remark 4.5 and Theorem 4.9 add the conditional component hypotheses. The smoothness definition requires all surjections, including A→k. Section 2 uses actual fixed classes, and Section 3 constructs natural induction. The [version record](https://arxiv.org/abs/1112.0352v1) dates the preprint to 2011; the candidate does not invent a later journal edition.

In the [published BC primary paper](https://www.numdam.org/article/AIF_2009__59_3_877_0.pdf), Section 2.1/Remark 2.2 permits nilpotent constants. Proposition 4.1's proof on p.896 gives the epsilon→epsilon+epsilon² involution conjugacy. Proposition 6.1 on p.899 exhibits distinct tangent/basepoint classes that become equal under k[e]/e²→k[w]/w³, e↦w². Since Hom(R,−) preserves target injections, naturality immediately implies the recipient collapse used here. The additive Klein-four action is also prior material. The candidate gives exact credit for these ingredients and claims the assembled restriction–induction obstruction as its contribution, not a new involution pathology.

As an extra independent check, the injection-collapse conjugacy can be exhibited directly: for delta²=c w², the matrix C_delta=((1+delta,delta),(0,1)) satisfies M_{c w²}C_delta=(1+delta)C_delta M_0. For each c∈F4 one can choose delta=sqrt(c)w. This verifies the antecedent without trusting a hull determinant criterion.

The package's priority ledger contains exactly 65 listed queries and 11 source/version records; their counts match its prose. This review added 12 bounded search queries, recorded in sources/PRIORITY_CHECK.json, and independently inspected the four central primary works. Search results returned the original question, established nonprorepresentability and unrelated deformation settings; no matching negative factorization assertion was identified in the inspected primary bodies. This is not an exhaustive originality certificate. The candidate explicitly avoids claims of first discovery, verified worldwide openness through 2026, human review or a formal proof-assistant certificate. No independent-research outreach was prepared or initiated.

## 4. Executable mathematical evidence and adversarial controls

The portable runner was read before execution. It uses Python's standard library and isolated child invocations with -I -S -B, at optimization levels 0,1,2. The 39 runs are exactly nine baselines, twelve actual-source mutation controls, and eighteen runtime fault controls. These mechanisms are honestly distinguished in the package.

The first source adapter actually changes a unique source assignment for the missing parameter shift and an explicit matrix-square predicate for the wrong scalar. The independent adapter changes a unique assignment for the shift and a return statement for the fixed-ring map. These are four actual defective-source families, each tested at three optimization levels. The rational/Artinian checker instead selects six faulty arithmetic branches at runtime: quotient action, derivation weight, parameter shift, translation, scalar and fixed ring. It is not incorrectly presented as eighteen distinct mutated source files.

The 39 fresh runs passed against complete stdout bytes, complete stderr bytes, exact exits and recursively typed JSON, with the source pins recorded. I then reconstructed all references independently from the original finite contract, independent baseline and independent control reasons. A typed-tree comparison distinguished booleans, integers, floats, null, arrays and objects; all 39 outputs agreed. Five deliberately tricky examples also tested the runner's type-equality predicate, including True versus 1 and nested occurrences. No trimming, field omission, traceback normalization or approximate number comparison was used. See receipts/PORTABLE_39.json and receipts/REFERENCE_INDEPENDENT_COMPARISON.json.

The archive was extracted into a fresh review-local directory and its runner executed without reaching outside the extracted package. It passed the same 39 cases. The extraction was removed after saving EXTRACTED_PORTABLE_39.json and EXTRACTED_RUN.json. This supports the advertised portable entry point; the historical UID1000 permission harness was neither replayed nor claimed as replayed.

The guard adaptation was audited more strongly than comparing selected predicate strings. All eleven Assert predicates and their labels agree exactly with the original AST. The inserted helper is exactly the expected RuntimeError guard. Removing that helper and reversing every require expression back to Assert reconstructs the *entire original module AST*, including imports, arithmetic, assignments and output logic. Original/adapted source hashes also match the record. Unchanged submitted sources, adapter and finite contract were byte-compared.

New extra controls individually forced each of the eleven guarded predicates to False in a review-local source copy, then executed every copy in normal/-O/-OO. All 33 runs failed at the intended guard, with empty stdout, exit one and the exact intended RuntimeError message. Thus all guards remain operative under optimization, not merely the two guards covered by the packaged mutants.

Nine malformed-package families were tested under all three outer optimization modes, giving 27 additional rejections: missing mathematical source, invalid reference JSON, boolean-to-integer reference substitution, extra stdout, unexpected stderr, unrelated RuntimeError, wrong intended control reason, invalid syntax and an unknown contract program. Every case failed for the intended contract reason and none earned the runner's PASS. Full outputs are preserved in receipts/EXTRA_CONTROLS.json. Syntax errors or unrelated failures are therefore not mistaken for accepted negative controls. This selected fault audit does not certify arbitrary malicious source intent or a security sandbox.

New independent arithmetic checks used a different field multiplication formula. They checked injection-collapse conjugacy for all four scalar tangents, all sixteen nilpotent cubic parameters for the projective parameter-shift identity, and the constant-coefficient obstruction for all 4096 polynomial conjugators of degree at most five. The all-series result is supplied by Section 2, not extrapolated from those polynomials.

The same new program computed (T−1)'s exact rank in M/(y^n) for every n from 2 to 65. It deliberately found a one-dimensional spurious H¹ at each of the 32 even cutoffs, represented by the top odd-order monomial. These classes disappear on extending the jet; they cannot be lifted to the full fixed Laurent field. At odd cutoffs the finite H¹ is zero. This is a meaningful adversarial boundary check: finite evidence alone would give misleading apparent counterexamples. The manuscript's complete fixed-field valuation argument and explicit series preimage correctly resolve this boundary. See receipts/INDEPENDENT_MATH_CHECKS.json and independent_math_checks.py.

## 5. Archive, inventory and stage provenance

The inventory lists 126 unique sorted content files. Every byte length and SHA-256 matches the actual candidate. The archive adds the manifest itself, for 127 sorted regular-file members under a single relative prefix; there are no duplicate names, absolute archive names, source/raw bodies or render PNGs. Every archive payload equals the corresponding candidate file, and every CRC passes.

The deterministic recipe in the local builder was independently replicated using the same selected top-level files and checks/expected/evidence contents, sorted names, fixed timestamp (2026,10,12,0,0,0), Unix regular-file permission 0644, empty extras/comments and deflate. The resulting *entire ZIP bytes* equal the candidate archive and have the same supplied SHA-256. The manifest's serialization is also exact. The rebuilt archive is retained as a review receipt. Determinism is verified for this recorded Python/zlib environment; no cross-zlib byte guarantee is invented.

The 27-file original snapshot was checked directly against Git objects at head 37b4b2fa44368f49e534e4982bd11f5667e0bf36, not just against another manifest. Each file's Git bytes match its pinned size/hash, the audit submitted snapshot and the archive's evidence/submitted copy. All 25 entries of the historical publication manifest retain their original byte seals. Their original paths remain relative to evidence/submitted, including current/ and historical/.

The first whole-package review is used here solely as provenance evidence. Its 18 copied authored files were compared directly with the original files and with the copy receipt's lengths and hashes; all bytes are unchanged. Its third-party source bodies and own-PDF renders are excluded. The prior review's input archive hash and counts describe that older stage, while CURRENT_REVIEW_STATE explicitly marks the second review pending and publication unapproved. This avoids presenting an earlier stage receipt as the current candidate inventory or silently replacing an old verdict.

README, SUPPLEMENT and evidence/INDEX relative navigation links all resolve to packaged files. Historical absolute local paths are expressly labeled as provenance, and the index provides the portable copies plus public primary source URLs and retrieved-byte hashes. Source records with Numdam/publisher PDFs retain their distinct hashes rather than falsely conflating the containers. The original permission/sealed harness is clearly historical and not the reproduction entry point. All of these checks are reproducible by audit_integrity.py and its INTEGRITY.json receipt.

The publication directory also contains local build/render intermediates and the deposit request alongside the selected archive contents; these are excluded by the documented builder selection. No selected-file omission, misleading archive inclusion, or third-party redistribution was found.

## 6. Exact metadata and five-page PDF review

The deposit metadata is structurally identical to metadata.json. Its title is “A characteristic-two counterexample to dévissage for local deformation functors”; creator Kriebel, Alec; affiliation Independent researcher; ORCID 0009-0001-9320-500X; date 2026-10-12; version 1.0; language eng; publication type preprint; open access; licence cc-by-4.0. README and manifest express the same licence. These agree with the paper's title, author, ORCID footnote and date. The description preserves unrestricted scope, arbitrary recipient tangent dimension, actual unframed classes, the untouched component-prorepresentable variant, exact prior credit, bounded priority limits and extensive AI/unrefereed disclosure.

The candidate TeX was copied byte-for-byte inside this review and compiled successfully using the built-in desktop LaTeX compiler. The source hash is pinned in COMPILE.json. The candidate PDF itself has hash 206114a917235504567f9f8487023c284aebacef00440e3c5bebfed98639d8cb, is a five-page unencrypted letter-size PDF, and was independently rendered at 110dpi. Text extraction was used for comparison, while the actual PNGs were visually inspected page by page.

| Page | Independently inspected contents | Visual result |
|---|---|---|
| 1 | Title, author/date, ORCID, abstract, category, original question and theorem | Legible; equations, accents, footnote and page number fit |
| 2 | Theorem continuation, full fixed rings, quotient action, cubic matrices and recipient naturality | Legible; matrices and displayed identities unclipped |
| 3 | Nonzero tangent, exact prior-credit paragraph, derivations, lattice and H¹ computation | Legible; fraction/partial/cohomology notation correct |
| 4 | Cocycle completion, prescribed space, smoothness contradiction, scope and AI/unrefereed disclosure | Legible; proof endings and paragraphs fit |
| 5 | Four primary references with links and exact proposition/question identifiers | Legible; accent glyphs and bibliography lines fit |

There are no clipped lines, overlap, missing glyphs, corrupted equation symbols or unreadable footnotes. The theorem and cocycle proof continue across page boundaries in normal prose; the fifth page's open space is not an error. The rendered statements agree with the reviewed TeX, including the crucial source attribution and final limitations.

## 7. Final assessment and limits

The strongest verified result is the exact unrestricted no-recipient theorem for this specified faithful F4 action and F2 subgroup. All full-series, actual-class, naturality, basepoint and small-extension steps were independently reconstructed. The independently checked finite arithmetic corroborates explicit identities and catches selected source/runtime/package defects; it is not used as a proof of arbitrary series or all natural transformations.

No actionable repair was found, including minor P3 issues. The modified question imposing prorepresentability of D_N and D_Q remains unaddressed, as the candidate states. Priority remains bounded rather than certified exhaustive; independent conventional human peer review and proof-assistant verification remain absent and are accurately disclosed. Those are stated scope limits, not concealed missing hypotheses in the proved counterexample.

This review certifies the inspected input package only as an AI adversarial audit with zero actionable concerns. It does not authorize immutable publication, claim a human certificate, guarantee source intent, or mutate any publication gate. The parent can incorporate the unchanged review and make its separately authorized gate decision using these exact input/output pins.
