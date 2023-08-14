from django import template
import re

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(text):
    censor_words = ["редиска", "зло", "подлец", "бастард",
                    "гордыня", "жадность", "лень", "зависть", ]

    if not isinstance(text, str):
        raise TypeError("custom_filters: censor TypeError")


    text = re.split(r"\b",text)

    for i, word in enumerate(text):
        word = word.lower()
        if word in censor_words:
            first_chr = text[i]
            text[i] = first_chr[0] + "*"*(len(text[i])-1)


    text = " ".join(text)
    return f"{text}"

