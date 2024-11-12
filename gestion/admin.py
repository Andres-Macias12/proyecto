from django.contrib import admin
from .models import Usuario, Paciente, Tratamiento, Cita, BlogArticle, ArticleSection

class ArticleSectionInline(admin.StackedInline):
    model = ArticleSection
    extra = 1

class BlogArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleSectionInline]
    list_display = ('title', 'published_date')
    search_fields = ('title',)

admin.site.register(Usuario)
admin.site.register(Paciente)
admin.site.register(Tratamiento)
admin.site.register(Cita)
admin.site.register(BlogArticle, BlogArticleAdmin)
