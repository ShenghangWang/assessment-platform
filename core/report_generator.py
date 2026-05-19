def build_paid_report(pack: dict, scored: dict) -> dict:
    weak_dims = sorted(scored.get('dimension_scores', {}).items(), key=lambda x: x[1])[:2]
    weak_label = '、'.join([slug for slug, _ in weak_dims]) if weak_dims else '暂无'
    return {'template_key': 'improvement_plan', 'title': f"{pack['title']}｜个性化提升建议", 'summary': f'你的主要改善方向集中在：{weak_label}', 'content_json': {'summary': f'你的主要改善方向集中在：{weak_label}', 'top_issues': [f'{slug} 得分偏低' for slug, _ in weak_dims] or ['暂无明显短板'], 'tips': [{'title': '先做最小行动', 'details': '把一个改进点拆成 7 天可执行任务。'}, {'title': '降低阻力', 'details': '减少执行建议时的心理门槛。'}, {'title': '每周复盘', 'details': '每周检查一次变化并微调。'}], '7_day_plan': ['Day 1: 明确你的弱项','Day 2: 选一个最小动作','Day 3: 执行一次','Day 4: 记录感受','Day 5: 调整阻力','Day 6: 再执行一次','Day 7: 复盘并决定下一步']}}
