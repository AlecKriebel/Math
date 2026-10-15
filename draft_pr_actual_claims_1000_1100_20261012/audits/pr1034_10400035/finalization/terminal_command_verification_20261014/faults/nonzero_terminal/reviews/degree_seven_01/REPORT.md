# Adversarial degree-seven review of PR1034

## Verdict

**Assigned family CLEAN.** At pinned head `86d076dae3e3fa8b7cda7fd9c6a822c3d7392c14`, I found no actionable mathematical defect in the claimed existence of a rational ordinary invariant of exact order seven, vanishing on every ordered two-string link with actual abstract free exterior group F₂. The same invariant proves Nₙ(2)≠0 for every n≥7. The conclusion follows from a valid marked genus-two argument, an ordinary nonzero reversal-odd symbol, and rational integration.

This verdict covers the degree-seven family only. The order-two spanning claim and all-k low-degree kernel claim are assigned elsewhere and remain conditional on their reviews. Orders 3–6, higher k, classification, minimum degree, novelty, and priority are not established here. This is an independent AI mathematical/source review with new exact arithmetic, not human peer review or formal proof-assistant verification.

No P0/P1/P2 actionable finding was identified in this family. The manuscript already states the material limits: existential integration, no named nonsingular-link value, actual group freeness, unframed category, and no higher-strand extrapolation.

## Inputs and independence

The binding input is the complete 19-file authored snapshot listed in `../../SUBMITTED_PINS.json`, not a current live branch or historical supplemental computation packet. `INITIAL_PINS.json` and `FINAL_PINS.json` verify all 19 lengths and SHA256 digests at the specified head. I used no Git commands, index changes, candidate edits, queue edits, service actions, publication, or external communication. All work products are confined to this review folder. Copied third-party bytes, extracted bodies, and rendered source pages are only in `sources/raw/`.

I first read `PROOF_KERNEL_ORDER_SEVEN.md` and `MARKED_FREE_REVERSAL_LEMMA.md`; independently derived geometry, symbol, and integration obligations; retrieved fresh primary bodies; wrote `DERIVATION.md`; and checked new arithmetic. Only afterward did I read the existing `AUDIT_KERNEL_ORDER_SEVEN.md` and acceptance summary for comparison. I did not read priority files or any other new review family's results, and I spawned no agents. The prior acceptance label was not an input to the conclusion.

## Exact mathematical obligations

The category consists of smooth ordered upward-oriented unframed proper arcs, fixed endpoint pairs and standard endpoint collars, modulo ambient smooth isotopy fixing the complete ball boundary. On the real transverse diameter,

r(x,y,t)=(x,−y,1−t), (ργ)ᵢ(s)=r(γᵢ(1−s)).

The hypothesis is freeness of the actual exterior π₁. There is no meridian-basis assumption, nilpotent-quotient replacement, framing, or component deletion. The three obligations are separate:

1. Every such actual free two-strand exterior is fixed by this exact labeled ρ.
2. A rational reversal-odd degree-seven diagram remains nonzero in the ordinary 1T quotient.
3. A rational ordinary invariant integrates that symbol, and antisymmetrization retains it.

The submitted argument meets these obligations. It uses neither a finite list of free examples as universal proof nor a raw Lie functional as automatic evidence of 1T survival.

## Geometric attacks and outcomes

