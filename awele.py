# - - - - - - - - - - - - - - - TYPES UTILISES
# POSITION : dictionnaire non vide qui contient différentes informations sur
#            une position d'Awélé, associées au nom de leur champ.
# COUP : valeur entière comprise entre 1 et le nombre de colonnes du tablier

# - - - - - - - - - - - - - - - INITIALISATION
def initialise(n):
    """ int -> POSITION
        Hypothèse : n > 0
        initialise la position de départ de l'awélé avec n colonnes
        avec 4 dans chaque case.
    """
    position = dict()                                 # initialisation
    position['tablier'] = [4 for k in range(0, 2*n)]  # on met 4 graines dans chaque case
    position['taille'] = n                            # le nombre de colonnes du tablier
    position['trait'] = 'SUD'                         # le joueur qui doit jouer: 'SUD' ou 'NORD'
    position['graines'] = {'SUD':0, 'NORD':0}         # graines prises par chaque joueur
    return position

# - - - - - - - - - - - - - - - AFFICHAGE (TEXTE)
def affichePosition(position):
    """ POSITION ->
        affiche la position de façon textuelle
    """
    print('\t* * * * * * * * TABLIER * * * * * * * * *')
    n = position['taille']
    buffer = 'Col:'
    for i in range(0,n):
        buffer += '\t ' + str(i+1)
    print(buffer)
    print('\t\t     NORD (prises: ' + str(position['graines']['NORD']) + ')')
    print('\t-------------------------------------------')
    buffer = ''
    for i in range(2*n-1,n-1,-1):   # indices n..(2n-1) pour les cases NORD
        buffer += '\t[' + str(position['tablier'][i]) + ']'
    print(buffer)
    buffer = ''
    for i in range(0,n):            # indices 0..(n-1) pour les cases SUD
        buffer += '\t[' + str(position['tablier'][i]) + ']'
    print(buffer)
    print('\t-------------------------------------------')
    print('\t\t     SUD (prises: ' + str(position['graines']['SUD']) + ')')
    print('-> Camp au trait: ' + position['trait'] + '\n');

# - - - - - - - - - - - - - - - CLONAGE
import copy
def clonePosition(position):
    """ POSITION -> POSITION
        retourne un clone de la position
        (qui peut être alors modifié sans altérer l'original donc).
    """
    leclone = dict()
    leclone['tablier'] = copy.deepcopy(position['tablier'])
    leclone['taille']  = position['taille']
    leclone['trait']   = position['trait']
    leclone['graines'] =  copy.deepcopy(position['graines'])
    return leclone

# - - - - - - - - - - - - - - - JOUE UN COUP
def joueCoup(position,coup):
    """ POSITION * COUP -> POSITION
        Hypothèse: coup est jouable.

        Retourne la position obtenue une fois le coup joué.
    """
    nouvelle_pos = clonePosition(position)   # on duplique pour ne pas modifier l'original
    n = nouvelle_pos['taille']
    trait = nouvelle_pos['trait']
    # on transforme coup en indice
    if trait == 'SUD':
        indice_depart = coup-1
    else:
        indice_depart = 2*n-coup
    # retrait des graines de la case de départ
    nbGraines = nouvelle_pos['tablier'][indice_depart]
    nouvelle_pos['tablier'][indice_depart] = 0
    # on sème les graines dans les cases à partir de celle de départ
    indice_courant = indice_depart
    while nbGraines > 0:
        indice_courant = (indice_courant + 1) % (2*n)
        if (indice_courant != indice_depart):              # si ce n'est pas la case de départ
            nouvelle_pos['tablier'][indice_courant] += 1   # on sème une graine
            nbGraines -= 1
    # la case d'arrivée est dans le camp ennemi ?
    if (trait == 'NORD'):
        estChezEnnemi = (indice_courant < n)
    else:
        estChezEnnemi = (indice_courant >= n)
    # réalisation des prises éventuelles
    while estChezEnnemi and (nouvelle_pos['tablier'][indice_courant] in range(2,4)):
        nouvelle_pos['graines'][trait] += nouvelle_pos['tablier'][indice_courant]
        nouvelle_pos['tablier'][indice_courant] = 0
        indice_courant = (indice_courant - 1) % (2*n)
        if (trait == 'NORD'):
            estChezEnnemi = (indice_courant < n)
        else:
            estChezEnnemi = (indice_courant >= n)
    # mise à jour du camp au trait
    if trait == 'SUD':
        nouvelle_pos['trait'] = 'NORD'
    else:
        nouvelle_pos['trait'] = 'SUD'
    return nouvelle_pos
    
