# A credited combinatorial proof of the two-thirds leaf limit

**Problem 30002545: already_solved, 1/5 substantive author turns.** The full source-requested proof presentation passed independent AI-assisted review, including its no-generating-functions, no-induction and no-assumed-limit requirements. The result is a reconstruction from classical bijections and a known exact mean, not a new theorem or historical-priority claim.

For n≥2, a uniform vertex of a uniform decreasing rooted plane tree on [n] is a leaf with probability (2n−1)/(3n). The limit is 2/3; the one-vertex tree has probability 1.

The [complete proof](TURN_1.md) identifies leaves with empty middle slots of ternary increasing trees by the credited Koganov–Janson and Gessel correspondences. Rotating all three slot types equates their aggregate counts. Static interval inverses establish the bijections without inductive enumeration. No formula counting the trees is needed.

Read [the independent review](final_review/ADVERSARIAL_REVIEW.md) for its full-source/method verdict and limits. This is AI-assisted checking, not human peer review or formal certification. The adjective “simple” in the source has no objective threshold; the method and entire mathematical conclusion were checked.

Run python verify_turn1.py and compare stdout with TURN_1_CHECKS.json: 3,346,451 exact controls over 146,599 finite objects through n=8. Run python final_review/independent_checks.py for 9,483 separately written controls over 1,069 objects. The finite checks supplement the all-size proof.

Author files retain their original first-turn candidate and pending-review wording as historical freeze records. The completed review is under final_review. Both frozen manifests remain unchanged. Source PDFs are linked and hash-pinned rather than republished. The original report's printed total-leaf typo is documented but is not the research conclusion.
