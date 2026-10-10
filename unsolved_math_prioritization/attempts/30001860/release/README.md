# 30001860: scoped reciprocal-log bounds and statement audit

Problem: **30001860 / OWR-11129-006**, rank **707**, *Asymptotic Proportion of Q in Classical Groups*.

**Disposition: partial; broad asymptotic-value request unresolved here.** No claim of novelty, global openness, publication, or human review.

The primary OWR statement defines even-order elements whose powered involution has fixed-space dimension in **[N/3,2N/3)**. Its printed **O(log N)** subquestion is automatically true for a probability. The cited Lübeck–Niemeyer–Praeger paper separately discusses the nontrivial reciprocal-log upper bound.

`PROOF.md` gives a complete derivation, using the explicitly credited published maximal-torus counting identity, of:

- Uniform odd-q **O(1/log N)** for **GL_N(q)** and the unitary isometry group **U_N(q)**.
- Uniform odd-q **O(1/log r)** for **Sp_(2r)(q), SO_(2r+1)(q), SO^+_(2r)(q), SO^-_(2r)(q)**.
- Combined with LNP's lower bound, **Theta(1/log rank)** for those families.
- Fixed-q **Theta_q(1/log N)** for intermediate SL/GL and SU/U groups, without claiming q-uniform upper bounds there.
- Exact centralizer reductions, an exact GL_2 formula showing that field growth cannot replace rank growth, and a strict-endpoint counterexample to defining the predicate on an arbitrary projective lift.

No asymptotic equivalent or limiting coefficient is obtained. Conformal, disconnected, Spin/half-spin, and quotient variants are not silently included.

Run the bounded exact controls with:

    python3 verify.py --sp4 --output verification_results.json

Only standard-library Python is needed. These enumerate small matrix groups exactly and compare with the torus model, check finite valuation and coefficient identities, and test endpoint/field/group negative controls. They do not prove asymptotics. See the proof for the infinite argument.

The exact public catalog page could not be read: the web tool reported inaccessible and direct retrieval returned HTTP 403. The supplied descriptor identifies the problem and source, but the statement body and prior raw AI records were unavailable. The primary OWR source, including its page image, was independently checked. `SOURCE_VERIFICATION.json` records public URLs, hashes, sizes, scope of inspection, and limits. Source PDFs, extracts, images, raw records, and coordination materials are not included.

The research bundle is prepared for independent audit. Authored claims must not be treated as independently verified merely because these files exist.
