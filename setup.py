from distutils.core import setup

setup(
    name='telegram-currency-bot',
    version='0.1',
    packages=['telegram-currency-bot'],
    url='https://github.com/DenchikBY/Telegram-Currency-Bot-Python',
    license='MIT',
    author='Denis Butko',
    author_email='butko.denis.95@gmail.com',
    description='Telegram bot for converting BYN to USD, EUR and RUR',
    install_requires=[
        'requests',
        'python-telegram-bot', 'telegram'
    ],
)
