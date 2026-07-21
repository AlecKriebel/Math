# Package manifest

- `full_symmetric_monodromy.md`: complete proof source.
- `output/pdf/full_symmetric_monodromy.pdf`: rendered two-page research note.
- `verify.py`: exact checks for the uniform family through any requested degree.
- `verify_announced_stdlib.py`: dependency-free exact verification of the
  announced Jacobian counterexample.
- `src/render_note.py`: deterministic ReportLab PDF renderer.
- `requirements.txt`: Python dependency used by `verify.py`.
- `README.md`: scope, novelty caveat, and reproduction instructions.

The package was finalized on 20 July 2026. It presents a structural refinement
of the Alpoge-Gallagher every-degree construction, not an independent discovery
of the underlying Jacobian counterexamples.
