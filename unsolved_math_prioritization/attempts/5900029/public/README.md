# Finite total scalar curvature and planarity

**Status: unsolved.** This is an AI-assisted, unrefereed investigation of
UnsolvedMath 5900029 / AMR-058-0029, the question attributed to Helen Moore
in Sullivan and Morgan's 1996 collection, Problem 29.

Five distinct routes were investigated. None proves the complete rigidity
statement or supplies a counterexample satisfying all its hypotheses.

The source normalization is important: for a minimal real k-dimensional
submanifold of Euclidean space the relevant quantity is

    T(M) = integral_M |A|^k dV = integral_M (-Scal)^(k/2) dV,

not the signed integral of scalar curvature. The intended global question
concerns complete, smooth, boundaryless submanifolds; connectedness is used
when the conclusion is a single affine plane. Throughout the proof notes,
area minimization means minimization against compactly supported competitors
as an oriented integral current, so it implies normal stability.

What this packet establishes or records:

- The hypersurface case is a credited prior theorem of Shen and Zhu (1998).
- Anderson's one-end theorem gives a second credited special case for k >= 3.
- An explicit compactly supported instability argument excludes ordinary
  catenoids. The application of Moore's two-end classification is recorded
  separately, with its source/proof-audit limitation.
- Calibrated intersecting plane cones show why a tangent-cone argument needs
  more than dimension counting and area minimization of the limit.
- A normal-translation second-variation calculation cancels exactly and
  does not produce the scalar stability estimate one might hope for.
- A complete calibrated parabola supplies the excluded equality case, while
  every nonflat Euclidean-product version has infinite critical curvature.
- Critical-energy scaling and a small-energy argument explain why finite
  energy alone does not supply a global smallness hypothesis.

See [PROOF.md](PROOF.md) for the mathematical statements and exact gaps,
[SOURCE_GATE.md](SOURCE_GATE.md) for source qualifications, and
[ATTEMPT_LOG.md](ATTEMPT_LOG.md) for the five routes.

Run `python3 verify.py` for finite exact algebraic checks. Those checks do not
verify the cited geometric theorems, replace the written arguments, or settle
the open target. No novelty or priority is claimed. No source PDF, source
full text, or dataset contents are included.
