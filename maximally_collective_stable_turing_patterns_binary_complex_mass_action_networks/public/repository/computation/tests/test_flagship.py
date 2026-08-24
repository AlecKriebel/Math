import json
from pathlib import Path
import subprocess
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
import frontier_verify_exposition_identities as exposition_identities
import verify_family as family_verifier


def assert_exact_minimum(values, candidate):
    assert all(sp.factor(value - candidate).is_nonnegative is True for value in values)


def assert_exact_maximum(values, candidate):
    assert all(sp.factor(candidate - value).is_nonnegative is True for value in values)


def test_family_flux_and_conservation():
    for m in (3, 4, 5, 6, 8, 10):
        rs = sc.reactions(m)
        assert len(rs) == m + 2
        assert all(sum(r.y) <= 2 and sum(r.yp) <= 2 for r in rs)
        G, Y = sc.gamma_y(m)
        selected_minor = family_verifier.selected_stoichiometric_minor(m, G)
        assert sp.factor(selected_minor.det()) == 4 * (-1) ** m
        family_verifier.verify_selected_minor(m, G)
        assert G.rank() == m
        assert len(G.nullspace()) == 2
        assert sc.conservation(m).T * G == sp.zeros(1, m + 2)
        a, b = sp.symbols("a b", positive=True)
        assert G * sc.flux(m, a, b) == sp.zeros(m + 1, 1)
        assert sc.A_matrix(m, a, b) == G * sp.diag(*list(sc.flux(m, a, b))) * Y.T


def test_pareto_verifiers_do_not_use_floating_ordering():
    for name in ("frontier_verify_pareto.py", "frontier_verify_pareto_curve.py"):
        text = (ROOT / "independent_verifier" / name).read_text()
        for forbidden in ("float(", ".evalf(", "sp.N("):
            assert forbidden not in text


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
            assert all(sp.sympify(x).is_positive is True for x in hs + ds)
            assert_exact_minimum(ds, ds[1])
            assert_exact_maximum(ds, ds[0])
            assert_exact_minimum(hs, sp.Integer(1))
            assert_exact_maximum(hs, hs[1])
            chiD = sp.factor(ds[0] / ds[1])
            chiH = sp.factor(hs[1])
            assert sp.simplify(chiD - sp.Rational(23, 63) * 91 * r * L) == 0
            assert sp.simplify(chiH - sp.Rational(91 * r - 1, 91 * r) / L) == 0
            assert sp.simplify(chiD - chiH).is_positive is True
            Hs = pc.Hsum(m)
            tau = pc.tau_formula(m, Hs, L)
            num = sp.factor(pc.N0(m, Hs) + tau * pc.Sterm(m, Hs))
            assert num.is_positive is True
            denominator = pc.den_formula(m, L)
            assert denominator.is_negative is True
            assert sp.factor(num / denominator).is_negative is True
            Hmat = sp.diag(*hs)
            Delta = sp.diag(*pc.Deff(m))
            right = pc.rcrit(m)
            left = pc.ellref(m)
            transformed_left = Hmat.inv() * left
            scaled_operator = Hmat * (pc.A(m) - Delta)
            assert sp.simplify(scaled_operator * right) == sp.zeros(m + 1, 1)
            assert sp.simplify(scaled_operator.T * transformed_left) == sp.zeros(m + 1, 1)
            assert scaled_operator.rank() == m
            # A generalized vector would solve scaled_operator*v=right.
            # Exact augmented-rank inconsistency rules that out.
            assert scaled_operator.row_join(right).rank() == m + 1
            transformed_numerator = sp.factor(
                (transformed_left.T * Hmat * Delta * right)[0]
            )
            unit_numerator = sp.factor((left.T * Delta * right)[0])
            assert transformed_numerator == unit_numerator
            assert unit_numerator == pc.eta_num(m, Hs)
            assert unit_numerator.is_negative is True


