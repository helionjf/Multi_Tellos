# -*-coding:utf-8 -*
import time
print("hello world : bonjour à la DP SFCE !")
question = input(">>>")
#print("Bonjour à toute la DP SFCE")
#n=0
while (question != "A+"):
    if (question == "Comment ca va ?"):
        print("Bien et toi ?")
    elif (question == "Qui est le plus intelligent ?"):
        print("Le public")    
    elif (question == "et moi ?"):
        print("Tu es mon maître un peu fourbe")      
    elif (question == "et Jacques ?"):
        print("Jacques a dit 'Tais toi et travaille, tu as une démonstration à faire et tu tournes autour du pot'")
    elif (question == "As tu quelques infos sur des personnes de la DP ?"):
        print("Oui Maître")      
    elif (question == "Mais encore ?"):
        print("Par exemple c'est François qui a la plus belle et Jean-Luc la plus vieille")
        time.sleep(3)
        print("Je parle des voitures bien sûr")
        time.sleep(2)
        print("Bon maintenant tu vas passer à la suite")
    else:
        print("Je ne comprends pas")    
    question = input(">>>")

