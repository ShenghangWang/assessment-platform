# Placeholder for future LLM integration.
import json
import os
from openai import OpenAI


REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "top_issues": {
            "type": "array",
            "items": {"type": "string"}
        },
        "strengths": {
            "type": "array",
            "items": {"type": "string"}
        },
        "tips": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "details": {"type": "string"}
                },
                "required": ["title", "details"],
                "additionalProperties": False
            }
        },
        "seven_day_plan": {
            "type": "array",
            "items": {"type": "string"}
        },
        "thirty_day_plan": {
            "type": "array",
            "items": {"type": "string"}
        },
        "conversation_starters": {
            "type": "array",
            "items": {"type": "string"}
        },
        "low_cost_date_ideas": {
            "type": "array",
            "items": {"type": "string"}
        },
        "disclaimer": {"type": "string"}
    },
    "required": [
        "summary",
        "top_issues",
        "strengths",
        "tips",
        "seven_day_plan",
        "thirty_day_plan",
        "conversation_starters",
        "low_cost_date_ideas",
        "disclaimer"
    ],
    "additionalProperties": False
}


def build_question_answer_summary(pack: dict, answers: dict) -> list[dict]:
    question_map = {q["key"]: q for q in pack["questions"]}
    labels = pack["answer_scale"]["labels"]

    rows = []
    for qkey, raw in answers.items():
        q = question_map.get(qkey)
        if not q:
            continue
        rows.append({
            "question_key": qkey,
            "question": q["text"],
            "answer_score": raw,
            "answer_label": labels.get(str(raw), ""),
            "reverse_scored": q.get("reverse_scored", False),
            "dimensions": q.get("dimensions", []),
        })

    return rows


def generate_ai_report_payload(pack: dict, attempt) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return generate_fallback_report_payload(pack, attempt)

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    meta = attempt.meta_json or {}
    answers = meta.get("answers", {})
    scored = meta.get("scored", {})

    dimension_scores = scored.get("dimension_scores", {})
    weakest = sorted(dimension_scores.items(), key=lambda x: x[1])[:3]
    strongest = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)[:2]

    qa_summary = build_question_answer_summary(pack, answers)

    system_prompt = """
你是一个中文恋爱成长建议产品的 AI 报告生成器。
你的任务是基于用户的自评答案，生成温和、具体、可执行的“提升脱单机会”报告。

要求：
1. 不要做确定性预测，不要说“你一定会/不会脱单”。
2. 不要羞辱用户，不要用PUA、操控、贬低他人的建议。
3. 不要把经济状况当成人的价值判断，只能把它解释为社交预算、压力和生活稳定性的现实因素。
4. 建议必须具体、可执行、适合普通用户。
5. 输出必须是中文。
6. 输出必须符合 JSON schema。
"""

    user_payload = {
        "product": pack["title"],
        "band_key": attempt.band_key,
        "final_score": float(attempt.final_score or 0),
        "display_score": attempt.display_score,
        "dimension_scores": dimension_scores,
        "weakest_dimensions": weakest,
        "strongest_dimensions": strongest,
        "question_answers": qa_summary,
    }

    try:
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        "请基于以下用户测评数据，生成一份个性化提升建议报告。"
                        "报告目标是帮助用户更有机会建立健康关系，而不是制造焦虑。\n\n"
                        f"{json.dumps(user_payload, ensure_ascii=False)}"
                    ),
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "dating_readiness_report",
                    "strict": True,
                    "schema": REPORT_SCHEMA,
                }
            },
        )

        return json.loads(response.output_text)

    except Exception as e:
        print(f"AI report generation failed: {e}")
        return generate_fallback_report_payload(pack, attempt)


def generate_fallback_report_payload(pack: dict, attempt) -> dict:
    meta = attempt.meta_json or {}
    scored = meta.get("scored", {})
    dimension_scores = scored.get("dimension_scores", {})

    if dimension_scores:
        weak = sorted(dimension_scores.items(), key=lambda x: x[1])[:2]
        weak_names = [k for k, _ in weak]
    else:
        weak_names = ["行动力", "社交机会"]

    return {
        "summary": f"你的主要改善方向集中在：{', '.join(weak_names)}。",
        "top_issues": [f"{name} 可能是当前最值得优先优化的方向。" for name in weak_names],
        "strengths": ["你已经完成了自我评估，这说明你愿意理解和调整自己的状态。"],
        "tips": [
            {
                "title": "先做一个低压力社交动作",
                "details": "本周选择一次低成本、低压力的社交机会，例如和朋友吃饭、参加兴趣活动，或主动开启一次轻松聊天。"
            },
            {
                "title": "把目标改成可执行行为",
                "details": "不要只想“我要脱单”，而是设定行为目标，例如每周认识1个新人、优化一次社交资料、主动发起2次聊天。"
            },
            {
                "title": "降低经济压力带来的社交阻力",
                "details": "如果预算有限，可以优先选择散步、咖啡、展览、校园/社区活动等低成本约会方式。"
            }
        ],
        "seven_day_plan": [
            "Day 1：写下你最想改善的一个维度。",
            "Day 2：联系一位朋友，增加一次社交连接。",
            "Day 3：优化你的自我介绍或社交资料。",
            "Day 4：主动和一个感兴趣的人开启轻松聊天。",
            "Day 5：选择一个低成本社交场景。",
            "Day 6：复盘你在哪一步最容易退缩。",
            "Day 7：制定下周的一个具体行动目标。"
        ],
        "thirty_day_plan": [
            "第1周：恢复社交节奏。",
            "第2周：增加认识新人的渠道。",
            "第3周：练习主动表达兴趣。",
            "第4周：复盘有效渠道并持续执行。"
        ],
        "conversation_starters": [
            "最近有没有什么让你觉得很放松的事情？",
            "你周末一般喜欢怎么安排？",
            "我发现我们好像都对这个话题挺感兴趣。"
        ],
        "low_cost_date_ideas": [
            "一起散步或逛公园",
            "咖啡店短聊天",
            "免费展览或书店",
            "校园/社区活动"
        ],
        "disclaimer": "本报告基于自我报告答案生成，只是当前状态下的建议，不是确定性预测或心理诊断。"
    }