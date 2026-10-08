"""Independent scalar diagnostics, not a certified quadrature or Brownian proof."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import os
import mpmath as mp

mp.mp.dps = 105
HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def spectral(t, alpha, ell, right=False):
    nmax = math.ceil(math.sqrt(2 * float(ell**2 / t) * 125 * math.log(10)) / math.pi) + 8
    return mp.pi / ell**2 * mp.fsum(
        ((-1) ** (n + 1) if right else 1) * n
        * mp.sin(n * mp.pi * alpha / ell)
        * mp.exp(-n*n * mp.pi**2 * t / (2*ell**2))
        for n in range(1, nmax + 1)
    ), nmax


def images(t, alpha, ell):
    nmax = math.ceil(math.sqrt(2 * float(t / ell**2) * 125 * math.log(10)) / 2) + 8
    return mp.fsum(
        (alpha + 2*n*ell) * mp.exp(-(alpha + 2*n*ell)**2 / (2*t))
        for n in range(-nmax, nmax + 1)
    ) / (mp.sqrt(2*mp.pi) * t**mp.mpf('1.5')), nmax


rows = []
maximum_scaled_absolute_error = mp.mpf(0)
maximum_relative_error_above_cutoff = mp.mpf(0)
for ell_text in ('0.37', '1', '3.75'):
    ell = mp.mpf(ell_text)
    for ratio_text in ('0.0001', '0.125', '0.5', '0.875', '0.9999'):
        alpha = ell * mp.mpf(ratio_text)
        for time_ratio in ('0.0001', '0.003', '0.03', '0.2', '1', '5'):
            t = ell**2 * mp.mpf(time_ratio)
            for right in (False, True):
                eigen, ne = spectral(t, alpha, ell, right)
                image, ni = images(t, ell-alpha if right else alpha, ell)
                error = abs(eigen-image) * ell**2
                maximum_scaled_absolute_error = max(maximum_scaled_absolute_error, error)
                require(error < mp.mpf('1e-85'), 'independent kernel mismatch')
                require(eigen * ell**2 >= -mp.mpf('1e-85'), 'negative spectral density')
                require(image * ell**2 >= -mp.mpf('1e-85'), 'negative image density')
                relative = None
                if abs(image * ell**2) > mp.mpf('1e-50'):
                    relative = abs((eigen-image)/image)
                    maximum_relative_error_above_cutoff = max(maximum_relative_error_above_cutoff, relative)
                    require(relative < mp.mpf('1e-50'), 'relative flux mismatch')
                rows.append({'ell':ell_text, 'alpha_over_ell':ratio_text,
                             't_over_ell_squared':time_ratio, 'right_exit':right,
                             'spectral_terms':ne, 'image_halfwidth':ni,
                             'scaled_absolute_error':str(error),
                             'relative_error_above_cutoff':None if relative is None else str(relative)})

laplace_checks = 0
for ell_text in ('0.37', '1', '3.75'):
    ell = mp.mpf(ell_text)
    for ratio_text in ('0.0001', '0.125', '0.5', '0.875', '0.9999'):
        alpha = ell * mp.mpf(ratio_text)
        for s_text in ('0.00001', '0.2', '1', '100'):
            s = mp.mpf(s_text)
            r = mp.sqrt(2*s)
            left_geometric = (mp.exp(-alpha*r)-mp.exp(-(2*ell-alpha)*r))/(1-mp.exp(-2*ell*r))
            left_sinh = mp.sinh((ell-alpha)*r)/mp.sinh(ell*r)
            right_sinh = mp.sinh(alpha*r)/mp.sinh(ell*r)
            singleton_cosh = mp.cosh((alpha-ell/2)*r)/mp.cosh(ell*r/2)
            require(abs(left_geometric-left_sinh) < mp.mpf('1e-95'), 'image Laplace normalization')
            require(abs(left_sinh+right_sinh-singleton_cosh) < mp.mpf('1e-95'), 'singleton two-flux Laplace normalization')
            laplace_checks += 2

receipt = {
    'actual_ROOT_PID':os.getpid(), 'UTC':datetime.now(timezone.utc).isoformat(),
    'precision_decimal_digits':mp.mp.dps, 'mpmath_version':mp.__version__,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'verdict':'PASS_SCALAR_DIAGNOSTICS', 'kernel_cases':len(rows),
    'laplace_identity_checks':laplace_checks,
    'maximum_scaled_absolute_error':str(maximum_scaled_absolute_error),
    'maximum_relative_error_for_scaled_density_above_1e-50':str(maximum_relative_error_above_cutoff),
    'scope':'Independent image-sum versus spectral exit flux and explicit Laplace normalization. Finite high-precision diagnostics; no certified quadrature, uniform numerical-error theorem, or proof by computation.',
    'cases':rows,
}
(HERE/'RESULT.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k != 'cases'}, indent=2))
