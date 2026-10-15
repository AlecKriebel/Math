# Independent complete-package adversarial review 3 — frozen candidate v2

Review date: October 6, 2026 PDT / October 7, 2026 UTC. Reviewer: a fresh automated research agent, with a separately spawned, fresh mechanical-payload agent. This is an independent mathematical and package audit, not conventional human refereeing or formal proof certification.

## Verdict and required repair

**Candidate v2 is not yet publication-ready. One required scope-framing repair remains.** I found no mathematical counterexample, unsupported central step, false boundary reduction, incorrect equality witness, attribution overclaim, or reproducibility failure in the scope actually needed for this note.

The frozen title is “The Sperner property of Artinian complete intersections in characteristic zero.” It omits **standard graded**, whereas the original PROJECT_BRIEF.txt explicitly requires: “Make the resolved scope unmistakable in the title, abstract, introduction and conclusions.” The original problem also expressly excludes an inferred nongraded complete-intersection result. The abstract, theorem, body, description, and README prose do specify standard grading, but the title on the paper, PDF metadata, publication README, and deposit metadata does not. This is a concrete failure of the original title-scope condition, even if a reader familiar with the surrounding literature might infer the intended convention.

Required action: propagate “standard graded” into the title everywhere, rebuild the actual PDF and archives, freeze the new hashes, and obtain a fresh complete review of that revised package. A suitable exact title is “The Sperner property of standard graded Artinian complete intersections in characteristic zero.” I have not changed any candidate file. This report closes the audit of v2 only and does not approve a prospective v3.

Audit completion estimate at this checkpoint: 100% of this assigned v2 review. The mathematical audit found no remaining mathematical repair in the exact target; the publication package has the mandatory title repair and renewed-review step pending. These estimates are descriptions of review progress, not proof evidence.

## Independence, order, and limits

I read /Users/alec/Documents/Math/AGENTS.md and the original project brief. I did not read the project root README.md, THEOREM_STATUS.md, RESEARCH_LOG.md, prior complete-package reviews or verdicts, response records, or other reviewers' conclusions. I did not inspect the agent inventory. The separately delegated mechanical agent received the same restrictions with no inherited history; its task was payload integrity, reproduction, metadata, and safety, rather than mathematical endorsement.

Before reading the dependency ledger, approach table, or favorable scoped notes, I independently read the required primary upstream build TeX Sections 01–08, including the integrated proof of actual division, and reconstructed its mechanism. I also read the full-length field descent in Section 09 and the primary HWW full text, including Theorem 11's entire proof. Only afterward did I inspect the archived scoped notes and compare their claims to the independently reconstructed arguments. Those notes were evidence to attack; neither their confidence percentages nor favorable conclusions served as acceptance criteria.

The source clone remained read-only. I performed no commit, publication, tracker operation, branch/index mutation, or external communication with an individual. I made only my own review artifacts and scratch files in the dedicated project folder. Both actual archives were extracted into my own ignored scratch directory; all five actual deposited PDF pages were rendered and visually inspected. Only my own scratch was removed at audit closure.

This audit does not certify the stronger, unnecessary Lex-Plus-Powers Betti proof, every theorem in the upstream collection, a Lean formalization, or exhaustive priority. No applicable family-200 formalization was found in the inspected pinned catalogue; no Lean build or follow-on formalization is claimed. Standard background results such as complete-intersection duality, Morita theory, splitting of bundles on the projective line, Grothendieck–Riemann–Roch, and topological K-theory are used with their stated hypotheses; this report is not a reconstruction of all of those theories.

## Exact claim and boundary checks

The reviewed claim is the original one. For any characteristic-zero field k and any standard graded Artinian algebra

\[
A=k[x_1,\ldots,x_n]/(f_1,\ldots,f_n)
\]

with a homogeneous regular sequence of positive degrees d_i,

