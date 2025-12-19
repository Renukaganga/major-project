# modules/matching.py

from sklearn.metrics.pairwise import cosine_similarity

THRESHOLD = 0.85

def match_embedding(query_embedding, db_records):
    """
    query_embedding: 512-d vector
    db_records: list of dicts with 'embedding'
    returns: (matched_record, similarity_score)
    """
    best_match = None
    best_score = 0

    for record in db_records:
        score = cosine_similarity(
            [query_embedding],
            [record["embedding"]]
        )[0][0]

        if score > best_score:
            best_score = score
            best_match = record

    if best_score >= THRESHOLD:
        return best_match, best_score

    return None, best_score
