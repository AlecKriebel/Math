# Fractional coefficient savings for binary-adder cardinality contradictions

## Result and source scope

This note proves an explicit, unbounded separation for a fixed normalized Boolean Nullstellensatz convention. There is a family of width-at-most-five CNFs with linearly many variables and clauses, encoding the contradictory requirements

- every input bit is zero; and
- their binary-adder sum is half the number of inputs,

for which fractional total coefficient mass is logarithmic while every proof has linearly many monomial terms. Consequently every integer-coefficient proof has linear mass. The construction uses ordinary cardinality-adder encoding, but the separation is encoding-sensitive and the underlying contradiction is elementary.

**Conservative disposition:** a quantitative explicit-family result; the original qualitative request for *natural* examples with *great* savings is not declared fully resolved. In particular, no superpolynomial proof-size lower bound, encoding-independent separation, bit-complexity saving, historical priority, or human peer review is claimed. The source does not quantify either adjective. Whether this elementary cardinality family meets its intended standard remains a scope question.

The question occurs in Aaron Potechin's contribution, joint with Aaron Zhang, in OWR 15/2024, printed p. 927 [1]. The exact mass convention comes from their ICALP paper [2, Definitions 5–9 and Remark 10]. They already prove a constant-size separation in Appendix A; that example is credited and is not presented as a discovery. Binary-adder encodings of pseudo-Boolean/cardinality constraints are established prior work [3, Section 5.4]. The explicit mass estimate and elementary support argument below are proved in full; no claim is made to having found their first occurrence.

## 1. Precisely fixed proof system

Let `v_1,...,v_N` be Boolean variables and write `bar(v)=1-v`. A literal monomial is a product of distinct compatible literals, including the empty product. The axioms `A=0` used here are all literal monomials with coefficient exactly one, namely the violation indicators of CNF clauses. No axiom is rescaled.

A weakening is a nonzero literal monomial obtained by multiplying an axiom by a compatible literal monomial, with Boolean repetitions removed. Let `W(F)` be the finite set of distinct weakenings. A refutation is

\[
1=\sum_{W\in W(F)} c_W W
\tag{1}
\]

as functions on the Boolean cube, equivalently modulo the Boolean and twin-variable relations. Its mass is `sum_W |c_W|`, and its support size is the number of nonzero coefficients. Let `C_R(F)`, `C_Q(F)`, and `C_Z(F)` minimize this mass over real, rational, and integer coefficients respectively; let `S_R(F)` minimize support over real coefficients. Thus

\[
C_R\le C_Q\le C_Z,\qquad C_Z\ge S_R.
\tag{2}
\]

The second inequality concerns integer coefficients in the **literal-weakening representation**, not a different notion of integer coefficients after an arbitrary change of basis. Rational and real optima agree for this finite rational linear program, but only explicit rational upper bounds are needed below.

The measure does not charge the input-axiom descriptions or Boolean/twin manipulations, exactly as in [2]. We separately count the formula size and coefficient bit lengths. Indeed our principal certificate, after substituting `bar(v)=1-v`, is an ordinary polynomial identity and needs no Boolean correction terms.

Every unsatisfiable monomial-axiom system has an integer refutation: for each full Boolean assignment choose an axiom it violates, take the full-assignment indicator as a weakening of that axiom, and sum all the indicators. Thus `C_Z` in our examples is finite.

## 2. Main theorem

For every integer `d>=1`, put `m=2^d` and `r=m/2`. There is an explicitly defined CNF `F_d` with

\[
N_d=5m-2d-4\quad\hbox{variables},\qquad
M_d=37m-23d-35\quad\hbox{clauses},
\tag{3}
\]

all of width at most five, such that

\[
\begin{split}
C_Q(F_d)&\le 72d-102+106/m,\\
S_R(F_d)&\ge m/2+1,\\
C_Z(F_d)&\ge m/2+1.
\end{split}
\tag{4}
\]

In particular,

\[
\frac{C_Z(F_d)}{C_R(F_d)}
\ \ge\ \frac{m/2+1}{72d-102+106/m}
\ =\ \Omega(m/\log m)
\ =\ \Omega(N_d/\log N_d).
\tag{5}
\]

The same lower bound holds for `S_R/C_R`. The displayed denominator is an explicit upper bound, not a claim to the exact optimum. It is positive for every `d>=1`.

The certificate has constant axiom multipliers, degree at most five, `O(m)` nonzero terms, coefficients of absolute value at most three, and denominators dividing `m/2`. Its coefficient bit length is `O(m log m)`, not logarithmic. A standard explicit encoding also spends `O(m log m)` bits on variable indices; equation (3) counts variables and clauses.

### 2.1 Completely specified circuit and CNF

Start with `m` input variables, arranged as one-bit words. At level `s=1,...,d`, pair the words from level `s-1` and add each pair. Each input word at this level has `s` bits and each output word has `s+1` bits. There are `m/2^s` additions at level `s`.

