# Fresh preprint review, round 2

**Review date:** 23 September 2026 (UTC).  
**First recorded checkpoint (after paper-first reading):** 2026-09-23T13:33:01Z.  
**Proof/source/render checkpoint:** 2026-09-23T13:35:08Z.  
**Extreme-case checkpoint:** 2026-09-23T13:35:44Z.  
**Completed and embedded checks rerun:** 2026-09-23T13:38:23Z.  
**Review completion estimate:** 100% of this bounded preprint-readiness review. This is not a probability of correctness or an estimate of first priority.

## Verdict and independence

**Initial manuscript verdict: no actionable findings.** I found no issue requiring a change to the paper before releasing it as an unrefereed preprint. During integration, the root reviewer identified an error in an auxiliary calculation added by this review; that error is corrected and disclosed in the integration note below. The manuscript verdict is unchanged, but the original extra-test calculation should not be treated as having been error-free.

I read `manuscript/paper.tex` first. I did not read any existing audit report, including the existing independent geometric proof or earlier review verdicts. I subsequently inspected the verifier and public-facing descriptions to check their consistency with my own mathematical assessment. The independent route used here is positivity of bilinear slices followed by a finite maximum argument, supplemented by exact signed-polarization checks written independently of the packaged verifier.

This review concerns a concise preprint, not a journal submission or external peer review. No person was contacted. The bounded priority search was not repeated; the manuscript correctly does not claim established first priority. Final archive rebuilding and checksum synchronization during the ongoing review cycle are outside this review's mathematical verdict.

## Reviewed artifacts

The following hashes were checked initially at 2026-09-23T13:33:01Z and again at 2026-09-23T13:35:08Z; both were unchanged:

```text
317ab083bdfc4e986921e517b368de8e1501c7f9a24b4faef5b047fe1d504f43  manuscript/paper.tex
a84cfe9347d3d0ce05ef0fb22e8648ee64fd77992825729d24991cf0fc1d627d  output/pdf/paper.pdf
```

All three PDF pages were rendered with Poppler and visually inspected. Extracted PDF text agrees with the LaTeX source. I also read `verification/verify.py`, `verification/README.md`, the project README, `site/index.html`, `CITATION.cff`, and `zenodo/metadata.json`. The live project page was retrieved directly and was byte-identical to `site/index.html` at the second hash checkpoint.

## Independent mathematical reconstruction

The precise target is: for every positive definite real homogeneous polynomial of positive degree, its symmetric multilinear polarization has a real basis with pure values one and mixed values strictly in `(0,1)`. The degree is necessarily even and at least two. The permitted change of variables is any invertible real matrix, with no conditioning constraint.

Normalize the positive sphere minimum to one, and write the minimizing unit vector as `v`. At the minimum, the radial/tangential decomposition of

\[
B_0(a,b)=A(v^{d-2},a,b)
\]

has

\[
B_0(v,v)=1,\quad B_0(v,u)=0,\quad
B_0(u,u)\geq \frac{\|u\|^2}{d-1}\quad(u\perp v).
\]

The last bound follows from differentiating the comparison with the Euclidean norm, as in the manuscript; it also follows from the constrained second derivative at a sphere minimum. Therefore, for `a=t v+u`,

\[
B_0(a,a)\geq t^2+\frac{\|u\|^2}{d-1}>0\qquad(a\ne0).
\]

Thus this is a positive definite bilinear form on the full ambient space, not merely on the tangent space. Its smallest eigenvalue is at least `1/(d-1)` after the stated normalization.

The matrix of `A(y_1,...,y_{d-2},-, -)` depends continuously on the conditioning arguments. Positive definiteness is open. Hence every such slice is positive definite when all its conditioning vectors lie sufficiently close to `v`. This is a local statement for the fixed polynomial; it does not assume a uniform neighborhood over all forms. For `d=2`, the slice is simply `A`, with no conditioning arguments.

