# Independent review: PR1329, 30003208 / 30002897

Review completed 2026-10-22 UTC. This is an AI-assisted mathematical and source audit, not independent human refereeing, a proof-assistant certificate, a publication-ready declaration, or a worldwide firstness certificate. No source-author code was executed. No external writes, outreach, Git mutations, merge, publication, reservation, or tracker append occurred.

## Decision and exact scope

**Accept the mathematical proof of the entire independent generation question.** For every unital C*-algebra A and every state ψ on its countable universal unital free product invariant under finite permutations, in the original GNS representation,

    D'' = T.

Here D has precisely the recursive canonical-expectation definition of Dykema–Köstler–Williams (DKW), not a substitute definition. In fact the proof establishes bounded WOT density of F(π(𝔄)) in T, with represented inputs and outputs bounded by the norm of the target. No faithfulness, separability, trace, factoriality, quantum symmetry, or normal extension of F is needed. This answers DKW Question5.3.5 and the separately posed Question2 in both OWR reports. The different inclusion question D⊂π(𝔄) remains open in this package and is not a prerequisite for eligibility here. Catalog30003208 and30002897 are aliases of this one mathematical question.

**Priority/accounting finding:** no authenticated prior publication of the full general theorem was located in the bounded search described below. The core stabilization method is unquestionably prior, and an additional route through Liu's bilateral future-expectation results makes the relation to prior work even closer than a title search suggests. Do not advertise a new coefficient lemma or a new Kaplansky technique. The defensible possible contribution is a short, fully attributed deduction answering the original general question. This audit neither certifies historical novelty nor equates the existing technique citations with a published full-target resolution. The parent must assess that narrow contribution when preparing and reviewing any publication package. No existing-record four-cell tracker proposal is warranted on the sources authenticated here.

## Input, duplicate check, and original provenance

Immutable PR head: `46e2906b587bbd76091021807218e95419d3f9c0`; PR https://github.com/AlecKriebel/Math/pull/1329. Eight exact Git blobs, including the entire QUEUE.md and seven authored files, were captured and authenticated. All seven authored files and the PR body were read; only the relevant queue entry was semantically evaluated. SOURCE_PINS.json records exact byte counts, SHA256 and Git blob identifiers. Live PR capture at this review showed open/draft, not merged. This is an input receipt, not authority for a later action without a live recheck.

Fresh numeric-gid Google Workspace CLI read occurred before substantive mathematics at 2026-10-22T11:36:06.049402Z: spreadsheet1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20, gid1254632077, all43 columns,191 rows. No target identity or semantic coverage lead was found under both catalog IDs, PR1329, DKW names, symmetric-state, tail-algebra, and question aliases. Broad token hits were unrelated. INITIAL_LEDGER_CHECK.json contains only row numbers; raw cell bodies are private. A pre-publication check would have to be repeated.

Actual primary original sources read:

* DKW, arXiv1305.7293v3, §5 opening (explicitly general symmetric states), Definition5.3.1, Observations5.3.2–3, Questions5.3.4–5, printed p16. The generation question is separate from the inclusion question. Theorem7.3 already covers quantum symmetric states, including nonfaithful states.
* Ken Dykema, OWR40/2016, *Tail algebras, amalgamated free products and KMS states*, printed pp2334–2335: https://ems.press/content/serial-article-files/46645 ; report DOI https://doi.org/10.4171/OWR/2016/40 . The setup is arbitrary finite-permutation-symmetric free-product states. Question2 is explicitly separate.
* OWR28/2015, printed pp1618–1619: https://ems.press/content/serial-article-files/46575 ; report DOI https://doi.org/10.4171/OWR/2015/28 . The same Question2 is asked, and the quantum special case is distinguished immediately afterward. Thus neither an extra faithfulness condition nor answering Question1 can be imposed on this target.

The current arXiv-v3 response has running headers dated9August2021 while the abs page labels v3 as22September2014. These exact current bytes were inspected and pinned; no claim is made that they are identical to historical2014 or journal bytes. The OWR questions independently authenticate original scope. Likewise the current1310.1566 response labels v1 while carrying an internal2018 date; historical binary identity is not inferred from its URL.

## Independent proof, including the required functional-analytic bridges