def test_pareto_minimax_is_exactly_at_lower_endpoint():
    nu = sp.symbols("nu", integer=True, positive=True)
    L = sp.symbols("L", positive=True)
    chiD = sp.Rational(2093, 63) * nu * L
    chiH = (91 * nu - 1) / (91 * nu * L)
    assert sp.diff(chiD, L).is_positive is True
    assert sp.diff(chiH, L).is_negative is True
    assert sp.factor(sp.Rational(27209, 2430) - 1) > 0
    ratio_minus_one = sp.factor(
        sp.Rational(136045, 36) * nu / (91 * nu - 1) - 1
    )
    assert sp.simplify(
        ratio_minus_one - (132769 * nu + 36) / (36 * (91 * nu - 1))
    ) == 0
    assert ratio_minus_one.is_positive is True


def test_near_threshold_affine_ansatz_and_printed_source():
    for m in (3, 4, 5, 6, 8, 10):
        u, v, p, q = sp.symbols("u v p q", nonzero=True)
        right = sp.Matrix(
            [1]
            + [
                -(u + v * sp.Rational(m - 1 - i, m - 2))
                for i in range(2, m)
            ]
            + [-p, q]
        )
        diffusion = [
            -2 + u + p + 2 * q,
            sp.factor(
                (1 + 2 * p - u - v * sp.Rational(m - 3, m - 2))
                / (u + v * sp.Rational(m - 3, m - 2))
            ),
        ]
        diffusion += [
            sp.factor(v / ((m - 2) * u + v * (m - 1 - i)))
            for i in range(3, m)
        ]
        diffusion += [
            sp.factor((2 * u - 5 * p - 2 * q - 1) / p),
            sp.factor((2 - 2 * p - 4 * q) / q),
        ]
        residual = (pc.A(m) - sp.diag(*diffusion)) * right
        assert all(sp.factor(entry) == 0 for entry in residual)

    epsilon, omega, theta, M, nu, k = sp.symbols(
        "epsilon omega theta M nu k", positive=True
    )
    p = epsilon
    u = 1 + (2 - omega) * epsilon + theta * epsilon**2
    v = omega * epsilon - theta * epsilon**2
    q = (
        sp.Rational(1, 2)
        - (sp.Rational(1, 2) + omega) * epsilon
        + (theta - M / 2) * epsilon**2
    )
    d_z = sp.factor((2 - 2 * p - 4 * q) / q)
    d_i = sp.factor(v / (nu * u + v * k))
    sum_interior = sp.factor(
        sp.summation(sp.series(d_i, epsilon, 0, 3).removeO(), (k, 0, nu - 1))
    )
    excess = sp.factor(
        sp.series(d_z - 8 * sum_interior, epsilon, 0, 3).removeO()
    )
    expected = 4 * epsilon**2 * (
        M + 6 * omega + 3 * omega**2 - omega**2 / nu
    )
    assert sp.factor(excess - expected) == 0

    supplement = (ROOT / "manuscript" / "supplement.tex").read_text()
    assert r"\nu=1+(2-t)\varepsilon" not in supplement
    assert r"u=1+(2-t)\varepsilon" not in supplement
    for marker in (
        r"r^{\rm aff}",
        r"(A_m-D)r^{\rm aff}=0",
        r"d_1=-2+u+p+2q",
        r"d_m=\frac{2u-5p-2q-1}{p}",
        r"d_Z=\frac{2-2p-4q}{q}",
        r"u=1+(2-\omega)\varepsilon+\theta\varepsilon^2",
        r"v=\omega\varepsilon-\theta\varepsilon^2",
        r"(\omega,\theta,M)=(2/9,1/2,1)",
    ):
        assert ''.join(marker.split()) in ''.join(supplement.split())

    certificate = json.loads(
        (ROOT / "independent_verifier" / "pareto_all_m_certificate.json").read_text()
    )
    bounds = certificate["bounds"]
    assert bounds["harmonic_bounds"]["upper"] == "nu/(90*nu+1)"
    assert bounds["reference_N0_lower_bound"]["shift"] == "nu=v+1"
    assert "8*nu-1" in bounds["reference_N0_lower_bound"]["denominator"]
    assert bounds["tau_bound"]["nu_ge_2_sqrt_bound"] == "sqrt(3*nu) <= 5*nu/4"
    assert bounds["tau_bound"]["claim"] == (
        "tau(hfrak,L) < 1/20 for hfrak>=1/91 and L>=1/sqrt(3*nu)"
    )
    assert bounds["tau_bound"]["monotone_in_hfrak"] == "decreasing"
    assert "monotone_in_H" not in bounds["tau_bound"]
    assert bounds["cubic_conclusion"]["claim"] == (
        "N_L=N0+tau*S > 1/200 and ell^T Hmat^{-1}r<0, hence c<0"
    )
    path = certificate["near_threshold"]["general_affine_path"]
    assert path == {
        "p": "epsilon",
        "u": "1+(2-omega)*epsilon+theta*epsilon^2",
        "v": "omega*epsilon-theta*epsilon^2",
        "q": "1/2-(1/2+omega)*epsilon+(theta-M/2)*epsilon^2",
        "delta_leading": "4*(M+6*omega+3*omega^2-omega^2/nu)*epsilon^2",
    }


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


