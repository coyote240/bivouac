import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
        name='Bivouac',
        version='0.1.1',
        author='Adam A.G. Shamblin',
        author_email='adam.shamblin@gmail.com',
        packages=find_packages(),
        url='https://github.com/coyote240/bivouac',
        download_url='https://github.com/downloads/coyote240/bivouac/Bivouac-0.1.1.tar.gz',
        license='MIT',
        keywords='web mvc wsgi framework',
        classifiers=[
            'Classifier: Development Status :: 3 - Alpha',
            'Classifier: Intended Audience :: Developers',
            'Classifier: License :: OSI Approved :: MIT License',
            'Classifier: Topic :: Internet :: WWW/HTTP :: WSGI',
            'Classifier: Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
        ],
        description='a light-weight, wsgi-compliant web framework in Python',
        long_description=open('README.txt').read(),
        install_requires=[
            'WebOb >= 1.2.1',
            'Paste >= 1.7.5.1',
            'pymongo >= 2.1.1'
        ],
        py_modules=[
            'distribute_setup'
        ]
)
