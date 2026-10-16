# Current priority audit: unmarked metric cubic compactification

Checkpoint: 2026-10-06 22:45 PDT. Assigned source/scope audit: 99%; certainty of a first-disclosure claim: 0%; mathematical completion of the proposed additional boundary theorem: assigned separately and not certified here. No external individual was contacted. No Git, deposit, tracker, or reviewed-source mutation was performed.

## Scope and verdict

The candidate additional statement is the homeomorphism

\[
\overline{\mathcal M^{\rm KE,metric}_{\rm smooth\ cubic\ n}}^{\rm GH}
\simeq
\bigl(\mathbf P(\operatorname{Sym}^3\mathbf C^{n+2})\mathbin{/\!/}\operatorname{SL}(n+2)\bigr)(\mathbf C)/\langle\sigma\rangle,
\qquad n\geq5,
\]

where the left side remembers only the unmarked compact real metric space, KE metrics have a fixed Ricci normalization, and sigma is coefficientwise complex conjugation. The potential substantive addition is a rigorous **singular-boundary metric rigidity theorem**, not the notation for the conjugation quotient. A proof must show that every isometry between boundary KE cubic spaces is globally holomorphic or antiholomorphic, and that the cubic polarization is preserved.

Current primary sources establish the old conjugation convention, smooth irreducible Fano rigidity, singular KE splitting, and the now-public arbitrary-dimensional complex K/GIT comparison. I did **not** find the exact proposed high-Cartier-index rigidity theorem or the exact n>=5 cubic unmarked-metric boundary quotient explicitly stated in the primary texts inspected below. This is an affirmative scope comparison of particular texts, not proof of global novelty. It does not justify a first-solution claim. Conversely, it would overstate the evidence to say that OSS already proves the exact arbitrary-dimensional singular cubic assertion, or that the competing theorem uses the same proof as our gap-based deduction.

The boundary-rigidity route remains a justified candidate for complete mathematical investigation and fresh review. This audit does not clear publication of an unproved claim and does not independently establish a first public disclosure. Its permissible framing, if verified, would be an explicit metric-boundary deduction/extension of existing K-moduli and decomposition theorems, with the cubic complex comparison expressly credited as prior work.

**Concrete recommendation under the original gate, conditional on the full proof passing independent review: proceed with a modest extension note.** A sharp singular rigidity criterion together with all-boundary metric-fiber identification supplies a checkable additional theorem and an argument absent from the exact source results below. This is not merely a new notation for the old convention. Its mechanism is a short numerical deduction from a deep existing decomposition theorem, followed by established positive-Ricci tensor geometry. Modesty of the deduction does not make it the identical theorem/proof already supplied by those sources. The note must lead with this actual addition; the inherited all-dimensional complex comparison must be presented as a consequence/known theorem rather than advertised as a first solution. This recommendation is an originality/scope judgment from actual comparison of relevant statements and proof mechanisms, not a guarantee that no unnoticed equivalent corollary exists anywhere. It does not waive mathematical or full-package review gates.

## Primary texts inspected and exact overlap

### Odaka–Spotti–Sun, arXiv:1210.0858v3

