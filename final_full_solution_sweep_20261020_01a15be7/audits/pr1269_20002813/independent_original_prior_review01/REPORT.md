# PR1269 /20002813: independent original-subquestion, mathematics and prior-publication audit

Date:22October2026 UTC. Immutable head `11aff32f2bb6900234c5f468f21860913c09dcd7`, base `4b27092a448d53b61408355ce44ec38d103a1ce4`. The full PR body and all eight immutable added files were read and hash-authenticated. The comparison changes only attempts/20002813 and no QUEUE line. All work is confined to this independent folder; no old review, Git state, service, person or other agent was modified/contacted.

## Decision

**Accept the complete affirmative answer to the actual separately posed algebra-group question in the remark to AIM Problem1.1.** For every finite-dimensional associative nilpotent algebra J over every finite field, the canonical degree-weighted characters of the standard two-sided-orbit theory of G=1+J multiply with nonnegative integral coefficients. These coefficients count decompositions of one fixed target functional. This is not a manufactured special case: the primary problem list expressly asks this algebra-group question separately. The broad classification of all supercharacter theories is not resolved.

**Prior publication is authenticated.** The result is an elementary direct consequence of the construction and normalization already proved by Persi Diaconis and I.M.Isaacs, *Supercharacters and superclasses for algebra groups*, Transactions of the AMS360(5),2359–2392, May2008, DOI **10.1090/S0002-9947-07-04365-6**, electronically published20November2007. In this audit the actual publisher PDF was obtained with HTTP200,344264bytes, SHA256 `97f2ec10b33e448f3d669c112c99ecfadd59e53e7563549ae7bc17f396ceeae8`. Its essential proofs were directly read. The earlier PR's403/source-access statements are historical; this audit does not repeat them as current access limits.

The exact canonical bridge is now directly certified by **Theorem5.5(b) and Theorem5.6**, not an invented theorem number inferred from an abstract. The canonical fixed-functional product formula follows by the complete finite counting proof below. The paper's separate Theorem6.6 concerns conventional normalized supercharacters. Its mere integrality under that other normalization would not, alone, justify integrality after rescaling; it is not the sole argument used here.

One qualified four-literal-string tracker row, blankB, is proposed in `PROPOSED_ROW.json`, using the existing journal DOI and explicitly covering only the original algebra-group remark. Fresh full43-column numeric-gid GWS reads at09:38:24 and09:47:27UTC returned the same191rows, with no matching problem/result/DOI/title/author family. No row was written. Parent adoption and the immediate pre-write concurrency check remain required. No new Zenodo record or new mathematical novelty claim is appropriate for this prior corollary.

## 1. Original question and eligibility

