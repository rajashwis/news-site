from django.contrib import admin

# Register your models here.

from django.contrib import admin
from home.models import Article, Tag, Category, Comments, Advertisments

class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'id')
    exclude = ('author', 'post_views')

    def save_model(self,request,obj,form,change):
        obj.author=request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and obj.author == request.user: 
            return True  
        return False 

    def has_delete_permission(self, request, obj=None):
        if obj and obj.author == request.user: 
            return True  
        return False 
   

# Register your models here.


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Advertisments)