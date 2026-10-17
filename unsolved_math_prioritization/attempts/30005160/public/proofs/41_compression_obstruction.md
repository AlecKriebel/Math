# Proof 41  An exact obstruction to independently aligning compressed pairs

Included dependencies: [Exact one phase integration of the entropy kernel](14_one_phase_entropy.md); [Angular order under a common rotation](15_common_rotation.md); [Dominant endpoint entropy and nearby power comparisons](17_dominant_endpoint_entropy.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## 1. The proposed compression and the lost angle

For independent unit complex variables `Z1,Z2`, use the Haar-preserving torus map

`Z1=UV`, `Z2=U/V`,

where `U,V` are independent uniform unit complex variables. The map is a surjective torus homomorphism; its finite kernel does not affect the pushforward Haar law.

Fix `a1>a2>0`, `0<q<1`, and put `b_j=q a_j`. The all-positive pair sum, conditional on `V`, is

`p(V) U+q conjugate(p(V))/U`, `p(V)=a1 V+a2/V`.

After a harmless reparametrization of `U`, this is a horizontal ellipse with endpoint magnitudes `R_+(V),q R_+(V)`, where

`R_+^2=a1^2+a2^2+2a1a2 cos(2 arg V)`.

Flip only `b2`. The conditional expression is now

`p(V) U+q(a1/V-a2 V)/U`.

Its endpoint magnitudes are `R_+(V),q R_-(V)`, where

`R_-^2=a1^2+a2^2-2a1a2 cos(2 arg V)`.

In general this compressed ellipse is rotated. The accepted common-rotation theorem bounds its Green expectation, at a nonnegative real center, above by the expectation of the horizontal ellipse with the same endpoint magnitudes.

It is tempting to finish by claiming that the all-positive average dominates this independently aligned upper bound. That claim is false, even strictly inside a regime where the actual target has an exact positive gap.

## 2. Exact difference of the all-positive value and that upper bound

Write

`J(a,b;c)=E K(c+aU+b/U)`.

Assume

`0<=c<=a1-a2-q(a1+a2)`.                                          (1)

For every `V`, both horizontal ellipses in the proposed comparison satisfy `a>=b` and `c<=a-b`, so the accepted interior formula applies:

`J(a,b;c)=(a^2+b^2+c^2)log a+c^2+b^2+(b/(2a))c^2`.

Define the difference

`D=E_V J(R_+,q R_+;c)-E_V J(R_+,q R_-;c)`.

The two marginal second moments of `R_+` and `R_-` agree. Subtracting the two interior formulas gives exactly

`D=2q^2 a2^2-(q c^2/2)(C-1)`,                                   (2)

where

`C=E_V R_-/R_+`.

Here is a direct verification of the first term. Set `t=2 arg V`, which is uniform modulo `2pi`. The absolutely convergent Fourier series

`log R_+=log a1+sum_(k>=1) (-1)^(k+1)(a2/a1)^k cos(kt)/k`

and `R_+^2-R_-^2=4a1a2 cos t` imply

`E[(R_+^2-R_-^2)log R_+]=2a2^2`.

For the second term, write

`kappa=2a1a2/(a1^2+a2^2)`, so `0<kappa<1`.

Pairing `t` and `t+pi` yields

`C=E_t (1-kappa^2 cos^2 t)^(-1/2)`.

Since `(1-u)^(-1/2)>=1+u/2` on `0<=u<1`,

`C-1>=kappa^2/4`.                                               (3)

In particular the negative term in (2) is linear in `q`, whereas the positive term is quadratic. For every allowed `a1,a2,c>0`, sufficiently small positive `q` makes `D<0`.

## 3. A fully rational instance and the actual target's opposite sign

Choose

`a1=2`, `a2=1`, `q=1/200`, `c=1/2`.

The endpoint pairs are `(2,1/100)` and `(1,1/200)`, both genuinely unequal and nonzero. Condition (1) holds because

`1/2<=1-3/200=197/200`.

Here `kappa=4/5`, so (2)--(3) give

`D<=1/20000-1/10000=-1/20000<0`.                                 (4)

Thus the independently aligned compressed upper bound is strictly larger than the all-positive expectation. It cannot prove the desired comparison for this example.

Nevertheless, the **actual** all-positive minus one-pair-flipped entropy gap for exactly these coefficients is

`1/20000>0`.                                                      (5)

Indeed, integrate out the first endpoint pair `(a,b)=(2,1/100)`. Its root-containment margin is `a-b=199/100`, whereas the magnitude of the remaining center-plus-pair is at most

`c+a2+b2=1/2+1+1/200=301/200<199/100`.

Both sign configurations therefore use the accepted interior quadratic. Its exact orthogonality gap, with the first pair unflipped and the second flipped, is

`(2b/a) a2 b2=(1/100)(1/200)=1/20000`.

Equivalently, the retained orientation of the compressed signed ellipse contributes a favorable term that the common-rotation upper bound discards. Formula (4) demonstrates that this loss is not merely a technical concern or a zero-gap endpoint.

## 4. Equivalent local obstruction in the one-ellipse kernel

There is also an exact differential warning against using ordinary endpoint-square supermodularity after compression. Put

`H(u,v)=J(sqrt(u),sqrt(v);c)`.

On the open interior region `sqrt(u)>sqrt(v)+c`, direct differentiation of the same interior formula gives

`H_uv=1/(2u)-c^2/(8u^(3/2)sqrt(v))`.

It is negative whenever `c^2>4sqrt(uv)`, which is compatible with that region. Thus the horizontal one-ellipse expectation is not generally supermodular in its squared endpoint magnitudes. This is a different kernel from the accepted scalar center/random-radius supermodularity and does not contradict it.
