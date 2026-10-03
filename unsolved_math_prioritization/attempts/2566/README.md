# Odd-prime maximal subgroups and normal intersections

Problem: [UnsolvedMath 2566 / KOU-21.57](https://www.unsolvedmath.com/problems/2566), proposed by W. Guo and D. O. Revin in the 2026 Kourovka Notebook, printed page 185.

**Outcome: unresolved after five substantive attempts.** These AI-assisted, unrefereed notes contain reductions and positive subcases, not a solution of the full problem. No historical novelty or priority is claimed. A fresh independent AI audit found no blocking defect in the partial deductions; this is not peer review and does not settle the original problem.

The question concerns a complete class X consisting of finite odd-order groups. Given an X-maximal H≤G and N normal in G, must H∩N be X-maximal in N? Here maximal means maximal by inclusion among subgroups belonging to X.

## Deductions retained for review

1. By the odd-order theorem and extension closure, X is the class of all finite pi-groups for a set pi of odd primes. One may replace G by HN. Hall theory proves the assertion if N is solvable, or if H is pi-Hall in HN.
2. Quotienting by a solvable normal subgroup R≤N preserves both H's pi-maximality and the success/failure of the target intersection. A smallest counterexample can be chosen with Rad(G)=Rad(N)=1 and C_G(N)=1.
3. For N a direct product of nonabelian simple factors, H∩N splits as the product of its projections. Any failure then induces an almost-simple counterexample on one factor. In particular, such N satisfies the assertion if every factor has pi'-outer automorphism group, even when H permutes the factors.
4. The established Wielandt–Hartley normalizer theorem implies that no proper nilpotent pi-overgroup of H∩N can exist. A small odd Frobenius group shows why the normalizer condition alone does not finish the proof.
5. The target is equivalent to a fixed point for H/(H∩N) on the maximal pi-overgroups of H∩N in N. A failure under an odd quotient requires at least three such overgroups. Published minimal-simple classification gives further positive cases, and the earlier lifting lemmas extend them through solvable radicals and direct products.

The remaining gap involves genuinely odd outer actions on non-minimal simple groups and radical-free normal groups with layers above their socles. No invariant-overgroup theorem covering those cases and no actual odd-prime counterexample were obtained.

## Exact controls

Run `python verify_controls.py` using Python 3, with no third-party packages.

- Reproduces the known even-prime PGL₂(7)/PSL₂(7) example: H has order 16; H∩N has order 8 and lies in two pi-maximal subgroups of order 24; the outer quotient exchanges them. Each of the 320 elements outside H generates the full group of order 336 together with H.
- Checks N_B(A)=A for a subgroup A of order 3 in C₇⋊C₃ of order 21. This is a control against an invalid normalizer-only argument, not an instance of the target normal-intersection construction.

Neither control is an odd-prime counterexample to KOU-21.57. Finite checks do not establish the general lemmas, the published classification, or novelty.

## Files

- `turn_01.md` through `turn_05.md`: complete attempts and explicit gaps
- `RESEARCH_LOG.md`: substantive-attempt accounting
- `SOURCE_GATE.md`: statement and primary-literature scope
- `verify_controls.py`, `control_results.json`, `verification.json`: exact checks and their limits

## Independent review and reproduction

The full [independent audit](audit/INDEPENDENT_AUDIT.md) and separately written matrix-model checker are included. Run `python run_checks.py` to replay both controls and compare their stored results. [Terminology clarifications](PUBLICATION_NOTE.md) fix the meanings of “fixed-point-free” and the small-prime-intersection boundary case without changing any proof claim.