[Primary manuscript](https://arxiv.org/html/1210.0858v3), introduction following Theorem 1.1 and Section 2 following Remark 2.8; cached PDF and text were read. The authors explicitly distinguish complex-preserving GH convergence from ordinary metric GH convergence. For their del Pezzo surface moduli, ordinary metric compactification is the quotient by conjugation. Their Section 4.2 identifies conjugation on cubic-surface GIT with its natural antiholomorphic involution. Section 2 refers to Spotti's thesis for the assertion that isometric KE log del Pezzo surfaces have equal or conjugate complex structures.

This is a rigorous precedent for singular **surface** boundaries and the exact quotient construction. It supplies no statement for all higher-dimensional singular cubics. The source's arXiv version history, not an experimental HTML renderer date, is the public-version evidence.

### Spotti, thesis, arXiv:1211.5334

[Primary PDF](https://arxiv.org/pdf/1211.5334), printed pp.14–16, Theorem 1.1.1 and Corollary 1.1.1: for a smooth KE Fano manifold, two compatible KE complex structures that differ by more than sign force a holomorphic/isometric product decomposition. The proof first removes the (2,0) part of the second Kähler form, then uses a parallel self-adjoint endomorphism and de Rham splitting. The remark says the author expected expert familiarity but supplied a proof because an exact statement was not located. Later printed pp.82–83 gives the degree-four metric quotient explicitly.

This is the correct smooth precursor. Its completeness and smoothness assumptions do not silently extend to singular regular loci.

### Druel–Guenancia–Păun, published 2024 version

[Published primary article, DOI 10.5802/crmath.612](https://comptes-rendus.academie-sciences.fr/mathematique/articles/10.5802/crmath.612/), printed pp.94–96, Theorems A/C; printed p.101, Theorem 6; final Section 5 were inspected. Theorem A supplies a finite quasi-étale cover of a weak KE klt Q-Fano and an isometric product of KE Q-Fano factors with stable tangent sheaves. Theorem 6 gives parallel stable summands downstairs. Theorem C supplies the underlying algebraic product-cover theorem for integrable tangent summands. The article explicitly warns that the KE metric on the regular locus is generally incomplete, precluding a direct use of smooth de Rham theory.

No high-Cartier-index criterion, cubic moduli application, or uniqueness-up-to-sign of a second parallel complex structure is explicitly asserted there. The published version is preferable to quoting the 2020 arXiv version's theorem numbering. Journal online date is June 6, 2024; arXiv v1 was public August 12, 2020.

### Höring, 2026: additional current source

[arXiv:2602.15427v1](https://arxiv.org/pdf/2602.15427v1), Theorem 1.1 and Corollary 1.2, plus the author's [revised primary PDF](https://math.univ-cotedazur.fr/u/hoering/articles/a57-fano-split-tangent.pdf), were inspected. Corollary 1.2 supplies an algebraic product on a finite quasi-étale cover whenever a normal projective variety of Fano type has split tangent sheaf. This removes the KE assumption from that splitting step; it does not assert metric rigidity or the index criterion. Its citation chain invokes DGP Theorem C. Corollary 2.16 in arXiv v1 (2.15 in the revised copy) also rules out tangent splitting at Picard number one when the summand determinants are Q-Cartier.

The [authoritative arXiv history](https://arxiv.org/abs/2602.15427) gives initial public submission February 17, 2026. The author-hosted PDF currently says September 18, 2026; that manuscript date does not establish its posting date. The relevant Corollary 1.2 was verified in both versions. This additional current primary input further narrows any claim of a newly invented splitting mechanism.

### Prior tangent-stability results: exact smooth scope

[Peternell–Wiśniewski, arXiv:alg-geom/9306010v2](https://arxiv.org/pdf/alg-geom/9306010v2), introduction Theorems 2/3, Corollary 1.5, and Section 2 Lemma 2.1/Theorem 2.3 were inspected in the primary PDF. Corollary 1.5 proves tangent/cotangent stability for **smooth** projective complete intersections of dimension at least three. Theorem 2.3 proves stable tangent bundle for smooth del Pezzo manifolds of index n-1 and b2=1. Its proof uses smooth divisor slicing and smooth vanishing; no singular weak-KE index criterion or boundary isometry classification is asserted. Thus smooth cubic tangent stability is old, independently of KE existence, and must not be claimed as an innovation of the proposed note. The source is arXiv v2, November 14, 1993, later J. Algebraic Geom. 4 (1995), 363–384.

[Dailly, arXiv:2601.19608v1](https://arxiv.org/pdf/2601.19608v1), introduction Theorem A/Corollary B and statement scope were inspected. Its main theorem extends tangent and canonical-extension **polystability** to adapted sheaves for singular KE log Fano pairs; its corollary is Miyaoka–Yau equality uniformization. It explicitly credits DGP for the no-boundary singular Q-Fano theorem. No high-index stable-factor exclusion or conjugation quotient is asserted. The authoritative arXiv public submission is January 27, 2026.

These texts rule out claiming a new general tangent-polystability theorem, a new smooth cubic stability result, or a new singular splitting principle. They do not discharge the candidate's numerical exclusion and all-boundary metric-fiber proof.

### Contemporary conflicting wording requiring care

[Chen–Lai, arXiv:2601.18526v1](https://arxiv.org/pdf/2601.18526v1), introduction Corollaries 1.9–1.11, claims a weak KE canonical del Pezzo surface with slope-unstable tangent and an alleged failure of polystability. This literally conflicts with DGP Theorem A. However, the same text calls `P^1 x P^1` unstable, while Corollary 1.9 says all its canonical weak del Pezzo tangents are semistable. Its use of “unstable” therefore cannot be identified uncritically with failure of semistability.

A directly checkable example cautions against the asserted polystability inference: DGP itself mentions `X=(P^1 x P^1)/<iota x iota>`, `iota([u:v])=[u:-v]`, a KE surface with four A1 points. The two factor tangent line bundles are invariant, descend reflexively, and have equal anticanonical slope downstairs. They are rank-one stable reflexive sheaves and their direct sum is polystable. Non-strict-stability cannot establish the advertised failure of polystability. The authors' broad classification is not independently audited here; no correction or contact was initiated. This source supplies neither the high-index criterion nor its metric application and is not used as a pivotal dependency. Its contradictory claim was forwarded for adversarial checking rather than silently treated as refuting the established DGP theorem.

### Kong–Shen–Zhao–Zhao

The local public manuscript was read at Theorem 1.1, proof sketch, final proof, and bibliography: SHA256 `6813e3d3be36c087e60b696f40652f8a837da7fcd9e3bdbd7af7df030c3ad65e`, 403,695 bytes. The current [author research page](https://sites.google.com/uic.edu/jzhao/research) still links [that manuscript](https://drive.google.com/file/d/1eB16wLGE2G5QrbV-pUDmw_ieLMiLlOcO/view?usp=sharing). Theorem 1.1 gives all-dimensional complex K/GIT equivalence, including stacks and good moduli spaces. Its proof uses local inequalities, the limiting linear system, tangent-sheaf slope semistability, and minimal-degree classification. DGP is cited for the semistability input.

The inspected text does not state the ordinary unmarked metric quotient by conjugation or a boundary isometry rigidity theorem. It proves a stronger **algebraic** comparison than our original complex-point target, but that does not itself imply the new isometry-fiber assertion without additional geometry. Its manuscript date is September 30, 2026. Earliest actual public posting remains unknown; presently public access is verified.

### Spotti–Sun, 2017

[Primary manuscript](https://arxiv.org/abs/1705.00377), Theorem 1.3(2), Remark 5.6(1), and Section 5.2 were reread in the cached exact version. The authors already state that the metric ODP gap in every required dimension implies the cubic KE/K-GIT identification. Their Remark 5.6 discusses the algebraic formulation/route; Section 5.2 already uses the surviving Cartier hyperplane root, Fujita classification, CM stability comparison, and moduli continuity.

Consequently, our all-dimensional upstream-gap-to-complex-cubic composition introduces no separate new cubic reduction. KSZZ uses a different proof: their overlap in conclusion cannot honestly be described as identical-proof duplication. Nevertheless, our original proposed cubic proof is an instance of the established Spotti–Sun transfer. The genuinely new unrestricted gap proof belongs to the upstream manuscript, and global Reeb minimization belongs to Li–Liu. An immediate newly available consequence must be attributed as such.

## Candidate mechanism and provenance

Here is the specific additional argument to be audited, rather than a novelty assertion based on a failed search. Suppose X is n-dimensional weak KE klt Fano with exact linear equivalence `-K_X = rL`, L ample Cartier, and `2(r-1)>n`. DGP supplies `Y=product Y_i -> X`. Pullback retains the ample Cartier root. Restricting to one factor at a regular complementary point gives `-K_{Y_i}=rL_i`. Kawamata–Viehweg vanishing and negativity imply that the degree-d_i Hilbert polynomial of L_i has roots `-1,...,-(r-1)`, hence `d_i>=r-1`. Two positive-dimensional factors contradict the strict bound. DGP's parallel-polystable decomposition then has one factor and yields tangent stability. For cubics `r=n-1`, the bound holds precisely for n>=5.

This numerical exclusion is short, depends essentially on **Cartier** rather than Q-Cartier divisibility, and appears to be an explicit additional deduction absent from the above exact statements. A competing route could apply Höring Corollary 1.2 to an existing tangent splitting. It would be incorrect to claim either product-cover construction is new.

Possible proof simplification, forwarded for independent mathematical checking: the (2,0) part of `g(J'·,·)` is parallel on the regular locus. Positive KE Ricci curvature should annihilate every such parallel holomorphic p-form by the pointwise curvature contraction identity: the contraction acts as `p*lambda` and a parallel tensor has zero curvature action. Thus J and J' commute without invoking global rational connectedness, reflexive-form vanishing, compactness, or completeness. J' then extends as a holomorphic endomorphism of the reflexive tangent sheaf; stability gives a scalar and `J'^2=-1` gives ±J. This local identity is established geometry and must receive a checked derivation before use; this note is not its mathematical certification.

The index inequality is sharp as a general numerical sufficient criterion: on `P^m x P^m`, `n=2m`, `r=m+1`, the product KE metric admits `J1 x J2` and `J1 x (-J2)`, differing by more than sign. Equality in `2(r-1)=n` therefore cannot be included in a universal statement. This example concerns general Fanos; it is not asserted to be a cubic.

## Exact remaining publication/priority gap

1. Complete the boundary theorem, including tensor extension, factorwise Cartier index, algebraic/metric regularity, extension of a regular-locus (anti)holomorphic isometry to the normal compactifications, and the cubic root's uniqueness. These are the actual new proof obligations; the old conjugation convention does not discharge them.
2. Give the verified additional theorem a fresh independent adversarial review. Existing reviews of the original audit source/PDF do not cover it.
3. Frame originality at the level justified by the completed argument: an explicit high-index singular rigidity criterion and resulting unmarked-metric boundary comparison, if established. Do not claim a first all-dimensional cubic K/GIT solution, newly invented splitting, or invented conjugation convention. Do not turn lack of an exact searched statement into proof of being first.
4. The entire-result-and-proof condition in original request Section 3 must be applied accurately. It is not a blanket ban on a rigorously established additional theorem derived from old ingredients, nor is it permission to relabel old results. Current inspected exact statements do not establish duplication of the candidate boundary rigidity proof; priority uncertainty still requires transparent limits rather than fabricated provenance.

I recommend keeping this route open for the dedicated mathematical audits already underway. If those fail or merely assume the fiber-rigidity assertion, it provides no eligible replacement. If they succeed, an accurately attributed modest extension can be assessed on its actual statement and proof. Publication eligibility is not certified by this source audit alone.

## Retrieval record and search limits

New cached primary artifacts, not publication payloads:

- `references/dgp_2024_crmath612.pdf`: 541,497 bytes, SHA256 `56421a3a50673066ee2be70db6a19eb38609458612b5cc6ff27492a1b501ed0f`; fetched October 7, 2026 05:40:40 UTC.
- `references/hoering_2026_split_tangent.pdf`: 450,559 bytes, SHA256 `7f2ccabeff45c7f95ecf4a1a4b1425229b5607dc470bb18a9b91055df8ac2ed3`; fetched October 7, 2026 05:40:41 UTC.
- `references/peternell_wisniewski_1993v2.pdf`: 167,290 bytes, SHA256 `f6a4ac6e4f73bd5d8c8e92e411d84cbe37441b4987ec5052c4aea73df5933bbf`; fetched October 7, 2026 05:45:30 UTC.
- `references/dailly_2026_2601.19608v1.pdf`: 754,618 bytes, SHA256 `05d55bb246b87d18c9b06fa2e9e22ab36dbb463b10528f0a2d9f5f7f2bd03ac1`; fetched October 7, 2026 05:45:30 UTC.
- `references/chen_lai_2026_2601.18526v1.pdf`: 536,051 bytes, SHA256 `59ced92c1d2f61b1ef97f99ba278cc2cda0fe1515501f2700e4c0789a95d2bca`; fetched October 7, 2026 05:45:30 UTC.
- Their local text extractions and `references/metric_priority_retrieval_receipt.json` preserve reproducible source/version evidence. The revised author-hosted Höring source was checked against the arXiv v1 statement through the primary web PDF.

Current searches on October 6, 2026 PDT covered combinations of `Kähler-Einstein`, `isometric`, `antiholomorphic`, `complex conjugation`, `parallel complex structures`, `Q-Fano`, `high index`, `Cartier`, `stable tangent sheaf`, `Gromov-Hausdorff`, `cubic`, and `modulo conjugation`; exact title/citation queries covered DGP and Höring. Follow-up primary-source reading covered Peternell–Wiśniewski, Dailly, and Chen–Lai. Search snippets were used only to locate primary texts. I did not rely on ResearchGate, AI paper summaries, aggregator abstracts, or guessed publication dates as mathematical evidence. No outreach was prepared or initiated.
