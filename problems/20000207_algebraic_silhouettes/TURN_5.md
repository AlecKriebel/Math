# Turn 5: explicit calibrated real silhouette ambiguity and the final scope boundary

AI-assisted mathematical research; independent review pending. Fifth and final author turn. This is a self-contained physical realization of the classical conic/sphere ambiguity, not a claimed new negative discovery. Kahl–Heyden (ICCV1998) already treats quadric silhouettes and their insufficient single-pair constraints; the imported research report explicitly credits that result and proves complex quadric realizability. Here the same fixed real sphere and fixed calibration suffice to make a continuum of different relative epipolar geometries indistinguishable by their entire visible silhouettes.

## 1. One fixed sphere and a fixed calibrated camera

Let the world object be the unit sphere centered at the origin, including its opaque solid interior for visibility. Fix R>1 and focal length f=sqrt(R²-1). Let K=diag(f,f,1). Camera1 has center C1=(0,0,R), world-to-camera rotation A1=diag(1,-1,-1) and translation t1=(0,0,R). It has positive depth R-Z for every sphere point, at least R-1>0.

For theta in (0,pi), write c=cos theta and s=sin theta. Camera2 has center C2=(R s,0,R c), rotation

A2 = [[c,0,-s],[0,-1,0],[-s,0,-c]],

and translation t2=(0,0,R). The rows are orthonormal and det A2=1; A2 C2+t2=0. Its optical axis also points toward the sphere center. In either camera the sphere center has coordinates (0,0,R), with the same radius and calibration. All sphere points have positive camera depth.

## 2. The complete visible silhouette is unchanged

For an image point (u,v,1), its camera ray is rho*(u/f,v/f,1), rho>0. Intersecting this ray with the unit sphere centered at (0,0,R) in camera coordinates gives

rho²*(1+(u²+v²)/f²)-2R rho+(R²-1)=0.

The discriminant divided by4 is

R²-(R²-1)*(1+(u²+v²)/f²)=1-u²-v².

Thus the ray meets the sphere exactly for u²+v²<=1. For such points both roots are positive: their sum and product are positive, and their discriminant is nonnegative. The nearer intersection is the visible surface point. The entire projected solid silhouette is exactly the closed unit disk, and its visible boundary is the unit circle. This calculation holds for every theta. It uses full real visibility and cheirality, not merely complex contour equations or clipped arcs.

## 3. The fundamental matrix actually changes

Relative camera motion is

A=A2*A1^T=[[c,0,s],[0,1,0],[-s,0,c]],
t=t2-A*t1=(-R s,0,R(1-c)).

With the convention x2^T F x1=0, E=[t]_cross A and F=K^(-T) E K^(-1). Direct multiplication gives

F(theta)=R*[[0,(c-1)/f²,0],[(c-1)/f²,0,s/f],[0,-s/f,0]].

For theta in (0,pi), c-1 is nonzero and s>0, so F has rank exactly2 (a nonzero 2-by-2 minor and the zero determinant verify this). Its projective ratio

F23/F12=f*s/(c-1)=-f*cot(theta/2)

is strictly varying on this interval. Hence distinct theta give distinct fundamental matrices up to scalar. Both images nevertheless show exactly the same unit disk, with exactly the same algebraic boundary u²+v²=1. The world sphere and camera calibration were fixed throughout.

A rational subfamily avoids numerical trigonometry: set a=tan(theta/2)>0, c=(1-a²)/(1+a²), s=2a/(1+a²). Taking R=5/3 and f=4/3 makes every matrix rational for rational a. The ratio becomes -f/a, so infinitely many positive rational a give pairwise distinct rational fundamental matrices with identical full visible data.

## 4. Consequences without overstating the source

There cannot be a universally single-valued recovery of F from one arbitrary silhouette pair, even with algebraic boundaries, complete visibility, known calibration and this one fixed smooth convex object. This is a concrete instance of the established low-class/conic ambiguity. It is compatible with Turns3–4, whose generic smooth-primal theorem requires d>=3 and data general in that fixed-degree family. Spherical symmetry and degree2 lie outside it.

There are nevertheless algebraic constraints for suitable full contours: the credited dual-section/Kruppa identity equates the divisors of tangent epipolar lines. This packet advances their exact recovery interpretation through (i) local rank and global recovery for a general smooth dual-degree family, (ii) local isolation for a general smooth primal surface of any fixed degree d>=3, and (iii) global finite F-values among the corresponding actual admissible smooth fixed-degree realizations. It neither determines the finite ambiguity count in (iii) nor proves global uniqueness there, and it does not turn clipped/noisy visible data into full complex contour equations.

The broad original AIM item is an informal two-part research question, not a theorem with an explicit genericity convention. The imported expanded title must not replace it. Recommended conservative disposition of this five-turn packet is **unsolved5/5 with reviewed partial theorems**, unless the independent source review supplies a different carefully qualified classification. No sixth author search or novelty claim is made.

## 5. Exact verification

The standard-library checker uses the rational subfamily, checks rotations, centers, relative motion, essential/fundamental matrices, rank, pointwise epipolar identities for rational world points, the ray discriminant identity and pairwise-distinct projective ratios. Positive-depth and the complete disk visibility conclusions follow from the written inequalities for all R>1, not from finite sampling.