\[
\max_{I\triangleleft A}\dim_k(I/\mathfrak m I)
=\max_j\dim_k A_j
=\max_j[t^j]\prod_i(1+t+\cdots+t^{d_i-1}).
\]

The maximum ranges over all ideals, including zero, the unit ideal, and nonhomogeneous ideals. For p the last maximal Hilbert degree, the witness is \(\mathfrak m^p\). These are the actual quantifiers in the manuscript and metadata; the manuscript does not silently replace them by homogeneous ideals or an algebraically closed field.

I checked the following reductions directly:

* A standard graded Artinian algebra with A_0=k is local with unique maximal ideal A_{>0}; Nakayama therefore gives the stated minimal-generator formula for every ideal.
* The empty sequence n=0 gives A=k, product 1, and maximum 1, attained by the unit ideal. All-linear sequences give the same algebra and witness. Zero ideal has generator count zero and causes no exceptional maximum.
* Linear members are independent: dependence would yield fewer than n generators for an ideal of height n. A graded linear coordinate change eliminates them. The surviving forms cannot vanish or lose their stated positive degree as parameters: otherwise the Artinian quotient would violate the height bound. Their quotient is a homogeneous system of parameters in a polynomial ring, hence a regular sequence by Cohen–Macaulayness.
* The resulting graded isomorphism preserves all ideals, generator counts, and Hilbert dimensions. Each removed degree-one factor in the product is 1.
* Sorting the degrees is legitimate because every permutation of a homogeneous system of parameters in a Cohen–Macaulay polynomial ring is regular. Relabeling the pure-power variables restores the original convention.
* The only EGH input needed is fixed full-length Hilbert-function EGH: every homogeneous ideal containing the particular regular sequence has a counterpart containing the matching pure powers and with the same quotient Hilbert function in every degree. The counterpart need not preserve generator counts or generator degrees. Neither shorter-length EGH nor Betti domination is used.
* For arbitrary k, finite coefficients define a finitely generated subfield k_0 over Q. Include the regular-sequence generators in the defining ideal over k_0. Faithful flatness descends regularity, an embedding k_0 into C permits the complex theorem, and the obtained monomial exponents define the same counterpart over k_0 and k. Graded dimensions are unchanged under field extension. This does not require embedding an arbitrary characteristic-zero field into C, and does not require descent of every ideal over the larger field.

The regular-sequence Hilbert series, top degree \(c=\sum_i(d_i-1)\), one-dimensional top socle, and perfect multiplication pairings are used correctly. No assertion of weak or strong Lefschetz, a nongraded complete-intersection extension, or an unrestricted positive-characteristic analogue follows or is claimed.

## Independent reconstruction of the central upstream input

The pivotal source is OpenAI's “Commuting Division-Coefficient Forms and the Artinian Eisenbud–Green–Harris Conjecture,” pinned at adc7f1241b42e322a6451854ab7e4b4c146bf78a. The construction is not accepted merely because its theorem is printed. I read the entire build Sections 01–08, including the assembly and monomial extraction, and followed the following chain.

### Ordered basis and extraction

Section 02 requires a genuine finite-dimensional division algebra and commuting coefficient-linear forms with triangular annihilating rows. A quotient basis alone would be inadequate. I checked the stronger ordered-basis step: the constructed commutative graded algebra is finite over the central polynomial algebra in the original x variables; the triangular rows make the t variables parameters; the Cohen–Macaulay depth calculation makes them regular; the quotient Hilbert-series count is the dimension of the coefficient division algebra. The spanning t-monomials and dimension count consequently give the full ordered basis of the ambient module.

For an overideal I, extending to the central coefficient ideal produces a two-sided ideal. Lexicographically least exponents, ordered from the last coordinate backward, and right multiplication by the commuting t variables produce an upward-closed exponent set. Division-coefficient row elimination computes its graded dimensions. Each triangular annihilating row has least exponent \(d_i e_i\), so all the required pure powers belong to the extracted monomial ideal. This yields one monomial ideal with equality in every graded degree, rather than unrelated per-degree bounds. Left/right coefficient conventions and noncommuting individual matrix coefficients are not interchanged.

