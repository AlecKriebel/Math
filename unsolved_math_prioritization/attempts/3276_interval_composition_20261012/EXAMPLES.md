# Small examples and the recursive separation family

These examples illustrate the exact theorems; they are not unrestricted finite-search evidence.

## Positive return cycles matter

Let Q be a directed three-cycle with every arc red. Put any nonempty factors into its three vertices. Every quotient vertex is a source and lies on a positive red return cycle. Therefore every vertex in the substitution is a source, regardless of internal source sets. In particular, a cyclic-rainbow triangle used as one factor has no internal source, but its vertices gain red paths to each other through the two other quotient blocks. This expanded example contains a cyclic rainbow triangle internally, so it is not a rainbow-free counterexample to the target.

For a singleton quotient there is no positive return cycle. Substitution gives the original sole factor and its original source set. Treating a length-zero self-path as a return cycle would incorrectly make every vertex of a transitive three-vertex factor a source. With all its forward arcs red, the factor has exactly source 0.

## Direction-only modules are insufficient

Take the four-vertex tournament with arcs 0→1 red, 0→2 red, 1→2 blue, 2→3 red, 3→0 red and 3→1 red. The block {0,1} is direction-uniform toward each outside vertex, but its two arcs to 2 have different colors. There is no directed cyclic rainbow triangle. Its source set is exactly {0,2,3}; vertex 1 is not a source.

Keeping representative 0 gives a monochromatic cyclic quotient on {0,2,3}. An invalid direction-only application of the exact colored-substitution formula would add vertex 1 as a source. This is why both direction and color uniformity are required.

## Local intervals require actual local arcs

Let 0→1→2 be a red path and let 2→0 be blue. Globally 0 reaches 2 in red, but inside {0,2} it does not. A global virtual red relation 0→2 cannot serve as an actual red edge of the restricted interval. The possible-arc graph must be built from actual arc domains, while virtual relations are used only for global consequence tests.

## Arbitrarily large surviving whole cores

For depth d>=1, form the recursive substitution tree whose quotient at level ell is a monochromatic directed three-cycle colored ell modulo three; its leaves are singletons. Its order is 3^d. Every internal quotient has empty incidence core. Exact rainbow transfer makes the root cyclic-rainbow-free, and the quotient-return formula makes every vertex a source.

At depth at least three, every vertex has an incoming and an outgoing sibling block at levels of each color. Thus every vertex has all three incoming and outgoing colors, no first deletion is possible, and the whole incidence core is the entire 3^d-vertex tournament. The displayed depths one through four have orders 3, 9, 27 and 81 and whole-core sizes 0, 0, 27 and 81. The proof extends to every finite depth, so the recursive empty-quotient-core criterion covers arbitrarily large whole cores. This separates that criterion from any fixed whole-core-size sufficient bound, without a claim about the strongest known literature classes.
