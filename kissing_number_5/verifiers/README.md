# Verifiers

Verification programs must be materially simpler than discovery programs and
must reject malformed, rounded, or incomplete certificates.

`verify_d5.py` uses exact integer arithmetic.  It treats each stored row \(r\)
as \(r/\sqrt2\), so normalization and the \(1/2\) pair bound reduce respectively
to `r·r == 2` and `r·s <= 1`.