### Low relations, parameters, and connectivity

Section 03 starts from a generic anti-commuting skew-Laurent construction. The domain and center/parity arguments establish actual division at that initial stage. The prescribed low-degree relations are square relations; the central quadratic forms used in the later parameter construction remain independently generic in the required sense.

I checked the no-small-curves argument rather than assuming “generic” suffices. A bounded-degree curve has a field of definition with a uniform bounded transcendence degree. Only that many independent coefficient blocks can be rejected. On the projected curve, retained generic quadrics have nonempty, reduced, pairwise disjoint zero divisors; their squareclasses are independent. The resulting extension degree is at least \(2^{m-d_*}\), exceeding the proposed small-degree bound. Finite graded relation extensions preserve the obstruction because pullback of the hyperplane bundle and the degree of the finite map give the correct curve-degree comparison.

The simple-factor argument for a nonzero constraint polynomial uses its linear/quadratic annihilating differential relations. A repeated nonlinear factor would give a gradient curve in the characteristic set of explicitly bounded degree; a nonconstant gradient in the all-linear repeated-factor case gives the remaining small-curve contradiction, and a constant gradient is the pure-power case ruled out by basepoint freeness. Thus the factor needed for the level-set connectivity is simple.

The parameter section does not hide smooth properness. A simple factor gives the connected nonzero level via cyclic meridian monodromy. The separated block sum has the join connectivity stated in the source, yielding reduced homology vanishing through the required degree. The Jacobian incidence count supplies the expected codimension, reduced complete intersection, and singular-codimension bound. For the incidence map to the punctured line bundle, the top compactly supported fiber cohomology is the constant orientation sheaf, while lower rows have a long vanishing interval. The real base dimension makes the compact-support Leray calculation work in that interval even though the map is nonproper.

I independently checked the cited primary sheaf-theoretic scope: Schnürer–Soergel permit separated locally proper maps and their derived compact-support base-change and composition statements; Schapira gives the real-manifold compact-support cohomological dimension bound. I did not replace these by a claim that the map is a proper fibration.

Removing the singular stratum is justified by the given codimension/range inequality, and H_0=Z establishes connectedness of the smooth component. The cited quasiprojective Lefschetz result applies to the smooth open complement and general hyperplane sections; reduction to a smooth complete-intersection surface then gives trivial fundamental group. The circle-bundle sequence makes the cone's fundamental group abelian, its H_1 vanishes, and Hurewicz gives the needed connectivity. The s=0 case is separately the sphere case. The inequality between the desired connectivity \(\kappa=M+2h\) and the singular-removal bound \(2c-2\) is satisfied by the stated parameter choices.

### Curve, Picard, and character data

Section 05 constructs its group and curve data for every b, not just prime b. The Kummer functions have independent valuations, so the degree and group size are \(e=b^b\). The group is the diagonal-root quotient with cyclic permutation. The ramification indices at 0, 1, and infinity are b. The auxiliary cyclic cover ramified also at 2 is linearly disjoint; after normalization its ramification cancels the former indices. The result is a connected étale G-cover of the specified base curve. I checked the genus and degree formulas, including b=2, and the genuine linearization of the needed line bundle.

For a generic degree-zero twist A, \(A L^{g_T-1}\) has degree g-1 and is outside the theta divisor, so its cohomology vanishes. The finite pushforward V on the projective line has \(H^*(V(-1))=0\), forcing its canonical evaluation map to identify it with a trivial bundle. Multiplication therefore gives commuting linear matrix forms. This asserts commutation of the forms, not pairwise commutation of every matrix coefficient.

The use of Pic^1 is essential. If a nontrivial cyclic subgroup fixed a degree-one line bundle, scalar rescaling of the cyclic lift would linearize it, and étale descent would force its degree to be divisible by the subgroup order. Thus Pic^1 has free G action; no false freeness claim about Pic^0 is needed.

