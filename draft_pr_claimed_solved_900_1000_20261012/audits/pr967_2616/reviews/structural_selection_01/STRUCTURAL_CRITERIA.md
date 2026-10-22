# Structural selection criteria and exact boundary

Saved UTC: 2026-10-16T20:30:51.387179+00:00

All results below are proved here. No external selection theorem is assumed. N means {0,1,2,…}.

## 1. Finite-to-one formulation for a countable space

For a countably infinite topological space X, the following are equivalent:

(a) There exist pairwise disjoint finite F_n⊂X such that every nonempty open U meets F_n for all sufficiently large n.

(b) There is a finite-to-one function f:X→N such that f(U) is cofinite for every nonempty open U.

Proof of (b)⇒(a): set F_n=f^{-1}({n}). Finite-to-one gives finite, disjoint fibers, and the cofinite image condition is exactly eventual hitting.

Proof of (a)⇒(b): enumerate the points of R=X\⋃_n F_n. If R is infinite attach its nth point to F_n; if it is finite attach its points to finitely many distinct blocks. Denote the resulting finite blocks by E_n. They partition X, and enlarging F_n preserves eventual hitting. Define f(x)=n for x∈E_n. Then each fiber E_n is finite and f(U) is cofinite. Empty early blocks cause no problem. There cannot be infinitely many empty blocks because U=X must be hit eventually. QED.

For comparison, a countably infinite dense partition is equivalent to a coloring c:X→N with c(U)=N for every nonempty open U. This imposes a different fiber-size condition from (b). The equivalences alone do not solve the target: they organize its selection difficulty. The independently constructed ultrafilter group supplies the actual counterexample and verifies every needed condition.

## 2. A general obstruction using a coordinate map

Suppose f:X→N is finite-to-one, p is a free ultrafilter on N, and every A∈p contains the f-image of some nonempty open O_A. Then X has no expansive disjoint finite blocks.

Proof: the point-finite thinning argument in INITIAL_ATTACK.md extracts blocks with disjoint finite images M_k. For E=⋃_{k even}M_k, use E if E∈p and use its complement otherwise. The selected parity opposite this A has all its image outside A, so infinitely many whole blocks miss O_A. QED.

For the Boolean group G=[N]^{<ω} with H_A=[A]^{<ω}, take f(s)=max s for s≠∅ and f(∅)=0. The finite-to-one fibers and open nonempty O_A=H_A\{∅} meet the criterion. Deleting the identity is valid because the group is Hausdorff. The direct subgroup proof in the candidate handles the identity-containing block instead and needs no deletion.

## 3. Exact general-filter characterization

Let F be any proper filter containing the cofinite filter on N. Give G=[N]^{<ω} the group topology with basic identity neighborhoods H_A=[A]^{<ω}, A∈F. Every A∈F is infinite, since a finite A would have its cofinite complement in F. The topology and dense cardinality partition are the same proofs as before; ultrafilter maximality is not needed for them.

Then G has an expansive sequence if and only if N has a partition (Q_k) into nonempty finite sets such that

    for every A∈F, Q_k∩A≠∅ for every sufficiently large k.

Necessity. Start with an expansive disjoint finite-block sequence. Pass finite prefixes to remove empty blocks and the at most one block containing ∅, exactly as in the candidate. Its maximum-coordinate images M_n are finite and nonempty, and each coordinate occurs in only finitely many M_n because the maximum map has finite fibers. Thin to n_0<n_1<… with pairwise disjoint images M_{n_k}. Expansiveness for H_A implies M_{n_k}∩A≠∅ for all sufficiently large k, for every A∈F: take s∈F_{n_k}∩H_A and note max s∈A. Enumerate the coordinates outside ⋃_k M_{n_k}; attach at most one leftover coordinate to each M_{n_k}. This gives a finite nonempty partition Q_k of N, preserves the eventual intersection property, and proves necessity.

Sufficiency. Given Q_k, set

    B_k={s∈G\{∅}: max s∈Q_k}.

