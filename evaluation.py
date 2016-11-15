#!/usr/bin/env python

import subprocess
import os
import platform

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def filterTER (line):
    if "Total TER:" in line:
        line = line.replace("Total TER:", "")
        line = line.split('(', 1)[0]
        line += "\n"
        return line
    else:
        return ''

def filterBLEU (line, BLEU_type):
    if BLEU_type == "BLEU":      line = line.split(',', 1)[0]
    if BLEU_type == "BLEU2GRAM": line = line.split(',', 1)[1].split('/')[0]
    if BLEU_type == "BLEU3GRAM": line = line.split(',', 1)[1].split('/')[1]
    if BLEU_type == "BLEU4GRAM": line = line.split(',', 1)[1].split('/')[2]
    return line

def filter_verbose_output(output,method):
    specific_line = ""
    while True:
      line = output.stdout.readline()
      if line != '':
        if method == "TER": filtered_line = filterTER(line)
        #add more complicated methods to filter over here

        if filtered_line != '':
            specific_line = filtered_line
      else:
        break
    return specific_line

cached_results = {}

def evaluate(checkbox_indexes, test, reference):
    checkbox_indexes_constants = ["WER","PER","HTER", "GTM", "BLEU","BLEU2GRAM","BLEU3GRAM","BLEU4GRAM"]
    DIRECTORY = "./evaluation_scripts/"
    TER_DIRECTORY = DIRECTORY + "tercom-0.7.25/src/"
    GTM_DIRECTORY = DIRECTORY + "gtm-1.4/"
    EXEC_PERL = "perl "
    EXEC_JAVA = "java "
    return_results = ""
    checkbox_index = 0
    BLEU_cached_results = ""
    for checkbox in checkbox_indexes:
        if checkbox:
            key = (test,creation_date(test),reference,creation_date(reference), checkbox_indexes_constants[checkbox_index])
            if key in cached_results: return_results += cached_results[key]
            else:
                if checkbox_indexes_constants[checkbox_index] == "WER" or checkbox_indexes_constants[checkbox_index] == "PER":
                    command = EXEC_PERL + DIRECTORY +  checkbox_indexes_constants[checkbox_index] + ".pl" + " -t " + test + " -r " + reference
                    proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
                    result = "\n" + checkbox_indexes_constants[checkbox_index] + "..... " + proc.stdout.read()
                    return_results += result
                    cached_results[key] =  result

                if checkbox_indexes_constants[checkbox_index] == "HTER":
                    command_2 = EXEC_JAVA + "-cp " + TER_DIRECTORY + " TERtest " + " -r " + reference + " -h " + test
                    proc = subprocess.Popen(command_2, shell=True,stdout=subprocess.PIPE)
                    result = "\n" + checkbox_indexes_constants[checkbox_index] + "....." + filter_verbose_output(proc,"TER")
                    return_results += result
                    cached_results[key] =  result


                if checkbox_indexes_constants[checkbox_index] == "GTM":
                    command_2 = EXEC_JAVA + "-cp " + GTM_DIRECTORY + " gtm" + " -t " +  test + " " + reference
                    proc = subprocess.Popen(command_2, shell=True,stdout=subprocess.PIPE)
                    result = "\n" + checkbox_indexes_constants[checkbox_index] + "....." + filter_verbose_output(proc,"GTM")
                    return_results += result
                    cached_results[key] =  result

                if "BLEU" in checkbox_indexes_constants[checkbox_index] and BLEU_cached_results == "":
                    command = EXEC_PERL + DIRECTORY + "BLEU.pl " + test +" < " + reference
                    proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
                    while True:
                      line = proc.stdout.readline()
                      if line != '':BLEU_cached_results += line
                      else: break

                if "BLEU" in checkbox_indexes_constants[checkbox_index]:
                    result = "\n" + checkbox_indexes_constants[checkbox_index] + "..... "\
                        + filterBLEU(BLEU_cached_results,checkbox_indexes_constants[checkbox_index])
                    return_results += result
                    cached_results[key] =  result


        checkbox_index += 1
    return_results
    return return_results