The character-equivariant circles come from lifting a monodromy character to integral first cohomology of the base, dividing the pulled-back class by b, and integrating its harmonic representative against the period lattice. The resulting Abel/Jacobian difference is the required constant character. The character is abelian data; the proof does not assert that the full nonabelian group lifts through integral H^1. I checked the period-lattice description against Milne's primary Jacobian notes.

### Descent and the actual-division index argument

Sections 06–07 are the decisive audit, since a merely central simple algebra would not support the extraction argument.

I traced the Morita ranks and the inclusion of the earlier division algebra. A finite module of reduced rank r becomes the stated twisted vector space of rank \(e_0r\). Summing translated coherent lattices supplies a global rational descent lattice; the determinant line cancels the full cocycle with the correct weights. The derived restriction uses a Koszul resolution and remains valid for the possibly singular constraint complete intersection. After splitting the earlier central simple algebra, the reduction divides by exactly e_0, leaving fiber rank r, not \(e_0r\).

The mixed Poincaré pairing in the determinant's first Chern class is unimodular; saturating the Picard torus consumes its full top degree. Grothendieck–Riemann–Roch therefore gives fiber Euler characteristic \(\pm r\), with no omitted factorial or factor of two. Signs are irrelevant to the divisibility conclusion but do not conceal a rank factor.

I checked the finite-torsor Euler divisibility even on singular schemes: the rank-zero virtual class lowers the support filtration on G_0, so it is nilpotent. The identity involving the finite torsor then makes that class torsion after rationalization; Euler characteristic kills torsion. The free Pic^1 action supplies the torsor used here. The dimensions of cohomology after descent, including the earlier division-algebra module structure, give divisibility by \(e_0e_1\) for the polynomial p(l).

The equivariant section used for the index calculation follows by obstruction theory from the established connectivity and the finite base dimension. Its relative version supplies the homotopy needed for the comparison. Target freeness is not assumed where it is unnecessary. The character maps to the torus and the integral topological K-theory pushforward are compatible with the required coefficient integral structure. The comparison with a smooth linear section avoids the singular locus and uses the same tautological line and the constructed homotopy.

The comparison first produces coefficients \(q_j\in e_1\mathbb Z\) with \(q_0=\pm r\). The polynomial used in the arithmetic step is explicitly the normalized polynomial \(Q_*(u)=\sum_j(q_j/e_1)u^j\), whose constant coefficient is \(\pm r/e_1\). The exact arithmetic conclusion is a truncated-polynomial annihilation

\[
A_b(u)^s Q_*(u)=0\pmod{(e_0,u^{h+1})}.
\]

For every prime dividing e_0, the initial order modulo p is the stated \(\nu=s(p^{v_p(b)}-1)\). Choosing \(h\ge v_p(e_0)\nu\) permits repeated division by p and truncation, forcing \(e_0\mid Q_*(0)\), hence \(e_0e_1\mid r\). This normalization is essential: separate divisibility of r by e_0 and e_1 would not suffice when they share primes. Parameters h and M are chosen before e_1; the index of the new algebra is not used circularly to choose its own connectivity. Applying the divisibility to a hypothetical proper simple left ideal excludes a reduced rank strictly between zero and the degree \(e_0e_1\), so the central simple algebra is a division algebra. Composite b, s=0, and e_0=1 do not invalidate the argument.

### Inductive assembly

Section 08 does not substitute noncommuting scalar coefficients as though they commute. Fresh tensor-factor coefficients centralize the previous algebra, while the previously constructed linear forms commute. The Veronese exchange relations connect allocations and give the asserted bth-power identities, establishing finiteness and integrality with only degree-one and degree-two relations.

