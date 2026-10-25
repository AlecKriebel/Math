"""Bind raw supplied primary texts and independent reading scope only."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

HERE=Path(__file__).resolve().parent
PAPER=HERE.parents[1]
ROWS=[
 ("bpt-arxiv.pdf","bpt.txt","eda67be8b0f5fa60cb2060af4ce71c70136449ea6bec6c8386f84e05675e62d0","Actual arXiv1801.09868v1; body has internal date6Nov2018, header30Jan2018","Definition3.1/Remark3.2, Theorem4.4 and strong-stability definition, Conjecture5.7, Theorem6.2, Theorem6.6 statement; printed7 visually inspected"),
 ("conca.pdf","conca.txt","3080e4190c38f9b24d018bb05a303d32c4608445fe57776b0e001c894df7c287","Actual arXiv math/0210064v1","Infinite-field setup and complete Lemma1.2 statement/proof"),
 ("migliore-nagel-v1.pdf","mn.txt","95e53b96441cc4c1caaa5ba1f1eec80b3cb1581c02fd44f181ff76b6d4deb9d5","Exactly arXiv2508.12113v1,2025","Section2 definition of Jac(f)^top; Section8.2 hypothesis, Theorem8.11 and Corollary8.12"),
 ("tohaneanu-v2.pdf","tohaneanu.txt","693f4fd933adc816cecc87c59258d060f5d3c61b5de24358dd8313d67ad91d02","Exactly arXiv1405.2122v2,2015","Section2.1 linear logarithmic derivation/eigenvector mechanism and explicit Orlik–Terao attribution"),
 ("falk-proudfoot-v2.pdf","fp.txt","9df58c61ffef11da684b26bd8e709a6a2ee60437f9b42147c86164696e3a91fb","Exactly arXiv math/0002094v2","Section4 common-coordinate construction, point-flat parallel connection and Theorem4.1"),
 ("owr2021-5.pdf","owr.txt","1549890c7373abbbd4e17ff3bf1895d80c321c74e17e43e4e46ceee3fb83f1a8","Actual76pp publisher report5/2021","Conjecture7 printed234 and surrounding arrangement/rank-three discussion; printed234 visually inspected"),
 ("mpt-final.pdf","mpt.txt","c34c76d72c9373c68e678a611fb6a5052c857d22eb844c10519a415732b0e813","Actual EMS published text Port.Math.83(2026),1–18, copyright2025","Section4 Jacobian definition, Conjecture4.6, Theorem4.7 rank-three case and relation to Corollary3.8"),
 ("pt2020.pdf","pt2020.txt","8213aed90bdbf2d5dc34a8495de110a22fb0bd555301b9efc2b21eb93a2cda81","Actual HUSCAP manuscript version, repository cover identifies journal555(2020),289–304","Repository edition notice and Conjecture7.9 with surrounding text"),
 ("pt2022.pdf","pt2022.txt","a28f8a39dd2277944ce39f49e1be9da688c1f16e68cde0da5d2401cc0ec82d03","Actual HUSCAP manuscript version, repository cover identifies journal590(2022),215–233","Repository edition notice and Conjecture7.9 with surrounding text"),
]

if __name__=="__main__":
    transport=json.loads((PAPER/"reviews/scope/primary-fetch-receipts.json").read_text())
    objects=[]
    for pdf,text,expected,edition,scope in ROWS:
        row=next(item for item in transport if Path(item.get("path","")).name==pdf)
        data=Path(row["path"]).read_bytes()
        assert len(data)==row["bytes"] and sha256(data).hexdigest()==expected==row["sha256"]
        assert data.startswith(b"%PDF-") and row["status"]==200
        extracted=HERE/"replay-work/primary"/text;body=extracted.read_bytes()
        objects.append({"path":row["path"],"bytes":len(data),"sha256":expected,"requested_url":row["requested_url"],
                        "final_url":row["final_url"],"edition":edition,"passages_independently_inspected":scope,
                        "ignored_extraction":str(extracted),"extraction_bytes":len(body),"extraction_sha256":sha256(body).hexdigest()})
    renderings=[]
    for name in ["bpt-conjecture.png","owr-conjecture.png"]:
        path=HERE/"replay-work/primary"/name;data=path.read_bytes()
        renderings.append({"path":str(path),"bytes":len(data),"sha256":sha256(data).hexdigest(),"visually_inspected":True})
    target=HERE/"PRIMARY_INTERFACES.json"
    if target.exists():raise RuntimeError("Refusing evidence overwrite")
    target.write_text(json.dumps({"utc":datetime.now(timezone.utc).isoformat(),"status":"INDEPENDENT_PRIMARY_INTERFACES_AFTER_EARLY_SEAL",
        "raw_supplier":"sol_three_pdf_download_finish","evaluative_conclusions_supplied_or_read":False,
        "objects":objects,"renderings":renderings,
        "Ilardi_access":{"institutional_url":"https://www.iris.unina.it/handle/11588/726226",
                         "independently_opened_web_record":True,"file_listing":"Authorized users only; private/restricted access",
                         "full_body_obtained":False,"request_copy_or_external_outreach":False},
        "original_Galligo_Burch_Orlik_Terao_bodies_acquired":False,
        "classical_interfaces_used":"Galligo/strong stability stated explicitly in BPT Theorem4.4; revlex section identity in BPT Theorem6.2 and Conca Lemma1.2; classical graded Hilbert–Burch applied in its stated two-variable height-two setting, with an exact independent finite certificate check.",
        "foreign_text_preignored":"Root .gitignore /papers/*/reviews/*/replay-work/ verified before own writes; raw primary cache preignored by supplier.",
        "novelty_limit":"No exhaustive historical/current-openness search or first-disclosure authentication. Original Ilardi body unavailable; relevant predecessor cannot be ruled out from its abstract."},indent=2,ensure_ascii=False)+"\n")
    print("Nine raw primary PDFs, exact editions/passages and two visual source checks bound.")