Put C_N=C*(π_j(A):j>N), B_N=C*(π_j(A):1≤j≤N), H_N=closure(B_Nξ), with orthogonal projection P_N. These are unital concrete C*-algebras. T=intersection_N C_N''. Q=C*(T∪π(𝔄)). DKW Theorem5.1.10 gives the actual canonical contractive conditional expectation F:Q→T as WOT-limit α^k on Q; it is the restriction of their G:R→fixed-point algebra. It does not give a normal expectation on all M=π(𝔄)'' in general. The finite permutation actions are spatially implemented by U_σ with U_σξ=ξ. They remain well-defined even when the original state or representation is nonfaithful: state preservation preserves the GNS null space and its inner product. DKW's isometric shift on Q is the one used below.

**Exact future compression.** Suppose x is a polynomial in copies indexed by a finite S⊂{N+1,…}. For every integer k≥1 the injection i↦i+k on S extends to a permutation of the finite ambient set U=S∪(S+k): match U\S bijectively with U\(S+k). Extend by identity off U. Its support is future-only, it fixes every first-N copy, and repeated occurrences of an index are all transported together. For y,z∈B_N,

    <α^k(x)yξ,zξ> = ψ(z*α^k(x)y)
                    = ψ(β_σ(z*xy)) = <xyξ,zξ>.

This holds for every k, not just eventually. Passing k→∞ uses only the defining shift limit on this fixed polynomial, yielding the same coefficient with F(x). Future polynomials are norm dense in C_N; F is contractive. Thus the equality extends to every x∈C_N. B_Nξ is dense in H_N; the bounded operators F(x),x then give

    P_N F(x) P_N = P_N x P_N,    x∈C_N.                 (1)

No global equality F(x)=x is asserted. No continuity of F on a WOT-convergent input net is used.

**Bounded density on arbitrary vectors.** Fix t∈T, r=||t||>0, finitely many pairs (η_l,ζ_l), and ε>0. Cyclicity implies the increasing union H_N is dense even for nonseparable A,H: each approximating word or finite sum uses finitely many copy indices; there is no countable dense subset assertion. Hence P_N→1 strongly. Choose one N such that, for every l,

    2r( ||η_l−P_Nη_l|| ||ζ_l||
        + ||P_Nη_l|| ||ζ_l−P_Nζ_l|| ) < ε/2.

Since t∈C_N'', Kaplansky density in the concrete represented algebra gives x∈C_N with ||x||≤r and

    |<(x−t)P_Nη_l,P_Nζ_l>| < ε/2.

The exact norm radius is valid for nonselfadjoint t as well: apply selfadjoint norm-ball Kaplansky in M_2(C_N) to [[0,t],[t*,0]], and use upper-right corners. Nonselfadjoint norm-ball WOT density follows without an ad hoc factor2 in the input norm. C_N⊂π(𝔄), since the image of a C*-homomorphism is norm closed. No raw universal-algebra lift with an attained norm is required.

Set d=F(x). Contractivity gives ||d||≤r and ||d−t||≤2r. By(1) its compressed error equals the error for x. Splitting each original vector at P_N bounds the remaining coefficient error by the displayed2r expression. Thus |<(d−t)η_l,ζ_l>|<ε for every l. The case r=0 uses x=0. Direct WOT neighborhoods give a bounded approximating net; no separability or sequential WOT-density assumption occurs. Since outputs lie in the WOT-closed T,

    closure_WOT F(π(𝔄)) = T,

with the claimed exact input norm bound. This is a written universal proof, not extrapolation from finite diagnostics.

**The recursive D.** Its definition includes F of every finite copyword by taking all inserted D-elements equal to1; arbitrary repeated indices are allowed. Their span is norm dense in π(𝔄); boundedness of F and norm closure of D give F(π(𝔄))⊂D⊂T. Therefore T⊂D''⊂T. No assertion that D equals the first-stage C*-algebra or lies in π(𝔄) follows from this argument.

## Deliberate falsification and independent controls

No substantive mathematical defect was found in the PR proof. The following potential failures were tested or excluded explicitly:

