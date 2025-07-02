from django.template import engines, TemplateDoesNotExist
from django.template.loader import get_template
from .models import EmailTemplate

def render_email(shop, code, context):
    """
    1. Try to load EmailTemplate for this shop+code.
    2. If exists, render its subject & body via the Django engine.
    3. Otherwise, load file templates/email_config/{code}.html,
       split first line as subject, rest as body.
    Returns (subject, body) as rendered strings.
    """
    try:
        et = EmailTemplate.objects.get(shop=shop, code=code)
        engine = engines["django"]
        subj_tpl = engine.from_string(et.subject)
        body_tpl = engine.from_string(et.body)
        return subj_tpl.render(context), body_tpl.render(context)
    except EmailTemplate.DoesNotExist:
        tpl = get_template(f"email_config/{code}.html")
        rendered = tpl.render(context)
        # assume first line up to newline is subject:
        subject, body = rendered.split("\n", 1)
        return subject.strip(), body.strip()
