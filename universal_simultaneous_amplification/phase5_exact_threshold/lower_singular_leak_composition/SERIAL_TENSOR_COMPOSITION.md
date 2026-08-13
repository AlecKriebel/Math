# Serial and tensor composition of the singular leak ray

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Question and conclusion

The singular three-type adjoint family supplies, after positive
normalization, the response ray

\[
                         (G,D)=(1,r-1),                       \tag{1}
\]

where `G` is Bd gain over the complete branching baseline and `D` is dB
cost below it.  Since `0<r-1<1` below fitness two, it is natural to ask
whether a depth-`L` serial, tensor, or hierarchical composition changes the
ray to

\[
                         (1,(r-1)^L).                         \tag{2}
\]

For the literal tensor product and for a serial cascade made from the same
singular cold-root mechanism, the answer is **no**.  The exact composition
law changes only the total mass of polarized starting types.  The ratio
remains `r-1` at every depth.

The obstruction is local and proof-first: the outer singular root saturates
its Bd and dB survival coordinates to `(1,0)`.  It does not transmit a
small response linearly, so there is no transfer matrix whose lower
coordinate can be repeatedly multiplied by `r-1`.

## 2. One exact cold-root identity

Let `p` be the uniform-initialization type law, let `P` be row stochastic,
and put

\[
 R=D_p^{-1}P^TD_p,\qquad t=R\mathbf1.                         \tag{3}
\]

The diffuse rare-mutant survival vectors at fitness `r>1` obey

\[
 t_i b_i=r(1-b_i)(Pb)_i,\qquad
 s_i=r(1-s_i)(Rs)_i.                                        \tag{4}
\]

Writing `y_i=(Pb)_i` and `z_i=(Rs)_i`, (4) gives pointwise, without an
approximation,

\[
 \boxed{b_i={r y_i\over t_i+r y_i},\qquad
        s_i={r z_i\over1+r z_i}.}                            \tag{5}
\]

Because `0<=s<=1` and `R` is nonnegative,

\[
                         0\le z_i\le(R\mathbf1)_i=t_i,
\]

and hence

\[
 \boxed{0\le s_i\le {r t_i\over1+r t_i}.}                  \tag{6}
\]

Consider a singular root sequence `i=i_k` satisfying

\[
 t_i\longrightarrow0,qquad {t_i\over(Pb)_i}\longrightarrow0. \tag{7}
\]

The second condition is exactly the live-leak condition: however small the
downstream leak is, it is still asymptotically larger than the root's
reverse temperature.  Equations (5)--(7) force

\[
                         (b_i,s_i)\longrightarrow(1,0).      \tag{8}
\]

Write `p_0=(r-1)/r` for the complete branching baseline.
In fact, saturation is the *best* cold-root tradeoff, not merely one
special case.  Suppose only that `t_i->0`, and pass to a subsequence on
which `b_i->b`.  Then (6) still gives `s_i->0`.  If this root has positive
Bd gain, so `b>p_0`, its limiting cost/gain ratio obeys

\[
 {p_0\over b-p_0}-(r-1)
 ={(r-1)(1-b)\over b-p_0}\geq0.                             \tag{9}
\]

Equality holds exactly when `b=1`, equivalently in the live-leak
saturation regime (7).  Thus allowing a finite crossover
`t_i/(Pb)_i` does not improve the ray: while the root remains cold, it can
only make the tradeoff worse.  Moving initialization mass `c` from a
baseline type `(p_0,p_0)` to the cold root (8) changes the two averages by

\[
 \Delta\beta=c(1-p_0)={c\over r},\qquad
 p_0-\Delta\sigma={c(r-1)\over r}.                          \tag{10}
\]

Thus

\[
 \boxed{{\hbox{dB cost}\over\hbox{Bd gain}}=r-1.}           \tag{11}
\]

This is the exact mechanism behind the three-type ray.  Importantly, the
downstream value `y_i` disappears from the limit (8).  An outer cold root
therefore **resets** to (8); it does not multiply the response supplied by
the next layer.

### Serial consequence

Suppose a serial or hierarchical cascade has cold roots `i_l` of
initialization masses `c_l`, its relay masses are `o(sum_l c_l)`, and all
other types retain the baseline coordinates to `o(sum_l c_l)`.  If every
root satisfies (7), summing (10) gives

\[
 \Delta\beta={1\over r}\sum_lc_l+o\!\left(\sum_lc_l\right),
\]

\[
 p_0-\Delta\sigma={r-1\over r}\sum_lc_l
                  +o\!\left(\sum_lc_l\right).              \tag{12}
\]

The ratio again tends to `r-1`, regardless of depth or ordering.  More
generally, (9) shows that any nonnegative sum of positive-gain cold-root
responses has ratio at least `r-1`.  This is the strongest serial statement
justified by the cold-root equations.  It does not cover a gain-carrying
layer whose temperature stays bounded away from zero, nor a same-order
compensating response elsewhere in the hierarchy.

## 3. Literal tensor composition

Now take the positive undirected-realizable three-type family before its
singular limits.  Its type law and symmetric weight matrix may be written

\[
 p=(c-\varepsilon,\varepsilon,1-c),                          \tag{13}
\]

