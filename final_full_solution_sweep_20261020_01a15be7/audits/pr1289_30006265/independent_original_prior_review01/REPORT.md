# PR1289 / 30006265 — independent original-scope review01

**Classification: partial coverage of the original bundled identification target; complete valid explicit ordinary-module obstruction. No full-solution accounting row.** For SL2 over an algebraically closed field of characteristic3, the PR correctly proves Sym²(Sym²E)=T(4) and t(2)=z²+z⁻², which is not the character of any finite-dimensional rational SL2-module. This refutes a universal always-an-ordinary-module interpretation and corrects the corpus's dated claim that such identification is merely unestablished. It does not identify a natural geometric/representation-theoretic object for every dominant weight, nor give a pointwise classification of which quotients are module characters.

The actual original asks what t(λ) is the character of and announces a geometric answer later in the same contribution. The corpus appends a subordinate module clause to that one compound target, rather than presenting a separate original yes/no conjecture. Root confirmed the compound-target interpretation and instructed closure as partial. The original-scope gap is recorded precisely; the review does not expand the unrelated56-page geometric proof to manufacture full coverage. No literal four-cell proposal is created.

This is an AI-assisted independent internal audit, not external human/referee review or proof-assistant certification. No people, other agents or chats were contacted. No source-author code was run. Only public uncredentialed primary-source reads, read-only existing Git objects, read-only cached corpus extraction and local diagnostics occurred. No service writes, credential use, CASE/cursor changes, Git/index/ref/worktree mutations or uploads. `publication_ready=false`, `root_adopted=false`, `new_publication=false`. Own audit completion100%; overall research goal80%.

## Exact inputs and priority scope decision

Head `d31d3b3cda1b56d9e85e3d5e07847355d1a6814f` has eight actual attempt files. Every file was copied from existing immutable objects, checked by Git blob SHA1 and SHA256/size, and read fully. `INPUT_BINDING.json` records the identities. The8,301-byte EXPLICIT_PROOF has SHA256 `eca4d136130bbe4b2d74bf634f18cb1770f1cbd74974ab50062e50b14a9dcf0b`. The complete acceptance, audit, README, source pins, manifests and check-result/summary files were inspected. No QUEUE change is among the eight paths. Historical acceptance labels and computations were not substituted for this fresh review.