The actual [AIM problem list](https://aimath.org/WWN/supercharacters/supercharacters.pdf), edited by Carolina Benedetti, identifies the workshop17–21May2010. PDF1 displays the canonical character `sigma_X=sum_(chi in X)chi(1)chi`, where X is a block in a supercharacter theory of a finite group. Problem1.1 asks when products in this basis have nonnegative integral expansion coefficients. Its accompanying remark independently asks about the natural algebra-group characters. This exact page was freshly fetched, text-read and visually inspected. The file is53794bytes, SHA256 `b25dad747e4e42f81db9346826caf0de42d54800c612e59d1031b0fafd48105c`.

The natural algebra-group theory is the standard Diaconis–Isaacs two-sided-orbit theory. The PR answers its whole class of finite fields and nilpotent associative algebras, not just unitriangular examples. It therefore qualifies as a complete answer to that original subquestion even though general Problem1.1 remains a classification problem. The tracker must preserve that distinction.

Products here are pointwise products of class functions on one fixed group, equivalently tensor products of its representations. No induction product between different group sizes, Hopf multiplication, arbitrary coarsening, or every possible theory on the same algebra group is asserted. Zero coefficients are allowed; a linear combination lists only basis terms with positive coefficients. Multiplication by the trivial character shows why strict positivity at every possible target is not intended.

## 2. Exact universal claim and finite-field pairing

Let J be finite-dimensional, associative and nilpotent over F_q, and G=1+J. Nilpotence makes each1+x invertible by a finite geometric series, and associativity gives `(1+x)(1+y)=1+x+y+xy`. Fix any nontrivial additive character theta of F_q. Write `J*=Hom_Fq(J,F_q)` and

`e_lambda(1+x)=theta(lambda(x))`.

These are additive Fourier characters on J pulled back by the set bijection J→G. They are generally not ordinary linear group characters of G; that distinction is essential.

If lambda-mu is a nonzero F_q-linear functional, its image is all of F_q. Its composite with theta is therefore a nontrivial additive character of J. The map from J* to the full character group of J's additive group is injective, and both sides have cardinality|J|, so it is bijective. Thus the e_lambda form an orthonormal basis for all functions on the underlying set of G, using normalized counting measure. It does not matter that theta may have a nontrivial kernel: surjectivity of a nonzero F_q-linear functional is enough. No false faithfulness assumption is introduced for extension fields.

Changing nontrivial theta amounts to multiplication of the functional label by a nonzero field scalar and permutes the same orbit family. All prime powers q>=2, including characteristic2, are covered. For J=0 there is one functional, one group element and one orbit, and the formula below reduces to1*1=1.

## 3. Canonical normalization: two independently checked routes

Let O=G lambda G and put `F_O=sum_(mu in O)e_mu`. Let r_O=|lambda G|=|G lambda|. The conventional supercharacter is

`tau_O=(r_O/|O|)F_O`.

Write `n_lambda=|O|/r_O`, the integral number of one-sided orbits in the two-sided orbit. It is important that the target AIM character is **canonical** `sigma_O=sum_(chi in X_O)chi(1)chi`, rather than tau_O.

The direct journal-source route is now available. Diaconis–Isaacs Lemma4.2 identifies one-sided orbits as affine linear spaces and proves equality of their sizes; Lemma4.3 proves the orbit count n_lambda. Lemma5.3 constructs invariant spans in the regular group bimodule. For the right orbit of -lambda this span affords an actual character; Theorem5.4 identifies it as induced from a linear character of the stabilizer. Theorem5.5 proves that the span for the full negative two-sided orbit is a two-sided ideal of CG and affords `n_lambda tau_O=sigma_O`, with disjoint exhaustive irreducible supports. Theorem5.6 then computes its trace as exactly F_O. Combining5.5(b) and5.6 gives `sigma_O=F_O` with no remaining scalar.

The essential published proofs were read, not just their statements. In5.5 the two-sided span is a direct sum of n_lambda isomorphic one-sided modules, and semisimplicity of CG identifies its right character as the sum of irreducible degrees times irreducibles. Different orbit ideals sum to the regular module, so supports cannot overlap. In5.6 the trace initially sums over functionals fixed by the tested group element. Lemma5.7 shows that the missing left-orbit sums vanish by a surjective evaluation map and nontrivial additive-character orthogonality. Adding these missing terms yields the entire two-sided Fourier sum. The signs from using the negative orbit and g versus g^(-1) are handled by conjugating character values; no incorrect identification of an individual e_lambda as a group character is used. Maschke/semisimple complex group-algebra decomposition and elementary character orthogonality are standard imported background, not unproved new research assertions.

An independent normalization derivation also verifies the PR's route. The conventional tau_O are characters with disjoint exhaustive irreducible supports, by the established construction. Fourier orthogonality gives `sum_O F_O=rho_G`, the regular character, since its value is|G| at1 and0 elsewhere. Each F_O is a positive scalar multiple of tau_O, supported on its block. Comparing each irreducible coefficient in rho_G, which is its degree, forces that coefficient in its unique F_O to equal the same degree. Hence F_O=sigma_O. This does not assume that an arbitrary rational rescaling of a character remains integral; the correct integral multiplicities follow from the regular-character comparison and disjointness.

In particular `sigma_O(1)=||sigma_O||²=|O|`, whereas `tau_O(1)=r_O` and `||tau_O||²=r_O²/|O|`. For UT3(F2), canonical degrees are1,1,1,1,4, but conventional degrees are1,1,1,1,2. Their conventional unweighted sum has degree6 rather than8, so it is not rho_G. The Diaconis–Thiem preprint's incompatible unweighted regular-sum wording is excluded. The current Marbergv2 equation(2.3) corroborates the correctly weighted identity. The actual Diaconis–Isaacs publication itself now supplies the decisive version, so the audit need not depend on that faulty sentence.

## 4. Complete product proof and fixed-target integrality

For O,P two-sided orbits and nu in J*, let

`N(nu)=#{(lambda,mu) in O x P : lambda+mu=nu}`.

For g,h in G, the dual transformation `T_(g,h)nu(x)=nu(g^(-1) x h^(-1))` is invertible and F_q-linear. Its transformations are closed under composition and inversion; the right factor may be described using the opposite group. Each preserves every two-sided orbit as a set.

If nu'=T_(g,h)nu, simultaneous application of T_(g,h) to both entries gives a bijection between the decompositions counted by N(nu) and N(nu'). Its inverse is the inverse linear transformation. Consequently N is constant on a full two-sided target orbit R. This does not merely prove constancy on a smaller conjugacy orbit.

