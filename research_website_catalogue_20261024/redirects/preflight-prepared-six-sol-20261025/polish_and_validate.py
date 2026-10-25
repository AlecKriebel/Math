"""Readability pass and artifact/custody validation, confined to this folder."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

D=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
replacements={
 'be1-solvable':'be 1-solvable','fitness3/2':'fitness 3/2','all76legacyPDFSHA256s':'all 76 legacy PDF SHA256 values',
 'oldHTML/URL/PDF/DOI':'old HTML/URL/PDF/DOI','sourcePDFSHA':'source PDF SHA256','version1.0.0':'version 1.0.0',
 '8August2026':'8 August 2026','8August':'8 August','10pages':'10 pages','21pages':'21 pages','10page':'10-page','21page':'21-page',
 'version2.0.4':'version 2.0.4','25August2026':'25 August 2026','21 pages,214040bytes':'21 pages, 214040 bytes',
 '107063bytes':'107063 bytes','16223bytes':'16223 bytes','selfDOI':'self DOI','reference DOI21850042':'reference DOI 21850042',
 'oldreader':'old reader','current21page':'current 21-page','v1reader':'v1 reader','full-repository21852072snapshot':'full-repository 21852072 snapshot',
 'isNewVersionOf`21852072':'isNewVersionOf` 21852072','old21753404':'old 21753404','current22089806':'current 22089806',
 '481658460-byte':'481,658,460-byte','from21852072':'from 21852072','oldPDFsection8/p9':'old PDF Section 8/page 9',
 'order22':'order-22','every old claim':'every old claim','oldPDF':'old PDF','oldarticle':'old article','exact-target':'exact target',
 'source/config/receipt/rootclearance/docs/helper/Git':'source/config/receipt/root-clearance/docs/helper/Git','rootclearance':'root clearance',
 'existingJC':'existing JC','completedJC':'completed JC','all203works':'all 203 works','203work':'203-work','full-old/newproof-containment':'full old/new proof containment',
 'liveHTTP':'live HTTP','inbrowser':'in a browser','recordedlive':'recorded live','old/newproofequivalence':'old/new proof equivalence',
 '6publication':'6 publication','6current':'6 current','47pinnedHTML':'47 pinned HTML','76pinnedPDF':'76 pinned PDF',
 '854pages':'854 pages','HTML/PDFobjects':'HTML/PDF objects','title,H1,canonical,citation/meta,links,rawHTML':'title, H1, canonical, citation/meta, links, raw HTML',
 '47HTML':'47 HTML','76PDF':'76 PDF','47html':'47 HTML','76pdf':'76 PDF','all6':'all 6','all10legacyPDF':'all 10 legacy PDF',
 'readeridentity':'reader identity','firstpage':'first page','fulltexts':'full texts','complete-text':'complete-text',
 '6original':'6 original','6machine':'6 machine','13falsepositive':'13 false-positive','currentPDF':'current PDF','legacyPDF':'legacy PDF',
 'noarticle':'no article','PDFbytes':'PDF bytes','PDFSHA256':'PDF SHA256','PDFmatches':'PDF matches','endGitHub':'end GitHub',
 'FreshGitHub':'Fresh GitHub','FreshZenodo':'Fresh Zenodo','NoZenodo':'No Zenodo','Noexhaustive':'No exhaustive','Noactualtarget':'No actual target',
 'Nonewscientific':'No new scientific','Nooriginalfiles':'No original files','ZIPdownload':'ZIP download','whole-archiveMD5':'whole-archive MD5',
 'page20':'page 20','Theorem2':'Theorem 2','Theorem3':'Theorem 3','oldTheorem':'old Theorem','currentTheorem':'current Theorem',
 'OldTheorem':'Old Theorem','OldProposition3':'Old Proposition 3','currentProposition15':'current Proposition 15',
 'OldRemark4':'Old Remark 4','currentCorollary16':'current Corollary 16','Oldequations17–18':'Old equations 17–18',
 'currentequations41–42':'current equations 41–42','rationalparameters19/137,20/27':'rational parameters 19/137, 20/27',
 '1.0.0, released8':'1.0.0, released 8','DOI10.':'DOI 10.','archive at21852072':'archive at 21852072',
 'record_id21852072':'record_id 21852072','scope previous':'scope previous','scope_note':'scope_note',
 'Commitc82':'Commit c82','commitc82':'commit c82','OldHTML':'Old HTML','oldHTML':'old HTML','reader10':'reader 10',
 'reader21':'reader 21','6page':'6-page','prooffamily':'proof family','wholeZIP':'whole ZIP','oldaffine':'old affine',
 'Current amplifier pages1–5(mainmodel/construction/theorem),17–21(response/theorem/limitations/availability/references)':'Current amplifier pages 1–4, the main theorem and beginning of Section 4 on page 5, and pages 17–21 (responses, theorem, limitations, availability and references)',
 'pages6–16':'pages 6–16','complete old/newproof-containment':'complete old/new proof containment',
 'All76legacy PDF SHA256s':'All 76 legacy PDF SHA256 values','DOI[':'DOI [','and8 August':'and 8 August',
 'threshold1.502':'threshold 1.502','`de30e1f`root':'`de30e1f` root','The481,':'The 481,',
 'current21-page':'current 21-page','older10-page':'older 10-page','historicalPDF':'historical PDF',
 'taggedsource':'tagged source','versionedcertificate':'versioned certificate','commit`':'commit `',
 'cachedPDFidentity':'cached PDF identity','sameDOI/exactreader':'same DOI/exact reader',
}
paths=[D/'REPORT.md',D/'RESEARCH_LOG.md']
for p in paths:
 s=p.read_text()
 for a,b in replacements.items():s=s.replace(a,b)
 p.write_text(s)
def clean(v):
 if isinstance(v,str):
  for a,b in replacements.items():v=v.replace(a,b)
  return v
 if isinstance(v,list):return [clean(x) for x in v]
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
 return v
for p in [D/'READ_COVERAGE.json',D/'correspondence.json',*sorted((D/'papers').glob('*.json'))]:
 j=json.loads(p.read_text());p.write_text(json.dumps(clean(j),indent=2,ensure_ascii=False)+'\n')
base=json.loads((D/'protected-input-baseline.json').read_text())
assert all(digest(Path(p))==r['sha256'] for p,r in base['files'].items())
sub=json.loads((D/'supplemental-input-baseline.json').read_text())
assert all(digest(Path(p))==r['sha256'] for p,r in sub.items())
c=json.loads((D/'correspondence.json').read_text());assert len(c['papers'])==6
assert len([p for p in c['papers'] if p['classification']=='NO_CORRESPONDING_ARTICLE_IDENTIFIED_IN_PINNED_SNAPSHOT'])==5
assert len([p for p in c['papers'] if p['classification']=='PLAUSIBLE_DOCUMENTED_OLDER_EDITION_REQUIRING_ROOT_LINEAGE_AUDIT'])==1
assert all(not p['html_redirect_authorized'] and not p['exact_old_pdf_matches'] for p in c['papers'])
for p in c['papers']:
 individual=json.loads((D/'papers'/f'{p["record_id"]}.json').read_text());assert individual==p
seal={'utc':datetime.now(timezone.utc).isoformat(),'scope':'All current regular files under this owned preflight folder except HASH_SEAL.json itself; no originals included as outputs.','files':{str(p.relative_to(D)):{'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p),'git_blob_sha1':hashlib.sha1(b'blob '+str(p.stat().st_size).encode()+b'\0'+p.read_bytes()).hexdigest()} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='HASH_SEAL.json'}}
(D/'HASH_SEAL.json').write_text(json.dumps(seal,indent=2,ensure_ascii=False)+'\n')
assert all(digest(D/k)==v['sha256'] for k,v in seal['files'].items())
print(json.dumps({'validated':True,'sealed_files':len(seal['files']),'report_sha256':digest(D/'REPORT.md'),'correspondence_sha256':digest(D/'correspondence.json'),'seal_sha256':digest(D/'HASH_SEAL.json'),'protected_unchanged':len(base['files']),'supplemental_unchanged':len(sub)}))
