# Infinite-order conjugacy classes in profinite groups

## Status: unresolved after five substantive proof attempts

This is an AI-assisted, unrefereed research package for Kourovka Notebook
Problem 21.136, catalogue ID 2645. It does not resolve the general problem and
makes no novelty claim. The full statement asks whether a profinite group with
fewer than continuum many conjugacy classes of infinite-order elements must be
torsion. The problem is attributed to John S. Wilson.

The principal restricted result established in the written attempts is:

> If such a group has a closed normal soluble subgroup of finite derived length
> with torsion quotient, then the whole group is torsion.

The proof uses an exact description of conjugacy fusion among generators of a
closed subgroup isomorphic to Z_p. It is included in full. It does not cover all
prosoluble groups, since their derived length can be unbounded.

- Attempt 1: countably based quotient reduction and the finite-generation gap.
- Attempt 2: normalizer action and an exact fusion-index formula.
- Attempt 3: the abelian-by-torsion lemma and finite-derived-length induction.
- Attempt 4: an affine counterexample candidate, its failure, and exact controls.
- Attempt 5: the class-space topology and a single-orbit non-torsion coset
  reduction.

The central obstacles are fusion under infinite-index closed normalizers and
the unproved exclusion of an open coset whose nonempty infinite-order locus
lies in one global conjugacy class. The few-classes hypothesis has not been
shown to pass to the relevant closed normalizers.

Ten small finite affine groups were checked exactly, with all assertions
passing. Run `python3 checks/affine_controls.py` using the Python standard
library. The script validates formulas for those finite controls. It does not
prove the infinite-group results or resolve the general problem.

Source references and scope limits are in SOURCES.md. No third-party source PDF,
source screenshot, or source corpus is included. An [independent adversarial review](audit/INDEPENDENT_AUDIT.md)
passed the complete package as unresolved partial results. The original frozen
package is preserved in frozen_original/. Two nonblocking wording clarifications
are listed in CHANGE_MAP.json.

For a portable integrity and independent-check replay, run
`python3 verify_package.py` from any working directory. The full mathematical
audit and its independent permutation-action controls are included in audit/.
