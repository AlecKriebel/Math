# A sharper concentration certificate for {13,17,21}

Status: separate PASS2 refinement for independent audit. The accepted
`52/75` proof in `THREE_DEADLINES_13_17_21.md` is unchanged.

Use its notation `Q=[-4,4]^2`, `U=1_Q`, and

`g=b_17+U*b_21/53`.

The two update types for `g` are `delta_0` and `U/53`. Their exact
largest-square-average profile at sides nine and three is

`c_g(9)=1/53`,
`c_g(3)=1/9`.

For gap four, the concentration-profile boundary reduction therefore
permits

`D_2=81[1-c_g(9)-3c_g(3)]=2781/53`,

and define `f=b_13+U*g/D_2`.

If `f(a_13)<1`, the local `g`-mass is below `D_2`. The boundary
announcement adds at most average `1/53` on its side-nine square; the
following three traversal announcements add at most total average
`3c_g(3)=1/3` on the chosen side-three square. Thus the terminal `g`
value at time 17 is strictly below

`D_2/81+1/53+1/3=1`.

The last phase from time 17 to 21 is exactly as in the accepted proof.

For the first phase the update kernels are now

`delta_0`, `U/D_2`, and `(U*U)/2781`.

For the side-nine concentration of the last kernel, write
`u=1_{[-4,4]}`. Then

`(U*U)(x,y)=(u*u)(x)(u*u)(y)`,
`(u*u)(x)=9-|x|` for `|x|<=8` and zero otherwise.

The largest sum over nine consecutive entries of this symmetric
unimodal sequence is its centered sum

`9+2(8+7+6+5)=61`.

Hence the largest side-nine average of `(U*U)/2781` is
`61^2/(81*2781)`, smaller than the middle kernel's `53/2781`, since
`61^2=3721<81*53=4293`. The delta's average `1/81` is also smaller.
Thus

`c_f(9)=53/2781`.

At side three, both smeared kernels have pointwise peaks below `1/9`:
their peaks are `53/2781` and `81/2781`. The delta supplies exactly
`1/9`, so `c_f(3)=1/9`.

With terminal time 13, the online concentration-profile strategy gives

`f(a_13) <= 9(53/2781)+3(1/9)=52/103<1`.

All subsequent implications and the boundary timing are explicit above.
This sharper bound is an optional improvement of the same restricted
three-deadline theorem, not a broader allowed-deadline result. The exact
rational implementation in `profile_certificate.py` reproduces both
denominators and the final bound.
