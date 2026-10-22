# Independent elementary verification of the ACM and radical step

Recorded 2026-10-21 05:04:42 UTC. Audit completion estimate: 80%, with the extended finite search pending. This supplement was obtained without reading the original final review or other fresh audit reports.

There is a direct algebraic verification that avoids invoking generic reducedness or an embedded-prime criterion in the plane-arrangement step. It establishes exactly the saturation/radicality statement at issue.

Let `P1,...,Pd` be distinct nonproportional linear forms in `R=k[x0,x1,x2,x3]`, with `d>=2`; put `F=product Pi` and `J_d=(F/P1,...,F/Pd)`.

## Ideal identity under the no-triple-line hypothesis

If every three forms are linearly independent, then

`J_d = intersection_{i<j} (Pi,Pj)`.

The inclusion from left to right follows term by term. For the reverse inclusion, induct on d, starting with `d=2`. For `f` in the right-hand side, reduce modulo `Pd`. The restrictions of `P1,...,P_(d-1)` to `R/(Pd)` are nonzero, pairwise nonproportional linear forms; otherwise `Pd,Pi,Pj` would be linearly dependent. Since the quotient is a polynomial UFD, the intersection of their principal ideals is their product. Hence

`f = A P1 ... P_(d-1) + Pd B`.

Both f and the first summand belong to every pair ideal `(Pi,Pj)` with `i<j<d`. Each such ideal is prime, and `Pd` is not in it. Therefore B belongs to their intersection. The induction hypothesis expresses B as a combination of `product_{j<d,j!=i} Pj`, so the displayed expression for f is a combination of exactly `F/Pd` and the `F/Pi` for `i<d`.

This proves that J is the intersection of its distinct saturated line primes. It is consequently radical and saturated over every field, with no condition on concurrency of planes at a point. For `d=2`, no restriction on triples is needed.

## Exact free resolution without a Hilbert-Burch black box

For arbitrary distinct forms (even if a triple shares a line), the generator map has all syzygies generated freely by

`Pi e_i - Pd e_d`, for `1<=i<d`.

Indeed, if `sum hi (F/Pi)=0`, reduction modulo `Pi` shows that `Pi` divides `hi`: all other terms have the Pi factor, while `F/Pi` is nonzero in the domain `R/(Pi)`. Write `hi=Pi ai`; cancel F in the original relation to obtain `sum ai=0`. Thus the relation is `sum_{i<d} ai(Pi e_i-Pd e_d)`. These d-1 syzygies are independent because their ith coordinates are `Pi ai` in a domain.

Consequently there is an exact graded sequence

`0 -> R(-d)^(d-1) -> R(-(d-1))^d -> J_d -> 0`.

The common vanishing locus of J is the union of pair intersections, so its height is two. The resolution gives depth at least two for `R/J`; its dimension is two, hence it is Cohen-Macaulay. Combining this with the ideal identity proves that the reduced line union is ACM. It also gives the tested Hilbert-series numerator `1-d*t^(d-1)+(d-1)*t^d`.

## Why the excluded degeneration matters

For `F=x*y*(x+y)*z`, the line union is the four distinct pair-intersection lines. Its radical ideal contains `x*z`, whereas J is generated in degree three and cannot contain that quadratic. Yet `(x*z)^2=z*(g_y-g_(x+y))` belongs to J, where `g_y=x*(x+y)*z` and `g_(x+y)=x*y*z`. Thus J really is nonradical in every characteristic, including characteristic two. The proposed proof's no-triple-line deduction is essential and correctly precedes the radical/ACM conclusion.

Status: the full ACM/saturation step is independently verified by an elementary ideal identity and explicit resolution. This remains downstream of the separately audited surface assertion.