* Nonfaithful GNS quotient: the symmetry preserves its null space. The sparse Boolean fixture sends the universal word a_1a_2a_3 to0 although the universal word is nonzero under all-copy evaluation at the+1 character. Faithfulness was not smuggled in.
* Overlapping S and S+k and repeated indices: the complement-completion argument is a genuine finite permutation, even with overlaps; an occurrence-by-occurrence shift is rejected.
* Nonnormal F: the compact-plus-scalar Boolean model has F(λI+K)=λI+K_00e_00. Finite-rank q_m=sum_{j=0}^m e_jj converge strongly toI but F(q_m)=e_00≠F(I)=I. Thus a normal-limit shortcut is false. The proof uses (1) instead.
* Testing ξ alone would miss e_11; arbitrary vector pairs are essential. Likewise equality outside the future domain, global instead of compressed equality, or only first moments all fail.
* No fixed finite-dimensional normalized trace substitutes for the infinite scalar quotient character. The test suite explicitly rejects that substitution.
* Dense-vector convergence without a uniform bound is insufficient: n e_0n annihilates every finitely supported vector eventually, but for η_n=1/n (n≥1), η∈ℓ² and <n e_0nη,e_0>=1. Uniform boundedness in the proof prevents this failure.
* Normal states, nonfaithful states, arbitrary nonselfadjoint targets, A=C, scalar tails, repeated words, and zero target require no exceptional modification. The zero C*-algebra under conventions excluding a unital state is vacuous.

The fresh stdlib-only check_controls.py was authored independently and imports no PR or author programs. It verifies exact sparse compact-plus-scalar and finite-permutation mechanisms using rational real/imaginary coefficients. Normal,-O,-OO outputs are byte-identical:82376 explicit guards;3072 permutation cases,1708 overlaps,3048 repeated-word cases,4372 matrix-word cases,8 rejected false controls. Finite tests do not prove the universal claim, do not certify arbitrary C*-algebras, and do not replace the argument above. Normal/-O/-OO runs preserve explicit guards because no Python assert is used.

## Priority: what is prior, what was actually inspected, and a stronger bridge

The main source is Kenneth J. Dykema, Claus Köstler, John D. Williams, *Quantum symmetric states on free product C*-algebras*, Trans.AMS369(1)(2017),645–679; DOI https://doi.org/10.1090/tran6661 . Crossref authenticates title/authors, online2016 and issue2017. Its §5 is general, whereas Theorem7.3's tail generation is quantum symmetric. The full relevant current arXiv §5 source arguments and theorem statements were read. Lemma5.1.8, proof ofTheorem5.1.10 and Remark5.1.11 already contain coefficient stabilization and bounded-vector extension. They deserve material method credit; this review does not claim to have invented them. Proposition5.2.4 also yields normal-expectation cases, for which generation is immediate from normality and Kaplansky. No new result should be advertised for those cases.

Weihua Liu, *Extended de Finetti theorems for boolean independence and monotone independence*, arXiv1505.02215v1, §6.2, printed pp31–34, Lemmas6.5–6.9, Proposition6.10, Lemmas6.12–6.14 were read, including proofs. Journal metadata: Trans.AMS370(3)(2018),1959–2003, DOI https://doi.org/10.1090/tran/7034 . The inspected lemma numbers refer to arXivv1; the publisher accepted-manuscript PDF returned403. Liu's word “non-degenerated” means faithful GNS representation, not a faithful state. Therefore that adjective alone does NOT exclude the general DKW GNS state. His setup is bilateral bounded variables, nonunital polynomial generation with the unit in its WOT closure, and a spatial normal bilateral shift. Lemma6.8 supplies a past/future coefficient identity; Proposition6.10 establishes normality on each fixed future von Neumann algebra, not on the entire generated bilateral algebra (Remark6.11 expressly distinguishes these).

**Additional independent bridge relevant to novelty assessment.** Merely saying “bilateral, so unrelated” would understate this prior art. Suppose a symmetric unilateral process is extended to indices Z by its finite-index distributions, and use its bilateral GNS representation. Write M_+ for the von Neumann algebra generated by positive copies on that larger Hilbert space. Its positive cyclic subspace H_+ reduces M_+, and restriction ρ:M_+→M_original is a normal surjective *-homomorphism. For each future von Neumann algebra C_N^Z, ρ(C_N^Z)=C_N_original'': normal *-homomorphic images are von Neumann algebras and contain the same copy generators. For t in the original tail and r=||t||, the compact sets

    {s∈C_N^Z : ||s||≤r, ρ(s)=t}

are nonempty and nested. Norm-ball lifts exist by the central-kernel decomposition of a normal surjection. Ultraweak compactness then gives a tail lift s∈T_Z with ρ(s)=t. Thus ρ(T_Z)=T_original; one must prove this intersection step, not commute image with intersection without justification.

