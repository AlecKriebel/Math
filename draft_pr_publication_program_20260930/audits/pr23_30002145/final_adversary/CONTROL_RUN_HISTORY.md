# Fresh-control run history

2026-10-01T20:38:42.348564+00:00: Initial run completed all mathematical assertions, then failed while serializing a SymPy integer in the result: TypeError: Object of type One is not JSON serializable. Initial script SHA256 233b95928d712796ce84496cf19ea911ef9736445e6e200f875affde1d50b2ce. Preserved initial script in ignored tmp/fresh_controls_initial.py. Repair adds default=str to JSON serialization only; no equation, expected value, tolerance, control or claim changes.

2026-10-01T20:41:19.620638+00:00: Corrected run exited0; all12 grouped new exact controls passed with Python3.9.6/SymPy1.14.0. No mathematical assertion was changed.

2026-10-01T20:47:38.214493+00:00: Final receipt inspection caught an audit-script catalog lookup comparing the string numeric-ID field to an integer. Converted both sides to strings and added uniqueness assertion; primary-family provenance replay had already confirmed the correct selected catalog. This changes audit metadata extraction only, not candidate claims or mathematical controls. Final integrity replay rerun. Final fresh suite now contains13 controls after the2011 source-wording countercontrol; all13 passed.
