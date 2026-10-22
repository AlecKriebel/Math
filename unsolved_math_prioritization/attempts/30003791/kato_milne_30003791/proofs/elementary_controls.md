# Elementary reductions and countercontrols

These statements are elementary or overlap cited literature. No originality is claimed. Throughout, `p` is prime and `F` is a field of characteristic `p`. Put

\[
H_p^{q+1}(F)=\Omega_F^q/(d\Omega_F^{q-1}+\wp\Omega_F^q),\qquad
\wp(a\,d\log b_1\wedge\cdots\wedge d\log b_q)
=(a^p-a)\,d\log b_1\wedge\cdots\wedge d\log b_q
\]

where the latter formula is interpreted modulo exact forms. A symbol in `H_p^n` has **one additive slot and n−1 logarithmic slots**. Its degree is `n`, not `n−1`. Write `[a;b_1,...,b_{n-1}]` for its class. All multiplicative entries are nonzero.

## 1. Appending a logarithmic slot is well defined

For fixed `c ∈ F×`, the operation `ω ↦ ω ∧ dlog c` descends to `H_p^n(F) → H_p^{n+1}(F)`.

Indeed `d(dlog c)=0`. Thus an exact form `dη` is sent to `d(η∧dlog c)`. For an Artin–Schreier generator `(a^p−a)dlog b_1∧...∧dlog b_q`, its image is the Artin–Schreier image of `a dlog b_1∧...∧dlog b_q∧dlog c`. Additivity proves the claim. Repeating this argument permits any fixed string of logarithmic factors. Notice that this constructs a module action by logarithmic forms, not a product of two arbitrary Kato–Milne classes.

## 2. Universal separable linkage implies symbol length at most one

Assume `n≥2` and every two symbols in `H_p^n(F)` admit a common symbol factor `θ∈H_p^{n−1}(F)`, so that they can be written `θ∧dlog x` and `θ∧dlog y`.

Their sum is `θ∧dlog(xy)`, hence is again a symbol; `xy` is nonzero. Zero is a symbol, for example one whose additive entry is zero. By induction on the number of summands, every finite sum of symbols is a symbol. Symbols generate `H_p^n(F)`, because differential forms are finite sums of decomposable forms and every nonzero differential entry can be converted to a logarithmic entry by moving its value into the coefficient. Therefore every class has symbol length at most one.

This is only a consequence in degree `n`; it does not establish vanishing in degree `n+1` or `n+2`. We do not assert the converse for odd `p`.

## 3. A finite p-basis gives direct vanishing

Suppose `F` has a finite p-basis `t_1,...,t_r`: the monomials `t_1^{e_1}...t_r^{e_r}`, `0≤e_i<p`, form a basis of `F` over `F^p`.

Every `a∈F` has a unique expansion `Σ_e c_e^p t^e`. Differentiating this expression shows that `dt_1,...,dt_r` span `Ω_F^1`. They are independent: the formal partial derivatives of the monomials define `F^p`-derivations `∂_i` with `∂_i(t_j)=δ_ij`. One can construct these on `F^p[T_1,...,T_r]/(T_i^p−t_i^p)`; the defining relations have derivative zero and this quotient maps isomorphically to `F`. Applying the induced linear functionals on `Ω_F^1` proves independence.

Consequently `Ω_F^q=0` for `q>r`, and therefore `H_p^m(F)=0` for `m>r+1`. In particular:

- `r≤n` implies `H_p^{n+2}(F)=0`;
- `r≤n−1` implies `H_p^{n+1}(F)=0`.

Neither conclusion requires linkage. These cover restricted fields only; no p-rank bound is inferred from linkage.

## 4. Total inseparable one-factor sharing is sufficient

Fix `n≥2`. Assume the following extra property: for every symbol `θ∈H_p^{n−1}(F)` and every `b,c∈F×`, the two symbols `θ∧dlog b` and `θ∧dlog c` share all their logarithmic one-factors (factors in `ν_F(1)`). In particular, the specific factor `dlog c` of the second symbol is a factor of the first. Thus there is a symbol `η∈H_p^{n−1}(F)` such that

\[
\theta\wedge d\log b=\eta\wedge d\log c.
\]

Append `dlog c` using Section 1. The result is zero, since an exterior product with a repeated one-form is zero in every characteristic, including two. Every generator of `H_p^{n+1}(F)` is of the form `θ∧dlog b∧dlog c`, so `H_p^{n+1}(F)=0`.

This is the elementary mechanism also described in Chapman–Dolphin, *Types of linkage of quadratic Pfister forms*, Remark 3.7. Universal pairwise or triple **separable** linkage does not state this extra property. We have not derived it from either target hypothesis.

## 5. A self-contained nonvanishing detector over Laurent-series fields

Let

\[
K_r=\mathbf F_p((t_1))\cdots((t_r)),\quad r\ge1,
\qquad \Lambda_r=d\log t_1\wedge\cdots\wedge d\log t_r.
\]

The ordered iterated Laurent-series expansion defines the constant-coefficient functional `C_r:K_r→F_p`: first extract the coefficient of `t_r^0`, then `t_{r−1}^0`, and so on. This is additive, not asserted to be multiplicative.

### 5.1 The p-basis

