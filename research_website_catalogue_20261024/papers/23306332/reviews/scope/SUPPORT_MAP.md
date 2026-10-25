# Published support map

Every listed file is byte-bound in `CUSTODY.json` and `reader-manifest.json`. All allowed bodies were read completely and statically; no published helper was executed. Opaque bodies were hashed without reading content. No source was edited.

| Body | Reader status | Evidence role and limit |
|---|---|---|
| `nonunique_nearest_stable_complex_quadratics.tex` | complete_read | C1–C4 analytic proof source |
| `README.md` | complete_read | Package description, scope and execution instructions; instructions not executed |
| `publication_metadata.json` | complete_read | Authored bibliographic description; compared to Zenodo metadata |
| `LICENSE.md` | complete_read | CC BY4.0 license of original materials |
| `verify_exact.py` | static_complete_read | 80 rational t values; root/derivative/support identities plus mixed metric controls; no nearest-pair solver |
| `verify_function_boundary.py` | static_complete_read | 90-digit Decimal, fixed seed, finite function-boundary supports/controls; not interval arithmetic |
| `check_archive_hashes.py` | static_complete_read | Administrative archive hash helper; not run |
| `expected_exact.json` | complete_read_authored_expected_output | Expected output only; not fresh execution evidence |
| `expected_function_boundary.json` | complete_read_authored_expected_output | Expected output only; not fresh execution evidence |
| `HASHES.json` | complete_read | 11 body hashes; self excluded; administrative independent byte comparison done |
| `SOURCE_PRIORITY.md` | opaque | Dedicated authored prior opinion/priority memorandum, quarantined |
| `SOURCE_PROVENANCE.json` | opaque | Dedicated authored provenance/assessment body, quarantined |

The separate published PDF has six pages, all read and visually inspected. No embedded file, JavaScript, form, nested archive, hidden member, symlink, additional reader PDF or external TeX include was found. The standalone TeX uses standard packages. Administrative fresh hashing/CRC/member comparison is distinct from running `check_archive_hashes.py`.

`verify_exact.py`: exact `Fraction` arithmetic on 80 dyadic t values; checks factorization, 4 monic/6 full real derivatives, support/distance identities and a mixed metric. Static count/description only. It does not compute a multiply projected target or quantify over all SPD matrices. `expected_exact.json` status is an authored expectation.

`verify_function_boundary.py`: Decimal precision90, fixed seed26330000170; finite scalar boundary, coefficient-support, adverse-curvature and horizontal-normal controls. Numerical arithmetic is not interval-certified, and finite samples do not prove the analytic uniform/local/limiting statements. `expected_function_boundary.json` is authored expected output. Incidental PASS strings are quarantined.

The mathematical proof obligations remain: proximal-normal membership at every fixed path point; nonproximity of the limiting normal; correct imported projection hypotheses; monic closedness/attainment; full-degree compact localization; all fixed SPD metrics including cross-coordinate terms; epigraph normal geometry; finite-subgradient characterization, diffeomorphism transport and uniform local function support.
