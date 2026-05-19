from core.scoring import score_assessment

def test_scoring_returns_band():
    pack = {'dimensions':[{'slug':'opportunity'},{'slug':'motivation'}],'dimension_weights':{'opportunity':0.5,'motivation':0.5},'questions':[{'key':'q1','reverse_scored':False,'dimensions':[{'slug':'opportunity','weight':1.0}]},{'key':'q2','reverse_scored':False,'dimensions':[{'slug':'motivation','weight':1.0}]}],'bands':[{'band_key':'high','min_score':4.2},{'band_key':'medium','min_score':3.4},{'band_key':'low','min_score':2.6},{'band_key':'self_improvement','min_score':1.0}]}
    result = score_assessment({'q1':5,'q2':5}, pack)
    assert result['band_key'] == 'high'
