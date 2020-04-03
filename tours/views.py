from itertools import islice

from django.views.generic import TemplateView

from tours.mock_data import tours, departures


# Create your views here.

def dummy_sort(all_tours, sort_by='price', reverse=False, limit=None):
    # Horrible sort, actually.
    limit = len(all_tours) if limit is None else limit
    result = {tour_id: all_tours[tour_id] for tour_id in
              islice(
                  sorted(all_tours, key=lambda x: f'{all_tours[x][sort_by]}-{all_tours[x]["title"]}',
                         reverse=reverse), limit)}

    return result


def dummy_filter(all_tours, departure):
    filtered_ids = filter(lambda x: all_tours[x]['departure'] == departure, all_tours)
    result = {tour_id: all_tours[tour_id] for tour_id in filtered_ids}
    return result


def get_property_extrema(all_tours, prop):
    min_id = min(all_tours, key=lambda x: all_tours[x][prop])
    max_id = max(all_tours, key=lambda x: all_tours[x][prop])
    min_prop = all_tours[min_id][prop]
    max_prop = all_tours[max_id][prop]
    return min_prop, max_prop


def form_departure_text(all_departures, current_departure):
    return all_departures[current_departure][3:]


class MainView(TemplateView):
    template_name = "tours/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sorted_tours = dummy_sort(tours, limit=6)
        context['tours'] = sorted_tours
        return context


class DepartureView(TemplateView):
    template_name = "tours/departure.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        departure = context['departure']
        filtered_tours = dummy_filter(tours, departure)
        sorted_tours = dummy_sort(filtered_tours)
        context['tours'] = sorted_tours
        context['tours_count'] = len(sorted_tours)
        context['min_price'], context['max_price'] = get_property_extrema(sorted_tours, 'price')
        context['min_nights'], context['max_nights'] = get_property_extrema(sorted_tours, 'nights')
        context['departure_text'] = form_departure_text(departures, departure)
        return context


class TourView(TemplateView):
    template_name = "tours/single_tour_info.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        tour_id = context.get('id')
        tour = tours.get(tour_id)
        context['tour'] = tour
        departure = tour['departure']
        context['departure_text'] = form_departure_text(departures, departure)
        return context