def test_printed_exposition_identities_and_modulus_sources():
    exposition_identities.verify()


def test_77_and_84_term_source_mutations_are_rejected(tmp_path):
    unit_source = ROOT / "independent_verifier" / "improved_modulus_certificate.json"
    unit_payload = json.loads(unit_source.read_text())
    unit_payload["improved_mode"]["terms"][0]["coefficient"] = "2"
    mutated_unit = tmp_path / "mutated_unit_modulus.json"
    mutated_unit.write_text(json.dumps(unit_payload))
    with pytest.raises(AssertionError):
        exposition_identities.verify_modulus_source_polynomials(
            unit_certificate=mutated_unit,
        )

    pareto_source = ROOT / "independent_verifier" / "pareto_all_m_certificate.json"
    pareto_payload = json.loads(pareto_source.read_text())
    coefficient = pareto_payload["modulus"]["spatial"]["terms"][0][
        "coefficient_in_A_ascending"
    ]
    coefficient[0] = str(sp.Rational(coefficient[0]) + 1)
    mutated_pareto = tmp_path / "mutated_pareto_modulus.json"
    mutated_pareto.write_text(json.dumps(pareto_payload))
    with pytest.raises(AssertionError):
        exposition_identities.verify_modulus_source_polynomials(
            pareto_certificate=mutated_pareto,
        )


def test_printed_rational_identity_mutation_is_rejected(tmp_path):
    source = ROOT / "data" / "sign_certificate_tables.tex"
    mutated_text = source.read_text().replace(
        r"C_m=-\frac{215P_C(m)}",
        r"C_m=-\frac{214P_C(m)}",
        1,
    )
    assert mutated_text != source.read_text()
    mutated = tmp_path / "mutated_sign_certificate_tables.tex"
    mutated.write_text(mutated_text)
    with pytest.raises(AssertionError):
        exposition_identities.verify_printed_scalar_table(mutated)


def test_printed_modulus_table_mutation_is_rejected(tmp_path):
    source = ROOT / "data" / "certificate_tables.tex"
    mutated_text = source.read_text().replace(
        r"10 & 0 & $1$\\",
        r"10 & 0 & $2$\\",
        1,
    )
    assert mutated_text != source.read_text()
    mutated = tmp_path / "mutated_certificate_tables.tex"
    mutated.write_text(mutated_text)
    with pytest.raises(AssertionError):
        exposition_identities.verify_printed_modulus_table(mutated)


def test_printed_triad_table_mutation_is_rejected(tmp_path):
    source = ROOT / "data" / "triad_routh_gap.tex"
    mutated_text = source.read_text().replace("4 a^{2}", "5 a^{2}", 1)
    assert mutated_text != source.read_text()
    mutated = tmp_path / "mutated_triad_routh_gap.tex"
    mutated.write_text(mutated_text)
    with pytest.raises(AssertionError):
        exposition_identities.verify_printed_triad_table(mutated)


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
    assert 'Let $n\\ge2$' in sec
    assert 'sum_{|I|=n-1}a_I>0' in sec
    assert 'at most one' not in sec
    assert '\\label{thm:diffusionray}' in sec


