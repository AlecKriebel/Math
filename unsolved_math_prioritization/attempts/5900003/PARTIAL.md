# Spherical Plateau networks: volume labels and a negative exchange mode

**5900003 / AMR-058-0003. Scoped obstruction; original intended question unresolved.** One approach. The construction below is a stationary connected network of spherical and planar pieces with genuine Plateau triple circles. It is unstable when two physical components share one volume label. Section7 also gives a fully spherical version with no planar interface. This is not offered as a resolution of Kusner's intended question for separate bubble volumes or globally spherical pairwise interfaces. No novelty claim is made. Independent review is pending.

## 1. Exact source and the unresolved convention

Sullivan–Morgan's *Open Problems in Soap Bubble Geometry* (1996), Problem3, asks whether clusters built from spherical pieces satisfying Plateau's rules have nonnegative second variation. Its introductory cluster problem prescribes a list of enclosed volumes; the adjacent Problem2 explicitly allows disconnected regions. The short Problem3 paragraph does not spell out whether distinct physical bubbles may share a volume constraint or whether each entire interface between a fixed pair of labeled cells must lie in one sphere.

This distinction cannot be suppressed. In the modern labeled-cell formulation a cluster is a tuple of regions, and a region may be disconnected. Its prescribed volume is the sum over its components. By contrast, treating those components as separately labeled bubbles imposes more constraints. The same geometric network can be stable under the smaller perturbation class and unstable under the larger one.

Milman–Xu, *Standard bubbles (and other Möbius-flat partitions) on model spaces are stable*, arXiv:2504.11185v1 (2025), explicitly defines possibly disconnected cells. It establishes important positive results for **regular, Möbius-flat, spherical Voronoi partitions**, with an explicit technical restriction on the scalar perturbation fields. Its spherical Voronoi definition requires a globally compatible sphere for each nonempty pairwise interface, not merely independent spherical pieces. Milman's survey arXiv:2510.07078v2, revised31July2026, Section9(3), continues to list Kusner's question as open.

The1996 full PDF could not be recovered in this attempt: the old author endpoint returned a gateway error and the indexed copy redirected to an archive HTML page. The primary indexed text of the introduction and exact Problem3 was read. The full2025 paper and2026 survey were retrieved and their relevant definitions, statements and qualifications inspected. This source-access and interpretation hold is retained.

## 2. The precise partial theorem

There exists a bounded two-cell cluster \((A,B)\) in \(\mathbb R^3\), with exterior \(O\), such that:
- \(A\) has two connected components and \(B\) is connected;
- the union of all interfaces is connected;
- every interface piece is a spherical cap, a spherical band or a planar disk;
- the only singularities are two triple circles meeting at120 degrees;
- the cluster is stationary for the two prescribed volumes \((|A|,|B|)\);
- a smooth, compactly supported, first-order volume-preserving deformation has
\[
 Q=\delta^2\operatorname{Area}-2\delta^2|A|-2\delta^2|B|
 =-\frac{243\pi}{16}<0. \tag{1}
\]

An exactly volume-preserving smooth variation with the same negative constrained second derivative also exists. Section7 gives an explicit version with every interface piece on a finite-radius sphere and with negative constrained second variation \((72\sqrt3-136)\pi\).

This disproves the implication from componentwise spherical geometry and Plateau angles to stability in the broad labeled-cell class. The example does **not** have a single global sphere containing each labeled interface \(A\!-\!O\) or \(A\!-\!B\), and its exchange mode does **not** preserve the two component volumes separately.

## 3. The stationary base configuration

Let \(e=(0,0,1)\), write a point as \(x=(x_1,x_2,z)\), and put
\[
 A_+=B_1(e)\cap\{z>1/2\},\qquad
 A_-=B_1(-e)\cap\{z<-1/2\},
\]
\[
 A=A_+\cup A_-,\qquad
 B=B_1(0)\cap\{-1/2<z<1/2\}. \tag{2}
\]
Here boundaries can be assigned arbitrarily because they have zero volume. The exterior is the complement of the three closed regions, up to those null sets.

The \(A\!-\!B\) interfaces are disks at \(z=\pm1/2\), of radius \(\sqrt3/2\). The \(B\!-\!O\) interface is the corresponding band on the unit sphere centered at zero. The \(A\!-\!O\) interfaces are the remaining major caps of the unit spheres centered at \(\pm e\).