Choose the manuscript's nearby independent basis, then normalize its columns to obtain `z_i` with `p(z_i)=1`. Those normalized vectors still approach `v`. Shrink the perturbation so all relevant bilinear slices are positive definite and all tensor entries are positive. The latter follows directly from continuity at `A(v,...,v)=1`.

Let `M` be the maximum of the finitely many tensor entries on this normalized basis. Pure tuples have value one, so `M>=1`. If a mixed tuple attained `M`, select two unequal indices `i,j` appearing in it, and condition the bilinear form on the other `d-2` arguments. Strict Cauchy--Schwarz gives

\[
M^2=B(z_i,z_j)^2
  < B(z_i,z_i) B(z_j,z_j)\leq M^2.
\]

The strict inequality holds because distinct basis columns are not proportional; the final inequality follows from the definition of `M`. This contradiction forces `M=1` with no mixed maximizer. Positivity then gives the desired strict mixed bounds. This argument verifies the conclusion independently of the manuscript's polynomial-gap expansion.

I also checked the expansion in the manuscript directly. The quadratic term in the product of diagonal values is `d(d-1)/2` times the sum of diagonal `Q` terms; the quadratic term in the `d`th power of the mixed value is `d` times the sum over unordered pairs. Their difference is exactly the displayed sum of squared pair differences. There is no missing factor of `d`, multinomial coefficient, sign, or normalization factor. Restoring the original common scale multiplies both sides of the unnormalized coefficient inequality by the same positive number. Positive column rescaling gives the claimed unit diagonals.

**Strongest verified conclusion:** the universal theorem as stated, including positivity, strictness, pure equality, and the rational unnormalized-basis consequence. **Remaining mathematical gap found:** none.

## Attacks on assumptions and boundary cases

- **Dimension one.** The tangent basis is empty, the sole basis vector is nonzero, and the mixed assertion is vacuous. For `p(x)=c x^d`, the normalization is the ordinary positive real `d`th-root scaling. No hidden requirement `m>=2` remains.
- **Degree two.** The proof reduces to positive definite bilinear geometry. The expansion remains valid because omitted higher terms are zero or of higher order. Distinct nearby normalized basis columns have inner products strictly below one and, sufficiently near the same direction, strictly above zero.
- **Degenerate or nonisolated sphere minima.** These do not undermine the argument. For `p_lambda(x,y)=(x^2+y^2)^2+lambda y^4`, the sphere minimum at `(1,0)` has zero tangential second derivative for every `lambda>=0`; at `lambda=0` every sphere point minimizes. Nevertheless, the ambient bilinear slice has tangent value `1/3`. The Euclidean radial contribution supplies the needed strict lower bound.
- **Nonconvex positive quartics.** The family `p_delta=(x^2-y^2)^2+2 delta x^2 y^2` is positive definite for `delta>0`, while for `0<delta<1` its `y,y` Hessian entry at `(1,0)` is `4 delta-4<0`. Thus the tested family is genuinely nonconvex. The argument uses only local positivity near a suitable minimizing direction, not global convexity.
- **Approach to a nonnegative boundary.** At `delta=0`, `p_delta(1,1)=0`, so division by the minimum fails exactly where strict positive definiteness is lost. The manuscript explicitly excludes merely nonnegative forms. The exact tests below include `delta=10^-80` without treating that number as zero.
- **Conditioning and the size of the perturbation.** For the same nonconvex family, a fixed perturbation `h=1/4` fails a mixed inequality when `delta=10^-8` and `10^-80`. A sufficiently smaller perturbation passes. The manuscript neither asserts a common perturbation nor a bound on the condition number; its stated quantifiers are correct.
- **Strictness.** The finite maximum argument above independently verifies strictness. In the manuscript's proof, distinct members of `{w_1,...,w_{m-1},0}` make at least one pair difference nonzero in every mixed tuple. Finitely many tuples allow one strictly positive choice of epsilon. Positivity is checked separately before taking even roots, so an absolute-value issue cannot be hidden in the power comparison.
- **Rational density.** Invertibility, positivity of all tensor entries, and strict mixed power gaps are simultaneous open conditions on a finite real matrix. A rational approximation preserves them. Pure equality is an identity for every matrix and imposes no additional closed constraint. Normalization may be irrational, as expressly stated. No rationality of the polynomial or of the original sphere minimum is required.

