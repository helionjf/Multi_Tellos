# -*- coding: utf-8 -*-
# Auteur : Jean-Christophe HENRY 
# Mail   : jeanchristophe.henry@orange.com 
# Service: DTSI/DSI CCMD
# Script permettant d'intéragir directement avec les drones
# Pour ajouter des actions il faut aller dans la méthode
# if __name__ == '__main__':
# Puis ajouter une nouvelle ligne thread
import time
import socket
from threading import Event
 
#################################################################
#                   CONFIGURATION DU SOCKET                     #
#################################################################
# IP and port of Tello
telloAdress = ('192.168.10.1', 8889)

# Ajout du socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# On bind sur quel port on veut faire nos échanges
sock.bind(('', 9000))
# On ajoute un time out de 8 secondes
sock.settimeout(7)

#################################################################
#                   FONCTION POUR LES ACTIONS                   #
#################################################################
# Function to send messages to Tello
def send(message, sleep = 0):
  try:
    sock.sendto(message.encode(), telloAdress)
    print("Message envoyé: " + message)
  except Exception as e:
    print("Erreur d envoi: " + str(e))

    # Delay for a user-defined period of time
  time.sleep(sleep)

# Function that listens for messages from Tello and prints them to the screen
def receive():
  try:
    response, ip_address = sock.recvfrom(128)
    print("Message reçu : " + response.decode(encoding='utf-8') + " from Tello with IP: " + str(ip_address))
  except Exception as e:
    print("Erreur de reception: " + str(e))


# do_actions permet d'automatiser les actions pour le drone
def do_actions(action, sleep, stop_event):
    print("")
    print("---")
    send(action, sleep)

    # Receive response from Tello
    receive()
    print("---")
    print("")

    # Ici, nous vérifions si l'autre thread a envoyé un signal pour arrêter l'exécution.
    if stop_event.is_set():
        sock.close()
        print("")
        print("Le socket est fermé")
        print("")
 