The pointwise additive-character identity `e_lambda e_mu=e_(lambda+mu)` is valid despite the nonabelian multiplication on G. Therefore

`F_O F_P=sum_(nu in J*)N(nu)e_nu=sum_R m(O,P;R)F_R`,

where `m(O,P;R)=N(nu)` for one fixed nu in R. Substituting the established F_R=sigma_R proves the exact canonical product formula. Each coefficient is a finite cardinality, hence a nonnegative integer. No divisibility condition or cancellation argument remains.

The total number of pairs whose sum lies somewhere in R is `|R|m(O,P;R)` and is generally the wrong structure coefficient. Multiplying by the zero orbit already detects that error: for a nontrivial orbit P the correct coefficient of P is1, while its aggregate pair count is|P|.

Further universal boundary identities are `m(O,{0};R)=1` for R=O and0 otherwise; the coefficient at{0} is|O| when P=-O and0 otherwise; and evaluation at identity gives `|O||P|=sum_R m(O,P;R)|R|`. They follow by direct finite bijections and independently match Fourier orthogonality. The zero algebra, q=2, nonprime fields and nonfaithful theta require no exceptions. A trivial theta is excluded; when J has positive dimension it collapses all e_lambda to1 and destroys the Fourier-basis and canonical-normalization identification.

This proves the full original algebra-group remark for its standard natural theory. It does not prove the broader classification, every supercharacter theory on the same G, or any induction/Hopf product statement.

## 5. Prior-source authentication and exact reading limits

The fresh DOI request resolved with200 to the AMS article. The HTML response was capped at6000000bytes and is explicitly marked possibly truncated; it is used only for resolver/landing identity, not as an asserted whole-body read. Separately the actual publisher PDF at the established AMS PDF URL returned a complete34-page PDF with proper end marker, journal header, article identifier, authors, online date and page range. Crossref independently matches title, journal360(5),2359–2392 and online20November2007. The printed issue is May2008. The actual source prints I.M.Isaacs, completing Crossref's abbreviated given-name field.

Directly read journal portions are: introduction/category; Lemma2.1 and its proof; the dual actions and Lemmas4.1–4.3 with proofs; the finite-field Fourier setup and Lemma5.1; the regular bimodule setup, Lemma5.3, Theorems5.4–5.6 and Lemma5.7, with their full proofs; and the conventional product Theorem6.6 and its direct-product/diagonal proof, with preceding Lemma6.5 context. Printed2375–2377/PDF17–19 were also rendered and visually checked. Theorem6.6 imports restriction Theorem6.4; its whole proof was not independently re-audited, and the canonical argument above does not require it. No claim is made to have audited all34pages or every later application.

Fresh corroborating primary sources are Diaconis–Thiem, arXivmath/0610161v1, Section2.3/PDF6–7 (orbit prefactor/support and the excluded unweighted sentence), and Eric Marberg, arXiv1012.2191v2, Sections2.2–2.3 and the relevant start of2.4/PDF4–6 (actions, equation2.2 prefactor, equation2.3 weighted regular identity and induced-character construction). Their current arXiv histories confirm v1 only for Diaconis–Thiem and latestv2 dated13January2012 for Marberg. These are corroborating publications, not duplicate publication rows for the original question. Their complete unrelated theorems are not audited here.

The foundational published source already proves the canonical Fourier identity and theory for every finite field/nilpotent associative algebra. The product count is an elementary consequence of that identity and an invertible linear action. This establishes mathematical prior coverage and defeats a new-result claim, even without proving the first date on which somebody explicitly announced an answer to the later2010 remark. No claim that the question was genuinely open at PR development is justified: the required construction predates both the2010 list and the2026 exposition. No global firstness certificate or exhaustive history of all related work is claimed.

## 6. Independent finite falsification controls

`verify_readonly.py` is newly reviewer-authored, with no imports or execution of source-author software. It constructs finite fields, nilpotent algebra multiplication, unit inverses, left/right dual actions, and two-sided orbits from those actions. It uses no downloaded orbit tables or presupposed orbit classification. Models over F2,F3,F4 include the zero algebra, a two-dimensional square-zero algebra, strictly upper-triangular3x3 matrices, and the commutative nilpotent algebra tF_q[t]/(t^4), twelve models altogether.

