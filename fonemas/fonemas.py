import re
from dataclasses import dataclass
from silabeador import Syllabification

@dataclass
class Values:
    words: list
    syllables: list

class Transcription:
    """
    Class for transcribing sentences into their phonological, phonetic, and SAMPA representations.
    """

    def __init__(self, sentence, mono=False, exceptions=1,
                 epenthesis=False, aspiration=False, rehash=False,
                 stress='"'):
        """
        Initialize the Transcription class.

        :param sentence: The sentence to be transcribed.
        :param mono: Boolean indicating whether to treat monosyllabic words as unstressed.
        :param exceptions: Level of exceptions handling (0: none, 1: basic, 2: extended).
        :param epenthesis: Boolean indicating whether to apply epenthesis.
        :param aspiration: Boolean indicating whether to mark aspiration.
        :param rehash: Boolean indicating whether to apply rehashing to syllables.
        :param stress: Character used to mark stressed syllables in the SAMPA transcription.
        """
        self.sentence = self.__clean(sentence, epenthesis)
        self.__exceptions = exceptions
        
        if rehash:
            self.sentence = self.make_rehash(self.sentence)
        
        self.phonology = self.transcription_fnl(self.sentence, mono, aspiration)
        self.phonetics = self.transcription_fnt(self.phonology)
        self.sampa = self.ipa2sampa(self.phonetics, stress)

    @staticmethod
    def __clean(raw_sentence, epen):
        """
        Clean and normalize a raw sentence for transcription.

        :param raw_sentence: The sentence to be cleaned.
        :param epen: Boolean indicating whether to apply epenthesis.
        :return: The cleaned sentence.
        """
        letters = {
            'b': 'be', 'c': 'θe', 'ch': 'ʧe', 'd': 'de', 'f': 'efe',
            'g': 'ge', 'h': 'haʧe', 'j': 'jota', 'k': 'ka', 'l': 'ele',
            'll': 'eʎe', 'm': 'eme', 'n': 'ene', 'p': 'pe', 'q': 'ku',
            'r': 'erre', 's': 'ese', 't': 'te', 'v': 'ube',
            'w': 'ubedoble', 'x': 'ekis', 'z': 'θeta'
        }
        
        symbols = [
            '(', ')', '¿', '?', '¡', '!', '«', '»', '“', '”', '‘', '’',
            '[', ']', '—', '…', ',', ';', ':', "'", '.', '–', '"', '-'
        ]
        
        diacritics = {
            'à': 'á', 'è': 'é', 'ì': 'í', 'ò': 'ó', 'ù': 'ú',
            'æ': 'e', 'ä': '_a', 'ë': '_e', 'ï': '_i', 'ö': '_o',
            'ã': 'á', 'õ': 'ó', 'â': 'a', 'ê': 'e', 'î': 'i',
            'ô': 'o', 'û': 'u', 'ç': 'θ'
        }

        raw_sentence = raw_sentence.lower()
        
        # Replace letters with their phonetic equivalents
        for char in letters:
            raw_sentence = re.sub(rf'\b{char}\b', letters[char], raw_sentence)
        
        # Remove symbols
        for symbol in symbols:
            raw_sentence = raw_sentence.replace(symbol, ' ')
        
        # Replace diacritics
        for char, replacement in diacritics.items():
            raw_sentence = raw_sentence.replace(char, replacement)
        
        # Apply epenthesis if necessary
        if epen:
            raw_sentence = re.sub(r'\bs((?![aeiouáéíóú]))', r'es\1', raw_sentence)

        return raw_sentence

    @staticmethod
    def make_rehash(sentence):
        """
        Rehash syllables to adjust syllable boundaries based on phonological rules.

        :param sentence: The sentence represented as a list of syllables.
        :return: The rehashed list of syllables.
        """
        vowels = 'aeioujwăĕŏ'
        
        for idx, syllable in enumerate(sentence):
            if idx > 0 and len(syllable) > 1:
                if syllable[0].lower() in vowels and sentence[idx - 1][-1].lower() not in vowels:
                    sentence[idx] = sentence[idx - 1][-1] + syllable
                    sentence[idx - 1] = sentence[idx - 1][:-1]
        
        return sentence

    def transcription_fnl(self, sentence, mono, aspiration):
        """
        Generate the phonological transcription of a sentence.

        :param sentence: The cleaned sentence to transcribe.
        :param mono: Boolean indicating whether to treat monosyllabic words as unstressed.
        :param aspiration: Boolean indicating whether to mark aspiration.
        :return: A Values object containing the words and syllables of the phonological transcription.
        """
        diacritics = {
            'á': 'a', 'à': 'a', 'ä': 'a',
            'é': 'e', 'è': 'e', 'ë': 'e',
            'ú': 'u', 'ù': 'u', 'ü': 'u',
            'í': 'i', 'ì': 'i', 'ï': 'i',
            'ó': 'o', 'ò': 'o', 'ö': 'o',
            '_': ''
        }

        consonants = {
            'w': 'b', 'v': 'b', 'z': 'θ', 'ñ': 'ɲ', 'x': 'ks',
            'j': 'x', 'r': 'ɾ', 'R': 'r', 'ce': 'θe', 'cé': 'θé',
            'cë': 'θë', 'ci': 'θi', 'cí': 'θí', 'cï': 'θï',
            'cj': 'θj', 'ch': 'ʧ', 'c': 'k', 'qu': 'k', 'll': 'ʎ',
            'ph': 'f', 'hie': 'ʝe', 'h': ''
        }

        # Apply consonant replacements and handle aspiration
        sentence = re.sub(r'(?:([nls])r|\br|rr)', r'\1R', sentence)
        if aspiration:
            sentence = re.sub(r'\bh', 'ʰ', sentence)
        for consonant, replacement in consonants.items():
            sentence = sentence.replace(consonant, replacement)

        # Handle 'y' and 'g' specific cases
        if 'y' in sentence:
            sentence = re.sub(r'\by\b', 'i', sentence)
            sentence = re.sub(r'uy\b', 'wi', sentence)
            sentence = re.sub(r'y\b', 'j', sentence)
            sentence = sentence.replace('y', 'ʝ')
            for key, value in diacritics.items():
                if key in 'áéíóú':
                    sentence = re.sub(rf'{value}ʝ\b', f'{key}i', sentence)
            sentence = re.sub(r'ʝ((?![aeiouáéíóú]))', r'i\1', sentence)

        if 'g' in sentence:
            sentence = re.sub(r'g([eiéíëï])', r'x\1', sentence)
            sentence = re.sub(r'g[u]([eiéíëï])', r'g\1', sentence)
            sentence = re.sub(r'gü([eiéí])', r'gw\1', sentence, re.IGNORECASE)
            sentence = re.sub(r'gu([aoáó])', r'gw\1', sentence, re.IGNORECASE)

        # Split sentence into words and syllables
        transcription = self.__split_variables(sentence, mono)

        # Apply diacritic replacements
        for key, value in diacritics.items():
            transcription.words = [word.replace(key, value) for word in transcription.words]
            transcription.syllables = [syllable.replace(key, value) for syllable in transcription.syllables]

        return transcription

    def __split_variables(self, sentence, mono):
        """
        Split the sentence into words and syllables, applying stress marks.

        :param sentence: The cleaned sentence to split.
        :param mono: Boolean indicating whether to treat monosyllabic words as unstressed.
        :return: A Values object containing the words and syllables.
        """
        words = []
        syllables_sentence = []

        for word in sentence.split():
            if len(word) > 5 and word.endswith('mente'):
                syllabification = Syllabification(word=word[:-5], exceptions=self.__exceptions, ipa=True, h=True)
                syllables = syllabification.syllables
                stress = syllabification.stress - 2 if len(syllables) > 1 else -2
                syllables += ['ˌmen', 'te']
                word = word.replace('mente', 'ˌmente')
            else:
                syllabification = Syllabification(word, exceptions=self.__exceptions, ipa=True, h=True)
                syllables = syllabification.syllables
                stress = syllabification.stress

            syllables = self.__diphthongs(syllables)
            syllables[stress] = f'ˈ{syllables[stress]}'
            word = ''.join(syllables)

            if not mono and len(syllables) == 1:
                word = word.strip('ˈ')

            words.append(word)
            syllables_sentence.extend(syllables)

        return Values(words, syllables_sentence)

    def __diphthongs(self, syllables):
        """
        Adjust diphthongs within syllables according to phonetic rules.

        :param syllables: The list of syllables to process.
        :return: The modified list of syllables.
        """
        for idx, syllable in enumerate(syllables):
            if re.search(r'[aeioáéó][ui]', syllable):
                syllable = re.sub(r'([aeoáéó])i', r'\1j', syllable)
                syllable = re.sub(r'([aeioáéó])u', r'\1w', syllable)
            if re.search(r'[ui][aeiouáéó]', syllable):
                syllable = re.sub(r'i([aeoáéó])', r'j\1', syllable)
                syllable = re.sub(r'u([aeoiáéó])', r'w\1', syllable)
            syllables[idx] = syllable

        return syllables

    def transcription_fnt(self, phonology):
        """
        Convert the phonological transcription to a phonetic transcription.

        :param phonology: A Values object containing the phonological transcription.
        :return: A Values object containing the phonetic transcription.
        """
        words = ' '.join(phonology.words)
        syllables = '-'.join(phonology.syllables)

        return Values(self.__fsubstitute(words), self.__fsubstitute(syllables))

    @staticmethod
    def __fsubstitute(words):
        """
        Apply phonetic substitutions to simulate allophones and coarticulations.

        :param words: The string of words to process.
        :return: The modified string with allophones and coarticulations applied.
        """
        allophones = {'b': 'β', 'd': 'ð', 'g': 'ɣ'}
        for allo in allophones:
            regex = re.compile(rf'([^mnɲ\n\-\sˈ][\-\s]{{,1}}ˈ{{,1}}){allo}')
            words = re.sub(regex, rf'\1{allophones[allo]}', words)

        coarticulations = {
            r'θ([\s\-ˈ]*)([bdgβðɣmnɲlʎrɾ])': r'ð\1\2',
            r's([\s\-ˈ]*)([bdgβðɣmnɲlʎrɾ])': r'z\1\2',
            r'f([\s\-ˈ]*)([bdgβðɣmnɲʎ])': r'v\1\2',
            r'([lmn])([\s\-ˈ]*)ð': r'\1\2d',
            r'n([\s\-ˈ]*)([bpm])': r'm\1\2',
            r'n([\s\-ˈ]*)f': r'ɱ\1f',
            r'n([\s\-ˈ]*)k': r'ŋ\1k',
            r'n([\s\-ˈ]*)[gɣ]': r'ŋ\1g',
            r'n([\s\-ˈ]*)x': r'ŋ\1x',
            r'x([\s\-ˈ]*)(uow)': r'χ\1\2',
        }

        for pattern, replacement in coarticulations.items():
            words = re.sub(pattern, replacement, words)

        return words.replace('-', ' ').split()

    @staticmethod
    def ipa2sampa(ipa, stress_mark):
        """
        Convert IPA transcription to SAMPA transcription.

        :param ipa: A Values object containing the IPA transcription.
        :param stress_mark: The character to mark stress in SAMPA transcription.
        :return: A Values object containing the SAMPA transcription.
        """
        transliteration = {
            'β': 'B', 'ð': 'D', 'ɣ': 'G', 'ʎ': 'L', 'r': 'rr',
            'ɾ': 'r', 'ɱ': 'M', 'ŋ': 'N', 'ɲ': 'J', 'ʧ': 'tS',
            'ʝ': 'y', 'χ': '4', 'θ': 'T',
            'ˈ': stress_mark, 'ˌ': '%'
        }

        ipa_sampa = Values(ipa.words.copy(), ipa.syllables.copy())

        for key, value in transliteration.items():
            ipa_sampa.words = [word.replace(key, value) for word in ipa_sampa.words]
            ipa_sampa.syllables = [syllable.replace(key, value) for syllable in ipa_sampa.syllables]

        return ipa_sampa
