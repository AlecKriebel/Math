# Independent adversarial review: moments and rational ball module

Final mathematical checkpoint: 2026-10-06 18:01:00 UTC.
Assigned-review completion estimate: 100% after final manifest closure.
Target: PR 278, problem 30005468, original head
`deb9d7491a0bf887f7615717a5b484caf212cfd6`.
Bound original PROOF SHA-256:
`866f036f3541721d82cc9d06da2ee4e1d8ed8f083c44bdb914b7befc9fa12881`.

**Verdict: PASS for the assigned fixed-polynomial, rational-square,
arbitrary-finite-degree mathematical claim.** No repair is required to the
frozen proof's moment construction or origin-jet exclusion. This is a review
of a credited construction. It does not approve publication, historical
novelty, the source's intended interpretation, or any claimed-solved label.
Original-question interpretation is owned by the separate source family.

## Exact statement checked

Let `g=1-x²-y²-z²`, let `K={g>=0}`, and set `p=1+f`, with the nine-term
quartic displayed in the frozen proof. Let `m` include every monomial of
total degree at most four, with `m_0=1`, `m_(4,0,0)=-1`, and all other
entries zero. A rational module certificate means a finite identity

`p-1 = Σ a_j² + g Σ b_k²`, with `a_j,b_k in Q[x,y,z]`.

The number and degrees of factors are arbitrary but finite. The checked
claim is that this identity exists over `R` and fails over `Q`, whereas
`L_m(p)=0` and `p>=1` on `K`. It is existential for this fixed `p`.

## Moment and support checks

There are `binomial(7,3)=35` required entries. Since the coefficient of
`x⁴` in `f` is one, `L_m(p)=1-1=0`. Any nonnegative representing measure
would have nonnegative `x⁴` integral, contradicting `m_(4,0,0)=-1`.
This is a support-independent contradiction and does not rely on any
conic-duality theorem. On the ball there is also the mass-one contradiction
`integral p >= integral 1 = 1`, incompatible with `L_m(p)=0`.

The moment matrix indexed through degree two has ten rows and columns.
Its diagonal entry at the index `x²` is `-1`; thus the vector is not PSD.
The full exact matrix and index order are recorded in CONTROL_RESULTS.json.
The construction therefore does not answer a variant restricted to
relaxation-feasible PSD inputs. The frozen proof states that limitation.

The ball contains zero and is compact. Its rational Archimedean witness
is exactly `1-x²-y²-z²=g`. Positive rational scalar coefficients are
rational sums of squares, so there is no irrational-scalar ambiguity in
this witness. Since `f` is a global real SOS and `f(0)=0`, the exhibited
minimum is **exactly one**. The polynomial's strict positivity is sufficient
for the stated moment separation; the residual `p-1` has zero margin.

## The all-degree obstruction

Assume the rational finite identity for `f=p-1`. Write `a_j^[d]` for the
degree-`d` homogeneous part of a factor, and similarly for `b_k`.
Evaluation at zero gives

`0 = Σ (a_j^[0])² + Σ (b_k^[0])²`.

Both weights are one. Every constant factor is therefore zero. This is
an equality of ordinary real nonnegative numbers, so there is no possible
cancellation between the two collections.

The degree-two component then becomes

`0 = Σ (a_j^[1])² + Σ (b_k^[1])²`.

The term `- (x²+y²+z²) Σ b_k²` cannot contribute at degree two, because
the constants have vanished. Evaluate this polynomial identity at every
real point: each summand is nonnegative, so every linear form is zero.
All square factors now have vanishing order at least two.

Consequently the degree-four identity is exactly

`f = Σ (a_j^[2])² + Σ (b_k^[2])²`.

The generator's nonconstant part contributes only from degree six onward.
This is a rational SOS of quadratic forms and contradicts the credited
quartic obstruction, independently rechecked below. The reasoning neither
bounds maximum factor degrees nor assumes high-degree terms cannot cancel.
It concerns the earliest possible nonzero terms after the nonnegative
low-order sums have forced vanishing.

The independent checker assigns unrelated symbolic coefficients to every
monomial of two factors through degree four, with independent tails of
degrees 5, 7 and 20. It verifies the constant, degree-two and degree-four
formulas coefficient by coefficient. These symbolic checks supplement the
human vanishing argument; they do not replace its quantification over
arbitrary finite degrees or numbers of factors.

A deliberate countercontrol shows that high-degree cancellation does occur:
with `r²=x²+y²+z²`, take

`a=x²(1-2r²)`, `b_i=2x² x_i` for `x_i=x,y,z`.

Then `a²+(1-r²)Σ b_i²=x⁴`, although the factors have degrees four and
three and degree-eight terms cancel. The lowest-order proof still gives
the correct quadratic jet. An attempted global degree bound for module
factors would have been invalid; the frozen proof does not use one.

The strict positivity of the generator values at the expansion point is
material. A generator `g=x` at zero permits the nonsquare odd leading form
`x=g*1²`. A negative weight allows constants to cancel. Neither control
applies to the displayed `g(0)=1`.

## Independent check of the credited quartic premise

The multiplication-by-`t` matrix in `Q[t]/(t⁴-t+1)` was constructed
directly, and `det(xI+yT+zT²)` equals the nine displayed terms exactly.
The polynomial `t⁴-t+1` has no real roots: split the real line into
`t<=0`, `0<=t<=1`, and `t>=1`, where its value is positive in each
case. It is irreducible modulo two; modulo three it is the product of
the distinct linear factor `t+1` and irreducible cubic `t³-t²+t+1`.
The usual good-prime factorization-cycle argument supplies a four-cycle
and a three-cycle. The group has order 12 or 24; an index-two subgroup
of `S_4` is `A_4` and has no four-cycle, so the group is `S_4`.