The needed positive-future expectation is also obtainable in the arbitrary-A block setting by the same prior argument, without assuming faithfulness. To make this comparison checkable: extend ψ to the free product indexed by Z by a bijection Z→N. Symmetry makes every finite prescribed index relabeling have the same law, so the positive restriction has the original law. The bilateral shift preserves the state (check on finite words) and is implemented by a unitary, hence extends normally to the bilateral represented von Neumann algebra. Fix a future cutoff k. For initial finite-copy test vectors whose copy indices are≤n, choose L so that k+L>n. For every l≥L, future word coefficients of α^l(a) equal those of α^L(a), by a finite permutation fixing these test indices. Normality of the bilateral shift and norm-ball Kaplansky extend this identity from future polynomials to every a in that fixed future von Neumann algebra. Uniform boundedness extends it to arbitrary test vectors, proving existence of the WOT shift limit E_+(a). It lies in every later future algebra. On each fixed future algebra it is normal: for a bounded convergent net of inputs, coefficients on the dense finite-word vectors equal those of one fixed normal map α^L; the uniform bound extends convergence to all vectors. In particular bounded increasing nets are preserved, the usual normality criterion for a positive map. For a in the bilateral tail, apply the identity in an arbitrarily later future algebra; α(a) and a have identical coefficients on every finite-word vector, so α(a)=a. The shift-limit map therefore fixes the tail. Being a unital completely positive contractive projection onto that tail, it is a conditional expectation. This reproduces the block/nets form of Liu's mechanism; it is an independent extension written here, not a source theorem quoted beyond its stated scope.

Now normal Kaplansky approximation on M_+ gives T_Z=closure_WOT E_+(π_Z(𝔄_+)), with norm bounds. On that C*-algebra, the shift-limit formula and normality of ρ give ρE_+(x)=F_originalρ(x). The preceding tail-surjectivity proves the desired original generation theorem, including nonseparable A. Crucially, E_+ need NOT descend through ρ on all M_+; only the C*-input compatibility is needed. In the bilateral Boolean example the negative-space central projection is killed by ρ, while its E_+ image can survive, illustrating why a blanket descent assertion would be false.

This is an independently supplied mathematical bridge, not a theorem located verbatim in Liu or an authenticated claim that he answered DKW5.3.5. His displayed variable formulation directly supports its prescribed variable setting. The block-index and net extension needed for arbitrary unital A is supplied above, as is the representation/tail-surjectivity bridge; these steps were not found stated as the original general generation theorem in an authenticated prior body. Accordingly the potential new contribution is at most this short general deduction and its precise representation bridge, not a new stabilization mechanism. The bridge warrants explicit discussion in any manuscript and novelty assessment. It does not justify inserting Liu's dependency DOI as if it published this full general answer. No unresolved mathematical obstruction to the submitted unilateral proof results from this comparison.

Further actual primary comparisons (read relevant body statements/proofs, not just snippets):

| Primary source | Relevant scope and result of comparison |
|---|---|
| Dykema–Köstler1202.4749v2, Prop3.1 and proof | Prior moment generation in faithful normal amalgamated-free construction; not arbitrary general symmetric-state DKW target. DOI10.1090/S0002-9939-2014-12116-2. |
| Dabrowski–Dykema–Mukherjee1401.4692v2, introduction/main setup | Tracial quantum-symmetric simplex result; not general symmetric-state generation. |
| Dykema–Mukherjee1609.01225, §4 printed pp7–8 | KMS quantum symmetric states; explicitly uses recursive D and existing canonical F, no general generation theorem. DOI10.1063/1.4974361 metadata lead. |
| Liu1511.05651v2, introduction/Theorem1.2 | Faithful/free and stronger quantum/Boolean distributional symmetry settings; no full arbitrary symmetric-state claim. |
| Liu2512.16170v1, introduction/Theorems2,3,6.3 | Faithful normal setting for its de Finetti assertions; commutative classical or quantum permutation frameworks, not all finite-permutation symmetric free-product states. |
| Crismale–Rossi2207.04323v1, Props3.4/Thm3.9 and proofs | Concrete monotone and q-deformed processes with explicitly computed tails; not arbitrary A. |
| Evans–Gohm–Köstler1508.03168v3, Thm4.5/proof | Semicosimplicial algebraic spreadability; concrete coface realization needs stated extra faithfulness. Does not state DKW recursive-tail generation. |
| Köstler–Krishnan–Wills2009.14811v4, initial probability setup and §2.3 context | Faithful normal W* framework/Markov and Thompson-monoid conclusions; no removal of general DKW expectation obstruction. DOI10.1016/j.jfa.2022.109818. |
| Evans–Gohm–Köstler2603.27373v1, Thm2.14/proof context | Saturated Hilbert-space semicosimplicial/partial-shift classification; its orthogonal layers are not DKW's recursive C*-algebra. |
| Aiello–DelVecchio–Rossi2509.02270, actual v2(30June2026), Thms3.7,4.9,4.10 and Cor4.11 | Current de Finetti results for distributions factoring through twisted tensor products with explicit bicharacter/abelianness compatibility; stronger structural assumptions, not arbitrary free-product symmetric states. DOI10.1016/j.aim.2026.111119 is a journal metadata lead, not a body equivalence certification. |
| Crismale–Fidaleo1310.1566, general process/ergodicity statements, §5 setup and Prop5.3 proof | The tempting normal-tail expectation inProp5.3 is under A=CAR(N), expressly fixed in§5, not the arbitrary free-product algebra of earlier sections. |
| Crismale–Fidaleo1609.09856v1, theorem inventory and tail sections | General correspondence and ergodicity plus concrete Bose/Fermi/Boolean/monotone models, no unrestricted recursive-tail result. |
| Primary India survey2019, DKW/KMS paragraph and bibliography | Reports quantum/tracial/KMS advances, no full general solution. Not an independent proof authority. |
| Dykema official CV | Dated21August2022, lists DKW, quantum-tail, tracial-simplex and KMS papers; not a current2026 exhaustive publication index. |

