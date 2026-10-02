# Independent early target seal — PR32 candidate only

Stage: CANDIDATE ONLY, original-stage source/proof/scope adversary. No complete priority or whole revised-package acceptance gate is underway.

Before this seal, I retrieved and read only the fresh literal university TeX source and relevant flag-question context. No submitted proof/code/results, prior review, readiness, source audit, root/sibling findings or project history have been read.

## Exact source identity and target
Fresh source: https://www.imo.universite-paris-saclay.fr/~pansu/problems_MTDG.tex . Bytes 42,288; SHA-256 33d853a6de512584aeedfaf5b491bcc7f0cf02d2964e8b1f1be67a5b3b97c48e. Literal retrieval succeeded; the web extraction tool could not access the TeX URL. The source is the Morgan–Pansu conference collection, 2018, with Elisha Falbel's section on flag manifolds. The second question in that section is global Question 7 (counted from the TeX question environments).

The full target is the homotopy classification of totally real immersions of real 3-manifolds into the complex full flag manifold F12=SL(3,C)/B, B upper triangular. The first neighboring question asks which manifolds are modeled on a real-form orbit. That different uniformization problem is not bundled into Question 7 and must not be claimed solved by an immersion classification. The contextual cited arXiv paper and h-principle observation are antecedent framework, not an explicit classification answer in the source.

## Scope and conventions fixed before candidate comparison
The source does not restrict to closed, compact, oriented, connected, or parallelizable domains. A broad answer must account for noncompact and nonorientable smooth real 3-manifolds. A result on closed orientable M is only a subclass unless separately extended. Standard manifold conventions may omit boundary, but the source does not specify a boundary-relative problem; a candidate should state its domain convention instead of silently asserting a relative theorem.

The flag is an ordered complex line contained in a complex 2-plane. It has the standard integrable complex structure coming from the stated Borel subgroup. The six root/order choices can alter labeled tautological Chern classes and tangent-bundle formulas; an unlabelled SU(3)/T2 identification must retain this complex structure and ordering. Classification is for a fixed domain M, not modulo domain diffeomorphisms or mapping-class action, unless explicitly stated.

The source's phrase “homotopy classification” does not explicitly distinguish ordinary homotopy of the underlying maps from regular homotopy through totally real immersions. These are materially different. An h-principle relates genuine totally real immersions to *formal immersion data*, which includes a real bundle monomorphism TM→f*TF with complexification an isomorphism. It does not by itself identify regular classes with just the homotopy classes [M,F12] of underlying maps. Any claimed complete answer must fix this convention and state which classification it delivers. I will test both readings; I will not silently erase differential/formal data.

The source imposes no embedding, injectivity, metric-completeness or properness condition. Noncompact M cannot map properly into the compact flag target unless M itself is compact (preimage of the entire target). Adding properness would change and possibly empty the target. Families/parametric/relative h-principle hypotheses and their effect on regular homotopy require the applicable complete theorem, not its existence-only summary.

## Independent mechanisms and falsifiers
* A necessary condition for a totally real immersion f is the complex bundle isomorphism TM⊗C ≅ f*TF12. Ordinary-map homotopy determines the target pullback but not a chosen isomorphism; formal-data homotopies matter for regular classification.
* For orientable 3-manifolds, parallelizability may simplify that condition. Nonorientable tangent complexifications cannot be assumed trivial. Characteristic torsion, not only rational Chern classes, must be checked.
* Primary map data should respect the three ordered tautological line quotients and their sum-zero relation. Secondary degree-3 obstruction data and the action of homotopies of primary data require an integral treatment, including torsion and nonorientable coefficients. Simply giving an integer for S3 does not classify all M.
* Dimension-three CW arguments cannot silently assume a finite CW complex or finite generation when M is noncompact. Absolute compact-open/weak topologies and homotopies at infinity must be declared; proper or compact-supported classes are different.
* Regular-homotopy fibers of formal complex isomorphisms have the homotopy type of GL(3,C)≈U(3), suggesting possible degree-one and degree-three differential data. A map-only formula needs a proof that the relevant data is intentionally forgotten or identified; the h-principle alone is insufficient.
* Boundary controls: S3 (secondary map data and differential π3), a 3-torus (primary classes and possible H1 action), lens spaces (integral torsion), a nonorientable product such as RP2×S1 (complexified-tangent obstruction), open R3 and punctured examples (ordinary vs proper/support conventions), disconnected domains, and relabeling flag lines.

## Success criteria and current gap
A full answer must give explicit classification parameters/equivalence relations for the exact declared domain and homotopy convention, prove necessity and sufficiency via valid formal-data and realization statements, and check all ordering/torsion/noncompact boundary cases. Finite identity checks or already known S3 results cannot independently certify such a classification. The exact gap is currently the entire candidate claim, not a preaccepted desired formula. No novelty or current open-status determination is made at this seal, and no new full-target proof attempt is initiated.

Best-guess assigned-audit completion: 10%; no mathematical discovery progress is claimed.
