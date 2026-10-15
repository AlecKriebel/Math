#!/usr/bin/env python3
"""Fetch primary bytes, authenticate identities, render temporary selected pages, retain no source text."""
from pathlib import Path
import hashlib, json, subprocess, urllib.request
ROOT=Path(__file__).resolve().parent
TMP=ROOT/"tmp"/"pdfs"
TMP.mkdir(parents=True,exist_ok=True)
sources=[
 ("k3","https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf","ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f",[167,168]),
 ("bs","https://msp.org/gt/2018/22-7/gt-v22-n7-p13-p.pdf","8878155672962cf4fd6489b3f6f4e7d1dcf889108f3caf692319de3c42f85c15",[47,49]),
 ("bascape2026","https://arxiv.org/pdf/2608.20551v1","e1c97c5fdd295379f2c92271aee50af6f195d7b1fe9c00661d3d91040537a484",[5,9]),
 ("li_ye2025","https://arxiv.org/pdf/2511.17877v1","3b88dc67d7c71df68b2ac67e3a827615332fd2285cdc13fa4669e83a7b75b9b9",[32]),
 ("bascape2024","https://arxiv.org/pdf/2408.16635v2","e7fea7edce809d7003b81bc5d8d2ea5436bf04bc8cf38c1026c80c309e65c752",[1,3,38]),
 ("sivek_zentner","https://spiral.imperial.ac.uk/server/api/core/bitstreams/31fba2ba-24ed-45cb-9374-dad47877adcc/content","ca374df2576d443ec8e6e057ee218ca250ae0e4156be2e9dcb990eabe5f052df",[14]),
 ("bs_author","https://www.ma.imperial.ac.uk/~ssivek/papers/stein_fillings.pdf","a239ca5e167b91c51c0c8fb9f44c200039b5d47b9a243007d2a94482431d7f93",[])
]
results=[]
for label,url,expected,pages in sources:
    try:
        with urllib.request.urlopen(url,timeout=45) as response: b=response.read(); final_url=response.url
        sha=hashlib.sha256(b).hexdigest()
        assert b.startswith(b"%PDF-")
        assert sha==expected,(label,sha)
        record={"label":label,"url":url,"final_url":final_url,"bytes":len(b),"sha256":sha,"expected_hash_matches":True,"selected_pdf_pages":pages}
        if pages:
            pdf=TMP/(label+".pdf");pdf.write_bytes(b)
            for page in pages:
                prefix=TMP/(label+"_page_"+str(page))
                subprocess.run(["/opt/homebrew/bin/pdftoppm","-f",str(page),"-l",str(page),"-r","110","-png","-singlefile",str(pdf),str(prefix)],capture_output=True,check=True)
            pdf.unlink()
        results.append(record)
    except Exception as error:
        results.append({"label":label,"url":url,"error":repr(error),"authenticated":False})
out={"sources":results,"foreign_bytes_policy":"PDFs read in memory, temporary selected-page PNGs deleted after personal inspection; no text, headers, or source pixels in permanent artifacts."}
(ROOT/"SOURCE_IDENTITIES.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
assert all(r.get("expected_hash_matches") for r in results)
