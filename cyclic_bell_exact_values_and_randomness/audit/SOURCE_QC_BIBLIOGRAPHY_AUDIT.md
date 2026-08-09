# Source, commuting-operator, normalization, and bibliography audit

**Audit date:** 9 August 2026
**Released merged baseline audited:** commit `9cc4d0da42d2c2aea0f5cc5e4d7754ae0350878d`
**Scope:** the seven source/QC/bibliographic items in the author-ready revision
feedback
**Status:** fresh independent replay; no external contact

## Verdict

| Feedback item | Verdict | Required disposition |
|---|---|---|
| Harden the `qc` polar proof using \(\mathcal A''\), commutants, and the canonical partial isometry | **Correct and load-bearing** | Restore the full bicommutant/strong-limit argument. The `qc` theorem survives. |
| Credit the source's \(d\sqrt2\) upper bound and its numerical dimensions | **Correct** | State Proposition 3 and NPA evidence through \(d=6\), while keeping the exact analytic upper bound as the present contribution. |
| Restore the \(d=2,\ldots,6\) radical table | **Correct** | All five radicals check exactly; restore as a compact benchmark table. |
| Identify the polar canonical observables with the source observables, including \(d=3\) | **Correct** | Restore the Fourier sums and qutrit formula with transpose/conjugation conventions explicit. |
| Derive \(\sum_\ell|\lambda_\ell|^2=1\) from the cosecant-square identity | **Correct and load-bearing for the second SOS** | Add the one-line cotangent differentiation proof and its specialization. |
| State the source's Conjecture 2 exactly and say what the counterexample refutes | **Correct, subject to the source's printed normalization inconsistency** | Identify Conjecture 2 by number, repair its value using the operator definition, and state explicitly that its intended scalar-value implication is refuted for \(d\ge4\). |
| Repair NPA and Coccia--Padovan--Vallone bibliography data | **Correct in part** | The released merge has an uncited NPA-2007 item. Its Coccia initials are already correct; the wrong initials occur only in the preserved third historical manuscript and must not be propagated. |

The feedback sentence calling \(d\sqrt2\) “asymptotically close” should be
narrowed. It has the correct linear order, but is not asymptotically tight:
\[
 \frac{d\sqrt2}{2\csc(\pi/(2d))}
 \longrightarrow \frac{\pi}{2\sqrt2}
 =1.1107207345\ldots .
\]
Thus the source bound remains about \(11.1\%\) above the exact value in
relative terms.

## Sources and exact anchors

