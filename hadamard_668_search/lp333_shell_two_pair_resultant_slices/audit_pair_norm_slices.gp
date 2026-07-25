\\ Exact nine-trit slice audit for the three pairwise resultant norms.
\\
\\ This constructs the repository's pinned F_(167^36) model without using
\\ floating point:
\\   * z is the image of X in F_167[X]/Phi_37;
\\   * omega is selected by the promoted FACTOR_PLUS;
\\   * alpha is reconstructed from promoted field_fixture(2).
\\
\\ Each channel slice varies three complete three-trit physical classes and
\\ fixes every other class to local option zero.  Thus every reported count
\\ is exact on 3^9 physical placements, not a random sample.

default(parisizemax, 2000000000);
default(parisize, 500000000);

p = 167;
n = 37;
T = Mod(polcyclo(n), p);
z = ffgen(T, 'z);
generator = ffprimroot(z);
om = generator^((p^36 - 1) / 3);

factor_plus_a = [1,62,5,121,113,15,114,119,111,121,111,119,114,15,113,121,5,62,1];
factor_plus_b = [0,123,0,79,44,35,44,79,44,79,44,79,44,35,44,79,0,123,0];
if(sum(i=0,18,(factor_plus_a[i+1]+factor_plus_b[i+1]*om)*z^i) != 0,error("the pinned omega/FACTOR_PLUS embedding changed"));

H = [1,10,26];
classes = vector(12,j,vector(3,k,(2^(j-1)*H[k])%n));
classof = vector(36);
for(j=1,12,for(k=1,3,classof[classes[j][k]]=j));

fixture(seed) =
{
  my(total = Mod(0,p)*z);
  my(a0=(17*seed+23)%p, b0=(31*seed+7)%p);
  total += a0+b0*om;
  for(c=1,36,
    my(j=classof[c]);
    my(a=(seed^2+11*(j-1)+3)%p);
    my(b=(7*seed+(j-1)^2+5)%p);
    total += (a+b*om)*z^c;
  );
  total;
};

alpha = fixture(2)^((p^12-1)/9);
if(alpha^3 == om^2, alpha=alpha^-1);
if(alpha^3 != om || alpha^9 != 1 || alpha^(p^6) != alpha || alpha^(p^3) != alpha^-1,error("the pinned ninth root changed"));

profiles = [[0,0,3],[0,1,2],[0,2,1],[0,3,0],[1,0,2],[1,1,1],[1,2,0],[2,0,1],[2,1,0],[3,0,0]];
profile_labels = ["h2-222222-0","h2-422220-0","h2-422220-1","h2-422220-2","h2-422220-3"];
canonical_a = [[2,5,8,1,7,9,5,8,5,5,5,7],[2,5,7,8,6,5,2,5,7,8,6,5],[2,8,8,5,5,5,2,8,8,5,5,5],[4,9,8,5,5,5,4,9,8,5,5,5],[8,5,4,5,9,1,6,8,5,5,2,6]];
canonical_b = [[2,5,3,6,5,5,5,4,7,5,4,7],[5,8,5,0,1,5,5,8,5,0,1,5],[2,5,5,4,1,3,2,5,5,4,1,3],[2,7,5,1,5,6,2,7,5,1,5,6],[2,3,5,5,1,5,1,4,7,5,5,5]];
astar_a = [[5,7,5,5,5,8,1,5,7,2,8,9],[1,5,8,7,4,5,1,5,8,7,4,5],[1,7,7,5,5,5,1,7,7,5,5,5],[6,9,7,5,5,5,6,9,7,5,5,5],[4,7,5,5,1,4,7,5,6,5,9,2]];

zero_a = [1,1,1,0,0,1,0,1,0];
zero_b = [1,1,1,1,0,0,1,0,0];
zero_value(ch) =
{
  my(word=if(ch==0,zero_a,zero_b));
  sum(r=0,8,word[r+1]*alpha^r);
};

actual(ch,j,pid) =
{
  my(v=profiles[pid+1]);
  my(high=if(ch==0,(j%2)==0,(j%2)==1));
  if(high,[3-v[1],3-v[2],3-v[3]],v);
};

term(count,residue,trit) =
{
  if(
    count==1,
    alpha^(residue-3*trit),
    if(count==2,-alpha^(residue+3*trit),Mod(0,p)*z)
  );
};

options(ch,j,pid) =
{
  my(v=actual(ch,j,pid),out=List());
  my(m0=if(v[1]==1||v[1]==2,3,1));
  my(m1=if(v[2]==1||v[2]==2,3,1));
  my(m2=if(v[3]==1||v[3]==2,3,1));
  for(t0=0,m0-1,for(t1=0,m1-1,for(t2=0,m2-1,
    listput(
      out,
      term(v[1],0,t0)+term(v[2],1,t1)+term(v[3],2,t2)
    )
  )));
  Vec(out);
};

periods = matrix(6,12,r,j,sum(k=1,3,(z^(p^(r-1)))^classes[j][k]));

rootset(ell) =
{
  my(rho=generator^((p^36-1)/ell),values=vector(ell));
  values[1]=Mod(1,p)*z^0;
  for(k=2,ell,values[k]=values[k-1]*rho);
  Set(values);
};

roots2 = rootset(2);
roots83 = rootset(83);
roots28057 = rootset(28057);
norm_exponent = (p^12-1)/(p^3-1);

label_triples_from_w(w) =
{
  my(nus=vector(3,r,(w[r]*w[r+3])^norm_exponent));
  [
    vector(3,r,setsearch(roots2,nus[r]^((p^3-1)/2))),
    vector(3,r,setsearch(roots83,nus[r]^((p^3-1)/83))),
    vector(3,r,setsearch(roots28057,nus[r]^((p^3-1)/28057)))
  ];
};

audit_slice(ch,ids) =
{
  my(opts=vector(12,j,options(ch,j-1,ids[j])));
  my(selected=List());
  for(j=1,12,
    if(#opts[j]==27 && #selected<3,listput(selected,j))
  );
  selected=Vec(selected);
  if(#selected!=3,error("a channel lacks three full three-trit classes"));

  my(base=vector(6,r,zero_value(ch)));
  for(j=1,12,for(r=1,6,base[r]+=opts[j][1]*periods[r,j]));

  my(delta=vector(3,k,vector(27,t,vector(
    6,r,(opts[selected[k]][t]-opts[selected[k]][1])*periods[r,selected[k]]
  ))));
  my(size=27^3);
  my(data2=vector(size),data83=vector(size),data28057=vector(size));
  for(index=0,size-1,
    my(q=index,w=vector(6,r,base[r]));
    for(k=1,3,
      my(choice=(q%27)+1);
      q=q\27;
      for(r=1,6,w[r]+=delta[k][choice][r]);
    );
    my(labels=label_triples_from_w(w));
    data2[index+1]=labels[1];
    data83[index+1]=labels[2];
    data28057[index+1]=labels[3];
  );
  [vector(3,k,selected[k]-1),data2,data83,data28057];
};

support_summary(data) =
{
  [
    vector(3,r,#Set(vector(#data,i,data[i][r]))),
    #Set(data)
  ];
};

match_count(left,right) =
{
  my(a=vecsort(left),b=vecsort(right),i=1,j=1,total=0);
  while(i<=#a && j<=#b,
    my(order=cmp(a[i],b[j]));
    if(
      order<0,
      i++,
      if(
        order>0,
        j++,
        my(ii=i+1,jj=j+1);
        while(ii<=#a && a[ii]==a[i],ii++);
        while(jj<=#b && b[jj]==b[j],jj++);
        total+=(ii-i)*(jj-j);
        i=ii;
        j=jj;
      )
    )
  );
  total;
};

match_summary(left,right) =
{
  [
    vector(3,r,match_count(
      vector(#left,i,left[i][r]),
      vector(#right,i,right[i][r])
    )),
    match_count(left,right)
  ];
};

print_channel(label,kind,result) =
{
  print(Str(
    "CHANNEL|",
    [label,kind,result[1],27^3,
     support_summary(result[2]),
     support_summary(result[3]),
     support_summary(result[4])]
  ));
};

print_pair(label,kind,left,right) =
{
  print(Str(
    "PAIR|",
    [label,kind,(27^3)^2,
     match_summary(left[2],right[2]),
     match_summary(left[3],right[3]),
     match_summary(left[4],right[4])]
  ));
};

run_all() =
{
  for(profile_index=1,5,
    my(a=audit_slice(0,canonical_a[profile_index]));
    my(b=audit_slice(1,canonical_b[profile_index]));
    my(s=audit_slice(0,astar_a[profile_index]));
    my(label=profile_labels[profile_index]);
    print_channel(label,"A",a);
    print_channel(label,"B",b);
    print_channel(label,"Astar-A",s);
    print_pair(label,"canonical-A-vs-B",a,b);
    print_pair(label,"Astar-A-vs-B",s,b);
  );
};

started=gettime();
run_all();
print(Str("SUMMARY|",["elapsed_milliseconds",gettime()]));
quit;