For an addition of `a=(a_0,...,a_{s-1})` and `b=(b_0,...,b_{s-1})`, create fresh sum bits `z_0,...,z_{s-1}` and fresh carries `c_1,...,c_s`; set `c_0=0` as a constant, not as a variable or additional axiom. Its output is `(z_0,...,z_{s-1},c_s)`.

- Position zero is a half-adder on `(a_0,b_0,z_0,c_1)` satisfying `a_0+b_0=z_0+2c_1`.
- Position `j>=1` is a full-adder on `(a_j,b_j,c_j,z_j,c_{j+1})` satisfying `a_j+b_j+c_j=z_j+2c_{j+1}`.

For **each** Boolean tuple violating a gate equality, include its full tuple indicator as a monomial axiom. Thus each half-adder gives 12 width-four clauses and each full-adder 24 width-five clauses. These clauses specify the gate truth table exactly, not just an implication or an arithmetic equation with an unnormalized coefficient.

Finally include the `m` input axioms `x_i=0`. If the root word is `y_0,...,y_d`, include `d+1` unit axioms fixing it to the binary expansion of `r=2^{d-1}`: use `1-y_{d-1}=0` and `y_j=0` for `j!=d-1`. This completes the definition of `F_d`.

For every Boolean input, all gates have a unique correct assignment, and the root word represents the number of true inputs. Hence exactly the weight-`r` inputs extend to assignments satisfying all gate and root axioms. Adding all the zero-input axioms makes the system unsatisfiable.

The total number of gates is

\[
G_d=\sum_{s=1}^d (m/2^s)s=2m-d-2.
\tag{6}
\]

There are `m-1` half-adders and `m-d-1` full-adders. Each gate creates exactly two fresh variables, giving `m+2G_d=N_d`. Counting the gate clauses, input units, and root units gives

\[
12(m-1)+24(m-d-1)+m+(d+1)=M_d.
\]

### 2.2 Local residuals are normalized-axiom combinations

For a gate, let `u` denote its four or five distinct variables, and define its affine residual

\[
R_H(a,b,z,t)=a+b-z-2t,\qquad
R_F(a,b,c,z,t)=a+b+c-z-2t.
\tag{7}
\]

For a Boolean tuple `alpha`, write `delta_alpha(u)` for its full literal indicator. Multilinear interpolation gives the exact polynomial identity

\[
R(u)=\sum_{\alpha\in\{0,1\}^{|u|}} R(\alpha)\delta_\alpha(u)
     =\sum_{\alpha:R(\alpha)\ne0}R(\alpha)\delta_\alpha(u).
\tag{8}
\]

Every monomial on the right is one of the gate axioms. The equality holds as an ordinary polynomial after twin substitution: both sides are multilinear and agree at every cube vertex.

Enumerating only the 16 or 32 local tuples gives

\[
\sum_\alpha|R_H(\alpha)|=18,\qquad
\sum_\alpha|R_F(\alpha)|=36.
\tag{9}
\]

For transparency, the half-adder residual multiplicities at values `-3,-2,-1,0,1,2` are `1,3,4,4,3,1`. The full-adder multiplicities at `-3,-2,-1,0,1,2,3` are `1,4,7,8,7,4,1`. These finite facts are also checked in the executable verifier.

### 2.3 Telescoping and certificate mass

For one addition, multiply the position-`j` residual by `2^j`. The internal carries cancel exactly, so

\[
\operatorname{val}(a)+\operatorname{val}(b)-\operatorname{val}(z)
=\sum_{j=0}^{s-1}2^jR_j.
\tag{10}
\]

Sum equation (10) over all nodes. Every nonroot output word is an input word at its parent, hence cancels. If `Z=sum_{j=0}^d 2^j y_j`, then

\[
\sum_{i=1}^m x_i-Z=\sum_g w_gR_g,
\qquad w_g=2^{\text{position}(g)}.
\tag{11}
\]

Write the root axioms as `B_j=y_j` for target bit zero and `B_j=1-y_j` for target bit one, and let `epsilon_j=1` or `-1` respectively. Then

\[
Z-r=\sum_{j=0}^d 2^j\epsilon_j B_j.
\tag{12}
\]

Combining (11) and (12) yields the explicit normalized certificate

\[
1=\frac1r\sum_i x_i
 -\frac1r\sum_g w_g\sum_{\alpha:R_g(\alpha)\ne0}
       R_g(\alpha)\delta_{g,\alpha}
 -\frac1r\sum_{j=0}^d2^j\epsilon_j B_j.
\tag{13}
\]

All terms are original axioms. There are no extension rules invoked inside the proof: gate variables and gate clauses belong to the input formula `F_d` from the outset.

One level-`s` addition has residual mass

\[
18+36\sum_{j=1}^{s-1}2^j=36\,2^s-54.
\]

Consequently the total unnormalized gate mass is

\[
\sum_{s=1}^d(m/2^s)(36\,2^s-54)
 =36md-54m+54.
\tag{14}
\]

