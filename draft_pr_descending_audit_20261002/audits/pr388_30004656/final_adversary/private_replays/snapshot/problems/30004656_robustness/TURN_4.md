# Turn 4: a log-free lower bound for independent, bias-free ReLU units

Fourth substantive turn. This is a restricted architecture theorem, not the full source conjecture. Inputs are independent uniform on S^{d-1}, d≥2, and labels are independent fair signs. Consider

    f(x)=c+sum_{j=1}^k a_j max(0,w_j·x),

where 1≤k≤d and the first-layer rows w_j are linearly independent. There are no hidden biases or separate affine skip. All parameters may depend arbitrarily on the labeled sample. With probability at least

    1-4exp(-d)-2exp(-n/8),

every such network with empirical squared error at most1/256 satisfies

    Lip_{S^{d-1}}(f) ≥ (1/4096)sqrt(n/k).                 (1)

Constants are deliberately loose. For small d this displayed probability can be weak; as both d and n grow it tends to one without a logarithmic loss. Full row rank and zero hidden biases are essential restrictions of this proof. The original BLN spectral-proxy approach and classical subgaussian chaining are credited ingredients; no historical novelty is certified. The arbitrary-weight piecewise-linear preprint discussed in the source gate addresses a broader class up to logarithms, so this subclass result is not a replacement for it.

## 1. Actual sphere Lipschitz norm controls the coefficient energy

Put h=f-c and L=Lip_S(f). Since W has full row rank, W maps R^d onto R^k. Every strict activation pattern therefore occurs on a nonempty open cone. The empty pattern gives a unit vector u_0 with h(u_0)=0. Consequently |h(u)|≤2L for every unit u.

Positive homogeneity then gives, for r≥s≥0 and unit u,v,

    |h(ru)-h(sv)|≤Ls||u-v||+2L(r-s)≤3L||ru-sv||.

Indeed ||ru-sv||²=(r-s)²+rs||u-v||², which separately dominates (r-s)² and s²||u-v||². The origin follows by continuity. Thus the GLOBAL Lipschitz constant G of h is at most3L. This argument does not identify sphere and global norms without proof.

For every subset A of units, the gradient on its open activation cone is g_A=sum_{j∈A}a_jw_j, so ||g_A||≤G. Write v_j=a_jw_j. For any signs ε_j, sum ε_jv_j=g_A-g_{A^c}, hence its norm is at most2G. Averaging its squared norm over all signs cancels every cross term and proves

    sum_j a_j²||w_j||²≤4G²≤36L².                        (2)

No condition number or lower singular-value bound for W is needed. Dependent rows may prevent a pattern from occurring and are not covered by this argument.

## 2. A self-contained uniform atomic correlation estimate

Condition on the labels and put z_i=y_i-bar(y). Then sum z_i=0 and sum z_i²≤n. For a unit vector u define

    Z(u)=sum_i z_i max(0,u·x_i).

We claim

    P(sup_{u∈S^{d-1}} |Z(u)|>256sqrt(n) | labels)
        ≤4exp(-d).                                     (3)

Here are explicit increment and chaining details, including the centering needed for the output constant. For unit u,v, let H=max(0,u·x)-max(0,v·x). Rotational invariance gives EH=0, and the contraction property gives |H|≤|(u-v)·x|. The spherical moment identity used in turn3 implies

    E|H|^{2m}≤||u-v||^{2m}(2m-1)!!/d^m.

For an independent copy H', Jensen's inequality gives Eexp(tH)≤Eexp(t(H-H')). The difference is symmetric and its 2m-th moment is at most2^{2m}E|H|^{2m}. Summing its even exponential series therefore yields

    Eexp(tH)≤exp(2t²||u-v||²/d).

The identical independent-copy argument applied to max(0,u·x) minus its expectation gives the same bound with ||u-v|| replaced by1. Independence over observations and sum z_i²≤n give

    P(|Z(u)-Z(v)|>t)≤2exp[-dt²/(8n||u-v||²)],          (4)
    P(|Z(u)|>t)≤2exp[-dt²/(8n)].                        (5)

In(5), the deterministic mean term cancels because sum z_i=0.

Choose finite nets S_j of radius2^{-j}, j≥1, with |S_j|≤2^{d(j+2)}, using the usual disjoint-ball volume bound. Set S_0={u_0}. For every u choose u_j∈S_j within2^{-j}. For j≥2, ||u_j-u_{j-1}||≤3·2^{-j}; for j=1 the bound2=4·2^{-1} is sufficient. Thus all links have length at most4·2^{-j}. There are at most2^{d(2j+3)} possible links at level j (also a valid loose bound when j=1).

For an arbitrary v>0 set

    t_j=32sqrt(n/d)·2^{-j}sqrt(d(j+2)+v+j).

By(4) the failure probability for one link is at most2exp[-8(d(j+2)+v+j)]. After multiplying by the link count, it is at most2exp[-v-j]: indeed log2<1 and the remaining exponent is strictly more negative. Summing over j≥1 gives at most2exp(-v)/(e-1)<2exp(-v). The base point bound |Z(u_0)|≤8sqrt(nv/d) fails with probability at most2exp(-8v) by(5). Consequently, outside a set of probability at most4exp(-v), continuity of the finite ReLU sum and telescoping the net approximants give

    sup_u |Z(u)|≤8sqrt(nv/d)+sum_{j≥1}t_j.

Use sqrt(a+b+c)≤sqrt(a)+sqrt(b)+sqrt(c), and

    sum 2^{-j}=1,
    sum 2^{-j}sqrt(j+2)≤sum 2^{-j}(j+2)=4,
    sum 2^{-j}sqrt(j)≤sum 2^{-j}j=2.

With v=d, the last bound is at most

    8sqrt(n)+128sqrt(n)+32sqrt(n)+64sqrt(n/d)
       ≤232sqrt(n)<256sqrt(n).

This proves(3). It is a uniform event over all unit directions, rather than a finite net that depends on the eventual network. All infinite suprema are measurable since the sample process is continuous on the compact sphere and has a countable dense determining subset.

## 3. Centered-label correlation and the width bound

Hoeffding gives |bar(y)|≤1/2 with failure probability at most2exp(-n/8). On that event, if e_i=f(x_i)-y_i and sum e_i²≤n/256, then

    sum_i z_i f(x_i)
      =n(1-bar(y)²)+sum_i z_i e_i
      ≥3n/4-n/16≥n/2.                                  (6)

The output constant drops out. Normalize each row u_j=w_j/||w_j|| and put b_j=a_j||w_j||. Equations(2), (3), Cauchy–Schwarz and(6) give

    n/2≤|sum_j b_j Z(u_j)|
        ≤6L sqrt(k)·256sqrt(n).

Thus L≥sqrt(n/k)/3072, which implies(1). Both probability events were chosen independently of the network, so the conclusion holds simultaneously for all allowed data-dependent parameters. If L is infinite the assertion is automatic.

## 4. Remaining scope

This proves the source lower order without polynomial parameter bounds in this explicitly independent, bias-free ReLU subclass. It does not cover dependent or overcomplete hidden rows, hidden biases, arbitrary Lipschitz activations, or Gaussian data under a sphere norm. In particular it does not settle the original conjecture. The checker verifies the subset-gradient identity, radial distance inequalities and the exact algebra behind the constants. The full stochastic theorem follows from the displayed moment and chaining proof, not from a finite empirical experiment. Original unresolved4/5.
