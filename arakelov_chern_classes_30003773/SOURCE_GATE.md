# Source gate: geometric Chern classes in Arakelov cobordism

Checked 21 October 2026. Ordered queue row 1832; catalogue ID 30003773; source key OWR-16158-016.

## Verdict

**Original research question recovered; no complete solution verified.** Its target is the arithmetic homotopy-fibre construction described by Gereon Quick, not merely Rodriguez's weak arithmetic cobordism or the later complex-manifold Hodge-filtered cycle model. The source does not specify enough conventions to turn its informal request into a unique fully quantified assertion. The catalogue's claim of a self-contained statement and its conflation with Rodriguez require correction before proof work.

## Provenance and exact question

Gereon Quick, joint work with Michael J. Hopkins, *Algebraic Cycles in Generalized Cohomology Theories*, printed pp. 1074–1075, in *Mini-Workshop: Arithmetic Geometry and Symmetries around Galois and Fundamental Groups*, Oberwolfach Reports 15 (2018), no. 2, 1021–1080, DOI 10.4171/OWR/2018/17. [Official record](https://ems.press/journals/owr/articles/16158), [official PDF](https://ems.press/content/serial-article-files/46740). Workshop: 15–21 April 2018; publication: 12 April 2019. Thus the catalogue's 2019 bibliographic date and 2018 problem year describe different events, not two sources.

The question on p. 1075 asks for a geometric interpretation of Chern classes in Arakelov algebraic cobordism (paraphrase; no source text included).

The immediately preceding construction takes the homotopy fibre of a natural map from the motivic Thom spectrum to a pushforward of Hodge-filtered cobordism for schemes over number rings. Rodriguez is mentioned as related work, not as an identified equivalent theory. The preceding discussion of complex varieties and Abel–Jacobi invariants provides motivation; its compactness and nullbordism conditions must not automatically be assigned to every object of the arithmetic question.

## Supplementary original-author model

Quick's [2016 Paris lecture slides](https://gereonq.folk.ntnu.no/Presentation%20Paris%202016.pdf), PDF p. 161, display

\[
\mathrm{MGL}_{\mathrm{Arakelov}}\longrightarrow\mathrm{MGL}_S
\longrightarrow\eta_*(\mathrm{MU}_D).
\]

The slide specifies a finite-type scheme over the integers and its generic point. The left object is identified as the homotopy fibre. This confirms the type and direction of the construction; it is not a substitute for a full foundational definition. Neither the slide nor the OWR paragraph supplies all realization choices, embeddings, descent/conjugation conventions, twists, coefficient conventions, or geometric cycle relations. The notation for the generic point should not be silently generalized to reducible schemes without clarification.

In particular, the source does not say whether “Chern classes” means Chern operators acting on the fibre theory, or fibre-valued classes attached to additional geometric/trivialization data. It does not assert that every ordinary motivic Chern class canonically lifts to the fibre. A proposed formalization must state which meaning it uses and prove the needed compatibility, rather than import a unital orientation or universal lifting claim without justification.

## Three related but distinct established constructions

### Hopkins–Quick: Hodge-filtered cohomology

Hopkins–Quick, [*Hodge filtered complex bordism*, arXiv:1212.2173](https://arxiv.org/abs/1212.2173), Journal of Topology 8 (2015), 147–183, constructs the Hodge-filtered target. Section 7 constructs Chern classes for algebraic vector bundles on smooth complex algebraic varieties, proves a projective-bundle formula, and proves compatibility with complex cobordism and Deligne cohomology (Proposition 7.8). These are classes in Hodge-filtered cohomology, not automatically classes in the arithmetic homotopy fibre.

### Rodriguez: weak arithmetic cobordism

Rodriguez, [*Weak Arithmetic Cobordism*, arXiv:1608.04191](https://arxiv.org/abs/1608.04191), constructs a geometric arithmetic theory over a number field. Remark 3.2.1 deliberately confines the construction to varieties over a field rather than general Dedekind schemes. Definition 3.2.2 uses projective maps with Hermitian line-bundle decorations and analytic current data. Definition 3.3.6 explicitly defines a first Chern operator: it adds the pulled-back Hermitian line bundle on geometric generators and multiplies the analytic component by the Chern form times a universal inverse Todd form. Section 3.5 passes to the arithmetic relations, including formal-group-law relations.

Consequently, a blanket statement that Rodriguez supplies no geometric Chern interpretation is not supported. What is missing from the inspected material is an identification with Quick's arithmetic homotopy-fibre construction and a compatibility theorem transferring this geometric operator to that target. A formula in Rodriguez's theory alone does not resolve the OWR request. The introductory proposed future extension of an exact sequence by higher motivic cobordism is not an already-proved comparison equivalence.

### Haus–Quick: later geometric Hodge-filtered theory

Haus–Quick, [*Geometric Hodge filtered complex cobordism*, arXiv:2210.13259v2](https://arxiv.org/abs/2210.13259v2), Advances in Mathematics 431 (2023), 109244, gives a geometric model on filtered smooth manifolds and compares it to Hopkins–Quick for complex manifolds. The paper's abstract, introduction, construction and comparison headings were inspected and the full extracted text was searched for arithmetic/Arakelov terminology; no arithmetic-fibre comparison was found.

Haus–Quick, [*Geometric pushforward in Hodge filtered complex cobordism and secondary invariants*](https://ems.press/content/serial-article-files/47265), Documenta Mathematica 29 (2024), 457–509, DOI 10.4171/DM/951, constructs pushforwards along proper holomorphic maps, geometric fundamental classes and secondary Abel–Jacobi invariants. Introduction and §§2, 6 scope were inspected, with a full-text arithmetic/Arakelov screen. These are substantive advances in the complex-manifold target theory, not an asserted construction over number rings. Chern–Simons forms and geometric fundamental classes do not by themselves prove the missing arithmetic comparison.

## Current-status boundary and next research obligation

The original 2018 problem is explicitly open in its source. Searches on 21 October 2026 for the exact arithmetic name and geometric Chern target, together with screening Quick's [current publication list](https://gereonq.folk.ntnu.no/) through listed 2026 preprints and the directly relevant later papers above, did not verify a resolution. This is a bounded negative finding, not a proof of present-day openness or a full audit of every cited proof. No newer explicit author statement that this precise problem remains open was recovered.

A defensible next step must fix the arithmetic category and regulator model, then distinguish fibre-valued classes from Chern operations on a module theory. It must justify how any geometric model maps to the actual homotopy fibre and respects the relevant characteristic-class operation. Simply reusing ordinary oriented-cohomology classes, Rodriguez's operators, or the 2023/2024 Hodge-filtered model is insufficient.

