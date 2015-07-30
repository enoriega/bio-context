import pickle
print "Reading dictionaries"

# Load the dictionaries
with open('species_dict.pickle') as f,\
    open('organ_dict.pickle') as g,\
    open('celllines_dict.pickle') as h:
    lu_species = pickle.load(f)
    lu_organs = pickle.load(g)
    lu_celllines = pickle.load(h)

def resolve(type, text):
    if type == "species":
        if text in lu_species:
            return lu_species[text]
        else:
            return None
    elif type == 'organ':
        if text in lu_organs:
            return lu_organs[text]
        else:
            return None
    elif type == 'cellline':
        if text in lu_celllines:
            return lu_celllines[text]
        else:
            return None
    else:
        return None
