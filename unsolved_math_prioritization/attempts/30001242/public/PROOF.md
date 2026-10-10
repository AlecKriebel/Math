# No ring-independent generic bound for ordinary ideal membership

## Result and attribution

The uniform assertion in catalogue item **30001242 / OWR-3472-013** is false.
It already fails for two generic linear generators in standard-graded
two-dimensional integral domains over one fixed infinite field. The negative
answer is classical and is explicitly stated in the cited 2009 report,
printed p. 1212, and in the introduction to Brenner–Fischbacher-Weitz,
*Generic bounds for Frobenius closure and tight closure*, arXiv:0810.4518v3,
p. 1. This note supplies a complete elementary realization of their
parameter/hypersurface obstruction. It makes no discovery or priority claim.

The question concerns ordinary membership, not tight closure or Frobenius
closure. The catalogue's ring-independent quantifier is essential: a bound
allowed to depend on the ring is a different assertion.

## 1. A family of domains with fixed dimension and generator degrees

Fix any infinite field k; its characteristic may be zero or positive. For
each integer N >= 2 put

    S = k[x,y,z],    F_N = x^N - y^(N-1) z,    R_N = S/(F_N),

with all three variables of degree one. The ring is standard graded and
R_N,0 = k.

The polynomial F_N is primitive as an element of k[x,y][z], because its two
nonzero coefficients x^N and -y^(N-1) have no common nonunit factor. Over
the fraction field k(x,y) it has degree one in z and is irreducible. Gauss's
lemma therefore makes it irreducible in k[x,y,z]. A polynomial ring over a
field is a unique factorization domain, so F_N is prime and R_N is a domain.
This argument remains valid after any extension of k.

Viewed instead as a polynomial in x, F_N is monic of degree N. Division by
this monic polynomial shows that R_N is free of rank N over k[y,z], with
basis 1,x,...,x^(N-1). Thus k[y,z] embeds in R_N and the extension is finite
and integral. Integral extensions preserve Krull dimension, giving

    dim R_N = 2.

There are no degree-one relations because N >= 2. Hence (R_N)_1 has basis
x,y,z, and ordered pairs of linear forms are parametrized by affine 6-space.
For the entire family the fixed problem data are d = n = 2 and
(a_1,a_2) = (1,1). Only the defining degree of the ring varies.

## 2. The generic quotient, with an explicit nonempty open set

Write the two linear forms as

    l_1 = a x + b y + c z,    l_2 = d x + e y + f z,

and define their signed-minor vector

    v = (b f-c e, c d-a f, a e-b d).

The two coefficient rows annihilate v. Let

    U_N = { (a,b,c,d,e,f) : F_N(v) != 0 }.

This is Zariski open. It is nonempty over every field: the pair (y,z)
has v = (1,0,0) and F_N(v) = 1. Since affine 6-space is irreducible, U_N is
dense and contains the generic point.

For a pair in U_N, v is nonzero and the two coefficient rows have rank two.
The common kernel is the line k v. The graded map

    S -> k[t],    x -> v_x t, y -> v_y t, z -> v_z t,

is onto because at least one v-coordinate is nonzero. Its kernel is
(l_1,l_2): an invertible linear change of coordinates identifies this with
the quotient of a polynomial ring by two independent coordinate variables.
Homogeneity gives F_N(v t) = F_N(v) t^N. Therefore

    R_N/(l_1,l_2) = S/(F_N,l_1,l_2) ~= k[t]/(t^N)          (1)

as graded k-algebras. The same argument works over the function field of
the parameter space. It also works after every field extension, so there is
no specialization or rational-point ambiguity in the generic assertion.

The quotient (1) has basis 1,t,...,t^(N-1), with these elements in distinct
degrees. Consequently its degree-m Hilbert function is

    1, if 0 <= m < N;
    0, if m >= N.

The generic ideal (l_1,l_2) is R_N,+-primary, since its quotient is the
finite-dimensional graded local ring k[t]/(t^N). Thus these are genuine
parameter ideals, not examples where the number of generators is too
small to make a finite cutoff possible. Their least membership cutoff is
exactly N.

## 3. Even nongeneric pairs cannot improve the lower bound

For any two linear forms, let L be the ideal they generate in S. When
0 <= m < N, the homogeneous ideal (F_N) has no component in degree m.
It follows that

    (S/(L,F_N))_m = (S/L)_m.

The quotient S/L is a polynomial ring in 3-r variables, where r <= 2 is
the rank of the coefficient rows. It has at least one variable, so its
degree-m component is nonzero. Thus

    (R_N)_m is not contained in (l_1,l_2) for every m < N,   (2)

for every ordered pair, including dependent pairs. In particular a different
choice of generic open set cannot evade the obstruction.

## 4. Contradiction to the proposed uniform bound

Suppose a finite nonnegative bound B(d;a_1,...,a_n), independent of R,
existed as in the question. Set M = B(2;1,1), and choose
N > max(M,1). Apply the assertion to R_N. Equation (2) says that
(R_N)_M is not contained in the generated ideal for any pair of linear
forms. This contradicts the proposed generic containment.

Therefore there is no such uniform generic ordinary-membership bound.
The argument works with a fixed k, fixed dimension, fixed number of
generators, fixed generator degrees, and even fixed embedding dimension 3.
It requires neither nonreduced rings nor changing the characteristic.

## 5. Scope and the actual source distinction

The standard grading implies that if an ideal contains R_m, it contains
every R_q for q >= m: multiplication R_1 R_q = R_(q+1) propagates the
containment. Thus the single-degree and tail-cutoff formulations agree.

This result does not assert that a cutoff fails for a fixed ring and a
generic parameter ideal; (1) gives a finite cutoff in every example.
It does not settle the Fröberg conjecture, a plus-closure question, or any
variant with extra ring invariants fixed. Normality is not claimed for
R_N. The ordinary-membership obstruction was already known when the
2009 question-like introductory sentence was written.

The companion paper's Theorem 3.4(c) permits dependence on the ring's
a-invariant for ordinary membership. Its closure results have different
conclusions and hypotheses; none is used in the proof above. For this
reason an ordinary-membership counterexample does not contradict them.

## References

- H. Fischbacher-Weitz, joint work with H. Brenner, “Generic bounds for
  tight closure,” in *Kommutative Algebra*, Oberwolfach Report 22/2009,
  pp. 1211–1214, especially p. 1212. DOI:
  https://doi.org/10.4171/OWR/2009/22 .
- H. Brenner and H. Fischbacher-Weitz, *Generic bounds for Frobenius closure
  and tight closure*, https://arxiv.org/abs/0810.4518v3 , introduction
  p. 1 and Theorem 3.4(c). Published in *American Journal of Mathematics*
  133 (2011), no. 4, 889–912, https://doi.org/10.1353/ajm.2011.0032 .
  The full-text version inspected here is arXiv v3, not the publisher PDF.
