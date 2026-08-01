#!/usr/bin/env python3
"""Build the local Gamma_A -> Gamma_(A,z) complement bridge.

On a pair-symmetric degree-three source, Gamma_AA positivity is equivalent
to Gamma_(A,z) positivity by pair exchange and full transpose.  If ``C_A``
and ``C_Az`` are the normalized local crossings from holomorphic S7
coordinates, weighted isometry gives the bridge

    B = C_Az H C_A^T D_A,

where ``H`` repeats each holomorphic carrier dimension and ``D_A`` repeats
each Gamma_A mixed carrier dimension.  It obeys ``B C_A = C_Az`` and is a
weighted isometry.  Numerically its nonzero local Choi blocks have rank at
most two, making it the efficient complement route once Gamma_A coordinates
are already available.

The output is floating-point discovery data; the formula itself follows
exactly from the audited finite-group Fourier crossings.
"""

from argparse import ArgumentParser
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import numpy as np
import scipy.linalg as la


DEFAULT_GAMMA_A = DISCOVERY / "dth_level2_local_gammaA_crossing.npz"
DEFAULT_GAMMA_AZ = DISCOVERY / "dth_level2_local_gamma_az_crossing.npz"
DEFAULT_OUTPUT = (
    DISCOVERY / "dth_level2_local_gammaA_to_gammaAz_bridge.npz"
)


def repeated_metric(carriers, multiplicities):
    return np.repeat(
        np.asarray(carriers, dtype=float),
        np.asarray(multiplicities, dtype=int) ** 2,
    )


def local_choi_audit(bridge, input_multiplicities,
                     output_multiplicities, tolerance=2e-10):
    input_offsets = np.cumsum(
        np.r_[0, input_multiplicities * input_multiplicities]
    )
    output_offsets = np.cumsum(
        np.r_[0, output_multiplicities * output_multiplicities]
    )
    nonzero = 0
    maximum_rank = 0
    maximum_asymmetry = 0.0
    for output_index, output_size in enumerate(output_multiplicities):
        for input_index, input_size in enumerate(input_multiplicities):
            raw = bridge[
                output_offsets[output_index]:output_offsets[output_index + 1],
                input_offsets[input_index]:input_offsets[input_index + 1],
            ]
            if la.norm(raw) < 1e-12:
                continue
            nonzero += 1
            choi = raw.reshape(
                output_size, output_size, input_size, input_size
            ).transpose(0, 2, 1, 3).reshape(
                output_size * input_size, output_size * input_size
            )
            asymmetry = la.norm(choi - choi.T) / max(1.0, la.norm(choi))
            singular_values = la.svdvals(choi)
            rank = int(np.sum(
                singular_values > tolerance * max(1.0, singular_values[0])
            ))
            maximum_rank = max(maximum_rank, rank)
            maximum_asymmetry = max(maximum_asymmetry, asymmetry)
    assert maximum_asymmetry < 4e-12
    assert maximum_rank <= 2
    return nonzero, maximum_rank, maximum_asymmetry


def main():
    parser = ArgumentParser()
    parser.add_argument("--gamma-a", type=Path, default=DEFAULT_GAMMA_A)
    parser.add_argument("--gamma-az", type=Path, default=DEFAULT_GAMMA_AZ)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    gamma_a = np.load(args.gamma_a)
    gamma_az = np.load(args.gamma_az)
    first = gamma_a["crossing"]
    second = gamma_az["crossing"]
    hol_metric_inverse = repeated_metric(
        gamma_a["hol_carrier_dimensions"],
        gamma_a["hol_multiplicities"],
    )
    input_metric = repeated_metric(
        gamma_a["mixed_carrier_dimensions"],
        gamma_a["mixed_multiplicities"],
    )
    output_metric = repeated_metric(
        gamma_az["mixed_carrier_dimensions"],
        gamma_az["mixed_multiplicities"],
    )
    bridge = (
        (second * hol_metric_inverse[None, :]) @ first.T
    ) * input_metric[None, :]
    reconstruction = la.norm(bridge @ first - second) / la.norm(second)
    isometry = la.norm(
        bridge.T @ (output_metric[:, None] * bridge)
        - np.diag(input_metric)
    ) / la.norm(input_metric)
    input_multiplicities = gamma_a["mixed_multiplicities"].astype(int)
    output_multiplicities = gamma_az["mixed_multiplicities"].astype(int)
    choi = local_choi_audit(
        bridge, input_multiplicities, output_multiplicities
    )
    assert reconstruction < 2e-12
    assert isometry < 2e-12
    print("bridge reconstruction/weighted-isometry:",
          reconstruction, isometry)
    print("nonzero local blocks/max Choi rank/asymmetry:", choi)
    np.savez_compressed(
        args.output,
        bridge=bridge,
        input_multiplicities=input_multiplicities,
        input_carrier_dimensions=gamma_a["mixed_carrier_dimensions"],
        output_multiplicities=output_multiplicities,
        output_carrier_dimensions=gamma_az["mixed_carrier_dimensions"],
        diagnostics=np.asarray((reconstruction, isometry) + choi),
    )
    print("saved:", args.output)


if __name__ == "__main__":
    main()
