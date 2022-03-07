#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import silabeador


consonantes = {'w': 'b', 'v': 'b', 'z': 'θ', 'x': 'ks', 'j': 'x', 'ch':'tʃ',
               'ñ': 'ɲ',
               'qu': 'k', 'll': 'ʎ', 'ch':'tʃ', 'r': 'ɾ', 'ɾɾ': 'r',
               'sɾ': 'sr', 'lɾ': 'lr', 'nɾ': 'nr',
               'ce': 'θe', 'cé': 'θe', 'cë': 'θe',
               'ci': 'θi', 'cí': 'θi', 'cï': 'θi', 'cj': 'θi',
               'c': 'k', 'h':''}
alofonos    = {'nv': 'mb', 'nf': 'mf', 'nr': 'nrr', 'lr': 'lrr'}
diacriticos = {'á': 'a', 'à': 'a', 'ä': 'a',
               'é': 'e', 'è': 'e', 'ë': 'e',
               'í': 'i', 'ì': 'i', 'ï': 'i',
               'ó': 'o', 'ò': 'o', 'ö': 'o',
               'ú': 'u', 'ù': 'u', 'ü': 'u'}




def transcribe(palabra):
    palabra = palabra.lower()
    for alofono in alofonos:
        palabra = palabra.replace(alofono, alofonos[alofono])
    silabas_des = silabeador.silabas(palabra)
    silabas = silabas_des.silabas
    for idx, silaba in enumerate(silabas):
        if silaba.endswith('y'):
            silaba = silaba.replace('y','i')
        for letras in consonantes:
            if letras in silaba:
                silaba  = silaba.replace(letras, consonantes[letras])
        if 'g' in silaba:
            for reg in [[r'g([eiéíiëï])', rf'x\1'],
                        [r'g[u]([eiéíëï])', rf'g\1']]:
                silaba = re.sub(reg[0], reg[1], silaba)
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
    if silabas[0].startswith('ɾ'):
        silabas[0] = re.sub('^ɾ', 'r', silabas[0])
    silabas[silabas_des.tonica] = f"'{silabas[silabas_des.tonica]}"
    return silabas