The input mass is `m`; the root mass is `sum_{j=0}^d2^j=2m-1`. Divide their sum by `r=m/2` to obtain the first bound in (4). For each gate, `|R_g(alpha)|<=3` and `w_g<=2^{d-1}=r`; root coefficients have magnitude at most two. All coefficient claims in the theorem follow. Equation (13) is a constructive proof, independent of numerical optimization.

### 2.4 All-degree, all-coefficient support lower bound

Consider any refutation (1), with arbitrary degree and real coefficients. Assign each nonzero weakening term to any one original axiom that it weakens. Let `I` consist of the input indices assigned to input axioms among those terms.

If `|I|<=m-r`, choose a set `S` of exactly `r` input indices disjoint from `I`. Set precisely the inputs in `S` to one and extend uniquely through the circuit. All gate and root axioms vanish on this assignment. Every used weakening assigned to an input axiom also vanishes, because its chosen `x_i` has `i in I` and is zero. Thus the right side of (1) is zero, contradicting the left side.

Therefore `|I|>=m-r+1`. There must be at least that many distinct nonzero terms. This argument permits a weakening to be eligible for several axioms: choosing any one source for each term is sufficient. It also covers arbitrary multipliers after expansion into literal weakenings. The integer mass bound then follows from each nonzero integer having absolute value at least one.

This is a hitting-set argument, not a degree lower bound. It proves neither a superlinear nor a superpolynomial support lower bound.

## 3. Precisely limited Sherali–Adams extension

One standard static equality-axiom formulation augments normalized weakenings by arbitrary nonnegative literal monomials:

\[
-1=\sum_W c_W W+\sum_M b_M M,\qquad b_M\ge0,
\tag{15}
\]

with mass `sum |c_W|+sum b_M`. This is the formulation called “resolution-like” in the older arXiv full version [4, Definition 16]; the ICALP discussion relates its discussion to Sherali–Adams. We state the convention explicitly rather than claiming every variant has identical costs.

Negating (13) and taking no remainder gives the same fractional upper bound in (15). The support argument survives: on the valid weight-`r` assignment avoiding all used input indices, the axiom part is zero and the remainder is nonnegative, so (15) would say `-1>=0`. Therefore at least `m-r+1` input-axiom terms are needed, and integer mass is at least that amount.

Thus the quantitative separation also holds for precisely (15). The Nullstellensatz theorem alone already addresses one of the source's two named systems; no unverified equivalence of proof-system variants is needed.

## 4. What does and does not follow

1. The theorem gives an unbounded `Omega(N/log N)` mass and support-versus-mass gap on a linearly sized, bounded-width adder-cardinality family. All normalized input coefficients are one. There is no exponential truth-table padding in this final family.
2. It does not give a bit-length saving: the displayed certificate still has linearly many written terms, each with logarithmic-bit rational data.
3. The lower bound is linear in input size; it does not exhibit the difficult, superpolynomially large proofs one might intend by the source's informal wording.
4. The circuit encoding is part of the theorem. Replacing it by a single arithmetic equation, different clauses, extension rules, or a preprocessing-derived contradiction changes the input/proof measure and requires a new analysis.
5. Cardinality encodings and the proof ingredients are classical. A bounded literature search did not locate this exact estimate, which is not evidence of first priority.
6. The original qualitative “natural/greatly” scope remains explicitly qualified. The conservative recommended campaign disposition is an independently reviewable partial result, with no new paper or DOI claimed here.

## References

[1] Aaron Potechin, joint work with Aaron Zhang, “Bounds on the Total Coefficient Size of Nullstellensatz Proofs of the Pigeonhole Principle,” contribution in *Proof Complexity and Beyond*, Oberwolfach Reports 15/2024, printed pp. 926–927. DOI: https://doi.org/10.4171/OWR/2024/15 . Official report: https://publications.mfo.de/bitstream/handle/mfo/4161/OWR_2024_15.pdf?sequence=4 .

[2] Aaron Potechin and Aaron Zhang, *Bounds on the Total Coefficient Size of Nullstellensatz Proofs of the Pigeonhole Principle*, ICALP 2024, LIPIcs 297, article 117. Definitions 5–9, Remark 10, Proposition 12, Appendix A. https://doi.org/10.4230/LIPIcs.ICALP.2024.117 .

[3] Niklas Eén and Niklas Sörensson, *Translating Pseudo-Boolean Constraints into SAT*, Journal on Satisfiability, Boolean Modeling and Computation 2 (2006), Section 5.4. https://doi.org/10.3233/SAT190014 ; author-hosted text: https://minisat.se/downloads/MiniSat%2B.pdf . This is credit for the established encoding method, not an attribution of the bound in (4).

[4] Aaron Potechin and Aaron Zhang, *Bounds on the Total Coefficient Size of Nullstellensatz Proofs of the Pigeonhole Principle and the Ordering Principle*, arXiv:2205.03577v1 (2022), Definition 16. https://arxiv.org/abs/2205.03577 . The 2022 version uses terminology differing from the 2024 conference discussion.
