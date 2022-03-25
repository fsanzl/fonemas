[![License: LGPL](https://img.shields.io/github/license/fsanzl/fonemas)](https://opensource.org/licenses/LGPL-2.1)
[![Version: 2.0.1](https://img.shields.io/github/v/release/fsanzl/fonemas)](https://pypi.org/project/fonemas/)
[![Python versions: 3.5, 3.6, 3.7, 3.8, 3.9](https://img.shields.io/pypi/pyversions/fonemas)](https://pypi.org/project/fonemas/)


<h2 align="center">Fonemas</h2>
<h3 align="center">A Python phonologic transcription library for Spanish</h2>


*fonemas* is a Python library of methods and functions for phonologic and phonetic ranscription of Spanish words.

This library is part of the research project [Sound and Meaning in Spanish Golden Age Literature](https://soundandmeaning.univie.ac.at/). Automatic verse scansion required identifying phonologic features that can be used using this library.

## Installation

```bash
pip3 install fonemas
```

## Use

The library provides the class  *transcription(sentence, mono, epenthesis)*. The class takes the obligatoy argument *sentence*, which is a string of characters with a Spanish word or words. It optionally takes two Boolean arguments *mono* and *epenthesis* set to False as default. The argument *mono* sets whether the output shows graphic stresses for monosyllabic words and *epenthesis* set the behaviour S bfore consonant in onset (spiritu -> es pi ri tu|spi ri tu).

*transcription()* has three dictionary attributes: *phonology* for the phonological transcription, *phonetics* for the phonetic transcription in IPA symbols (requires UNICODE support), and *sampa* for the phonetic transcription SAMPA transliteration. All attributes are dictionaries with two keys *{sentence, syllables}* containing each a list of strings, which may be words or syllables, respectively.

```python
>>> from fonemas import transcription
>>> object = transcription('Averigüéis')
>>> object.phonology
{'words': ["abeɾig'wejs"], 'syllables': ['a', 'be', 'ɾi', "'gwejs"]}
>>> object.phonetics
{'words': ["aβe'ɾiɣwejs"], 'syllables': ['a', 'βe', "'ɾi", 'ɣwejs']}
>>> object.sampa
{'words': "aBeri'Gwejs", 'syllables': "a Be ri 'Gwejs"}
```

## Description

The transcription is done according to the Spanish phonology and phonotactics described by Quilis (2019).


## Contributions

Feel free to contribute using the [GitHub Issue Tracker](https://github.com/fsanzl/fonemas/issues) for feedback, suggestions, or bug reports.


## Licence

This project is under GNU LGPL 2.1. See [LICENCE](https://github.com/fsanzl/fonemas/LICENCE) for details.

## References

Quilis, Antonio, *Tratado de fonología y fonética españolas*. Madrid, Gredos, 2019.