def joueCoup_v2(position,coup):
    """ POSITION * COUP -> POSITION
        Hypothèse: coup est jouable.

        Retourne la position obtenue une fois le coup joué.
        V2 : Ajout de la règle additionnelle : pas de prise si le coup affame
        l'ennemi, mais les graines sont semées.
    """
    nouvelle_pos = clonePosition(position)   # on duplique pour ne pas modifier l'original
    n = nouvelle_pos['taille']
    trait = nouvelle_pos['trait']
    # on transforme coup en indice
    if trait == 'SUD':
        indice_depart = coup-1
    else:
        indice_depart = 2*n-coup
    # retrait des graines de la case de départ
    nbGraines = nouvelle_pos['tablier'][indice_depart]
    nouvelle_pos['tablier'][indice_depart] = 0
    # on sème les graines dans les cases à partir de celle de départ
    indice_courant = indice_depart
    while nbGraines > 0:
        indice_courant = (indice_courant + 1) % (2*n)
        if (indice_courant != indice_depart):              # si ce n'est pas la case de départ
            nouvelle_pos['tablier'][indice_courant] += 1   # on sème une graine
            nbGraines -= 1
    
    position_avant_prise = clonePosition(nouvelle_pos)    
    
    # la case d'arrivée est dans le camp ennemi ?
    # on en profite pour compter les graines de l'ennemi
    if (trait == 'NORD'):
        estChezEnnemi = (indice_courant < n)
        nbGrainesEnnemi = 0
        for i in range(0,n):            # indices 0..(n-1) pour les cases SUD
            nbGrainesEnnemi += nouvelle_pos['tablier'][i]
    else:
        estChezEnnemi = (indice_courant >= n)
        nbGrainesEnnemi = 0
        for i in range(2*n-1,n-1,-1):   # indices n..(2n-1) pour les cases NORD
            nbGrainesEnnemi += nouvelle_pos['tablier'][i]
            
    nbGrainesAvantPrise = nouvelle_pos['graines'][trait]
    
    # réalisation des prises éventuelles
    while estChezEnnemi and (nouvelle_pos['tablier'][indice_courant] in range(2,4)):
        nouvelle_pos['graines'][trait] += nouvelle_pos['tablier'][indice_courant]
        nouvelle_pos['tablier'][indice_courant] = 0
        indice_courant = (indice_courant - 1) % (2*n)
        if (trait == 'NORD'):
            estChezEnnemi = (indice_courant < n)
        else:
            estChezEnnemi = (indice_courant >= n)
            
    nbGrainesApresPrise = nouvelle_pos['graines'][trait]
    
    # si on affame l'ennemi avec cette prise alors on annule cette prise
    if nbGrainesApresPrise - nbGrainesAvantPrise == nbGrainesEnnemi:
        # on redonne les graines prises à l'adversaire tout en laissant ce qui avait été semé (position avant la prise)
        if (trait == 'NORD'):
            for i in range(0,n):            # indices 0..(n-1) pour les cases SUD
                nouvelle_pos['tablier'][i] = position_avant_prise['tablier'][i]
        else:
            for i in range(2*n-1,n-1,-1):   # indices n..(2n-1) pour les cases NORD
                nouvelle_pos['tablier'][i] = position_avant_prise['tablier'][i]
        
        nouvelle_pos['graines'][trait] = position_avant_prise['graines'][trait]
    
    # mise à jour du camp au trait
    if trait == 'SUD':
        nouvelle_pos['trait'] = 'NORD'
    else:
        nouvelle_pos['trait'] = 'SUD'
    return nouvelle_pos

def coupJouable(position,nombre):
    """ POSITION * int -> bool

        Indique si le nombre donné est jouable dans la position donnée.
    """
    n = position['taille']
    
    # nombre est un entier compris entre 1 et n
    if nombre >= 1 and nombre <= n and isinstance(nombre, int):
        trait = position['trait']
        # on transforme coup en indice
        if trait == 'SUD':
            indice = nombre-1
        else:
            indice = 2*n-nombre
            
        # la case correspondante contient-elle au moins 1 graine
        if position['tablier'][indice] > 0:
            return True
        else:
            return False
    else:
        return False