The source inventory separates actual read scopes from whole-paper audits; a primary PDF being stored does not mean every theorem in it was checked. No source body was used solely on a search snippet to establish full-target coverage.

## Search/accounting and source-access limits

SEARCH_INDEX.md records query families, primary leads, current versions, and limitations. Searches included exact questions, both IDs, general tail generation, ordinary/shifted moments, symmetric-state/conditional-expectation variants, DKW author records, Liu's later work, quantum/exchangeable process terminology, current2026 de Finetti work, and forward citation discovery. OpenAlex's DKW index reported5 citing works; all five were followed to relevant primary bodies (KMS, tracial simplex, semicosimplicial, Thompson Markovianity, India survey), but that index is not exhaustive. Author CV and current arXiv metadata were checked. Public Zenodo searches found no matching target package/record; the single “tail generation” hit was an unrelated thermodynamics record19699489. The existing PR itself is prior public proof material dated13October2026, so it must be credited and preserved rather than represented as a fresh proof created by this audit.

Access facts: both official AMS full-body routes returned403; Crossref metadata and inspected arXiv bodies were used with explicit version qualifications. Liu's2016 eScholarship dissertation landing/PDF route did not yield the thesis body (PDF202 with zero bytes); indexed excerpts are not a thesis body audit. An alleged standard lecture PDF returned200 with an Incapsula HTML challenge, not a PDF or evidence of theorem access. The author homepage returned a construction stub; the accessible CV is dated2022. These limitations do not invalidate the independent proof; they prevent claims of exhaustive priority or unseen journal/thesis inspection. Standard Kaplansky density is imported, with its needed nonselfadjoint reduction supplied above; no claim is made of re-proving all foundational operator algebra.

No full-target DOI or appropriate partially prepared Zenodo record was authenticated. The original-problem report DOIs and restricted-result/method dependency DOIs must not be entered as a publication of the general answer. Consequently NO_ROW_PROPOSAL.json explicitly declines a four-cell existing-publication row. Both IDs and original-question aliases must be treated as one family in any later duplicate check. If a new manuscript is prepared, it needs the user's required extensive AI disclosure and unrefereed-preprint statement, complete attribution, independent package reviews, live duplication rechecks and actual publication/accounting verification; none of those later gates is claimed completed here.

## Strongest verified result and exact remaining work

The full general mathematical claim is proved by the argument above and matches a separately posed original question. There is no mathematical repair request. The closest prior mechanisms and a bilateral-corollary route are identified precisely. No full general prior publication was established by this audit; no worldwide novelty or novelty of the method is asserted. Remaining parent work is to adopt the correctness review, assess whether the narrowly framed general deduction merits a new preprint after this primary comparison, complete the actual publication package and fresh adversarial loops, and perform any authorized merge/publication/tracker actions with new live checks. This packet is evidence for those decisions, not publication clearance or an external row.
