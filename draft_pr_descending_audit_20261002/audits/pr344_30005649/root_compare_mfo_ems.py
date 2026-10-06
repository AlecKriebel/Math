"""Read-only comparison of two retrieved versions of the exact source question."""
from pathlib import Path
import datetime, hashlib, json, sys
A = Path(__file__).resolve().parent
out = A / 'ROOT_MFO_EMS_QUESTION_COMPARISON.json'
assert not out.exists()
inputs = {'mfo_pdf': A / 'root_priority_private/mfo_retrieval001/mfo2023_42.pdf',
          'mfo_text': A / 'root_priority_private/mfo_retrieval001/mfo2023_42.txt',
          'mfo_metadata': A / 'root_priority_private/mfo_retrieval001/mfo_full_metadata.html',
          'ems_pdf': A / 'root_sources_private/owr2023-42.pdf',
          'ems_text': A / 'root_sources_private/owr2023-42.txt'}
def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'mode': p.stat().st_mode & 0o7777}
before = {name: pin(path) for name, path in inputs.items()}
assert before['mfo_pdf']['sha256'] == '2fd1d13149d46dd3c45caa48d93faaed63312f4e6762222d961fb30f6a7b68ff'
assert before['ems_pdf']['sha256'] == '3145acc3558489bc818125001721a4c7a26f458f187697a81c18fb8c18706d0a'
mfo = inputs['mfo_text'].read_text().split('\f')
ems = inputs['ems_text'].read_text().split('\f')
assert len(mfo) == len(ems) == 113
comparisons = {}
for i in range(99,104):
    comparisons[str(i+1)] = {'identical_whole_extracted_page': mfo[i] == ems[i],
                              'mfo_page_sha256': hashlib.sha256(mfo[i].encode()).hexdigest(),
                              'ems_page_sha256': hashlib.sha256(ems[i].encode()).hexdigest()}
assert all(row['identical_whole_extracted_page'] for row in comparisons.values()), comparisons
html = inputs['mfo_metadata'].read_text()
stamp = '2024-03-15T11:42:57Z'
assert '<td class="label-cell">dc.date.available</td><td class="word-break">'+stamp+'</td>' in html
assert '<td class="label-cell">dc.date.accessioned</td><td class="word-break">'+stamp+'</td>' in html
after = {name: pin(path) for name, path in inputs.items()}
assert before == after
record = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'status': 'PASS_IDENTICAL_OPERATIVE_PAGES100_TO104_REPOSITORY_AVAILABILITY_FIELD_CONFIRMED',
          'source_pins': before, 'whole_operative_page_comparisons': comparisons,
          'repository_date_available': stamp, 'repository_date_accessioned': stamp,
          'publisher_publication_date_previously_verified': '2024-04-18',
          'workshop_date_range': ['2023-09-24', '2023-09-29'], 'input_bytes_modes_unchanged': True,
          'program': pin(Path(__file__)), 'interpreter': sys.executable, 'version': sys.version,
          'reading_scope': 'Root separately read all5 operative extracted pages and displayed metadata fields before running this comparison; original EMS pages had also been visually inspected.',
          'limits': 'Repository metadata supplies an observed availability date, not proof of earliest circulation. Different whole PDFs are not asserted byte-identical. This record is computed comparison metadata, not a subprocess exit receipt.'}
out.write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
