# Attempt 2/5: conservative translations and uniformly finite construction stages

**Corrected release, 3 October 2026.** This revises substantive attempt 2/5 after independent review; it is not a new attempt. All claims use [DATA_CONVENTIONS.md](DATA_CONVENTIONS.md). The frozen original remains unchanged. See [CHANGE_MAP.md](CHANGE_MAP.md) and the full audits in `audits/`.

Date: 2026-10-03 UTC. Continuing the explicit presented pretopos of attempt 1. The objective is to turn its finite normal forms into genuine constructive definitional extensions and prove the span/zigzag normalization. This is additional mathematical work; the earlier source gate remains frozen.

## A. Translating formulas without assuming representatives can be chosen

Suppose every sort A in an extended signature has been assigned a presentation (sum_i phi_i(x_i))/E in P_T, and every function and relation a proof-carrying arrow or subobject. For a context z_1:A_1,...,z_r:A_r, take one tag i_k for each variable. This produces a finite family of old-sort contexts and the support formula D=and_k phi^k_i_k(x_k).

Each extended coherent formula theta(z) translates to an old coherent formula theta_i(x), invariant under the product of the relevant E's. The clauses are explicit:

- true translates to D, and false to false;
- equality of variables in the same presented sort translates to E, conjoined with the other context supports;
- an atomic relation translates to its invariant predicate matrix;
- conjunction/disjunction translate entrywise;
- exists z:A theta translates to disjunction_j exists x_j theta_(i,j).

For a function term, first replace its occurrence by its functional graph and a local existential result variable. Its arrow matrix then supplies the preceding clauses. Graph totality and functionality modulo E prove that replacement preserves the formula. Induction on the term and then the formula gives invariance. Crucially, the sum over j remains outside that branch's existential witness; there is no tuple requiring a witness from an unused or empty component.

A sequent theta entails eta in an extended context translates to one old sequent theta_i entails eta_i for each finite context-tag combination. Contexts with zero possible tag combinations contribute no obligations, as appropriate for an empty context object.

Substitution is respected. For example, substituting an arrow matrix R for a variable amounts to existentially composing its graph with the translated formula. If two R-witnesses represent the same quotient value, invariance of the formula identifies the two results; totality provides a local witness. Identity substitution uses E-saturation, and composite substitution uses the composition formula of attempt 1. Thus the coherent deduction rules translate to finite coherent derivations. Cut corresponds to composition of the finite case splits, and existential rules merely introduce or discharge local variables.

## B. Conservative expansion theorem

Let U be obtained from T by a specified finite chain of the source's definitional/sort additions. Interpret the old symbols by their trivial presentations and interpret the newly added symbols stage by stage using attempt 1. The tuple, subsort, sum and quotient axioms translate respectively to the universal properties already explicitly derived there. A new predicate translates to its definition. A unique-function definition translates to its supplied total single-valued graph. Hence every axiom of U has a finite proof of its translation in T.

By induction on a U-derivation, its translated sequents are T-derivable. For an old-language sequent the trivial presentations and equality graphs translate back to the original sequent, modulo the elementary coherent identities already proved. Therefore U is conservative over T. This is a transformation of given finite proofs; it neither appeals to completeness for Set-models nor constructs a model of T in a classical universe.

This also proves that every newly introduced sort, predicate and arrow has a finite old-language matrix description. Repeatedly nesting quotients or sums does not escape the presentation form, because all the closure operations of attempt 1 produce another such form.

## C. A genuinely uniform finite-stage library

All proof-carrying presentations and arrows of P_T can be adjoined in five construction stages, with arbitrarily large sets of independent definitions permitted at each stage:

1. Add products for every finite old-sort context, including the empty context.
2. Add subsorts for every coherent old formula in such a context.
3. Add the finite disjoint sums of the subsorts needed by every object presentation.
4. Add a quotient for every presentation's specified provable equivalence relation on its sum.
5. Add names for the arrow graphs and invariant predicates on the resulting quotient sorts.