Every input orbit pair is convolved by explicit functional addition; target constancy and the exact pointwise product are checked at every group element. Character values use integer coordinates in the appropriate prime cyclotomic ring, including exact Z[zeta3] arithmetic, and F4 is explicitly built with t²+t+1. Trace characters with nontrivial kernels are tested, as are every nontrivial additive-character choice in these fields. The checker independently evaluates the ordinary induced-character formula from the functional stabilizer and verifies `sigma=n_lambda Ind(theta_lambda)` at every element. It checks that theta_lambda really restricts to a linear group character on that stabilizer rather than presuming it from additive linearity alone.

All1028orbit products and39314pointwise identities pass. Additional checks cover Fourier regular-character values, canonical norms/degrees, one-sided stabilizer index, zero-target coefficients, characteristic2, the trivial group, and induction normalization. Negative controls reject the trivial additive character, the orbit-aggregate coefficient and the unweighted conventional regular sum. These finite controls attempt to falsify the theorem and expose normalization mistakes; the universal conclusion is the proof in Sections2–4 and the directly inspected published construction, not an inference from examples.

Explicit exception guards remain active under normal,-O,-OO. The read-only verifier additionally checks exact source receipts, every immutable Git blob, the nested PR manifest, private flags and whole closed inventory, actual PDF signature/end marker and SHA, Crossref identity, both numeric-gid ledger captures and the proposed-row scope. It reads this folder only, writes nothing and makes no network/subprocess call. Final validation outputs record the stable three-mode replay. Source-author code was never executed; the PR contains no source program whose reported diagnostics were silently adopted as proof.

## 7. Publication accounting and public-package checks

The existing journal DOI is an appropriate record for this original subquestion. Its canonical bridge is directly published and its complete short product deduction has now been verified; no new paper is necessary to cover a missed original answer. The row explicitly calls it a consequence of Theorems5.5(b)/5.6 rather than pretending the exact fixed-functional formula is Theorem6.6 or assigning a new authorship to this project. The general classification remains unresolved in the row.

Both all43-column numeric-gid spreadsheet captures have191rows and SHA256 `fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1`. OriginalID, numericID, exact PR URL, Diaconis–Isaacs DOI, authors, supercharacter/algebra-group terminology and corroborating arXiv aliases have no matching row. Initial naked1269substring matches were unrelated OWR identifiers, independently rejected semantically. The proposal respects the four-column schema and leaves Solution Chat URL empty.

Public original-ID/numeric searches and DataCite title searches found no additional target package; DataCite's zero result does not negate a Crossref-registered journal DOI. A Zenodo supercharacter/algebra query returned only Ferudun23018019, whose actual registry metadata concerns a distinct AIM0102 symmetric-group Hopf obstruction and different operation/families. It is not this pointwise product theorem. The guessed EulerSolve target path returns404. No matching public unfinished upload was found; private/unindexed deposits cannot be ruled out by these searches. The paper's ordinary journal proof is the needed scientific support; no computer certificate or Zenodo source ZIP is required for this classical theorem, and none is falsely claimed downloaded.

The PR and this audit are AI-assisted research/proof exposition and verification. That is not a statement about the use of AI in the2007/08 source, nor does it replace or certify conventional journal peer review. No new preprint, new DOI, upload reservation or public-service mutation was performed by this audit.

## 8. Disposition and evidence preservation

Recommend parent adoption of the original-remark-only existing-publication row after a fresh immediate semantic/DOI duplicate check. No mathematical repair is required. Preserve the PR's correct short proof with its scope and credit; general classification being unresolved is not a reason to discard a completely answered question that the original remark explicitly poses. Update any current source-access description to distinguish this audit's newly obtained journal PDF from the earlier historical403, without rewriting history as though the earlier reviewer read it.

Raw source/PR/ledger/search bodies, text extracts and renders remain ignored private_sources and are marked private in the closed manifest. Only authored reasoning, verifier and public-scope provenance/hash metadata are intended for sharing. SOURCE_INDEX and SEARCH_INDEX identify actual read scopes and the capped HTML response; ALIASES and PRIORITY_DECISION preserve result/operation/normalization boundaries. The closed inventory covers nested manifests and excludes only its exact top-level MANIFEST.json. Previous closed reviews remain untouched. Family completion100% means this bounded review is complete; parent sweep remains80%.