def test_threshold_and_algebraic_simplicity_precision_closures():
    main=(ROOT/'manuscript'/'main.tex').read_text()
    supplement=(ROOT/'manuscript'/'supplement.tex').read_text()
    proof_criterion=(ROOT/'proof_audit'/'exact_diffusion_criterion.tex').read_text()

    assert 's_*(H,D)' not in main
    assert 's_*(H,D)' not in proof_criterion
    assert 's_*(a,b,H,D)' in main

    compact_main=''.join(main.split())
    compact_supplement=''.join(supplement.split())
    derivative_formula=(
        r"\Pi_m'(0)=\frac{7043400m-13600927-7043400\mathfrakh_m}{255150}"
        r"=-\frac{163}{45}\,\ell^Tr>0"
    )
    assert derivative_formula in compact_main
    assert derivative_formula in compact_supplement
    for marker in (
        r'\ker\!\left[\mathsfH_m(L)(A_m-\Delta_m)\right]',
        r'\mathsfH_m(L)(A_m-\Delta_m)v=r',
        r'Fredholmofindexzero',
        r'(\pi/2)\ell^TD_mr\ne0',
    ):
        assert marker in compact_main

    for compact in (compact_main, compact_supplement):
        assert r'r=(r_1,\ldots,r_m,r_Z)^T' in compact
        assert r'\ell=(\ell_1,\ldots,\ell_m,\ell_Z)^T' in compact
        assert r'\widetilde\ell(L)=\mathsfH_m(L)^{-1}\ell' in compact
        assert r'c_m(L)=\frac{N_m(L)}{\widetilde\ell(L)^Tr}' in compact

    pareto_theorem=main.split(r'\label{thm:pareto}',1)[1].split(r'\end{theorem}',1)[0]
    compact_pareto=''.join(pareto_theorem.split())
    assert r'On$(0,\pi)$withhomogeneousNeumannboundaryconditions' in compact_pareto
    assert (
        r'\partial_tx=f_m\!\left(\mathsfH_m(L)x\right)+(1-\mu)'
        r'D_m^{\rmphys}(L)\partial_{\xi\xi}x'
    ) in compact_pareto
    assert 'physical fixed-mass covector becomes' in ' '.join(main.split())

    ill_typed = (
        r'\ell_m^T', r'\widetilde\ell_m',
        r'\operatorname{span}\{r_m', r'\operatorname{span}\{\ell_m',
        r'D_mr_m',
    )
    corpus=main+supplement
    assert all(token not in corpus for token in ill_typed)

    m,hfrak=sp.symbols('m hfrak',integer=True,positive=True)
    derivative=(7043400*m-13600927-7043400*hfrak)/sp.Integer(255150)
    assert sp.factor(
        derivative+sp.Rational(163,45)*dc.ellr_formula(m,hfrak)
    )==0


def test_scope_and_certificate_honesty_markers():
    text=(ROOT/'manuscript'/'main.tex').read_text()
    supplement=(ROOT/'manuscript'/'supplement.tex').read_text()
    assert '\\mathfrak S_m' in text
    assert 'not classified here' in text
    assert 'not asserted to be an intrinsic' in text
    assert 'wave instability' in text
    assert 'b=2a' in text
    assert 'N_m(L)>1/200' in text
    assert 'square-root-balanced' not in text
    assert 'right panel' not in text
    for marker in (
        r'\label{eq:fourier-fredholm}',
        r'\label{eq:high-mode-inverse}',
        r'Fredholm of index zero',
        r'sectorial with compact resolvent',
        r'neither complete long cycle',
    ):
        assert marker in text
    for marker in (
        r'B_m^{\rm core}',
        r'\det B_m^{\rm core}=2a^2b',
        r'fixed-mass subspaces invariant',
        r'2\|D_m^{-1}\|k^{-2}',
    ):
        assert marker in supplement


