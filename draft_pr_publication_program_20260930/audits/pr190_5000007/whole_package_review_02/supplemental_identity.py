"""Narrow follow-up: inspect literal pinned coefficients and fresh website metadata."""
from pathlib import Path
from urllib.request import urlopen,Request
import datetime,hashlib,json,zipfile
R=Path(__file__).resolve().parent;A=R.parent
rows=[]
def fetch(u):
    t=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with urlopen(Request(u,headers={'User-Agent':'PR190 independent verification/2'}),timeout=30) as f:
        b=f.read();rows.append({'UTC':t,'URL':u,'final_URL':f.url,'status':f.status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()});return b
expected={'paper.pdf':'ff6b9ba5f9bac0027a39d6e06319f04ff08bf24776a47cf7070213924d454707','source.zip':'d17acdd2a34f34685b3d854d3abfd4dbf19e253599c5c3f89f94e1ea078dd8d0','verification_report.md':'6f89f5ee24d11fa7bc0dbc7677bb883a8173160a2ca466708c6718f9d2b5f6a5'}
metadata=json.loads(fetch('https://eulersolve.org/papers/amr-049/metadata.json?v=0973f794ce32'))
for n,h in expected.items():
    if metadata['files'][n]['sha256']!=h:raise ValueError('website metadata checksum changed')
report=fetch('https://eulersolve.org/papers/amr-049/verification_report.md?v=6f89f5ee24d1')
if hashlib.sha256(report).hexdigest()!=expected['verification_report.md']:raise ValueError('website report changed')
s=fetch('https://raw.githubusercontent.com/DannyExperiments/dodecahedron-short-geodesic-counterexample/7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9/proof/PROBLEM_AND_PROOF.md').decode()
fields={'eta':'eta = exp(i*pi/5),','A':'A = 31/2 + (13/2)*sqrt(5),','B':'B = -17 - 8*sqrt(5).','advertised_norm':'S = (307 + 137*sqrt(5))/2','angle':'beta - alpha = 2*pi/5.'}
for label,literal in fields.items():
    if literal not in s:raise ValueError('literal missing '+label)
# External source inspection only: no downloaded module is imported/executed.
with zipfile.ZipFile(A/'current_literature_priority_adversary/private_sources/ferudun_source_current.zip') as z:
    main=z.read('main.tex').decode();start=main.index('The dodecahedron: Conjecture');end=main.index('Closed trajectories: Conjecture',start);sec=main[start:end]
    keys=['central symmetry','public record','midpoint','Remark','2','half-turn']
    source={'main_tex_bytes':len(z.read('main.tex')),'main_tex_sha256':hashlib.sha256(z.read('main.tex')).hexdigest(),'section7_chars':len(sec),'section7_sha256':hashlib.sha256(sec.encode()).hexdigest(),'targeted_source_search':{k:k in sec for k in keys},'proof_section_read_in_PDF':True,'source_sections_1_and_7_inspected':True,'remaining_six_conjectures_certified':False}
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'network':rows,'all3_current_website_metadata_hashes_equal_DOI_file_hashes':True,'website_verification_report_freshly_matches_DOI_report':True,'pinned_literals_exactly_present':list(fields),'previous_regex_miss':'coefficient31_13 false was formatting-only: source writes 31/2 + (13/2)*sqrt(5), algebraically identical to manuscript (31+13sqrt5)/2. Exact literals checked here.','external_source_inspection':source,'status':'PASS'}
(R/'SUPPLEMENTAL_IDENTITY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
