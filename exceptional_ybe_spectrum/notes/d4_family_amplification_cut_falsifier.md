# Numerical cut test for amplified \(d=4\) family points

**Date:** 2026-07-29

**Status:** numerical falsifier only; no nonexistence theorem

## Question

Claim C40 rules out a codimension-two square-invariant local subspace of
the identity amplification of the published \(d=4\) witness. The exact
color/face circle in C15 contains other matrix representatives, so that
proof does not automatically exclude the same mechanism for every point
on the circle.

For three exact parameter values

\[
(s,t)=(1,0),\qquad
(0,1/\sqrt2),\qquad
(1/\sqrt2,1/2),
\]

this experiment amplified \(H_4(s,t)\) to local dimension eight and
searched for a rank-six projection \(Q\) satisfying

\[
[H_4(s,t)\boxtimes I_2,Q\otimes Q]=0.
\tag{1}
\]

Such a \(Q\) would restrict the amplified solution to a \(d=6\)
exceptional solution.

## Protocol and outcome

The first predeclared protocol requested 24 runs of 2000 iterations. It
was interrupted during its second seed after the first run required
54.4 seconds. That completed seed ended at normalized squared
commutator \(0.2272990108834362\); the interruption and its output are
retained rather than silently discarded.

A reduced protocol was declared before further evaluation: four new
seeds at each of the three family points, with 400 iterations per seed.
All twelve runs ended at

\[
0.22729901088344
\]

to the displayed precision, with tangent-gradient norms between
\(8.1\cdot10^{-10}\) and \(1.2\cdot10^{-8}\). No candidate satisfying
(1) appeared.

The agreement across all three exact family points suggests that these
points may share the same amplification-cut landscape under a natural
equivalence. That interpretation is not proved here. In particular:

- optimizer convergence does not prove a global lower bound;
- the common decimal has not been recognized as an exact algebraic
  value;
- the test covers only three points of the known \(d=4\) circle;
- it says nothing about amplifications of arbitrary \(d=4\) solutions.

Thus the result is useful only as a construction falsifier and as a
target for a possible exact extension of C40.

## Replay

The retained script reconstructs each family point, verifies its
involution and cubic identities, performs the site-factor amplification,
and imports the previously audited Grassmann objective and gradient:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/search_d6_cut_from_color_face_d4.py \
  --point axis_s --seed-start 26074301 --runs 4 \
  --maximum-iterations 400 \
  --output-jsonl results/d6_cut_from_color_face_d4_axis_s_reduced_runs.jsonl
```

The corresponding `axis_t` and `interior` commands and all parameters
are recorded in the reduced seed manifest.
