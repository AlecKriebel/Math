#!/usr/bin/env python3
"""Independent finite-Fock controls for the bounded-region proof.

These are numerical and algebraic controls, not a discretized proof of the
infinite-dimensional statement. No author verification code is imported.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eigh

PROOF_SHA256 = '2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350'
AUTHOR_MANIFEST_SHA256 = 'd6a0862cbf2f6500cc5fd7ee2239e0e8a2c5864c9d09a6cd9a13b1b4f99176ef'


def fingerprint(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def input_integrity(root, sources):
    manifest = json.loads((root / 'AUTHOR_MANIFEST.json').read_text())
    assert fingerprint(root / 'AUTHOR_MANIFEST.json')['sha256'] == AUTHOR_MANIFEST_SHA256
    assert fingerprint(root / 'BOUNDED_REGION_PROOF.md')['sha256'] == PROOF_SHA256
    assert set(manifest['files']) | {'AUTHOR_MANIFEST.json'} == {p.name for p in root.iterdir() if p.is_file()}
    for name, expected in manifest['files'].items():
        assert fingerprint(root / name) == expected, name
    source_result = 'not requested'
    if sources:
        src_manifest = json.loads((root / 'SOURCE_MANIFEST.json').read_text())
        for src in src_manifest['sources']:
            p = sources / src['file_label']
            assert p.read_bytes().startswith(b'%PDF-')
            assert fingerprint(p) == {k: src[k] for k in ['bytes', 'sha256']}, src['file_label']
        source_result = 'all three retained PDF fingerprints match'
    return {'status': 'pass', 'author_manifest_sha256': AUTHOR_MANIFEST_SHA256,
            'proof_sha256': PROOF_SHA256, 'source_bytes': source_result}


def controls():
    rng = np.random.default_rng(30006191)
    modes, inside_modes = 7, 5
    size = 1 << modes
    eye = np.eye(size, dtype=complex)
    creation = []
    for j in range(modes):
        c = np.zeros((size, size), complex)
        for bits in range(size):
            if not bits & (1 << j):
                sign = -1 if (bits & ((1 << j)-1)).bit_count() % 2 else 1
                c[bits | (1 << j), bits] = sign
        creation.append(c)
    car_error = max(float(np.max(np.abs(creation[i].conj().T @ creation[j]
                 + creation[j] @ creation[i].conj().T - (eye if i == j else 0))))
                 for i in range(modes) for j in range(modes))
    assert car_error == 0
    def create(g):
        return sum(g[j] * creation[j] for j in range(modes))
    z = rng.normal(size=(modes, modes)) + 1j*rng.normal(size=(modes, modes))
    h = z.conj().T @ z / (3*modes)
    energies_h, basis_h = eigh(h)
    def one_free(t, g):
        return basis_h @ (np.exp(-1j*t*energies_h) * (basis_h.conj().T @ g))
    T = sum(h[i,j] * (creation[i] @ creation[j].conj().T)
            for i in range(modes) for j in range(modes))
    counts = np.array([bits.bit_count() for bits in range(size)])
    inside = np.array([(bits & ((1 << inside_modes)-1)).bit_count() for bits in range(size)])
    missing = counts - inside
    q = np.diag([0]*inside_modes+[1]*(modes-inside_modes)).astype(complex)
    z = rng.normal(size=(inside_modes, inside_modes)) + 1j*rng.normal(size=(inside_modes, inside_modes))
    u, _ = np.linalg.qr(z)
    orbitals = np.zeros((modes, inside_modes), complex)
    orbitals[:inside_modes, :] = u
    f = orbitals[:, 0]
    A = create(f)
    vacuum = np.zeros(size, complex); vacuum[0] = 1
    eval_T, evec_T = eigh(T)
    def evolve(e, v, t, vector):
        return v @ (np.exp(-1j*t*e) * (v.conj().T @ vector))
    metrics = {'car_max_error': car_error, 'reference_matrix_element_max_error': 0.,
               'slater_first_moment_max_error': 0., 'slater_second_moment_max_error': 0.,
               'duhamel_identity_max_error': 0., 'adjoint_matrix_element_max_error': 0.,
               'comparison_bound_max_excess': 0., 'variance_bound_max_excess': 0.,
               'free_covariance_max_error': 0., 'phase_cases': 0, 'moment_cases': 0,
               'duhamel_cases': 0, 'post_evolution_occupied_overlap_max': 0.}
    negative = {'wrong_free_covariance_sign_detected': False,
                'wrong_sector_phase_sign_detected': False,
                'omitted_normal_order_correction_detected': False,
                'false_second_moment_equals_mean_detected': False}
    for sigma in (0, 1):
        H = T + np.diag(inside*(inside-sigma))
        K = T + np.diag(counts*(counts-sigma))
        W = H - K
        evH, vecH = eigh(H)
        evK, vecK = eigh(K)
        for n in (1, 2, 3, 4):
            occupied = orbitals[:, 1:n+1]
            psi = vacuum.copy()
            for g in reversed(occupied.T):
                psi = create(g) @ psi
            xi = A @ psi
            assert abs(np.linalg.norm(psi)-1) < 1e-12
            assert abs(np.linalg.norm(xi)-1) < 1e-12
            assert np.linalg.norm(A.conj().T @ psi) < 1e-12
            for t in (.071, .217, np.pi/(2*n+1-sigma)):
                psiK = evolve(evK, vecK, t, psi)
                xiK = evolve(evK, vecK, t, xi)
                F_K = np.vdot(xiK, A @ psiK)
                freef = one_free(-t, f)
                free_overlap = np.vdot(f, freef)
                predicted = np.exp(1j*t*(2*n+1-sigma)) * free_overlap
                err = abs(F_K-predicted)
                metrics['reference_matrix_element_max_error'] = max(metrics['reference_matrix_element_max_error'], float(err))
                cov_direct = evolve(eval_T, evec_T, -t, A @ evolve(eval_T, evec_T, t, psi))
                cov_right = create(freef) @ psi
                metrics['free_covariance_max_error'] = max(metrics['free_covariance_max_error'], float(np.linalg.norm(cov_direct-cov_right)))
                metrics['post_evolution_occupied_overlap_max'] = max(metrics['post_evolution_occupied_overlap_max'], float(np.linalg.norm(occupied.conj().T @ freef)))
                if t == .217:
                    negative['wrong_free_covariance_sign_detected'] |= abs(F_K-np.exp(1j*t*(2*n+1-sigma))*np.vdot(f,one_free(t,f))) > 1e-3
                    negative['wrong_sector_phase_sign_detected'] |= abs(F_K-np.exp(-1j*t*(2*n+1-sigma))*free_overlap) > 1e-3
                    if sigma == 1:
                        negative['omitted_normal_order_correction_detected'] |= abs(F_K-np.exp(1j*t*(2*n+1))*free_overlap) > 1e-3
                psiH = evolve(evH, vecH, t, psi)
                xiH = evolve(evH, vecH, t, xi)
                F_H = np.vdot(xiH, A @ psiH)
                bound = np.linalg.norm(psiH-psiK) + np.linalg.norm(xiH-xiK)
                metrics['comparison_bound_max_excess'] = max(metrics['comparison_bound_max_excess'], float(abs(F_H-F_K)-bound))
                Dxi = evolve(evH, vecH, -t, A.conj().T @ xiH) - A.conj().T @ xi
                metrics['adjoint_matrix_element_max_error'] = max(metrics['adjoint_matrix_element_max_error'], float(abs(np.vdot(psi,Dxi)-np.conj(F_H-1))))
                metrics['phase_cases'] += 1
                for phi, gs in ((psi, occupied), (xi, np.column_stack((f, occupied)))):
                    phi0 = evolve(eval_T, evec_T, t, phi)
                    free_gs = np.column_stack([one_free(t,g) for g in gs.T])
                    P = free_gs @ free_gs.conj().T
                    mean = float(np.vdot(phi0, missing*phi0).real)
                    second = float(np.vdot(phi0, missing*missing*phi0).real)
                    lam = float(np.trace(P@q).real)
                    predicted_second = lam**2+lam-float(np.trace(P@q@P@q).real)
                    metrics['slater_first_moment_max_error'] = max(metrics['slater_first_moment_max_error'], abs(mean-lam))
                    metrics['slater_second_moment_max_error'] = max(metrics['slater_second_moment_max_error'], abs(second-predicted_second))
                    metrics['variance_bound_max_excess'] = max(metrics['variance_bound_max_excess'], second-mean**2-mean)
                    negative['false_second_moment_equals_mean_detected'] |= abs(second-mean) > 1e-5
                    metrics['moment_cases'] += 1
            # Vector-valued Duhamel identity: generic time avoids phase-only tests.
            t=.217
            nodes, weights = leggauss(40)
            for phi, count in ((psi,n),(xi,n+1)):
                integral = np.zeros(size, complex)
                absolute_integral = 0.
                for x,w in zip(nodes, weights):
                    s=t*(x+1)/2
                    reference = evolve(evK, vecK, s, phi)
                    integrand = evolve(evH, vecH, t-s, W @ reference)
                    integral += (t*w/2)*integrand
                    absolute_integral += (t*w/2)*2*count*np.linalg.norm(missing*reference)
                difference = evolve(evH, vecH, t, phi)-evolve(evK, vecK, t, phi)
                metrics['duhamel_identity_max_error'] = max(metrics['duhamel_identity_max_error'], float(np.linalg.norm(difference+1j*integral)))
                assert np.linalg.norm(difference) <= absolute_integral+1e-11
                metrics['duhamel_cases'] += 1
    # The Slater hypothesis cannot be silently dropped: a cat state with
    # four particles all inside or all outside has variance 4 > mean 2.
    cat_mean, cat_second = 2., 8.
    cat_variance = cat_second-cat_mean**2
    assert cat_variance > cat_mean
    negative['non_slater_variance_bound_counterexample'] = True
    # First-moment/probability control alone misses number fluctuations:
    # P(M=n)=1/n^2 has E M=1/n but E M^2=1.
    rare_n = 100
    assert rare_n*(1/rare_n**2) == 1/rare_n
    assert rare_n**2*(1/rare_n**2) == 1
    negative['leakage_probability_not_second_moment_counterexample'] = True
    assert all(bool(x) for x in negative.values())
    for key, value in metrics.items():
        if key.endswith('_max_error') or key.endswith('_max_excess'):
            assert value < 1e-10, (key, value)
    assert metrics['post_evolution_occupied_overlap_max'] > .01
    return {'status':'pass', 'modes':modes, 'fock_dimension':size,
            'seed':30006191, 'metrics': metrics,
            'negative_controls':{k:bool(v) for k,v in negative.items()}}


def scaling():
    cases=[]
    for d in (1,2,3,4,9):
        kinetic=1+Fraction(2,d)
        first=1+kinetic/2-2
        second=1+kinetic-3
        assert first == Fraction(-1,2)+Fraction(1,d)
        assert second == -1+Fraction(2,d)
        assert (first < 0 and second < 0) == (d>2)
        cases.append({'dimension':d,'kinetic':str(kinetic),'first_error':str(first),'second_error':str(second)})
    # Integer version of ceil(N^(1/3)) to avoid floating cube-root rounding.
    for n in (1,2,7,8,9,26,27,28,63,64,65,1000,1001,1000000):
        m=1
        while m**3<n: m+=1
        assert m**3>=n and (m-1)**3<n
        assert m**3<=8*n
        # ell^-2 = 4m^2, so the gradient sum <=16 n^(5/3).
        assert (4*m*m)**3 <= 16**3*n*n
    sector_count=0
    for sigma in (0,1):
        for n in range(1,129):
            for leaked in range(n+1):
                diff=(n-leaked)*(n-leaked-sigma)-n*(n-sigma)
                assert diff == -leaked*(2*n-sigma-leaked)
                assert abs(diff) <= 2*n*leaked
                sector_count+=1
    return {'status':'pass', 'dimension_cases':cases, 'sector_cases':sector_count,
            'packing_bound':'integer-checked at cube boundaries; analytic proof remains required'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-dir', type=Path, required=True)
    parser.add_argument('--source-dir', type=Path)
    args=parser.parse_args()
    result={'scope':'Independent finite controls and frozen-byte verification; not a proof by simulation.',
            'python':sys.version.split()[0], 'numpy':np.__version__,
            'input_integrity':input_integrity(args.author_dir,args.source_dir),
            'fock_controls':controls(), 'scaling_and_polynomials':scaling()}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__=='__main__':
    main()
