import os
from .report_generator import build_paid_report

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import DynamicQuizForm
from .pack_loader import load_pack
from .scoring import score_assessment
from .models import AssessmentPack, AssessmentVersion, AssessmentAttempt, AssessmentAnswer, GeneratedReport


def landing(request, slug):
    pack = load_pack(slug)
    return render(request, 'core/landing.html', {'pack': pack})

def quiz_view(request, slug):
    pack = load_pack(slug)
    form = DynamicQuizForm(questions=pack['questions'])
    return render(request, 'core/quiz.html', {'pack': pack, 'form': form})

def submit_view(request, slug):
    pack = load_pack(slug)
    form = DynamicQuizForm(request.POST, questions=pack['questions'])
    if not form.is_valid():
        return render(request, 'core/quiz.html', {'pack': pack, 'form': form})
    answers = dict(form.cleaned_data)
    scored = score_assessment(answers, pack)
    pack_obj = get_object_or_404(AssessmentPack, slug=slug)
    version_obj, _ = AssessmentVersion.objects.get_or_create(pack=pack_obj, version_number=pack['version'], defaults={'status': 'published', 'config_json': pack})
    attempt = AssessmentAttempt.objects.create(
    pack=pack_obj,
    version=version_obj,
    status='completed',
    final_score=scored['final_score'],
    display_score=scored['display_score'],
    band_key=scored['band_key'],
    completed_at=timezone.now(),
    meta_json={
        "answers": answers,
        "scored": scored,
    },
    )
    for q in pack['questions']:
        raw_val = answers[q['key']]
        normalized = 6 - raw_val if q.get('reverse_scored', False) else raw_val
        AssessmentAnswer.objects.create(attempt=attempt, question_key=q['key'], raw_value=str(raw_val), normalized_score=normalized)
    return redirect('core:result', attempt_id=attempt.id)

def result_view(request, attempt_id):
    attempt = get_object_or_404(AssessmentAttempt, id=attempt_id)
    pack = load_pack(attempt.pack.slug)
    band = next(b for b in pack['bands'] if b['band_key'] == attempt.band_key)
    return render(request, 'core/result.html', {'attempt': attempt, 'pack': pack, 'band': band})

def paywall_view(request, attempt_id):
    attempt = get_object_or_404(AssessmentAttempt, id=attempt_id)
    pack = load_pack(attempt.pack.slug)
    band = next(b for b in pack['bands'] if b['band_key'] == attempt.band_key)
    return render(request, 'core/paywall.html', {'attempt': attempt, 'pack': pack, 'band': band})

def unlock_view(request, attempt_id):
    attempt = get_object_or_404(AssessmentAttempt, id=attempt_id)
    if attempt.status != 'paid':
        attempt.status = 'paid'
        attempt.paid_at = timezone.now()
        attempt.save(update_fields=['status', 'paid_at'])
    return redirect('core:report', attempt_id=attempt.id)

def report_view(request, attempt_id):
    attempt = get_object_or_404(AssessmentAttempt, id=attempt_id)
    pack = load_pack(attempt.pack.slug)

    mock_payments = os.getenv("MOCK_PAYMENTS", "True") == "True"

    if not mock_payments and attempt.status != "paid":
        return redirect("core:paywall", attempt_id=attempt.id)

    if not hasattr(attempt, "report"):
        report_payload = build_paid_report(pack, attempt)
        GeneratedReport.objects.create(
            attempt=attempt,
            template_key=report_payload["template_key"],
            title=report_payload["title"],
            summary=report_payload["summary"],
            content_json=report_payload["content_json"],
            model_name=os.getenv("OPENAI_MODEL", "fallback"),
            prompt_version="v1",
        )

    return render(
        request,
        "core/report.html",
        {
            "attempt": attempt,
            "pack": pack,
            "report": attempt.report,
            "content": attempt.report.content_json,
        },
    )

def mock_pay_view(request, attempt_id):
    attempt = get_object_or_404(AssessmentAttempt, id=attempt_id)
    attempt.status = "paid"
    attempt.paid_at = timezone.now()
    attempt.save(update_fields=["status", "paid_at"])

    return redirect("core:report", attempt_id=attempt.id)