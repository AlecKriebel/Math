# Literal obstructions and the unresolved formulation

**4600032 / AMR-045-0032. One substantive author turn, 1/5. Formulation hold; no repaired research theorem claimed solved.**

## 1. The exact imported sentence is false

For any integer N≥2, take an alphabet A of size N+1 and let

\[
S=\{a^\infty:a\in A\}\subset A^{\mathbb N_0}.
\]

This is a one-sided shift of finite type: forbid every adjacent pair ab with a≠b. Equivalently, its edge presentation has adjacency matrix I_(N+1), consisting of N+1 disjoint loops. Thus S is a nonempty compact shift-invariant set and is admissible under the primary definitions. No mixing hypothesis on S appears in the imported record or printed Question 20.2.

The shift map on S is the identity. In particular every point has exactly one preimage under the shift restricted to S, so the asserted bound of at most N preimages holds. For each length k≥1, the allowed words are exactly the N+1 constant words a^k. Consequently

\[
h(S)=\lim_{k\to\infty}\frac1k\log(N+1)=0<\log N.
\]

Suppose an injective map f:S→{1,...,N}^{N_0} commuted with the shifts. For each x∈S,

\[
\sigma(f(x))=f(\sigma x)=f(x).
\]

So f(x) is a fixed point of the full N-shift. Those fixed points are exactly its N constant sequences. Injectivity would map N+1 distinct points into N points, which is impossible. Continuity is not even needed for this contradiction, so it excludes in particular a topological conjugacy onto a subshift.

The smallest example is N=2 and S={0^infinity,1^infinity,2^infinity}. This is an elementary instance of the classical necessary periodic-orbit capacity condition explicitly present immediately above the question in the primary source. It is not presented as a new dynamical obstruction.

## 2. The opposite printed direction also cannot hold

The primary PDF p.21 instead asks for the full shift T to be isomorphic to a subshift of S, under h(S)<h(T). Entropy is invariant under topological conjugacy and does not increase on a subsystem, so this would give h(T)≤h(S), a contradiction. Even without entropy theory, the finite S above gives a direct counterexample to that printed direction: an infinite full shift on N≥2 symbols cannot inject into a set of N+1 points.

The forward direction in the imported record is a plausible directional correction, and a 2013 workshop report of Boyle's question uses that direction. Correcting the direction alone does not remove the fixed-point example in §1.

## 3. What additional conditions would remove this example?

An injective equivariant map preserves the least period of every periodic point. Indeed, if x has least period n, its image has some period dividing n; if its least period were d<n, then f(shift^d x)=f(x) would force shift^d x=x, a contradiction. Distinct periodic orbits also have distinct image orbits. Hence every embedding necessarily satisfies

\[
|O_n(S)|\le |O_n(T)|\qquad(n\ge1),
\]

where O_n denotes the set of orbits of least period n. For the example in §1, the condition already fails at n=1. This necessary condition is classical and is stated in the same source's preceding account of Krieger's two-sided theorem.

Similarly, for an embedding f and x∈S, the map y↦f(y) injects the one-step preimages of x in S into the one-step preimages of f(x) in T. Thus the target has at least as many such preimages, not at most as many. This observation explains a further reversed comparison in the printed surrounding paragraph, but does not determine a complete corrected hypothesis.

We do **not** assert sufficiency of entropy, periodic capacity, and the one-step preimage bound in the one-sided category. We do not assume that adding just those conditions is the author's intended correction. A repaired statement must first be grounded in a clear primary source; the available 2008 and 2013 presentations do not supply an unambiguous complete repair in the special-case question itself.

## 4. Exact remaining issue

The imported unqualified assertion and the opposite printed conclusion are both rejected by standard necessary conditions. The meaningful unresolved issue is the intended one-sided embedding problem after its hypotheses and direction are fixed. The broader adjacent Problem 20.1 is not solved. This is therefore a formulation-hold packet, not a claimed solution to a longstanding embedding theorem and not an exhausted 5/5 proof attempt.