\[
 W=\begin{pmatrix}
 \varepsilon&(1-\theta)/\varepsilon&\theta/(1-c)\\
 (1-\theta)/\varepsilon&1&1\\
 \theta/(1-c)&1&1/\varepsilon
 \end{pmatrix}.                                             \tag{14}
\]

The prescribed order of limits is

\[
 \varepsilon\downarrow0,quad\hbox{then}\quad
 \theta\downarrow0,                                       \tag{15}
\]

with `c` retained.  The infinitesimal `theta` leak is what keeps the cold
root's Bd input live while its reverse temperature vanishes.

For depth `L`, use

\[
 p^{(L)}=p^{\otimes L},\qquad W^{(L)}=W^{\otimes L}.         \tag{16}
\]

The tensor weight matrix is symmetric and positive.  Moreover, if
`delta_i=sum_j p_jW_ij`, then

\[
 \delta_{(i_1,\ldots,i_L)}^{(L)}=\prod_{l=1}^L\delta_{i_l},
\]

so the induced row kernel and its `p`-adjoint are exactly

\[
                         P^{(L)}=P^{\otimes L},\qquad
                         R^{(L)}=R^{\otimes L}.              \tag{17}
\]

Thus this is a legitimate tensor composition inside the same
undirected-realizable diffuse normal form, not merely a formal product of
response vectors.

After (15), a tensor type containing at least one cold `A` coordinate and
no vanishing-mass relay coordinate has temperature tending to zero.  The
positive leak in every `A` coordinate makes its Bd input live before
`theta` is sent to zero.  Equations (5)--(8) therefore give the same
polarized limit `(1,0)` for every such type.  The all-sticky `C^L` type has
the baseline limit `(p_0,p_0)`, while every type containing a `B` relay has
vanishing initialization mass.

The total polarized mass is consequently

\[
                         q_L=1-(1-c)^L.                       \tag{18}
\]

The limiting averaged endpoints are exactly

\[
 \boxed{
 \beta_L=p_0+{q_L\over r},\qquad
 \sigma_L=p_0-{(r-1)q_L\over r}.}                           \tag{19}
\]

Therefore, for every `L>=1` and every `0<c<1`,

\[
 \boxed{
 {p_0-\sigma_L\over\beta_L-p_0}=r-1,}                       \tag{20}
\]

not `(r-1)^L`.

The binary composition law is equally explicit.  If two singular profiles
have polarized masses `q_1,q_2`, then

\[
 q_1\oplus q_2=1-(1-q_1)(1-q_2)
               =q_1+q_2-q_1q_2.                            \tag{21}
\]

The response map

\[
 \Phi_r(q)=\left({q\over r},{(r-1)q\over r}\right)          \tag{22}
\]

satisfies

\[
 \Phi_r(q_1)\mathbin{\widehat\otimes}\Phi_r(q_2)
 =\Phi_r(q_1\oplus q_2).                                   \tag{23}

This is a union law on polarized mass.  It is not the coordinatewise
product of the two response vectors.

At the tangent scale,

\[
 q_L=Lc-\binom L2c^2+O(L^3c^3).                             \tag{24}
\]

Hence fixed-depth first responses add.  The same conclusion holds on a
growing diagonal whenever `Lc->0` and the singular-limit errors are chosen
`o(Lc)`.

## 4. Why depth does not solve interval uniformity

For

\[
 I_k=[1+1/k,2-1/k],
\]

the actual tensor or cold-root serial ratio satisfies

\[
 \sup_{r\in I_k}{D_L(r)\over G_L(r)}=1-{1\over k}            \tag{25}
\]

at every depth.  The hoped-for powered law would instead give

\[
 \sup_{r\in I_k}(r-1)^L=(1-1/k)^L,                          \tag{26}
\]

which tends to zero if `L/k->infinity`.  Equations (20) and (25) show that
this attenuation does not occur.  Choosing `L_k>>k` only changes the
amplitude `q_L`; it does not rotate the response cone toward the Bd axis.

## 5. Exact escape conditions

The result closes the direct interpretation of the singular leak ray as a
repeatable diagonal attenuator.  It is not a universal no-go theorem for
all lower constructions.  A successful hierarchy must violate at least one
of the ingredients above:

1. **A non-cold gain layer:** some gain-carrying layer must keep `t_i`
   bounded away from zero at the response scale.  By (9), merely putting a
   cold root at the crossover `t_i/(Pb)_i asymptotic 1` worsens rather than
   improves its local ratio.
2. **Same-scale compensation:** types outside the cold roots must contribute
   positive dB response at the same order as the Bd gain.
3. **Non-diffuse interaction:** same-colony collisions or portal action must
   survive at the response scale, invalidating the independent branching
   equations (4).
4. **Signed rather than positive composition:** cancellation between
   genuinely different response mechanisms may rotate the cone, whereas a
   nonnegative sum of copies of (1) cannot.

Any one of these would be a materially different mechanism.  Merely taking
more tensor factors or nesting more saturated leak roots cannot produce
the power `(r-1)^L`.

## 6. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_serial_tensor_composition.py
```

The replay checks the cold-root algebra, the tensor realization identities,
the union composition law, the depth expansion, and the compact-interval
comparison symbolically.
