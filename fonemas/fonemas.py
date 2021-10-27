#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import silabeador


consonantes = {'w': 'b', 'v': 'b', 'z': 'θ', 'x': 'ks', 'j': 'x', 'ch':'tʃ',
               'ñ': 'ɲ', 'y': 'j'}
dobles = {'qu': 'k', 'll': 'ʎ', 'ch':'tʃ',  'r': 'ɾ', 'ɾɾ': 'r',
          'sɾ': 'sr', 'lɾ': 'lr', 'nɾ': 'nr',
          'ce': 'θe', 'cé': 'θe', 'cë': 'θe',
          'ci': 'θi', 'cí': 'θi', 'cï': 'θ', 'c': 'k'}
diacriticos = {'á': 'a', 'à': 'a', 'ä': 'a',
               'é': 'e', 'è': 'e', 'ë': 'e',
               'í': 'i', 'ì': 'i', 'ï': 'i',
               'ó': 'o', 'ò': 'o', 'ö': 'o',
               'ú': 'u', 'ù': 'u', 'ü': 'u'}




def transcribe(palabra):
    palabra = palabra.lower()
    for unica in consonantes:
        if unica in palabra:
            palabra = palabra.replace(unica, consonantes[unica])
    for doble in dobles:
        if doble in palabra:
            palabra = palabra.replace(doble, dobles[doble])
    if palabra.startswith('ɾ'):
        palabra = re.sub('^ɾ', 'r', palabra)
    #if re.search('[nls]ɾ', palabra):
    #    re.sub('([nls])ɾ','\1r', palabra)
    if 'g' in palabra:
        for reg in [[r'g([eiEIéíÉÍËÏëï])', rf'x\1'],
                    [r'g[uU]([eiEIéíÉÍËÏëï])', rf'g\1']]:
            palabra = re.sub(reg[0], reg[1], palabra)
    if 'c' in palabra:
        for reg in [[r'c([eiEIéíÉÍËÏëï])', rf'θ\1'],
                    [r'c([aouAOUÁÓÚáóúäöüÄÖÜ])', rf'k\1']]:
            palabra = re.sub(reg[0], reg[1], palabra)
    silabas_des =  silabeador.silabas(palabra)
    silabas = silabas_des.silabas
    silabas[silabas_des.tonica] = f"'{silabas[silabas_des.tonica]}"
    if any('h' in silaba for silaba in silabas):
        silabas = [silaba.replace('h', '') for silaba in silabas]


    for idx, silaba in enumerate(silabas):
        if 'gü' in silaba:
            silaba = silaba.replace('gü', 'gw')
        if re.search('[aeiouáéíóú]{2,}', silaba):
            silaba = re.sub(r'([aeiouáééó])i', rf'\1j', silaba)
            silaba = re.sub(r'([aeiouáééó])u', rf'\1w', silaba)
        if re.search('[ui][aeiouáééiíóú]', silaba):
            silaba = re.sub(r'i([aeouáééiíóú])', rf'j\1', silaba)
            silaba = re.sub(r'u([aeioáééiíóú])', rf'w\1', silaba)
        for letra in diacriticos:
            if letra in silaba:
                silaba = silaba.replace(letra, diacriticos[letra])
        silabas[idx] = silaba
    return silabas