At the upper triple circle, with \(|x|=1\) and \(z=1/2\), the outward normals toward the exterior are
\[
 n_{AO}=x-e,\qquad n_{BO}=x,
\]
and the normal from \(A_+\) to \(B\) is \(n_{AB}=-e\). Hence
\[
 n_{AB}+n_{BO}-n_{AO}=0.
\]
All three are unit vectors, so the three oriented conormals balance and the sheets meet at120 degrees. The lower circle is its reflection. There are no quadruple points.

Every outer spherical piece has scalar mean curvature2, and both internal disks have mean curvature zero. Thus the pressure vector is \(p_A=p_B=2,\ p_O=0\). The first variation of area, including cancellation at the balanced triple circles, gives
\[
 \delta\operatorname{Area}=2\delta|A|+2\delta|B| \tag{3}
\]
for every smooth compactly supported ambient variation. This is constrained stationarity, not an assertion of minimality.

The initial volumes and total area are
\[
 |A|=\frac{9\pi}{4},\qquad |B|=\frac{11\pi}{12},
 \qquad \operatorname{Area}=\frac{19\pi}{2}. \tag{4}
\]

## 4. A smooth geometric family through the triple circles

Keep the central outer sphere at radius1. For a positive satellite radius \(r\) define
\[
 d(r)=\sqrt{1+r^2-r},\qquad
 z_b(r)=\frac{2-r}{2d(r)},\qquad
 \rho(r)^2=1-z_b(r)^2. \tag{5}
\]
The upper satellite's outer sphere has center \(d(r)e\) and radius \(r\). Its intersection with the central sphere is the circle \(z=z_b(r)\), of radius \(\rho(r)\). The choice of \(d(r)\) makes the two exterior unit normals have inner product \(1/2\) there.

The internal interface is the portion, inside that circle, of the generalized sphere
\[
 F_r(x):=(1-r)|x|^2-2d(r)z+1=0. \tag{6}
\]
The satellite lies on the side \(F_r<0\). At \(r=1\) this is the plane \(z=1/2\). Its unit normal from satellite to central cell is
\[
 n_{AB}=\frac{1-r}{r}x-\frac{d(r)}r e. \tag{7}
\]
Equation (6) verifies that this vector has length1 on the interface. At the triple circle it equals \(n_{AO}-n_{BO}\), so all Plateau angles remain120 degrees. Its mean curvature is \(2/r-2\), the difference between satellite and central pressures. All pieces therefore form a smooth family of stationary three-physical-bubble configurations, with pressures \(2/r_+,2/r_-,2\) when the upper and lower radii are \(r_+,r_-\).

For sufficiently small changes from the displayed base radii in \(r_\pm\), the two satellite regions remain disjoint, the central region remains connected, and the two triple circles remain separated. The planar limit in (6) is nonsingular as a graph near the closed disk, since its \(z\)-derivative at \(r=1\) is minus2. This family does not require interpreting an infinite-radius sphere as a singular geometric surface.

## 5. Exact area and volume calculation

For one upper satellite put
\[
 z_0(r)=\frac1{d(r)+r},\qquad
 h(r)=z_b(r)-z_0(r),\qquad
 h_A(r)=r+d(r)-z_b(r),\qquad h_B(r)=1-z_b(r).
\]
The axial point of the internal interface is \(z_0(r)\). The signed volume between its graph and the plane of its boundary circle is
\[
 W(r)=\frac{\pi h(r)}6\bigl(3\rho(r)^2+h(r)^2\bigr). \tag{8}
\]
This formula is smooth through \(h=0\); its sign changes with the side of the cap.

Let \(V(r)\) be the satellite volume, \(U(r)\) the volume removed from the central unit ball by that satellite, and let \(S(r)\) be its contribution to the total area, including the corresponding share of the central sphere:
\[
\begin{split}
 V(r)&=\pi h_A(r)^2\left(r-\frac{h_A(r)}3\right)+W(r),\\
 U(r)&=\pi h_B(r)^2\left(1-\frac{h_B(r)}3\right)+W(r),\\
 S(r)&=2\pi r h_A(r)+2\pi z_b(r)
       +\pi\bigl(\rho(r)^2+h(r)^2\bigr).
\end{split} \tag{9}
\]
The last term in \(S\) is the internal cap area, including its disk limit.

