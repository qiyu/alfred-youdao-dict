from setuptools import setup

install_requires = list(filter(None, ('''

xmltodict
requests
pydash

''').splitlines()))

setup(
    name='alfred_youdao_dict',
    version='1.0.0',
    entry_points={
        'console_scripts': ['alfred_youdao_dict = alfred_youdao_dict.main:main']
    },
    url='https://github.com/qiyu/alfred-youdao-dict',
    maintainer='qiyu',
    package_data={
        '': ['*.txt']
    },
    include_package_data=True,
    packages=['alfred_youdao_dict'],
    install_requires=install_requires
)
