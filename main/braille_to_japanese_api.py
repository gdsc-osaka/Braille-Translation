from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from main.converter import convert_dots_to_text
from main.forms import BrailleDotsForm


@require_POST
def convert_braille_to_japanese(request: HttpRequest) -> JsonResponse:
    form = BrailleDotsForm(request.POST)

    if not form.is_valid():
        errors = form.errors.get("dots")
        message = (
            str(errors[0])
            if errors
            else "点字データを確認してください。"
        )
        return JsonResponse({"error": message}, status=400)

    converted_text = convert_dots_to_text(form.get_validated_dots())
    return JsonResponse({"result": converted_text})
