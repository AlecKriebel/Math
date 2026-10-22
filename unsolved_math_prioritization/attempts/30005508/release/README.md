# Projective characters and square roots in real blocks

**Problem:** 30005508 / OWR-13750328-013, queue rank 489.  
**Assessment date:** 3 October 2026.  
**Status:** Unresolved after five substantive approaches. No general proof or counterexample is claimed. No novelty claim is made for the reductions or examples below.

Let B be a real nonprincipal 2-block with defect pair (D,E). Let (x,b) be a B-subsection with defect pair (C_D(x),C_E(x)) and one projective indecomposable character Φ. The question is whether, for every y²=x,

[Res^{C_G(x)}_{C_G(y)} Φ,1] = |y^{C_G(x)} ∩ (E\D)|.

## Main findings

1. The statement is genuinely conjectural in the source. The published orbit-by-orbit involution conjecture is stronger than a scalar Frobenius–Schur indicator identity. Results about the latter do not by themselves establish this problem.
2. The square-root extension reduces to that involution conjecture on central quotients. For H=C_G(x), Z=⟨x⟩ and x≠1, both sides are t times their involution-case counterparts in H/Z, where t is either 1 or 2. The factor need not be 1. A full proof appears in [Approach 2](turn_02.md).
3. The formula holds throughout the standard family C₃⋊E realizing every index-two pair of 2-groups D<E. This does not prove it for every block with that defect pair. See [Approach 3](turn_03.md).
4. The assertion is stable under direct products with arbitrary 2-groups. See [Approach 4](turn_04.md).
5. An explicit nonnilpotent one-simple-module block of a group of order 864 satisfies every involution-orbit test. Its two nonzero multiplicities are 2 and 6. The example is proved and checked in [Approach 5](turn_05.md).

The exact remaining obstacle is the general involution-orbit multiplicity statement, even at x=1. An aggregate sum of these multiplicities cannot determine each summand.

## Files and checks

- [Source and prior-attempt gate](SOURCE_GATE.md)
- [Approach 1: orbit modules and zero cases](turn_01.md)
- [Approach 2: central-quotient reduction](turn_02.md)
- [Approach 3: all-pair model family](turn_03.md)
- [Approach 4: direct-product transfer](turn_04.md)
- [Approach 5: nonnilpotent block](turn_05.md)
- [Research log](RESEARCH_LOG.md)
- [Exact check program](check_exact.py) and [recorded results](exact_results.json)

Run `python3 check_exact.py`. It uses only the Python standard library and exact integers/rational numbers. It checks the six involution classes of the explicit order-864 group and quotient fibers with both possible multipliers. It is not an exhaustive search over finite groups and does not certify the general conjecture.
