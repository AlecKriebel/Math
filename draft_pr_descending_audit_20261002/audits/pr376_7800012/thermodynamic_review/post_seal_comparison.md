# Post-seal corroboration

At 2026-10-03T05:53:40Z, after verdict_seal.md bound the independent verdict, I read the packet's existing final_review/REVIEW.md and final_review/independent_check.py. Its scoped PASS and exact remaining gap agree with this review. That agreement was not an input to the sealed verdict.

The private copied verify_review.py and the existing independent checker each exited zero. Full stdout/stderr are in checks/post_seal_existing_review.* and checks/post_seal_existing_independent.*. The checker reports 984 exact controls. These are recorded as existing-review controls, separately from this thermodynamic review's 17,809 controls.

LiebLoss1992 SectionVII was additionally read directly during the proof audit. It explicitly distinguishes determinant optimization from spectral-sum optimization and gives amplitude-varying counterexamples outside the present uniform unit-hopping square-lattice target. This supplies a useful non-transfer warning, not a target counterexample.
