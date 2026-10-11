# Degree normalization in a Hasse-semigroup formula

## Result and scope

For the standard embedding of `P^1` with coordinate ring `C[x,y]`, choose the two strata `P^1 > {[0:1]}` and extremal functions `x^2,y^2`. The edgewise rational-root condition in the 2019 report holds. For the explicitly defined, extremal-function-normalized Seshadri valuation of Chirivì–Fang–Littelmann, the homogeneous value semigroup is

\[
\Gamma=\tfrac12\mathbb Z_{\geq0}^{2}.
\]

It therefore does **not** satisfy the unweighted-total formula printed in Theorem 2 of the 2019 report. This is a rigorous obstruction to applying that formula to arbitrary homogeneous degrees with this normalization. It is not a refutation of the flag-variety theorem, modern LS-type results, or an unspecified alternative normalization of the abbreviated 2019 construction.

The distinction is substantive: replacing the coordinate ring by its quadratic Veronese, with the induced degree-one grading, makes the displayed formula correct in this example. Thus a claim that the original historical conjecture has been conclusively refuted would exceed this audit.

## 1. Source interpretation

Littelmann's contribution, *Flag varieties, Valuations and Standard Monomial Theory*, is a work-in-progress report in Oberwolfach Report 46/2019, pp. 2905–2907. Its general setup allows homogeneous extremal functions without an explicit degree-one restriction. Its flag-variety example places them in `R_1`. Theorem 2 concerns that flag-variety setting; Conjecture 3 proposes a general extension under an edgewise rational-root condition. Section 2 announces the modified valuation without giving its formula or explicitly specifying its values on the extremal functions. Consequently the 2019 text alone does not establish its normalization for this higher-degree example. [S1]

The later construction fixes the missing convention: Remark 2.10 adds the cone vertex and its terminal bond; Definition 6.2 defines the chain valuation; Example 6.8 gives `V_C(f_p)=e_p`. Corollary 7.5 recovers homogeneous degree as the sum of value coordinates weighted by the degrees of the extremal functions. [S2]

For further scope control, *On normal Seshadri stratifications*, arXiv:2206.13171v2, Definition 2.9, explicitly requires degree-one extremal functions in its definition of LS-type. This example has degree-two extremal functions and falls outside that definition. [S3]

## 2. Geometric data and hypotheses

Work over `K=C`, and use the standard embedding

\[
X=\mathbb P^1=\mathbb P(\mathbb C^2),\qquad
R=\mathbb C[x,y],\quad \deg x=\deg y=1.
\]

Here `R` is the homogeneous coordinate ring of the embedding, equivalently the coordinate ring of the affine cone `A^2`. It is not the ring of global regular functions on the projective curve, and it is not a Veronese subring.

Let `A={p>q}`, with

\[
Y_p=X,\qquad Y_q=\{[0:1]\},\qquad f_p=x^2,\quad f_q=y^2.
\]

All the geometric requirements of the reported setup hold:

1. The poset is finite and graded, with unique maximum `p` and unique minimum `q`.
2. `Y_q` is a point of codimension one in `Y_p`, and this is the only covering relation.
3. Both strata are projectively normal: their homogeneous coordinate rings are `C[x,y]` and `C[y]`, respectively, and both are integrally closed.
4. The equations indexed by elements not at most `p` are an empty family, defining `Y_p=X`. For `q`, the only such equation is `x^2=0`, whose projective zero set is exactly `Y_q`. These requirements are set-theoretic; they do not require a reduced defining equation.
5. `f_p` is nonzero on a dense open subset of `Y_p`, while `f_q([0:1])` is nonzero. The zero set of `f_p` on `Y_p` is `Y_q`. The zero set of `f_q` on `Y_q` is empty, the required empty union at a minimal stratum.

These checks also verify the conditions for the modern Seshadri construction. No singularity or projective-normality exception is being used.

The affine cones are

\[
\widehat Y_p=\mathbb A^2,\qquad
\widehat Y_q=\{x=0\}\simeq\mathbb A^1_y.
\]

The bond on `p>q` is

\[
b_1=\operatorname{ord}_{x=0}(x^2)=2.
\]