These sets are finite (|B_k|=∑_{j∈Q_k}2^j), pairwise disjoint, and cover G\{∅}. Fix any basic open coset x△H_A. For sufficiently large k, Q_k∩A is nonempty. Also, for sufficiently large k, every coordinate in Q_k is greater than max x: only finitely many Q_k meet the finite interval [0,max x]. For x=∅ use max x=-1. Choose j∈Q_k∩A. Then s=x∪{j} has max s=j, so s∈B_k; and s△x={j}∈H_A. Thus B_k meets x△H_A for every sufficiently large k. Every nonempty open set contains a basic open coset, proving expansiveness. QED.

This theorem does not appeal to any named characterization of filters by category. It is a direct deduction from point-finite images and the particular coordinate group topology, so it does not transfer the problem to an unproved selection principle.

## 4. Two checkable extremes

For the cofinite filter, Q_k={k} satisfies the criterion. Explicit expansive blocks are B_k={s≠∅:max s=k}. The group has a countable neighborhood base H_{N\[0,m]}, so ordinary diagonalization succeeds.

For a free ultrafilter p, no such finite partition Q_k can work. Let E=⋃_{k even}Q_k. Exactly one of E,N\E lies in p, and that member misses every Q_k of the opposite parity. This rederives the obstruction independently from the exact general-filter criterion. It uses an arbitrary free ultrafilter and no stronger property.

## 5. Countable π-base boundary

Suppose a space has a countable π-base U_0,U_1,… (every nonempty open set contains some nonempty U_i) and a partition into dense D_n. Choose a finite F_n⊂D_n meeting U_0,…,U_n. Density supplies each choice; reuse of a point within the same F_n is harmless. The F_n are pairwise disjoint because the D_n are, and they eventually hit every nonempty open set. This is a complete positive theorem under an additional hypothesis.

Consequently the ultrafilter example has no countable π-base. In particular it is not metrizable: a countable metrizable space has a countable base formed from balls centered at each of its countably many points with positive rational radii. It is not first countable either: a countable first-countable group has a countable base by translating a countable identity neighborhood base by its countably many elements, and hence a countable π-base. Arbitrary nonmetrizable topology is therefore exactly where the naive countable diagonalization lacks a justified enumeration of the open constraints.

## 6. Point-finite strengthening

The obstruction also excludes an expansive sequence of finite blocks that is merely point-finite: every group element may belong to finitely many blocks, with no common multiplicity bound required. Each finite maximum-coordinate fiber then occurs in only finitely many blocks, so the same disjoint-image thinning and ultrafilter split apply verbatim. Pairwise disjointness is a sufficient special case of point-finiteness. Nested finite exhaustions are not point-finite, so this strengthening does not rule out the elementary eventually hitting sequence obtained from an arbitrary increasing exhaustion of a countable set.

## 7. Route ledger

- Finite-to-one formulation: proved; an exact reformulation, not by itself a resolution. Gap: none in the equivalence; a further mechanism is needed to settle a given space.
- Free-ultrafilter coordinate obstruction: proved; finite fibers permit thinning, ultrafilter dichotomy supplies one open set missing infinitely many blocks. Gap: none for the stated ZFC example.
- Dense cardinality coloring: proved directly for every free filter topology above. Gap: none.
- General-filter finite-partition criterion: proved both directions. Gap: none under the stated countable Boolean group/filter inputs.
- Countable π-base diagonalization: proved with its extra hypothesis. Blocked as a route to the original unrestricted assertion because the example has no such π-base.
- Arbitrary-open simultaneous selection/category shortcut: blocked if it merely assumes an unproved selection statement equivalent to expansiveness. No such theorem is imported or used. No new mechanism found or claimed for this route.

All claims are mathematical deductions. The sole nonconstructive set-theoretic input to the counterexample is existence of a free ultrafilter in ZFC; no finite experiment certifies that input. The report's source-lineage and priority observations are outside this family's verified result.
