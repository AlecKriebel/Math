#!/usr/bin/env python3
"""Independent rational finite checks and custody validation. No VOA theorem certificate."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import gzip
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / "private"
HEAD = "92652a37a6f0508ea34a0e8b14a7722c7d99530a"
BASE = "4b27092a448d53b61408355ce44ec38d103a1ce4"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def zeros(n):
    return [[Q(0) for j in range(n)] for i in range(n)]


def comm(a, b):
    n = len(a)
    return [[sum(a[i][k]*b[k][j]-b[i][k]*a[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def flatten(a):
    return [x for row in a for x in row]


def nullspace(rows, columns):
    a = [list(map(Q,row)) for row in rows if any(row)]
    pivots = []
    lead = 0
    for column in range(columns):
        pivot = next((i for i in range(lead,len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[lead],a[pivot] = a[pivot],a[lead]
        scale = a[lead][column]
        a[lead] = [v/scale for v in a[lead]]
        for i in range(len(a)):
            if i != lead and a[i][column]:
                scale = a[i][column]
                a[i] = [v-scale*w for v,w in zip(a[i],a[lead])]
        pivots.append(column)
        lead += 1
        if lead == len(a):
            break
    free = [j for j in range(columns) if j not in pivots]
    result = []
    for j in free:
        v = [Q(0)]*columns
        v[j] = Q(1)
        for i,k in enumerate(pivots):
            v[k] = -a[i][j]
        result.append(v)
    return result


def commuting_space(matrices):
    n = len(matrices[0])
    units = []
    for i in range(n):
        for j in range(n):
            u = zeros(n)
            u[i][j] = Q(1)
            units.append(u)
    rows = [[Q(i//n==i % n) for i in range(n*n)]]
    for a in matrices:
        images = [flatten(comm(u,a)) for u in units]
        rows += [list(r) for r in zip(*images)]
    vectors = nullspace(rows,n*n)
    return [[v[i*n:(i+1)*n] for i in range(n)] for v in vectors]


def triple(partition):
    n = sum(partition)
    e,f,h = zeros(n),zeros(n),zeros(n)
    offset = 0
    labels = []
    multiplicity = Counter(partition)
    seen = Counter()
    for d in partition:
        index = seen[d]
        seen[d] += 1
        for j in range(d):
            h[offset+j][offset+j] = d-1-2*j
            if j:
                e[offset+j-1][offset+j] = j*(d-j)
            if j < d-1:
                f[offset+j+1][offset+j] = 1
            labels.append((Q(d-1,2)-j,
                           Q(1 if index==0 else -1) if d==2 and multiplicity[d]==2 else Q(0),
                           d,j))
        offset += d
    require(comm(e,f)==h,"sl2 triple commutator")
    require(flatten(comm(h,e))==[2*v for v in flatten(e)],"h,e")
    require(flatten(comm(h,f))==[-2*v for v in flatten(f)],"h,f")
    permutation=sorted(range(n),key=lambda i:(-labels[i][0],-labels[i][1]))
    ordered=[labels[i] for i in permutation]
    e,f,h=([ [a[i][j] for j in permutation] for i in permutation] for a in [e,f,h])
    return e,f,h,ordered


# Exact ring Q(sqrt(3)); pairs represent a+b*sqrt(3).
def mul(x,y):
    a,b=x;c,d=y
    return (a*c+3*b*d,a*d+b*c)


def divide(x,y):
    a,b=y
    norm=a*a-3*b*b
    require(norm!=0,"nonzero quadratic denominator")
    return mul(x,(a/norm,-b/norm))


def pow_sqrt3(exponent):
    return (Q(3)**(exponent//2),Q(0)) if exponent % 2==0 else (Q(0),Q(3)**((exponent-1)//2))


def asymptotic_dimension(grades,n):
    exact_sine={Q(1,2):(Q(1),Q(0)),Q(1):(Q(0),Q(1)),
                Q(3,2):(Q(2),Q(0)),Q(2):(Q(0),Q(1))}
    numerator=(Q(1),Q(0))
    for grade,count in grades.items():
        if grade:
            require(grade in exact_sine,"positive known sine factor")
            for i in range(count):
                numerator=mul(numerator,exact_sine[grade])
    half=grades.get(Q(1,2),0)
    require(half % 2==0,"even half-degree dimension")
    denominator=mul((Q(2)**(half//2),Q(0)),pow_sqrt3(2*grades[0]+n-1))
    return numerator,denominator,divide(numerator,denominator)


def transpose(partition):
    return [sum(x >= i for x in partition) for i in range(1,max(partition)+1)]


def dominates(upper,lower):
    n=max(len(upper),len(lower))
    return sum(upper)==sum(lower) and all(sum(upper[:i])>=sum(lower[:i]) for i in range(1,n+1))


def trace_by_degree(x,t,grade=None):
    return sum((t[i]-t[j])**2 for i in range(len(x)) for j in range(len(x))
               if i!=j and (grade is None or x[i]-x[j]==grade))


def calculate(partition):
    n=sum(partition); p=n;q=3;k=-Q(n)+Q(p,q)
    require(math.gcd(p,q)==1 and p>=n,"ambient admissibility")
    require(k+n!=0,"noncritical ambient")
    e,f,h,labels=triple(partition)
    x=[v[0] for v in labels];t=[v[1] for v in labels]
    t_matrix=zeros(n)
    multiplicity_e,multiplicity_f=zeros(n),zeros(n)
    for i in range(n):
        t_matrix[i][i]=t[i]
        for j in range(n):
            if labels[i][2:]==labels[j][2:] and t[i]==1 and t[j]==-1:
                multiplicity_e[i][j]=1
                multiplicity_f[j][i]=1
    require(comm(multiplicity_e,multiplicity_f)==t_matrix,"actual multiplicity sl2 generators")
    for generator in [t_matrix,multiplicity_e,multiplicity_f]:
        require(all(not any(flatten(comm(generator,a))) for a in [e,f,h]),"multiplicity sl2 centralizes triple")
    grades=Counter(x[i]-x[j] for i in range(n) for j in range(i+1,n))
    require(sum(grades.values())==n*(n-1)//2 and min(grades)>=0,"complete positive root count")
    actual_centralizer=commuting_space([e,f,h])
    actual_f_centralizer=commuting_space([f])
    # Intersecting this ambient commutant with the triple centralizer requires
    # all triple matrices in the same list; this avoids an ambient double commutant.
    actual_center=commuting_space([e,f,h]+actual_centralizer)
    expected_triple=sum(c*c for c in Counter(partition).values())-1
    expected_f=sum(c*c for c in transpose(partition))-1
    require(len(actual_centralizer)==expected_triple,"actual triple centralizer dimension")
    require(len(actual_f_centralizer)==expected_f,"actual f centralizer dimension")
    require(len(actual_center)==len(Counter(partition))-1,"actual center dimension")
    # The multiplicity sl2 Cartan has normalized target norm2.
    ambient_norm=sum(v*v for v in t)
    traces=[trace_by_degree(x,t),trace_by_degree(x,t,Q(0)),trace_by_degree(x,t,Q(1,2))]
    ell=(k*ambient_norm+(traces[0]-traces[1]-traces[2])/2)/2
    require(ambient_norm==4 and ell==-Q(4,3),"induced affine level")
    require(ell+2==Q(2,3) and math.gcd(2,3)==1,"admissible noncritical affine sl2")
    dense=[3]*(n//3)+([n % 3] if n % 3 else [])
    require(dominates(dense,partition) and dense!=list(partition),"proper orbit closure membership")
    growth=Q(expected_f)-Q(n*(n*n-1),p*q)
    require(growth==2,"DS reduction growth")
    numerator,denominator,dimension=asymptotic_dimension(grades,n)
    require(dimension==(Q(0),Q(1,9)),"DS asymptotic dimension3^-3/2")
    left=sorted([-Q(j) for d in partition for j in range(d)],reverse=True)
    left_grades=Counter(left[i]-left[j] for i in range(n) for j in range(i+1,n))
    require(asymptotic_dimension(left_grades,n)[2]==dimension,"Dynkin/left-adjusted dimension")
    g0=n-1+2*grades[0];ghalf=grades.get(Q(1,2),0)
    rho=[Q(n-1,2)-i for i in range(n)]
    shifted_norm=sum((r-(k+n)*v)**2 for r,v in zip(rho,x))
    central_charge=g0-Q(ghalf,2)-12*shifted_norm/(k+n)
    require(central_charge==-6,"Dynkin central charge")
    if n==7:
        z=[Q(4) if item[2]==3 else Q(-3) for item in labels]
        znorm=sum(v*v for v in z);zt=[trace_by_degree(x,z),trace_by_degree(x,z,0),trace_by_degree(x,z,Q(1,2))]
        zlevel=k*znorm+(zt[0]-zt[1]-zt[2])/2
        positive_trace=sum(z[i]-z[j] for i in range(n) for j in range(n) if x[i]>x[j])
        require(sum(z)==0 and zlevel==0 and positive_trace==0 and sum(v*w for v,w in zip(x,z))==0,
                "extra center zero form/self-duality trace")
        require(divide(numerator,pow_sqrt3(2*grades[0]+n-1))!=dimension,
                "missing half-grade sine denominator negative control")
        extra={"norm":str(znorm),"traces":list(map(str,zt)),"form":str(zlevel)}
    else:
        require(len(actual_center)==0 and len(actual_centralizer)==3,"m0 has exactly sl2 and no center")
        extra=None
    # Negative controls must disagree with the genuine finite values.
    require((k*ambient_norm+(traces[0]-traces[1])/2)/2!=ell if n==7 else True,
            "omitted half-grade term negative control")
    require(len(actual_center)!=1 if n==4 else True,"spurious m0 scalar negative control")
    return {"n":n,"p":p,"q":q,"k":str(k),"partition":partition,"dense_partition":dense,
            "Dynkin_x":list(map(str,x)),"Cartan_t":list(map(str,t)),
            "Dynkin_positive_root_grades":{str(a):b for a,b in sorted(grades.items())},
            "left_adjusted_positive_root_grades":{str(a):b for a,b in sorted(left_grades.items())},
            "triple_centralizer_dimension":len(actual_centralizer),"center_dimension":len(actual_center),
            "f_centralizer_dimension":len(actual_f_centralizer),"full_zero_half_traces":list(map(str,traces)),
            "affine_level":str(ell),"asymptotic_weight":0,"asymptotic_growth":str(growth),
            "asymptotic_dimension_Qsqrt3":list(map(str,dimension)),
            "g0_dimension":g0,"g_half_dimension":ghalf,"rho_shift_squared":str(shifted_norm),
            "central_charge":str(central_charge),"extra_center":extra}


def binding():
    pr=json.loads((PRIVATE/"pr.json").read_text());b=json.loads((ROOT/"PR_BINDING.json").read_text())
    require(pr["head"]["sha"]==HEAD and pr["base"]["sha"]==BASE,"exact PR pins")
    require(pr["state"]=="open" and pr["draft"],"captured OPEN draft")
    require(digest(pr["body"].encode())==b["body_sha256"],"body pin")
    final=json.loads((ROOT/"FINAL_PR_RECHECK.json").read_text())
    require(final["head"]==HEAD and final["base"]==BASE and final["state"]=="open" and
            final["draft"] and final["changed_files"]==8 and final["body_sha256"]==b["body_sha256"],
            "final PR head/body/scope recheck")
    files=json.loads((PRIVATE/"files.json").read_text())
    require(len(files)==8 and all(f["status"]=="added" for f in files),"8 added files")
    require(not any("QUEUE" in f["filename"] for f in files),"no QUEUE edit")
    for pin in b["eight_blobs"]:
        data=(PRIVATE/Path(pin["path"]).name).read_bytes()
        require(len(data)==pin["bytes"] and digest(data)==pin["sha256"],"public blob digest")
        require(hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==pin["git_blob_sha"],"Git blob pin")
    manifest=json.loads((PRIVATE/"MANIFEST.json").read_text())
    require(sorted(manifest["members"])==sorted(Path(f["filename"]).name for f in files),"manifest members")
    for pin in manifest["entries"]:
        data=(PRIVATE/pin["file"]).read_bytes()
        require(len(data)==pin["bytes"] and digest(data)==pin["sha256"],"manifest digest")
    for pin in json.loads((ROOT/"PRIMARY_RECEIPT.json").read_text())["sources"]:
        if "error" in pin:
            continue
        if pin.get("storage_encoding")=="gzip":
            data=gzip.decompress((ROOT/pin["stored_path"]).read_bytes())
        else:
            data=(PRIVATE/pin["name"]).read_bytes()
        require(len(data)==pin["bytes"] and digest(data)==pin["sha256"],"source body pin")
    expected={"original.pdf":"b33ed36eaa470877bc6cfb5b45b1019564f568925ea9d94e8dc7ee355879976e",
              "arxiv_v3.pdf":"2349653f92ebfa2499ad28e82aaba943ddca51b9da95b2231fb052692cc64cfc",
              "published.pdf":"882e6fc9af404f7d5c1c5816e24c0b046753b394c4f7a899f301903df0b0726f"}
    for name,h in expected.items():
        require(digest((PRIVATE/name).read_bytes())==h,"independent exact source pin")
    for name,count in [("original.txt",66),("arxiv_v3.txt",92),("published.txt",92)]:
        require(len((PRIVATE/name).read_text().split("\f"))-1==count,"extracted PDF page count")
    g=json.loads((ROOT/"GWS_CLEARANCE.json").read_text())
    require(g["numeric_gid"]==1254632077 and g["requested_columns"]==43 and g["rows_including_header"]==191,"fresh numeric full-width GWS")
    require(digest((PRIVATE/"GWS_FULL43.json").read_bytes())==g["sha256"] and not g["unresolved_duplicate_leads"],"duplicate clearance")
    crossref=json.loads((PRIVATE/"crossref.json").read_text())["message"]
    require(crossref["DOI"]=="10.1017/fms.2024.81" and crossref["volume"]=="12" and crossref["article-number"]=="e95","journal identity")
    require([a["family"] for a in crossref["author"]]==["Arakawa","van Ekeren","Moreau"],"author identity")
    require(crossref["published-online"]["date-parts"]==[[2024,11,8]],"online publication date")
    require((ROOT/"PRIVATE_BODY_SEAL.json").exists(),"required private body seal")
    for pin in json.loads((ROOT/"PRIVATE_BODY_SEAL.json").read_text())["private_files"]:
        data=(ROOT/pin["path"]).read_bytes()
        require(len(data)==pin["bytes"] and digest(data)==pin["sha256"],"private seal")
    proposal=json.loads((ROOT/"LITERAL_FOUR_CELL_PROPOSAL.json").read_text())
    require(len(proposal["literal_cells"])==4 and proposal["literal_cells"][1]=="", "four literal cells; blankB")
    require(proposal["literal_cells"][2]=="https://doi.org/10.1017/fms.2024.81" and
            proposal["status"]=="PROPOSAL_ONLY_NOT_APPENDED","existing DOI; accounting incomplete")
    return {"head":HEAD,"base":BASE,"blobs":8,"tracker_rows":191,"published_DOI":"10.1017/fms.2024.81"}


if __name__=="__main__":
    cases=[calculate([3,2,2]),calculate([2,2])]
    require(cases[0]["f_centralizer_dimension"]!=cases[1]["f_centralizer_dimension"],
            "distinct universal associated slice dimensions")
    require(Q(-4,3)*3/(Q(-4,3)+2)==-6,"affine c")
    require((1-Q(2,2*3))*3==2,"affine growth")
    # Affine A: 2 / (3*sqrt(12)) = sqrt(3)/9 exactly.
    require(divide((Q(2),Q(0)),(Q(0),Q(6)))==(Q(0),Q(1,9)),"affine dimension")
    print(json.dumps({"status":"PASS","bindings":binding(),"cases":cases,
                      "negative_controls_rejected":["orbit equals dense orbit","extra scalar at m0",
                        "omit half-integral trace term","omit half-grade sine denominator",
                        "universal-W equality from distinct slice dimensions"],
                      "mathematical_limit":"Finite algebra only; imported VOA/affine character theorems are not machine-proved.",
                      "source_author_code_executed":False,"service_writes":False},indent=2))
