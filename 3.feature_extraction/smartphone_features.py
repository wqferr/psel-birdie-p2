import re
from operator import itemgetter

import pandas as pd
from more_itertools import first_true

# Dicionário de cores para nomes alternativos
_color_alt_names = {
    'black': ('preto', 'preta'),
    'white': ('branco', 'branca'),
    'gold': ('ouro', 'dourado', 'dourada'),
    'red': ('vermelho', 'vermelha'),
    'green': ('verde',),
    'blue': ('azul',),
    'pink': ('rosa',),
    'silver': ('platinum', 'gray', 'platina', 'prata', 'cinza')
}

_color_re = {}

for color_name, alt_names in _color_alt_names.items():
    names = (color_name,) + alt_names
    options = '|'.join(names)
    _color_re[color_name] = re.compile(fr'\b({options})\b', re.IGNORECASE)


def get_color(title):
    title = title.lower()
    for color_name, color_re in _color_re.items():
        if color_re.search(title) is not None:
            return color_name
    return None


# Xgb[[ de] ram]
# se não houver "ram" após a quantidade, assume-se que é
# o tamanho do armazenamento Interno
_ram_storage_re = re.compile(
    r'(?P<amount>\d+) ?GB(?P<ram>(?: de)? ram)?',
    re.IGNORECASE
)


def get_memory_and_storage(title):
    stats = {
        'ram': None,
        'storage': None
    }

    matches = _ram_storage_re.finditer(title)
    for match in matches:
        groups = match.groupdict()
        ram = groups['ram'] is not None
        amount_type = 'ram' if ram else 'storage'
        stats[amount_type] = groups['amount']
    return stats


_screen_size_re = re.compile(
    r'((?:\d+)(?:\.\d+))[\'"”]',
    re.IGNORECASE
)


def get_screen_size(title):
    match = _screen_size_re.search(title)
    return match and match.group(1)


_brands = [
    'samsung', 'motorola', 'microsoft', 'apple', 'asus', 'xiaomi',
    'lenovo', 'lg'
]

_brands_re = [
    re.compile(fr'\b({brand})\b', re.IGNORECASE) for brand in _brands
]


_known_models = {
    r'(galaxy (?:young |ace |[a-z])\d)': 'samsung',
    r'(moto [a-z]\d?)': 'motorola',
    r'(iphone (?:\d|X)[a-z]?)': 'apple',
    r'(zenfone \d(?: zoom| max| selfie|)(?: pro)?)': 'asus',
    r'(redmi \d)\b': 'xiaomi',
    r'(\bmi [a-z]\d)': 'xiaomi',
    r'(pocophone [a-z]\d)': 'xiaomi'
}


def get_model(title):
    title = title.lower()
    model, brand = _extract_known_model(title)
    if brand is None:
        brand_matches = (brand_re.search(title) for brand_re in _brands_re)
        brand = first_true(brand_matches, default=None)
        if brand is not None:
            brand = brand.group(1)

    return {
        'brand': brand,
        'model': model
    }


_known_models_re = {
    re.compile(model_re, re.IGNORECASE): brand
    for model_re, brand in _known_models.items()
}


def _extract_known_model(title):
    for known_model, brand in _known_models_re.items():
        match = known_model.search(title)
        if match is not None:
            model = match[1]
            return model, brand
    return None, None


_plus_re = re.compile(r'(\+|plus\b)', re.IGNORECASE)


def is_plus(title):
    return _plus_re.search(title) is not None


def series_to_attr(title_series):
    models = title_series.apply(get_model)
    sep_model_brand = models.apply([
        itemgetter('model'),
        itemgetter('brand')
    ])
    sep_model_brand.columns = ['model', 'brand']
    res = pd.DataFrame(columns=[
        'TITLE',
        'BRAND',
        'MODEL',
        'PLUS',
        'COLOR',
        'SCREEN_SIZE'
    ])

    res.TITLE = title_series
    res.BRAND = sep_model_brand.brand
    res.MODEL = sep_model_brand.model
    res.PLUS = title_series.apply(is_plus)
    res.COLOR = title_series.apply(get_color)
    res.SCREEN_SIZE = title_series.apply(get_screen_size)

    return res
