#!/usr/bin/env python3
"""Pure offline editorial custody plus tiny in-memory scope controls.

No subprocess, network, writes, old content verifier or scientific campaign.
Controls illustrate already-cleared distinctions, not another science family.
"""
from fractions import Fraction as F
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re

OWN=Path(__file__).resolve().parent
P=OWN.parent.parent
EXCLUDED={"OWNED_MANIFEST.json","FINAL_SEAL.json","CLOSURE_RESULTS.json"}


def data(f):return json.loads(f.read_text())
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def strict(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(strict(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


guard=data(OWN/"INPUT_MANIFEST.json")
for row in guard["protected_preexisting_files"]:
    f=Path(row["absolute_path"])
    require(f.is_file() and not f.is_symlink() and f.stat().st_size==row["bytes"] and sha(f)==row["sha256"],"Protected file changed: "+str(f))
literal=data(OWN/"WHOLE_LITERAL_INPUT_VERDICTS.json")
for rid,record in literal.items():
    q=P/"papers"/rid
    for row in record["raw_copies"]:
        require((OWN/row["raw_copy"]).read_bytes()==Path(row["source"]).read_bytes(),"Whole raw input copy changed")
    for lane,item in record["whole_three_literal_scientific_verdicts"].items():
        original=q/"reviews"/lane/"VERDICT.json"
        require((OWN/item["raw_byte_copy"]).read_bytes()==original.read_bytes(),"Raw whole scientific verdict changed")
        require(strict(item["whole_literal_original"],data(original)),"Literal verdict type/order/value changed")
    require(strict(record["whole_original_editorial_verdict"],data(q/"reviews/editorial/VERDICT.json")),"Whole editorial verdict changed")


class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.abstract_active=False;self.abstract=[];self.meta={};self.canonical=[];self.script_types=[];self.in_ld=False;self.ld=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="p" and a.get("id")=="original-abstract":self.abstract_active=True
        if tag=="meta" and a.get("name"):self.meta[a["name"]]=a.get("content")
        if tag=="link" and a.get("rel")=="canonical":self.canonical.append(a.get("href"))
        if tag=="script":
            self.script_types.append(a.get("type"));self.in_ld=a.get("type")=="application/ld+json"
    def handle_endtag(self,tag):
        if tag=="p":self.abstract_active=False
        if tag=="script":self.in_ld=False
    def handle_data(self,s):
        if self.abstract_active:self.abstract.append(s)
        if self.in_ld:self.ld.append(s)


def white(s):return re.sub(r"\s+","",s)
def abstract(tex):return tex.split(r"\begin{abstract}",1)[1].split(r"\end{abstract}",1)[0].strip()
def norm117(s):
    s=s.replace(r'K\"ahler',"Kähler").replace("--","–").replace("–","-").replace("−","-")
    s=s.replace(r"\OO","O").replace(r"\PP^1","P1").replace("ℙ¹","P1")
    s=s.replace(r"\times","×").replace(r"\oplus","⊕").replace(r"\simeq","≃").replace(r"\log","log")
    s=s.replace("$","").replace("{","").replace("}","")
    s=re.sub(r"e\^\((-?2t)\)",r"e^\1",s)
    return white(s)


for rid,date in [("23149775","2026-10-04"),("23331080","2026-10-12")]:
    q=P/"papers"/rid;cfg=data(q/"publication/promotion/promotion.json");state=cfg["state"]
    for key,value in state.items():
        if key=="private_editorial_complete":require(value is True,"Private editorial completion changed")
        elif key in ["root_editorial_adoption","canonical_url","AA"]:require(value is None,"Premature adoption/canonical/AA")
        else:require(value is False,"Premature public gate")
    require(cfg["science"]["follow_up"] is None,"Unsupported follow-up")
    h=Page();h.feed((q/"publication/promotion/page.html").read_text())
    require(not h.canonical and h.meta["robots"]=="noindex,nofollow","Private canonical/robots changed")
    require(h.script_types==["application/ld+json"],"Scientific body depends on an unapproved script")
    require(h.meta["citation_publication_date"]==date.replace("-","/") and h.meta["citation_doi"]=="10.5281/zenodo."+rid,"Citation metadata changed")
    plain=(q/"publication/promotion/abstract.txt").read_text()
    require(white("".join(h.abstract))==white(plain),"Whole visible/standalone abstract mismatch")
    ready=data(q/"sources/SOURCE_READY.json");texrow=ready["controlling_TeX"]
    texpath=Path(texrow["path"] if "path" in texrow else texrow["extracted_path"])
    src=abstract(texpath.read_text());saved=(q/"reviews/editorial/ORIGINAL_ABSTRACT.tex").read_text().strip()
    require(src==saved,"Exact original abstract TeX substring changed")
    require((white(src)==white(plain)) if rid=="23149775" else (norm117(src)==norm117(plain)),"Full original abstract transcription changed")
    ld=json.loads("".join(h.ld))
    require(ld["datePublished"]==date and ld["version"]=="1.0" and ld.get("url") is None,"Scholarly date/version/private URL changed")
    if rid=="23331080":require(white(ld["abstract"])==white(plain),"Whole Kähler scholarly abstract changed")

focal=data(P/"papers/23149775/publication/promotion/promotion.json")
require(focal["science"]["domain"]["primitive_N_upper_bound"] is None and focal["science"]["domain"]["star_orbits"] is True,"All-period/star scope narrowed")
require(focal["science"]["C0_phase_independent"] is True and focal["science"]["common_focal_ratio_phase_constant_claimed"] is False,"Multiplier/focal-ratio conflation")
require(focal["source"]["paper_prose_license"]=="CC BY 4.0" and focal["source"]["original_code_license"]=="MIT","Focal mixed licenses changed")
kahler=data(P/"papers/23331080/publication/promotion/promotion.json")
require(kahler["source"]["separate_code_license"] is None and kahler["source"]["license_original"]=={"id":"cc-by-4.0"},"Invented Kähler software license")
require(kahler["science"]["source_equation13_vs_literal_equation14_distinction_retained"] is True and kahler["credit"]["specific_2025_Naumann_habilitation_body_recovered"] is False,"Kähler source/priority qualification lost")

controls=[]
# Readable control from the CLEARED triangle certificate, not a new projection campaign.
ratio=F(7*625,10*84)
require(ratio==F(125,24),"Triangle common multiplier algebra changed")
require(7*7*21-5==1024 and 7*7*21>5,"Triangle positive radical denominator changed")
controls.append({"family":"Fixed multiplier versus variable focal ratio","certificate":"B±/A±=7*625/(10*84)=125/24. For T=7sqrt21,s=sqrt5, T²-s²=1024>0: (T+s)/(T-s)>1 and inversion yields its unequal reciprocal.","limit":"Already-cleared exact triangle algebra, not a new geometry/reflection proof."})

def area(poly):
    return sum(F(poly[i][0])*poly[(i+1)%len(poly)][1]-F(poly[i][1])*poly[(i+1)%len(poly)][0] for i in range(len(poly)))/2
triangle=[(0,0),(2,0),(0,1)]
require(area(triangle)==1 and area(list(reversed(triangle)))==-1 and area(triangle*3)==3,"Signed reversal/repetition changed")
require(area([(0,0),(2,2),(0,2),(2,0)])==0,"Signed bow-tie control changed")
controls.append({"family":"Signed cyclic area","certificate":"An oriented triangle reverses sign and triple traversal triples its area; a bow-tie has algebraic area0 while its two unsigned lobes have total2.","limit":"Definition control, not a billiard counterexample."})

line_foot=(F(0),F(0));clamped=(F(1),F(0))
require(line_foot!=clamped,"Supporting-line/segment control changed")
controls.append({"family":"Supporting lines versus clamped segments","certificate":"Project F=(0,2) onto line through (1,0),(2,0): foot(0,0); clamping gives(1,0).","limit":"Elementary construction distinction, not an extension of the theorem."})

e=F(1,96);d=F(1,4);pole=lambda y:e-(1-y)/24
require(pole(F(1))==e and pole(F(3,4))==0 and pole(F(1,2))==-e,"Exact Kähler witness changed")
controls.append({"family":"Exact finite Kähler witness","certificate":"With y=exp(-2t), pole(1)=1/96, pole(3/4)=0, pole(1/2)=-1/96.","limit":"No finite check is used to prove the all-finite-time PDE theorem."})

require(F(2)-F(2)==0 and F(2)*2-F(2)==2,"Stationary-product reaction calibration changed")
require(-d/3==-F(1,12) and e>0,"Normalization mean term diagnostic changed")
controls.append({"family":"Declared flow and quantifier boundary","certificate":"Stationary product: reaction1 gives2-2=0, same-weight reaction2 gives4-2=2. Omitting the mean changes the initial pole derivative from-1/12 to+1/96. A positive stationary product prevents a claim that every initial metric loses positivity.","limit":"Small normalization/quantifier control from cleared identities; no new source/PDE campaign."})

if (OWN/"OWNED_MANIFEST.json").exists():
    manifest=data(OWN/"OWNED_MANIFEST.json");actual={str(f.relative_to(OWN)) for f in OWN.rglob("*") if f.is_file() and str(f.relative_to(OWN)) not in EXCLUDED}
    require(actual=={x["relative_path"] for x in manifest["files"]},"Owned inventory changed")
    for row in manifest["files"]:
        f=OWN/row["relative_path"];require(f.stat().st_size==row["bytes"] and sha(f)==row["sha256"],"Owned audit bytes changed")
if (OWN/"FINAL_SEAL.json").exists():
    seal=data(OWN/"FINAL_SEAL.json")
    for key,name in [("owned_manifest_sha256","OWNED_MANIFEST.json"),("input_manifest_sha256","INPUT_MANIFEST.json"),("report_sha256","REPORT.md"),("verdicts_sha256","VERDICTS.json"),("closure_result_sha256","CLOSURE_RESULTS.json")]:require(seal[key]==sha(OWN/name),"Final seal mismatch")
print(json.dumps({"status":"PASS_PURE_OFFLINE_FOCAL_KAHLER_EDITORIAL_CUSTODY","protected_preexisting_files":len(guard["protected_preexisting_files"]),"whole_scientific_verdicts":6,"whole_editorial_verdicts":2,"full_original_abstracts":2,"small_inmemory_control_families":len(controls),"controls":controls,"new_blind_scientific_family":False,"legacy_content_or_science_programmes_network_subprocess_or_writes":False,"root_adoption_or_publication_AA_authority":False},indent=2))
