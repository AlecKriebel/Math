# Exact collar-germ verification

This is an independent differential-topology clarification of the marked proof. It makes precise why restoring boundary values and restoring smooth gluing germs are separate steps. It does not require the chosen boundary identification between the two handlebodies to extend.

Let M=H be the smooth rounded exterior and τ its prescribed smooth boundary involution. The tube maps Jᵢ and the outer map r define a compatible local involution j near ∂M: at each seam the charts are standard, so both formulas agree in a full neighborhood. The exterior side is invariant under j. Average any local metric with j's pullback. The inward normal collar c for this invariant metric satisfies

j(c(x,u))=c(τx,u).

Let F be any smooth extension already corrected to have F|∂M=τ. Its image collar, parametrized with the same boundary point, is

d(x,u)=F(c(τ⁻¹x,u)).

It is a collar and d(x,0)=x. Thus c and d agree as embeddings at the boundary. The uniqueness of smooth collars relative to boundary, followed by isotopy extension, gives a diffeomorphism K supported in a boundary neighborhood, fixing the boundary pointwise, with

K(d(x,u))=c(x,u)

for sufficiently small u. Positive inward transverse derivatives ensure these collars belong to the same collar component; no orientation sign or annular twisting condition is added. Now

(K∘F)(c(x,u))=K(d(τx,u))=c(τx,u)=j(c(x,u)).

Consequently the corrected extension agrees with the prescribed local map in a full exterior neighborhood, so it glues smoothly to Jᵢ and r. The required K need not commute with τ and the final global extension need not square to identity. Neither condition is used.

For the last ball isotopy, suppose g is identity on a boundary collar. Contractibility of smooth Diff(D³ rel∂D³) supplies a relative-boundary path. Apply the same collar uniqueness parametrically, with correction identity at the two path endpoints, to make a uniformly smaller boundary collar fixed throughout. Compactness of the path parameter gives a common positive collar width. That path extends by the identity outside the compact ball in the long-link model. This is a smooth collar argument, not a smooth version of the elementary radial Alexander trick.
