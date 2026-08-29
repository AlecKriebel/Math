# Independent spot checks

These checks execute referee-authored scripts and import no reviewed-package
module. Six scripts are frozen copies from the prior independent review and
are rerun against the new sealed package; the revised-cut script also reads no
stored certificate and derives its counts and Fourier minor from scratch.
Execution is offline in `offline_reviewer_checks.sb` with clean environment
variables and outputs confined to `results/`.

The package's complete 55-command regeneration remains the primary exhaustive
machine replay. These checks are deliberately different, bounded spot checks
of formulas, witness reconstruction, ledgers, and interval arithmetic.
