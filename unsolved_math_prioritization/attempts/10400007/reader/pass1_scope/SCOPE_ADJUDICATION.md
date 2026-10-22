# Scope adjudication of the conformal-block H₀ candidate

**Edition note.** This records the accepted PASS1 transported construction and its scope at that stage. The mathematical theorem remains valid. The later direct geometric definition and current qualified acceptance are in [the reader](../JONES_RESEARCH_READER.md) and [PASS2 scope report](../pass2_scope/SCOPE_ADJUDICATION.md); the former imported-state objection does not apply to that strengthened definition.

14 October 2026 UTC. Roberts Problem 1.7 / row 1786 / problem 10400007.

This is an independent assessment of the candidate's relationship to the recovered source. It is not a new mathematical pass. The separate technical audit accepts the candidate's mathematical assembly; this report does not reopen its anomaly, normalization or interpolation calculations.

## Decision

**Accept the formal local-system-homology realization. Do not treat that acceptance as a certificate that Roberts's qualitative construction problem has been resolved.**

The candidate is substantially more than assigning an arbitrary coefficient vector space after computing a Jones value. It uses independently defined geometric local systems, a structure-preserving modular-functor comparison, and coherent three-dimensional operations. These are real mathematical merits.

Nevertheless, the candidate has not justified the further interpretation that its H₀ realization supplies the requested homological explanation of knot dependence. Its knot-dependent state is defined by importing the existing WRT exterior state; the added H₀ identification cancels from the scalar extraction. This identifiable dependency, rather than a lack of historical recognition or author endorsement, is the reason not to promote the formal theorem to an unqualified source-level solution.

**There is no exact, explicit source condition shown false here.** In particular, no mathematical counterexample to the candidate has been found. The unresolved item is the explanatory adequacy of this realization, not the existence of its spaces, local systems, homology groups, states, maps, or polynomial.

## 1. Source evidence and its limits

The question on printed page 385 requests, in paraphrase, an intrinsic construction of the Jones polynomial through local-system homology. The adjacent remark contrasts Alexander's complement interpretation with Bigelow's braid/plat construction and suggests complement configuration spaces as an example. It leaves the admissible construction class unspecified. Roberts's discussion on page 383 emphasizes ambient three-dimensional naturality without selecting a projection plane or axis. His introduction on pages 377–379 asks what topological information quantum invariants explain, while recognizing the value of TQFT cutting and pasting. [Ohtsuki volume, primary publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf)

There is useful corroborating context elsewhere in the same volume. Section 8.4, page 496, distinguishes a geometric realization of surface state spaces from assigning a geometric state to a bounding three-manifold; Problem 8.8 asks for the latter. This is contextual evidence, not an additional clause of Problem 1.7. It predates the later Andersen–Ueno comparison and cannot be used to deny that comparison's contribution. [Same primary source, §8.4](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf)

The source does not formulate an if-and-only-if test for the word “intrinsic.” Consequently, an adjudication should not pretend to extract a formal prohibition of H₀, quantum coefficient fibers, boundary surfaces, comparison isomorphisms, or auxiliary decompositions from it.

## 2. What the primary comparison literature establishes

