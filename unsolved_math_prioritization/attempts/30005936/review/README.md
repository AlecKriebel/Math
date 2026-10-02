# Replaying the independent review

ADVERSARIAL_REVIEW.md contains the source and analytic verdict, bound to the final author SHA-256 manifest. AUTHOR_REPLAY.json records the exact five-script replay and nested/source integrity checks.

Run python check_independent.py (standard library) and compare stdout to INDEPENDENT_CHECKS.json. Run python check_barrier.py with SymPy1.14.0 and compare to BARRIER_CHECKS.json. These scripts have no absolute author-path dependency. They check supplemental algebra and cannot substitute for the analytic stochastic-calculus review.

PRELIMINARY_AUDIT.md is intermediate review work, outside the frozen publication manifest. Raw source PDFs/screenshots/imports are not included in this review bundle. No publication or repository status change is performed by this review.
