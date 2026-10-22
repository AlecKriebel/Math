# Reverse cross-challenge: Gabe–Szabó uniqueness and the full graph target

This report follows, and does not modify, the separately sealed structural_reductions and structural_followup_general_lemmas audits. It challenges the direct-lineage claim after verifying its initial output manifest hash. It is an explicitly cross-informed review, not an independent rediscovery.

## Verdict

**The outer arbitrary-period consequence in KNOWN_CONSEQUENCE.md passes. No missing theorem hypothesis, wrong equivalence direction, hidden group-law requirement, or failure of exact fixed-algebra recovery was found.**

Moreover, combining that consequence with the already checked vertex inner-kernel normalization and honest finite-abelian cocycle invariance gives the **entire stated graph/CK target**. This closes a mathematical implication gap left open by the direct-lineage report's deliberately outer-only note. It does not establish that an older paper explicitly printed the full combined CK statement.

Accordingly:

- Positive prior consequence: the outer periodic extension follows from a general theorem publicly available in 2022, by a short equivariant phase homotopy and averaging argument.
- Positive composed consequence: the full nonouter result follows after the explicit normalized vertex split and honest cocycle transfer; the old Matsumoto mechanism already supplies the cycle/coboundary input.
- Historical statement priority: an explicit older statement of the combined graph theorem remains unlocated in the inspected bodies. “Not explicitly located” is not a novelty certificate.
- Attribution: do not write that Gabe–Szabó printed or proved the exact full nonouter CK theorem. The correct wording is a consequence of their equivariant uniqueness theorem together with the displayed elementary structural reductions.
- Mechanism novelty: the submitted return-corner route is distinct from this uniqueness route, but its corner construction and diagonal-coboundary mechanism have older specific predecessors. No claim of a new first proof mechanism is cleared.

## 1. Primary bodies and exact version locators

James Gabe and Gábor Szabó, *The dynamical Kirchberg–Phillips theorem*:

| Inspected body | Public date/version | Exact relevant locators |
|---|---|---|
| [arXiv v1](https://arxiv.org/pdf/2205.04933v1) | 10 May 2022, 14:43:38 UTC in official history | Definition 1.2 p.9; Definition 1.15 p.13; Definition 1.22 pp.15–16; Proposition 3.14 p.29; Theorem 5.8 pp.45–46 |
| [arXiv v3](https://arxiv.org/pdf/2205.04933v3) | 16 August 2023 | Definition 1.15 p.13; Proposition 3.15 p.29; Theorem 5.8 p.46 |

Both PDFs were freshly acquired and text-inspected. The v1 pages 13, 29 and 45 were rendered and visually inspected. The theorem statement in v3 confirms the same applicable hypotheses. V1's proof contains a stabilization notation defect corrected in v3; the theorem statement and the relevant conclusion are unchanged. The audit uses the v3 confirmation rather than treating every line of an early proof as frozen final typesetting.

Publication metadata records Acta Math. 232 (2024), 1–77, DOI [10.4310/ACTA.2024.v232.n1.a1](https://doi.org/10.4310/ACTA.2024.v232.n1.a1). A direct publisher PDF download and a subsequent web open both returned HTTP 403. A search provider displayed the publisher's printed p.59 theorem passage, but this is not a downloaded or fully inspected final body. All decisive theorem locators here are bound to the actual arXiv bodies.

## 2. The theorem really is strong enough

Theorem 5.8 assumes: G exact; source A separable, unital and exact with a continuous G-action; target B a unital Kirchberg algebra; target action beta amenable and isometrically shift-absorbing; and two unital cocycle embeddings. It concludes equality of the associated KK^G classes if and only if the cocycle embeddings are asymptotically unitarily equivalent.

There is no UCT assumption, no graph primitivity assumption, no separate strong-stability hypothesis in this unital theorem, and no requirement that the cocycles be anchored or homotopic to the trivial cocycle. Those extra conditions occur in related stable results; importing them into Theorem 5.8 would misread the actual statement.

Definition 1.15 explicitly controls both the map limit and the cocycle defect. For two trivial cocycles, with target action alpha, the latter is

    max_(h in K) ||1-u_t alpha_h(u_t)*|| -> 0.

Since the norm equals ||alpha_h(u_t)-u_t||, this is exactly uniform approximate invariance. For finite G, take the compact set K=G. In a unital target the multiplier unitaries are actual unitaries in A. The theorem does not promise the path starts at 1; the requested strong approximate innerness only needs sequences, so this distinction causes no gap.

Proposition 3.14 in v1 (3.15 in v3) applies to any countable discrete group action on a Kirchberg algebra and equates isometric shift absorption with pointwise outerness. This is the precise reason the application needs an outer action. Faithfulness alone would not suffice.

## 3. Complete hypothesis map for the outer graph action

Let A=C*(E) for finite strongly connected noncycle E, and let alpha be an outer finite-abelian edge-diagonal action.

| Theorem requirement | Verification |
|---|---|
| G second-countable locally compact and exact | G finite discrete; its reduced group algebra is finite dimensional and hence exact |
| Source separable unital exact A | Finite graph algebra is separable and unital; nuclearity gives exactness |
| Target unital Kirchberg B | Take B=A; graph simplicity and pure infiniteness, together with nuclearity/separability, give a Kirchberg algebra |
| Amenable target action | Directly from Definition 1.22: for counting Haar measure use the constant function zeta(h)=|G|^(-1/2)1_A; all approximation equalities are exact |
| Isometric shift absorption | Outer alpha and Proposition 3.14/3.15 |
| Two unital cocycle embeddings | (id_A,1) and (alpha_g,1), for fixed g; both maps are automorphisms |
| Exact equivariance of endpoint alpha_g | G abelian, so alpha_g commutes with every alpha_h |
| Equality of KK^G classes | The equivariant phase homotopy below |
| Correct map direction | Choose phi=id and psi=alpha_g, so Ad(u_t) tends to alpha_g |

For fixed g choose a real theta_e with exp(i theta_e)=chi_e(g) for each edge, and let

    delta_t(p_v)=p_v,
    delta_t(S_e)=exp(i t theta_e)S_e,     0<=t<=1.

The graph CK relations give an automorphism for every t, with inverse obtained by negating the phases. Point-norm continuity follows first on finite generator polynomials and then on A by uniform contractivity. Edge phases commute with all alpha_h, so every delta_t is equivariant. Endpoints are id and alpha_g. Consequently a -> [t -> delta_t(a)] is a unital equivariant homomorphism into C([0,1],A), and ordinary homotopy invariance of KK^G identifies the endpoint classes. No relation between the theta choices for different g is required.

Theorem 5.8 therefore supplies u_t in U(A) with Ad(u_t)->alpha_g and max_h ||alpha_h(u_t)-u_t||->0. Let

    b_t=|G|^(-1) sum_h alpha_h(u_t).

Then b_t is exactly in A^alpha and ||b_t-u_t||->0. It is eventually invertible, and its polar unitary lies in A^alpha and has the same limit. Sampling times tending to infinity proves the desired per-g sequence property.

**Conclusion:** the outer action is strongly approximately inner for every graph period. This application does not construct a return graph and does not use an approximate-representation upgrade.

## 4. Full nonouter target after the explicit split

Let K={g:alpha_g is inner}. The diagonal-inner/cycle criterion was authenticated in the initial structural audit using Matsumoto 2000 Lemma 5.14 and Proposition 6.4 plus a finite directed-path comparison. It covers strongly connected noncycle graphs with arbitrary period through the edge CK presentation.

Choose directed paths theta_v from a fixed b to every v, with theta_b empty. Define on all G

    D_g=sum_v chi_(theta_v)(g)^(-1) p_v.

The coefficients are characters, so D_g D_h=D_(gh). Every D_g is fixed by alpha. For k in K the normalized vertex-coboundary criterion gives alpha_k=Ad(D_k). Consequently beta_g=Ad(D_g*)alpha_g is an edge-diagonal action trivial on K. It factors through H=G/K.

The H-action is outer: inner beta_g would make alpha_g inner, so g belongs to K. H is finite abelian. For H nontrivial, §3 applies to this quotient action for the same graph, with no period condition. For H trivial beta is the identity and is strongly approximately inner immediately. Pullback from H to G has the same fixed algebra.

Finally alpha is the honest beta-cocycle perturbation by D_g. Beta fixes the vertex algebra, hence beta_g(D_h)=D_h, so

    D_g beta_g(D_h)=D_g D_h=D_(gh).

The finite-abelian cocycle-invariance lemma independently checked and sealed in structural_followup_general_lemmas gives strong approximate innerness of alpha with unitaries in the original A^alpha. Alternatively the submitted block pinch/polar calculation proves the same restoration in this special vertex situation.

This is an explicit closed deduction for the full graph target. The standard graph/CK generator correspondence returns it to the exact finite essential 0–1 CK question. No additional assumption of action faithfulness, graph aperiodicity, approximate group coherence, fixed-point simplicity, or fullness in A^alpha remains.

**Important historical qualification:** this composed argument is written in this audit. Its ingredients include the 2022 general theorem and older diagonal-coboundary machinery, plus elementary normalization and cocycle averaging. That is different from locating a dated prior paper that explicitly states this full consequence. The audit does not decide first public statement priority.

## 5. Reverse challenges attempted

- **Ordinary homotopy instead of equivariant homotopy:** rejected as a gap here, because every edge-phase delta_t commutes with the entire given phase action. The path is explicitly equivariant.
- **Only nonequivariant KK equality:** rejected; the same explicit homotopy lives in the equivariant category with trivial cocycles.
- **Wrong theorem direction:** rejected; phi=id and psi=alpha_g gives the requested orientation.
- **Only multiplier or stable implementers:** rejected by unitality and the actual unital Theorem 5.8, whose proof returns a path in U(B).
- **No exact fixed membership:** repaired by finite averaging/polar; the defect is uniform over G.
- **Hidden representation condition:** absent. The uniqueness theorem is invoked separately for each g; no group law for the different paths is used.
- **Need source amenability or UCT:** source exactness is enough in the displayed unital theorem; source and target are the same finite-group graph system anyway. No UCT hypothesis appears.
- **Apply uniqueness to a nonouter action:** invalid. The quotient step is essential to this application, and it is displayed explicitly.
- **Projective family mistaken for a genuine cocycle:** avoided by the exact character formula for all D_g, which is an actual representation fixed by beta.
- **Cocycle invariance inferred from the Pauli action:** invalid; that projective family is not an honest cocycle. The direct averaging proof applies here.
- **Historical claim that periodic mathematics was unavailable before the candidate:** unsupported after the authenticated 2022 uniqueness consequence.
- **Historical claim that Gabe–Szabó printed the full nonouter CK theorem:** unsupported; only the general uniqueness statement was found in those bodies.

## 6. Access-gap resolution and remaining limits

Following the direct-lineage lead, the original [Kyoto 2002 PostScript preprint](https://www.math.kyoto-u.ac.jp/preprint/2002/4.ps) of Izumi's *Finite group actions on C*-algebras with the Rohlin property, I* was freshly acquired. The [official 2002 preprint index](https://www.math.kyoto-u.ac.jp/preprint/preprint2002.html) identifies it as item 4. Generic Ghostscript with safe mode converted the document for inspection; this is document rendering, not execution of source-author research software.

Actual converted-original body inspected: Definition 3.6 and Remark 3.7 p.13, Lemma 3.8 pp.13–14, Lemma 3.10 p.15, Proposition 5.6 pp.28–29. The original explicitly separates whole-fixed-algebra strong approximate innerness from the extra representation requirement. Proposition 5.6(2) confirms the standard-presentation finite-abelian Cuntz predecessor. These pages do not supply a separately stated general corner or honest-cocycle invariance theorem. The final 2004 typeset article was still not acquired; no final-page identity is inferred.

The full Zacharias 2000 chapter remains an access gap; the direct-lineage report inspected only its two-page preview, and that does not exclude a result in the remaining pages. This gap limits historical priority certification, not validity of the checked implication above.

The cross-challenge ran 11 new literal public queries, primarily to verify dates/source bodies and seek counterexamples to the proposed consequence. No negative search result is used as a novelty certificate. An incidental self/project search hit was not used as mathematical or priority evidence.

## 7. Input binding and exposure

The direct_lineage OUTPUT_MANIFEST hash was verified as 44593cdf174f2e30537a27f9bf82905421792f4e39b69e6e33d5deda55997a2e before its two reports were read. The old initial structural and detached followup outputs remain unchanged and are separately bound in INPUT_BINDINGS.json. Parent-provided summaries and the corner_cohomology_adversary report are explicitly known exposures. This cross-review is not described as blind.

Only this cross folder was written. New primary documents, conversions, page images and provider responses remain local-only. Public outputs consist of authored reasoning, public URLs, qualified source metadata, literal queries, and hashes. No external person was contacted, and no git, remote, publication, or current-edition mutation occurred.