The generic constraint is nonzero: expressing the relevant forms by pure powers, with enough blocks, prevents the coefficient relation from vanishing identically. The redundant relation absorbs an arbitrary nonzero coefficient, so no monicity assumption is silently inserted. The character recursion, including the inverse block action and terminal trivial character, has the correct direction. Galois descent preserves the low relations. Evaluation into the newly proved division algebra retains the earlier triangular rows and supplies the next one. Induction from n down to one, followed by the full ordered-basis and extraction argument above, proves the full-length Hilbert-function EGH statement needed here.

I found no unsupported transfer of the central difficulty to a stronger assertion in these steps. The unrefereed upstream proof remains an explicitly cited external input; the downstream note does not pretend to prove it in five pages.

## HWW implication and all-ideal proof

I read the primary seven-page arXiv full text of Harima, Wachi, and Watanabe, including Definition 2, Propositions 7–8, the relevant truncation result, Conjecture 10, Theorem 11 and its proof, and the stated restricted consequences afterward. Definition 2 already quantifies over all ideals, and Theorem 11 assumes EGH for the given complete intersection, in exactly the form used by the note. The publisher DOI could not be fetched in this audit; I do not claim to have independently read the publisher PDF. The arXiv text is sufficient to check the cited argument.

I also reconstructed the manuscript's self-contained downstream proof:

* The displayed rectangle chains partition every product of two chains and have endpoint-rank sums equal to the total rank. Induction preserves saturated symmetric chains. Whenever consecutive rank sizes do not decrease, every chain meeting the earlier rank has a successor. This includes a plateau above the middle; an ending chain there would force strict decrease.
* A multiplicative monomial order and echelon basis transfer the shadow injection from monomials to any vector subspace of the pure-power quotient. Surviving variable multiples have the expected leading monomials, giving \(\dim W\le\dim B_1W\).
* Apply fixed-CI EGH to the preimage of AV for \(V\subseteq A_j\). Equality of quotient Hilbert functions gives \(\dim J_j=\dim V\) and \(\dim J_{j+1}=\dim A_1V\). The ideal property gives the intermediate inequality \(\dim B_1J_j\le\dim J_{j+1}\). Extra generators in the counterpart cause no false equality claim.
* Removing the initial homogeneous layer changes the generator count by exactly \(\dim A_1I_\alpha-\dim I_\alpha\). Matching makes this nonnegative below the last maximal Hilbert degree p; iterating gives \(\mu(I)\le\mu(I\cap\mathfrak m^p)\).
* For \(I\subseteq\mathfrak m^p\), let \(J=\operatorname{Ann}(\mathfrak m I)\). Frobenius duality identifies annihilator dimensions with complementary dimensions; \(\mathfrak mJ\subseteq\operatorname{Ann}(I)\) gives \(\mu(J)\ge\mu(I)\). The degree pairings give \(\operatorname{Ann}(\mathfrak m^u)=\mathfrak m^{c-u+1}\), including u=0 and u=c+1. Consequently J contains \(\mathfrak m^{c-p}\), hence \(\mathfrak m^p\). Compression of J gives \(\mu(I)\le\mu(\mathfrak m^p)=h_p\).
* For an arbitrary ideal, use the finite intersection filtration \(I\cap\mathfrak m^j\). Its associated graded ideal is a homogeneous ideal J in A. The inclusion \(\mathfrak mJ\subseteq\operatorname{gr}(\mathfrak m I)\), and preservation of total dimensions, give
  \(\mu(I)=\dim J-\dim\operatorname{gr}(\mathfrak m I)\le\dim J-\dim\mathfrak mJ=\mu(J)\).
  This is an inequality, not a false equality between the generator counts.
* Standard grading gives \(\mathfrak m^p/\mathfrak m^{p+1}\cong A_p\), so the power \(\mathfrak m^p\) actually attains the maximum. In the field case p=0, this is the unit ideal.

