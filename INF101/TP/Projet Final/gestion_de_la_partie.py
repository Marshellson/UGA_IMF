import time
import distutils.core

import initialisation


def continuer():
    continuer_le_jeux = input("Est-ce que vous voulais continuer? y ou n")
    if continuer_le_jeux == "y":
        return True
    else:
        return False

    # if history["score"][""]


def tourJoueur(j, scores, pioche, score_croupier_premier_round):
    score = 0
    round = 0
    print(scores)
    liste_score = []
    for nom in scores:
        if nom == j:
            for nom_item, item in scores[nom].items():
                if nom_item == "score":
                    score = item
                if nom_item == "round":
                    round = item
        for nom_item, item in scores[nom].items():
            if nom_item == "score":
                liste_score.append(item)

    round += 1
    scores[j]["round"] = round
    print("--------------------")
    print("The %s round " % round)
    print("Name of the player: %s" % j)
    for i in range(len(liste_score)):
        if i == 0:
            print("There are %s players, they have %s " % (len(liste_score), liste_score[i]), end="")
        elif i == len(liste_score) - 1:
            print("%s points." % liste_score[i])
        else:
            print("%s " % liste_score[i], end="")
    print("Le croupier a %s." % score_croupier_premier_round)

    scores[j]["history"]["round %s" % round] = score
    if score == 21:
        print("You win the game!")
        scores[j]["success"] = True
        scores[j]["point"] += 1
        return
    print("You have %s scores now " % score)
    print(scores)
    if continuer():
        # if not scores[j]["out"] and not scores[j]["give_up"]

        liste_pioche = pioche
        liste_carte = initialisation.piocheCarte(liste_pioche, 1)
        for carte in liste_carte:
            print("You get %s" % carte)
            score += initialisation.valeurCarte(carte)
        print("score: %s" % score)
        scores[j]["score"] = score
        if score > 21:
            print("You lose the game!")
            scores[j]["out"] = True
            scores[j]["history"]["round %s" % (round + 1)] = score
        elif score == 21:
            print("You win the game!")
            scores[j]["success"] = True
            scores[j]["point"] += 1
            scores[j]["history"]["round %s" % (round + 1)] = score
    else:
        scores[j]["give_up"] = True
        print("You have given up")

    time.sleep(2)


def tourComplet(scores, pioche):
    score_sroupier_premier_round = croupier_prendre_carte(pioche, 1)
    while True:
        count_out = 0
        count_giveup = 0
        count_success = 0
        for nom in scores:
            if scores[nom]["out"]:
                count_out += 1
            elif scores[nom]["give_up"]:
                count_giveup += 1
            elif scores[nom]["success"]:
                count_success += 1

        if count_giveup == len(scores) - count_out - count_success:
            # cest a dire que tous les joueurs sont give up , va gagner les personnes qui gangent le plus score.
            score_croupier = score_sroupier_premier_round
            # TODO: Croupier condition
            # while True:
            #     score = croupier_prendre_carte(pioche, 1)
            #     print("Croupier a prendre %s" % score)
            #     score_croupier += score

            nom, score = initialisation.gagnant(scores, 18)
            for nom_gagner_plus_point in nom:
                for nom_dans_liste in scores:
                    if nom_dans_liste == nom_gagner_plus_point:
                        scores[nom_gagner_plus_point]["success"] = True
                        scores[nom_gagner_plus_point]["point"] += 1
                        print("You have success %s" % nom_gagner_plus_point)
            return
        elif count_out == len(scores):
            # Cest a dire que tous les personnes sont out
            return
        else:
            for nom in scores:
                if not scores[nom]["give_up"] and not scores[nom]["success"] and not scores[nom]["out"] and not \
                        scores[nom][
                            "draw"]:
                    tourJoueur(nom, scores, pioche, score_sroupier_premier_round)


def croupier_prendre_carte(pioche, nombre):
    liste_pioche = pioche
    liste_carte = initialisation.piocheCarte(liste_pioche, nombre)
    score = 0
    for carte in liste_carte:
        print("You get %s" % carte)
        score += initialisation.valeurCarte(carte)
    return score


def bot_decision(path, scores, nom):
    history = {}
    count = 0
    for line in open(path, "r"):
        line = line[:-1]  # delete \n
        # list_chaque_personne = f.split("\n")
        history[count] = {}
        item_list = line.split(",")
        history[count]["round"] = int(item_list[0])
        history[count]["score"] = {}
        for score in item_list[1:-3]:
            list_temp = score.split(":")
            history[count]["score"][list_temp[0]] = int(list_temp[1])
        history[count]["success"] = bool(distutils.util.strtobool(item_list[-3]))
        history[count]["out"] = bool(distutils.util.strtobool(item_list[-2]))
        history[count]["give_up"] = bool(distutils.util.strtobool(item_list[-1]))
        count += 1
    print(history)
    score = scores[nom]["score"]
    liste_chance = []
    success = 0
    defayant = 0
    for i in range(21 - score):

          # stocker les resultats ancient
        for items in history:

            if history[items]["out"]:  # le resultat il est out
                liste_temp_out = []
                for key, item in history[items]["score"].items():
                    liste_temp_out.append(item)

                for i in liste_temp_out:
                    if i == score and i < len(liste_temp_out) - 1:
                        score_suite = liste_temp_out[i + 1]
                        if score_suite > 21:
                            defayant += 2
                        else:
                            success += 1


            else:  # le resultat il nest pas out
                liste_temp_continue = []
                for key, item in history[items]["score"].items():
                    liste_temp_continue.append(item)
                for i in liste_temp_continue:
                    if i == score and i < len(liste_temp_continue) - 1:
                        score_suite = liste_temp_continue[i + 1]
                        if score_suite > 21:
                            defayant += 1
                        else:
                            success += 2

    print(success, defayant)

# def croupier_decision(scores, ):
