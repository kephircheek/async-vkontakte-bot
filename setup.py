from setuptools import setup, find_packages

setup(
    name='aiovkbot',
    version='0.0.1',
    description='Asynchronous python interface for VK API',
    author='kephircheek',
    url='https://github.com/kephircheek/async-vkontakte-bot',
    packages=['aiovkbot'],
    install_requires=[
        'aiohttp',
        'aiojobs'
    ]
)
