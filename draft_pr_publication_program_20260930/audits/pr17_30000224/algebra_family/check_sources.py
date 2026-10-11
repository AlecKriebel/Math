#!/usr/bin/env python3
"""Record exact cited loci, versions, hashes; short paraphrases only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
HERE=Path(__file__).resolve().parent
receipts=json.loads((HERE/'evidence'/'primary_source_receipts.json').read_text())
byname={r['name']:r for r in receipts['records']}
checks=[
 ('singh_walther_v2','Question 3.6.',8,
  'arbitrary ideal b, characteristic zero, original parametrized kernel; no homogeneity restriction'),
 ('owr_2005_19','Cohen-Macaulay?',44,
  'same unrestricted question in Singh report; PDF page44 is printed page1116'),
 ('hassanzadeh_v2','Theorem 1.2.',2,
  'first alternative includes s>=r and localization minimal-generator condition; second continues on p3'),
 ('hassanzadeh_v2','R is local with infinite residue field',3,
  'second alternative includes proper sequence and pdim(Z_i)<=r-i-1 for every i>=1'),
 ('hassanzadeh_v2','Corollary 3.19.',22,
  'regular-local residual-intersection statement assumes sliding depth'),
 ('ma_schwede_shimomoto_v3','Proposition 4.9.',16,
  'regular local essentially finite type over C; requires Du Bois quotient'),
 ('ma_schwede_shimomoto_v3','Corollary 4.10.',17,
  'homogeneous reduced-support ideal over C, punctured Du Bois locus, nonzero nonpositive defect'),
 ('ma_schwede_shimomoto_v3','seminormalization of R',14,
  'h0 of the Du Bois complex is the seminormalization; Du Bois implies seminormal'),
 ('eisenbud_sturmfels_author','COROLLARY 2.2.',13,
  'classical Laurent-binomial radical theorem stated with algebraically closed field; direct descent covers arbitrary K'),
]
records=[]
for name,needle,page,interpretation in checks:
    receipt=byname[name]
    assert receipt['status']=='retrieved'
    path=HERE/receipt['text']
    pdf=HERE/receipt['pdf']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==receipt['text_sha256']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==receipt['pdf_sha256']
    pages=path.read_text().split('\f')
    observed=[i+1 for i,p in enumerate(pages) if needle in p]
    assert page in observed, (name,needle,page,observed)
    records.append({'name':name,'pdf_page':page,'needle':needle,'located_pages':observed,
                    'url':receipt['requested_url'],'pdf_sha256':receipt['pdf_sha256'],
                    'paraphrase':interpretation})
out={'checked_at_utc':datetime.now(timezone.utc).isoformat(),
     'scope':'bounded cited-source hypothesis check; no exhaustive resolution/priority claim',
     'records':records,
     'latest_version_metadata':{'2409.05705':'v2, last revised 2025-02-12',
                                '1605.02755':'v3, last revised 2017-04-14',
                                'math/0701524':'v2, last revised 2007-08-27'},
     'metadata_check_method':'arXiv abstract pages inspected using web tool 2026-10-01'}
(HERE/'evidence'/'source_locus_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print('Source loci passed:',len(records))
