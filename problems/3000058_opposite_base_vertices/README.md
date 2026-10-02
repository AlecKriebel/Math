# Opposite vertices: bounded-base partials and a source-scope correction

**Bounded research target: unsolved,5/5.** Separate full AI-assisted review passed the scoped proofs with a mandatory additive definition correction. No human peer-review, formal-verification or novelty claim.

## Read the correction first
The current Egres definition permits extended-valued ranks and unbounded base polyhedra. Its literal wording is refuted by the ray {(t,−t):t≤1}, whose only vertex is(1,−1). The negative point is feasible but is not a vertex. The historical author proofs silently started with finite ranks; their positive conclusions apply to **bounded base polytopes**. SOURCE_SCOPE_CORRECTION.md explicitly corrects that scope without changing frozen historical bytes. The question page dates to2011 and the linked definition's modification to2014; this record does not infer the original author's intended convention. The elementary ray does not solve the nontrivial bounded conjecture.

## Reviewed bounded results
- Complete result for at most5 coordinates, via a zero-face reduction and exhaustive exact enumeration; also applies when every reduced block has size≤5
- All-dimensional integral root-direction zonotopes
- Bases with laminar integer upper-constraint representations
- Translated sums of coordinate simplices, via tree/unicyclic incidence and explicit exposing weights
- A tight-partition forest criterion and a bounded four-coordinate example refuting a maximal-support shortcut, while satisfying the original opposite-pair conclusion by another pair

No special decomposition is asserted for all bases. The broad bounded conjecture and related Frank/g-polymatroid questions remain unresolved. Read FINAL_RESULT.md only together with SOURCE_SCOPE_CORRECTION.md and review/ADVERSARIAL_REVIEW.md.

## Integrity and controls
The25original author files,4additive correction files and13review files are unchanged. Two C++17 enumerators require assertions enabled; three author Python programs use the standard library. Per-turn counts are preserved rather than merged into an inaccurate total. Independent review adds142,934finite assertions and26ray controls; the author correction has344controls. Witness streams are reproducible but not retained; checksums are not full certificates. Raw source HTML/PDF, imports, binaries and private coordination are excluded.
