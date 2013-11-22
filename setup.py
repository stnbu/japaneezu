
from distutils.core import setup

setup_kwargs = {
    'name': 'japaneezu',
    'version': '0.0.1',
    'description': 'A Very Beta Language Study Aide',
    'author': 'Mike Burr',
    'author_email': 'meburr@gmail.com',
    'url': 'http://tbd.example.com',
    'packages': ['japaneezu', 'japaneezu.tests'],
    'requires': ['igo-python'],
}

setup(**setup_kwargs)
