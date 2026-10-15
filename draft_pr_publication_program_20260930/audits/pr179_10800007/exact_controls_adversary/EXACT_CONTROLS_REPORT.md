# Independent universal-control mechanism

exact_polynomial_controls.py implements sparse multivariate rational polynomial addition, multiplication, differentiation, and substitution, independently of both supplied scripts. It differentiates the full six-parameter system, proves coefficient identities by exact polynomial equality, and computes each quadratic norm range from its endpoints and its rational critical point. It uses explicit exceptions; optimization cannot suppress its checks.

The checker verifies F_slice=x²−y²−u, 2G_slice=2xy−v; |zeta|²−|embedding(zeta)|²=3v²/4; the general Jacobian determinant; its slice determinant 2(x²+y²); squared-loop norm identity; full path interval coverage; polynomial continuity and exact seam; root endpoints ±1; closed squared parameter endpoints; and the example strict disk inequality. The universal path bounds are exactly 1/2 to 1, with minima at t=1/2 and t=3/2, and maxima at piece endpoints.

For arbitrary r>0, the written argument chooses 0<c<sqrt(r); the universal norm bound implies |c²gamma²|<=c²<r. The code example c=1/3,r=1/8 is only an input sanity control, not a finite substitute for the arbitrary-radius argument.

The full derived Jacobian is 2x²+2y²+(a1+2b2)x+(2b1−a2)y+a1b2−a2b1. An adversarial sign change in −a2b1 is rejected even though it would vanish on the constant-coefficient slice, illustrating additional independence from slice-only rational tests.

| Model | Ordinary | Optimized | Reason |
|---|---|---|---|
| baseline | PASS | PASS | Correct universal controls. |
| wrong_embedding_b0 | FAIL | FAIL | universal_second_slice_identity |
| wrong_system_xy | FAIL | FAIL | universal_second_slice_identity |
| wrong_general_jacobian | FAIL | FAIL | universal_general_jacobian |
| wrong_path_seam | FAIL | FAIL | universal_path_nonzero_and_bounded |
| wrong_path_bound | FAIL | FAIL | universal_path_nonzero_and_bounded |
| bounded_but_discontinuous_seam | FAIL | FAIL | polynomial_path_continuous_join |
| root_endpoints_equal | FAIL | FAIL | exact_path_endpoints |
| path_through_zero | FAIL | FAIL | universal_path_nonzero_and_bounded |
| positive_control_reverse_orientation | PASS | PASS | A distinct valid lower semicircular polygon has the same exact endpoint obstruction and should pass. |
| zero_scale | FAIL | FAIL | positive_example_scale |
| touching_open_disk_boundary | FAIL | FAIL | strict_example_disk_inclusion |
| continuous_hidden_zero | FAIL | FAIL | supported_norm_degree_at_most_two |

The supported norm class has degree at most two. The degree-66 hidden-zero path is rejected as unsupported; this fail-closed behavior is not advertised as a universal high-degree inequality solver. The separate exact evaluation at t=1/128 proves that mutant actually fails the required lower bound. A valid reverse-orientation path passes in both modes, showing that the mechanism accepts distinct valid geometric controls.

The code does not prove connectedness, infer continuity of hypothetical selections from samples, or decide any general sectional genus. Its output explicitly states that topological assumptions are not verified by code. The mathematical argument supplies those analytic steps. All 26 runs, including intentional failures and the alternative valid path, are preserved in execution_evidence/exact_control_runs.json.
