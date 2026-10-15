# Independent source interpretation before frozen-proof review

Recorded: 2026-10-12T16:40:39.248651+00:00
Reviewer: /root/pr462_source_admissibility
Problem: 30005528 / OWR-13750333-009
Review completion estimate: 20% (source scope fixed; frozen proof not yet read).

## Independence record

I read the repository AGENTS.md, the PDF skill, and the original official EMS report PDF at https://ems.press/content/serial-article-files/47016 (DOI 10.4171/OWR/2023/22). I visually inspected complete PDF pages 59-61 (printed pages 1253-1255), and locally extracted those pages for private verification. I have not read the frozen PROOF.md, SOURCE_GATE.md, any historical audit, or any peer report as of this record. The related DOI resolver failed; no related-source content was obtained before this record.

## Exact target and formal reading

The target is Question 1 in Felipe Goncalves's Linear domino size problem, under Problem session, printed p. 1254. Definition 1 supplies the formal model: a triple (Sigma,T,s), with T a set of ordered pairs of symbols, and an infinite one-sided sequence of legal tiles [a_i,b_i] satisfying b_i=a_(i+1). Question 1 asks for an infinite compact topological Sigma and continuous s:Sigma->R_+ for which each periodic legal sequence w has A(w)>inf_omega A(omega), where the infimum is over all legal infinite sequences.

The printed average is precisely A(w)=limsup_(N->infinity) [s(a_1)+sum_(i=1)^N s(b_i)]/N. It counts N+1 vertex occurrences for N tiles. For a compact alphabet with continuous finite real s, s is bounded and the initial contribution vanishes, so it is equivalent to the limsup average of the successive symbols. For a legal period-q vertex/tile cycle the average is the mean of q symbol sizes, including wrap-around legality.

The source does not separately define periodicity. The ordinary reading is periodicity of the infinite tile sequence: a positive integer q with [a_(i+q),b_(i+q)]=[a_i,b_i] for every i. Compatibility makes this equivalent to periodicity of the associated vertex sequence. For a deterministic graph (x,f(x)), this means f^q(x)=x, not merely recurrence or approximate return. Eventual periodicity has the same asymptotic average as its periodic tail, but the source states periodic, not eventual periodic.

## Stated assumptions and absent restrictions

- Sigma must be infinite and compact. No metric or Hausdorff axiom is stated; a compact metric example would satisfy a stronger condition.
- The size function must be continuous with codomain R_+. The notation could mean strictly positive or nonnegative reals; a verified example should use strictly positive sizes to cover both conventions.
- Tiles are ordered pairs. No reversal symmetry, undirectedness, connectivity, ability to continue from every symbol, or realization as Euclidean intervals is required by Definition 1 or Question 1.
- No closedness or compactness of T is explicitly required. However, Example 3's compactification discussion implicitly inserts the limit tile [1,1]. A strongest-scope example should have closed T and should not depend on omitting limiting legal edges.
- The source does not require periodic legal sequences to exist. A nonvacuous example with at least one legal periodic sequence would remove that interpretive vulnerability.
- The displayed strict inequality only excludes periodic attainment; it does not by itself assert that the infimum is attained. The following explanatory prose calls minimizers nonperiodic. An attained nonperiodic minimum would satisfy both readings.
- Remark 4 is a motivating packing-density question after Question 1; it says a generic version reduces to Question 1. It is not part of the definition and supplies no geometric restriction on arbitrary (Sigma,T,s). In particular, Question 1 does not require distances to come from {0,1,e,pi} union [100,infinity), tiling by positive-length intervals, or an isometric/geometric realization.

## Falsifiable success criteria for this review

Check infinity and compactness explicitly; continuity and strict positivity of sizes; exact average normalization; all legal sequences classified; complete periodic-point classification, including possible seam/limit points; existence of both aperiodic minimizing sequences and periodic legal sequences; strict size gap for every periodic sequence; and closedness of T if claimed. Separate this general-symbolic result from the motivating geometric packing question and any more constrained later conjecture.

## Boundary risks fixed before proof access

Potential circularity arises if periodicity is merely asserted from irrational rotation without considering every alphabet component and transition. A disjoint topology can make a piecewise constant size continuous, but must be established explicitly. A compactification can add lower-cost periodic cycles; all limit points and graph closure must be checked. If a later source requires symmetric tiles, a connected alphabet, size equal to a physical length, all pairwise distance constraints, or a genuine interval-packing realization, those are a different admissibility test. Reversal symmetry would be particularly consequential because any permitted ordered edge could then yield a period-two cycle. None of these extra restrictions is stated in the original Question 1.
