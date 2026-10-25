"""Bind only raw supplied primary PDFs and own ignored reading extractions."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=ROOT/"papers/23442760/reviews/scope/cache/primary"
ROWS=[
    ("Slot–Laurent",BASE/"slot-laurent-v2.pdf",573575,"c8aebdfc6a1b6a65dbdebbea6b31edfcb4e4bd711d4fc80077a2485bd7e6764a","https://arxiv.org/pdf/1905.08142v2","slot-laurent-v2.txt","Exactly arXiv v2, 2020-01-30","Eq.(3), Lemmas1/4, Section4 and Theorem11, concluding open questions"),
    ("Laurent–Slot final overview",BASE/"laurent-slot-overview-final.pdf",590891,"5c90a15edce772e7d653704fa413c6fd97eb46a83289c1a9140c77c4836d61f8","https://ir.cwi.nl/pub/36052/36052.pdf","overview-final.txt","Actual final 2026 chapter, printed149–176","normalized hierarchy context, Table1 and surrounding discussion, Section2.4 Eq.(24) restrictive hierarchy"),
    ("de Klerk–Laurent annealing",BASE/"deklerk-laurent-annealing-v1.pdf",776201,"d5a7d1655545535ec7758fd4fbabe7985d6597a6321f318c8630c27a0bf21000","https://arxiv.org/pdf/1703.00744v1","annealing-v1.txt","Exactly arXiv v1","Corollary4.3 statement and quadratic-upper-estimator proof"),
    ("de Klerk–Laurent worst cases",BASE/"deklerk-laurent-worst-v1.pdf",240593,"fa7a1c702e96ae42070c59dd38ca2b7afa09bd5052aba190f0985b90239e9207","https://arxiv.org/pdf/1804.05524v1","worst-v1.txt","Exactly arXiv v1","Theorem3.1 and Corollaries3.2/3.3: root/eigenvalue link, Theta lower rate and products"),
    ("Totik–Varga",BASE/"totik-varga-published.pdf",285373,"004361b85bbaef05716c7789a108b9b764e3e7789ba22724a029e9ee5429a7a9","https://www.math.u-szeged.hu/pot/5fdp.pdf","totik-varga.txt","Actual journal-layout2012 body,13pp","Theorem2.1 statement and hypotheses (also rendered p.379); proof of Theorem3.1 shell/core comparison, especially(3.10)–(3.13)"),
    ("Laurent2018 OWR",ROOT/"papers/23181280/reviews/scope/cache/primary/kaibel-owr2018-50.pdf",590481,"a90207e0cadc310ab5a52a228c4b25a16f5e5f617542f006e9909cf90d4c72d2","https://ems.press/content/serial-article-files/46772?nt=1","owr2018.txt","Actual56pp publisher report50/2018","Complete Laurent contribution printed2991–2993; p.2991 normalization displays visually inspected"),
]

if __name__=="__main__":
    objects=[]
    for label,pdf,size,expected,url,text,edition,passages in ROWS:
        data=pdf.read_bytes()
        assert len(data)==size and sha256(data).hexdigest()==expected
        extraction=HERE/"replay-work/primary"/text
        body=extraction.read_bytes()
        objects.append({"label":label,"path":str(pdf),"bytes":size,"sha256":expected,
                        "acquisition_url":url,"edition":edition,"passages_independently_inspected":passages,
                        "own_ignored_extraction":str(extraction),"extraction_bytes":len(body),
                        "extraction_sha256":sha256(body).hexdigest()})
    renderings=[]
    for name in ["owr-normalization.png","totik-theorem.png"]:
        path=HERE/"replay-work/primary"/name;data=path.read_bytes()
        renderings.append({"path":str(path),"bytes":len(data),"sha256":sha256(data).hexdigest(),"visually_inspected":True})
    receipt={"utc":datetime.now(timezone.utc).isoformat(),"status":"RAW_PRIMARY_OBJECTS_ONLY_INDEPENDENTLY_INSPECTED_AFTER_EARLY_SEAL",
             "raw_supplier":"sol_three_pdf_download_finish","supplier_opinions_received":False,
             "objects":objects,"renderings":renderings,
             "foreign_full_text_all_preignored":True,
             "ignore_evidence":".gitignore /papers/*/reviews/*/replay-work/ verified before own extractions/rendering; raw supplier cache separately preignored.",
             "access_limits":["Specified preprint editions used for Slot–Laurent and deKlerk–Laurent; no publisher/preprint byte-equivalence assertion.","Author-hosted actual final overview and actual published-layout Totik–Varga read.","OWR actual publisher PDF reused unchanged from prior raw source lane; checksum independently verified.","Relevant primary interfaces inspected, not all proofs in all six papers.","No exhaustive priority/current-worldwide-openness search; no claim of absence of earlier or later equivalent results."]}
    target=HERE/"PRIMARY_INTERFACES.json"
    if target.exists():raise RuntimeError("Refusing evidence overwrite")
    target.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("Six actual primary objects and two visual inspections bound.")
