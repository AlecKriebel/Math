# Narrow cross-review: noncanonical scalar coefficient representations

Target: `137ffa9f1a340f621651395ad0236cf1bdadb51c`.
Completed 2026-09-07 local time.

**Assessment:** a real, narrowly contained rendering/validation inconsistency for noncanonical input. It does not invalidate any shipped coefficient, printed identity, or theorem, and does not change the mathematical proofreading verdict.

The unit homogeneous certificate's first row has powers `[10,0]` and the exact coefficient string `"1"`. Replacing only that value by JSON boolean `true` or the string `"1e0"` preserves the value obtained by the exact readers: both are coerced by `SymPy.Rational` to 1. However, the generator converts the original representation to text and emits `True` or `1e0` inside math delimiters. These are not the ordinary exact-rational notation 1 that the certificate table purports to display. In particular, bare mathematical letters in `$True$` are not a defined rational scalar; `$1e0$` is not rendered as scientific exponent notation.

The independent program `check_scalar_representation.py` derives

\[
E_{35}=|1+\lambda|^2|P(\lambda)|^2-|R(\lambda)|^2,
\]

with the manuscript's degree-four P and degree-two R, and confirms that the coefficient of x^10 is exactly 1. This is also immediate from the leading term: at y=0 the only degree-ten contribution is x^2 times x^8. The program then observes the actual generator's output for the three representations. Results are in `SCALAR_REPRESENTATION_RESULTS.json` and `scalar_representation.log`. It does not alter the frozen source or import the mathematical verifier implementation.

## Contract and precise locations

- `independent_verifier/verify_mode_isolation.py:32` coerces each supplied scalar using `sp.Rational`; the analogous exposition reader does the same.
- `computation/generate_tables.py:18–23` converts the supplied value directly to text, and lines 88–90 insert it into the scalar table.
- `independent_verifier/certificate_schema.json` requires only the outer certificate sections and their fields. It does not specify or enforce the lexical type of individual coefficients.
- The verifier README describes comparison of exact coefficients, but does not define a separate accepted scalar-encoding grammar.

All shipped scalar coefficients use canonical integer/fraction strings. Thus canonical encoding is an implicit producer convention, rather than a checked input boundary. The accepted alternative values do not change the numeric polynomial used in the proof checks; they change its generated presentation. This distinction makes the issue narrower than the previous conflicting A/U-field defect, which has been repaired.

## Bounded remedy and publication impact

Use the same exact rational value for comparison and rendering. One small remedy is to normalize an accepted scalar through exact rational parsing and print its canonical numerator/denominator representation. Another is to require canonical rational strings explicitly in both readers and generator, rejecting booleans and noncanonical strings. Either approach can be covered by these two exact regression cases; no broad parser redesign is needed.

I would classify this as low-priority hardening for malformed or noncanonical external data, not a mathematical submission blocker for the presently correct, frozen preprint. It should be recorded accurately rather than claiming that all possible accepted representations are already checked. The certificate referee separately owns evidence concerning aggregate-check and PDF-audit acceptance; this note makes no independent claim to have rerun those gates.
