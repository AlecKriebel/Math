# Checkable priority comparison, not a new proof gate

This note records deductions from actual prior equations, to measure overlap. It does not label a theorem previously published merely because it is derivable.

## Full multiset approximation already implicit in prior geometry

Let n=3g-3 and k be at most k_g=(3/5)log(2n). DL Theorems 3.2 and 1.4 identify the area law. DL Section 4 is literal conditioning on a one vertex graph with at most O(log g) loops, whose probability tends to one by Theorem 2.7. Thus the replacement by the exact conditional law is already a total variation replacement, even though Theorem 4.1 is phrased with expectations of bounded functions.

The positive expansion in the proof of DL Lemma 6.4 (printed p. 5117), followed by its height sum and simplex integral, gives the latent composition weight

    D_(g,k) ctilde_(g,k)(j_1,...,j_k) / k! × product_i ζ(2j_i)/(2j_i),

and the conditional area vector is Dirichlet(2j_1,...,2j_k). Here

    D_(g,k)=(6g-5-2k)! 2^(2k-3)/[(g-k)!(3g-3-k)! 3^(g-k)].

The uniform ctilde=1+o(1) over all compositions in this range is exactly DL (6.1)-(6.2). The other prefactor is uniformly constant in k by DL (6.7), or directly from

    D_(g,k+1)/D_(g,k)
      =12(g-k)(3g-3-k)/[(6g-5-2k)(6g-6-2k)]
      =1+O((k+1)/g).

Consequently the latent density ratio to the candidate's conditional marked assembly is 1+o(1), uniformly on the latent space. Normalization changes that ratio by 1+o(1) as well. Total variation is at most the two discarded tail probabilities plus the uniform density error. The ideal composition law, including ζ(2j)/(2j), is already the weighted permutation cycle law in DGZZ Lemma 3.6 and (3.20)-(3.23) with θ_j=ζ(2j)/2. Its logarithmic K tail follows from DGZZ Theorem 3.7. The real geometric tail is controlled by DL Theorem 2.7, or quantitatively by DGZZ Theorem 1.12 and low k Theorem 5.2.

This is a short consequence of old uniform inputs. No new geometric estimate is needed for candidate Theorem A. Neither paper explicitly states the candidate's full total variation approximation to the marked assembly.

## A checked older theorem covers the unmarked example window

Nikeghbali-Storm-Zeindler, arXiv:1302.5938 (submitted 24 February 2013), Theorem 3.3, treats the generalized weighted permutation generating function exp(w g(z)+sum v_l L_D_l(z)). Its analytic class includes

    g(z)=sum_j ζ(2j) z^j/(2j)
        =-(1/2)log(1-z)+(1/2)sum_(m>=2) -log(1-z/m^2).

The analytic remainder is holomorphic through |z|<4, so r=1 and θ=1/2. For moving index sets of maximum d_n, its explicit condition is

    C log n - n/d_n -> -infinity for every real C.

For finite intervals of indices [a q_n,b q_n], where q_n is proportional to sqrt(n), that condition holds. The theorem then gives the joint Poisson characteristic function with means sum_(j in interval)ζ(2j)/(2j), which tend to (1/2)log(b/a). It is therefore an older direct tool for the unmarked composition example. It does not itself treat the surface ensemble or Gamma marks. Its stated condition does not cover every q_n=o(n), for example q_n=n/sqrt(log n). The candidate's elementary factorial moment proof avoids that specific theorem's restriction. This does not prove that every other older assembly theorem has the same restriction.

Nikeghbali-Zeindler, arXiv:1105.2315, Theorem 3.1 and Corollary 3.1.1 only use a fixed finite number b of cycle sizes. Those statements alone cannot be applied with b moving without further uniform estimates.

## Two tempting identifications are invalid

1. A discrete normalized composition {j_i/n} and a Dirichlet marked area multiset are not close in total variation. For K>=2 the former lies in a finite set of rational grids and the latter has a simplex density. Their shared weak Poisson-Dirichlet limit does not remove that singularity. A marking argument is required.

2. A fixed microscopic point process limit and its intensity's large x asymptotics do not control windows escaping to infinity. For an elementary non-implication witness, start with any random normalized partition having the asserted endpoint limits, multiply all parts by 1-m s_g, and append m parts of size s_g, with fixed m and s_g->0, g s_g->infinity. The added mass vanishes; the new microscopic points escape every compact; but the mesoscopic window containing 1 acquires m extra atoms. This witness only concerns the two endpoint weak limits, not the entire collection of exact DL/DGZZ inputs or their refined K generating functions.

Thus the old endpoint theorems are not themselves a solution of OWR Problem 2. The extraction of uniform latent comparison and the all-rate Gamma/moment transfer is the candidate's potential contribution.
