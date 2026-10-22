# Independent mathematical argument for PR1297

This argument verifies a counterexample to the unrestricted degree-1/2
factorization assertion. It does not supply an absolutely irreducible
Yetter–Drinfeld module and does not resolve the conjecture in that setting.

## Construction and imported theorem

Work over the complex numbers. Fix a primitive fifth root ζ and put

\[
 Q=\begin{pmatrix}ζ&ζ^{-1}&1\\1&ζ&ζ^{-1}\\1&1&ζ\end{pmatrix},
 \qquad c(x_i\otimes x_j)=q_{ij}x_j\otimes x_i.
\]

The braiding is invertible. Both sides of the braid equation applied to a
basis triple have the same reversed triple and scalar
\(q_{ij}q_{ik}q_{jk}\). Thus no unstated constraint on a diagonal braiding is
needed here.

Let \(G=(\mathbb Z/5)^3\), with basis \(g_1,g_2,g_3\). Set
\(\chi_j(g_i)=q_{ij}\), act by \(g x_j=\chi_j(g)x_j\), and give \(x_j\)
homogeneous degree \(g_j\). All character values have fifth power one, so
the characters exist. Conjugation is trivial in this group and every action
preserves degree; hence the Yetter–Drinfeld compatibility holds. Its
categorical braiding is exactly the displayed one. The support generates G.

For each i, the line \(\mathbb Cx_i\) is stable under both action and
coaction. These are three nonzero proper subobjects with direct sum V.
Consequently this module fails simplicity over the original field itself;
it necessarily fails absolute simplicity. The connected Cartan diagram
expresses interactions among the summands and cannot eliminate them.

The explicit imported result is Andruskiewitsch–Schneider, *Pointed Hopf
algebras*, §6.1, Theorem 6.13, in the [2001 preprint](https://arxiv.org/pdf/math/0110136v1)
and [published 2002 chapter](https://library.slmath.org/books/Book43/files/andrus.pdf).
Its relevant conditions are an algebraically closed field of characteristic
zero, a root parameter of order N>2, diagonal entries equal to that
parameter, adjacent pair products its inverse, and all other pair products
one. They hold here with n=3 and N=5. In particular, restrictions on prime
divisors appearing in later pointed-Hopf classification theorems are not
conditions of this PBW theorem. The theorem supplies a basis of monomials
in the six interval root vectors with each exponent in {0,1,2,3,4}.
This foundational PBW theorem is inspected and imported, not reproved by
the finite checker.

In the source's endpoint convention the root vector \(e_{i,j}\) has degree
\(j-i\); its inclusive interval is [i,j−1]. The six ordinary degrees are
1,1,1,2,2,3. For an interval of length h, the self-braiding exponent is
h−(h−1)=1 modulo 5, so every root has order five. The same root set and
explicit PBW description occur in [Andruskiewitsch–Angiono, v1, §§4.1.1–4.1.4](https://arxiv.org/pdf/1707.08387v1).

Summing basis monomials in the ordinary grading therefore gives

\[
 H(t)=(5)_t^3(5)_{t^2}^{,2}(5)_{t^3},
 \quad H(1)=5^6=15625,\quad\deg H=4(3+4+3)=40.
\]

No regrading has made the degree-three root vector a degree-one generator.
In particular H begins 1+3t+8t²+17t³+33t⁴.

## Universal obstruction

Suppose H were a finite product of \((a)_t\) and \((b)_{t^2}\) with
positive integer lengths. Let η have order fifteen. Because η³ has order
five, the factor \((5)_{t^3}\) vanishes at η, so H(η)=0. Some factor of a
hypothetical product must vanish at η. Since both η and η² have order
fifteen, the length of that factor is divisible by fifteen.

Now let ω have order three. The same length is divisible by three; both ω
and ω² have order three, so that same permitted factor vanishes at ω.
Hence any such product vanishing at η must vanish at ω. But direct
reduction using \(1+ω+ω^2=0\) gives

\[
 H(ω)=(-ω^2)^3(-ω)^2\,5=-5ω^2=5(1+ω)\ne0.
\]

This contradiction excludes **every** finite product, with no bound on the
number or lengths of factors. Length-one factors are units; an empty
product cannot vanish. A length-zero factor, if artificially permitted,
would make the whole polynomial zero and cannot produce H. There is no
division or cancellation in the proposed expression.

Equivalently, exact integer polynomial division gives

\[
 H=\Phi_5^6\Phi_{10}^{,2}\Phi_{15},\qquad
 H\bmod\Phi_3=5+5t.
\]

Every degree-one or degree-two quantum integer containing Φ15 contains
Φ3. H has the former and lacks the latter. The example remains a product
of quantum integers if grading step three is allowed; a claim allowing
quotients would require a different argument.

There is a separate exhaustive arithmetic reduction: evaluating any
hypothetical product at one forces every nontrivial length to be a power
of five. Its degree at most forty leaves only \((5)_t\), \((5)_{t^2}\), and
\((25)_t\). If their multiplicities are a,b,c, then
\(a+b+2c=6\) and \(4a+8b+24c=40\). Their only nonnegative solutions are
(2,4,0) and (4,0,1). The corresponding coefficients of t are respectively
two and five, whereas H has coefficient three. Unit factors do not affect
this reduction.

## Inspection of the essential PBW proof

The source proof first obtains a spanning set through root-vector
commutation and nilpotence. It then splits off the last simple generator,
forms the coinvariant braided algebra R_n, and uses its n primitive
interval root vectors of degrees 1 through n. Triangular coproducts and
nonvanishing quantum binomial coefficients below N give at least N^n
independent monomials. The spanning bound supplies the opposite
inequality. This yields the induction, hence six independent bounded
exponents when n=3. For this specialization the field is characteristic
zero and N=5, so the needed quantum binomial coefficients do not vanish.

Two printed slips in both retained versions deserve explicit correction;
neither changes the theorem used here. On printed p.53 the antipode in the
display computing the action of \(e_{i,p}\) must be \(S(e_{i,p})\), not
\(S(e_{i,n+1})\). This follows immediately by applying the coproduct of
\(e_{i,p}\) to the adjoint-action formula; the last line is its counit
identity. Also Z_n denotes the bosonization, so its dimension carries a
factor |Γ|. Keeping the same Γ at successive ranks, the correct bounds
are

\[
 \dim Z_n\le |Γ|N^{n(n+1)/2},\qquad
 \dim Z_{n-1}=|Γ|N^{n(n-1)/2}.
\]

Their quotient is the stated bound \(\dim R_n\le N^n\). After the lower
bound, dividing back by |Γ| gives the theorem's dimension for B(V_n).
Thus the omitted common group factor is repairable explicitly, rather
than an assumption of the present argument.

## What the independent finite checks establish

The accompanying standard-library checker constructs the A3 root orbit
by reflections, checks all 46,875 character multiplicativity identities,
and verifies the proper coordinate summands. It multiplies the Hilbert
factors and independently counts all 15,625 exponent tuples. It checks
the complete cyclotomic valuations by exact division. Separately, it
builds the quantum symmetrizer matrices directly from the braiding and
computes their ranks in Q(ζ5) in degrees two, three, and four: 8,17,33.
Fifteen controls exercise changed Cartan data, grading changes, allowed
factor foils, quotient/step-three scope changes, and a simple quantum-line
positive foil. All computations pass identically in normal, -O, and -OO
modes. They supplement the universal argument and imported PBW theorem;
they do not prove all degrees of the Nichols presentation or interpret
the historical conjecture automatically.
