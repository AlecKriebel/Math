# Author turn 4: a genuine surface in a nilpotent cover

**Outcome:** all-order geometric intersection realization in a marked nilpotent cover, with a lower-data closing path and a proved descent obstruction. The comparison with Polyak's recursively derived link downstairs is still missing. This is author turn 4/5, with no final unresolved disposition yet.

This turn goes beyond merely labeling holonomy as a linking number: it constructs a closed integral cocycle on a genuine covering three-manifold, represents it by a properly embedded oriented surface, and pairs it with an actual compact closed lifted curve. The cover and the lower-data closing path are essential parts of the result. They are not silently identified with the source's original $L_{12\cdots n-1}$ and $L_n$.

## 1. The marked cover and a fixed section

Apply the construction of Turn 3 to the sub-string-link obtained by deleting the distinguished strand $k$. Write $M$ for this sublink exterior, $P$ for its bottom punctured disk, and retain the boundary base point and target word $I=(i_1,\ldots,i_r)$. We obtain the representation

$$
\rho:\pi_1(M,*)\longrightarrow U=U_{r+1}(\mathbb Z)
$$

by the same argument. Its boundary meridians map to the adjacent elementary matrices in (2) of that turn. The original strand $k$, now lying in this exterior, closes along the fixed boundary basing to a loop denoted $\lambda_k$. This is the image of its preferred parallel under forgetting strand $k$; any framing factor is killed. Forgetting the strand sets $X_k=0$ in the Magnus expansion and hence preserves every target coefficient here. Equivalently, the full-exterior representation of Turn 3 factors through this exterior because it sends the meridian $x_k$ to the identity. Thus the cover and the surface below can be chosen from the other strands alone; the closing correction will depend on the last strand's lower data. Let

$$
Z=\{I_{r+1}+zE_{1,r+1}:z\in\mathbb Z\},\qquad Q=U/Z.
$$

For $r=1$, $Z=U$ and $Q$ is trivial. Otherwise $Z$ is the usual central top-entry subgroup. Adjacent elementary matrices generate $U$ over the integers, so $\rho$ is surjective. Indeed their iterated commutators produce every $I+aE_{pq}$, and elementary elimination expresses every upper unitriangular matrix as a product of these matrices. Hence the composition $\overline\rho:\pi_1(M)\to Q$ gives a connected regular cover

$$
\pi:\widetilde M\longrightarrow M
$$

with a marked lift of the base point.

There is a fixed set-theoretic section $s:Q\to U$: in a coset, set the $(1,r+1)$ entry to zero and leave all other entries unchanged. Multiplication by a central matrix changes only that top entry, so this specifies one representative uniquely. In particular $s(1)=I_{r+1}$. This section is generally **not** a group homomorphism.

## 2. A closed integral cocycle on the cover

Use the flat edge labels $g_e$ of Turn 3 to describe the cover combinatorially. A lift of an oriented edge $e:v\to w$ starting at sheet $q\in Q$ ends at sheet

$$
q'=q\,\overline{g_e}.
$$

Define the integer $b(q,e)$ by