| Adversarial concern | Independent check | Outcome and remaining gap |
|---|---|---|
| Abstract free π₁ need not identify a preferred meridian basis | The compression proof needs only subgroup freeness, irreducibility, and the Loop Theorem. Disk cuts preserve free factors and irreducibility; complexity decreases to balls. | Pass. No basis assumption or central unsupported transfer. |
| Freeness could refer only to nilpotent quotients | The hypothesis explicitly concerns the actual compact exterior π₁; open complement and compact exterior retract to the same group. | Pass. Nilpotent data alone would not suffice and is not used. |
| A free tangle may be knotted and need not be a braid | The argument constructs a handlebody exterior, not a trivialization of the arcs. The boundary identification φ is not assumed extendible. | Pass. No braid or rational-tangle assumption. |
| An unmarked hyperelliptic extension could hide a four-punctured-sphere factor | τ is prescribed before extension, is literally r on the common outer four-holed sphere, and equals the tube conjugation on each annulus. Centrality gives an extension class; a displayed collar correction gives exactly τ. | Pass. No final mapping-class ambiguity. |
| Tube coordinates might fail to realize both prescribed end frames | The oriented normal bundle over an interval is trivial and the end frames lie in the same connected oriented frame space. Different integer twists alter both τ and tube fill by the same conjugation. | Pass. No independent framing to preserve. |
| Correct boundary values might still fail smooth gluing through normal derivatives | Compatible local involutions yield an invariant collar. For F|∂H=τ, image collar d(x,u)=F(c(τ⁻¹x,u)); relative collar uniqueness provides Kd=c. Then KF equals the desired local germ. `artifacts/EXACT_COLLAR_ARGUMENT.md` records the formulas. | Pass. The germ correction is a real needed step and is present. |
| A genus-two result might incorrectly require hyperbolicity | The relevant Bruno–Mecchia paragraph states surface centrality and handlebody extension before applying them to the later manifolds. | Pass. No hyperbolicity imported. |
| A strong inversion might permute labels or reverse only an unspecified parameterization | Explicit fill Jᵢ fixes each tube label and sends γᵢ(s) to γᵢ(1−s). Composition g=rh is identity on the whole boundary and sends γᵢ to (ργ)ᵢ with the same parameter. | Pass. Exact ordered orientation agreement. |
| A boundary-fixed ball diffeomorphism might not be smoothly isotopic to id | Hatcher's Appendix (1) supplies the relative smooth-ball statement. Parametric collar straightening preserves a smaller collar for the long extension. | Pass. No smooth Alexander-trick shortcut. |
| PL proof techniques could silently weaken the smooth conclusion | Hatcher's Basic 3-Manifold text works in the C∞ category, including tubular neighborhoods and isotopy extension. The Loop Theorem's PL proof method does not change its declared smooth theorem interface. Corners are rounded compatibly with local maps. | Pass. No wild embedding or nonsmooth category substituted. |
| The extension h might fail h²=id | Only h's boundary and core identities are used; the collar correction need not be equivariant globally. | Pass. Global involutivity is unnecessary. |

The crucial exact identities are

h|∂C=r, h(γᵢ(s))=γᵢ(1−s), g=rh, g|∂C=id, g(γᵢ(s))=(ργ)ᵢ(s).

Together with the relative-ball theorem, these give ρL=L for every free exterior in the required category. No plausible counterexample survived these identities. Higher genus lacks the centrality used here, so the method is correctly bounded to two strands.

## Diagram, reversal, and integration attacks

The fresh v5 body and figures fix numbered long ends at (i,0,t). Reversing both component parameters and applying R(x,y,z)=(x,−y,−z) restores those ends without label exchange. R has determinant +1 and becomes r after centering/rescaling. Its projected diagram reflection includes depth reflection, so it is not an ambient mirror. Simultaneous orientation reversal on both crossing branches preserves the positive/negative crossing resolution convention. Therefore the ordinary filtration and symbol action have the required convention.

Visual inspection of Proposition 2 shows the seven-wheel with cyclic colors 1121222, seven legs and seven trivalent vertices. Its degree is seven. The source odd-leg involution negates its symmetrization. A change of global vertex-orientation convention could negate the entire certificate, but cannot erase nonzero or oddness.

The independently authored program derives the wheel polynomial from all 128 left/right choices in adX=LX−RX, cyclically groups them, and separately forms the commutator operators on the matrix-unit basis. Both methods agree with the integer witness. This verifies nonzero over Q at N=4 without relying on eventual algebraic independence of large-N necklace variables. The result is a diagram weight value, not an actual nonsingular link value.

Ordinary survival is a separate source-backed step. Connectedness is combined with the deframing algebra: the monochromatic self-struts are central degree-one primitive generators, and the nonstrut connected primitive lies in the complementary ordinary subalgebra identified by Lemma 8. The actual v5 page 9 explicitly applies that statement to the heptapus. The earlier framed proofs alone, or v1 without the explicit deframing section, would not have been sufficient evidence. The controlling body inspected here is v5.

For the surviving ordinary class d, choose a rational functional W with W(d)=1 and form W⁻=(W−W◦τ_A)/2. Since τ_A(d)=−d, W⁻(d)=1 and W⁻◦τ_A=−W⁻. Rational symbol surjectivity gives ordinary f with top symbol W⁻. Then v=(f−f◦ρ)/2 has symbol W⁻, not zero, and exact order seven. Its nonzero symbol forces a nonzero nonsingular value somewhere by the definition of singular resolution. For a free L, the independently proved ρL=L gives v(L)=0. Thus v∈N₇(2) and v∈Nₙ(2) for every n≥7. The nonconstructive choice of functional/integration is sufficient for this existence claim.

## Fresh primary evidence and source boundaries

