stutils.core import setup
setup(
    name = 'mapscaler',
    packages = ['mapscaler'],
    version = '0.1',
    license='gpl-3.0',
    description = 'Scale areas of a geopandas map by any property to create more intuitive and beautiful choropleth visualizations.',
    author = 'Greg Condit',
    author_email = 'conditg@gmail.com',
    url = 'https://github.com/user/conditg/',
    download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
    keywords = ['DATA VISUALIZATION', 'MAP', 'CHOROPLETH', 'CARTOGRAM','MAP SCALER', 'GEOJSON'],
    install_requires=[
        'validators',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)