def test_generic_cubic_recurrence_bridge_is_standalone_and_aggregated():
    verifier = ROOT / "independent_verifier" / "verify_generic_cubic_recurrence.py"
    source = verifier.read_text()
    for forbidden_import in (
        "from common import",
        "from core import",
        "from pareto_core import",
        "from stable_core import",
    ):
        assert forbidden_import not in source

    result = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.stdout.strip() == "GENERIC_CUBIC_RECURRENCE_PASS"

    aggregate = (
        ROOT / "independent_verifier" / "verify_symbolic_certificates.py"
    ).read_text()
    assert '"verify_generic_cubic_recurrence.py"' in aggregate


def test_every_direct_verifier_entrypoint_rejects_optimized_python():
    verifier_dir = ROOT / "independent_verifier"
    support_modules = {"common.py", "core.py", "pareto_core.py", "stable_core.py"}
    entrypoints = sorted(
        path for path in verifier_dir.glob("*.py") if path.name not in support_modules
    )
    # The 38 pre-existing direct entrypoints plus the generic cubic bridge.
    assert len(entrypoints) == 39

    for entrypoint in entrypoints:
        result = subprocess.run(
            [sys.executable, "-O", str(entrypoint)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        combined = result.stdout + result.stderr
        assert result.returncode != 0, f"{entrypoint.name} ran with assertions disabled"
        assert "requires assertions" in combined, entrypoint.name


def test_replay_preserves_release_manifest_and_separates_self_consistency():
    release_dir = ROOT / "release"
    if release_dir.is_dir():
        full_replay = (release_dir / "one_command_replay.sh").read_text()
        refresh = (release_dir / "refresh_packages.sh").read_text()
        portable_replay = refresh.split(
            'cat > "$PUB/replay.sh" <<\'EOF\'', 1
        )[1].split("\nEOF", 1)[0]
        cases = (
            (
                "full replay",
                full_replay,
                'BASELINE_MANIFEST="$ROOT/release/sha256_manifest.txt"',
                "python computation/generate_current_profile_data.py",
            ),
            (
                "portable replay template",
                portable_replay,
                'BASELINE_MANIFEST="$ROOT/sha256_manifest.txt"',
                "python computation/generate_current_profile_data.py",
            ),
        )
    else:
        # In the portable package, exercise the materialized replay directly;
        # the canonical release-only orchestration is intentionally absent.
        cases = (
            (
                "portable replay",
                (ROOT / "replay.sh").read_text(),
                'BASELINE_MANIFEST="$ROOT/sha256_manifest.txt"',
                "python computation/generate_current_profile_data.py",
            ),
        )
    for name, script, baseline_definition, first_generator in cases:
        baseline_check = 'sha256sum -c "$BASELINE_MANIFEST"'
        preserve = 'cp "$BASELINE_MANIFEST" "$REPLAY_STATE/downloaded_manifest.txt"'
        unchanged = 'cmp -s "$BASELINE_MANIFEST" "$REPLAY_STATE/downloaded_manifest.txt"'
        exact_check = 'sha256sum -c "$EXACT_BASELINE"'
        self_definition = "SELF_MANIFEST="
        self_write = '> "$SELF_MANIFEST"'

        for marker in (
            baseline_definition,
            baseline_check,
            preserve,
            'EXACT_BASELINE="$REPLAY_STATE/exact_artifacts.sha256"',
            'manifest_line="$(awk -v target="./$relative_path"',
            '"$REPLAY_STATE/downloaded_manifest.txt")"',
            '>> "$EXACT_BASELINE"',
            unchanged,
            exact_check,
            self_definition,
            self_write,
            "REPLAY_SELF_CONSISTENCY_PASS",
        ):
            assert marker in script, f"{name} lacks {marker}"

        assert script.index(baseline_definition) < script.index(baseline_check)
        assert script.index(baseline_check) < script.index(preserve)
        assert script.index(preserve) < script.index(first_generator)
        assert script.index(unchanged) < script.index(exact_check)
        assert script.index(exact_check) < script.index(self_definition)
        assert script.index(self_definition) < script.index(self_write)
        assert '> "$BASELINE_MANIFEST"' not in script
