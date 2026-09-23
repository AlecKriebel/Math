# Fresh adversarial preprint-readiness review, round 3

Review checkpoint: 2026-09-23T13:45:36Z. Review completion estimate: **100% of the assigned fresh-review scope**. This is an internal mathematical and presentation review of version 1.0 as a preprint, not external peer review or journal-submission certification.

**Verdict: no actionable remaining findings in the reviewed manuscript, rendered PDF, or corrected supplementary script. No mathematical or presentation correction is requested.** The universal proof is valid under its stated hypotheses. The corrected hand-written quartic formulas agree with independent expansion and direct ordered tensor contraction. The positive and negative controls test the claims described below.

## Independence, scope, and reviewed artifacts

I read `manuscript/paper.tex` first. I then extracted the PDF text and visually inspected all three rendered pages, independently derived the proof's coefficient calculation and the supplemental formulas, read and executed the supplemental script, and checked its calculations using a separate direct tensor contraction. I did not consult earlier audit verdicts. I also read and ran the main verifier to check the manuscript's finite-verification description. Its separate adversarial-review files and the package's alternative proof were not used to establish this verdict. No broad priority search was repeated.

SHA-256 values observed at the start and confirmed after the mathematical checks:

| Artifact | SHA-256 |
| --- | --- |
| `manuscript/paper.tex` | `317ab083bdfc4e986921e517b368de8e1501c7f9a24b4faef5b047fe1d504f43` |
| `output/pdf/paper.pdf` | `a84cfe9347d3d0ce05ef0fb22e8648ee64fd77992825729d24991cf0fc1d627d` |
| `verification/preprint_round_2_checks.py` | `d777047b100b989d95de2baabea1519a81081b984d9a4d4df6a6fe39c615c833` |
| `verification/verify.py` | `f1d0b9755c3dab689878c0e8af758ea3f5e58ebcc86eb36afaed5f67b67dc82f` |

