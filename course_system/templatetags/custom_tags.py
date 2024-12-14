from django import template
import datetime


register = template.Library()

@register.filter(name="endswith")
def endswith(value, arg):
	return value.endswith(arg)

@register.filter
def custom_date_format(value):
    """
    Повертає дату у різних форматах:
    - Якщо сьогодні: показує час (години і хвилини).
    - Якщо цього тижня: показує день тижня.
    - Інакше: день і місяць.
    """
    if not value:
        return ""
    
    now = datetime.datetime.now()
    
    # Якщо сьогодні
    if value.date() == now.date():
        return value.strftime("%H:%M")  # Формат часу (години:хвилини)
    
    # Якщо цього тижня
    start_of_week = now - datetime.timedelta(days=now.weekday())  # Понеділок поточного тижня
    if value.date() >= start_of_week.date():
        return value.strftime("%A, %H:%M")  # Назва дня тижня
    
    if value.year != now.year:
        return value.strftime("%Y-%m-%d")
    
    # В іншому випадку
    return value.strftime("%b. %d")  # День і місяць
