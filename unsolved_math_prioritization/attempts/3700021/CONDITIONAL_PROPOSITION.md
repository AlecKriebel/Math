# A conditional bounded well construction for subharmonic functions

## Status

This is an authored sufficient criterion motivated by [Eremenko's Problem 2](https://www.math.purdue.edu/~eremenko/dvi/potvd.pdf). The existence of data satisfying its all-height hypothesis for arbitrarily small error is not established. The original problem remains unresolved.

## Proposition

Let Q={x+iy: |x|<1, |y|<1} and 0<δ<1/2. Let Ω be an open set containing Q, and let V be a locally integrable subharmonic function on Ω with Riesz measure μ=(2π)^(-1)ΔV. Suppose

    V(x+iy)≤x+δ for every x+iy∈Q.

Let {B_j=B(a_j,R_j)} be a finite or locally finite family in Ω with pairwise disjoint closures compactly contained in Ω. Local finiteness means that each compact subset of Ω meets only finitely many disks. Suppose there are finite c_j≥0 and γ_j>0 such that

    V≡c_j on B_j,
    μ|_{∂B_j}≥γ_j λ_j,

where λ_j=ds/(2πR_j) is normalized arclength on ∂B_j. Define

    G_j(z)=log(|z−a_j|/R_j) for z∈B_j,
    G_j(z)=0 otherwise,
    G_j(a_j)=−∞,
    W=V+Σ_j γ_jG_j,
    u(x+iy)=max(W(x+iy),x−δ),  x+iy∈Q.

Then u is finite and subharmonic on Q, and

    sup_Q |u(x+iy)−x|≤δ.

For r_j=R_j exp(−c_j/γ_j), every nonempty set

    N_j=Q∩B(a_j,r_j)∩{x<δ}

is a whole connected component of {u<0}, distinct from the component D* containing −1/2. In particular, if the union of the vertical projections of the N_j is (−1,1), then {u<0}\D* meets every horizontal segment at height t∈(−1,1).

If such data exist for a sequence δ_k→0, their corresponding u_k satisfy the whole-square uniform convergence and every-height property in Problem 2.

## Proof

The logarithmic patch satisfies

    (2π)^(-1)ΔG_j=δ_{a_j}−λ_j.

Indeed, integration by parts on a punctured disk gives the center mass 2πδ_{a_j}; the outward normal derivative drops from 1/R_j to zero across the outer circle, giving −ds/R_j there. Local finiteness makes all sums locally finite in the distributional calculation. The circle supports are disjoint, and the measure inequalities imply

    (2π)^(-1)ΔW
      =μ−Σ_j γ_jλ_j+Σ_j γ_jδ_{a_j}≥0.

We verify that the pointwise W is its subharmonic representative. Away from the centers, W is the sum of V and a locally finite continuous function. Averages over shrinking disks therefore converge to its given pointwise value, since this is true of V and of continuous functions. At a center, W=c_j+γ_j log(|z−a_j|/R_j) locally, so its disk averages tend to −∞, the prescribed value. Distributional positivity yields a subharmonic representative, and these averaging limits identify it with W everywhere.

Every G_j is nonpositive, so W≤V≤x+δ on Q. The maximum with the harmonic function x−δ is finite and subharmonic, with

    x−δ≤u≤x+δ

throughout Q. This proves the uniform estimate, including the centers.

Since c_j≥0, one has r_j≤R_j. Within B_j, no other patch is present, and

    W=c_j+γ_j log(|z−a_j|/R_j).

The two quantities in the maximum defining u are both negative precisely on N_j, so {u<0}∩B_j=N_j. At each b∈∂B_j∩Q, upper semicontinuity and the constant interior values give V(b)≥c_j≥0. All patches vanish at b; hence u(b)≥0. Thus the open set D={u<0} has no point on ∂B_j. Its intersection with B_j is both open and closed relative to D. Any component meeting that intersection stays inside it, and N_j is convex and therefore connected. It follows that each nonempty N_j is one whole component of D.

The connected left subrectangle Q∩{x<−δ} lies in D because u≤x+δ<0 there, and it contains −1/2. Meanwhile B_j∩Q has no point with x<−δ: such a point would contradict c_j=V≤x+δ<0. Since N_j is a whole component and is disjoint from that subrectangle, it is different from D*.

The projection condition supplies a point in a component N_j different from D* at each height. Finally, applying the same construction with δ=δ_k gives sup_Q|u_k−x|≤δ_k→0. This proves the conditional sequence assertion.

## Finite patch variant

For L_j>c_j/γ_j, define a finite patch by replacing log(|z−a_j|/R_j) inside B_j with its maximum with −L_j. Its normalized Laplacian is

    λ_{a_j,R_j exp(−L_j)}−λ_{a_j,R_j},

where each λ is normalized arclength on the indicated circle. The same circle-mass payment proves subharmonicity after patching. The strict inequality L_j>c_j/γ_j ensures that the negative core remains exactly B(a_j,r_j). Applying the same maximum with x−δ gives all conclusions above. This variant changes neither the negative-core radius nor the unproved coverage requirement.

## Exact threshold for retaining a prescribed smaller disk

For 0<q<1, before the final affine maximum one has

    B(a_j,qR_j)⊆{W<0} if and only if c_j≤γ_j log(1/q).

This follows from qR_j≤r_j. The nonstrict inequality is correct for an open disk: at equality only its boundary is at level zero. For the closed disk to be negative, or for a positive radial margin, the condition is strict. After the affine maximum, the separate condition x<δ must also hold at each retained point. This corrects a strict-inequality necessity claim in the explanatory discussion of the examined report; the proposition itself is unchanged.