Now take
\[
 r_+(t)=1+t,\qquad r_-(t)=1-t.
\]
For the two labels in (2),
\[
 |A_t|=V(1+t)+V(1-t),\qquad
 |B_t|=\frac{4\pi}{3}-U(1+t)-U(1-t),
\]
\[
 \operatorname{Area}_t=S(1+t)+S(1-t). \tag{10}
\]
Both volume derivatives vanish at zero by symmetry. Exact differentiation of (5)–(9) gives
\[
\begin{array}{c|ccc}
 &V&U&S\\ \hline
 \text{value at }1&9\pi/8&5\pi/24&19\pi/4\\
 \text{first derivative at }1&243\pi/64&27\pi/64&27\pi/4\\
 \text{second derivative at }1&135\pi/16&0&297\pi/32.
\end{array} \tag{11}
\]
Using the stationary pressures in (3), the constrained second variation is
\[
 Q=2S''(1)-4V''(1)+4U''(1)
   =-\frac{243\pi}{16},
\]
proving the negative value in (1). As a consistency check, the first-variation identity for one physical satellite is
\(S'(1)=2V'(1)-2U'(1)\).

## 6. The mode is a legitimate ambient variation

The negative direction is not just a formal independent displacement of interface sheets. Define the smooth polynomial vector field
\[
 Z(x)=zx-\frac{1+|x|^2}{2}e. \tag{12}
\]
It is tangent to the central unit sphere because
\[
 x\cdot Z(x)=\frac z2(|x|^2-1).
\]
On the upper exterior satellite cap,
\[
 Z\cdot(x-e)=\frac{1+z}{2},
\]
which is precisely the normal velocity obtained by differentiating its radius and center in (5), since \(d'(1)=1/2\). On the internal disk,
\[
 Z_z=-\frac{x_1^2+x_2^2}{2}-\frac38,
\]
which is the graph velocity obtained by differentiating (6). Thus one ambient field realizes the simultaneous first-order motion of all sheets at the upper triple circle.

Reflect (12) across \(z=0\) for the lower satellite and use its negative, since \(r_-'(0)=-1\). Multiply the two fields by smooth compact cutoffs equal to1 near the respective closed satellite caps and disks, with disjoint supports in \(z>1/4\) and \(z<-1/4\). On the remainder of the central outer sphere the fields are tangent. Their sum is a smooth compactly supported field whose normal components are those of (10) everywhere on the cluster.

For a stationary regular cluster the constrained second variation depends only on these normal components, as in the standard cluster Jacobi form, so (11) computes the second variation of this physical field. The initial component volume derivatives are nonzero and opposite:
\[
 \delta|A_+|=243\pi/64,\qquad \delta|A_-|=-243\pi/64.
\]
Their sum and the derivative of \(|B|\) vanish, exactly as required by the two-label constraint.

Finally, choose two auxiliary smooth fields supported on separate regular patches of \(A\!-\!O\) and \(B\!-\!O\), respectively. Their two-label volume-derivative vectors are independent. The implicit function theorem corrects the flow by parameters of order \(t^2\) to preserve both volumes exactly. By (3), the area second derivative of the corrected curve is the constrained value \(Q\). Thus requiring exact volume preservation rather than first-order preservation does not remove the instability.

## 7. A fully spherical version, without planar interfaces

The same family gives a concrete example in which even the internal interfaces have finite radius. Set \(r_0=1/2\) and \(d_0=\sqrt3/2\), and define
\[
 A_+=B_{1/2}(d_0e)\cap B_1(\sqrt3e),\qquad
 A_-=-A_+,
\]
\[
 A=A_+\cup A_-,\qquad
 B=B_1(0)\setminus
 \bigl(\overline{B_1(\sqrt3e)}\cup\overline{B_1(-\sqrt3e)}\bigr).
 \tag{13}
\]
The triple circles are at \(z=\pm\sqrt3/2\), with radius \(1/2\). The external satellite interfaces have radius \(1/2\), the central exterior interface has radius1, and both internal interfaces have radius1. At the upper circle,
\[
 n_{AO}=2x-\sqrt3e,\qquad n_{BO}=x,\qquad
 n_{AB}=x-\sqrt3e,
\]
so the same120-degree balance holds. The stationary pressures are now \(p_A=4,\ p_B=2,\ p_O=0\).

The upper and lower components lie in separated positive/negative halfspaces; the central cell is connected and the interface network joins through its spherical band. The family in (5)–(10) is smooth for radii near \(r_0\). In (6), the internal interface is now a regular spherical cap rather than a plane; the implicit derivative in the axial direction does not vanish on that closed cap.

Take \(r_\pm(t)=r_0\pm t\). All first-order two-label volume changes again vanish. Exact differentiation of the same cap formulas gives
\[
\begin{array}{c|ccc}
 &V&U&S\\ \hline
 \text{value at }r_0&
 3\pi/4-3\sqrt3\pi/8&
 4\pi/3-3\sqrt3\pi/4&
 5\pi/2\\
 \text{first derivative at }r_0&
 (17-9\sqrt3)\pi/2&
 (16-9\sqrt3)\pi/2&
 (18-9\sqrt3)\pi\\
 \text{second derivative at }r_0&
 (196-109\sqrt3)\pi/2&
 (96-55\sqrt3)\pi&
 (132-72\sqrt3)\pi .
\end{array} \tag{14}
\]
Consequently
\[
 Q=2S''(r_0)-8V''(r_0)+4U''(r_0)
   =(72\sqrt3-136)\pi<0. \tag{15}
\]
The inequality is exact, since \(9\sqrt3<17\), as follows from \(243<289\). Equivalently, (15) equals \(-16V'(r_0)\).

The ambient-field check also remains explicit. On the upper interfaces use
\[
 Z_0=\frac4{\sqrt3}Z
\]
with \(Z\) from (12). It is tangent to the central sphere. On the outer satellite cap, \(Z_0\cdot n_{AO}=1\), precisely the radius velocity because \(d'(r_0)=0\). On the internal unit sphere, \(Z_0\cdot n_{AB}=|x|^2\), precisely the normal velocity obtained by differentiating (6). Reflect and negate this field on the lower component and use compact cutoffs as before. Thus (15) is realized by a physical smooth volume-preserving-to-first-order field, and the same implicit correction gives exact preservation of the two volumes.

This version rules out an explanation based solely on allowing flat disks as generalized spheres. Its limitation remains the merged volume label and the lack of a single global sphere for each labeled pair.

## 8. Why this does not resolve the intended stronger question

If \(A_+\) and \(A_-\) are assigned separate prescribed volumes, the direction above is inadmissible. If “spherical interface” means that the entire interface between each fixed pair of labels lies in one generalized sphere, the merged example is excluded: \(A\!-\!O\) uses two different spheres and \(A\!-\!B\) uses two different planes. These are substantive changes, not cosmetic terminology.

A simpler control illustrates the same issue. Two disjoint equal-radius balls given one shared volume label are stationary with pressure \(2/R\), but the exactly volume-preserving radius change
\[
 R_\pm(t)=(R^3\pm3R^2t)^{1/3}
\]
has area second derivative \(-16\pi\). If their individual volumes are fixed, that direction is forbidden. The connected triple-circle example shows that the phenomenon is not caused by merely vacuous Plateau junction conditions.

There is also an analytic warning in the2025 positive result. Milman–Xu restrict their asserted perturbations to \(f=L_Vu\) for an admissible field \(u\), where \(L_Vu=V\Delta u-u\Delta V\). Their Remark1.4 explains the unresolved regularity/range issue for all physical volume-preserving fields. Even on two closed sphere components with constant \(V\), the range of \(L_V\) has zero average on **each** component, whereas the opposite constant exchange mode has only zero **total** average. One cannot simply replace the image condition by the volume constraint without proving the necessary range statement.

The exact remaining task is to settle the separately specified global-interface/separate-volume interpretation of Kusner's question, or reconcile that interpretation with the short1996 wording. The present artifact supplies neither a general stability theorem nor a counterexample satisfying those stronger conditions. The queue status therefore remains **unsolved, 1/5**, with a source-scope hold. The current literature's positive theorems are credited, not rebranded as discoveries or audited here in their full52-page analytic proof.