The extra hypothesis in Conjecture 3 is satisfied in precisely its stated function field:

\[
\eta=\frac{x}{y}\in\mathbb C(\widehat Y_p)=\mathbb C(x,y),
\qquad \eta^{b_1}=\frac{x^2}{y^2}=\frac{f_p}{f_q}.
\]

Indeed `eta` even has homogeneous degree zero. Therefore requiring this particular root to have degree zero would not remove the example.

## 3. Direct valuation computation

Use the modern chain valuation with coordinates ordered `(p,q)`, so the `p` coordinate is compared first. The terminal bond on the affine line to its origin is

\[
b_0=\operatorname{ord}_{y=0}(y^2)=2.
\]

Take `N=lcm(b_1,b_0)=2`. Let `g` be a nonzero homogeneous polynomial of ordinary degree `d`. Let `i` be the smallest exponent of `x` occurring with nonzero coefficient. Then

\[
g=x^i\big(cy^{d-i}+xh(x,y)\big),\qquad c\ne0,
\]

where the final term may be absent. Thus the first vanishing order is `nu_1(g)=i` and the first normalized coordinate is `i/2`. The next rational function in the defining recursion is

\[
g_0=\left.\frac{g^2}{(x^2)^i}\right|_{x=0}
    =c^2y^{2(d-i)}.
\]

Its vanishing order at the origin of the line is `2(d-i)`. Definition 6.2 divides this by `N b_0=4`. Hence

\[
V_C(g)=\left(\frac i2,\frac{d-i}{2}\right).
\tag{1}
\]

In particular,

\[
V_C(x)=\left(\tfrac12,0\right),\quad
V_C(y)=\left(0,\tfrac12\right),\quad
V_C(x^2)=(1,0),\quad V_C(y^2)=(0,1).
\]

Formula (1) proves that every homogeneous value lies in `(1/2)Z_{≥0}^2`. Conversely, for any integers `i,j≥0`, the homogeneous monomial `x^i y^j` has value `(i/2,j/2)`. There is exactly one maximal chain, so the minimum-over-chains condition introduces no further restriction. Therefore

\[
\Gamma_C=\tfrac12\mathbb Z_{\geq0}^{2}.
\tag{2}
\]

This conclusion follows from the explicit construction, not from assuming the contested semigroup formula.

## 4. Failure of the unweighted-total prescription

For a chain of length one with bond `b_1=2`, the displayed LS prescription specializes to

\[
\Gamma_{\mathrm{LS}}
 =\{(a_1,a_0)\in\mathbb Q_{\geq0}^2:
       2a_1\in\mathbb Z,\ a_1+a_0\in\mathbb Z_{\geq0}\}.
\tag{3}
\]

But `x` belongs to `R_1`, and its value `(1/2,0)` has nonintegral coordinate total. Equations (2) and (3) are unequal. Thus the geometric and root assumptions do not imply (3) for arbitrary-degree extremal functions under the normalization used in Section 3.

The correct degree identity here is

\[
\deg g=2a_1+2a_0.
\]

More precisely, this example admits the exact degree-aware description

\[
\Gamma_C
 =\{a\in\mathbb Q_{\geq0}^2:
        2a_1\in\mathbb Z,\ 2a_1+2a_0\in\mathbb Z_{\geq0}\}.
\tag{4}
\]

Indeed the two integrality conditions imply `2a_0∈Z`; together with nonnegativity they are equivalent to (2). This proves (4) only for this example. In general, Corollary 7.5 supplies the necessary identity

\[
\deg g=\sum_{s\in C}\deg(f_s)\,V_C(g)_s;
\]

it does not by itself give sufficient conditions for membership in an arbitrary value semigroup. No general repaired root-condition conjecture is proved here.

## 5. What genuine degree-one normalization changes

There are two distinct ways to leave the higher-degree example.

### 5.1 Replace the functions, keeping the embedding

For the same `R=C[x,y]`, choose `f_p=x` and `f_q=y`. The bonds, including the terminal bond, are both one. The same computation gives `V_C(x^i y^j)=(i,j)` and `Gamma_C=Z_{≥0}^2`. The unweighted prescription with `b_1=1` is exactly this semigroup. This replacement changes the extremal functions and their bonds.