For distinct roots `a,b`, the line pair has the explicit intersection
`P_ab=[ab:-(a+b):1]`. For a conjugate pair these coordinates are real.
If `f=Σq_j²` for rational quadratic forms, evaluation at that real zero
forces every `q_j(P_ab)=0`. Applying the verified `S_4` action to these
rational equations forces vanishing at all six pairs.

This audit independently computed the six-by-six quadratic evaluation
matrix with row

`[(ab)², -ab(a+b), ab, (a+b)², -(a+b), 1]`.

For roots treated as four algebraically independent variables, its
determinant is **minus the squared Vandermonde product**. Thus its
specialization at the distinct quartic roots is invertible, and every
quadratic coefficient vector must be zero. This gives a checkable alternative
to the frozen proof's restriction to three points on each line. Neither
argument reduces to rational sample points.

An inhomogeneous rational SOS cannot evade this: the highest homogeneous
parts of an unweighted real sum of squares cannot cancel, so all factors
have degree at most two. Zero constant and degree-two components then
force constants and linear parts to vanish. The remaining homogeneous
quadratics were just excluded.

For the real SOS, conjugate root pairs give a squared complex modulus of
a quadratic. Independently, direct exact expansion of the displayed `U,V`
identity after clearing beta denominators gives zero modulo
`beta³-4 beta-1`. There is a negative root in `(-2,-1)`, and the sign
`-beta>0` yields two real squares. There is no unresolved algebraic premise.
The exact quartic, construction and formula were visually matched to the
publisher's [Scheiderer paper](https://ems.press/content/serial-article-files/32129),
Theorem 2.1 and Example 2.8, printed pp.1499–1502. That paper retains credit.

## Quantifier and normalization controls

The same moments have `q=1+x⁴`, with `L_m(q)=0` and
`q-1=(x²)²`. Therefore an all-separators interpretation is falsified by
an explicit rational separator. A claim about minimal algorithmic relaxation
degree also receives no evidence from this construction.

The publisher's [Powers paper](https://msp.org/pjm/2011/251-2/pjm-v251-n2-p08-s.pdf),
Theorem 7 on printed p.389, assumes rational generators and a ball polynomial
in the real module. Its conclusion includes an extra ball term with rational
square factors. Here `N=1` and that term is the existing generator, so its
multiplier can be combined with the original one. The actual theorem and
continuation were visually checked on pp.389–390. No general descent from
real to rational Archimedeanity is being inferred.

For rational `c>1`, `cp-1=(c-1)+cf` is strictly positive on the ball.
The theorem gives rational module membership at some finite degree, preserving
`L_m(cp)=0`. It does not bound the degree or coefficient size. The ray has
the following exact boundary:

| Rational scale | Membership of `cp-1` in the displayed ball module |
| --- | --- |
| `0<c<1` | Fails even over `R`, since its value at zero is negative |
| `c=1` | Holds over `R`, fails over `Q` by the jet obstruction |
| `c>1` | Holds over `Q` by Powers's strict-positivity theorem |

Also **`p` itself belongs to `Q_Q(g)`**, since `p>=1>0`. The failure
is specifically `p in 1+Q_Q(g)`. This clarification is useful when reporting
the result but requires no mathematical correction to the frozen proof,
which already disclaims a failure of every positivity certificate for `p`.
In fact `p in t+Q_Q(g)` for every rational `t<1`, again by strict positivity
of `p-t` on the ball.

Merely asking for rational coefficients in multiplier polynomials would
also change the target: `sigma_0=f,sigma_1=0` is already such a list, with
real SOS meaning. Rational square factors are the checked requirement.
A rational PSD Gram matrix would imply rational square factors by rational
diagonalization and expressing each positive rational diagonal as a sum of
rational squares; it is therefore excluded too.

## Independence, comparison and evidence

INITIAL_FINDINGS.md was hashed and sealed before reading the original
`independent_review` or any other family's conclusions. A second control
seal followed the completed independent checker. Only then were the frozen
review and algebra family's preserved sealed derivation read. Their math
conclusions agree; the algebra family's Sturm, Frobenius and exact group
controls are materially distinct checks. Its seal and the compared bodies
are pinned in COMPARISON_INPUT_BINDINGS.json and copied byte-for-byte under
comparison_inputs. The prior review's original-question verdict is not
adopted here as fresh source evidence.

The independent checker passed **66** exact controls, including all 18
frozen file hashes. The frozen verifier replay passed **2,059** assertions
and produced byte-identical output to frozen CHECKS.json. Both freshly
downloaded primary PDFs match the original source manifest. Native launch
receipts contain actual command arguments, working directory, executable,
interpreter and input hashes, stdout/stderr bytes, timestamps, child PIDs and
return codes. All ten observed direct children returned zero, were waited
and reaped, and were absent at the post-wait PID probe. No descendant-reaping
claim is made.

The runtime profile and native receipt pins are qualified: they are not a
hermetic closure of the OS, shared libraries or tool-internal dependencies.
The separate profile process is labeled as such and is not presented as
retroactive observation inside the earlier control process. See
RECEIPT_AUDIT.json and RUNTIME_PROFILE.json.

No original/live source was edited, no Git or provider write was performed,
and no external individual was contacted. No required repair or mathematical
gap remains within this family's remit. Source interpretation, historical
priority and publication authority remain separate.