A useful adversarial check on the filtration direction is \(A=\mathbb Q[x,y]/(x^3,y^4)\) and \(I=(x^2+y^3)\). Here I has basis
\(x^2+y^3,x^2y,x^2y^2,x^2y^3,xy^3\), while \(\mathfrak mI\) has the last four as a basis, giving \(\mu(I)=1\). Its initial homogeneous ideal is \(J=(x^2,xy^3)\); \(\mathfrak mJ\) has basis \(x^2y,x^2y^2,x^2y^3\), giving \(\mu(J)=2\). Thus the inclusion can be strict inside the exact target class. The manuscript uses the correct inequality and survives this test.

I could not independently fetch Watanabe's original 1987 chapter through its DOI and do not claim to have read its Lemma 2.4. HWW supplies the bibliographic reference, and the note proves the requisite filtration inequality directly. That unavailable publisher text is therefore not an unsupported logical dependency of the note.

## Attribution, current scope, and priority

The precise new role of the note is to record the immediate consequence obtained by combining the external characteristic-zero EGH theorem with HWW's previously published implication. It does not supply a new Sperner mechanism or independently solve EGH. The paper, README, description, and bibliography make this inheritance explicit. The manuscript-specific supplied OpenAI citation metadata is retained, as are the pinned source revision and known-reduction citations.

The two upstream manuscripts are dated September 23, 2026. I checked the official OpenAI announcement dated October 6, 2026 and the current remote HEAD against the pinned revision. A manuscript date is not treated as public priority. HWW's arXiv v1 public submission is January 26, 2016; the retrieved v1 PDF has a later internal date, which is not used to overwrite the public arXiv history.

I inspected current primary scope sources, not only abstracts:

* Guntürkün's primary EGH survey discusses the known EGH-to-Sperner consequence. It reinforces the inherited-mechanism attribution.
* Kuzmanovski's August 2026 v1 has bounded-degree-window conclusions under sufficiently large initial-degree conditions and restricted multiplication assertions. Those statements do not by themselves provide every-overideal full-length EGH for this target.
* Abedelfatah's July 2026 v1 has restricted almost-complete-intersection quadratic conclusions with specified extra generators, not the unrestricted overideal quantifier here.
* I searched the pinned upstream TeX/Markdown catalogue for the Sperner/Dilworth/HWW terminology and inspected the relevant companion statements. I did not find an explicit duplicate unrestricted Sperner note there.
* I ran current exact-title and Sperner/complete-intersection/EGH/OpenAI searches and inspected the identified primary sources. I found no explicit previously public complete duplicate of this note's unconditional target among those inspected sources.

That is a bounded priority audit, not proof of firstness or of absence of a paper under other terminology. The package makes no first-priority claim and advertises the result as an immediate corollary; this restraint is appropriate. If a complete duplicate later emerges, this audit cannot establish novelty against it.

The LPP manuscript's Theorem 1.1 and Corollary 1.2 have the stated stronger characteristic-zero scope. I checked those exact statements, its imported construction, and field descent. Its later stronger Betti proof is unnecessary and has not been certified by this complete review. The frozen note correctly says that the stronger inequalities are not needed.

## Archived evidence and code audit

After the primary reconstruction, I read the actual intended dependency ledger, approach table, and all seven archived scoped proof/audit notes: companion_audit, picard_subaudit, lpp_audit, lpp_box_tests, downstream_proof, priority_audit, and root_dependency_check. I checked their assumptions, mechanisms, limitations, and stated gaps against the source and manuscript. They are explicitly scoped historical evidence, not seven independent certifications of the full deposit. In particular, an earlier partial confidence estimate or narrower conditional conclusion is not silently rewritten as a later complete-package approval.

I personally read the reproduction runner, Hilbert example code, companion arithmetic checker, and bounded-box checker. The Hilbert polynomials use exact integer convolution and independent small-case enumeration. The companion script checks bounded arithmetic patterns and the modular Frobenius orders; it is not a computational proof of the geometric division construction. The bounded-box code enumerates its finite admissible domain and compares independent incidence/shadow quantities. Its 63,319 stable sets do not prove the full stronger LPP theorem. These limitations are stated in the paper/README and reproduction receipt.