All tags are formal fresh tags. The indexing sets include the admissibility proof data, so no operation of deciding whether a formula is provably admissible or of choosing a proof is required. Distinct admissibility proofs can index distinct, canonically isomorphic copies; no minimal skeleton is selected.

Here is the explicit stage-5 graph construction. For the i-th old carrier of a presented quotient Q, let C_i(x,z) express that the carrier subsort's inclusion has coordinates x and that its image under the sum injection followed by the quotient map is z. This is a coherent formula using only stage-4 symbols. For a matrix R between Q and Q', its graph is

  disjunction_(i,j) exists x,y (C_i(x,z) and R_ij(x,y) and C'_j(y,w)).

The coverage axioms and matrix totality prove totality of this graph. Matrix functionality and the quotient axioms prove uniqueness. Invariance makes the result independent of different representing branches. An invariant predicate uses the same formula with only one tuple of codes and no target variable. Thus stage 5 is made of exactly the allowed predicate/unique-function additions. Function definitions use the displayed expanded formulas directly; they do not depend on a new predicate name introduced at that same stage. Similarly, the stage-4 congruence is written in the stage-3 sum language by the finite branch formulas. These conventions remove apparent same-stage dependencies.

No bound on the arity of the products across this stage is claimed. No bound on formula lengths is claimed. The number of stages is nevertheless five. This repairs the invalid inference from “each object has finite depth” to a uniform finite chain.

Trivial old-sort presentations can be realized by the old sorts themselves; their identity code is z=x. If it is more convenient to retain fresh quotient copies, add their canonical isomorphisms by the same graph rule. This is an alias convention, not an axiom asserting an arbitrary isomorphism. Original function and predicate names are retained alongside any generated graph-name aliases.

For any fixed finite extension chain U/T, interpret all U-sorts into these normal forms. To reproduce the actual U signature, two further stages suffice: first add a fresh unary-product copy of each chosen normal-form sort, using the desired renamed U sort label and its projection; then add the U functions and predicates by their transported matrix graphs. All U axioms are derivable by B. This seven-stage construction reconstructs a definitional presentation of U's translated generic data. It does not yet, by itself, prove that this translated expansion is a common extension over U; that requires the comparison data addressed in attempt 3.

## D. Finite zigzags can be amalgamated into a common extension

Suppose U and V are finite-chain definitional extensions of the same T. Rename their added symbols with disjoint tags while keeping the T symbols fixed. Then U union V is a finite-chain extension of U: repeat the successive definitions of V, now in the language containing U. Every defining formula is still present, every admissibility proof over its earlier V-stage is still valid, and the two added signatures cannot collide. Symmetrically it is an extension of V. This is a purely syntactic amalgamation construction.

Now consider a finite zigzag of finite-chain extensions and their reversals. Maintain a common upper extension of the part already traversed. At an arrow in the forward direction, amalgamate this upper extension with the next extension over the current theory. At an arrow in the reverse direction, the existing upper extension is already an extension of the next, smaller theory by concatenation. Induction gives a common upper extension. If the zigzag was originally expressed as consecutive spans, the same construction amalgamates the two span apices over the shared middle theory.

Renaming is indispensable: an identically spelled symbol in unrelated languages is not forced to retain incompatible definitions. Transport the endpoint theory through its recorded renaming bijection. The result is a finite span over the renamed endpoints, which is the source's “perhaps after renamings” convention. This argument is for a finite zigzag; no compactness or transfinite collapse has been assumed.

## Result of attempt 2

There is an explicit conservative proof translation and a uniformly finite-stage normal-form library, including empty sorts. Finite zigzags of these extensions normalize to a common extension after hygienic renaming. The remaining converse problem concerns obtaining a suitable comparison from an independently meaningful constructive Morita equivalence. A categorical equivalence supplied as actual functors and inverse isomorphisms is a promising next input; a merely essentially-surjective functor does not automatically supply such data constructively.
