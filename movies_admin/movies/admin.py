from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('name', 'description')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', 'creation_date', 'rating', )
    list_filter = ('type', 'creation_date', 'rating', )
    search_fields = ('title', 'description', 'id')
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline
    )    


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('full_name',)