The deterministic example JSON and bounded-box results reproduced exactly. The listed Hilbert examples, maxima, and all maximal layers agree: the field cases have maximum 1; degrees (1,2,4) give coefficients 1,2,2,2,1 and maximum 2; (2,2,2) give 1,3,3,1 and maximum 3; (2,3,4) give 1,3,5,6,5,3,1 and maximum 6; (3,3,3) give 1,3,6,7,6,3,1 and maximum 7; eight quadrics give binomial coefficients and maximum 70. Plateaus, one-variable cases, and empty/linear sequences were not omitted.

## Exact artifact and reproducibility evidence

The exact reviewed manifest SHA-256 is

497c2a0a2e8a0468ebb4b400867768dac144dedbc255ff0ff6a757355a4b37cf.

| Actual payload | Bytes | SHA-256 |
|---|---:|---|
| paper.pdf | 73113 | 5447339c4eedbaa9db5b973903092fca45d0ea243548efc72695d85facb81bf2 |
| source.zip | 9836 | 5812182936923da18c088033422b8f5a2455ecbe55b75fc24877159efdc903f2 |
| verification.zip | 65195 | 4f50fbb5089e360283b0e6136a1dfa46a722ba842b7e3526d7dfd25fd6aab975 |

Both my independent inventory and the fresh mechanical agent match receipts/candidate_v2.json exactly. The source archive contains exactly four members; the verification archive contains exactly twenty-one members. Every member hash is saved in reviews/review_3_exact_inventory.json. The manuscript member SHA-256 is 86a9fadc467764915dfb418a3898d01021b801af67b6c710291f2cdb48db865d. Duplicate shared README/license members are identical across archives. CRC checks passed; there were no duplicate archive entries, unsafe paths, symlinks, encrypted members, or unintended extra files.

The manifest lists the three actual payload files separately, not an outer organizer archive. Metadata says preprint, October 6, 2026, Alec Kriebel, ORCID 0009-0001-9320-500X, open access, CC BY 4.0, and the appropriate derived-from identifiers. No affiliation or coauthor is invented. The author/title/date/license agree across the package, subject to the required title-scope repair identified above. Extensive AI use and the absence of conventional human peer review/refereeing are expressly disclosed; automated adversarial reviews are not described as human review. No follow-on formalization is claimed.

No credential markers or embedded executable PDF content were identified. The PDF has no JavaScript or embedded-file payload, and no form or encryption. Only original project-authored material is licensed here under CC BY 4.0; the cited upstream works retain their own rights and are not redistributed in these archives.

I independently verified the 28 pinned-source receipt entries against the actual pinned Git objects. All original hashes match. Twenty-six local text/source copies match; the two original companion PDFs are intentionally absent as local redistributed copies, and their hashes match the originals in the read-only clone. The original companion PDF was inspected against its relevant TeX theorem statements. No source mismatch was found. Successful upstream builds, where reported in the archive, are explicitly distinguished from proof verification.

I ran the actual extracted runner with the specified compiler:

python3 verification/reproduce.py --compiler /Users/alec/.local/bin/tectonic

It passed 252 independent small Hilbert examples, 87,108 truncated arithmetic pairs, 396 Frobenius-order checks, and the complete archived bounded domain of 205 bound tuples, 2,138 degree boxes, and 63,319 stable sets. The maximal box size was 70. The fresh PDF build succeeded with no overfull boxes or undefined references. Runtime versions were Python 3.14.6, Tectonic 0.16.9, and Poppler 26.08.0. The Python source parses using the Python 3.10 grammar; actual execution under Python 3.10 was not performed, so runtime evidence is the stated 3.14.6 environment.

The reproduction runner's fresh PDF had SHA-256 406e80df186918f67565af77773eb9a8c068865d76b8c0deb9ab51b3f4013aa8 and the same 73,113-byte size. The README correctly allows timestamp-dependent PDF bytes. More strongly, I separately rebuilt the extracted manuscript and compared all five 110-dpi Poppler page render hashes: every rebuilt page was pixel-identical to the actual deposited PDF rendering.

