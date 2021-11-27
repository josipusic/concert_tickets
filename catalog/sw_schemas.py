from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


artist_list_sw_schema = swagger_auto_schema(
    operation_description='List all the artists.',
    manual_parameters=[
        openapi.Parameter(
            'sort',
            openapi.IN_QUERY,
            description='Sort by artist "popularity" keyword. You can also prefix it with "-" which will list least'
                        ' popular artists first.',
            type=openapi.TYPE_STRING
        )
    ]
)

concert_list_sw_schema = swagger_auto_schema(
    operation_description='List all concerts.',
    manual_parameters=[
        openapi.Parameter(
            'artist',
            openapi.IN_QUERY,
            description='Search by artist slug.',
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'sort',
            openapi.IN_QUERY,
            description='Sort by concert "popularity" keyword. You can also prefix it with "-" which will list'
                        ' least popular artists first.',
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search by Concert name or artist name.',
            type=openapi.TYPE_STRING
        )
    ]
)

concert_detail_sw_schema = swagger_auto_schema(
    operation_description='Concert detail.',
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Enter slug that follows this pattern: ^[-a-zA-Z0-9_]+$',
            type=openapi.TYPE_STRING
        )
    ]
)
