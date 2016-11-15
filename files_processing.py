# !/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
#
# PyKeylogger: TTT for Linux and Windows
# Copyright (C) 2016 Roxana Lafuente <roxana.lafuente@gmail.com>
#                    Miguel Lemos <miguelemosreverte@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from constants import train_fn
import os

# Get tokenizer output filename
def generate_input_tok_fn(language, outputdir):
    return outputdir + "/input.tok." + language

def generate_lm_tok_fn(outputdir):
    return outputdir + "/lm.tok"

# Get truecaser output filename
def generate_input_true_fn(language, outputdir):
    return outputdir + "/input.true." + language

def generate_lm_true_fn(outputdir):
    return outputdir + "/lm.true"

# Get cleaner output filename
def generate_input_clean_fn(outputdir):
    return outputdir + "/input.clean"

# Get language model training output filename
def generate_lm_fn(outputdir):
    # In: news-commentary-v8.fr-en.arpa.en
    # Out: news-commentary-v8.fr-en.blm.en
    return outputdir + "/lm.arpa"

# Get binarized language model training output filename
def generate_blm_fn(outputdir):
    # In: news-commentary-v8.fr-en.arpa.en
    # Out: news-commentary-v8.fr-en.blm.en
    return outputdir + "/lm.blm"

# Get translation model training output filename
def generate_tm_fn(outputdir):
    # In: news-commentary-v8.fr-en.arpa.en
    # Out: news-commentary-v8.fr-en.blm.en
    return outputdir + train_fn