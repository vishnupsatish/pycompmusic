#!/usr/bin/env python
# Copyright 2013,2014 Music Technology Group - Universitat Pompeu Fabra
# 
# This file is part of Dunya
# 
# Dunya is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation (FSF), either version 3 of the License, or (at your option) any later
# version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see http://www.gnu.org/licenses/


import sys
import os
import re
import logging
logging.basicConfig(level=logging.INFO)

#sys.path.insert(0, os.path.join(
#        os.path.dirname(os.path.abspath(__file__)), ".."))
#from dunya import settings
#from django.core.management import setup_environ
#setup_environ(settings)

#from carnatic.models import Raaga, Taala

reraaga = re.compile(r"\braa?gam?[0-9]*\b")
retaala = re.compile(r"\btaa?lam?[0-9]*\b")
remakam = re.compile(r"\bmakam\b")
reusul = re.compile(r"\busul\b")
reform = re.compile(r"\bform\b")

def has_raaga(tag):
    return re.search(reraaga, tag) is not None

def has_taala(tag):
    return re.search(retaala, tag) is not None

def has_makam(tag):
    return re.search(remakam, tag) is not None

def has_usul(tag):
    return re.search(reusul, tag) is not None

def has_form(tag):
    return re.search(reform, tag) is not None

def parse_raaga(raaga):
    raaga = raaga.strip()
    raaga = re.sub(r" ?: ?", " ", raaga)
    raaga = re.sub(reraaga, "", raaga)
    return raaga.strip()

def parse_taala(taala):
    taala = taala.strip()
    taala = re.sub(r" ?: ?", " ", taala)
    taala = re.sub(retaala, "", taala)
    return taala.strip()

def parse_makam(makam):
    makam = makam.strip()
    makam = re.sub(r" ?: ?", " ", makam)
    makam = re.sub(remakam, "", makam)
    return makam.strip()

def parse_usul(usul):
    usul = usul.strip()
    usul = re.sub(r" ?: ?", " ", usul)
    usul = re.sub(reusul, "", usul)
    return usul.strip()

def parse_form(form):
    form = form.strip()
    form = re.sub(r" ?: ?", " ", form)
    form = re.sub(reform, "", form)
    return form.strip()

def main():
    tags = open(sys.argv[1]).readlines()
    r = []
    t = []
    for tg in tags:
        if re.search(reraaga, tg):
            r.append(parse_raaga(tg))
        if re.search(retaala, tg):
            t.append(parse_taala(tg))
    rfp = open("raaga_list", "w")
    tfp = open("taala_list", "w")
    for ra in sorted(list(set(r))):
        try:
            Raaga.objects.fuzzy(ra)
        except Raaga.DoesNotExist:
            rfp.write("%s\n" % ra)
    for ta in sorted(list(set(t))):
        try:
            Taala.objects.fuzzy(ta)
        except Taala.DoesNotExist:
            tfp.write("%s\n" % ta)
    rfp.close()
    tfp.close()


if __name__ == "__main__":
    main()
