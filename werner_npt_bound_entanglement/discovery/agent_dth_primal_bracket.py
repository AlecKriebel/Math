#!/usr/bin/env python3
"""Audit numerical primal/dual brackets for the facially reduced DTH SDP.

This is a discovery-layer utility.  It reads an ADMM checkpoint, reconstructs
the first exposed mixed face, and reports:

* the dual lower bound supplied by the current scaled ADMM multiplier;
* a genuinely feasible numerical primal upper bound obtained by mixing the
  current holomorphic iterate with a relative-interior feasible point.

The reported bounds are floating-point diagnostics, not exact certificates.
"""

from __future__ import annotations

import argparse

import numpy as np
import scipy.linalg as la
import scipy.sparse.linalg as sla

import agent_dth_invariant_crossing as cross
import agent_dth_primal_admm as primal


def compressed_blocks(tensor, blocks, field):
    result = []
    for block in blocks:
        basis = block[field]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(
            tensor, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        result.append((block, basis.T @ matrix @ basis))
    return result


def dual_lower_bound(objective, trace, multiplier, local, hol_blocks,
                     mixed_blocks):
    """Return gamma with O+U^T multiplier-gamma*T PSD on K.

    The ADMM multiplier is normal to the mixed PSD cone, hence its compression
    should be negative semidefinite.  Equivalently -multiplier is the usual
    positive mixed dual variable.
    """
    mixed_max = -np.inf
    mixed_worst = None
    for block, matrix in compressed_blocks(multiplier, mixed_blocks, "kernel"):
        value = float(np.max(la.eigvalsh(matrix)))
        if value > mixed_max:
            mixed_max, mixed_worst = value, block["shapes"]

    slack = objective + primal.crossing_apply(
        local, multiplier, transpose=True)
    gamma = np.inf
    worst = None
    for block, matrix in compressed_blocks(slack, hol_blocks, "basis"):
        # The trace functional compresses to weight*I in each block.
        value = float(np.min(la.eigvalsh(matrix))) / block["weight"]
        if value < gamma:
            gamma, worst = value, block["shapes"]
    return gamma, worst, mixed_max, mixed_worst


def project_hol_affine(tensor, blocks, trace):
    """Orthogonally project onto hol support with trace one (no PSD clip)."""
    out = np.zeros_like(tensor)
    for block in blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(tensor, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        projected = basis @ (basis.T @ matrix @ basis) @ basis.T
        primal.put_block(out, block["indices"], projected, block["dimensions"])
    trace_norm_squared = float(np.vdot(trace, trace).real)
    coefficient = ((1 - float(np.vdot(trace, out).real))
                   / trace_norm_squared)
    out += coefficient * trace
    return out


def project_hol_tangent(tensor, blocks, trace):
    """Orthogonally project onto hol support with trace zero."""
    out = np.zeros_like(tensor)
    for block in blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(tensor, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        projected = basis @ (basis.T @ matrix @ basis) @ basis.T
        primal.put_block(out, block["indices"], projected, block["dimensions"])
    out -= (float(np.vdot(trace, out).real)
            / float(np.vdot(trace, trace).real)) * trace
    return out


def project_mixed_linear(tensor, blocks):
    """Orthogonally project a mixed tensor onto the current face span."""
    out = np.zeros_like(tensor)
    for block in blocks:
        basis = block["kernel"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(tensor, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        projected = basis @ (basis.T @ matrix @ basis) @ basis.T
        primal.put_block(out, block["indices"], projected, block["dimensions"])
    return out


def project_linear_intersection(tensor, local, hol_blocks, mixed_blocks,
                                trace, iterations=1000, tolerance=1e-13,
                                method="cg"):
    """Project onto the two affine linear support constraints.

    ``cg`` solves the normal equations on the trace-zero hol tangent space;
    ``alternating`` retains the slower von Neumann iteration for auditing.
    """
    a = project_hol_affine(tensor, hol_blocks, trace)
    if method == "cg":
        shape = a.shape

        def outside_mixed(hol_tensor):
            crossed = primal.crossing_apply(local, hol_tensor)
            return crossed - project_mixed_linear(crossed, mixed_blocks)

        initial_outside = outside_mixed(a)

        def normal_action(vector):
            delta = vector.reshape(shape)
            outside = outside_mixed(delta)
            pulled = primal.crossing_apply(local, outside, transpose=True)
            return project_hol_tangent(
                pulled, hol_blocks, trace).reshape(-1)

        pulled_rhs = primal.crossing_apply(
            local, initial_outside, transpose=True)
        rhs = -project_hol_tangent(
            pulled_rhs, hol_blocks, trace).reshape(-1)
        operator = sla.LinearOperator(
            (a.size, a.size), matvec=normal_action, dtype=float)
        count = [0]

        def callback(_):
            count[0] += 1

        delta, info = sla.cg(operator, rhs, x0=np.zeros(a.size),
                             rtol=tolerance, atol=0,
                             maxiter=iterations, callback=callback)
        a += project_hol_tangent(
            delta.reshape(shape), hol_blocks, trace)
        crossed = primal.crossing_apply(local, a)
        supported = project_mixed_linear(crossed, mixed_blocks)
        residual = float(la.norm(crossed - supported))
        normal_residual = float(la.norm(
            normal_action(delta) - rhs))
        return a, count[0], normal_residual, residual, info

    if method != "alternating":
        raise ValueError(f"unknown linear projection method {method}")
    step = np.inf
    for iteration in range(1, iterations + 1):
        mixed = primal.crossing_apply(local, a)
        mixed = project_mixed_linear(mixed, mixed_blocks)
        b = primal.crossing_apply(local, mixed, transpose=True)
        a_new = project_hol_affine(b, hol_blocks, trace)
        step = float(la.norm(a_new - a))
        a = a_new
        if step < tolerance:
            break
    crossed = primal.crossing_apply(local, a)
    supported = project_mixed_linear(crossed, mixed_blocks)
    residual = float(la.norm(crossed - supported))
    return a, iteration, step, residual, 0


def cone_pairs(current, interior, blocks, field):
    pairs = []
    for block in blocks:
        basis = block[field]
        if not basis.shape[1]:
            continue
        a = primal.get_block(current, block["indices"], block["dimensions"])
        b = primal.get_block(interior, block["indices"], block["dimensions"])
        a = basis.T @ ((a + a.T) / 2) @ basis
        b = basis.T @ ((b + b.T) / 2) @ basis
        pairs.append((block["shapes"], a, b))
    return pairs


def minimum_mixing(current_hol, current_mixed, interior_hol, interior_mixed,
                   hol_blocks, mixed_blocks):
    """Smallest theta making both hol and mixed compressed blocks PSD."""
    pairs = (cone_pairs(current_hol, interior_hol, hol_blocks, "basis")
             + cone_pairs(current_mixed, interior_mixed,
                          mixed_blocks, "kernel"))

    def minimum(theta):
        value = np.inf
        shape = None
        for shapes, a, b in pairs:
            candidate = float(np.min(la.eigvalsh((1 - theta) * a + theta * b)))
            if candidate < value:
                value, shape = candidate, shapes
        return value, shape

    lo, hi = 0.0, 1.0
    min_hi, _ = minimum(hi)
    if min_hi < -1e-11:
        raise RuntimeError(f"interior point is not cone feasible: {min_hi}")
    for _ in range(70):
        mid = (lo + hi) / 2
        if minimum(mid)[0] >= 0:
            hi = mid
        else:
            lo = mid
    min_zero, worst_zero = minimum(0)
    min_interior, worst_interior = minimum(1)
    min_mix, worst_mix = minimum(hi)
    return hi, (min_zero, worst_zero), (min_interior, worst_interior), (
        min_mix, worst_mix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkpoint")
    parser.add_argument("--rho", type=float, required=True)
    parser.add_argument("--mixed-face")
    parser.add_argument("--product-face")
    parser.add_argument("--mixed-face-field", default="a")
    parser.add_argument("--face-tol", type=float, default=1e-9)
    parser.add_argument("--interior", required=True)
    parser.add_argument("--interior-field", default="x")
    parser.add_argument("--linear-iterations", type=int, default=1000)
    parser.add_argument("--linear-tol", type=float, default=1e-13)
    parser.add_argument("--linear-method", choices=("cg", "alternating"),
                        default="cg")
    parser.add_argument("--save-feasible")
    parser.add_argument("--mix-safety", type=float, default=0.0)
    parser.add_argument("--mix-theta", type=float)
    args = parser.parse_args()

    crossing, hol, mixed = cross.local_crossing(verbose=False)
    local, hol_ranges, mixed_ranges = primal.normalized_local_crossing(crossing)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=False)
    hol_blocks, objective, trace = primal.prepare_hol_blocks(hol_ranges)
    mixed_blocks = primal.prepare_mixed_blocks(mixed_ranges, support)
    if bool(args.mixed_face) == bool(args.product_face):
        raise ValueError("choose exactly one of --mixed-face and --product-face")
    if args.product_face:
        primal.restrict_mixed_blocks_to_product_face(
            mixed_blocks, np.load(args.product_face))
    else:
        face = np.load(args.mixed_face)[args.mixed_face_field]
        primal.restrict_mixed_blocks_to_exposed_face(
            mixed_blocks, face, args.face_tol)

    data = np.load(args.checkpoint)
    x = data["x"]
    multiplier = args.rho * data["dual"]
    ux = primal.crossing_apply(local, x)
    objective_value = float(np.vdot(objective, x).real)
    trace_value = float(np.vdot(trace, x).real)

    gamma, worst, mixed_max, mixed_worst = dual_lower_bound(
        objective, trace, multiplier, local, hol_blocks, mixed_blocks)

    interior_data = np.load(args.interior)
    interior_x = interior_data[args.interior_field]
    interior_ux = primal.crossing_apply(local, interior_x)
    interior_value = float(np.vdot(objective, interior_x).real)
    interior_trace = float(np.vdot(trace, interior_x).real)
    linear_x, linear_iterations, linear_step, linear_residual, linear_info = (
        project_linear_intersection(
            x, local, hol_blocks, mixed_blocks, trace,
            args.linear_iterations, args.linear_tol, args.linear_method))
    linear_ux = primal.crossing_apply(local, linear_x)
    linear_value = float(np.vdot(objective, linear_x).real)
    theta, current_min, interior_min, mixed_min = minimum_mixing(
        linear_x, linear_ux, interior_x, interior_ux,
        hol_blocks, mixed_blocks)
    boundary_theta = theta
    if args.mix_theta is not None:
        theta = args.mix_theta
        if theta < boundary_theta:
            raise ValueError(
                f"requested mix theta {theta} is below PSD boundary "
                f"{boundary_theta}")
    else:
        theta = min(1.0, theta + args.mix_safety)
    upper = (1 - theta) * linear_value + theta * interior_value
    feasible_x = (1 - theta) * linear_x + theta * interior_x
    feasible_z = (1 - theta) * linear_ux + theta * interior_ux
    feasible_hol_min = primal.cone_minimum_eigenvalue(
        feasible_x, hol_blocks)[0]
    feasible_mixed_min = primal.cone_minimum_eigenvalue(
        feasible_z, mixed_blocks, mixed=True)[0]

    print("checkpoint objective:", objective_value)
    print("checkpoint trace:", trace_value)
    print("checkpoint crossing residual:", float(la.norm(ux - data["z"])))
    print("dual lower gamma:", gamma, "worst hol block", worst)
    print("dual normal max eigenvalue (must be <=0):", mixed_max,
          "worst mixed block", mixed_worst)
    print("interior objective:", interior_value, "trace", interior_trace)
    print("linear projection iterations:", linear_iterations,
          "method:", args.linear_method, "solver info:", linear_info,
          "last step:", linear_step,
          "crossed support residual:", linear_residual)
    print("linear-projected objective:", linear_value)
    print("linear-projected cone minimum:", current_min)
    print("interior cone minimum:", interior_min)
    print("PSD-boundary theta:", boundary_theta,
          "mixing theta (including safety):", theta,
          "boundary cone minimum", mixed_min,
          "safe hol/mixed minima", feasible_hol_min, feasible_mixed_min)
    print("linear-and-cone feasible numerical upper objective:", upper)
    print("numerical bracket:", gamma, "<= optimum <=", upper,
          "width", upper - gamma)
    if args.save_feasible:
        np.savez(args.save_feasible, x=feasible_x, z=feasible_z,
                 theta=np.array(theta), objective=np.array(upper),
                 linear_x=linear_x, linear_z=linear_ux,
                 linear_residual=np.array(linear_residual),
                 gamma=np.array(gamma), multiplier=multiplier)


if __name__ == "__main__":
    main()
