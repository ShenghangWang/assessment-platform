from statistics import mean
def normalize_answer(raw_answer: int, reverse_scored: bool) -> int:
    if raw_answer < 1 or raw_answer > 5: raise ValueError('Answer must be between 1 and 5')
    return 6 - raw_answer if reverse_scored else raw_answer
def get_band_key(final_score: float, bands: list[dict]) -> str:
    for band in sorted(bands, key=lambda b: b['min_score'], reverse=True):
        if final_score >= band['min_score']: return band['band_key']
    return bands[-1]['band_key']
def score_assessment(answers: dict[str, int], pack: dict) -> dict:
    qmap = {q['key']: q for q in pack['questions']}
    dims = {d['slug']: [] for d in pack['dimensions']}
    for qkey, raw in answers.items():
        q = qmap[qkey]
        adjusted = normalize_answer(raw, q.get('reverse_scored', False))
        for dim in q['dimensions']:
            dims[dim['slug']].append(adjusted * float(dim['weight']))
    dim_scores = {slug: round(mean(vals), 2) if vals else 0.0 for slug, vals in dims.items()}
    weighted_sum = 0.0
    total_weight = 0.0
    for slug, score in dim_scores.items():
        w = float(pack['dimension_weights'].get(slug, 0))
        weighted_sum += score * w
        total_weight += w
    final_score = round(weighted_sum / total_weight, 3) if total_weight else 0.0
    display_score = round((final_score - 1) / 4 * 100)
    display_score = max(0, min(100, display_score))
    return {'dimension_scores': dim_scores, 'final_score': final_score, 'display_score': display_score, 'band_key': get_band_key(final_score, pack['bands'])}