The elements `t_1,...,t_r` are a p-basis of `K_r`. Prove this by induction. For a Laurent series in `t_r`, group exponents according to their residue modulo `p`, and apply the p-basis decomposition to each coefficient in `K_{r−1}`. A series all of whose exponents are divisible by `p` and whose coefficients lie in `K_{r−1}^p` is the pth power of a Laurent series: divide exponents by `p` and take the unique pth roots of the coefficients. This gives a spanning decomposition into the `p^r` monomials; uniqueness follows by comparison of coefficients and the induction hypothesis. Thus Section 3 applies, and `Ω^r_{K_r}=K_r Λ_r`.

### 5.2 The functional annihilates the defining relations

Define `R_r(fΛ_r)=C_r(f)`. For every `f∈K_r`,

\[
C_r(f^p)=C_r(f)^p=C_r(f).
\]

The first equality follows by taking coefficients successively in the iterated series; the final equality uses `C_r(f)∈F_p`. Since `Λ_r` is a logarithmic basis form, every Artin–Schreier image in top degree is represented by `(f^p−f)Λ_r` modulo exact forms. Hence `R_r` kills these representatives.

Every `(r−1)`-form is uniquely a sum of terms

\[
g_i\,d\log t_1\wedge\cdots\wedge\widehat{d\log t_i}\wedge\cdots\wedge d\log t_r.
\]

Its derivative has top coefficient a signed sum of `t_i∂_i g_i`. In a series expansion, `t_i∂_i` multiplies a monomial by its `t_i`-exponent modulo `p`. The fully constant monomial has exponent zero, and no other monomial is moved to exponent zero. Therefore `C_r(t_i∂_i g_i)=0`. This termwise description agrees with the algebraic derivation from the p-basis: write a series as `Σ_e h_e^p t^e`, whose derivative is `Σ_e h_e^p d(t^e)`. No unproved interchange of an arbitrary discontinuous derivation and an infinite sum is needed.

Thus `R_r` annihilates exact forms and Artin–Schreier images. It induces an additive map

\[
\overline R_r:H_p^{r+1}(K_r)\longrightarrow\mathbf F_p.
\]

As `R_r(Λ_r)=1`, the class `[1;t_1,...,t_r]` is nonzero. In particular, `H_p^{r+1}(K_r)≠0`.

### 5.3 Selected linked symbols do not give global linkage

For any `n≥2`, take `r=n+1`, let `θ=[1;t_1,...,t_{n−2}]∈H_p^{n−1}(K_{n+1})`, and let

\[
s_j=\theta\wedge d\log t_{n-2+j},\qquad j=1,2,3.
\]

For `n=2`, the empty logarithmic string means `θ=[1]∈H_p^1`. The three symbols `s_j` have the displayed common separable `(n−1)`-factor. Nevertheless

\[
\theta\wedge d\log t_{n-1}\wedge d\log t_n\wedge d\log t_{n+1}
=[1;t_1,...,t_{n+1}]\ne0\quad\text{in }H_p^{n+2}(K_{n+1}).
\]

Each `s_j` is itself nonzero: if it were zero, appending the other logarithmic slots and adjusting their order would make the displayed nonzero top class zero. The same argument shows `θ≠0`.

Similarly, over `K_n`, the two displayed symbols `θ∧dlog t_{n−1}` and `θ∧dlog t_n` are linked but their appended class in `H_p^{n+1}` is nonzero.

**Logical scope:** these are counterexamples to an attempted *local* implication about one chosen pair/triple. We have not proved that either field satisfies universal linkage of all pairs or all triples in `H_p^n`. They are not counterexamples to either Oberwolfach question.

## 6. The odd-prime presentation-sign obstruction

For `a∈F`, `b∈F×`, a symbol algebra of degree `p` has presentation

\[
[a,b)_{p,F}=F\langle i,j\mid i^p-i=a,\quad j^p=b,\quad jij^{-1}=i+1\rangle.
\]

Here `j` is invertible. Set `I=−i`, `J=j^{-1}`. The characteristic-p identity `(-i)^p=−i^p` also holds when `p=2`, where minus equals plus. Directly,

\[
I^p-I=-a,\qquad J^p=b^{-1},\qquad JIJ^{-1}=-(i-1)=I+1.
\]

Conversely, `i=−I` and `j=J^{-1}`, so the new generators generate the same algebra. Hence `[a,b)≅[-a,b^{-1})` as central `F`-algebras.

Apply this change simultaneously to the pair `[a,b)`, `[a,c)`. Its proposed appended class changes by

\[
(-a)\,d\log(b^{-1})\wedge d\log(c^{-1})
=-a\,d\log b\wedge d\log c.
\]

For odd `p`, take `F=K_2`, `a=1`, `b=t_1`, `c=t_2`. Section 5 shows the original class has detector value `1`; the new one has value `−1`, which differs from `1`. Consequently the element of `H_p^3(F)` obtained this way is not an invariant of the pair of isomorphism classes. This reproduces the obstruction stated in Chapman, *Linkage and essential p-dimension*, Remark 3.6, with an explicit nonzero control.

This sign change does **not** disprove invariance of whether the class vanishes: `z=0` if and only if `−z=0`. It blocks treating the element itself as presentation-independent; it does not settle either target vanishing question.
