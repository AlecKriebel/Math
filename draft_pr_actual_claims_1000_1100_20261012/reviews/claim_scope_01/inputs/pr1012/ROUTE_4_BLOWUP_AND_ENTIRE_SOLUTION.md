# Route 4: point selection, normalized blow-up, and an exact Liouville obstruction

## 1. What failure of the target would give

Suppose a source-admissible extremal solution failed the target. There would be x_j->0 with r_j=|x_j| and r_j sqrt(V(x_j))->infinity. On the closed ball D_j=B_(r_j/2)(x_j), which avoids zero, maximize

    d_j(y) M(y),  where d_j(y)=r_j/2-|y-x_j| and M=sqrt(V).

For large j its maximum occurs at an interior point y_j with M(y_j)>0. Put M_j=M(y_j), rho_j=M_j^(-1). If |z-y_j|<d_j(y_j)/2, then d_j(z)>d_j(y_j)/2 and maximality gives M(z)<=2M_j. Thus

    V(y_j+rho_j z)/V(y_j)<=4  on B_(R_j),
    R_j=d_j(y_j)M_j/2 >= r_j M(x_j)/4 -> infinity.               (1)

Also y_j->0 and rho_j/|y_j|->0. This is a genuine point-selection consequence; no potential bound is being assumed.

Set s_j=u*(y_j), a_j=f(s_j)/f'(s_j), and

    v_j(z)=[u*(y_j+rho_j z)-s_j]/a_j,
    g_j(t)=f(s_j+a_j t)/f(s_j).

Then, exactly,

    -Delta v_j=g_j(v_j),  v_j(0)=0,
    g_j(0)=g_j'(0)=1,
    g_j'(v_j(z))=V(y_j+rho_j z)/V(y_j)<=4 on B_(R_j),           (2)

and stability is preserved by change of variables. Each g_j is positive, increasing, and convex. These are formal identities on the rescaled domains, not an assertion of compactness or convergence. Uniform function-space bounds on v_j and useful convergence of the varying g_j require proof; normalization at one value alone does not provide them.

## 2. A blanket stable-entire Liouville claim is false

Even granting enough compactness to pass to an entire limit, the equations and normalizations above do not create a contradiction in the relevant high dimensions.

For every n>=10 define on R^n

    w(x)=-log(1+|x|^2),
    G(t)=2(n-2)exp(t)+4exp(2t).

The function G is smooth, strictly positive, strictly increasing, strictly convex, superlinear at positive infinity, and has finite integral of 1/G on [1,infinity). Direct radial differentiation gives

    -Delta w=2(n-2)/(1+|x|^2)+4/(1+|x|^2)^2=G(w).             (3)

Its stability potential is

    G'(w)=2(n-2)/(1+|x|^2)+8/(1+|x|^2)^2.

Writing t=|x|^2, an exact identity is

    2(n-2)-t G'(w)
        =[2(n-2)+2(n-6)t]/(1+t)^2 >=0                       (4)

for n>=6. For n>=10,

    2(n-2) <= (n-2)^2/4.

Hardy's inequality therefore proves stability for all compactly supported tests on R^n. There is no singularity at the origin; w is smooth everywhere, w<=0, and w(0)=0.

To match both normalizations in (2), set

    a=G(0)/G'(0)=n/(n+2),  rho=[G'(0)]^(-1/2),
    v(z)=w(rho z)/a,       g(t)=G(a t)/G(0).

Then -Delta v=g(v), v(0)=0, g(0)=g'(0)=1, and stability still holds. Since v<=0 and g' is increasing, g'(v)<=1 globally. Thus this smooth nonconstant entire stable pair satisfies even a stronger potential bound than (1). Any proposed contradiction based only on the displayed normalized properties is invalid.

## Exact remaining gap

A successful blow-up proof would need extra compactness and a rigidity/exclusion property inherited from a single fixed nonlinearity, the actual extremal branch, and the isolated-singularity geometry. It cannot use a general no-entire-stable-solution assertion in dimensions n>=10. The example is not a positive zero-Dirichlet extremal solution on a bounded domain and is not a counterexample to the original problem.

Status: exact obstruction to the proposed general blow-up/Liouville route.
