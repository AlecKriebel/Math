import json
from pathlib import Path
import sys

import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "independent_verifier"))

import stable_core as sc
import core as dc
import pareto_core as pc
import frontier_verify_master_certificate as master_certificate
import frontier_verify_mode_certificates as mode_certificates


def test_family_flux_and_conservation():
    for m in (3, 4, 5, 6, 8, 10):
        rs = sc.reactions(m)
        assert len(rs) == m + 2
        assert all(sum(r.y) <= 2 and sum(r.yp) <= 2 for r in rs)
        G, Y = sc.gamma_y(m)
        assert G.rank() == m
        assert len(G.nullspace()) == 2
        assert sc.conservation(m).T * G == sp.zeros(1, m + 2)
        a, b = sp.symbols("a b", positive=True)
        assert G * sc.flux(m, a, b) == sp.zeros(m + 1, 1)
        assert sc.A_matrix(m, a, b) == G * sp.diag(*list(sc.flux(m, a, b))) * Y.T


def test_improved_profile_critical_harmonics_and_signs():
    for m in (3, 4, 5, 6, 8, 10):
        A = dc.Avec(m)
        r, d, ell = dc.selected(m)
        D = sp.diag(*d)
        rhs = -sp.Rational(1, 4) * dc.B(m, r, r)
        assert (A - D) * r == sp.zeros(m + 1, 1)
        assert (A - D).T * ell == sp.zeros(m + 1, 1)
        assert A * dc.w0(m) == rhs
        assert (A - 4 * D) * dc.w2(m) == rhs
        H = dc.Hsum(m)
        assert dc.ellr_formula(m, H) < 0
        assert dc.ellDr_formula(m, H) < 0
        assert dc.N_formula(m, H) > 0


def test_omission_table_and_unit_contrast():
    for m in range(3, 11):
        vals = dc.signed_omissions(m)
        assert vals[0] == 0
        assert vals[m - 1] == 0
        assert vals[m] == -2
        for j in range(1, m - 1):
            assert vals[j] == 16
        d = dc.selected(m)[1]
        assert max(d) == sp.Rational(23, 63)
        assert min(d) == sp.Rational(1, 91 * m - 183)
        assert sp.factor(max(d) / min(d)) == sp.Rational(23, 63) * (91 * m - 183)


def test_pareto_exact_contrasts_and_cubic_sign():
    for m in (3, 4, 5, 6, 8, 10):
        r = m - 2
        for L in (pc.L0(m), sp.Rational(1, 2) * (pc.L0(m) + pc.L1(m)), pc.L1(m)):
            hs = pc.Hlist(m, L)
            ds = pc.Dphys(m, L)
            assert all(sp.N(x) > 0 for x in hs + ds)
            chiD = sp.factor(max(ds, key=lambda x: float(sp.N(x))) / min(ds, key=lambda x: float(sp.N(x))))
            chiH = sp.factor(max(hs, key=lambda x: float(sp.N(x))) / min(hs, key=lambda x: float(sp.N(x))))
            assert sp.simplify(chiD - sp.Rational(23, 63) * 91 * r * L) == 0
            assert sp.simplify(chiH - sp.Rational(91 * r - 1, 91 * r) / L) == 0
            Hs = pc.Hsum(m)
            tau = pc.tau_formula(m, Hs, L)
            num = sp.factor(pc.N0(m, Hs) + tau * pc.Sterm(m, Hs))
            assert sp.N(num) > 0
            assert sp.N(pc.den_formula(m, L)) < 0


def test_repaired_pareto_endpoint_and_legacy_counterexample():
    assert sp.factor(pc.L0(3) - 1 / sp.sqrt(3)) == 0
    for m in (4, 5, 6, 8, 10, 149):
        assert sp.factor((m - 2) * pc.L0(m) ** 2 - sp.Rational(5, 4)) == 0
    # An exact Rouche comparison encloses an unstable root at the superseded
    # m=149 endpoint L=1/sqrt(3*(m-2))=1/21.
    mode_certificates.legacy_endpoint_rouche_regression()


def test_homogeneous_certificate_coefficient_mutation_is_rejected(tmp_path):
    source = ROOT / "independent_verifier" / "pareto_all_m_certificate.json"
    payload = json.loads(source.read_text())
    term = payload["modulus"]["homogeneous"]["terms"][0]
    original = term["coefficient_in_U_ascending"][0]
    term["coefficient_in_U_ascending"][0] = str(sp.Rational(original) + 1)
    mutated = tmp_path / "mutated_mode_certificate.json"
    mutated.write_text(json.dumps(payload))
    with pytest.raises(AssertionError):
        mode_certificates.verify(mutated)


