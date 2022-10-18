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

outputFolder    = r"C:\Users\ManonLeijser\Python handtekening automatiseren Manon\email-signature-generator\output"
releaseFolder   = "" # e.g. "in use
fileData        = r"C:\Users\ManonLeijser\Python handtekening automatiseren Manon\data.cfg"
fileTemplateSig = r"C:\Users\ManonLeijser\Python handtekening automatiseren Manon\setup.html"
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
numberImages = 1

# for every image in the data file, write the data file away
for image in images:
    image = str(image)
    numberImages = str(numberImages)
    html = soupImages.contents
    result = open("image" + numberImages + ".html", "w")
    result.write(image)
    numberImages = int(numberImages)
    numberImages += 1

# -----------------------------------------------------------------------------

# get webinars from kpi page
if resultWebinars.status_code == 200:
    soupWebinars = BeautifulSoup(resultWebinars.content, "html.parser")

# find webinar objects
webinars = soupWebinars.find_all('div',{'class':'elementor-cta'})
numberWebinars = 1

for webinar in webinars:
    webinar = str(webinar)
    numberWebinars = str(numberWebinars)
    html = soupWebinars.contents
    result = open("webinar" + numberWebinars +  ".html", "w")
    result.write(webinar)
    numberWebinars = int(numberWebinars)
    numberWebinars += 1

# -----------------------------------------------------------------------------

# access configuration
def ConfigSectionMap(section):
    dict1={}
    options = cfg.options(section)
    for option in options:
        try:
            dict1[option] = cfg[section][option]
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            # not part of the template
            print("exception on '%s!'" % option)
            dict1[option] = None
    return dict1

# create a directory
def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

# set up output folder
if not os.path.isdir(outputFolder):
    mkdir(outputFolder)
else:
    # else: delete all files (old signatures) in output directory
    for content in os.listdir(outputFolder):
        path = os.path.join(outputFolder, content)
        try:
            if os.path.isfile(path):
                os.unlink(path)
            #elif os.path.isdir(path): shutil.rmtree(path)
        except:
            print("exception on '%s'!" % path)


# create folder for the files that are in use
if releaseFolder != "" and not os.path.isdir(releaseFolder):
    mkdir(releaseFolder)
# read in template and data file
fpTemplate = open(r"C:\Users\ManonLeijser\Python handtekening automatiseren Manon\hubspotSignature.html")
src = Template(fpTemplate.read())

cfg = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)
cfg.read(r"C:\Users\ManonLeijser\Python handtekening automatiseren Manon\data.cfg")

# for every person in the data file
for person in cfg.sections():
    photo = ConfigSectionMap(person)["photo"]
    first_name =  ConfigSectionMap(person)["first_name"]
    last_name =  ConfigSectionMap(person)["last_name"]
    function =  ConfigSectionMap(person)["function"]
    team =  ConfigSectionMap(person)["team"]
    custom =  ConfigSectionMap(person)["custom"]
    mobile =  ConfigSectionMap(person)["mobile"]
    email =  ConfigSectionMap(person)["email"]

    # assemble dataset for signature
    d = {
        'photo':photo,
        'first_name':first_name,
        'last_name':last_name,
        'function':function,
        'team':team,
        'custom':custom,
        'mobile':mobile,
        'email':email
    }

    # substitute variables in template, save as result
    result = src.substitute(d)

    #write result to a file named like the current section
    fpResult = open(outputFolder + "/" + person + ".html", 'w')
    fpResult.write(result)
    fpResult.close()

# -----------------------------------------------------------------------------

# let user read the script's output
input("Finished!")