def coupAutorise(position,coup):
    """ POSITION * int -> POSITION ou bool

        Indique si le coup donné est autorisé dans la position donnée.
    """
    if not coupJouable(position,coup):
        return False
    else:
        n = position['taille']
        trait = position['trait']
        new_position = joueCoup(position,coup) # le coup est joué et donne une nouvelle position
        
        # comptage des graines de chaque camp dans la nouvelle position
        nbGrainesNORD = 0
        for i in range(2*n-1,n-1,-1):   # indices n..(2n-1) pour les cases NORD
            nbGrainesNORD += new_position['tablier'][i]
        nbGrainesSUD = 0
        for i in range(0,n):            # indices 0..(n-1) pour les cases SUD
            nbGrainesSUD += new_position['tablier'][i]
        
        # vérification de la légalité de la nouvelle position grâce au nombre 
        # de graines de chaque camp par rapport à celui qui a joué le coup
        if trait == 'SUD' and nbGrainesNORD == 0:
            return False
        elif trait == 'SUD' and nbGrainesNORD > 0:
            return new_position
        elif trait == 'NORD' and nbGrainesSUD == 0:
            return False
        elif trait == 'NORD' and nbGrainesSUD > 0:
            return new_position

def coupAutorise_v2(position,coup):
    """ POSITION * int -> POSITION ou bool

        Indique si le coup donné est autorisé dans la position donnée.
        V2 : Ajout de la règle additionnelle : un coup affamant devient
        autorisé, joueCoup_v2 gérera la situation.
        Du coup, coupAutorise_v2 = coupJouable.
    """
    if not coupJouable(position,coup):
        return False
    else:
        return joueCoup_v2(position,coup) # le coup est joué et donne une nouvelle position

def positionTerminale(position):
    """ POSITION -> bool

        Indique si la position est terminale (plus aucun coup jouable).
        ATTENTION : on prend en compte ici la règle additionnelle.
    """
    n = position['taille']
    
    # on regarde si au moins un coup est possible
    nbCoupsAutorises = 0
    for i in range(1,n+1):
        if coupAutorise_v2(position,i) != False:
            nbCoupsAutorises += 1
            break # inutile d'aller plus loin
    
    if nbCoupsAutorises == 0 or position['graines']['NORD'] >= 25 or position['graines']['SUD'] >= 25:
        return True
    else:
        return False      

def moteurHumains():
    """ 
        Permet à deux joueurs humains de s'affronter.
    """
    position = initialise(6) # initialisation nouvelle partie
    partieFinie = False
    
    while not partieFinie:
        affichePosition(position)
        trait = position['trait']
        print("Joueur ", trait, ", entrez votre coup : ")
        saisie = input() # la fonction input renvoie une chaîne de caractères
        coup = int(saisie) # conversion de la chaîne en un nombre entier
        
        new_position = coupAutorise_v2(position,coup) # vérification du coup
        
        # on harcèle le joueur s'il ne donne pas un coup valide
        while not new_position:
            print("Joueur ", trait, ", coup impossible")
            print("Joueur ", trait, ", entrez votre coup : ")
            saisie = input()
            coup = int(saisie)
            new_position = coupAutorise_v2(position,coup)
        
        if positionTerminale(new_position):
            partieFinie = True
        
        position = clonePosition(new_position)
    
    affichePosition(position)
    if position['trait'] == 'SUD':
        print('Partie finie, joueur NORD vainqueur');
    else:
        print('Partie finie, joueur SUD vainqueur');

import random
def choixAleatoire(position):
    """ POSITION -> int

        Retourne aléatoirement un coup autorisé pour une position donnée.
    """
    n = position['taille']
    coups_autorises = []
    
    for i in range(1,n+1):
        if coupAutorise(position,i) != False:
            coups_autorises.append(i)
    
    # si aucun coup autorisé n'est possible, on renvoie 0
    if len(coups_autorises) == 0:
        return 0
    # sinon on choisit le coup de façon aléatoire parmi les coups autorisés
    else:
        return random.choice(coups_autorises)

def moteurAleatoire(campCPU):
    """ string ->
    
        Permet à un joueur humain d'affrontrer l'ordinateur qui joue
        aléatoirement ses coups.
    """
    position = initialise(6) # initialisation nouvelle partie
    partieFinie = False
    
    while not partieFinie:
        affichePosition(position)
        trait = position['trait']
        
        if trait == campCPU:
            coup_aleatoire = choixAleatoire(position)
            
            # si aucun coup autorisé n'est possible, la partie s'arrête
            if coup_aleatoire == 0:
                partieFinie == True
            else:
                new_position = joueCoup(position,coup_aleatoire)
            
        else:
            print("Joueur humain, entrez votre coup : ")
            saisie = input() # la fonction input renvoie une chaîne de caractères
            coup = int(saisie) # conversion de la chaîne en un nombre entier
            
            new_position = coupAutorise(position,coup) # vérification du coup
            
            # on harcèle le joueur s'il ne donne pas un coup valide
            while not new_position:
                print("Joueur humain, coup impossible")
                print("Joueur humain, entrez votre coup : ")
                saisie = input()
                coup = int(saisie)
                new_position = coupAutorise(position,coup)
        
        if positionTerminale(new_position):
            partieFinie = True
    
        position = clonePosition(new_position)
    
    affichePosition(position)
    if position['trait'] == 'SUD':
        print('Partie finie, joueur NORD vainqueur');
    else:
        print('Partie finie, joueur SUD vainqueur');