### 5.2 Replace the embedding by the quadratic Veronese

Keep the sections `x^2,y^2` but use

\[
R^{(2)}=\bigoplus_{n\geq0}R_{2n}
       =\mathbb C[x^2,xy,y^2]
       \simeq\mathbb C[U,Z,W]/(UW-Z^2),
\]

with `deg U=deg Z=deg W=1`. This is the homogeneous coordinate ring of the conic embedding of `P^1` in `P^2`. The ring is normal: it is the invariant subring of `C[x,y]` under `(x,y)↦(-x,-y)`; an element of its fraction field integral over it lies in `C[x,y]` and is invariant. Thus this embedding is projectively normal.

Take the strata given by the whole conic and `[0:0:1]`, with extremal functions `U=x^2` and `W=y^2`. They now have degree one in this different coordinate ring. At the generic point of the point-stratum cone, `W` is a unit and `t=Z/W=x/y` is a local parameter. Since `U=t^2W`, the upper bond remains two, and `t^2=U/W` verifies the root condition. The terminal bond is now one because the line coordinate is `W`.

The resulting normalized valuation of a monomial `x^i y^j` in `R^{(2)}` is still `(i/2,j/2)`: after the first step, its squared-and-divided restriction is `y^{2j}=W^j`, whose terminal order is `j`, divided by `N b_0=2`. The allowed monomials have `i+j` even. Therefore the homogeneous value semigroup is

\[
\{(i/2,j/2):i,j\in\mathbb Z_{\geq0},\ i+j\text{ even}\}
 =\Gamma_{\mathrm{LS}}
\]

from (3). For the reverse inclusion, `2a_1` and `2a_0=2(a_1+a_0)-2a_1` are nonnegative integers with even total, so the corresponding monomial belongs to `R^{(2)}`. The conic degree is `a_1+a_0`.

Crucially, `x` is not an element of `R^{(2)}`. Calling `x^2,y^2` degree-one functions without changing the ring would erase this distinction. The fact that the underlying projective variety is isomorphic to `P^1` does not make the two embedded coordinate rings or their gradings interchangeable.

## 6. Conclusion

The frozen candidate's calculation is correct with the explicit modern normalized valuation. Its unconditional historical-refutation wording needs qualification because the abbreviated 2019 report does not determine that normalization outside its degree-one example. The defensible result is a **normalization-dependent arbitrary-degree obstruction**, together with the exact weighted description (4) and the two explicitly checked degree-one alternatives above.

No claim is made about novelty, a full resolution of Conjecture 3 under its intended conventions, or a general characterization after a grading repair.

## References

- **[S1]** Peter Littelmann, joint work with Rocco Chirivì and Xin Fang, *Flag varieties, Valuations and Standard Monomial Theory*, in *Mini-Workshop: Degeneration Techniques in Representation Theory*, Oberwolfach Report 46/2019, pp. 2905–2907. [Report PDF](https://ems.press/content/serial-article-files/46825), PDF pages 37–39. [Report DOI](https://doi.org/10.4171/OWR/2019/46).
- **[S2]** Rocco Chirivì, Xin Fang, Peter Littelmann, *Seshadri stratifications and standard monomial theory*, Inventiones mathematicae **234** (2023), 489–572. [Version of record](https://doi.org/10.1007/s00222-023-01206-4); [arXiv:2112.03776v2](https://arxiv.org/abs/2112.03776v2). Precise locators: arXiv pp. 11, 15, 20–24, 30; Remark 2.10, Definition 6.2, Example 6.8, Corollary 7.5. The latter four appear on journal pp. 504, 514, 515, 522.
- **[S3]** Rocco Chirivì, Xin Fang, Peter Littelmann, *On normal Seshadri stratifications*, [arXiv:2206.13171v2](https://arxiv.org/abs/2206.13171v2), revised 30 August 2025, Definition 2.9, p. 8. The arXiv record reports publication in Pure and Applied Mathematics Quarterly **20** (2024), no. 3, 1097–1139. The locator used here is specifically the 2025 arXiv revision.