## Original problem and references

I retrieved the publisher's report independently and visually inspected printed page 3182 (PDF page 42). Problem 11 is attributed to Brandes, concerns real positive definite homogeneous forms, asks about equivalence through a linear change of variables, and includes absolute values in its coefficient inequality. It imposes no orthogonality, integral, unimodularity, or conditioning condition. [Original report](https://ems.press/content/serial-article-files/46829#page=42).

The report leaves the summation index set implicit. The present paper explicitly supplies the symmetric ordered convention, and consistently uses it. This distinction is substantive: for `p(x,y)=(x^2+y^2)^2`, after unit-diagonal normalization the ordinary coefficient of `t_1^2 t_2^2` is `2+4 rho^2>=2`, where `rho` is the Euclidean inner product of the normalized columns. It could never satisfy an ordinary-coefficient bound of one. The manuscript already warns against dropping multiplicities, and its abstract names the ordered convention. I therefore do not regard this source-notation caveat as an unaddressed defect.

I checked the bibliographic metadata of the 2015 precursor against the publisher and inspected the author's arXiv version: Lemma 2.1 proves the positive definite quadratic matrix-entry inequality, which supports the manuscript's limited statement about that antecedent. The 2015 paper's earlier notation groups monomials, so it should not be used to silently identify ordinary coefficients with ordered tensor entries; the manuscript makes no such identification. [Publisher metadata](https://doi.org/10.1112/jlms/jdv028), [author's preprint](https://arxiv.org/pdf/1506.05343).

The report title, year, volume, report number, page range of the problem session, attribution, and DOI in the manuscript match the retrieved report. The two references are sufficient for the proof and its direct historical context. No uncited nonstandard theorem is needed.

## Verifier and additional reproducible exact checks

Running `python3 verification/verify.py` returned `PASS`: 12 certificates, 120 symmetric coefficient classes, 110 polarization cross-checks, the indicated finite identity checks, and two negative controls. Code inspection confirms that ordinary transformed coefficients are divided by their multinomial multiplicity. All inequality checks use exact rational arithmetic; mixed positivity and strictness are checked separately. The code and its documentation correctly disclaim deciding positivity of arbitrary supplied forms or proving universal existence.

The following complete Python program reproduces this review's additional checks. It uses the signed polarization identity, rather than importing the package's expansion or inclusion-exclusion implementation. The seven successful cases cover 33 coefficient classes and 19 positive definite bilinear slices. Two fixed-perturbation failures and the excluded nonnegative endpoint are expected negative controls. These finite computations supplement the independent argument above.

```python
from fractions import Fraction as F
from itertools import product
from math import factorial


def polar(p, vectors):
    d = len(vectors)
    total = F(0)
    for signs in product((-1, 1), repeat=d):
        point = tuple(sum(s * v[j] for s, v in zip(signs, vectors))
                      for j in range(len(vectors[0])))
        weight = 1
        for s in signs:
            weight *= s
        total += weight * p(point)
    return total / (2**d * factorial(d))


def check(label, d, p, z1, z2):
    values = [polar(p, [z1] * k + [z2] * (d-k))
              for k in range(d+1)]
    assert values[0] == p(z2) and values[d] == p(z1)
    gaps = [values[d]**k * values[0]**(d-k) - values[k]**d
            for k in range(d+1)]
    assert all(v > 0 for v in values)
    assert gaps[0] == gaps[d] == 0
    assert all(g > 0 for g in gaps[1:d])
    assert z1[0] * z2[1] - z1[1] * z2[0] != 0
    eye = [(F(1), F(0)), (F(0), F(1))]
    for k in range(d-1):
        rest = [z1] * k + [z2] * (d-2-k)
        B = [[polar(p, rest + [a, b]) for b in eye] for a in eye]
        assert B[0][0] > 0
        assert B[0][0] * B[1][1] - B[0][1]**2 > 0
    print(label, "PASS", len(values), "classes,", d-1, "slices")


for exponent in (1, 8, 80):
    delta = F(1, 10**exponent)
    h = F(1, 10**((exponent+1)//2 + 2))
    p = lambda z, delta=delta: ((z[0]**2-z[1]**2)**2
                               + 2*delta*z[0]**2*z[1]**2)
    check("nonconvex delta=1e-" + str(exponent), 4, p,
          (1+h, 1-h), (F(1), F(1)))

for lam in (F(0), F(1, 10**40), F(10**40)):
    p = lambda z, lam=lam: (z[0]**2+z[1]**2)**2 + lam*z[1]**4
    h = F(1, 10**12) if lam > 1 else F(1, 8)
    check("degenerate minimum lambda=" + str(lam), 4, p,
          (F(1), h), (F(1), F(0)))

lam = F(10**80)
p = lambda z: z[0]**2 + lam*z[1]**2
check("anisotropic quadratic lambda=1e80", 2, p,
      (F(1), F(1, 10**42)), (F(1), F(0)))

# For z1=(1+h,1-h), z2=(1,1), the k=2 tensor value below
# follows by expanding p_delta(t*z1+s*z2) and dividing by 6.
h = F(1, 4)
for delta in (F(1, 10**8), F(1, 10**80)):
    p0 = 2*delta
    p1 = 2*delta + (16-4*delta)*h*h + 2*delta*h**4
    n2 = 2*delta + (16-4*delta)*h*h/6
    actual_p = lambda z, delta=delta: ((z[0]**2-z[1]**2)**2
                                       + 2*delta*z[0]**2*z[1]**2)
    z1, z2 = (1+h, 1-h), (F(1), F(1))
    assert p1 == actual_p(z1)
    assert n2 == polar(actual_p, [z1, z1, z2, z2])
    assert p0**2 * p1**2 - n2**4 < 0
print("fixed-perturbation negative controls PASS")

p0 = lambda z: (z[0]**2-z[1]**2)**2
assert p0((F(1), F(1))) == 0
print("excluded nonnegative endpoint PASS")
```

## Preprint presentation and public claims

The three-page manuscript states its coefficient convention before the theorem, gives a complete short proof, identifies the near-singular basis issue, and separates finite evidence from the universal argument. All equations, references, page numbers, and links render legibly. The page break within the proof does not omit or obscure an argument. There are no missing figures, clipped equations, broken glyphs, placeholders, or unreadable bibliography entries.

The project README, live/local site, citation metadata, and proposed Zenodo description state the same real ordered-coefficient theorem. Their computational counts match the actual verifier output. They identify the work as an unrefereed AI-assisted preprint, distinguish internal checks from external review, and qualify the priority search. The manuscript's provenance statement is clear and proportionate. It does not claim formal verification, a conditioning guarantee, an integral result, or established first priority.

**Required minimal correction:** none. The review record can be added to the public package without changing the reviewed manuscript or PDF.

## Integration correction to an auxiliary check

At 2026-09-23 13:40:15 UTC, the root reviewer found a transcription error in the added fixed-perturbation negative-control formulas: the coefficient of h^2 must be 16-4*delta, not 8-4*delta, because ((1+h)^2-(1-h)^2)^2=16*h^2. The runnable block above has been corrected. It now explicitly compares the hand-derived p1 with direct polynomial evaluation and n2 with independently evaluated signed polarization before checking the negative gap. Both negative-control failures persist after correction. The error was confined to these extra reviewer calculations; it does not alter the manuscript, theorem, proof or previously packaged verifier. The corrected block is also saved as verification/preprint_round_2_checks.py. A new fresh adversarial review will check the resulting package.
