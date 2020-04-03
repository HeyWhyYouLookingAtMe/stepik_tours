from tours.mock_data import title, subtitle, description, departures


def prepare_mock(request):
    context = {
        'title': title,
        'subtitle': subtitle,
        'description': description,
        'departures': departures,
    }
    return context
