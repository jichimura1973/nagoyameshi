from django.contrib import admin

from .models import Category, Restaurant, Reservation, Review, FavoriteRestaurant

admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Reservation)
# admin.site.register(Review)
admin.site.register(FavoriteRestaurant)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'rate', 'visited_at')
    
admin.site.register(Review, ReviewAdmin)
    
    
    
