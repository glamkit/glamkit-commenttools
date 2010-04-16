from setuptools import setup, find_packages

setup(
    name='glamkit-commenttools',
    version='0.5.0',
    author='Julien Phalip',
    author_email='julien@interaction.net.au',
    description='Useful bits to spice up comments in your Django site.',
    long_description=open('README.rst').read(),
    url='http://github.com/glamkit/glamkit-commenttools',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)