# Multi_Tellos
Codes pour faire fonctionner un essaim de tellos

Code de référence en py27 :
https://github.com/TelloSDK/Multi-Tello-Formation


Cela fonctionne aussi avec un tello donc on peut en faire fonctionner avec plusieurs PC sachant que chaque PC pointe vers un tello particulier à l'aide de son ident.
Tableau des idents :

Configuration :
c:\python27 installé
Dans ce répertoire on installe le code nécessaire :
Il faut au minimum :
formation_setup.py dans lequel on spécifie le code et le passwd du point d'accès et qui permet au tello sur lequel on se connecte de rebooter et de se connecter en tant que station sur le point d'accès wifi.
Puis stats.py et tello_manager.py et enfin multi_tello_test.py qui est le programme à lancer avec un fichier de commande txt :
exemple coderoom2.txt


Après on se réfère au manuel du tello pour les autres commandes.

On peut enfin regrouper les commandes dans un même fichier pour faire voler tous les tellos en même temps à partir d'un seul PC.