The controlling primary source is Ignacio Perito, Raffaele D'Avino, Michał
Jung, Piotr Mironowicz, Antonio Acín, and Remigiusz Augusiak,
*Bell inequalities tailored to optimal global randomness certification*,
[arXiv:2606.21362v3](https://arxiv.org/html/2606.21362v3) (21 July 2026).
The relevant anchors in v3 are:

- Section III.2, Eqs. (10)--(17): definitions, source Fourier constraints,
  canonical strategy, and the value \(2\csc(\pi/(2d))\);
- Conjecture 1 immediately after Eq. (17): exactness of the reduced value;
- Conjecture 2 immediately thereafter: the first augmented family's
  maximal-value randomness assertion;
- Appendix A.2, Proposition 3, Eqs. (31)--(35):
  \(\beta_{\mathcal Q}(\mathcal I_d)\le d\sqrt2\);
- Appendix A.3, Table 1: NPA and see-saw values through \(d=6\);
- Section III.1, Eqs. (5)--(9): the qutrit functional, value, Fourier sums,
  and explicit \(B_y\);
- Section IV, Eqs. (18)--(23): Fourier compression, the second family, and
  its SOS;
- Appendix C, Eqs. (44)--(45): the full canonical Bob-observable formula.

Preserved local anchors are:

- `cyclic_bell_tsirelson_bound/main.tex`, lines 90--116 (source bound and
  dimensions), 538--563 (source-observable identification), and 607--620
  (radical table);
- `cyclic_randomness_counterexample/manuscript.tex`, lines 137--167
  (Conjecture 2, normalization, and exact logical implication);
- `minimum_bell_randomness/manuscript.tex`, lines 675--696
  (cosecant-square normalization and second-family SOS).

## 1. Commuting-operator polar decomposition

### Result of the audit

The `qc` upper bound is valid. The short released proof had the right idea but
did not display the closure argument needed to infer that Bob commutes with
the polar partial isometry. No tensor-factor decomposition, finite-dimensional
trace, or tracial state is needed in the upper-bound proof.

Let \(\mathcal A,\mathcal B\subseteq\mathcal B(\mathcal H)\) be unital
star-algebras that commute elementwise, let \(C\in\mathcal A\), and write the
canonical polar decomposition as \(C=V|C|\). Put
\(\mathcal M=\mathcal A''\). Then:

1. \(|C|\), \(|C|^{1/2}\), and
   \((|C|+\varepsilon I)^{-1}\) lie in \(\mathcal M\) by continuous
   functional calculus.
2. The support projection and canonical polar partial isometry satisfy
   \[
   s(|C|)=\operatorname*{s-lim}_{\varepsilon\downarrow0}
      |C|(|C|+\varepsilon I)^{-1},\qquad
   V=\operatorname*{s-lim}_{\varepsilon\downarrow0}
      C(|C|+\varepsilon I)^{-1}.
   \]
   The approximants to \(V\) have norm at most one, and the spectral theorem
   gives strong convergence. Since a von Neumann algebra is strongly closed,
   both limits belong to \(\mathcal M\).
3. Elementwise cross-party commutation is exactly
   \(\mathcal B\subseteq\mathcal A'\). Hence
   \(\mathcal M=(\mathcal A')'\) commutes with every element of
   \(\mathcal B\), including the displayed Bob unitary \(B\).
4. The support-sensitive identities are
   \[
   V^\dagger V=s(|C|),\qquad VV^\dagger=s(|C^\dagger|),\qquad
   |C^\dagger|^{1/2}V=V|C|^{1/2}.
   \]
   Therefore
   \(|C^\dagger|^{1/2}V|C|^{1/2}=C\), while
   \(|C|^{1/2}V^\dagger V|C|^{1/2}=|C|\).

For
\[
 P_{C,B}=|C^\dagger|^{1/2}-V|C|^{1/2}B,
\]
these facts give, without extending \(V\) to a unitary,
\[
 P_{C,B}^\dagger P_{C,B}
 =|C^\dagger|+|C|-CB-B^\dagger C^\dagger.
\]
This proves the positive-factor identity in the commuting model even when
\(C\) has a kernel.

### Replay of the rest of the `qc` theorem

- \(U=A_0^\dagger A_1\) is an Alice unitary.
- \(M_y=I+\omega^yU\) is normal, so
  \(|A_0M_y|=|M_y|\) and
  \(|(A_0M_y)^\dagger|=A_0|M_y|A_0^\dagger\).
- Continuous functional calculus applies the sharp scalar inequality on
  \(\operatorname{spec}(U)\subset\mathbb T\), giving
  \(0\le F_d(U)\le M_dI\).
- Every Alice functional-calculus factor commutes with Bob by the preceding
  bicommutant argument. Summing the positive-factor inequalities therefore
  gives the operator bound in `qc`.
- A finite-dimensional tensor-product strategy attains the same value. The
  inclusions \(q\subseteq qa\subseteq qc\) then force equality of all three
  suprema.

The augmented term uses only \(\operatorname{Re}(A_0B_d)\le I\). The
second-family SOS also has a commuting-operator reading because its expansion
uses only cross-party commutation and Fourier orthogonality within Bob's
algebra. The SOS itself and its value \(d\) remain attributed to the source;
the present new result is the biased permutation maximizer and its randomness
consequence, not a newly invented second-family upper bound.

### Integration-ready replacement proof

> Put \(\mathcal M=\mathcal A''\). Continuous functional calculus places
> \(|C|\), its square root, and \((|C|+\varepsilon I)^{-1}\) in
> \(\mathcal M\). Strong closure then gives
> \(s(|C|)=\mathrm{s}\!\!\lim_{\varepsilon\downarrow0}
> |C|(|C|+\varepsilon I)^{-1}\) and
> \(V=\mathrm{s}\!\!\lim_{\varepsilon\downarrow0}
> C(|C|+\varepsilon I)^{-1}\). Elementwise commutation gives
> \(\mathcal B\subseteq\mathcal A'\), hence every element of
> \(\mathcal A''=(\mathcal A')'\), in particular \(V\) and the displayed
> functional-calculus factors, commutes with \(B\). Now
> \(V^\dagger V=s(|C|)\) and
> \(|C^\dagger|^{1/2}V=V|C|^{1/2}\). Expanding gives
> \(P_{C,B}^\dagger P_{C,B}=|C^\dagger|+|C|-CB-B^\dagger C^\dagger\).
> No inverse of \(C\), unitary extension of \(V\), tensor factorization, or
> trace has been used.

Do not say that the support projection comes from *continuous* functional
calculus; it is the displayed strong limit (equivalently bounded Borel
functional calculus).

## 2. What the source had already proved

Appendix A.2, Proposition 3 of arXiv:2606.21362v3 proves
\[
 \beta_{\mathcal Q}(\mathcal I_d)\le d\sqrt2
\]
by a level-one SOS and says explicitly that this bound is generally non-tight.
Appendix A.3, Table 1 reports:

| \(d\) | Source analytic upper bound | Canonical/conjectured value | Tight source NPA level |
|---:|---:|---:|---|
| 2 | \(2\sqrt2\) | \(2.828\ldots\) | level 1 / CHSH |
| 3 | \(3\sqrt2\) | \(4.000\ldots\) | \(1+AB\) |
| 4 | \(4\sqrt2\) | \(5.226\ldots\) | \(1+AB\) |
| 5 | \(5\sqrt2\) | \(6.472\ldots\) | level 2 |
| 6 | \(6\sqrt2\) | \(7.727\ldots\) | level 2 |

The source supplies an analytic attaining strategy for every \(d\), not just
these five dimensions. Its numerical evidence for equality ends at \(d=6\).
The correct attribution language is:

> Perito et al. proved the general upper bound
> \(\beta_{\mathcal Q}(\mathcal I_d)\le d\sqrt2\), supplied an
> all-dimensional strategy of value \(2\csc(\pi/(2d))\), and conjectured
> that this lower value is exact. Their NPA calculations confirm equality
> through \(d=6\) to the reported precision. We prove the sharper value
> analytically for every \(d\), and the same operator proof extends to the
> commuting-operator model.

If an asymptotic comparison is included, use “same linear order and within an
asymptotic factor \(\pi/(2\sqrt2)\)” rather than “asymptotically tight.”

## 3. Exact low-dimensional benchmarks

All radical simplifications in the first exact-value manuscript are correct:

| \(d\) | \(2\csc(\pi/(2d))\) | Decimal |
|---:|---:|---:|
| 2 | \(2\sqrt2\) | 2.828427124746... |
| 3 | \(4\) | 4.000000000000... |
| 4 | \(2\sqrt{4+2\sqrt2}\) | 5.226251859506... |
| 5 | \(2(1+\sqrt5)\) | 6.472135955000... |
| 6 | \(2(\sqrt6+\sqrt2)\) | 7.727406610313... |

The exact reductions use
\(\sin(\pi/8)=\sqrt{2-\sqrt2}/2\),
\(\sin(\pi/10)=(\sqrt5-1)/4\), and
\(\sin(\pi/12)=(\sqrt6-\sqrt2)/4\). For example,
\((4+2\sqrt2)(2-\sqrt2)=4\), which checks the nested radical at \(d=4\).
The source's Table 1 truncates the decimals to three places; it reports
agreement within \(10^{-6}\), so a restored table should say “agreement to
reported numerical precision,” not imply an exact numerical proof.

## 4. Canonical source-observable identification

The polar construction and source construction agree in the main-text
no-adjoint convention. With
\[
 Z|j\rangle=\omega^j|j\rangle,\qquad
 X|j\rangle=|j+1\rangle,qquad
 W_y=\omega^yZ^\dagger X,
\]
let \(L_y=Z+\omega^yX=V_yH_y\). Maximally-entangled trace duality gives the
termwise optimizer
\[
 B_y^T=V_y^\dagger,\qquad B_y=\overline{V_y}.
\]
The source writes the same observable as
\[
 B_y^{\rm src}=\sum_{k=0}^{d-1}\lambda_{y,k}X^{k+1}Z^k,
 \qquad
 \lambda_{y,k}=
 \frac{(-1)^k\omega^{k(k+1)/2}\omega^{-y(k+1)}}
 {d\sin(\pi(k+\tfrac12)/d)}.
\]
Its Fourier identity is
\[
 \sum_{y=0}^{d-1}\omega^{my}\lambda_{y,k}
 =d\lambda_{0,k}\,\delta_{k,m-1\ ({\rm mod}\ d)}.
\]
At \(m=0,1\), this gives
\[
 \sum_yB_y=\alpha_dZ^\dagger,qquad
 \sum_y\omega^yB_y=\alpha_dX,qquad
 \alpha_d=\csc\!\left(\frac\pi{2d}\right).
\]
These two sums show that the source strategy reaches
\(2\alpha_d=M_d\). Since every \(L_y\) is invertible on this strategy and the
sum of its nonnegative polar deficits vanishes, termwise polar equality is
unique and forces \((B_y^{\rm src})^T=V_y^\dagger\). This identifies the
strategies, not merely their values.

For \(d=3\), the coefficient formula reduces to
\[
 B_y=\frac13\left(2Z^2+2\omega^{2y}X-\omega^{y+1}X^2Z\right),
\]
which is exactly Eq. (9) of the source and has \(\alpha_3=2\). The transpose
is dictated by
\(\langle\Phi_d|M\otimes N|\Phi_d\rangle=d^{-1}\operatorname{Tr}(MN^T)\).
The source appendix's all-Bob-adjoint convention is related by Bob outcome
inversion and must not be mixed into these formulas term by term.

### Integration-ready paragraph

> To compare conventions, the source observables satisfy
> \(\sum_yB_y=\alpha_dZ^\dagger\) and
> \(\sum_y\omega^yB_y=\alpha_dX\), with
> \(\alpha_d=\csc(\pi/(2d))\). Hence they attain the sum of the termwise polar
> bounds. Because \(Z+\omega^yX\) is invertible here, equality uniquely gives
> \(B_y^T=V_y^\dagger\); thus our polar observables are the source observables
> in the main-text convention. At \(d=3\) this is
> \(B_y=(2Z^2+2\omega^{2y}X-\omega^{y+1}X^2Z)/3\), exactly the source's
> displayed qutrit formula.

## 5. Coefficient normalization

For every \(x\) away from the poles,
\[
 \sum_{k=0}^{d-1}\cot\!\left(x+\frac{k\pi}{d}\right)=d\cot(dx).
\]
Differentiating gives
\[
 \sum_{k=0}^{d-1}\csc^2\!\left(x+\frac{k\pi}{d}\right)
 =d^2\csc^2(dx).
\]
Set \(x=-\pi/(2d)\). Then
\[
 \sum_{\ell=0}^{d-1}
 \csc^2\!\left(\frac{\pi(\ell-\tfrac12)}d\right)=d^2.
\]
The phase in the merged coefficient
\[
 \lambda_\ell=
 \frac{(-1)^{\ell-1}\eta^{\ell(\ell-1)}}
 {d\sin(\pi(\ell-\tfrac12)/d)}
\]
has unit modulus. Consequently
\[
 \sum_{\ell=0}^{d-1}|\lambda_\ell|^2
 =\frac1{d^2}\sum_{\ell=0}^{d-1}
 \csc^2\!\left(\frac{\pi(\ell-\tfrac12)}d\right)=1.
\]
All factors of \(d\), \(\pi\), and the half-index shift are correct. This
derivation should appear immediately before the second-family SOS, because
the constant term in that SOS uses it.

## 6. Conjecture 2: exact logical and normalization scope

In arXiv:2606.21362v3, the numbered **Conjecture 2** says that maximal
violation of the first augmented functional certifies \(2\log d\) random bits
for \(x=1,y=d\). Beside it, the source prints the purported maximum as
\[
 2\bigl[d\sin(\pi/(2d))\bigr]^{-1}+1.
\]
That factor \(d\) is incompatible with all of the following primary-source
anchors:

- Eq. (10), which defines the augmentation as one additional real correlator;
- Eq. (17), which gives the reduced canonical value
  \(2[\sin(\pi/(2d))]^{-1}\);
- the aligned extra observable, whose contribution is one; and
- the source's explicit \(d=3\) augmented value \(5\), whereas the printed
  Conjecture 2 formula would give \(7/3\).

The authoritative operator normalization is therefore
\[
 \max\overline{\mathcal I}_d=M_d+1,
 \qquad M_d=2\csc\!\left(\frac\pi{2d}\right).
\]
There is also a minor setting-label slip in the prose before Eq. (11), which
says \(y=d+1\); Conjecture 2, the zero-based setting set, and the qutrit
example consistently designate \(y=d\).

The merged construction proves, for every \(d\ge4\), that another
finite-dimensional behavior attains \(M_d+1\) but has a nonuniform target
table. It therefore refutes the intended scalar-value implication in
Conjecture 2 in exactly those dimensions. It does **not** determine the
maximal adversarial guessing probability, classify every maximizer, disprove
randomness of the canonical realization, or contradict the source's SDP after
the entire canonical behavior is fixed.

### Integration-ready wording

> Conjecture 2 of Ref. [source] asserts that maximal violation of the first
> augmented scalar functional certifies \(2\log_2d\) bits for the designated
> inputs. Its printed value contains a factor \(d\) inconsistent with the
> operator definition, Eq. (17), and the reported qutrit value; throughout we
> use the operator normalization \(\max\overline{\mathcal I}_d=M_d+1\). In
> that normalization, the nonuniform exact maximizers below refute the
> scalar-value implication of Conjecture 2 for every \(d\ge4\). This does not
> challenge the source's calculation conditioned on the complete canonical
> behavior or establish the exact worst-case guessing probability.

This is more accurate than either saying broadly that the source's randomness
result is false or describing the counterexample only as an unspecified
“scope limitation.”

## 7. Bibliography and official names

### NPA

The released merged file contains `\bibitem{NPA2007}` but does not cite it.
The feedback is correct. The most natural citation point is the sentence or
table cell reporting the source's NPA evidence through \(d=6\). The official
record is:

- Miguel Navascués, Stefano Pironio, and Antonio Acín, “Bounding the Set of
  Quantum Correlations,” *Physical Review Letters* **98**, 010401 (2007),
  [doi:10.1103/PhysRevLett.98.010401](https://doi.org/10.1103/PhysRevLett.98.010401).

The source paper cites both this article and the convergence article. Adding
the latter is optional but preferable if the manuscript discusses hierarchy
convergence or the commuting limit:

- Miguel Navascués, Stefano Pironio, and Antonio Acín, “A convergent hierarchy
  of semidefinite programs characterizing the set of quantum correlations,”
  *New Journal of Physics* **10**, 073013 (2008),
  [doi:10.1088/1367-2630/10/7/073013](https://doi.org/10.1088/1367-2630/10/7/073013).

Do not cite NPA at the sentence saying an analytic identity is “not a
finite-level NPA certificate”; cite it where the hierarchy or its numerical
bounds are actually used or described.

### Coccia--Padovan--Vallone

The official arXiv record lists **Lorenzo Coccia, Matteo Padovan, Giuseppe
Vallone**:
[arXiv:2606.21626v1](https://arxiv.org/abs/2606.21626v1). Therefore the correct
bibliographic initials are **L. Coccia, M. Padovan, and G. Vallone**.

- The released merged manuscript already has these correct initials.
- `minimum_bell_randomness/manuscript.tex` historically prints “E. Coccia,
  S. Padovan.” That historical source should remain preserved, but the error
  must not be copied into the canonical manuscript, website, packet, or
  metadata.
- The canonical priority audit also uses L. Coccia and M. Padovan correctly.

### Remaining merged bibliography

The remaining author lists, titles, years, volumes, and article numbers were
checked against their DOI publisher metadata or official arXiv records. No
further author-initial conflict was found:

| Entry | Official-name check |
|---|---|
| Perito et al. 2026 | Ignacio Perito; Raffaele D'Avino; Michał Jung; Piotr Mironowicz; Antonio Acín; Remigiusz Augusiak |
| Dhara et al. 2013 | Chirag Dhara; Giuseppe Prettico; Antonio Acín |
| Nieto-Silleras et al. 2014 | O. Nieto-Silleras; S. Pironio; J. Silman |
| Bancal et al. 2014 | Jean-Daniel Bancal; Lana Sheridan; Valerio Scarani |
| Buhrman--Massar 2005 | H. Buhrman; S. Massar |
| Salavrakos et al. 2017 | Alexia Salavrakos; Remigiusz Augusiak; Jordi Tura; Peter Wittek; Antonio Acín; Stefano Pironio |
| Kaniewski et al. 2019 | Jędrzej Kaniewski; Ivan Šupić; Jordi Tura; Flavio Baccari; Alexia Salavrakos; Remigiusz Augusiak |
| Sarkar et al. 2021 | Shubhayan Sarkar; Debashis Saha; Jędrzej Kaniewski; Remigiusz Augusiak |
| Wooltorton et al. 2022 | Lewis Wooltorton; Peter Brown; Roger Colbeck |
| Barizien et al. 2024 | Victor Barizien; Pavel Sekatski; Jean-Daniel Bancal |
| Klep et al. 2026 | Igor Klep; **Nando** Leijenhorst; Victor Magron |
| Farkas et al. 2026 | Máté Farkas; Piotr Mironowicz; Remigiusz Augusiak |
| D'Avino et al. 2026 | Raffaele D'Avino; Ignacio Perito; Piotr Mironowicz; Antonio Acín; Remigiusz Augusiak |

Use `Ac\'in` consistently in TeX prose as well as in the bibliography; one
unaccented “Acin” in the released introduction should be normalized.

## Verification artifact

The focused replay is:

```bash
python3 cyclic_bell_exact_values_and_randomness/verification/verify_exact_benchmarks.py
```

Result on 9 August 2026:

```text
PASS exact d=2..6 radical benchmarks and source decimals
PASS csc-square/lambda normalization d=2..100 and hostile general shifts
PASS source/polar/Fourier observables d=2..12 (77 Bob operators), including d=3
INFO source-bound asymptotic ratio (d sqrt(2))/(2 csc(pi/(2d))) -> 1.110720734540 (11.072% high)
```

The script is dependency-free. It independently constructs the canonical
polar observable by spectral interpolation, constructs the source observable
from Eq. (45), and compares them. Its finite floating-point sweeps are
regression evidence; the all-dimensional proofs above remain load-bearing.

## Final disposition

All seven feedback items contain a real improvement. None requires removing
the exact `qc` result. The only material qualification is that \(d\sqrt2\) is
not asymptotically tight, and the literal formula next to Conjecture 2 cannot
be repeated as a coherent maximum without explaining its normalization
discrepancy. With those qualifications, the source attribution, exact
benchmarks, Fourier convention check, SOS normalization, and bibliography
repairs should all be integrated.
