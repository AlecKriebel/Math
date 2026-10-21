# Compact-action stress test for the averaging hypotheses

This is an adversarial diagnostic of the axioms in PR48's equation (5), not a proposed solution of KP-4.85 or a claim of novelty. It was developed during this audit after the early independent universal derivation. Its role is to distinguish a missing uniform estimate from a universal impossibility assertion.

Take the closed orientable smooth four-manifold `X=R/Z x S^3`, fix a point `p` of `S^3`, and put `mu=delta_(0,p)`. Let `H(t,p')=1/t` for the unique representative `0<t<1`, and set `H(0,p')=0`. This is an everywhere finite Borel function, although it is neither bounded nor continuous. For any smooth diffeomorphism `f` set

`c(f,x)=H(fx)-H(x)`.

This is an exact cocycle with target the additive real group: `c(fg,x)=c(f,gx)+c(g,x)`. Set `psi(a)=a`, a homomorphism with defect zero. Every integral required by the displayed cocycle calculation is finite for this fixed Dirac measure, for every pair of diffeomorphisms: it is evaluation at one or two points and `H` is finite everywhere. The resulting average is `Q(f)=H(f(0,p))`.

Let `f_n` rotate the circle coordinate by `1/n`, and let `g` rotate it by `1/4`, acting identically on `S^3`. These are smooth diffeomorphisms in the full identity component. For every integer `n>=5`, there is no wraparound in `1/n+1/4`, and

`Q(f_n)=n`, `Q(g)=4`, `Q(f_n g)=4n/(n+4)`.

Consequently

`Q(f_n g)-Q(f_n)-Q(g)=-n-16/(n+4)`,

whose magnitude is at least `n`. Thus the target cocycle and `psi` have zero defect while the average has unbounded defect. It is exactly the signed-pushforward term, since `g_*mu=delta_(1/4,p)`:

`integral c(f_n,y) d(g_*mu-mu)(y)`
`= (H(1/n+1/4,p)-H(1/4,p))-(H(1/n,p)-H(0,p))`.

This example uses a Borel cocycle and an atomic measure. It does not claim that a particular smooth geometric cocycle from the literature has unbounded averaging defect, and it does not create a homogeneous quasimorphism on `Diff_0(X)`. Indeed `X=S^1 x S^3` belongs to the cited uniformly perfect class, consistently with the fact that this `Q` fails to be a quasimorphism.

There is also a simple contrasting example: replace `H` by a bounded Borel height. The signed-pushforward term is then uniformly bounded by `2||H(f(.))-H(.)||_infinity`, or a bound depending only on the height range. Noninvariance by itself need not produce unbounded defect. The original note states only that a uniform bound was not supplied for the intended transfer route, and its caveat that other averaging constructions might work is necessary and correct.

The accompanying new checker verifies the exact defect formula for `5<=n<=104`, tests weighted rational circle actions, and checks the opposite sign as a negative predicate. The formula above proves unboundedness for all integers `n>=5`; the conclusion is not extrapolated from the finite sample.