Andersen–Ueno construct anomaly-corrected flat bundles over marked Teichmüller spaces, naturally under the extended surface category. Their modular functor takes horizontal sections; contractibility identifies these with a fiber. Zero-labeled-point propagation handles unstable or unsaturated surfaces. The relevant locations are Theorem 11.4, Definitions 11.2–11.3 and Proposition 11.1, pages 59–60 of the retained version. [Geometric construction, arXiv:math/0306235v2](https://arxiv.org/pdf/math/0306235v2)

Their later Theorem 1.1 gives an explicit isomorphism between the skein/WRT and vacua modular functors, compatible with all modular-functor structures. They explicitly identify the resulting construction as geometric WRT theory, using the determination of a TQFT by its modular functor. They also explain that duality and unitarity are transferred through the comparison rather than separately constructed geometrically there. [WRT from CFT, arXiv:1110.5027v2, introduction and Theorem 1.1](https://arxiv.org/pdf/1110.5027v2)

These results exclude objections based on a mere dimension coincidence, absent gluing theory, or coefficients fabricated from the Jones scalar.

## 3. The precise accepted theorem

With the conventions and established ingredients in the candidate, for every ordinary smooth/tame oriented knot pair in oriented S³ and every integer level k≥1 there are:

1. A geometrically specified finite-rank complex local system Lₖ on the marked Teichmüller space of the peripheral torus.
2. The ordinary local-system homology object Hₖ=H₀(Teichmüller space; Lₖ).
3. A naturally transported exterior state hₖ(K) and fundamental-colored solid-torus functional fₖ.
4. An exact normalized contraction z_k(K)=f_k(h_k(K))/f_k(h_k(U)) equal to V_K(exp(−2πi/(k+2))).
5. Exact reconstruction of the source-normalized Laurent polynomial from 4c+1 such contractions when c is the crossing count of any chosen diagram.

The accepted scope is all knots, with preferred framing and anomaly correction. An entire link theorem would need additional component/framing bookkeeping. A diagram supplies only a finite degree bound.

This theorem meets the five operational criteria when they permit genuine geometric coefficients, H₀, and extraction by canonically transported TQFT maps. Rejecting it under that reading would change the acceptance criteria after the fact.

## 4. What is and is not explained homologically

The distinction is visible directly in the candidate's formulas. Write

    ν_Σ = θ_Σ I_Σ,
    h_k(K) = ν_T Z_k^RT(E_K)(1),
    f_k = Z_k^RT(N_K, core_1) ν_T^−1,

with the normalized empty-surface identification understood. Then

    f_k(h_k(K))
      = Z_k^RT(N_K, core_1) Z_k^RT(E_K)(1).

The homology comparison cancels before evaluating the scalar. This is a dependency analysis of the proposed definition, not a counterexample to it.

For knots with the same peripheral torus type, the underlying Teichmüller-space/local-system construction is the same up to its specified natural identifications. Ordinary H₀ identifies parallel fibers. The local-system chain boundary does not itself detect which knot exterior supplied the state. Every piece of knot-specific information in this implementation enters through Z_k^RT(E_K), followed by the chosen filling. If one knows only the boundary local system, its homology, and the standard filling, but not the exterior state, this implementation supplies no rule for determining the missing knot-dependent vector except the WRT/CFT three-dimensional theory already imported.

That observation has two equally important limits.

First, it does **not** show that the state is arbitrary. Naturality, factorization, and the geometric modular-functor comparison constrain the entire construction. In particular, the equivariant flat-bundle structure contains genuine surface geometry even though the Teichmüller base is contractible. Treating the candidate as equivalent in explanatory quality to an arbitrary vector space on a point would erase its strongest substantive ingredient.

Second, it does **not** follow that the extra ordinary H₀ step has supplied a new explanation of the exterior's topology. At this step the candidate re-expresses an already available geometric quantum theory. Passing from horizontal sections to H₀ is a canonical realization, but does not by itself identify a knot-sensitive homological mechanism beyond that theory.

Cancellation alone never invalidates a geometric interpretation: valid comparison theorems routinely identify apparently different formulas. The relevant feature here is that the knot-specific state is introduced by the transport formula itself, rather than first being specified by additional homological data whose agreement with the quantum state is then proved. That limits what this particular assembly establishes; it does not prohibit such additional data or prove they are necessary in every acceptable answer.

## 5. Exact requirement analysis

### Explicit mathematical conditions

No explicit condition about allowed degrees, ranks, spaces, monodromy or extraction has been exhibited that this candidate violates. Nor is there a missing existence theorem for its three-dimensional operations. The independent mathematical audit accepts those operations and their coherence.

The candidate also passes the narrow anti-circularity check: it does not read a previously computed Jones scalar into a local system or state. Importing a mathematically defined WRT functor is a dependency on prior theory, not circular reasoning.

### The qualitative obligation still unsubstantiated

The adopted contract asks for an explanation from the topology and its homological data, rather than a homological label. The candidate establishes a natural realization of the state spaces and operations but does not establish that moving this geometric quantum theory through H₀ supplies the additional explanation sought by that phrase.

There are two honest readings:

- Under a **realization reading**, an intrinsic geometric modular functor, its coherent three-dimensional extension, and its genuine local-system H₀ realization suffice. The candidate answers that precise reading.
- Under an **explanatory reading**, the homological description should reveal how knot/exterior topology determines the relevant classes or operations beyond transferring the existing quantum assignment. The current assembly does not provide that further account.

These labels describe the present adjudication; they are not terms defined in the source. The second reading is supported by the source's context, but is not formalized there into a unique extra axiom. Accordingly, the correct disposition is **source-level explanatory completion not established**, rather than **theorem false** or **explicit source condition contradicted**.

A direct geometric cycle, a correspondence, a characteristic construction of the exterior state, or another substantive account could strengthen the explanatory case. None is hereby imposed as a mandatory source condition. Positive degree, a classical fiber, a complement-configuration base, and a ban on comparison transport would all be unjustified blanket requirements.

## 6. Recommended claim and stopping boundary

A precise, defensible claim is:

> The Jones polynomial of every knot admits a functorial realization through degree-zero homology of the Andersen–Ueno geometric local systems, with exterior states and fillings transported from WRT theory, followed by exact finite reconstruction. This assembly is a formal local-system-homology realization of known geometric quantum theory; its status as the homological explanation requested in Roberts Problem 1.7 is not established here.

The independent audit is sufficient for accepting the formal theorem. No author contact is needed for that acceptance. Conversely, author endorsement would not repair a mathematical error if one existed.

Do not claim any of the following from this scope audit:

- A new theorem resolving the original qualitative research problem.
- That Roberts or the literature rejects or accepts this exact H₀ realization.
- Present-day openness, novelty, or impossibility of the original problem.
- That a genuine geometric CFT/WRT interpretation does not exist.
- That all transported or degree-zero constructions are vacuous.

The bounded searches did not locate a primary source expressly adjudicating this specific H₀ packaging as an answer to Problem 1.7. That negative search observation is not used as the logical basis of the disposition. The basis is the distinction between the accepted formal theorem and the additional explanatory interpretation.

## 7. Inspection and provenance

The source documents, complete candidate and independent technical audit were inspected, with primary locations cited above. Current arXiv records pin math/0306235v2 and 1110.5027v2. The accompanying metadata records input hashes. This is a separate scope supplement to the sealed pass-1 mathematical audit, not a new proof attempt or an exhaustive status survey. Mathematical passes added: **0**. No publication or third-party communication was performed.
