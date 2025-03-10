# LLC_rules_extractor
Projet d'extraction de règles pour la maladie LLC
## Requete SPARQL Question 5 
```sparql
#Enumérer tous les triplets de l'ontologie
SELECT ?s ?p ?o
	WHERE { 
	?s ?p ?o
	}
ORDER BY ASC(?r1)

```
