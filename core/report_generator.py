from .ai_client import generate_ai_report_payload


def build_paid_report(pack: dict, attempt) -> dict:
    payload = generate_ai_report_payload(pack, attempt)

    return {
        "template_key": "improvement_plan",
        "title": f"{pack['title']}｜个性化提升建议",
        "summary": payload.get("summary", ""),
        "content_json": payload,
    }