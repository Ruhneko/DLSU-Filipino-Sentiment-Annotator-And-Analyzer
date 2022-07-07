from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='FilEngS',
    url='https://github.com/Ruhneko/Filipino-English-Sentiment-Tagger',
    author='Us',
    author_email='us@yahoo.com',
    # Needed to actually package something
    packages=['FilEngS'],
    # Needed for dependencies
    install_requires=[  'emoji',
                        'pandas',
                        'sklearn',
                        'tensorflow',
                        'seaborn',
                        'demoji',
                        'scikeras',
                        'gensim'
                     ],
    dependency_links=['https://github.com/atmarges/pinoy_tweetokenize'],
    include_package_data=True,
    # *strongly* suggested for sharing
    version='0.1.2',
    # The license can be anything you like
    license='Someone',
    description='Filipino English Sentiment Tagger',
    long_description=open('README.md').read(),
)