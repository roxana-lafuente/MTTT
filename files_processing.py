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