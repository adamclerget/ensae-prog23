from graph import min_power_mst, graph_from_file

''' Pour chaque route, appliquer min power pour avoir la puissance minimale requise puis trouver le modèle le moins cher ayant au minimum cette puissance,
créer en sortie une liste Couples où le k-ieme élément correspond à la k-ième route [utilité de la route, meilleur prix du camion] '''

g = open("home/onyxia/work/ensae-prog23/input/routes.1.in",'r')
a = g.readline()
Couples = []
for i in range(a):
    z = g.readline()
# Chercher l'emplacement des " " dans la ligne pour sélectionner les éléments
    espaces = []
    for p in range(len(z)):
        if z[p] == " ":
            espaces.append(p)
# Chercher la puissance minimale pour traverser la route
    graph = graph_from_file('home/onyxia/work/ensae-prog23/input/network.1.in')
    Minimum = min_power_mst(graph, z[:espaces[0]], z[(espaces[0]+1):espaces[1]])
# Lister les prix des camions suffisament puissants pour cette traversée, puis garder le minimum
    f = open("home/onyxia/work/ensae-prog23/input/trucks.1.in", 'r')
    nb_camions = f.readline()
    prix_camions_assez_puissants = []
    for i in range(nb_camions):
        infoscamion = f.readline()
        esp = infoscamion.index(" ")
        if infoscamion[0:esp-1] >= Minimum:
            prix_camions_assez_puissants.append(infoscamion[esp+1:]) 
    meilleur_prix = min(prix_camions_assez_puissants)
    f.close()
    q = [z[(espaces[1]+1):], meilleur_prix]
    Couples[i] = q

'''Méthode du sac à dos pour savoir quels couples de routes-camions privilégier pour maximiser le profit pour un budget donné'''

# Attribution d'un score à chaque ensemble route-camion optimal dans une liste Scores avec chaque élément : [score, coût, numéro route]

Scores = [0]*len(Couples)

for i in len(Couples):
    sco_i = Couples[i][0]/Couples[i][1]
    prix_i = Couples[i][1]
    Scores[i]=[sco_i, prix_i, i+1]

Scores_tries = sorted(Scores, key=lambda x: x[0])  # Triage par score décroissant

# Voir jusqu'ou on peut dépenser

Budget = 25 * 10**9
depense = 0

for i in range(Scores_tries):
    while depense < Budget:
        depense += Scores_tries[i][1]
        print('Il faut commander 1 camion à'+str(Scores_tries[i][1])+'euros'+'pour la route numéro'+str(Scores_tries[i][2]))
