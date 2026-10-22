from pathlib import Path
import datetime, hashlib, json, subprocess

ROOT=Path("/Users/alec/Documents/Math")
BASE=ROOT/"draft_pr_actual_claims_1100_1200_20261017/audits/pr1136_2307037"
OUT=BASE/"reviews/priority_analytic_01"
P=OUT/"sources/private"
now=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda name,obj: (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
queries=[
['"Eremenko" "Hamilton" "area distortion" Beurling quadrature','"Hayman" "7.37" poles','"Fuchs" "Macintyre" "squared" poles','"Beurling" "point masses" "weak"'],
['"Beurling-Ahlfors" "weak" "conjecture" sharp','"Fuchs-Macintyre" squared','"Hayman" "squared poles"','"squared-pole" integral'],
['"Beurling" "sharp logarithmic"','"Beurling" "positive measures"','"Fuchs" "Macintyre" "second"','"quadrature" "Hayman"'],
['"7.37" "Hamilton" "Hayman"','"7.37" "rational" "Hayman"','"Research Problems in Function Theory" "quadrature"','"squared" "poles" "Eremenko"'],
['"Fuchs-Macintyre" "sum"','"Sakai" "Quadrature Domains" positive measure existence 1982','"Properties of some balayage operators" quadrature','"Beurling" "exceptional set" "positive"'],
['"On the area distortion by quasiconformal mappings" "quadrature"','"On the area distortion by quasiconformal mappings" "Hayman"','"Macintyre" "Fuchs" "Inequalities for the Logarithmic" pdf','"Sakai" "Applications of variational inequalities" pdf'],
['"Eremenko" "Hamilton" "Beurling" "L log L"','"Beurling" "positive" "atomic measures"','"Cauchy" "second order" "point masses"','"Properties of some balayage operators" pdf'],
['"sharp" "Beurling" "indicator" Eremenko Hamilton','"Fuchs-Macintyre" lemma','"On the area distortion by quasiconformal mappings" "logarithmic"','"What is a quadrature domain" Gustafsson Shapiro pdf'],
[],
['"On the packing dimension of the Julia set" Bergweiler pdf','"Gustafsson" "Shapiro" "quadrature" "what" kth pdf','"Sakai" "Solutions to the obstacle problem as Green potentials" pdf','"Beurling" "LlogL" sharp estimate'],
['"Eremenko" "Hamilton" "singular integral" "quadrature"','"squared poles" mathematics','"Beurling" "finite positive" "measure"','"Beurling" "point masses" transform'],
['"Baernstein" "poles" "area"','"Baernstein" "rational functions" integral','"Beurling" "positive measures" -"Malliavin" -"algebras" -"algebra" -"LASSO" -"quasicrystals" -"Fourier"','"Hayman" "7.37" -harmonic -bulletin -calculus'],
['"Gustafsson" "Sakai" "1994" "balayage" filetype:pdf','"On the structure of partial balayage" pdf','"Sakai" "1983" "quadrature" "ams.org"'],
['"Analysis of the Ahlfors-Beurling operator" "quadrature"','"Some conjectures about integral means" "poles"','"Eremenko" "Hamilton" "Sakai" "Beurling"','"squared-pole sums"'],
[],[],
['"Beurling transform" "positive measures" sharp','"Beurling-Ahlfors" "positive" "weak-type constant"','"rational functions" "2π" "log R" Baernstein','"Cauchy transforms of point masses" "derivative"'],
[],[],
['"Quasiconvexity of the Burkholder function on symmetric"','"Yongxi Lin" "Two partial"','"two-partial-balayage-principles" "2026"'],
[]]
opens={
9:["https://people.kth.se/~gbjorn/","https://www.ams.org/tran/1983-276-01/S0002-9947-1983-0684507-2/"],
13:["https://www.sciencedirect.com/science/article/abs/pii/S1874570902800075"],
15:["https://arxiv.org/abs/0712.3378v2","https://arxiv.org/abs/1809.07200v2","https://arxiv.org/abs/math/9709215","https://arxiv.org/abs/2109.04555"],
16:["https://link.springer.com/chapter/10.1007/978-3-030-25165-9_7","https://link.springer.com/book/10.1007/978-3-030-25165-9","https://doi.org/10.1007/BF02790192"],
18:["https://coolrmal.github.io/articles/two-partial-balayage-principles/"],
21:["https://arxiv.org/abs/2608.23388v1","https://arxiv.org/html/2608.23388v1"]}
outcomes={
1:"EH primary located; no exact-target answer.",
2:"Radial weak-type/logarithmic leads; MF1940 publisher record.",
3:"Radial LlogL lead; unrelated results excluded.",
4:"Target references and quadrature leads; third-party final-book excerpt not primary evidence.",
5:"Sakai publisher record and LP ancestry; no exact result.",
6:"MF1940 exact citation; original fullbody request blocked.",
7:"Sjödin2007 partial-balayage primary publisher introduction.",
8:"EH citation context, Bergweiler MF restatement, author QD PDF lead.",
9:"KTH homepage404; AMS403.",
10:"Bergweiler author/arXiv fullbody and Osękowski multiplier primary PDFs.",
11:"No exact target; broad term collisions.",
12:"Exact target appears in third-party final-book excerpt; not used as final-edition evidence.",
13:"Sjödin primary partial text; EH2002 publisher excerpt; not fullbody.",
14:"No exact answer; title-level EH citation triage.",
15:"Primary arXiv version/date records.",
16:"HL2019 publisher metadata/preview only; Sakai DOI unavailable through web tool.",
17:"Lin partial-balayage BA weakconstant2 lead and Anderson–Eiderman first-order body.",
18:"Lin current author article inspected.",
19:"Lin PDF opened; reference anchor stayed on same page.",
20:"Guerra dated preprint identified; Lin project/search metadata.",
21:"Guerra versioned primary abstract and HTML."}
write("QUERY_LEDGER.json",{
"utc":now(),"search_cutoff_for_priority":"strictly before 2026-10-10; retrieval was2026-10-17",
"notice":"Actual queries/opens, not suggested searches. Web queries were unrestricted by date; discovered bodies were checked individually. Raw outputs remain ignored. Response save times are not asserted to be publication dates.",
"web_calls":[{"sequence":i,"search_queries":q,"open_urls":opens.get(i,[]),"clicks":([{"page":"Lin author article","link_id":3,"target":"author PDF"},{"page":"Lin author article","link_id":26,"target":"Guerra reference anchor"}] if i==19 else []),"raw_response_path":f"sources/private/web_queries_{i:02}.json","outcome":outcomes[i]} for i,q in enumerate(queries,1)],
"search_query_count":sum(map(len,queries)),
"direct_requests":{"receipts":[f"sources/private/retrieval_receipt_{i:02}.json" for i in range(1,5)]+["sources/private/lin_partial_balayage_receipt.json","sources/private/lin_historical_body_receipt.json"],
"index_gets":["https://api.openalex.org/works/https://doi.org/10.1090/S0002-9939-1995-1283548-8","https://api.openalex.org/works?filter=cites:W2117443136&per-page=200","https://api.github.com/repos/coolrmal/coolrmal.github.io/commits?path=assets/papers/two-partial-balayage-principles.pdf&per_page=100"],
"index_scope":"80 EH citing titles screened; not80 fullbody reviews; GitHub path-history contains one returned commit. No API-key/email enrollment requested."}})
sources=[
("eh1995_fresh.pdf","Eremenko–Hamilton","1995 journal, scanned author-hosted body","https://www.math.purdue.edu/~eremenko/dvi/hamilt.pdf","All5 extracted pages; visually p.2. Fullbody read. p.5 rendered, not separately image-inspected in this review."),
("lp2009_fresh.pdf","Levine–Peres","May1,2009 author manuscript","https://lionellevine.github.io/scalinglimit.pdf","Relevant passages/complete relevant pages6,12–17,54–55,58–59; visuals16,17,58,59; not whole74pages."),
("lp_arxiv_v2.pdf","Levine–Peres","v2 submitted2009-05-02T04:50:53Z","https://arxiv.org/pdf/0712.3378v2","Version/date/body identity; selected page comparison against author body. No full rereading of both versions."),
("hl_v2_fresh.pdf","Hayman–Lingham","v2 submitted2018-09-21T13:10:21Z","https://arxiv.org/pdf/1809.07200v2","PDFpp.172–173 / printed171–172 read and visually inspected."),
("log_radial.pdf","Adam Osękowski","Author-hosted manuscript of2013 radial logarithmic paper","https://www.mimuw.edu.pl/~ados/publications/papers/log_BA_radial.pdf","pp.1–3; p.3 visual; no complete proof audit."),
("llogl_multipliers.pdf","Adam Osękowski","Undated retrieved author manuscript; no exact historical dating claimed here","https://www.mimuw.edu.pl/~ados/publications/papers/LlogL_multipliers.pdf","pp.1–3; p.3 visual; exact symbol/applicability statement."),
("bergweiler2011.pdf","Walter Bergweiler","arXiv1101.3479v1,2011-01-18","https://arxiv.org/pdf/1101.3479v1","pp.4–5 read; p.4 visual; MF theorem is first-order. p.5 rendered but not image-inspected."),
("baernstein_montgomerysmith1997.pdf","Albert Baernstein II and Stephen J.Montgomery-Smith","arXivmath/9709215v1,1997-09-15","https://arxiv.org/pdf/math/9709215v1","pp.1–5 selected relevant passages; whole extracted text keyword triage; v2/final not read."),
("volberg2021.pdf","Oliver Dragičević","arXiv2109.04555v1,2021-09-09; retrieval basename was mistaken","https://arxiv.org/pdf/2109.04555v1","Selectedpp.20–22,29–31,59–61; whole text keyword triage; not77page full review."),
("guerra2026v1.pdf","André Guerra","arXiv2608.23388v1,2026-08-24T15:33:51Z","https://arxiv.org/pdf/2608.23388v1","pp.1–3 and§6 corollary proofspp.12–14; p.2 visual; not independent full16page referee verification."),
("lin_partial_balayage.pdf","Yongxi Lin","Current author-hosted PDF retrieved2026-10-17","https://coolrmal.github.io/assets/papers/two-partial-balayage-principles.pdf","Relevantpp.1–4; whole text keyword screen; p.4 visual via identical historical body."),
("lin_pre10oct.pdf","Yongxi Lin","Commitb9c28f7af5694bd44d0f19cb4f14b5f66225174e, author/committer metadata2026-10-05T10:49:12Z","https://raw.githubusercontent.com/coolrmal/coolrmal.github.io/b9c28f7af5694bd44d0f19cb4f14b5f66225174e/assets/papers/two-partial-balayage-principles.pdf","PDF identical SHA256 to current author PDF; relevantpp.1–4; p.4 visual. Repository metadata is not first-publication or independence proof.")]
srec=[]
for fn,author,version,url,scope in sources:
 f=P/fn
 srec.append({"private_path":f"sources/private/{fn}","author":author,"version":version,"url":url,"sha256":sha(f),"bytes":f.stat().st_size,"pdf_magic":f.read_bytes()[:5]==b"%PDF-","read_scope":scope,"extracted_text":{"path":f"sources/private/{f.stem}.txt","sha256":sha(f.with_suffix(".txt"))}})
# Independent page-content matching of relevant author/arXiv pages; not a PDF identity claim.
matches={}
for page in [6,12,13,14,15,16,17,54,55,58,59]:
 a=subprocess.run(["pdftotext","-f",str(page),"-l",str(page),str(P/"lp2009_fresh.pdf"),"-"],capture_output=True,text=True,check=True).stdout
 b=subprocess.run(["pdftotext","-f",str(page),"-l",str(page),str(P/"lp_arxiv_v2.pdf"),"-"],capture_output=True,text=True,check=True).stdout
 matches[str(page)]="".join(a.split())=="".join(b.split())
write("SOURCE_PINS.json",{"utc":now(),"sources":srec,
"lp_selected_page_text_comparison":{"normalization":"remove whitespace","pages":matches,"whole_pdf_identity_claim":False},
"fresh_matches_to_inherited":{"EH1995":sha(P/"eh1995_fresh.pdf")==sha(BASE/"sources/private/eh1995.pdf"),"LPauthor2009":sha(P/"lp2009_fresh.pdf")==sha(BASE/"sources/private/lp2009.pdf"),"HLv2":sha(P/"hl_v2_fresh.pdf")==sha(BASE/"sources/private/hl_v2.pdf")},
"unavailable_or_not_fullbody":[{"name":"MF1940","result":"Wiley direct PDF403; publisher bibliographic record only"},{"name":"Sakai1983","result":"First AMS URL returned200 HTML of Transactions index, notPDF; alternate/direct requests403"},{"name":"Sakai1984","result":"Springer PDF request returned HTML subscription page, notPDF"},{"name":"Sakai1982 and Gustafsson–Sakai1994","result":"Metadata/ancestral citations only; no fullbody obtained"},{"name":"Gustafsson–Shapiro QD survey","result":"Author PDF404; search excerpts used only as discovery leads"},{"name":"HL2019 final chapter","result":"Primary publisher preview/subscription gate; final problem fullbody not inspected"},{"name":"EH2002 and Sjödin2007","result":"Primary publisher excerpts/intro only; not fullbodies"},{"name":"LP2010 journal final; BM1997v2/final","result":"Not retrieved/read"}],
"private_evidence_manifest":[{"path":str(x.relative_to(OUT)),"sha256":sha(x),"bytes":x.stat().st_size} for x in sorted(P.iterdir()) if x.is_file()]})
initial=json.loads((OUT/"INPUT_PINS.json").read_text())
end={fn:{"sha256":sha(BASE/fn),"bytes":(BASE/fn).stat().st_size,"unchanged":sha(BASE/fn)==info["sha256"]} for fn,info in initial["files"].items()}
branch=subprocess.run(["git","branch","--show-current"],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
head=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
ignored=subprocess.run(["git","check-ignore","-v",str(P/"web_queries_01.json"),str(OUT/"tmp/lp2009_16.png")],cwd=ROOT,capture_output=True,text=True)
write("END_PINS.json",{"utc":now(),"input_files":end,"all_pinned_inputs_unchanged":all(x["unchanged"] for x in end.values()),"branch_at_end":branch,"head_at_end":head,"initial_head_not_captured":True,"git_mutations_performed":False,"ignored_private_control_returncode":ignored.returncode,"ignored_private_control_output":ignored.stdout.strip()})
with (OUT/"RESEARCH_LOG.md").open("a") as f:
 f.write(f"\n- {now()}: Checkpoint: dated Guerra2026v1 and commit-addressed Lin2026 body checked. Both give weakconstant2, not the target logarithmic coefficient. Complete older-input bridge independently verified. Prior exact-answer publication not found; no novelty/first-priority claim. Completion estimate:90%.\n")
print(json.dumps({"queries":sum(map(len,queries)),"all_inputs_unchanged":all(x["unchanged"] for x in end.values()),"lp_page_matches":matches,"branch":branch,"ignore_controls":ignored.returncode}))

