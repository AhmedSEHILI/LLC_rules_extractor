from rdflib import Graph, URIRef, Literal
from rdflib.namespace import XSD


# chargement de l'ontologie
g = Graph()
g.parse("LLCdata/onto.ttl", format="turtle")



# partie 1: conversion en tsv

def clean_value(value):
    """
    Nettoie une valeur en supprimant les retours à la ligne et les tabulations.
    """
    if value is None or str(value).strip() == "":
        return "none"  # Remplace les valeurs vides par 'None'
    return str(value).replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()


# ecriture sous format tsv
with open("./LLCdata/ontoTSV.tsv", "w") as f:
    for subj, pred, obj in g:
        # Nettoyer chaque composant
        subj_str = clean_value(subj)
        pred_str = clean_value(pred)
        obj_str = clean_value(obj)
        # Écrire dans le fichier TSV
        f.write(f"{subj_str}\t{pred_str}\t{obj_str}\n")

print("conversion en tsv OK")



# partie 2: extraction des litteraux numériques présents dans l'ontologie

# definition des types numériques supportés par rdflib
types_numeriques = {XSD.integer, XSD.float, XSD.decimal, XSD.double, XSD.date, XSD.dateTime}

# extraction des prédicats qui ont des littéraux numériques 
mon_ensemble = set()
for subj, pred, obj in g:
    if isinstance(obj, Literal) and obj.datatype in types_numeriques:
        mon_ensemble.add(subj)

# ecrire les prédicats dans un fichier
with open("LLCdata/numericalLLC.tsv", "w") as f:
    for pred in mon_ensemble:
        f.write(f"{pred}\n")

print("extraction des prédicats numériques OK")
