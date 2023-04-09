from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value: str):
    ban_words = ['блять', 'сука', 'нахуй', 'дурак', 'мудак', 'Блять']
    text = value
    for word in ban_words:
        if word in text:
            text = text.replace(word, '')
    return text
