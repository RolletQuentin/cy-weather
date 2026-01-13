from prometheus_client import Counter

# Compteur de recherches de météo actuelle par ville
weather_current_searches = Counter(
    'weather_current_searches_total',
    'Total number of current weather searches',
    ['city', 'country_code']
)

# Compteur de recherches de prévisions par ville
weather_forecast_searches = Counter(
    'weather_forecast_searches_total',
    'Total number of forecast searches',
    ['city', 'country_code']
)