$$
s(q)\,g_e\,s(q')^{-1}=I_{r+1}+b(q,e)E_{1,r+1}. \tag{1}
$$

The left side lies in $Z$ by construction. Reversing a lifted edge negates $b$, because it inverts this central matrix. Around a lifted triangle, the three products telescope, and the flatness of $g$ makes their product identity. Therefore

$$
\delta b=0
$$

as an **ordinary additive integral one-cocycle** on $\widetilde M$. This is the feature that the separate higher entries downstairs lacked.

For a closed based lifted loop $\widetilde\gamma$, the same telescoping argument gives

$$
\sum_{e\in\widetilde\gamma} b(e)
=\rho(\gamma)_{1,r+1}, \tag{2}
$$

because a closed based lift has $\overline\rho(\gamma)=1$, so $\rho(\gamma)$ is central. Thus the cohomology class of $b$ is the central integer homomorphism on $\ker\overline\rho$.

This also proves independence of the vertex trivialization and the integral filling choices used in Turn 3. They yield the same based representation and marked cover. Changing the section modifies (1) by a coboundary on the cover. Its integral over every closed curve remains the same. The special zero-top section is retained below to specify the closing path and extract the intended integer without an extra lower-data term.

## 3. Actual properly embedded surface representative

The cover is a smooth, orientable, second-countable three-manifold with boundary and a locally finite lifted triangulation. Its integral cohomology class $[b]\in H^1(\widetilde M;\mathbb Z)$ is represented by a map

$$
f:\widetilde M\longrightarrow S^1.
$$

One explicit construction maps every vertex to a fixed circle point, maps each oriented edge with winding number $b(e)$, extends over each two-simplex because $\delta b=0$, and extends over higher cells because $\pi_j(S^1)=0$ for $j>1$. The locally finite CW topology makes this a continuous global map. Smooth approximation preserves its homotopy class.

Choose a value regular for both the smooth map and its boundary restriction. Such a value exists by applying Sard's theorem to a countable atlas for the manifold and its boundary. Then

$$
\Sigma=f^{-1}(z)
$$

is a properly embedded cooriented, hence oriented, surface. It can be noncompact and can have infinitely many components, but is locally finite. Properness follows because it is a closed regular level set; its intersection with any compact set is compact. A transverse compact curve meets it in finitely many points.

For every compact oriented closed curve $C$ transverse to $\Sigma$,

$$
C\cdot\Sigma=\langle[b],[C]\rangle. \tag{3}
$$

This is the degree of the circle map restricted to $C$. Choosing a different smooth representative or regular value does not change the pairing. Thus there is a genuine geometric surface-intersection invariant, not just formal dual-cell notation.

The surface is not claimed to be compact, nor to bound a compact derived link in the original ball. Its boundary may run through infinitely many lifted boundary cells and need not form a compact link. Those distinctions matter for the original problem.

## 4. Close the longitude using only lower-order data

For the distinguished component $k$, let

$$
G=\rho(\lambda_k),\qquad q=\overline G\in Q.
$$

All entries of $q$ are proper contiguous-subword coefficients of the target index word; the desired full coefficient is the omitted top entry. Thus $q$ is lower-order data for this flag.

Because the representation on the boundary free group surjects onto $U$, choose a based loop $\eta_q$ entirely in $P$ whose matrix is

$$
\rho(\eta_q)=s(q)^{-1}. \tag{4}
$$

This choice is constructive and does not require the unknown target coefficient. Starting from the explicit matrix $s(q)^{-1}$, elementary upper-triangular elimination factors it into integer powers of transvections. Nested commutators of the adjacent meridians realize each transvection. Fixing an elimination order makes a definite word algorithm. Every matrix used in this algorithm is calculated from $q$ alone.

The based loop

$$
\gamma=\lambda_k\eta_q
$$

has trivial $Q$-holonomy and therefore has a closed lift $\widetilde\gamma$ at the marked point. Since $G$ and $s(q)$ differ only in their top entry,

$$
\rho(\gamma)=G\,s(q)^{-1}
=I_{r+1}+G_{1,r+1}E_{1,r+1}. \tag{5}
$$

Perturb the compact lifted loop into the interior and into general position with $\Sigma$. It may be used as an oriented cycle; alternatively a small general-position perturbation in a three-manifold realizes the same loop class by an embedded closed curve. The intersection pairing is unchanged. Combining (2), (3), (5) and the coefficient identification of Turn 3 gives

$$
\boxed{\quad
\widetilde{\lambda_k\eta_q}\cdot\Sigma
=\mu_{i_1\cdots i_r,k}(S).
\quad} \tag{6}
$$

Any other boundary word with the **same full matrix image** in (4) gives the same value. It is not enough to have the same image merely in $Q$: an unspecified central factor would change the integer. This is the exact analogue of retaining the canonical lift in the previous turns.

For $r=1$, the cover is just $M$, the closing correction is trivial, and $[b]$ is the ordinary meridian-dual cohomology class. Thus (6) reduces to the usual pairwise linking number. This base-case agreement does not by itself establish the higher derived-link comparison.

### Explicit triple case

In $U_3$, write the lower entries as $a=G_{12}$ and $b=G_{23}$ and the top entry as $c=G_{13}$. The zero-top section can be represented by $x_{i_2}^b x_{i_1}^a$, so one may take

$$
\eta_q=x_{i_1}^{-a}x_{i_2}^{-b}.
$$

If the original word is $x_{i_1}x_{i_2}$, this turns its based closure into the commutator $x_{i_1}x_{i_2}x_{i_1}^{-1}x_{i_2}^{-1}$. Its lifted intersection with $\Sigma$ is 1. The correction depends on the two lower linking numbers, not on the desired triple coefficient.

## 5. A rigorous obstruction to one naive descent

For $r\ge2$, the class $[b]$ generally cannot be the pullback of an ordinary class in $H^1(M;\mathbb Z)$. To see this, use the based boundary commutator word

$$
w=[x_{i_1},[x_{i_2},\ldots,[x_{i_{r-1}},x_{i_r}]\ldots]].
$$

With the convention $[a,b]=aba^{-1}b^{-1}$, adjacent matrix-unit multiplication gives

$$
\rho(w)=I_{r+1}+E_{1,r+1}.
$$

The word has zero abelianization and has a closed lift to $\widetilde M$. Equation (2) pairs that lift with $[b]$ to give 1. But every class in $H^1(M;\mathbb Z)$ pairs trivially with $w$, since $w$ is a commutator. Pullback would preserve this pairing, a contradiction.

This rules out descending the present surface class to a single **closed additive dual class on the unmodified exterior**. It does not rule out the source's construction: a derived curve, its complement, and a relative bounding surface introduce additional geometry. Nor does it refute the classical vanishing-lower-invariant formula. It precisely identifies what cannot be discarded in this cover-based approach.

## 6. Status of the geometric route

Equation (6) is an all-order, choice-controlled intersection presentation using a genuine properly embedded surface and a lower-data-corrected lifted longitude. All original string links are allowed, and the integer is not computed first and then encoded by an artificial number of meridian circles.

Nevertheless, the original target asks to justify the iterated derived-link notation $L_{12\cdots n-1}$ and its linking with the original last component. This turn has not supplied a comparison from the nilpotent-cover surface to that recursively constructed downstairs link. In particular, compactness, allowed relative boundaries, ordered push-offs, and the relation between the closing correction and a derived Seifert surface remain to be proved. Calling (6) that requested linking number without this comparison would conceal the gap.

The final author turn will investigate whether this additional geometric comparison can be established, or isolate the strongest rigorously proved substitute. No full resolution or final partial PR is claimed at turn 4.
