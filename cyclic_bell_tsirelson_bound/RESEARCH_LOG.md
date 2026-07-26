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

### Verification and manuscript checkpoint

- **13:22 PDT - Analytic manuscript compiled.** Produced a seven-page
  self-contained note with the arbitrary-unitary theorem, scalar equality
  cases, exact positive-factor certificate, complete order-\(d\) proof, barred
  functional corollary, attribution, and explicit nonclaims.
- Rendered all seven pages to images and visually checked every page. One
  transcription defect in the boxed global certificate (missing displayed
  plus signs) was found and corrected before release.
- The deterministic verifier passed:
  - exact low-dimensional radical identities;
  - 21 polar-factor trials, including 15 singular cases;
  - 10 complete global-certificate trials with arbitrary unitaries and varied
    Alice/Bob dimensions;
  - every scalar equality root and all 77 Bob observables for
    \(d=2,\ldots,12\);
  - Bell saturation and top-eigenvalue checks; and
  - direct agreement of the polar Bob observables with Eqs. (15) and (45) of
    the originating paper.
- An extended non-default sweep through \(d=20\) also passed. These are finite
  sanity checks; the all-dimensional theorem rests on the analytic proof.
- The public-prior-art audit found no proof of Conjecture 1. It confirmed that
  the v3 note added cites a different randomness construction and that the
  nearest concurrent general SOS framework treats other Bell families.
  Priority remains explicitly provisional because public searches cannot rule
  out unpublished, unindexed, or simultaneous work.
- **13:35 PDT - Independent audit accepted the corrected proof.** A separate
  line-by-line adversarial review returned an accept verdict after checking
  normalization, adjoints, transpose conventions, singular polar factors,
  scalar equality cases, and the weighted-shift proof of \(B_y^d=I\). No
  mathematical blocker or hidden admissibility assumption was found.

### Post-publication feedback audit

- **14:52 PDT - Adversarial review of external feedback.** Three independent
  checks compared every suggested correction with the released source.
- Rejected the claimed mathematical error in the phase function: the released
  manuscript already defined
  \(q(z)=(1+\overline z)/|1+z|\), so
  \(Q_y=q(W_y)Z^\dagger\) was correct. The counterexample in the feedback used
  the different function \((1+z)/|1+z|\). The revision nevertheless adopts
  the clearer equivalent notation
  \(p(z)=(1+z)/|1+z|\) and
  \(Q_y=p(W_y)^\dagger Z^\dagger\), with a dedicated regression check.
- Accepted the commuting-operator strengthening after re-deriving the polar
  identity in commuting operator algebras. The certificate bounds
  \(\beta_{qc}\); the finite attaining strategy and
  \(\mathcal Q_q\subseteq\mathcal Q_{qa}\subseteq\mathcal Q_{qc}\) give
  equality of all three values for this functional.
- Confirmed directly from Appendix A.2, Proposition 3, of the originating
  paper that its general bound is \(d\sqrt2\).
- Accepted the convention, exposition, and verification improvements:
  explicit source Fourier constraints, the qutrit Bob formula, an explanation
  of the roots-of-unity reindexing, the odd-parity boundary identity, and the
  count \(\sum_{d=2}^{12}d=77\).
- Expanded the related-work coverage after checking the primary records for
  Buhrman--Massar, SATWAP, the modified Buhrman--Massar SOS family, CHSH mod 3,
  and the contemporaneous randomness and high-dimensional SOS papers. None
  was found to contain the present all-\(d\) bound.