def evaluation(position):
    """ POSITION -> int

        Donne l'évaluation d'une position donnée.
        IMPORTANT : plus l'évaluation est élevée, plus elle est favorable
        au camp SUD.
    """
    if positionTerminale(position):
        # il faut déterminer qui est le vainqueur
        if position['graines']['NORD'] >= 25:
            return -1000 # position gagnante pour NORD
        elif position['graines']['SUD'] >= 25:
            return 1000 # position gagnante pour SUD
        else:
            # le joueur ne peut pas jouer, toutes les graines restantes reviennent à l'adversaire
            n = position['taille']
            graines_restantes = 0
            for i in range(2*n-1,n-1,-1):   # indices n..(2n-1) pour les cases NORD
                graines_restantes += position['tablier'][i]
            for i in range(0,n):            # indices 0..(n-1) pour les cases SUD
                graines_restantes += position['tablier'][i]
            
            if position['trait'] == 'SUD':
                position['graines']['NORD'] += graines_restantes
            else:
                position['graines']['SUD'] += graines_restantes
                
            if position['graines']['NORD'] > position['graines']['SUD']:
                return -1000 # position gagnante pour NORD
            elif position['graines']['NORD'] < position['graines']['SUD']:
                return 1000 # position gagnante pour SUD
            else:
                return 0 # égalité, chaque joueur a le même nombre de graines
            
    else:
        return ( 2*fg(position,'SUD') + f12(position,'NORD') ) - ( 2*fg(position,'NORD') + f12(position,'SUD') )
        
def fg(position,camp):
    """ POSITION * str -> int

        Donne le nombre de graines déjà gagnées par le camp donné dans
        la position donnée.
    """        
    return position['graines'][camp]

def f12(position,camp):
    """ POSITION * str -> int

        Donne le nombre de cases du camp donné contenant 1 ou 2 graines dans
        la position donnée.
    """
    n = position['taille']
    nb_cases = 0
    
    if camp == 'SUD':
        for i in range(0,n):            # indices 0..(n-1) pour les cases SUD
            if position['tablier'][i] == 1 or position['tablier'][i] == 2:
                nb_cases += 1
    else:
        for i in range(2*n-1,n-1,-1):   # indices n..(2n-1) pour les cases NORD
            if position['tablier'][i] == 1 or position['tablier'][i] == 2:
                nb_cases += 1
    
    return nb_cases

import sys
minimax_node_count = 0
def evalueMinimax(position,prof):
    """ POSITION, int -> dict

        Retourne, pour une position et une profondeur donnée, le meilleur
        coup à jouer trouvé par l'algorithme MiniMax ainsi que
        l'évalutation de la position obtenue pour ce coup.
    """
    global minimax_node_count
    minimax_node_count += 1
    
    n = position['taille']
    meilleur_coup = 0
    meilleur_score = 0
    
    if positionTerminale(position) or prof == 0:
        meilleur_score = evaluation(position)
    
    else:
        # si c'est un noeud max (SUD est le camp maximisé par la fonction d'évaluation)
        # on calcule la valeur max des successeurs du noeud
        if position['trait'] == 'SUD':
            meilleur_score = -sys.maxsize
            # pour tous les coups autorisés
            for coup in range(1,n+1):
                new_position = coupAutorise(position,coup)
                if new_position != False:
                    score = evalueMinimax(new_position,prof-1)['valeur']
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = coup
        
        # sinon c'est un noeud min
        # on calcule la valeur min des successeurs du noeud
        else:
            meilleur_score = sys.maxsize
            # pour tous les coups autorisés
            for coup in range(1,n+1):
                new_position = coupAutorise(position,coup)
                if new_position != False:
                    score = evalueMinimax(new_position,prof-1)['valeur']
                    if score < meilleur_score:
                        meilleur_score = score
                        meilleur_coup = coup
    
    resultat = dict()
    resultat['coup'] = meilleur_coup
    resultat['valeur'] = meilleur_score
    
    return resultat

