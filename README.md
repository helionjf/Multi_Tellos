# Multi_Tellos
Codes pour faire fonctionner un essaim de tellos
dernière mise à jour le 04/12/2019 :
<B>Send-information-with-socket.py</B>
Code éloboré par jeanchristophe.henry@orange.com
Code qui permet une meilleure visibilité des interactions entre le drone et le PC.
Ajout d'une commande "flip" pour plus de démonstration.

Et pour passer le drone en mode station au lieu de son mode par défaut en accès point : <B>SetStationMode.py</B>

Pour le faire revenir en mode accès point lorsqu'il est actif en mode station, appuyer plus de 5 secondes sur le bouton [Marche/Arrêt] : cela réinitialise le drone.





Code de référence en py27 :
https://github.com/TelloSDK/Multi-Tello-Formation


Cela fonctionne aussi avec un tello donc on peut en faire fonctionner avec plusieurs PC sachant que chaque PC pointe vers un tello particulier à l'aide de son ident.
exemple de tableau des idents :

N°	IDENT	SN
1	D3FCE4	0TQDFCHEDB3F86
2	DC5CE0	0TQDG2KEDB4FH3
3	DC5CF3	0TQDG2KEDB04T1
4	D3F926	0TQDFCHEDBY3H0
5	DC5F6C	0TQDG2KEDBWK3X
6	DC5F05	0TQDG2KEDBPE19


Configuration :
c:\python27 installé
Dans ce répertoire on installe le code nécessaire :
Il faut au minimum :
formation_setup.py dans lequel on spécifie le code et le passwd du point d'accès et qui permet au tello sur lequel on se connecte de rebooter et de se connecter en tant que station sur le point d'accès wifi.
Puis stats.py et tello_manager.py et enfin multi_tello_test.py qui est le programme à lancer avec un fichier de commande txt :
exemple coderoom2.txt


Après on se réfère au manuel du tello pour les autres commandes : https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf

Le site de Ryze :
https://www.ryzerobotics.com/fr/tello-edu

Les docs sur Tello Edu :
https://www.ryzerobotics.com/fr/tello-edu/downloads



On peut enfin regrouper les commandes dans un même fichier pour faire voler tous les tellos en même temps à partir d'un seul PC.

