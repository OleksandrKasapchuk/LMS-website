from .models import Course, Subscription

def user_courses(request):
    subscribed_courses = Subscription.objects.filter(user=request.user).values_list('course', flat=True)
    joined = Course.objects.filter(id__in=subscribed_courses)
    owned = Course.objects.filter(user=request.user)
    
    # Якщо користувач не автентифікований, повертаємо порожній словник
    if not request.user.is_authenticated:
        return {}
    # Додаємо курси користувача до контексту
    courses = Course.objects.filter(user=request.user)
    return {'user_courses': owned, "joined_courses": joined}