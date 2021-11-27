from rest_framework import serializers

from .models import Genre, Artist, Concert


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Artist
        fields = 'id', 'name', 'slug', 'popularity', 'genre'


class ConcertSerializer(serializers.ModelSerializer):
    popularity = serializers.SerializerMethodField()
    artist = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Concert
        fields = 'id', 'name', 'slug', 'starts_at', 'ticket_price', 'tickets_sold', 'popularity', 'artist'

    @staticmethod
    def get_popularity(obj):
        return obj.popularity
