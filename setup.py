from distutils.core import setup

setup(
        name='Bivouac',
        version='0.1.0',
        author='Adam A.G. Shamblin',
        author_email='adam.shamblin@gmail.com',
        packages=['bivouac'],
        url='http://pypi.python.org/pypi/bivouac',
        license='LICENSE.txt',
        description='a light-weight, wsgi-compliant web framework in Python',
        long_description=open('README.txt').read(),
        install_requires=[
            'distribute',
            'WebOb >= 1.2.1',
            'Paste >= 1.7.5.1',
            'pymongo >= 2.1.1'
        ]
)
