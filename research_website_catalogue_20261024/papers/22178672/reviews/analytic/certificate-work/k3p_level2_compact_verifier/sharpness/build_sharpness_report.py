#!/usr/bin/env python3
"""Build the reader-facing sharpness report and a hash manifest."""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import os
import sys


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
KPATH = HERE / "K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json"
TPATH = HERE / "K3P_SHARPNESS_TOPOLOGY_ALL_N_CERTIFICATE.json"
REPORT = HERE / "K3P_SHARPNESS_KRAWCZYK_REPORT.md"
MANIFEST = HERE / "K3P_SHARPNESS_REPLAY_MANIFEST.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def scientific(value: str, digits: int = 8) -> str:
    x = Q(value)
    with localcontext() as ctx:
        ctx.prec = digits + 12
        d = Decimal(x.numerator) / Decimal(x.denominator)
        return f"{d:.{digits}E}"


def atomic_text(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def exact_min(summary: dict[str, object], category: str) -> tuple[str, str]:
    item = summary["minimum_by_category"][category]  # type: ignore[index]
    return str(item["lower_bound"]), str(item["expression"])


def main() -> int:
    k = json.loads(KPATH.read_text(encoding="utf-8"))
    t = json.loads(TPATH.read_text(encoding="utf-8"))
    if k["conclusion"]["all_checks_pass"] is not True or t["conclusion"]["all_checks_pass"] is not True:
        raise AssertionError("cannot report an incomplete sharpness replay")

    residual = max(abs(Q(x)) for x in k["equality_system"]["exact_center_residual"])
    kq = k["krawczyk"]["preconditioned_interval_jacobian_infinity_bound"]
    kratio = k["krawczyk"]["max_normalized_distance_from_box_center"]
    rows = []
    for name in ("W", "Wprime"):
        rank = k["rank_15_minors"][name]
        physical = k["physical_strict_continuous_time"][name]["summary"]
        eig, _ = exact_min(physical, "edge_eigenvalue_lower")
        trans, trans_label = exact_min(physical, "transition_probability")
        ct, ct_label = exact_min(physical, "strict_continuous_time")
        inh, inh_label = exact_min(physical, "inheritance_probability")
        rows.append(
            f"| {name} | `{rank['selected_columns']}` | {scientific(rank['point_determinant'])} | "
            f"{scientific(rank['neumann_infinity_bound'])} | {scientific(eig)} | "
            f"{scientific(trans)} ({trans_label}) | {scientific(ct)} ({ct_label}) | {scientific(inh)} ({inh_label}) |"
        )

    root = t["conclusion"]
    u = t["all_n"]["cherry_edge_physical_points"]["u"]
    v = t["all_n"]["cherry_edge_physical_points"]["v"]
    determinant = t["all_n"]["cherry_observable_jacobian"]
    input_hashes = {Path(x["path"]).name: x["sha256"] for x in k["provenance"]["frozen_inputs"]}

    report = fr"""# Independent K3P weak-class sharpness certification report

## Certified outcome

The sharpness gate passes independently. There is a strict continuous-time common three-leaf K3P tensor for the two fixed weak-but-not-strong tree-child level-2 networks `W` and `Wprime`. At that tensor both normalized maps have rank 15, so their images share an ambient-open regular 15-dimensional germ. Identical K3P cherry substitution gives, for every integer \(n\ge 3\), a common full-dimensional regular germ of dimension

\[
15+6(n-3)=6n-3.
\]

The base networks are labelled nonisomorphic and not ordinary-triangle-equivalent, and those properties and weak-not-strong tree-child status persist under every substitution.

This report certifies the weak-class sharpness component. It does not by itself certify the separate fourteen-orbit or local-to-global classification gates.

## Independence and provenance

The replay uses two separately structured standard-library verifiers. The algebraic verifier reconstructs displayed-tree Fourier monomials from the primitive rooted arcs and uses exact rational closed intervals throughout. It does not import the cloud map builder or certifier. The topology verifier reconstructs the fixed mixed graphs, exhaustively orients ordinary edges, and checks binary degree, acyclicity, reachability, the LSA condition by exact dominators, and tree-childness. Neither verifier accepts a stored final Boolean.

The cloud certifier refers to `sharpness_relative_root.json`, which is absent from the frozen package. This is a provenance discrepancy, not a proof gap here: the frozen certificate preserves all 64 rational direct-parameter data, the 15 pivot columns, the 15 rational scaled-variable center coordinates, the row scales, and the radius. The independent verifier reconstructs the equality system from the graphs and derives a new exact inverse preconditioner.

Primary frozen hashes used for reconstruction include:

- `k3p_sharpness_krawczyk.json`: `{input_hashes['k3p_sharpness_krawczyk.json']}`
- `sharpness_exact_maps.py`: `{input_hashes['sharpness_exact_maps.py']}` (provenance/cross-reference only; not imported)
- `certify_sharpness_krawczyk.py`: `{input_hashes['certify_sharpness_krawczyk.py']}` (provenance/cross-reference only; not imported)
- `k3p_sharpness_all_n.json`: `{input_hashes['k3p_sharpness_all_n.json']}`
- `k3p_rooting_censuses.json`: `{input_hashes['k3p_rooting_censuses.json']}`

## Exact equality system and box

Let \(y\in\mathbb R^{{15}}\) be the scaled pivot variables. For each of the 15 nonconstant zero-sum three-leaf K3P Fourier coordinates, the verifier constructs

\[
F_i(y)=s_i\bigl(q_i(W;x_W(y))-q_i(W';x_{{W'}}(y))\bigr).
\]

There are 64 direct parameters: ten edges times three K3P eigenvalues plus two inheritance probabilities on each side. Fifteen are pivot parameters of the form \(x_{{p_j}}=a_{{p_j}}y_j\); the other 49 are frozen at recorded rational values. The exact expanded sparse equations are embedded in the certificate and have SHA-256 `{k['equality_system']['expanded_sparse_polynomials_sha256']}`. Their term counts are `{[len(x) for x in k['equality_system']['expanded_sparse_polynomials']]}`.

The box is the rational cube

\[
X=\prod_{{j=1}}^{{15}}[y_{{0,j}}-\rho,y_{{0,j}}+\rho],
\qquad \rho={k['parameterization']['box_radius']}=10^{{-50}}.
\]

The largest exact scaled residual at the rational center is approximately {scientific(str(residual))}. The exact point Jacobian determinant is approximately {scientific(k['equality_system']['point_jacobian_determinant'])} and is nonzero.

## Krawczyk theorem replay

The verifier computes the exact rational preconditioner

\[
Y=J_F(y_0)^{{-1}}
\]

by rational Gauss-Jordan elimination. It then encloses the interval Jacobian \(J_F(X)\) and forms

\[
K(y_0,X)=y_0-YF(y_0)+\bigl(I-YJ_F(X)\bigr)(X-y_0).
\]

Every one of the 15 resulting intervals lies strictly inside the corresponding component of \(X\). The maximum distance of \(K(y_0,X)\) from the box center, normalized by \(\rho\), is {scientific(kratio)}. The independently derived bound

\[
\lVert I-YJ_F(X)\rVert_\infty\le {scientific(kq)}<1
\]

also holds. Thus the Krawczyk inclusion gives existence. The bound below one makes every mean Jacobian between two points of the convex box invertible, so the root in this slice is unique. This uniqueness concerns the 15-variable equality slice; it is not a claim of global numerical parameter identifiability.

The certificate records the full exact preconditioner, interval Jacobian, error matrix, Krawczyk intervals, and all left/right strict-inclusion margins—not just these decimal summaries.

## Uniform rank and strict physical inequalities

Lexicographic exact row reduction independently selects a 15-column minor for each 15-by-32 local network Jacobian. For each interval minor \(A(X)\), the verifier computes the exact inverse \(A(y_0)^{{-1}}\) and proves

\[
\lVert I-A(y_0)^{{-1}}A(X)\rVert_\infty<1.
\]

Consequently both selected minors are nonzero for every parameter point in the certified box.

| map | local columns | point determinant | Neumann bound | smallest eigenvalue lower bound | smallest transition lower bound | smallest CT lower bound | smallest inheritance lower bound |
|---|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

The very small point determinants reflect the unscaled lexicographic minors and tiny pendant eigenvalues; their exact nonzero values and the uniform Neumann exclusions, not their decimal magnitudes, are the certificates.

For every one of the 20 edge spectra throughout the box, the replay checks all three eigenvalue lower and upper margins, all four inverse-Fourier transition probabilities

\[
\frac{{1+C+G+T}}4,\quad\frac{{1+C-G-T}}4,\quad
\frac{{1-C+G-T}}4,\quad\frac{{1-C-G+T}}4,
\]

and all three strict continuous-time margins \(C-GT\), \(G-CT\), and \(T-CG\). It also checks both sides of every inheritance interval. Every exact lower bound is positive; all individual records are stored in the certificate.

## Why this proves a common regular germ

At the unique equality-slice root \(y_*\in X\), the two physical network parameter points have the same normalized Fourier tensor \(q_*\). Each network map has a nonzero 15-by-15 minor at—and uniformly around—its certified parameter point. The submersion theorem therefore gives an ambient-open neighborhood of \(q_*\) in each 15-dimensional normalized image. Their intersection is a common ambient-open regular germ. All box parameters are in the principal stochastic domain and, more strongly, in the strict continuous-time domain.

## Rooting census and topology replay

The independent exhaustive censuses are

\[
W:(5,2,3),\qquad W':(7,2,5),\qquad
\text{{collision reference}}:(7,0,7),
\]

where each triple is (admissible, tree-child, non-tree-child). The full root edge, unique valid orientation, directed arcs, tree-child result, non-tree-child witness, and LSA dominator check are stored for every rooting. The first two triples prove \(W,W'\in W_{{\mathrm{{TC}}}}\setminus S_{{\mathrm{{TC}}}}\).

Both fixed mixed graphs are simple, binary, and level two. Exact labelled mixed-graph comparison finds zero isomorphisms. Even after all internal arrowhead flags are forgotten, exact labelled underlying-graph comparison still finds zero isomorphisms. This is stronger than needed to exclude ordinary triangle redirection, which cannot alter the underlying labelled graph.

## All-n cherry certificate

For one K3P cherry with edge spectra \(u=(u_C,u_G,u_T)\) and \(v=(v_C,v_G,v_T)\), character conservation exposes six tensor observables

\[
R_h=u_h/v_h,\qquad P_h=u_hv_h,\qquad h\in\{{C,G,T\}}.
\]

A formal Laurent-polynomial determinant computation—not a substitution into the stored formula—gives

\[
\det\frac{{\partial(R_C,P_C,R_G,P_G,R_T,P_T)}}
{{\partial(u_C,v_C,u_G,v_G,u_T,v_T)}}
=\frac{{8u_Cu_Gu_T}}{{v_Cv_Gv_T}}.
\]

At the rational example \(u=({','.join(u['values'])})\), \(v=({','.join(v['values'])})\), this determinant is exactly `{determinant['example_determinant']}`. The replay checks the complete stochastic and continuous-time inequalities; its smallest recorded margins (including transition probabilities) are `{u['minimum_margin']}` and `{v['minimum_margin']}`.

On the positive branch,

\[
u_h=\sqrt{{R_hP_h}},\qquad v_h=\sqrt{{P_h/R_h}},
\]

so the six new edge coordinates are locally recovered. Dividing retained-cherry tensor coordinates by their nonzero pendant factors recovers the old tensor. Thus a cherry adds at most six parameters and at least six locally observable directions, hence exactly six dimensions. Iteration yields \(15+6(n-3)=6n-3\).

For class persistence, the verifier checks exact substitution/contraction through five stages on both sides. The general induction is local: a tree-child base rooting lifts; an old non-tree-child vertex and its incident arcs remain unchanged; the three new edges are bridges, so blobs and level are unchanged; and contracting the uniquely labelled newest cherry recovers the preceding graph. Any enlarged labelled isomorphism or triangle equivalence would therefore contract to one for the base pair, which was exhaustively excluded.

## Replay commands and artifacts

From the project root:

```bash
.venv/bin/python sharpness/independent_krawczyk_replay.py
.venv/bin/python sharpness/independent_topology_alln_replay.py
.venv/bin/python sharpness/build_sharpness_report.py
```

Observed on the Apple M1 Pro replay machine:

- algebraic/interval replay: about 10.3 seconds, 68.6 MB maximum resident memory;
- topology/all-n replay: about 21.6 seconds, 56.6 MB maximum resident memory.

Active certificate hashes:

- `K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json`: `{digest(KPATH)}`
- `K3P_SHARPNESS_TOPOLOGY_ALL_N_CERTIFICATE.json`: `{digest(TPATH)}`

## Honest status

Strongest verified claim: the complete three-leaf strict-CT Krawczyk common point, uniform rank-15 submersions, weak-class topology status, and all-(n) (6n-3) cherry extension pass independent exact replay.

Remaining sharpness proof gap: none. Remaining provenance discrepancy: the cloud intermediate `sharpness_relative_root.json` was not supplied; the preserved rational data were sufficient for a fresh exact reconstruction and are bound by hash above.
"""
    atomic_text(REPORT, report)

    paths = [
        HERE / "independent_krawczyk_replay.py",
        HERE / "independent_topology_alln_replay.py",
        Path(__file__),
        KPATH,
        TPATH,
        REPORT,
    ]
    manifest = {
        "schema": "k3p-sharpness-independent-replay-manifest-v1",
        "status": "PASS",
        "files": [{"path": str(p.relative_to(PROJECT)), "bytes": p.stat().st_size, "sha256": digest(p)} for p in paths],
        "replay_commands": [
            ".venv/bin/python sharpness/independent_krawczyk_replay.py",
            ".venv/bin/python sharpness/independent_topology_alln_replay.py",
            ".venv/bin/python sharpness/build_sharpness_report.py",
        ],
        "conclusion": {
            "krawczyk": k["conclusion"],
            "topology_all_n": t["conclusion"],
        },
    }
    atomic_text(MANIFEST, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"K3P_SHARPNESS_REPORT_PASS {REPORT}")
    print(f"report_sha256={digest(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
