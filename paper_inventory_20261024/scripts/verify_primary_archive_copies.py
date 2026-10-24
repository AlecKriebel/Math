"""Verify direct-corpus duplicates inside ZIPs by reading exact public member bytes."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from acquire_corpus import SOURCES, write_json
from acquire_archive_papers import extract_member

def main():
    archive = json.loads((SOURCES / 'archive_papers.json').read_text())
    listings = json.loads((SOURCES / 'archive_listings.json').read_text())['archives']
    main_rows = json.loads((SOURCES / 'corpus_records.json').read_text())['records']
    sources = {s['md5']: (r['id'], s) for r in main_rows for s in r['sources']}
    by_key = {}
    for record in listings:
        for member in record['selected_members']:
            if member['member'].lower().endswith('.pdf'):
                by_key.setdefault((member['crc32'], member['bytes']), (record, member))
    def verify(row):
        record, member = by_key[(row['crc32'], row['bytes'])]
        data = extract_member(record, member)
        md5, sha = hashlib.md5(data).hexdigest(), hashlib.sha256(data).hexdigest()
        direct = sources.get(md5)
        matched = bool(direct and direct[0] == row['main_corpus_id'] and direct[1]['sha256'] == sha)
        return {'crc32': row['crc32'], 'bytes': row['bytes'], 'main_corpus_id': row['main_corpus_id'],
            'source_deposit_id': record['deposit_id'], 'member': member['member'],
            'archive_filename': record['archive_filename'], 'archive_advertised_md5': record['archive_advertised_md5'],
            'member_md5': md5, 'member_sha256': sha, 'direct_pdf_md5_sha256_match': matched,
            'method': 'Exact public archive byte-range extraction; ZIP CRC32/size and direct-file MD5/SHA256 comparison'}
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(verify, archive['exact_matches_to_main_corpus']))
    result = {'records': results, 'all_direct_pdf_hashes_match': all(r['direct_pdf_md5_sha256_match'] for r in results)}
    write_json(SOURCES / 'corpus_primary_archive_identity.json', result)
    print(json.dumps({'copies': len(results), 'all_match': result['all_direct_pdf_hashes_match']}))
    if not result['all_direct_pdf_hashes_match']:
        raise RuntimeError('A purported archive duplicate has different bytes')

if __name__ == '__main__': main()
