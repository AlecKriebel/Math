# Attempt 4 of 5: exact finite-dimensional countermodels to cancellation

3 October 2026. Mechanism: test whether the one-particle algebraic identities
alone force multiplication or mass independence. Estimated full-target
completion: 20%; exact finite results, no continuum transfer.

## A two-coordinate building block

Let H=R², χ=diag(1,0), and

    S = (1/sqrt(2)) [[1,1],[1,−1]],
    A = S diag(α⁴,β⁴) Sᵀ,        0<α<β.

All spaces and powers are finite-dimensional. The standardness/factoriality
conditions hold: A^s e₁ and A^(−s)e₁ are linearly independent for s=±1/4,
and similarly for e₂, since the off-diagonal entries of A^(2s) are nonzero.
The remaining complementary-space conditions are automatic here.

Writing T=A^(1/4), direct multiplication gives

    B = TχT^−1+T^−1χT−I = b diag(1,−1),
    b=(α²+β²)/(2αβ)>1,
    T^−1 diag(1,−1) T^−1 = (1/(αβ))diag(1,−1).

Since arcoth(b)=log((β+α)/(β−α)),

    M_− = c(α,β) diag(1,−1),
    c(α,β)=2/(αβ) log((β+α)/(β−α)).                          (4.1)

Adding λI to A replaces α,β by (α⁴+λ)^(1/4),(β⁴+λ)^(1/4).
Thus the formula displays mass-shift dependence explicitly. As λ→∞,

    β(λ)−α(λ) ~ (β⁴−α⁴)/(4λ^(3/4)),
    α(λ)β(λ) ~ sqrt(λ),
    c(λ) ~ (2/sqrt(λ)) log(8λ/(β⁴−α⁴)) →0.                (4.2)

For λ=0, c>0, so c is not constant. This is a proof of nonconstancy without
relying on decimal evaluations.

## Four coordinates with a non-multiplication block

Take the direct sum of the (α,β)=(1,2) and (3,4) structures, ordered as
(inside₁,inside₂,outside₁,outside₂). Then

    χ=diag(1,1,0,0),
    M_−=diag(log 3, (log 7)/6, −log 3, −(log 7)/6).

Now conjugate A by O=diag(S,I₂); O commutes with χ, so the complete one-particle
construction is covariant under O and remains standard. In the same fixed
four-coordinate position basis the new interior block is

    (1/2) [[c₁+c₂, c₁−c₂], [c₁−c₂, c₁+c₂]],
    c₁=log 3, c₂=(log 7)/6.

Its off-diagonal entry is strictly positive: 3⁶=729>7, so log3>log7/6.
A multiplication operator on this four-point measure space is diagonal, hence
this example is not one. The sign of the off-diagonal entry is certified by
the integer inequality, not floating-point roundoff.

## What this does and does not test

This exact standard one-particle structure shows that no proof using only
the abstract block formula, standardness, and positivity can assert universal
multiplication or scalar-shift independence. Specific continuum localization
properties would be indispensable.

It is NOT the Helmholtz operator on Rⁿ, a ball truncation, or a certified limit
of any field approximation. Even its large-λ behavior differs from physical
wedge behavior. It therefore does not answer either original question.
The accompanying script verifies B exactly for both rational blocks and
checks the closed formula and its derivative numerically at high precision as
supplementary replay tests.

