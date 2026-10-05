# Why the factored-polynomial check is exact

This justifies `verify_factored_witness.py`. It is not a construction of a counterexample.

Let f_1,...,f_k be nonconstant monic, squarefree, pairwise coprime polynomials in Q[z], and let a_i,b_i be positive integers. Put

P = product_i f_i^{a_i},  Q = product_i f_i^{b_i},  S = product_i f_i.

All roots of the factors are distinct across factors. Positivity of every exponent gives Z(P)=Z(Q)=Z(S), and monicity of the factors gives monicity of P and Q.

By the product rule,

P' = (product_i f_i^{a_i-1}) N_P,

where N_P = sum_i a_i f_i' (S/f_i).

The divisions S/f_i are exact in Q[z]. Consequently the set of complex zeros of P' is the zero set of

N_P product_{i:a_i>1} f_i.

The monic squarefree part of this polynomial uniquely encodes that zero set over C. The same formula with b_i encodes Z(Q'). Comparing those two squarefree parts is therefore equivalent to comparing the complete derivative zero sets, including zeros of P or Q that remain zeros after differentiation. This is why simply comparing the reduced logarithmic-derivative numerators is insufficient when some exponents equal 1.

Finally, P^m=Q^n for positive integers m,n holds exactly when m a_i=n b_i for every i. Necessity follows by comparing the multiplicity of any complex root of f_i; sufficiency follows from the factorizations. Positive integer vectors are proportional over Q exactly when a_1 b_i=b_1 a_i for every i. This is the code's proportionality test. No numerical root calculation or approximate equality is used.

The code thus certifies a counterexample precisely when the derivative zero sets agree and these exponent vectors are not proportional, assuming its explicitly checked factor input conditions. Its included tests check ordinary cases and invalid inputs. Since no counterexample factor list has been certified in this reconstruction, the test result deliberately records `known_counterexample_verified: false`.

## Exact-input boundary

The independent audit found that converting directly to SymPy's QQ domain can rationalize approximate Float coefficients. The revised input guard first checks that every supplied polynomial coefficient is an exact SymPy Rational (integers included), then converts to QQ. Thus decimal Float inputs are rejected rather than silently changed. Callers should use explicit exact rational values. If a caller has already converted an approximation to a rational before passing it to the verifier, this verifier cannot recover that history; it certifies only the exact input it receives.

Independent controls compare the returned derivative radicals to expanded derivatives reduced by a gcd, and compare power equality to normalized irreducible-factor multiplicities. Both implementations use SymPy, so this is algorithmic cross-checking rather than a second computer-algebra system. A successful counterexample fixture is still absent.
