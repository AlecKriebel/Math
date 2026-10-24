# Central extension route: exact lift formula and remaining realization gap

UTC:2026-10-24T23:23:43Z. Research status: blocked at a genuinely new central
word-cocycle construction, not a counterexample. Discovery estimate2%.

## Model attempted

Let `H` be an infinite profinite group and `pi_i:E_i -> H` continuous surjective
homomorphisms of profinite groups with finite central kernels `K_i`. Take their
full fiber product over `H`.
To avoid an immediate large image under projection, choose a fixed word `w`
that is a law on `H`. Every word value in the fiber product then belongs to
the central kernel `product_i K_i` and consequently has a singleton conjugacy
class. This avoids the branch/FC obstruction, but **does not** establish a
small image or construct any of the required extensions.

## Lift variation cannot implement rare activation

Let `r_j` be the exponent sum of variable `j` in `w`. Since each kernel is
central, for arbitrary lifts `g_j` and kernel elements `k_j` one has exactly

    w(g_1 k_1,...,g_k k_k)=w(g_1,...,g_k) product_j k_j^(r_j).

Put `d=gcd(r_1,...,r_k)`, with `d=0` when every exponent sum is zero and with
`K^0={1}`. Each `K_i` is abelian; Bezout's identity gives

    product_j K_i^(r_j)=K_i^d.

Thus the restricted image over **every** quotient-input tuple is a coset of
the same finite subgroup `K_i^d`. The activation set `|S_i(h)|>1` is either
empty or all of `H^k`. It cannot be a small clopen annulus. If infinitely many
`K_i^d` are nontrivial, any one quotient-input tuple gives a Cartesian Cantor
family. A small global image forces `product_i K_i^d` to be finite.

For a commutator word (`r_j=0` for every variable), all lift images are
singletons automatically. However, it is incorrect to deduce that the word
value is determined by the **word value in H**. It is determined by the
whole input tuple in `H^k`. For instance, a central extension of an abelian
group can have a nontrivial commutator pairing even though every quotient
commutator is1. In our model this leaves a continuous central-valued map

    c_w:H^k -> product_i K_i

which must be realized by compatible genuine finite central extensions.
Designing an arbitrary continuous map with countably infinite image is not
enough: it must satisfy the group-cocycle constraints of one fixed word.

## Most concrete residual candidate

Take `H` metabelian, and a central extension `E` of it. Then `E''` is central,
so the fixed nontrivial word

    w(x,y)=[[x,y],[x,y]^x]

is central-valued on `E` and is a law on `H`. This would put a counterexample
in a group of derived length at most3 rather than in the already covered
metabelian class. The word is not being claimed to have any special unknown
status by itself; its full literature audit would be required before a
solution claim. No finite or inverse-system family with the required
countably infinite values has been found.

Attempts to realize its cocycle independently in separate finite coordinates
restore Cartesian independence and hence continuum. Finite-controller
coupling also fails by FIBER_PRODUCT_OBSTRUCTION.md. Taking `H` nilpotent of
bounded class makes the central extension nilpotent of bounded class, already
covered by Detomi--Klopsch--Shumyatsky. The recent metabelian result is not a
license to assert the same conclusion for all central-by-metabelian groups.

The exact gap is to construct compatible finite central word cocycles whose
joint image is compact, infinite, and smaller than continuum, or prove that
the cocycle identities rule this out. Either assertion currently transfers
the main mathematical difficulty; this route is marked blocked unless a
materially new cocycle mechanism appears.

## Why isolated-value recursion did not supply that mechanism

An isolated word value does not force a finite image. For example, for an odd
prime `p`, let `G=Z_p semidirect C4`, with a generator of `C4` acting by
inversion on `Z_p`. Its square values are exactly the disjoint union

    (Z_p x {1}) union {(0,t^2)}.

Indeed `(a,t^k)^2=((1+(-1)^k)a,t^(2k))`. The second value is isolated in the
image, whereas the first part already has continuum cardinality. In finite
versions with `Z/p^n`, the square-image size is `p^n+1`. Trying to turn this
into a countable comb by increasing cyclic depth inevitably retains the
infinite compact subgroup of square values. This metabelian example is
already in a known positive class; it is only a falsifier of an invalid
isolated-value shortcut, not a proposed counterexample to21.122.