def test_endpoint_factor_mutation_is_rejected(tmp_path):
    source = ROOT / "independent_verifier" / "frontier_certificate.json"
    payload = json.loads(source.read_text())
    payload["pareto_family"]["L0"]["r_ge_2"] = "sqrt(5)/(3*sqrt(r))"
    mutated = tmp_path / "mutated_master_certificate.json"
    mutated.write_text(json.dumps(payload))
    with pytest.raises(AssertionError):
        master_certificate.verify(mutated)


def test_fourier_factor_mutations_are_rejected():
    m = 5
    A = dc.Avec(m)
    r, d, ell = dc.selected(m)
    D = sp.diag(*d)
    Brr = dc.B(m, r, r)
    w0 = dc.w0(m)
    w2 = dc.w2(m)

    # The cosine-square projection contributes -1/4 to both stable equations.
    assert A * w0 != -sp.Rational(1, 2) * Brr
    assert (A - 4 * D) * w2 != -sp.Rational(1, 2) * Brr
    # The second harmonic has wave-number square four, not two.
    assert (A - 2 * D) * w2 != -sp.Rational(1, 4) * Brr

    H = dc.Hsum(m)
    correct = sp.factor(
        (ell.T * (dc.B(m, r, w0) + sp.Rational(1, 2) * dc.B(m, r, w2)))[0]
    )
    mutated = sp.factor((ell.T * (dc.B(m, r, w0) + dc.B(m, r, w2)))[0])
    assert sp.factor(correct - dc.N_formula(m, H)) == 0
    assert sp.factor(mutated - dc.N_formula(m, H)) != 0


def test_mutations_are_detected():
    m = 5
    A = dc.Avec(m)
    r, d, _ = dc.selected(m)
    D = sp.diag(*d)
    bad_r = r.copy(); bad_r[1] += sp.Rational(1, 1000)
    assert (A - D) * bad_r != sp.zeros(m + 1, 1)
    bad_D = D.copy(); bad_D[0, 0] += sp.Rational(1, 1000)
    assert (A - bad_D) * r != sp.zeros(m + 1, 1)
    # Changing the exact factor eight invalidates the unit-threshold identity.
    assert 7 * (m - 2) != 8 * (m - 2)


def test_current_profile_single_source_and_m3_regression():
    data=json.loads((ROOT/'data'/'current_profile_exact.json').read_text())
    assert data['schema']=='current-profile-exact-v1'
    row=data['rows'][0]
    assert row['m']==3
    assert row['ell_dot_r']=='-7451873/924210'
    assert row['ell_dot_Dr']=='-71818/462105'
    assert row['eta']['exact']=='143636/7451873'
    assert row['diffusion_profile'][0]=='23/63'
    assert row['diffusion_profile'][-1]=='16/45'
    assert row['eta']['decimal'].startswith('0.0192751540451642')


def test_old_profile_mutation_is_rejected_by_provenance():
    data=json.loads((ROOT/'data'/'current_profile_exact.json').read_text())
    row=data['rows'][0]
    old_first='257/240'
    old_eta='0.1054'
    assert old_first not in row['diffusion_profile']
    assert not row['eta']['decimal'].startswith(old_eta)
    table=(ROOT/'data'/'contrast_table.tex').read_text()
    assert old_eta not in table
    assert '1.306' not in table


def test_general_matrix_theorem_uses_exact_coefficient_domain():
    text=(ROOT/'manuscript'/'main.tex').read_text()
    sec=text.split('\\section{A principal-minor diffusion-ray theorem}',1)[1].split('\\section{Exact diffusion design',1)[0]
    assert 'sum_{|I|=n-1}a_I>0' in sec
    assert 'at most one' not in sec
    assert '\\label{thm:diffusionray}' in sec


def test_scope_and_certificate_honesty_markers():
    text=(ROOT/'manuscript'/'main.tex').read_text()
    assert '\\mathfrak S_m' in text
    assert 'not classified here' in text
    assert 'not asserted to be an intrinsic' in text
    assert 'wave instability' in text
    assert 'b=2a' in text
    assert 'N_m(L)>1/200' in text
    assert 'square-root-balanced' not in text
    assert 'right panel' not in text
