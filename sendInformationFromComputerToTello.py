# -*- coding: utf-8 -*-
# Auteur : Jean-Christophe HENRY 
# Mail   : jeanchristophe.henry@orange.com 
# Service: DTSI/DSI CCMD
# Script permettant d'intéragir directement avec les drones
# Pour ajouter des actions il faut aller dans la méthode
# if __name__ == '__main__':
# Puis ajouter une nouvelle ligne thread

# Import the built-in socket and time modules
import time
from threading import Thread, Event

# Import des actions envoyé au socket du drone
import actionToTello

# Event object used to send signals from one thread to another

stop_event = Event()

 ##########################################################################
 # On utilise la fonction do_actions et on éxécute le programme dans main #
 # Si on veut ajouter une action alors il faudra créer un autre thread    #
 ##########################################################################
if __name__ == '__main__':
    print("")
    print("______________________________________________________")
    print("")
    print("Debut du programme")
    print("______________________________________________________")
    print("")

    # l'action command permet d'exécuter une commande sur le drone
    Thread(target=actionToTello.do_actions("command", 3, stop_event))

    for i in range(2):
        # Je demande le niveau de batterie du drone
        Thread(target=actionToTello.do_actions("battery?", 3, stop_event))

    # Nous envoyons un signal indiquant que l'autre thread doit s'arrêter.
    stop_event.set()

    print("")
    print("______________________________________________________")
    print("")
    print("Fin du programme")
    print("______________________________________________________")
    print("")
