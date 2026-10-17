# Kourovka 21.144

Checkpoint: 2026-10-17T21:06:09.333273+00:00. Status: **unsolved** after distinct dynamics, algebraic and counterexample approaches. Both a complete proof and a valid counterexample remain absent. Discovery estimate: **8%**; this is not a probability of correctness. The attempt record and its scoped audits are complete.

## Exact statement and current priority

Brin–Sapir conjecture, official 21st edition, 6 October 2026 update, printed p. 198: every subgroup of Thompson’s group F is elementary amenable or contains a subgroup isomorphic to F. All subgroups are quantified; directed-union closure of elementary amenability reduces the assertion to finitely generated subgroups. The checked official Notebook and newer proposer list still treat the conjecture as open. Recent proofs that ambient F is nonamenable do not resolve this subgroup statement. See priority_20261017.md for precise primary sources and access limits.

## Strongest reviewed deductions and failed families

1. For an F-free subgroup, the two endpoint-germ kernels on every group orbital agree. In a finitely generated group the joint endpoint quotient is free abelian and its kernel consists of elements supported away from all orbital endpoints. Any hypothetical finitely generated counterexample therefore has infinite descent through actual finitely generated nonEA, F-free subgroups with compactly nested supports. No justified well-founded decrease has been found; shrinking supports alone is no contradiction.
2. Brin endpoint imbalance detects a copy of F. Transition chains, infinite towers and nonsolvability alone do not: the Brin–Navas group B is nonsolvable and elementary amenable. Published ordinal/fast-system classifications cover a restricted class. The transformations needed to cover arbitrary F-free generators remain conjectural.
3. Residually finite PL subgroups are solvable. Residually solvable PL subgroups are locally solvable and elementary amenable, with solvability for finitely generated inputs. The latter follows from the standard base-inclusion wreath limit L inside B and the nontrivial perfect subgroup L-prime. Root checked the coordinate commutator calculation; independent agents checked the exact source orientation and hypotheses. These deductions eliminate those proposed counterexample families. They do not eliminate residual elementary amenability: EA perfect subgroups exist here.
4. Infinite diagonal actions on invariant cells fail finite-breakpoint membership; finite-active EA coordinates and EA permutation extensions stay EA. Full subdirect subgroups of finite powers of F already contain F. Groups with no F form a closed set in each fixed-rank marked-group space, but a marked limit need not embed in F. A separate finite dyadic realization is essential and has not been constructed.
5. No nonsplit PL extension mapping onto F and avoiding every F copy has been found. A copy in an orbital quotient cannot be lifted without an argument. Cutting at a nondyadic fixed point can leave F; an exact dyadic PL map with fixed point 7/24 is preserved as a boundary-case certificate.

## Verification

The dynamics deductions and construction filters received independent internal adversarial checks. Root read their proofs and reproduced verify_counterexample_filters.py: the standard F presentation certificate passes with noncommuting generators, the commuting pair is rejected, and the diagonal examples have 3N+1 breaks for the six recorded N values. These finite checks supplement the general arguments, not a bounded-search claim about the conjecture. Source notes distinguish actual group orbitals from element orbitals, arbitrary PL maps from finite dyadic maps, and subgroup conclusions from quotient conclusions.

AI tools were used extensively. No independent human peer review, formal proof-assistant verification, historical novelty, or full solution is claimed for these partial deductions. No Zenodo upload or tracker row was made for this problem.

## Exact remaining gap

A positive answer needs a mechanism forcing arbitrary F-free finite generators into elementary amenable structure; known germ recursion does not supply the missing well-founded rank. A negative answer needs an explicit nonelementary-amenable, F-free subgroup with finite dyadic generators; abstract residual certificates, marked limits and infinite-piece actions do not supply membership. Reopen blocked routes only with a new mechanism or evidence. Continue descending to 21.143.