I independently retrieved the [primary printed Oberwolfach report](https://ems.press/content/serial-article-files/46829) and visually inspected PDF page 42, printed page 3182. Its SHA-256 was `549b3c1ecb3abb2a970f622e499b1b5aac23a02f4c73567408dfd8c457aff021`. Problem 11 presents tuple-indexed coefficients and an absolute-value bound by the geometric mean of the associated diagonal coefficients. The manuscript states explicitly the symmetric ordered convention it uses and proves that bound for every ordered tuple. It imposes no extra restriction on the allowed real invertible change of variables.

Only this report was added to the effort. Temporary PDF-rendering files were outside the repository. No manuscript, script, archive, metadata, or other research file was edited; no commit or external communication was performed. Ongoing changes to the parent's review summaries or package manifests are outside this mathematical review.

## Universal theorem: independent reconstruction and attempted failure modes

The exact claim is existence, for every positive definite real homogeneous polynomial of positive even degree and every finite positive dimension, of an invertible basis with unit diagonal ordered coefficients and every mixed ordered coefficient in `(0,1)`. No convexity, strict sphere minimum, orthogonality of the final basis, rationality of the normalization, or uniform bound on its condition number is assumed.

### Sphere comparison and derivative factors

Continuity and compactness give a sphere minimum `c>0`. Positive homogeneity then gives `p(x)>=c||x||^d`, including at zero. After division by `c`, write `p(v)=1` and `p(x)>=||x||^d`. For `u` perpendicular to `v`, direct multilinear expansion gives

\[
p(v+tu)=1+d t A(v^{d-1},u)
 +\binom d2 t^2 A(v^{d-2},u,u)+O(t^3).
\]

The comparison term is

\[
(1+t^2\|u\|^2)^{d/2}
=1+\frac d2 t^2\|u\|^2+O(t^4).
\]

Their difference is nonnegative and vanishes at zero. Its first derivative at zero is zero, and its second derivative at zero is nonnegative. Thus the factors are exactly

\[
dA(v^{d-1},u)=0,\qquad
d(d-1)Q(u,u)-d\|u\|^2\ge0.
\]

In particular, `Q` is strictly positive on every nonzero tangent vector even when the restriction of `p` to the sphere has a degenerate or completely flat minimum. This avoids the principal possible hidden hypothesis: strict positivity of the spherical Hessian is unnecessary.

### The complete tuple calculation

For arbitrary ordered arguments `a_1,...,a_d` from the stated tangent vectors, put

\[
S=\sum_{r<s}Q(a_r,a_s),\qquad
D=\sum_r Q(a_r,a_r).
\]

All linear terms vanish separately. Therefore

\[
N_J=1+S\varepsilon^2+O(\varepsilon^3),\qquad
\prod_r p(v+\varepsilon a_r)
=1+\binom d2 D\varepsilon^2+O(\varepsilon^3),
\]

while `N_J^d=1+dS epsilon^2+O(epsilon^3)`. Consequently the quadratic coefficient of `F_J` is

\[
\frac{d(d-1)}2D-dS
=\frac d2\sum_{r<s}
 \bigl(Q(a_r,a_r)+Q(a_s,a_s)-2Q(a_r,a_s)\bigr)
=\frac d2\sum_{r<s}Q(a_r-a_s,a_r-a_s).
\]

The factor `d/2` and the use of the `d`th power of `N_J` are correct. This calculation applies to all multiplicity patterns, including tuples containing more than two distinct indices; it is not a binary or two-coefficient argument. Since the `m-1` orthonormal tangent vectors and zero are pairwise distinct, a mixed tuple has a nonzero pair difference. Every summand is nonnegative and at least one is positive.

For each mixed tuple, dividing its polynomial `F_J` by `epsilon^2` gives a function with a positive limit at zero. Thus it is positive on an interval `(0,eta_J)`. There are finitely many tuples, so their interval lengths have a positive minimum. Independently, each `N_J` tends to one; a second finite intersection ensures positivity of every `N_J`. No uniform remainder estimate over an infinite family is being assumed, and no perturbation independent of the input form is promised.

For a pure tuple, `N_J=p(x_j)`, and the product defining `F_J` is exactly `p(x_j)^d`, so `F_J` vanishes identically. The pure/mixed equality statement is therefore exact.

### Invertibility, signs, and scaling

Projecting a linear dependence among the `v+epsilon w_i` onto the tangent space forces the first `m-1` coefficients to vanish when `epsilon` is nonzero; its radial component then forces the final coefficient to vanish. Every column is nonzero and has positive `p` value.

The strict gap gives

\[
N_J^d<\prod_r p(x_{j_r})
\]

for mixed tuples. Even degree gives the absolute-value bound; the separately established positivity of `N_J` yields the stronger positive bound. Restoring the original polynomial multiplies the tensor value by `c` and multiplies the product of `d` positive `d`th roots by `c`. There is no missing power of `c`.

With original `p`, positive column scaling by `p(x_i)^{-1/d}` preserves independence and makes the diagonal one. Multilinearity divides each mixed tensor entry by precisely the corresponding product of roots. This completes the stated normalization and the transformation law for the ordered coefficients.

### Boundary and scope checks

| Attempted obstruction | Outcome |
| --- | --- |
| `m=1` | The tangent basis is empty, the sole column is `v`, and mixed tuples are vacuous. The normalization is valid. |
| `d=2` | `Q=A`, the tangent lower bound is `Q(u,u)>=||u||^2`, and the gap's leading term is `Q(a_1-a_2,a_1-a_2) epsilon^2`. No degree-four assumption enters. |
| Odd degree | Excluded by positive definiteness: `p(-x)=-p(x)` would contradict positivity. |
| Degenerate/nonunique sphere minimum | The Euclidean norm comparison still supplies the positive tangent quadratic term. |
| Nonconvex positive form | Convexity is nowhere used; the nonconvex supplementary family below provides explicit stress cases. |
| Highly anisotropic coefficients | Finite continuity applies for each fixed form; no common perturbation across forms is claimed. |
| Merely nonnegative forms | The proof requires `c>0`. The manuscript explicitly excludes this extension. |
| Rational-basis observation | The strict inequalities and nonzero determinant are open in matrix entries. Rational density applies to an unnormalized basis even for real polynomial coefficients; final normalization need not be rational. |
| Ordinary monomial coefficients | The coefficient of `t^alpha` is the ordered tensor entry times the multinomial. The example `x^4+12x^2y^2+y^4` correctly gives `A1122=12/6=2`. |

No counterexample or unsupported central lemma remained after these checks.

## Corrected supplemental script: independent derivations

### Polarization, full scope of `check`, and exact arithmetic

For a homogeneous degree-`d` polynomial, expanding the sign-polarization sum shows that multiplication by the product of the `d` signs kills every term except those in which every argument occurs an odd number of times. There are `d` arguments and total degree `d`, so each must occur exactly once. These surviving terms contribute `2^d d! A(v_1,...,v_d)`. The denominator in `polar` is therefore correct.

For two columns, symmetry means the `d+1` values indexed by the multiplicity `k` exhaust all `2^d` ordered tuples. `values[0]=p(z2)` and `values[d]=p(z1)`, and the tested gap is exactly

\[
G_k=p(z_1)^k p(z_2)^{d-k}-A(z_1^k,z_2^{d-k})^d.
\]

The two pure gaps vanish. The positivity tests add the required positive sign to the strict absolute-value inequality. The determinant test checks actual independence of the columns. For bilinear slices, the `d-1` choices of `k` exhaust all multiplicities in the remaining `d-2` arguments. Polarization gives symmetric real `2x2` matrices; positive first leading entry and positive determinant are exactly Sylvester's criterion for positive definiteness. These slice tests are stronger supplementary finite checks, not assumptions needed by the paper's proof.

All evaluated numbers in these examples are integers or `Fraction` values. The polarization accumulator and denominator division preserve rational arithmetic; no small-gap conclusion comes from floating-point subtraction. I ran the script with ordinary Python, not optimization mode that disables assertions.

### Nonconvex positive quartics, including the corrected factor

Let

\[
p_\delta(x,y)=(x^2-y^2)^2+2\delta x^2y^2,
\quad v=(1,1),\quad w=(1,-1),\quad
z_1=v+hw,\quad z_2=v.
\]

For every `delta>0`, the two nonnegative summands cannot both vanish away from zero, so this is positive definite. For the three tested values `delta<1`, the second derivative in the `y` direction at `(1,0)` is `4(delta-1)<0`, so the nonconvex label is justified.

Put `a=2 delta`, `b=16-4 delta`. Direct substitution, with independent variables `U,T`, gives

\[
p_\delta(Uv+Tw)=aU^4+bU^2T^2+aT^4.
\]

Hence

\[
p_\delta(tz_1+sz_2)
=a(s+t)^4+bh^2t^2(s+t)^2+ah^4t^4.
\]

Dividing the coefficients of `t^k s^(4-k)` by `binom(4,k)` yields the complete list

\[
(N_0,N_1,N_2,N_3,N_4)
=\left(a,a,a+\frac{bh^2}{6},
 a+\frac{bh^2}{2},a+bh^2+ah^4\right).
\]

In particular, the corrected hand-written value

\[
N_2=2\delta+\frac{16-4\delta}{6}h^2
\]

is correct. The diagonal formula `p1=2 delta+(16-4 delta)h^2+2 delta h^4` is also correct. The factor `1/6` comes from the ordinary `t^2s^2` coefficient and cannot be omitted.

For the three positive cases, set `T=bh^2/a` and `H=h^4`. The chosen parameters give `0<T<8/10000`, and `H>0`. All entries are positive. After division by `a^4`, the three mixed gaps are

\[
T+H,\qquad
(1+T+H)^2-(1+T/6)^4,\qquad
(1+T+H)^3-(1+T/2)^4.
\]

Dropping `H` only decreases the last two expressions. At `H=0` they are respectively

\[
\frac43T+\frac56T^2-\frac1{54}T^3-\frac1{1296}T^4,
\qquad
T+\frac32T^2+\frac12T^3-\frac1{16}T^4,
\]

which are positive in the tested range. The basis determinant is `2h`, hence nonzero.

For completeness, the three bilinear slice matrices in the basis `(v,w)`, with `k=0,1,2` copies of `z1` in the two fixed arguments, are

\[
B_0=\begin{pmatrix}a&0\\0&b/6\end{pmatrix},\quad
B_1=\begin{pmatrix}a&hb/6\\hb/6&b/6\end{pmatrix},\quad
B_2=\begin{pmatrix}a+h^2b/6&hb/3\\hb/3&b/6+ah^2\end{pmatrix}.
\]

Their determinants are

\[
\frac{ab}{6},\quad
\frac{ab}{6}(1-T/6),\quad
\frac{ab}{6}\left(1+H+\frac{6ah^2}{b}-T/2\right),
\]

and their first entries are positive. Thus all three are positive definite. Positive definiteness is invariant under the invertible change from `(v,w)` to the standard basis used by the script. This checks the slice assertions by formulas independent of the sign-polarization implementation.

### Quartics with degenerate sphere minimum

Here `p_lambda=(x^2+y^2)^2+lambda y^4`, with `lambda>=0`, `z1=(1,h)` and `z2=(1,0)`. On the unit sphere the polynomial is `1+lambda y^4`, so the minimum at `(1,0)` is degenerate to quadratic order; for `lambda=0` the entire sphere is minimizing. Positive definiteness follows from the first summand.

Substitution gives

\[
p_\lambda(tz_1+sz_2)
=(s+t)^4+2h^2t^2(s+t)^2+(1+\lambda)h^4t^4,
\]

and therefore

\[
(N_0,N_1,N_2,N_3,N_4)
=\left(1,1,1+h^2/3,1+h^2,1+2h^2+(1+\lambda)h^4\right).
\]

Writing `q=h^2>0`, the last entry satisfies `N4>1` and `N4>=(1+q)^2`. Thus `G1=N4-1>0`, `G2=N4^2-(1+q/3)^4>0`, and `G3=N4^3-(1+q)^4>0`. These statements include all three tested magnitudes of `lambda`. The basis determinant is `-h`.

In standard coordinates the three slice matrices are

\[
\begin{pmatrix}1&0\\0&1/3\end{pmatrix},\quad
\begin{pmatrix}1&h/3\\h/3&1/3\end{pmatrix},\quad
\begin{pmatrix}1+h^2/3&2h/3\\2h/3&1/3+(1+\lambda)h^2\end{pmatrix}.
\]

The determinants are `1/3`, `1/3-h^2/9`, and

\[
\frac13+\left(\frac23+\lambda\right)h^2
+\frac{1+\lambda}{3}h^4.
\]

They are positive for the tested `h<=1/8`. This independently validates the slice controls, including the large `lambda` case.

### Anisotropic quadratic

For `p=x^2+lambda y^2`, `lambda=10^80`, and `h=10^-42`, the three ordered coefficient classes are exactly `(1,1,1+10^-4)`. The sole mixed gap is `10^-4>0`; the basis determinant is `-h`. The only slice is the original positive definite diagonal matrix `diag(1,10^80)`. This is a genuine degree-two and large-anisotropy test.

### Negative controls and their precise interpretation

For the fixed `h=1/4` in the nonconvex family, the independently simplified formulas are

\[
p_0=2\delta,\qquad
p_1=1+\frac{225}{128}\delta,\qquad
N_2=\frac16+\frac{47}{24}\delta.
\]

The tested gap is `4 delta^2 p1^2-N2^4`. For either `delta=10^-8` or `10^-80`, it is strictly negative. A simple independent bound is `p1<2` and `N2>=1/6`, so the positive term is less than `16*10^-16`, while the subtracted term is at least `1/1296`. Exact computation additionally placed both gaps strictly between `-1/1000` and `-1/2000`.

Thus these are actual coefficient-inequality failures in invertible candidate bases for positive definite forms, rather than failures of a formula unrelated to the polynomial. The script now explicitly compares both hand-written formulas with direct evaluation or polarization, and the independent contraction check below removes reliance on those comparisons alone. For any fixed `h>0`, the same gap tends as `delta` tends to zero to `-((8/3)h^2)^4<0`. These examples illustrate why the successful perturbation size may depend on the input form; they do not contradict the existence theorem.

The final endpoint test verifies that `(x^2-y^2)^2` vanishes at the nonzero vector `(1,1)`. This accurately checks exclusion from the positive-definite hypothesis. It does **not** claim to prove failure of every possible normalization for that semidefinite polynomial, and it is not a test of the universal theorem at an included endpoint.

## Reproducible computational evidence

Environment: Python 3.14.6, standard library only. From the effort directory, `python3 verification/preprint_round_2_checks.py` exited successfully with the seven positive-case PASS lines, the fixed-perturbation negative-controls PASS line, and the excluded-endpoint PASS line.

The following independent calculation was run without writing a new script file. It compares the six quartic cases against a direct ordered tensor contraction using the original monomial coefficients, not against a second copy of the sign-polarization formula. It checks 30 coefficient values and 72 entries of the hand-derived slice matrices. The transcript can be reproduced by pasting this block into Python from the effort directory.

```python
from fractions import Fraction as F
from contextlib import redirect_stdout
from itertools import product
import io, runpy

with redirect_stdout(io.StringIO()):
    s = runpy.run_path('verification/preprint_round_2_checks.py')
polar = s['polar']

def tensor4(c40, c22, c04, vectors):
    total = F(0)
    for ids in product((0, 1), repeat=4):
        count = sum(ids)
        coeff = (c40 if count == 0 else c04 if count == 4
                 else c22 / F(6) if count == 2 else F(0))
        term = coeff
        for v, j in zip(vectors, ids):
            term *= v[j]
        total += term
    return total

checks = 0
rows = []
eye = [(F(1), F(0)), (F(0), F(1))]
cases = [('delta', F(1, 10**e), F(1, 10**((e+1)//2+2)))
         for e in (1, 8, 80)]
cases += [('lambda', lam, F(1, 10**12) if lam > 1 else F(1, 8))
          for lam in (F(0), F(1, 10**40), F(10**40))]
for kind, param, h in cases:
    if kind == 'delta':
        a, b = 2*param, 16-4*param
        p = lambda z: (z[0]**4 + (2*param-2)*z[0]**2*z[1]**2
                       + z[1]**4)
        z1, z2 = (1+h, 1-h), (F(1), F(1))
        expected = [a, a, a+b*h*h/6, a+b*h*h/2,
                    a+b*h*h+a*h**4]
        coeff = (F(1), 2*param-2, F(1))
        axis = [z2, (F(1), F(-1))]
        matrices = [
            [[a, 0], [0, b/6]],
            [[a, h*b/6], [h*b/6, b/6]],
            [[a+h*h*b/6, h*b/3], [h*b/3, b/6+a*h*h]],
        ]
    else:
        p = lambda z: (z[0]**4 + 2*z[0]**2*z[1]**2
                       + (1+param)*z[1]**4)
        z1, z2 = (F(1), h), (F(1), F(0))
        expected = [F(1), F(1), 1+h*h/3, 1+h*h,
                    1+2*h*h+(1+param)*h**4]
        coeff = (F(1), F(2), 1+param)
        axis = eye
        matrices = [
            [[1, 0], [0, F(1, 3)]],
            [[1, h/3], [h/3, F(1, 3)]],
            [[1+h*h/3, 2*h/3],
             [2*h/3, F(1, 3)+(1+param)*h*h]],
        ]
    for k in range(5):
        vs = [z1]*k + [z2]*(4-k)
        assert expected[k] == tensor4(*coeff, vs) == polar(p, vs)
        checks += 1
    for k in range(3):
        rest = [z1]*k + [z2]*(2-k)
        for i in range(2):
            for j in range(2):
                vs = rest + [axis[i], axis[j]]
                assert matrices[k][i][j] == tensor4(*coeff, vs) == polar(p, vs)
                checks += 1
        B = matrices[k]
        assert B[0][0] > 0 and B[0][0]*B[1][1] - B[0][1]**2 > 0
    rows.append((kind, str(param),
                 'direct tensor, coefficient formulas, and slice matrices PASS'))
print('independent formula/tensor comparisons:', checks)
for row in rows:
    print(*row)
for delta in (F(1, 10**8), F(1, 10**80)):
    h = F(1, 4)
    a, b = 2*delta, 16-4*delta
    p1 = 1+F(225, 128)*delta
    n2 = F(1, 6)+F(47, 24)*delta
    assert p1 == a+b*h*h+a*h**4
    assert n2 == a+b*h*h/6
    gap = a*a*p1*p1-n2**4
    assert gap < 0
    print('negative control delta=', delta,
          'gap between -1/1000 and -1/2000:',
          -F(1, 1000) < gap < -F(1, 2000))
```

Observed: `independent formula/tensor comparisons: 102`, six formula/tensor/slice PASS rows, and `True` for both negative-gap intervals. The displayed code differs from the executed block only in formatting, factoring the case list into a named variable, moving the `product` import to the top, and removing an unused import; the report block itself was subsequently executed successfully as a reproducibility check.

The main verifier also exited successfully. Its output reported 12 certificates, 120 coefficient classes, 110 polarization cross-checks, two negative controls, and the formal quadratic identity for degrees 2 through 24. The degree-eight classes are not polarization-cross-checked by that verifier; the manuscript does not assert that every class receives that second check. These computations support the finite-example description and do not substitute for the universal analytic proof.

## Preprint presentation and findings disposition

All three PDF pages are readable, with complete equations, clear coefficient notation, visible mathematical symbols, consistent page numbering, and no clipping or overlap. The page break within the proof retains a clear continuation. The extracted text agrees with the reviewed source. The title, author, ORCID, date, and version are present. The two references and project-page link are clearly presented.

The manuscript defines its coefficient convention before the theorem, supplies the entire necessary proof, identifies the permitted linear group and conditioning limitation, treats the one-variable boundary, separates computations from proof, and labels the result unrefereed with AI assistance and bounded priority-search disclosure. A reader does not need the internal reviews, computation package, or alternative proof to check the theorem. I did not recertify the priority search or claim external independent referee endorsement.

| Severity | Findings | Disposition |
| --- | --- | --- |
| Mathematical blocker | None | No correction requested. |
| Supplemental formula or control defect | None in the corrected reviewed hash | The revised `N2` factor and all tested controls independently verified. |
| Preprint self-containment or rendering defect | None | Ready on the reviewed mathematical and presentation criteria. |
| Remaining limitations | Internal review; finite computations; no renewed broad priority search | These do not create an unsupported premise in the proof and are not reasons to change version 1.0. |

Strongest verified result: the complete universal theorem as stated, together with correct exact supplemental finite checks. Exact remaining gap within the assigned scope: **none**. This verdict applies to the hashes listed above; archive manifests and review-summary integration remain the parent's separate task.
