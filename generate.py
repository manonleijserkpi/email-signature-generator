#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2015  Matthias Kolja Miehl
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
DESCRIPTION: Python script for generating email signatures from
             a single (HTML) template for all employees at once
UPDATES    : https://github.com/makomi/email-signature-generator
"""


# -----------------------------------------------------------------------------

# include libraries and set defaults
import os, shutil, errno
from configparser import ConfigParser, ExtendedInterpolation
from string import Template
import requests
import pandas as pd
from bs4 import BeautifulSoup

outputFolder    = "C:/Users/ManonLeijser/Python handtekening automatiseren/email-signature-generator/output"
releaseFolder   = "" # e.g. "in use
fileData        = "C:/Users/ManonLeijser/Python handtekening automatiseren/email-signature-generator/data.cfg"
fileTemplateSig = "C:/Users/ManonLeijser/Python handtekening automatiseren/email-signature-generator/signature.template.html"
websitePage = "https://kpisolutions.nl/over-kpi-solutions/"
bannerPage = "https://kpisolutions.nl/webinars/"
resultImages = requests.get(websitePage)
resultWebinars = requests.get(bannerPage)

# -----------------------------------------------------------------------------

# get photos from kpi page
# parse page into BeautifulSoup object
if resultImages.status_code == 200:
    soupImages = BeautifulSoup(resultImages.content, "html.parser")

# find photo objects
images = soupImages.find_all('div',{'class':'elementor-cta__bg elementor-bg'})

# for every image in the data file, write the data file away
for image in images:
    image = str(image)
    html = soupImages.contents
    # with open("output1.html", "w") as file:
    result = open("image.html", "w")
    result.write(image)

# -----------------------------------------------------------------------------

# get webinars from kpi page
if resultWebinars.status_code == 200:
    soupWebinars = BeautifulSoup(resultWebinars.content, "html.parser")

# find webinar objects
webinars = soupWebinars.find_all('div',{'class':'elementor-cta'})

for webinar in webinars:
    webinar = str(webinar)
    html = soupWebinars.contents
    result = open("webinar.html", "w")
    result.write(webinar)

# -----------------------------------------------------------------------------

# let user read the script's output
input("Finished!")
