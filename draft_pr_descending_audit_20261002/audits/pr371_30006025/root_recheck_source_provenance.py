"""Compare exact fresh source bytes with every historical declaration; no normalization."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent;S=A/'raw_sources';T=A/'snapshot/problems/30006025_geometric_chapuy'
def sha(b):return hashlib.sha256(b).hexdigest()
fresh=[]
for f in sorted(S.iterdir()):
    if f.is_file() and f.suffix in ('.pdf','.txt','.png'):
        b=f.read_bytes();fresh.append({'path':'raw_sources/'+f.name,'bytes':len(b),'sha256':sha(b)})
rows=[]
for name in ['SOURCE_HASHES.json','SOURCE_ADDENDUM_TURN_2.json','SOURCE_ADDENDUM_TURN_3.json','SOURCE_ADDENDUM_TURN_4.json']:
    for old in json.loads((T/name).read_bytes())['files']:
        matches=[f['path'] for f in fresh if f['bytes']==old['bytes'] and f['sha256']==old['sha256']]
        rows.append({'manifest':name,'historical_declaration':old,'exact_fresh_matches':matches,'exact_historical_bytes_reproduced':bool(matches)})
assert len(rows)==27 and len({r['historical_declaration']['path'] for r in rows})==25
original_pdfs={r['historical_declaration']['path']:r for r in rows if r['historical_declaration']['path'].endswith('.pdf')}
assert len(original_pdfs)==10
matches=sum(r['exact_historical_bytes_reproduced'] for r in original_pdfs.values());assert matches==9
published=json.loads((A/'bgl2025-published_fresh_receipt.json').read_bytes())
actual=(S/published['name']).read_bytes()
assert len(actual)==published['bytes'] and sha(actual)==published['sha256']
old=original_pdfs['sources/bgl2025.pdf']['historical_declaration']
assert sha(actual)!=old['sha256']
readings=[
 {'name':'OWR_2024_41.pdf','read':'Full Louf contribution, PDF36-38/printed2404-2406; Question4 visual PDF37'},
 {'name':'chapuy2010.pdf','read':'PDF1,12-13; dominant maps, opening/gluing marked triples and unique inverse'},
 {'name':'cff2013.pdf','read':'PDF1-3,6-8; Theorem5, signed copy multiplicities, graph preservation and perfect matching'},
 {'name':'janson-louf2021.pdf','read':'PDF1-4,7; graph regime, actual square-root scale, unsigned correspondence and conjecture'},
 {'name':'bgl2025-published.pdf','read':'Published PDF2-5,25; metric-map law, L=2 sum lengths, conditional uniform simplex'},
 {'name':'delaygue2025.pdf','read':'PDF1; actual classical TheoremsA/C, overline on algebraic coefficient field visual'},
 {'name':'philippe2008-journal.pdf','read':'PDF28-29/printed2685-2686; orientation-preserving group, exact p=3 Corollary5.2 visually verified'},
 {'name':'mirzakhani-petri.pdf','read':'PDF1-2; displayed Theorem4.1 intensity visually verified; adjacent inaccurate epsilon approximation not used'},
 {'name':'uniform-dessins2025.pdf','read':'PDF3-6; signature, torsion-free cover, subgroup index and geodesic-edge realization'},
 {'name':'izmestiev2014.pdf','read':'PDF1-3; intrinsic Theorem1 and cone/boundary definitions, overlaps allowed'}]
for r in readings:
    b=(S/r['name']).read_bytes();r.update(bytes=len(b),sha256=sha(b))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FRESH_MATHEMATICAL_SOURCES_WITH_DECLARED_HISTORICAL_LIMITATION',
     'historical_binding_instances':27,'historical_distinct_paths':25,'exact_matched_instances':sum(r['exact_historical_bytes_reproduced'] for r in rows),
     'required_primary_pdf_identities':10,'exact_primary_pdf_identities_matched':matches,'historical_binding_comparisons':rows,
     'fresh_source_files':fresh,'used_primary_readings':readings,'fresh_published_bgl':published,
     'historical_published_bgl':old,'dynamic_footer_observed':True,
     'all_differences_proved_footer_only':False,'all_27_historical_bindings_recertified':False,
     'limitations':'The exact historical Cambridge PDF, text extractions and raster assets were not recovered. Its IP/time footer is dynamic; without the historical bytes no complete difference attribution is claimed. The arXiv v1 and Numdam alternatives are separately identified, not substituted for the journal versions. Current mathematical statements were directly checked; no global priority/novelty certification.'}
(A/'root_source_provenance_recheck.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','historical_binding_instances','exact_matched_instances','required_primary_pdf_identities','exact_primary_pdf_identities_matched','all_27_historical_bindings_recertified']},indent=2))
