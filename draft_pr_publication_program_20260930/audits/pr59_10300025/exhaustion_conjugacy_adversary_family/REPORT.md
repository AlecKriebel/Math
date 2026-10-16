# Independent adversarial review of PR59 / 10300025

**Verdict: PASS for the literal common-conjugacy, per-element additive-distance condition.** No essential mathematical repair is needed in the supplied KNOWN_RESULT.md, SHA256 3cf3b548da6d0fbddd0577f02b7cfae056e30bee44ca0af2ba967d304c2fdbb8, from ROOT's original intake at head bdee508c676c98cb96dbc1a2e5aef2fe9cd1c744. The credited already_solved/source-clarification classification is supported. This review does not justify a new-solution announcement, a paper, or a resolution of an unidentified stronger geometric question.

## Independence and mechanism

I read the literal source_record and policy first, then developed and saved INITIAL_SCOPE_AND_ARGUMENT.md before reading the candidate proof, old review, author checker, or other reviewer argument. My mechanism is asymmetric nested intervals with forward/inverse endpoint barriers. After reading the candidate, I found that it independently uses the same broad compact-exhaustion mechanism in symmetric form. This overlap is disclosed; it is not a newly distinct mathematical mechanism relative to the author. No new author or historical program replay is credited as independence, and no other fresh reviewer argument was read.

PROOF.md supplies a complete universal derivation for any countable family in Homeo(R), both orientations, with one coordinate h. Its explicit bounds are |h g_i h^(-1)(t)-epsilon_i t|<=2i+1 and additive two-point error <=4i+2. Those slightly tighter indexing bounds apply to my recursion; they do not require changing the candidate's valid weaker bounds. No finite computation is needed for the theorem.

## Adversarial checks

- Countability: each stage has only finitely many compact images/inverse images; no infinite maximum or hidden common local bound is assumed. A single completed enumeration determines h before an element is fixed. Finite images, repetitions, identity, and nonfaithful actions are harmless.
- Topology: both endpoint sequences escape to infinity; interpolation covers the entire line, is continuous and strictly increasing, and has a continuous global inverse. There is no collapsed orbit, atomic CDF, missing gap, finite accumulation of knots, or incomplete coordinate.
- Inverses: their image containment supplies the inner endpoint barriers. Dropping it controls escape in one direction only and fails on contraction examples.
- Orientation: decreasing maps require comparison to -t. The four endpoint inequalities explicitly cover both ends; the n=i=1 zero boundary is covered by strict inverse containment.
- Quantifiers: the distance bound holds for every point pair after the same h. Constants may depend on the element; the theorem supplies no group-uniform bound. Conjugation preserves group composition and inverses automatically.
- Measures and weights: this proof requires none. A finite probability sum has bounded CDF range and cannot by itself supply a coordinate onto R; an additional reparameterization does not automatically preserve additive bounds. An unrelated measure argument would need its own atom/full-support/local-finiteness/bi-infinite-mass and displacement estimates.
- Geometry: no coarse control relative to the old coordinate or ambient leaf metric, leaf-distance conclusion, or simultaneous Lipschitz conclusion is deduced from this construction.

The candidate's finite-generator maximum-envelope proof is also valid: a finite maximum is continuous, strictly increasing and onto; the added translation gives no fixed point and escaping iterates. Symmetric generators give F^(-1)(x)<=s(x)<=F(x), one conjugacy sends F to unit translation, and word displacement bounds add. Its positive C at identity and reduction to the displayed distance inequality are correct.

## Fresh actual controls

The own controls import no author or prior reviewer helpers. Actual operator PID 91902 launched child 91903 at 2026-10-03 16:46:27.734957 UTC and completed at 16:46:28.227817 UTC, exit 0. Child's internal interval was 16:46:27.780933–16:46:28.222596 UTC. Literal argv, complete prelaunch proof/code/operator/initial-plan bodies, full stdout and empty stderr are preserved in actual_controls/. Source SHA is 4e8d73f730880f2fbc43f043d9e50bf3a9257062e3082d4c6c89220b4e62e630; stdout SHA is 79fa05474f46ded689001fe32277c403b221d97489aaddef1b1cb5e95f40838b.

