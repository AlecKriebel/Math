# Rank 697 / 30001599: alpha bounds for uniform fat-point schemes

Status: five substantive approaches completed; full target unresolved. This is a partial-results and obstruction package, not a solution or a novelty claim. A fresh independent audit is required before any remote publication.

The target is the numerical Harbourne--Huneke inequality at the symbolic exponent n(r-1)+1, not an assertion about general points only and not a symbolic-power containment. The supporting OWR source is the 2010 report, printed p. 2626. Its short statement does not specify the field; the direct Cooper--Hartke follow-up works over an algebraically closed field of characteristic zero. All nontrivial authored arguments here explicitly use that scope unless stated otherwise.

## Contents

- PROOFS.md: exact formulation, proved partials, and the precise unresolved gap.
- APPROACH_LOG.md: five distinct substantive attempts and limitations.
- SOURCE_VERIFICATION.json: public source and repository verification metadata only.
- check_controls.py: dependency-free exact arithmetic and interpolation controls.
- control_results.json: reproducible output.
- LIMITATIONS.md: source, proof, computation, and publication boundaries.
- MANIFEST.json: SHA-256 and byte counts of the frozen safe files.

Run `python3 check_controls.py` from this folder. The script overwrites control_results.json with deterministic output.

## Main takeaways

1. Differentiation falls short of the target by exactly (r-1)(alpha(I)-1).
2. The Chudnovsky asymptotic bound has an explicit, nonvanishing finite-exponent deficit; replacing the target with that bound loses information.
3. A complete hyperplane-peeling argument recovers equality for point star configurations in every projective dimension in characteristic zero. This family was already known; the proof here is authored independently for verification.
4. Equal Hilbert functions of reduced supports do not determine higher symbolic initial degrees: the supplied six-point configurations have the same function (1,3,6,6,...) but alpha(I^(3)) equal to 7 and 8.
5. In the plane, a squarefree curve cannot witness a failure for r>=3; the remaining issue includes how repeated irreducible components distribute multiplicities.

The 2014 Cooper--Hartke paper already handles the original report's staircase line-count family for every r>=1. That update is not a resolution of arbitrary point configurations. Recent work about generic/very general points and Demailly bounds likewise does not discharge the full target.
