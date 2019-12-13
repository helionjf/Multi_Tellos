# Multi_Tellos
Codes pour faire fonctionner un essaim de tellos
dernière mise à jour le 04/12/2019 :
<B>Send-information-with-socket.py</B>
Code éloboré par jeanchristophe.henry@orange.com
Code qui permet une meilleure visibilité des interactions entre le drone et le PC.

Ajout d'une commande "flip" pour plus de démonstration.

Et pour passer le drone en mode station au lieu de son mode par défaut en accès point : <B>SetStationMode.py</B>
Qui rend obsolete "formation_setup.py"

Pour le faire revenir en mode accès point lorsqu'il est actif en mode station, appuyer plus de 5 secondes sur le bouton [Marche/Arrêt] : cela réinitialise le drone.

Schéma des liaisons entre PC et drone en mode par défaut (accès point) :
[TELLO1] ---wifi---[PC]
Connecter le PC au wifi TELLO1, puis lancer les commandes avec le programme <B>Send-information-with-socket.py</B>
Chaque drone sera relié successivement à un PC ou bien il faut 1 PC par drone.

Schéma des liaisons entre PC et drone en mode station :
<br>
                    _______<br>
[TELLO1] ---wifi---/       \<br>
[TELLO2] ---wifi---|       |<br>
[TELLO3] ---wifi---[ROUTEUR] --- [PC]<br>
[TELLO4] ---wifi---|       |<br>
[TELLO5] ---wifi---\_______/<br>


Chaque drone doit être positionné en mode station en le connectant au PC et en lancant le script SetStationMode.py.
Puis le PC doit se connecter au routeur et lancer le script <B> multi_tello_test.py coderoom2.txt</B> où coderoom2.txt regroupe les commandes qui seront diffusées vers les drones connectés et identifiés.""A compléter par rapport à une version compatible py 3.8"".

Note :
Expérience de relier 5 PC à 5 drones via le routeur :
                    _______
[TELLO1] ---wifi---/       \ --- [PC]
[TELLO2] ---wifi---|       | --- [PC]
[TELLO3] ---wifi---[ROUTEUR] --- [PC]
[TELLO4] ---wifi---|       | --- [PC]
[TELLO5] ---wifi---\_______/ --- [PC]

Cela ne semble pas fonctionner terriblement si l'organisation n'est pas stricte (un PC peut contrôler un drone qui ne lui est pas attribué. (A vérifier)

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

