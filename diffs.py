import difflib

def get_insertion_and_deletions(original, modified):
    s = difflib.SequenceMatcher(None, original, modified)
    insertions = []
    deletions = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == "insert" or tag == "replace":insertions.append((j1,j2))
        if tag == "delete"or tag == "replace": deletions.append((i1,i2))
    return (insertions,deletions)
