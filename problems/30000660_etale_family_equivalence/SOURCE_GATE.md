# Exact source and prior-attempt gate: 30000660

Gate completed 2026-10-02. This gate consumes no author turn.

## Original and imported target

The authority is Hanspeter Kraft and Peter Russell's Problem2 in *Affine Algebraic Geometry*, OWR01/2007, printed p.69 (physical PDF65), DOI10.4171/OWR/2007/01. [Publisher](https://ems.press/journals/owr/articles/1452); [official full PDF](https://ems.press/content/serial-article-files/46087). The whole local contribution, preceding problem-session setup and relevant later definitions were read; p.69 was visually inspected.

Proposition1 states that for morphisms p:S->X and q:T->X of k-varieties over an algebraically closed field of infinite transcendence degree over its prime field, isomorphic schematic fibers imply equivalence after a dominant **étale** base change. Problem2 asks for extension to every algebraically closed field, or counterexamples over **F_p-bar or Q-bar**. The import dropped both overbars. It also says “every schematic fiber” without clarifying the classical closed-point convention.

The hypothesis is about closed fibers in the classical variety formulation. This is made explicit by the authors' subsequent paper's abstract, and by its proof using a closed k-point representing a generic fiber of a smaller field of definition. It is not a hypothesis of isomorphism over every residue field including the generic point; that stronger hypothesis already gives a generic isomorphism which spreads over a dense open.

Neither the proposition nor the problem assumes reduced fibers, geometrically integral fibers, smooth morphisms, or an affine-space fibration. The report's problem session has separate contributions with their own hypotheses, not a global characteristic-zero convention. The Kraft–Russell contribution explicitly allows the prime field of positive characteristic. The counterexample proved here has **smooth geometrically integral A¹ geometric fibers**, so no conclusion depends on exploiting nonreduced fibers.

## Decisive later-version distinction

Kraft–Russell, *Families of Group Actions, Generic Isotriviality, and Linearization*, Transformation Groups19 (2014),779–792, DOI[10.1007/s00031-014-9274-9](https://doi.org/10.1007/s00031-014-9274-9), [author-hosted published copy](https://dmi.unibas.ch/fileadmin/user_upload/dmi/Personen/Kraft_Hanspeter/Families_Group_Actions.pdf), §2 printed782–784, gives the Generic Equivalence Theorem with **affine morphisms**, the same infinite-transcendence-degree condition, and a dominant base change of **finite degree**. It does not assert étaleness in positive characteristic. The introduction p.780 explicitly explains that in characteristic zero the finite-degree morphism can be chosen étale. Remark2.2 leaves the arbitrary-algebraically-closed-field version of that finite-degree theorem open, mentioning Q-bar.

The April2012 arXiv1204.3196v1 theorem still says étale although its proof only produces a finite extension; the 2014 published version is the later authority for that theorem. All these exact source passages were read, and the 2014 p.780 and p.782 were visually inspected. No claim is made about why the wording changed, beyond the mathematical distinction actually printed.

The separate definition of an affine fibration in the paper requires flatness and reduced mutually isomorphic fibers. It is not imposed on the Generic Equivalence Theorem. In any event the smooth counterexample in TURN_1.md satisfies this stronger fiber requirement.

## Classical input and credit

Peter Russell, *Forms of the affine line and its additive group*, Pacific J. Math.32(2) (1970),527–539, DOI[10.2140/pjm.1970.32.527](https://doi.org/10.2140/pjm.1970.32.527), explicitly gives on p.527 the form y^p=x+a x^p for a not a p-th power; Lemma1.1 describes purely inseparable minimal splitting fields. [Official MSP PDF](https://msp.org/pjm/1970/32-2/pjm-v32-n2-p19-s.pdf). Our family specializes this **classical form** to a=t and supplies a direct elementary proof. Russell himself credits an earlier source for the example. No invention or historical priority claim is made here.

The negative answer pertains to the literal **2007 étale** question, including its F_p-bar alternative. It does not refute the later finite-degree statement, settle the Q-bar case, or answer a positive-characteristic question after changing its conclusion without saying so.

## Retrieval and prior-attempt checks

The requested unsolvedmath.com/problems/30000660 page was attempted but inaccessible in the web tool. The pinned imported record was recovered and checked against the primary PDF, including the lost overbars. Full official2007,2012arXiv,2014published and1970Russell papers are retained locally; raw PDFs/images and imported records are excluded from public artifacts.

Live main efd29c05204703acca9a0860812f54b94fae54b1 had row380 queued0/5. Exact ID all-state PR, branch and commit searches returned none; main code search found catalog metadata only. Searches for “generic equivalence,” Kraft/Russell, and fiberwise/fibrewise isomorphism found no overlapping public attempt. A read-only recovered clone with443 refs had no matching all-ref commit subjects or per-ref tree paths. This is a bounded prior-attempt search, not an exhaustive semantic search of every historical blob.

Pinned dataset revision37e53eabe540fb458758e198be61634bd02ee008; problems.json SHA04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf; research_results.json SHA8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b. No prior report for this ID was present.

**Gate:** enough primary material to distinguish the literal étale question from the later finite-degree residual question. The next proof is a genuine author turn applying an explicitly credited classical example; final disposition awaits independent review.