I visually inspected every actual deposited page using image viewing, rather than accepting a log or prior receipt. Formulas, table, typography, references, ORCID, page breaks, and glyphs were clean and legible. No clipping, overlap, missing glyph, or broken reference was identified. Page 3 is dense but readable. The paper is five pages as advertised. The title remains the required repair; a clean rendering does not excuse that scope issue.

## Primary sources actually read

Local pinned sources, all before scoped-note acceptance:

* The upstream repository README and the two manuscript-specific README citation blocks at the pinned revision.
* Commuting-Division-Coefficient-Forms build Sections 01–08 in full, and Section 09's full-length characteristic-zero field descent. The tail of Section 03 was reread after an initially truncated combined display.
* The actual companion PDF's relevant first theorem/corollary statements, checked against the source.
* LPP build Section 01 introduction statements, Section 01 forms/imported construction, and Section 08 characteristic-zero field scope. I did not certify all later stronger Betti sections.
* The pinned Lean README/catalogue and searches for genuinely applicable family-200 declarations; no relevant formalization was found.

Public primary sources and inspected portions:

* [Harima–Wachi–Watanabe, arXiv:1601.06928v1](https://arxiv.org/abs/1601.06928v1): full seven-page text, especially Definition 2 and Theorem 11's entire proof.
* [Official OpenAI collection announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/): release date and repository link.
* [Hamm–Lê, BSMF 113 (1985), original PDF](https://www.numdam.org/article/BSMF_1985__113__123_0.pdf): Theorem 1.1.3(ii), printed page 126, and its relevant open-complement scope.
* [Schnürer–Soergel, original primary PDF](https://www.numdam.org/item/10.4171/RSMUP/135-13.pdf): Corollary 2.11 and Theorems 5.9–5.10 concerning locally proper compact-support pushforwards and base change.
* [Schapira, author-hosted sheaf notes](https://webusers.imj-prg.fr/~pierre.schapira/LectNotes/SHV.pdf): Proposition 5.1.2(ii), printed page 106, for real-manifold compact-support cohomological dimension.
* [Milne, author-hosted Jacobian varieties notes](https://www.jmilne.org/math/xnotes/JVs.pdf): the integral period-lattice description, Proposition 2.2 and Theorem 2.5.
* [Guntürkün, EGH survey v2](https://arxiv.org/pdf/2103.14106v2): Section 5's known Sperner consequence.
* [Kuzmanovski, August 2026 v1](https://arxiv.org/html/2608.17281v1): introductory scope and Theorems 1.4–1.5 and 1.10–1.11.
* [Abedelfatah, July 2026 v1](https://arxiv.org/pdf/2607.20035v1): Theorems 4.2–4.3 and their restricted hypotheses.

DOI pages for HWW and Watanabe were attempted but were not accessible in this audit. I distinguish those failed retrievals from the primary full text actually read. Search failure is not a novelty certificate.

## Saved independent receipts and closure

The independent artifacts are:

* reviews/review_3_exact_inventory.json — manifest, payload SHA-256/MD5/bytes, all 25 exact archive-member hashes.
* reviews/review_3_reproduction.json — my fresh extracted-package run and compiler/version results.
* reviews/review_3_visual_versions.json — all-five-page personal visual inspection and exact rebuilt render comparison.
* reviews/review_3_pinned_inputs.json — all 28 pinned original inputs and local-copy status.
* reviews/review_3_payload_receipt.json — independently delegated mechanical audit with its own exact member inventory and restrictions.
* reviews/review_3_closure.json — final frozen-version rehash and audit closure.

No publication or tracker action was taken. The frozen v2 bytes remain the audited bytes. The mandatory scope-title repair must be applied globally and then independently reviewed as a new exact candidate before publication.