def choixMinimax(position,prof):
    """ POSITION, int -> int

        Retourne, pour une position et une profondeur donnée,
        le meilleur coup autorisé trouvé par l'algorithme MiniMax.
    """
    global minimax_node_count
    minimax_node_count = 0
    
    # ici on peut utiliser indifféremment evalueMinimax ou evalueNegaMax
    minimax = evalueMinimax(position,prof)
    print("Résultat minimax : ", minimax)
    return minimax['coup']

def moteurMinimax(campCPU,prof):
    """ str, int ->
    
        Permet à un joueur humain d'affrontrer
        l'ordinateur qui joue selon l'algorithme MiniMax.
    """
    position = initialise(6) # initialisation nouvelle partie
    partieFinie = False
    
    while not partieFinie:
        affichePosition(position)
        trait = position['trait']
        
        if trait == campCPU:
            coup_minimax = choixMinimax(position,prof)
            
            # si aucun coup autorisé n'est possible, la partie s'arrête
            if coup_minimax == 0:
                partieFinie == True
            else:
                new_position = joueCoup(position,coup_minimax)
            
        else:
            print("Joueur humain, entrez votre coup : ")
            saisie = input() # la fonction input renvoie une chaîne de caractères
            coup = int(saisie) # conversion de la chaîne en un nombre entier
            
            new_position = coupAutorise(position,coup) # vérification du coup
            
            # on harcèle le joueur s'il ne donne pas un coup valide
            while not new_position:
                print("Joueur humain, coup impossible")
                print("Joueur humain, entrez votre coup : ")
                saisie = input()
                coup = int(saisie)
                new_position = coupAutorise(position,coup)
        
        if positionTerminale(new_position):
            partieFinie = True
        
        position = clonePosition(new_position)
    
    affichePosition(position)
    if position['trait'] == 'SUD':
        print('Partie finie, joueur NORD vainqueur');
    else:
        print('Partie finie, joueur SUD vainqueur');
          
alphabeta_node_count = 0
def evalueAlphaBeta(position, prof, alpha, beta):
    """ POSITION, int, int, int -> dict

        Cette fonction retourne, pour une position et une profondeur donnée,
        le meilleur coup à jouer trouvé par l'algorithme AlphaBeta ainsi que
        l'évalutation de la position obtenue pour ce coup.
    """
    global alphabeta_node_count
    alphabeta_node_count += 1
    
    n = position['taille']
    resultat = dict()
    resultat['coup'] = 0
    
    if prof == 0 or positionTerminale(position): 
        resultat['valeur'] = evaluation(position)
    
    else:  
        if position['trait'] == 'SUD':
            for coup in range(1,n+1):
                new_position = coupAutorise(position,coup)
                if new_position != False:
                    score = evalueAlphaBeta(new_position,prof-1,alpha,beta)['valeur']
                    if score > alpha:
                        alpha = score
                        resultat['coup'] = coup
                    if beta <= alpha:
                        break # coupure beta
            resultat['valeur'] = alpha    
        
        else:
            for coup in range(1,n+1):
                new_position = coupAutorise(position,coup)
                if new_position != False:
                    score = evalueAlphaBeta(new_position,prof-1,alpha,beta)['valeur']
                    if score < beta:
                        beta = score
                        resultat['coup'] = coup
                    if beta <= alpha:
                        break # coupure alpha
            resultat['valeur'] = beta
    
    return resultat
    
def choixAlphaBeta(position,prof):
    """ POSITION, int -> int

        Cette fonction retourne, pour une position et une profondeur donnée,
        le meilleur coup autorisé trouvé par l'algorithme AlphaBeta.
    """
    global alphabeta_node_count
    alphabeta_node_count = 0
    
    # ici on peut utiliser indifféremment evalueAlphaBeta ou evalueNegaBeta
    alphabeta = evalueAlphaBeta(position,prof,-sys.maxsize,sys.maxsize)
    print("Résultat alphabeta : ", alphabeta)
    return alphabeta['coup']

def moteurAlphaBeta(campCPU,prof):
    """ str, int ->
    
        Cette fonction permet à un joueur humain d'affrontrer
        l'ordinateur qui joue selon l'algorithme AlphaBeta.
    """
    position = initialise(6) # initialisation nouvelle partie
    partieFinie = False
    new_position = clonePosition(position)
    
    while not partieFinie:
        affichePosition(position)
        trait = position['trait']
        
        if trait == campCPU:
            coup_alphabeta = choixAlphaBeta(position,prof)
            
            # si aucun coup autorisé n'est possible, la partie s'arrête
            if coup_alphabeta == 0:
                partieFinie = True
            else:
                new_position = joueCoup(position,coup_alphabeta)
            
        else:
            print("Joueur humain, entrez votre coup : ")
            saisie = input() # la fonction input renvoie une chaîne de caractères
            coup = int(saisie) # conversion de la chaîne en un nombre entier
            
            new_position = coupAutorise(position,coup) # vérification du coup
            
            # on harcèle le joueur s'il ne donne pas un coup valide
            while not new_position:
                print("Joueur humain, coup impossible")
                print("Joueur humain, entrez votre coup : ")
                saisie = input()
                coup = int(saisie)
                new_position = coupAutorise(position,coup)
        
        if positionTerminale(new_position):
            partieFinie = True
        
        position = clonePosition(new_position)
    
    affichePosition(position)
    if position['trait'] == 'SUD':
        print('Partie finie, joueur NORD vainqueur');
    else:
        print('Partie finie, joueur SUD vainqueur');

