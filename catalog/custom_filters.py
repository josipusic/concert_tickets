from rest_framework.filters import OrderingFilter


class FlippedOrderingFilter(OrderingFilter):
    """ Class that flips sort order in terms of ASC and DESC sql keywords. """

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            flipped_ordering = [f'-{i}' if i[0] != '-' else i[1:] for i in ordering]
            return queryset.order_by(*flipped_ordering)

        return queryset
