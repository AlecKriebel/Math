# Research log: exact cyclic Bell Tsirelson bound

All timestamps use America/Los_Angeles.

## 2026-07-26

- **13:13 PDT - Workstream opened.** Created a dedicated research package for
  Conjecture 1 of Perito--D'Avino--Jung--Mironowicz--Acin--Augusiak,
  arXiv:2606.21362v3.
- Preserved the supplied candidate package in
  `/Users/alec/Downloads/cyclic_bell_solution/` without modification and
  recorded its hashes in `SOURCE_SNAPSHOT.md`.
- Confirmed from the full v3 paper that Conjecture 1 concerns the reduced
  functional \(\mathcal I_d\), not the barred randomness functional
  \(\bar{\mathcal I}_d\). Appendix A.2 proves only
  \(\beta_Q(\mathcal I_d)\le d\sqrt2\), and the July 21 note added concerns a
  different randomness construction rather than this conjecture.
- Began three independent checks: a line-by-line proof audit, a public
  prior-art audit, and a repository/Pages integration audit. No outside party
  was contacted.
- Repository isolation decision: the ordinary checkout and the existing
  `main` worktree both contain unrelated active research. This work is being
  prepared from the exact current `origin/main` snapshot in a detached
  publication worktree so that no unrelated files are touched. The eventual
  release target remains `main`, as required by the repository policy.

### Preliminary mathematical checkpoint

- Re-derived the polar-decomposition identity. The polar factor need only be a
  partial isometry: its initial projection acts as the identity on the support
  of \(|C|\). This removes the finite-dimensional unitary-extension caveat and
  makes the upper-bound identity valid for bounded operators on arbitrary
  Hilbert spaces.
- Re-derived the scalar maximum
  \[
  \max_{|z|=1}\sum_{y=0}^{d-1}|1+\omega^y z|
  =2\csc\!\left(\frac{\pi}{2d}\right),
  \]
  including the exact equality condition
  \(z^d=(-1)^{d-1}\).
- Checked the proposed polar-form attaining strategy algebraically. The
  load-bearing order relation follows from writing the Bob unitary as a
  weighted cyclic shift and using
  \(\prod_{r=0}^{d-1}(1+a\omega^r)=1-(-a)^d\); the two facts cited in the
  earliest summary are not by themselves a proof, so the full conjugation and
  product argument will appear in the manuscript.