The [primary original](https://ems.press/content/serial-article-files/51851) is Pramod N.Achar, *Smith–Treumann localization and the Steinberg module*, joint work with Paul Sobaje, in OWR25/2025, printed pp.1275–1277 / PDF5–7. All three contribution pages were read completely; the setup, Question1 and Theorem1 were also visually checked. Its setup is semisimple simply connected G over algebraically closed k of characteristic p>0. No explicit good-prime restriction appears in the inspected Question1/setup. After defining the Steinberg quotient and discussing positivity/monotonicity, it asks:

> What is t(λ) the character of?

Questions2/3 intervene before the reported geometric Theorem1 on p.1276. That theorem expresses the quotient through ranks of suitable Smith-parity restrictions. The contribution explicitly describes work in progress and reports results. It does not separately pose a universal ordinary finite-dimensional rational-G-module conjecture, and it does not supply the complete geometric proof mechanism.

The exact cached corpus payload was recovered using a read-only SQLite connection and `SELECT payload FROM records WHERE key=?` for key30006265. The original4,146UTF8bytes have SHA256 `7fe3346657ba0cce3a138e587f5592fa6607168301f82f9c8aadff9c0a15dc7c`, exactly the parent's pin. `private/CACHED_CORPUS_SQLITE_PAYLOAD.json` preserves those bytes. Its decoded object equals the independently selected pretest record from the canonical cached problems.json. `CORPUS_BINDING02.json` records both provenance routes and equality. A first lookup in research_results returned null and is retained explicitly as a failed lookup, not a claimed corpus record.

The corpus's single statement first asks, for each dominant λ, to identify a natural representation-theoretic or geometric object with character t(λ), then adds an in-particular question about finite-dimensional modules. Its `original_statement` retains the open-ended original question. The appended clause is not a separately numbered original problem. The `corrected_verified` metadata cannot turn that added wording into a separately posed source conjecture. The cached `partially_solved` tag is historical triage, not a mathematical proof or an exclusion by itself.

Two logical distinctions matter. First, a single valid example refutes “all quotients are ordinary module characters.” Second, it does not answer the full identification request for every λ. Even the module question read pointwise is not classified by one example: t(0)=1 is the trivial module character, whereas t(2) in this example is not a rational-G-character. The accepted result is therefore a complete obstruction to the universal positive reading, retained within a partial-original-target packet. This classification does not depend on inventing an extra bad-prime requirement; the logical mismatch remains even restricted to good characteristic.

## Fresh sources and exact inspection limits

All four versioned primary PDFs were freshly retrieved with HTTP200 and exactly match the submitted pins:

| Source | Bytes | SHA256 |
| --- | ---: | --- |
| OWR25/2025, EMS51851 |672,101|`2c0ebcb4a95623163e3a3d6e3d5e0889c2a0239c902b976fb525c3dcc782ea6f`|
| Achar–Sobaje arXiv2606.21697v1 |912,896|`e4afd737b0a45dc77c4e9c17c5df40057d9a02f906fa2ae9b081ab66e3605e98`|
| Doty–Henke arXivmath/0205186v1 |202,015|`8fb52434afec7149a85783fbc791f17cb2f7c539312bc3aec94a14ada10f4d6f`|
| Martin arXiv1705.06980v3 |277,008|`235d7b2f26ca808c6ddfad8d738b744aca23a06a623b3f27108a3c85dbc5f1f2`|

[Achar–Sobaje v1](https://arxiv.org/abs/2606.21697v1), submitted19June2026 19:09:44UTC, is *Steinberg quotients and Smith–Treumann localization*. The primary record identifies its authors and arXiv DOI10.48550/arXiv.2606.21697. Its introduction explicitly says a Steinberg quotient is in general not a G-module character. Pages1–4 and41 were read, with Theorem1.2/setup restrictions visually checked. Theorems1.1/1.2 and7.6 assume p good. The general reductive setup needs a weightς pairing1 with every simple coroot; for semisimple simply connected G,ς=ρ. The sheaf setup uses a different auxiliary characteristic, Gm-equivariance and the pς-twisted loop action; the formula uses unsigned total stalk ranks, not an alternating Euler characteristic.

The page41 proof gives a conditional formal division mechanism: Corollary5.9 identifies the averaging image of an indecomposable spherical parity object; Figure7.1/Theorem7.5 relates characters through the commuting localization/averaging diagram; a Riche–Williamson Smith-image result and character identities identify the numerator with the tilting character. The full essential proofs of those geometric identifications, commutativity, perversity and indecomposability preservation were not independently checked here. A statement/setup match plus formal division conditional on those results is not promoted to a full proof audit. The56-page manuscript was not reviewed in full because the partial scope decision already settles this packet's accounting treatment.

The original report announces a geometric answer; the later manuscript supplies a detailed theorem under its own hypotheses. This review neither calls the geometric interpretation false nor claims that any bad-prime cases are open, solved or required by an invented strengthened question. The printed original setup and the later explicit restrictions are reported separately. No complete-original geometric certification is given without substantive essential-mechanism verification. The existence of an announced source formula does not convert the rank-one obstruction into that verification.

[Doty–Henke v1](https://arxiv.org/abs/math/0205186v1), *Decomposition of tensor products of modular irreducibles for SL2*, by Stephen Doty and Anne Henke, submitted16May2002, supplies the needed established-character check. Pages2–3 were read; Lemma1.1 and proof were visually inspected. Part(a) identifies restricted T(u)=L(u)=∇(u)=Δ(u) for0≤u≤p−1. Part(b) gives T(u) in the range p≤u≤2p−2, with character χ(u)+χ(2p−2−u). At p=3,u=4 this is χ(4)+χ(0). The proof explicitly recalls ∇(r)=Sym^rE; p.2 states existence/uniqueness of indecomposable tiltings with both filtrations. This cross-check establishes that the rank-one character phenomenon is old, without claiming that this paper separately phrases the precise present quotient objection or a first-counterexample chronology.

[Samuel Martin v3](https://arxiv.org/abs/1705.06980v3), *On Certain Tilting Modules for SL2*, version19September2017, p.2 was read and visually inspected. It states the induced convention ∇(r)=Sym^rE, Δ(r)=∇(r)*, the two-filtration definition and uniqueness of T(r), and ordinary characters in the integer Laurent polynomial ring. These authenticate the conventions and imported standard structural input. Their foundational proofs need not be re-proved for the explicit argument; the main indecomposability proof avoids using direct-summand closure of the tilting category.

`SOURCE_REVIEW.json` records exact read scope. No journal-final identity or peer-review status is invented from arXiv versions. No source DOI is assigned to a nonexistent separate counterexample paper or used to create a full-target row. Source PDFs, text and images remain private local evidence, not redistributed or uploaded.

## Complete explicit module verification

Let k be algebraically closed of characteristic3, E its natural SL2-module with basis x,y, and V=Sym²E with basis a=x²,b=xy,c=y² of exact integer torus weights2,0,−2. The lower root subgroup sends x↦x+ty and y↦y, hence

\[
a\mapsto a+2tb+t^2c,\quad b\mapsto b+tc,\quad c\mapsto c.
\]

The upper subgroup has the exchanged formulas. Every nonzero submodule contains a torus weight vector. Starting with any of a,b,c, these root orbits generate all three vectors, since2≠0 and polynomial coefficients can be recovered over infinite k. Thus V is simple and equals ∇(2). The symmetric bilinear form with B(a,c)=B(c,a)=B(b,b)=1 and all other pairings0 is invariant under both full root polynomials and the torus; its determinant is−1. Hence V is self-dual, also Δ(2), and is the indecomposable tilting T(2)=St.

Set W=Sym²V, with ordered basis a²,ab,ac,b²,bc,c² and exact torus weights4,2,0,0,−2,−4. Its induced symmetric invariant form is

\[
C(v_1v_2,w_1w_2)=B(v_1,w_1)B(v_2,w_2)+B(v_1,w_2)B(v_2,w_1).
\]

Its nonzero pairings are C(a²,c²)=2, C(ab,bc)=1, C(ac,ac)=1 and C(b²,b²)=2, together with symmetric partners. The Gram matrix is nondegenerate, so W≅W*. Equivalently the degree-two symmetrizer is permitted because2 is invertible. No degree-four symmetrizer or claim that Sym⁴E is self-dual is used.

Multiplication W→Sym⁴E sends the six basis vectors to x⁴,x³y,x²y²,x²y²,xy³,y⁴. It is equivariant and onto, with kernel kq for q=ac−b². Direct root formulas fix q. Therefore

\[
0\to\nabla(0)\to W\to\nabla(4)\to0
\]

is a good filtration. Ordinary duality and W≅W* give a Weyl filtration0→Δ(4)→W→Δ(0)→0. W is tilting. The distinction between a symmetric-power quotient and divided powers is essential here: E≅E* identifies Sym⁴E with Sym⁴(E*), not automatically with the linear dual of Sym⁴E in characteristic3. The submitted convention is correct and independently authenticated.

An invariant vector must be r ac+s b². Its lower-root variation is (r+s)(2tbc+t²c²), so invariance forces r+s=0; conversely q is fixed. Thus W^G=kq. An invariant functional is supported on the two weight-zero basis vectors. Writing its values there as u,v, the t² coefficient in the image of a² gives2u+4v=0, hence v=u in characteristic3. Every invariant functional kills q. The functionalℓ with values1 on ac and b² and0 elsewhere is invariant under the full root groups, andℓ(q)=0. Thus q cannot split off as a trivial summand.

For indecomposability, the whole lower orbit expands as

\[
\ell(t)a^2=a^2+tab-t^2q+t^3bc+t^4c^2.
\]

The five coefficients are linearly independent. Since k is infinite, any submodule containing a² contains every coefficient, in particular q, and has dimension at least5. In a hypothetical nontrivial decomposition W=A⊕D, the one-dimensional weight4 space belongs to one summand, say A. Then D has dimension1. Any one-dimensional rational SL2-module is trivial: on a root subgroup an algebraic homomorphism Ga→Gm must be constant, as units in k[t] are constants; root subgroups generate SL2. Consequently D⊂W^G=kq⊂A, contradiction. This proves elementary indecomposability, independently of closure-of-summands theory. The standard uniqueness of indecomposable tiltings now gives W=T(4).

The character calculation is overZ, with dimensions never reduced modulo3:

\[
\operatorname{ch}T(4)=z^4+z^2+2+z^{-2}+z^{-4}
=(z^2+1+z^{-2})(z^2+z^{-2}).
\]

Since p=3 andρ=1, this is t(2)=z²+z⁻² after division by chSt=z²+1+z⁻². It also agrees with the authenticated Doty–Henke character χ(4)+χ(0).

Suppose a finite-dimensional rational G-module M had that quotient character. Its only exact torus weights would be2 and−2, each with multiplicity1. For standard root derivatives e,f,h with[e,f]=h, conjugation by the torus has root weights±2, so eM_m⊂M_{m+2} and fM_m⊂M_{m−2}. The targets4,0,−4 are all absent. Therefore e=f=0, so h=0. But h on the weight2 line is the differential of t↦t², namely the nonzero scalar2 in characteristic3. Contradiction.

The argument concerns exact algebraic torus characters, not just their differential residues modulo3. Frobenius twists do not evade it: pure Frobenius-twisted weights are multiples of3 and have zero torus differential, unlike the proposed weight2. For example, a twist of the natural module has weights±3, not±2. The quotient remains a torus character and a virtual G-character: t(2)=chSt−chk. The example is in good characteristic for typeA1. It proves no statement about the truth of general geometric formulas at bad primes, and no novelty or firstness.

## Falsification and finite diagnostics

The independent route checks symmetric/dual conventions, both invariant forms, the multiplication kernel and both filtrations, all invariant vectors/functionals, elementary indecomposability and the full rational-module differential contradiction. The only imported representation-theoretic structure needed to name T(4) is the authenticated standard induced/Weyl convention and uniqueness of an indecomposable tilting with prescribed highest weight. No Smith–Treumann theorem, geometric Satake equivalence or general tilting-character formula is needed to prove the explicit obstruction.

`check_review.py`, SHA256 `95181402cb2501cdfbfd460f7e96af3d29ce2d53d8685194c1cab0f7ad3b7743`, constructs natural root substitutions and their symmetric powers independently from the frozen monomial inputs. It compares identities coefficientwise in F3[t], including degree4 terms; it does not sample only SL2(F3). The nonzero polynomial t³−t vanishes at all three F3 points, explicitly demonstrating why such point sampling would be insufficient. Integer torus weights and character multiplicities are tracked separately; an St⊗St zero-weight multiplicity3 countercheck detects illegal reduction of character coefficients modulo3.

The diagnostics verify nondegenerate invariant forms, equivariance/rank5/kernel of multiplication, q andℓ invariance, one-dimensional invariant vector/functional spaces, a five-dimensional lower-orbit coefficient span containing q, and the two-dimensional full algebraic G-endomorphism algebra with nonzero square-zero qℓ. These polynomial linear-algebra ranks over F3 remain unchanged after extension to k. The local endomorphism algebra supports the independent elementary indecomposability proof. Exact weight-shift exclusions and nonzero weight2 differential are also checked.

Normal,−O and−OO all pass on the same checker,38frozen local source/control/scope inputs and8root anchors, including all8actual PR blobs and4matched primary PDFs. Five wrong-science controls reject in every mode: characteristic reduction of formal dimensions, false Frobenius escape, modular-weight identification, a false split retraction and replacing polynomial equality by F3-point equality. A separate unconditional deliberate failure exits1 in each mode; every positive run exits0. Explicit exceptions keep guards active under optimization. No failed positive run occurred. `VALIDATION.json` and private raw replay outputs/receipts preserve exact commands, return codes and hashes.

The exact SQLite raw-payload pin arrived after this successful diagnostic matrix. Its decoded equality to the already frozen selected JSON record was checked explicitly; it adds custody confirmation without changing any mathematical input, code, control, interpretation or result. Both carriers and `CORPUS_BINDING02.json` are closed in the final manifest. The final seal repeats this exact-payload/equality check alongside full payload readback. Tests corroborate the written proof and scope classification; their success is not a full-original geometric proof certificate.

## Aliases, preserved prior packages and final gap

The root-provided10:03:11UTC ledger snapshot was independently scanned across all returned cells: requested A1:AQ1178,43columns,191rows including header and maximum4nonempty returned columns. There are no direct target/problem/source/author matches. Four broad Frobenius leads at rows20/64/85/142 are retained in full with explicit distinctness reasons: group-scheme self-duality, Gram-matrix norm bounds, difference-field inverse Frobenius and permanent inequalities. None identifies this Steinberg quotient target. These are bounded point-in-time semantic recommendations, not eventual concurrency clearance or automatic publication exemptions.

A bounded default-visible local Markdown/JSON/text package search found the present PR/root/input records. It was not a hidden/archive census or exhaustive priority search. No source archive was copied. The primary Doty–Henke/Martin character/convention identities and Achar–Sobaje's explicit non-module warning establish old representation-theory context, without claiming an earliest exact quotient-counterexample publication.

All48closed PR1281 payloads,64closed PR1273 payloads and77closed PR1267 payloads were read back exact and left unchanged. Older operations and accounting proposals were not edited. Private sources/evidence remain local. No full-solution row, new DOI, publication, service mutation, CASE or cursor action follows from this packet.

The strongest verified theorem is the complete characteristic3 SL2 obstruction above. The exact remaining original-target gap is a general natural object identification supported by verified essential geometric mechanisms under the relevant hypotheses; source statement/setup inspection alone does not fill it. This is a completed partial-scope classification, not a claim that the geometric literature is false or globally unresolved. Root may adopt this precise disposition separately. `SCOPE_DISPOSITION.json` records the nonpromotion fields, and no `LITERAL_FOUR_CELL_PROPOSAL.json` exists.

`MANIFEST.json` closes every public/private payload by exact size/SHA256, excluding only itself and the separately hashed final `SEAL_CHECK.json` to avoid self-reference. The final source-anchored complete readback enforces exact membership and the25MiB allocated-storage cap. Own audit100%; original coverage remains partial; overall80%; readinessfalse.