All four controlling PDFs were freshly retrieved via their versioned/journal/author URLs with HTTP 200. The bodies match the manuscript's claimed byte counts and digests; `SOURCE_FETCH.json` records per-source timestamps, URLs, sizes, and SHA256. This review inspected full relevant pages, rather than relying on extracted figure labels alone.

| Primary interface | Retrieved body and visual locations | Relevance |
|---|---|---|
| [Duzhin–Karev v5, 25 July 2005](https://arxiv.org/pdf/math/0507015v5) | 195094 bytes, SHA256 `f92b93fe6cfe04f1720c8ee080f19af2103ced2ab4fcc616c7c95ed3df6dfae3`; PDF/printed pages 1–3, 5–6, 8–9 visually inspected | Labeled reversal, Q-valued ordinary symbol interface, seven-wheel/odd legs, and actual Section 6/Lemma 8 deframing. |
| [Bruno–Mecchia, 2014](https://rendiconti.dmi.units.it/volumi/46/014.pdf) | 780746 bytes, SHA256 `b4c1c4a76c3028a54ba1223536ec7b1c1820474e6584d622161bfba743c12f0c`; PDF page 2, printed p.272 visually inspected | Closed genus-two hyperelliptic centrality and handlebody extension. |
| [Hatcher, Basic 3-Manifold Topology](https://pi.math.cornell.edu/~hatcher/3M/3Mfds.pdf) | 702282 bytes, SHA256 `c8add1a8633f36cb50de313f8f340a3f2b63b5548077d6e30f9c51a073398ff6`; PDF pages 2 and 57, printed pp.1 and 56 visually inspected | Smooth sphere theorem, Loop Theorem, and C∞ conventions. |
| [Hatcher, Smale Conjecture, 1983](https://pi.math.cornell.edu/~hatcher/Papers/SmaleConjecture.pdf) | 14720341 bytes, SHA256 `d85554b61d9315081c51e8cf0438d5674c41507e2ac634dd465e029753333344`; PDF page 52, printed p.604 visually inspected | Smooth relative-ball diffeomorphism theorem, Appendix (1). |

The two Hatcher bodies could not be opened by the web text interface during this review, but direct fresh author-hosted downloads succeeded and source images were inspected. Their access is therefore not a dependency gap. Haas–Susskind was not retrieved and is not a premise: the controlling Bruno–Mecchia input and explicit marked construction suffice. Nogueira is also unnecessary for the independent compression proof. No primary authors or other individuals were contacted.

## Checkable computational artifacts

Run from this folder:

```
python3 artifacts/independent_wheel_check.py
python3 -O artifacts/independent_wheel_check.py
```

`artifacts/WHEEL_RESULT.json` records both runs with identical output. The checks use exceptions, so optimized mode does not remove them. The trace values are −2, 38, 20, −12, −23 in the order specified in the proof. Grouping, explicit 128-term evaluation, and direct 16×16 adjoint multiplication all give 6. Word reversal gives −6, antisymmetric difference is 12, and cyclic rotations preserve 6. A coefficient-3-to-2 mutation produces −18 and is detected. All arithmetic is exact integer arithmetic with no floating-point tolerance, package dependency, or old supplemental script import.

This is a fresh certificate for this review. The theoretical edition's historical descriptions of unavailable old scripts are not treated as reruns, and the new script does not purport to reconstruct every historical guard or artifact. Geometry, deframing, and integration remain separately verified mathematical obligations.

## Comparison to prior written audit and acceptance

After saving the independent derivation and result, I read the old degree-seven audit. Its bounded mathematical conclusion and category agree with the independent result. Historical hashes and omitted computational packet accounts there bind older artifacts, and I have not pretended to replay them. The present conclusion binds the 19 current snapshot pins and its new artifacts. The acceptance summary's degree-seven statement and residual-scope language match this review. Its separate order-two conclusions were not adjudicated by this family.

No repair is necessary for the degree-seven theorem as submitted. The exact boundary-map/collar correction, ordinary v5 deframing, and rational symbol integration must remain in any shorter presentation because each resolves a genuine logical obligation. Removing them would reopen the relevant gaps.

## Completion and retained gap

Review completion: **100% of the assigned bounded verification target**. Strongest independently supported result: a nonzero rational ordinary exact-order-seven invariant in N₇(2), hence all Nₙ(2) for n≥7 are nonzero. Exact remaining mathematical scope: orders 3–6, higher k, minimum order, and classification are unresolved by this mechanism. The other families' order-two results remain conditional here. All 19 pinned originals are unchanged, and all authored work and copied source evidence are confined to the allowed review directory.