There are 5,185 exact rational assertions on 10 maps and 18 asymmetric exhaustion levels, including 536 basic PL-constructor checks. The substantive interval certificates cover 10 complete finite compact cores and 230 complete finite annuli: every breakpoint of the signed displacement is checked, so each certified finite interval is covered throughout, not merely at sampled points. Other checks cover image/inverse containment, signs, inverse identities, two-point reductions, and common-coordinate composition. Maps include noncommuting pieces, strong contraction, unequal slopes, offsets, identity, reflection, and general orientation reversal.

Three broken variants have explicit exact witnesses: forward-only error 20 exceeds the claimed tail bound 2; a reflection compared with +t gives error 80 instead of 0; separate coordinates turn the dilation/translation relation's value at 0 into 5 instead of 2. The probability-CDF diagnostic checks a finite geometric partial sum; its bounded-range conclusion is a mathematical fact about total probability mass, not a numerical test of arbitrary measures. Finite orbit-growth checks support the separate universal proof that a cyclic dilation cannot have a group-uniform error under any conjugacy.

The finite PL h in the checker is a truncated diagnostic coordinate. It is not asserted to satisfy the global theorem outside the certified intervals. Arbitrary nonlinear maps, every real point, and infinitely many group elements are covered by PROOF.md's compactness and monotonicity argument. These counts are neither response budgets nor formal verification. Prelaunch files were mode 0644; the prepared packet later freezes their logical bytes at 0444, with both states disclosed.

## Primary scope and bounded priority

Calegari's [2002 Q8.2](https://arxiv.org/html/math/0209081) gives the per-element inequality and separately discusses a constant independent of the element. Its toroidal remark conflicts with the unrestricted topological reading; it supplies no explicit alternative geometric hypothesis. The [2000 paper](https://msp.org/gt/2000/4-1/gt-v4-n1-p17-p.pdf), §1.1 and Q5.3.19, has closed co-oriented context and likewise allows choosing a parameterization and a separate bound per element. These exact local passages were read; the entire papers were not reviewed.

[Deroin–Kleptsyn–Navas–Parwani, Theorem 8.5](https://arxiv.org/html/1103.1650v3), provides the stronger finitely generated increasing bounded-displacement/Lipschitz conclusion. Its irreducibility condition is removed for the application by adding two irrationally related translations, as its proof paragraph does, and restricting the resulting conjugacy. I read the theorem, irreducibility definition, Proposition 8.4, and adjoining-translations proof paragraph, not the entire stochastic dependency chain. This verifies the credited literature implication; it is not an exhaustive priority audit of the general countable extension or a claim that the authors explicitly answered Calegari.

Usual second-countable 3-manifolds have countable fundamental group, so the universal theorem applies to the stated leaf-line action. The original closed co-oriented setting is also covered by the credited finitely generated theorem. The toroidal interpretation gap remains explicitly outside the verified mathematical conclusion and must remain in any operative summary.

## Historical and administrative limits

Read the SOURCE packet's existing accounting receipt rather than re-running raw/SQL accounting: it records a present JSON-object report and non-NULL SQL TEXT report, with semantic equality. The original attempt records already_solved, one conservative known-result validation turn of five, and no discovery credit. Those are inherited SOURCE accounting facts; this family does not freshly authenticate the raw corpus, Git/API head, or native queue. This fresh review is a separate verification activity. No counter was incremented, reset, or inferred from the 5,185 diagnostics.

No original-source, candidate, Git, queue/native, remote, publication, or approval state was changed. This is independent AI review, not human peer review or a formal proof certificate. ROOT custody/acceptance and any later merge are unperformed by this family. Review completion estimate: 100% for the literal mathematical scope; historical geometric intent remains unresolved rather than counted as solved.