def evaluation_v2(position):
    """ POSITION -> int

        Cette fonction donne l'évaluation d'une position donnée.
        IMPORTANT : plus l'évaluation est élevée, plus elle est favorable au camp SUD.
    """
    if positionTerminale(position):
        # il faut déterminer qui est le vainqueur
        if position['graines']['NORD'] >= 25:
            return -1000
        elif position['graines']['SUD'] >= 25:
            return 1000
        else:
            # le joueur ne peut pas jouer, toutes les graines restantes reviennent à l'adversaire
            n = position['taille']
            graines_restantes = 0
            for i in range(2*n-1,n-1,-1):   # indices n..(2n-1) pour les cases NORD
                graines_restantes += position['tablier'][i]
            for i in range(0,n):            # indices 0..(n-1) pour les cases SUD
                graines_restantes += position['tablier'][i]
            
            if position['trait'] == 'SUD':
                position['graines']['NORD'] += graines_restantes
            else:
                position['graines']['SUD'] += graines_restantes
                
            if position['graines']['NORD'] > position['graines']['SUD']:
                return -1000
            elif position['graines']['NORD'] < position['graines']['SUD']:
                return 1000
            else:
                return 0 # égalité, chaque joueur a le même nombre de graines
            
    else:
        # On prend la différence des graines capturées par chaque joueur
        # mais pour prendre en compte l’avancement de la partie, cette 
        # différence est multipliée par le score de celui qui mène. 
        # Plus on va vers la fin de la partie, plus on a de graines 
        # capturées, et plus la valeur de la fonction d'évaluation augmente.
        n = position['taille']
        
        difference = position['graines']['SUD'] - position['graines']['NORD']
        
        # si SUD mène
        if difference > 0:
            return difference*position['graines']['SUD']
        # sinon NORD mène
        else:
            return difference*position['graines']['NORD']

def moteurIA_versus_IA(campCPU):
    """ int ->
    
        Permet de faire jouer le programme contre lui-même. Il est intéressant
        de donner des profondeurs différentes à chaque camp, ou même les faire
        utiliser chacun un algorithme différent.
        
        On ajoute ici une nouvelle règle de fin de partie :
            S'il ne reste que 6 graines en jeu, le gagnant est celui qui a le
            plus de graines prises.
        Cette règle n'est pas ajouté à la fonction positionTerminale par
        volonté de ne pas trop s'éloigner de l'énoncé d'origine.
        
        On compte à la fois le nombre de noeuds parcourus par l'algorithme
        alphabeta mais aussi le nombre de noeuds parcourus par l'algorithme 
        minimax. Cette fonction ne reflète donc pas la vitesse d'exécution du
        programme car elle fait tourner les deux algorithmes en même temps
        dans le but de comparer le nombre de noeuds parcourues.
    """
    n = 6
    position = initialise(n) # initialisation nouvelle partie
    partieFinie = False
    
    graines_restantes_tablier = 2*n*4 # 2 lignes de n cases remplies de 4 graines
    
    while not partieFinie and graines_restantes_tablier > 6:
        affichePosition(position)
        trait = position['trait']
        
        if trait == campCPU:
            coup_minimax = choixMinimax(position,4)
            coup_alphabeta = choixAlphaBeta(position,4)
            print("Coup choisi par minimax : ", coup_minimax)
            print("Coup choisi par alphabeta : ", coup_alphabeta)
            print("Nombre de noeuds parcourus par minimax : ", minimax_node_count)
            print("Nombre de noeuds parcourus par alphabeta : ", alphabeta_node_count)
            
            # si aucun coup autorisé n'est possible, la partie s'arrête
            if coup_alphabeta == 0:
                partieFinie == True
            else:
                new_position = joueCoup(position,coup_alphabeta)
                print('\n' + position['trait'] + ' joue le coup ', coup_alphabeta);
            
        else:
            coup_minimax = choixNegaMax(position,4)
            coup_alphabeta = choixNegaBeta(position,4)
            print("Coup choisi par minimax : ", coup_minimax)
            print("Coup choisi par alphabeta : ", coup_alphabeta)
            print("Nombre de noeuds parcourus par minimax : ", minimax_node_count)
            print("Nombre de noeuds parcourus par alphabeta : ", alphabeta_node_count)
            
            # si aucun coup autorisé n'est possible, la partie s'arrête
            if coup_alphabeta == 0:
                partieFinie == True
            else:
                new_position = joueCoup(position,coup_alphabeta)
                print('\n' + position['trait'] + ' joue le coup ', coup_alphabeta);
        
        if positionTerminale(new_position):
            partieFinie = True
    
        position = clonePosition(new_position)
        
        graines_restantes_tablier = 0
        
        for i in range(2*n-1,n-1,-1):   # indices n..(2n-1) pour les cases NORD
            graines_restantes_tablier += position['tablier'][i]
        for i in range(0,n):            # indices 0..(n-1) pour les cases SUD
            graines_restantes_tablier += position['tablier'][i]
            
    affichePosition(position)
    
    # si la partie s'arrête pas manque de graines sur le tablier
    if graines_restantes_tablier <= 6: 
        if position['graines']['SUD'] < position['graines']['NORD']:
            print('Partie finie, joueur NORD vainqueur');
        elif position['graines']['SUD'] > position['graines']['NORD']:
            print('Partie finie, joueur SUD vainqueur');
        else:
            print('Egalité')
    
    # sinon la partie s'est arrêtée de façon standard (position terminale)
    else:
        if position['trait'] == 'SUD':
            print('Partie finie, joueur NORD vainqueur');
        else:
            print('Partie finie, joueur SUD vainqueur');


