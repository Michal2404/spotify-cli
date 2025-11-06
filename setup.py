from setuptools import setup

setup(
    name='spotify-cli',
    version='1.0.0',
    py_modules=['spotify_cli'],
    install_requires=[
        'spotipy',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'sptfy=spotify_cli:main',
        ],
    },
)