# Classical tree mechanisms: corrected effective V2 priority audit of PR108

No checked source in this family establishes an earlier resolution of the literal Kaibel Problem1 or implies the candidate's complete restriction bundle through an authenticated mapping. Priority remains **0% established**. The inherited mathematical gate is100%; this family reviewed sources and model correspondences, with **zero new central proof-search approaches**. These are separate conclusions. The source differences below do not certify novelty.

The audit is bound to original head `3526d46bf143b08e5055ffa7728c6278e9f958ea` and the repaired proof's SHA in [INPUT_BINDINGS.json](INPUT_BINDINGS.json). The original approach record remains2/5, sourced from QUEUE and two-approach prose; no original structured ledger has been supplied or reconstructed. V1 is immutable history; this correction writes only the corrected_v2 subfolder. No Git/index, service/editor, publication, outreach, or preparation of outreach was performed.

## Exact claim and independence

I read the **full original Kaibel contribution first**, printed3014–3015/PDF46–47 of [OWR50/2018](https://ems.press/content/serial-article-files/46772?nt=1), and then the entire repaired candidate proof. The target selects **one common undirected spanning tree** T. At every vertex r, T determines its rooted orientation T^r. Independently supplied costs c_r(u,v) are summed over **all arcs** of T^r and then over **all roots**. The cost data are explicit and finite.

Independent per-root tree choices are a different feasible set. Destination-path costs in one fixed-root tree are the neighboring Problem2. Neither is the target reviewed here. Kaibel's Martin-formulation motivation is part of the original statement; the candidate does not claim a formulation-equivalence theorem.

[immutable V1 mechanism freeze](../MECHANISM_FREEZE.md) records the mechanism and the first primary-source search before any current peer priority output or root priority conclusion was read. Frozen UTC was2026-10-06T05:00:54.331783+00:00. JLRK and communication-tree sources were independent first leads. The shared-arborescence preprint was a later source lead from the parent, explicitly identified as such. Original-author source records/logs were inspected only after the freeze and supplied no additional primary literature receipt. They did not replace the independent search.

## Cost distinctions that need an exact mapping

For an edge e=uv of T, write S_u,S_v for the two components of T−e. For outward orientations, the literal contribution of e is

    sum_(r in S_u) c_r(u,v) + sum_(r in S_v) c_r(v,u).          (A)

Summing(A) over e gives the full target objective. Thus the cost of a specified edge is linear in individual root membership in its fundamental cut. By contrast, an unordered communication-tree objective has contribution

    w_e * sum_(s in S_u, t in S_v) demand(s,t),                 (B)

which ordinarily couples two cut memberships. In a rooted flow model the charge is arc length times the **tree-dependent flow amount**, rather than a fixed input coefficient times the binary orientation indicator. A source model with the same tree support can therefore have a different objective.

If c_r(u,v)=c_r(v,u) for every r, the literal objective reduces to an ordinary edge sum with edge weight sum_r c_r(e). In particular, setting every root's two directed costs to the same edge length charges each chosen edge N times. It does not produce pair-path distance. On K4, symmetric unit costs give literal value12 to both a star and a path, while unordered routing costs are9 and10. Four possible cuts containing endpoint0 but not1 have unit pair loads3,4,4,3; their mixed difference is−2, whereas a linear root-membership expression has mixed difference0.

These observations falsify direct cost identifications. They do **not** prove that no polynomial reduction, extra gadget, or global reformulation can exist. Every claimed transfer still needs a check of all feasible choices, both reduction directions, complete objective/threshold correspondence, and all claimed input restrictions.

## Checked constructions and closest models

**JLRK: the earliest full hardness proof retrieved in this family.** The [institutional primary preprint](https://ir.cwi.nl/pub/9700/9700D.pdf) is BW70/77, with February1977 on its cover; the [Networks journal publication](https://onlinelibrary.wiley.com/doi/10.1002/net.3230080402) is1978. I read the complete preprint, including both reductions. Theorem2 uses unit lengths, a spanning-tree budget and exact3cover. Its threshold forces a fixed hub/set core and element leaves. The remaining objective rewards element pairs grouped at the same set vertex. The graph and numerical quantities are polynomially bounded. These are restrictions for its pair-distance problem, not an established transfer to the present target.

There is a stronger same-support obstruction. Let H be any fixed core tree; every additional vertex x is a leaf whose chosen attachment a_x lies in H. Its permitted attachment set may vary with x. On this support family, **any** prescribed all-root single-arc costs have the separable form

    F(T) = constant + sum_x g_x(a_x),
    constant = sum_(r in H) c_r(H^r),
    g_x(a) = c_x(x,a) + sum_(r != x) c_r(a,x) + c_x(H^a).      (C)

To check(C), root x directs its own leaf edge x→a and the core away from a. Every other root directs that leaf edge a→x. For a root in H the core orientation is fixed; for a leaf root x it depends only on a_x. Every leaf edge and every core edge is charged exactly once per root by the displayed expression. There is no dependence on a second leaf's attachment in g_x.

JLRK's threshold-forced support family has this form. Its pair-grouping savings cannot be recovered simply by assigning target arc costs to those same structured supports. A five-vertex check with two independent leaf attachments gives literal values20,21,18,19 (mixed difference0), while unit all-pair distance values are18,20,20,18 (mixed difference−4). This is a comparison lemma about the published architecture, not a new target-hardness route. A materially different reduction remains possible and unaudited.

**Hu: earlier definition, incomplete proof access.** [Official SIAM metadata](https://epubs.siam.org/doi/10.1137/0203015) dates *Optimum communication spanning trees* to September1974, pp188–195. The publisher's full PDF could not be retrieved (curl exit56, zero bytes). I did not authenticate its complete special-case/cut-tree proofs or import any hardness restriction. The original printing date, a model definition, and a sufficient prior literal-target theorem are distinct evidence categories.

**All-root communication-tree formulations (corrected V2).** [Tilk–Irnich2016](https://download.uni-mainz.de/RePEc/pdf/Discussion_Paper_1613.pdf), §3.2, couples commodity supports through one common undirected spanning tree, but the compact objective charges flow amounts f, rather than fixed coefficients times orientation indicators y. In the independent commodity-u pricing model(5), printed7/§4.3.2, the objective is fixed activation charge γ^u_ij y^u_ij plus flow charge c_ij f^u_ij, less a column constant; γ=−π≥0 comes from dual edge-coupling prices. The model uses at most N−1 selected arcs.

The source explicitly distinguishes demand cases. It guarantees spanning-tree generation only when every nonroot demand r_ui is positive. When a commodity has zero-demand vertices, the pricing support need only reach positive-demand terminals; the paper adds nonroot-indegree inequalities and explicitly prunes zero-demand leaves. Its global assumption that each vertex has some positive incident communication does **not** make every vertex a positive-demand terminal for every commodity.

Consequently, setting every flow-charge coefficient to0 can still leave a **fixed-cost Steiner support problem**. The source's Steiner-generalization hardness statement does not make the flow-charge term essential. The historical V1 inference to minimum spanning arborescence without a mandatory-vertex condition was incorrect and is withdrawn.

There is a conditional statement for the independent pricing problem: if every nonroot vertex must be reached (for example r_ui>0 for each i≠u), M is sufficient for the total demand, and only the source's nonnegative fixed activation charges remain, a feasible support with at most N−1 arcs is a spanning arborescence rooted at u. Conversely, each rooted spanning arborescence carries the given demands with such M. Minimizing these fixed charges is then a minimum-cost rooted spanning-arborescence problem. This restricted observation says nothing about the complexity of coupling all roots through one common tree.

No exact prior-target implication follows from either demand case. The full communication-tree objective charges tree-dependent flow; its hard pricing subclass may omit optional zero-demand vertices, and an individual pricing problem is decoupled by commodity. The literal target instead requires one shared undirected spanning support, every vertex root, and costs over every arc of every induced full rooted tree. A source-to-target transfer must prove all these feasible-set and objective correspondences. [Zetina et al.2017](https://www.cirrelt.ca/documentstravail/cirrelt-2017-72.pdf), complete definitions and arc model1–7, likewise uses communication demand on pair paths; no target correspondence was authenticated.

**Shared arborescences.** In the [Alvarez-Miranda et al.2016 primary preprint](https://msinnl.github.io/pdfs/MKLSTP-main.pdf), generic MCSN allows arbitrary topology families. That framework can describe many subclasses, but its broad hardness does not establish hardness of each subclass. The specialized shared Steiner-arborescence model has one common root, user terminal subsets, and a shared directed network. Its complete model and Figure1 permit shared2cycles and multiple incoming arcs. They do not enforce one common undirected spanning tree with all induced vertex-root orientations and whole-tree charges. I checked complete relevant §§1–2.2, SCF1–11 and directed-cut/subproblem models§3–3.1. No exact specialized-model-to-target mapping was authenticated.

**Tree orientation.** [Medvedovsky et al.2008](https://www.cs.tau.ac.il/~roded/orient.pdf), complete Theorems1–2, reduces MaxDiCut/Max2SAT to orienting an **input** star/binary tree so that ordered pairs become reachable. The orientation is freely chosen. On a fixed tree input, the literal target has one feasible undirected support and all rooted orientations are forced. This direct correspondence already fails at the level of feasible choices; the degree and approximation results do not transfer by identifying objectives.

**Changeover/reload costs.** [Gozupek et al.2014](https://bilmuh.gtu.edu.tr/~dgozupek/Gozupek_TCS14.pdf), complete relevant definitions and all§§3–4 hardness proofs, is closer in choosing an undirected rooted tree. Its objective charges the color pair of an edge and its **chosen predecessor edge** in that tree. That predecessor is a variable, whereas c_r(u,v) is prescribed input on one arc. The paper's bounded-degree and0/1, two-color theorem does not establish the target's0/1/2 or positive-cost restriction without a gadget/objective correspondence.

The [SEA2011 original chapter](https://link.springer.com/chapter/10.1007/978-3-642-20662-7_10) remains subscription-only at the checked publisher page. I subsequently retrieved the associated [author revised2013 primary preprint](https://optimization-online.org/wp-content/uploads/2011/09/3166.pdf), read both complete §2 reductions/proofs, §3.1 and the full BQP model2–5 in§4. Its actual objective uses products of adjacent selected-arc indicators. Prescribed single-arc minimum arborescence supplies only a **lower bound** in§3.1. The original2011 version remains a chronology gap: the revised text explicitly adds a theorem, so all retrieved2013 results must not be dated to2011. This narrower gap is no evidence of a sufficient literal-target antecedent.

**Rainbow/compatible support issues.** [Berczi et al.](https://arxiv.org/abs/2412.15457) was retrieved as v2 dated December9,2025; v1 was posted in2024. I checked the complete §2 RootedRA reduction and §4.4 common-underlying-tree result. The hard problem selects one output arborescence with exactly one arc of each input color, with a fixed output root and potentially parallel colored arcs. The two-input-root restriction concerns roots of colored input arborescences, not two active target cost vectors. The identical-underlying-tree section proves an existence case, not the target's arbitrary-cost hardness. No full simple-graph/all-root encoding of color feasibility and objective was found. Searches of directed-Hamiltonian and compatible-branching phrases located no independently authenticated construction for the literal target; that search outcome is not a nonexistence theorem.

## Entire advertised bundle

[NOVELTY_MATRIX.json](NOVELTY_MATRIX.json) compares every checked source against every advertised restriction. None of the checked mappings establishes the whole bundle, or a genuinely new residual within it. The status for each target restriction is **unestablished transfer**, even when a source proves a similar named restriction for its different model.

The candidate uses a connected simple graph with N=n+m+2 vertices and at most1+2n+3m edges. A **dense finite cost table** means that all N×2|E| entries are explicitly supplied; it does not assert a dense or complete input graph. Original costs are0,1,n+1 and K=(n+1)m+n. Their polynomial bounds support the candidate's strong-NP/unary claim under the inherited mathematical gate. Root-dependent directional asymmetry appears in its clause-root costs.

For the same two-hub construction, the audited identity at arbitrary B≥2 is

    p+Bq = (Bm+n)+(1−h)+(B−1)(q−m).                           (D)

Because q≥m and h≤1, a cost at most Bm+n forces h=1,q=m. Thus B2 gives costs0,1,2 and threshold2m+n using the same literal-cost argument. This is an audit consequence of the existing mechanism. It supplies no independent priority clearance or new approach count. A uniform shift by1 adds N(N−1) to every feasible objective, giving positive costs1,2,n+2 in the original choice or1,2,3 for B2. The same constant must be added to K.

No candidate claim reviewed here concerns unrestricted global OPT=K+minimum-unsatisfied-clauses (which is false), bounded degree, planarity, a fixed number of active roots, approximation, formulation equivalence, or neighboring Problem2. Such stronger/different claims must not be inferred from a source's neighboring results or from the structured-tree identity.

## Evidence, limits, and result

[COMPARISON_RESULTS.json](COMPARISON_RESULTS.json) and [immutable V1 compare_cost_models.py](../compare_cost_models.py) retain the first-party finite checks: all16 K4 spanning trees satisfy(A), direct symmetric-cost ranking differs from routing ranking, and four fixed-core leaf supports satisfy(C) with the predicted distinct mixed differences. [TILK_ZERO_FLOW_RESULTS.json](TILK_ZERO_FLOW_RESULTS.json) checks the pricing-model boundary: with zero flow charges, a zero-demand leaf is omitted at fixed cost1, whereas making that leaf a positive-demand terminal forces the full support at cost6. This is a finite model check, not a new central proof-search route. These checks corroborate the identities and failed mappings; they are not a complexity proof or a comprehensive reduction search.

[SOURCES_AND_READ_SCOPE.json](SOURCES_AND_READ_SCOPE.json) distinguishes full proofs, full relevant models, metadata-only evidence, and unread portions. [SEARCH_LEDGER.json](SEARCH_LEDGER.json) records dated ordered queries, primary URLs, provenance and coverage gaps. Web search has no exposed CLI process ID; query dates/sequence are recorded without invented timestamps. The [immutable V1 CLI ledger](../CLI_LEDGER.jsonl) records original retrieval/extraction processes, including failed access. The effective [V2 CLI ledger](CLI_LEDGER.jsonl) records the primary-model reread and finite boundary check with actual PIDs, argv, UTC, exits, byte counts and hashes. Existing source bodies are pinned in place; no PDF is copied into V2. Raw third-party PDFs, text extracts and retained raw search responses are private; public artifacts contain metadata and first-party comparative reasoning.

The strongest verified priority finding is the failure of the checked direct transfers, particularly the fixed-core leaf separability comparison. The earliest related printing is Hu1974 metadata; the earliest fully checked related hardness printing is JLRK's February1977 preprint, followed by its1978 journal version. **No sufficient earlier literal-target result was authenticated. No genuinely new residual is certified.** Full prior coverage and novelty remain unresolved. No human-referee, novelty, publication or closure authority is claimed.

## Independent go/no-go recommendation

**GO at this family's source-priority review stage** to the parent's fresh combined adversarial review and, if it passes, a narrowly attributed note answering the cited2018 question. This family found no concrete sufficient antecedent or exact source-to-target mapping that blocks that limited claim. **NO-GO** for certified novelty, absolute first-discovery or exhaustive-history language.

Hu1974's unavailable full proof and SEA2011's unavailable original version are explicit coverage/chronology limits in visibly different pair-path and predecessor-edge models. The related revised2013 predecessor-edge proofs/model have now been checked. These gaps do not themselves supply a concrete reason to suspect an earlier sufficient literal-target result. Generic unknown transformations are a possibility, not an identified material obstruction. The direct mapping obstruction proved here concerns JLRK's fixed-core leaf architecture; it is not an objection to the candidate's mathematical argument.

Concrete follow-ups, if primary access becomes available, are Hu's full original special-case/cut-tree proofs and the SEA2011 version comparison. A newly located exact-target paper or explicit proposed transfer would warrant another full proof audit. A finite literature search cannot guarantee the absence of every earlier result; an impossible exhaustive-history guarantee is not a prerequisite for completing this bounded packet. A properly attributed answer to a recorded2018 question makes a narrower historical assertion than absolute first discovery. This recommendation does not confer publication authority.


## Correction and effective-version boundary

[CORRECTION_LEDGER.json](CORRECTION_LEDGER.json) identifies the historical defect, withdrawal, exact replacement and impact. V1 remains byte-for-byte sealed history. This complete V2 report, verdict, novelty matrix and source/read-scope ledger are the effective family assertions. Primary source pins bind the existing V1 PDF and full text; the relevant model was independently re-read at printed3–7, including §3.2, §4.2 and all of §4.3.2.

The correction removes an invalid argument about why the pricing problem is hard. It does not establish a new literal-target antecedent or invalidate the fixed-core leaf separability comparison. The source-priority recommendation remains GO to fresh combined review and a narrowly attributed answer to the2018 question if that review passes; NO-GO for novelty certification or absolute priority. Mathematical gate100% is inherited, priority establishment0%, original approaches2/5, new central proof routes0. The parent and its fresh reviewer must recheck the corrected packet; this is no publication/closure authority.