def evalueNegaMax(position, prof):
    """ POSITION, int -> dict

        Variante de l'algorithme minimax, minimiser une valeur revient à
        maximiser l'opposé de celle-ci.
    """
    global minimax_node_count
    minimax_node_count += 1
    
    n = position['taille']
    resultat = dict()
    
    if prof == 0 or positionTerminale(position):
        if position['trait'] == 'SUD':
            resultat['valeur'] = evaluation(position)
        else:
            resultat['valeur'] = -evaluation(position)
    
    else:
        meilleur_score = -sys.maxsize
        meilleur_coup = 0
        
        for coup in range(1,n+1):
            if coupAutorise(position,coup) != False:
                new_position = joueCoup(position,coup) # on simule le coup
                score = -evalueNegaMax(new_position, prof-1)['valeur']
                if score >= meilleur_score:
                    meilleur_score = score;
                    meilleur_coup = coup;
        
        resultat['valeur'] = meilleur_score
        resultat['coup'] = meilleur_coup
                    
    return resultat
    
def choixNegaMax(position,prof):
    """ POSITION, int -> int

        Retourne, pour une position et une profondeur donnée,
        le meilleur coup autorisé trouvé par l'algorithme MiniMax sous
        convention NegaMax.
    """
    global minimax_node_count
    minimax_node_count = 0
    
    minimax = evalueNegaMax(position,prof)
    print("Résultat minimax : ", minimax)
    return minimax['coup']

def evalueNegaBeta(position, prof, alpha, beta):
    """ POSITION, int -> dict

        Variante de l'algorithme alphabeta avec la convention NegaMax.
    """
    global alphabeta_node_count
    alphabeta_node_count +=1
    
    n = position['taille']
    resultat = dict()
    
    if prof == 0 or positionTerminale(position):
        if position['trait'] == 'SUD':
            resultat['valeur'] = evaluation_v2(position)
        else:
            resultat['valeur'] = -evaluation_v2(position)
    
    else:
        meilleur_score = -sys.maxsize
        meilleur_coup = 0
        
        for coup in range(1,n+1):
            if coupAutorise(position,coup) != False:
                new_position = joueCoup(position,coup) # on simule le coup
                score = -evalueNegaBeta(new_position, prof-1, -beta, -alpha)['valeur']
                if score > meilleur_score:
                    meilleur_score = score;
                    meilleur_coup = coup;
                    if meilleur_score > alpha:
                        alpha = meilleur_score
                        if alpha >= beta:
                            break
        
        resultat['valeur'] = meilleur_score
        resultat['coup'] = meilleur_coup
                    
    return resultat

