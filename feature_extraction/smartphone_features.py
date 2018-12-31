import pandas as pd
import re


# Dicionário de cores para nomes alternativos
_color_alt_names = {
    'black': ('preto'),
    'white': ('branco'),
    'gold': ('ouro', 'dourado'),
    'red': ('vermelho'),
    'green': ('verde'),
    'blue': ('azul'),
    'pink': ('rosa'),
    'silver': ('platinum', 'gray', 'platina', 'prata', 'cinza')
}

_color_re = {}

for color_name, alt_names in _color_alt_names.items():
    names = tuple(color_name) + alt_names
    options = '|'.join(names)
    re.compile(fr'\b({options})\b', re.IGNORECASE)


def get_color(title):
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
    return match.group(1)


_brands = ['samsung', 'motorola', 'microsoft', 'apple', 'asus', 'xiaomi']

_brands_re = [
    re.compile(fr'\b({brand})\b', re.IGNORECASE) for brand in _brands,
    re.IGNORECASE
]


def get_model(title):
    model = _extract_known_model(title)
    if model is None:
        brand_matches = (brand_re.match(title) for brand_re in _brands_re)
        brand = next(brand_matches, None)
    else:
        brand = _get_brand_by_model(model)

    return {
        'brand': brand,
        'model': model
    }


_known_models = {
    r'(galaxy (?:young |ace |[a-z])\d)': 'samsung',
    r'(moto [a-z]\d?)': 'motorola',
    r'(lumia)': 'microsoft', # só tem 1 exemplo na base de dados, não conheço o padrão
    r'(iphone (?:\d|X)[a-z]?)': 'apple',
    r'(zenfone \d(?: zoom| max| selfie|))': 'asus',
    r'(redmi \d)\b': 'xiaomi',
    r'(mi [a-z]\d)': 'xiaomi'
    r'(pocophone [a-z]\d)': 'xiaomi'
}


def _extract_known_model(title):
    pass


def _get_brand_by_model(model):
    pass
