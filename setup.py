from setuptools import setup, find_packages

setup(
    name='glamkit-commenttools',
    version='0.0.1',
    description='Useful bits to spice up comments in your Django site.',
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