try:
    import os
except:
    print "Dependency unfulfilled, please install os library"
    exit(1)

# Language codes.
ENG = "en"
FR = "fr"
DE = "de"

def adapt_path_for_cygwin(is_windows, directory):
    assert len(directory) > 0
    adapted_directory = "/cygdrive/"
    if is_windows:
        if directory[1:3] == ":\\":
            adapted_directory += directory[0] + "/" + directory[3:].replace("\\", "/")
        else:
            adapted_directory = directory.replace("\\", "/")
    else:
        adapted_directory = directory
    return adapted_directory

# Languages we show in the GUI to work with Moses.
languages = [ENG, FR, DE]

# Config file where info from Moses is saved.
moses_dir_fn = "moses.config"

# Filenames.
train_fn = "training.out"

# Check OS
is_win = os.name == 'nt'

# Moses commands
tokenizer = adapt_path_for_cygwin(is_win, "%s/scripts/tokenizer/tokenizer.perl ")

truecaser_train = adapt_path_for_cygwin(is_win, "%s/scripts/recaser/train-truecaser.perl ")
model = adapt_path_for_cygwin(is_win, "%s/truecase-model.en")

truecaser = adapt_path_for_cygwin(is_win, "%s/scripts/recaser/truecase.perl ")

cleaner = adapt_path_for_cygwin(is_win, "%s/scripts/training/clean-corpus-n.perl ")

lm_train = adapt_path_for_cygwin(is_win, "%s/bin/lmplz ") + "-o 3 " # TODO: Should be chosen by the user.

blm_train = adapt_path_for_cygwin(is_win, "%s/bin/build_binary ")

tm_train = "nohup nice " + adapt_path_for_cygwin(is_win, "%s/scripts/training/train-model.perl") + " -root-dir train "

test = adapt_path_for_cygwin(is_win, "%s/bin/moses") + " -f "