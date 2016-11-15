from constants import *
import os

# Process in background (non-blocking)
def get_background_command(background):
    return " &" if background else ""

# Tokenizer script
def get_tokenize_command(mdir, language, in_file, out_file, background=False):
    amp = get_background_command(background)
    return "%s -l %s < %s > %s %s\n" % (tokenizer % mdir, language, in_file, out_file, amp)

# Truecaser train script
def get_truecaser_train_command(mdir, corpus, background=False):
    amp = get_background_command(background)
    return "%s --model %s --corpus %s %s\n" % (truecaser_train % mdir, model % mdir, corpus, amp)

# Truecaser script
def get_truecaser_command(mdir, in_file, out_file, background=False):
    amp = get_background_command(background)
    return "%s --model %s < %s > %s %s\n" % (truecaser % mdir, model % mdir, in_file, out_file, amp)

# Cleaner script
def get_cleaner_command(mdir, in_lang, out_lang, in_file, out_file, background=False):
    amp = get_background_command(background)
    return "%s %s %s %s %s 1 80 %s\n" % (cleaner % mdir, in_file, out_lang, in_lang, out_file, amp)

# LM training script
def get_lmtrain_command(mdir, language, in_file, out_file, background=False):
    amp = get_background_command(background)
    return "%s < %s > %s %s\n" % (lm_train % mdir, in_file, out_file, amp)

# Binarize LM training script
def get_blmtrain_command(mdir, language, in_file, out_file, background=False):
    amp = get_background_command(background)
    return "%s %s %s %s\n" % (blm_train % mdir, in_file, out_file, amp)

# Train MT system.
def get_tmtrain_command(mdir, in_lang, out_lang, lm_file, corpus, output_dir, background=False):
    # print "output dir:", output_dir
    # print "current path:", os.getcwd()
    amp = get_background_command(background)
    cmd = tm_train % mdir
    cmd += " -cores 6 -corpus " + corpus + " -f " + in_lang + " -e " + out_lang
    cmd += " -alignment grow-diag-final-and -reordering msd-bidirec"
    cmd += "tional-fe -lm 0:3:" + lm_file.replace("~", "$HOME")
    cmd += " -external-bin-dir " + mdir + "/scripts >& " + output_dir + "/" + train_fn
    return cmd + amp + "\n"

# Run the decoder.
def get_test_command(mdir, moses_ini, in_file, out_file, background=False):
    amp = get_background_command(background)
    return "%s %s < %s > %s %s\n" % (test % mdir, moses_ini, in_file, out_file, amp)