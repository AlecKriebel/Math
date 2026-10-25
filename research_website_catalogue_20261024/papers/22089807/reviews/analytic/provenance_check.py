#!/usr/bin/env python3
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import re
import tarfile

HERE=Path(__file__).resolve().parent
SOURCES=HERE.parents[1]/"sources"
def sha(data): return hashlib.sha256(data).hexdigest()
expected={
"simultaneous_amplification_beyond_three_halves.pdf":"1d6d1d31a782776b07b9240467f02d624b47dcde5c83f4740a192136c2dfb8e3",
"simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz":"e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae"}
inputs=[]
for name,digest in expected.items():
    data=(SOURCES/name).read_bytes()
    if sha(data)!=digest: raise RuntimeError("input digest mismatch "+name)
    inputs.append({"path":str(SOURCES/name),"bytes":len(data),"sha256":digest})
archive=SOURCES/"simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz"
with tarfile.open(archive,"r:gz") as tar:
    members=tar.getmembers()
    if len(members)!=23 or any(not m.isfile() for m in members):
        raise RuntimeError("archive shape")
    payloads={m.name:tar.extractfile(m).read() for m in members}
manifest=payloads.pop("MANIFEST.sha256").decode()
entries={name:digest for digest,name in (line.split("  ",1) for line in manifest.splitlines())}
if set(entries)!=set(payloads): raise RuntimeError("manifest set mismatch")
for name,digest in entries.items():
    if sha(payloads[name])!=digest: raise RuntimeError("archive member hash mismatch "+name)
    if (SOURCES/"published-source"/name).read_bytes()!=payloads[name]:
        raise RuntimeError("extraction mismatch "+name)
stand=(HERE/"artifacts/main-layout.txt").read_text()
embed=(HERE/"artifacts/embedded-layout.txt").read_text()
(HERE/"artifacts/pdf-text-diff.txt").write_text("".join(difflib.unified_diff(stand.splitlines(True),embed.splitlines(True),fromfile="standalone",tofile="embedded")))
def normalize(txt):
    txt=txt.replace("August 22, 2026","August 2026")
    a,b=txt.index("mt hub leaves"),txt.index("Figure 1:")
    txt=txt[:a]+"[FIGURE 1 DIAGRAM]"+txt[b:]
    return re.sub(r"\s+"," ",txt).strip()
if normalize(stand)!=normalize(embed):
    raise RuntimeError("PDF substantive extracted text differs")
result={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"submitted_inputs":inputs,"archive_members":len(members),"manifest_members_checked":len(entries),"all_extracted_files_byte_identical":True,"embedded_pdf_sha256":entries[next(k for k in entries if k.endswith("output/pdf/simultaneous_amplification_beyond_three_halves.pdf"))],"normalized_extracted_text_sha256":sha(normalize(stand).encode()),"text_equivalence_scope":"entire extraction after normalizing date, all whitespace, and replacing diagram region by a common token; figure checked visually separately"}
(HERE/"artifacts/provenance-check.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
print("PASS submitted hashes, 23-member archive, internal manifest, extraction identity, and PDF text equivalence")