def choixNegaBeta(position,prof):
    """ POSITION, int -> int

        Cette fonction retourne, pour une position et une profondeur donnée,
        le meilleur coup autorisé trouvé par l'algorithme AlphaBeta sous
        convention NegaBeta.
    """
    global alphabeta_node_count
    alphabeta_node_count = 0
    
    alphabeta = evalueNegaBeta(position,prof,-sys.maxsize,sys.maxsize)
    print("Résultat alphabeta : ", alphabeta)
    return alphabeta['coup']  
    
# - - - - - - - - - - - - - - - TESTS

# ------------------------- TEST exemple
#maPosition = initialise(6)
#affichePosition(maPosition)
#maPosition2 = joueCoup(maPosition,1) # SUD joue
#maPosition2 = joueCoup(maPosition2,1) # NORD joue
#maPosition2 = joueCoup(maPosition2,2) # SUD joue
#maPosition2 = joueCoup(maPosition2,4) # NORD joue
#maPosition2 = joueCoup(maPosition2,3) # SUD joue
#maPosition2 = joueCoup(maPosition2,2) # NORD joue
#maPosition2 = joueCoup(maPosition2,5) # SUD joue
#affichePosition(maPosition2)
#print("------\nPartie sur un tablier réduit pour tester:")
#maPosition = initialise(3)
#affichePosition(maPosition)
#maPosition2 = joueCoup(maPosition,1) # SUD joue
#maPosition2 = joueCoup(maPosition2,1) # NORD joue
#maPosition2 = joueCoup(maPosition2,3) # SUD joue
#maPosition2 = joueCoup(maPosition2,3) # NORD joue
#maPosition2 = joueCoup(maPosition2,1) # SUD joue
#maPosition2 = joueCoup(maPosition2,1) # NORD joue
#affichePosition(maPosition2)
# ------------------------- FIN TEST exemple

# ------------------------- TEST coupJouable
#print(coupJouable(maPosition,1))
#print(coupJouable(maPosition2,1))
# ------------------------- FIN TEST coupJouable

# ------------------------- TEST coupAutorise
#affichePosition(coupAutorise(maPosition,1)) # coup autorisé
#print(coupAutorise(maPosition2,1)) # coup non autorisé car non jouable
#maPosition3 = dict()
#maPosition3['tablier'] = [2,5,4,6,2,6,2,1,1,1,1,1]
#maPosition3['taille'] = 6
#maPosition3['trait'] = 'SUD'
#maPosition3['graines'] = {'SUD':0, 'NORD':0}
#print(coupAutorise(maPosition3,6)) # coup non autorisé car position résultante illégale
# ------------------------- FIN TEST coupAutorise

# ------------------------- TEST positionTerminale
#maPosition4 = dict()
#maPosition4['tablier'] = [0,0,0,0,0,6,1,1,1,1,1,1]
#maPosition4['taille'] = 6
#maPosition4['trait'] = 'SUD'
#maPosition4['graines'] = {'SUD':0, 'NORD':0}
#affichePosition(maPosition4)
#print(positionTerminale(maPosition4))
# ------------------------- FIN TEST positionTerminale

# ------------------------- TEST moteurHumains
#moteurHumains()
# ------------------------- FIN TEST moteurHumains

# ------------------------- TEST choixAleatoire
#print(choixAleatoire(maPosition))
# ------------------------- FIN TEST choixAleatoire

# ------------------------- TEST moteurAleatoire
#moteurAleatoire('SUD')
# ------------------------- FIN TEST moteurAleatoire

# ------------------------- TEST evaluation
#print(evaluation(maPosition4))
#print(evaluation_v2(maPosition4))
# ------------------------- FIN TEST evaluation

# ------------------------- TEST moteurMinimax
#moteurMinimax('NORD',3)
# ------------------------- FIN TEST moteurMinimax

# ------------------------- TEST moteurAlphaBeta
#moteurAlphaBeta('NORD',3)
# ------------------------- FIN TEST moteurAlphaBeta

# ------------------------- TEST règle additionnelle
#maPosition5 = dict()
#maPosition5['tablier'] = [0,0,0,0,0,6,1,1,1,1,1,1]
#maPosition5['taille'] = 6
#maPosition5['trait'] = 'SUD'
#maPosition5['graines'] = {'SUD':0, 'NORD':0}
#affichePosition(maPosition5)
#print(coupAutorise(maPosition5,6)) # coup non autorisé car position résultante illégale selon les règles de base
#print(coupAutorise_v2(maPosition5,6)) # coup autorisé, on ne fait pas de prise qui affamerait l'ennemi
# ------------------------- FIN TEST règle additionnelle

# ------------------------- TEST moteurIA_versus_IA
#moteurIA_versus_IA('NORD')
# ------------------------- FIN TEST moteurIA_versus_IA