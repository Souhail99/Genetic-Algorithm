# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 22:39:33 2021

@author: Souha
"""
import time
import random
import numpy as np
from math import *
import csv
import pandas as pd
from itertools import permutations
import matplotlib.pyplot as plt




def LireCSV():
    df=pd.read_csv("D:/ESILV/temperature_sample.csv",sep=';')
    return df

class Individu:
    def __init__(self, a=None, b=None, c=None):
        if(a==None or b == None or c== None ):
             h=list(np.random.standard_normal(1))
             self.a=h[0]
             while abs(self.a)>1:
                 h=list(np.random.standard_normal(1))
                 self.a=h[0]
             self.a=abs(self.a)
             self.b=random.randint(1,20)
             self.c=random.randint(1,20)
        else :
            self.a=a
            self.b=b
            self.c=c
    def __str__(self):
        return str(f"La valeur de a est :{self.a}, la valeur de b est :{self.b}, et la valeur de c est :{self.c}")
   
    def Fitness(self):
        ecart=0
        sommetheorique=0
        df=LireCSV()
        for i in range(len(df["#i"])):
            sommetheorique=0
            for x in range(self.c+1):
                sommetheorique = sommetheorique + (self.a**x)*(cos((self.b**x)*pi*df["#i"][i]))
            ecart+=abs(sommetheorique-df["t"][i])
        return ecart/len(df["t"])
    
def Fitness(self):
        ecart=0
        sommetheorique=0
        df=LireCSV()
        for i in range(len(df["#i"])):
            sommetheorique=0
            for x in range(self.c+1):
                sommetheorique = sommetheorique + (self.a**x)*(cos((self.b**x)*pi*df["#i"][i]))
            ecart+=abs(sommetheorique-df["t"][i])
        return ecart/len(df["t"])
def Population(nombre):
     return [Individu() for i in range(nombre)]

def Fitness2(a,b,c):
     sommetheorique=0  
     for x in range(c+1):
          sommetheorique = sommetheorique + (a**x)*(cos((b**x)*pi*0.27))
     return sommetheorique
 
    
def Selection(population):
    
    selection=[]
    for i in range(20):
        selection.append(population[i])
    i=len(population)-10
    while i<len(population):
        selection.append(population[i])
        i+=1
    return selection

def Croisement(individu1, individu2):
    c1=[]
    c2=[]
    value=random.randint(0,2)
    if(value==0):
        c1.append(individu1.a)
        c1.append(individu1.b)
        c1.append(individu2.c)
    if(value==1):
        c1.append(individu1.a)
        c1.append(individu2.b)
        c1.append(individu2.c)   
    if(value==2):
        c1.append(individu2.a)
        c1.append(individu2.b)
        c1.append(individu1.c)
    croisement1=Individu(c1[0],c1[1],c1[2])
    value=random.randint(0,2)
    if(value==0):
        c2.append(individu1.a)
        c2.append(individu1.b)
        c2.append(individu2.c)
    if(value==1):
        c2.append(individu1.a)
        c2.append(individu2.b)
        c2.append(individu2.c)   
    if(value==2):
        c2.append(individu2.a)
        c2.append(individu2.b)
        c2.append(individu1.c)
    croisement2=Individu(c2[0],c2[1],c2[2])
    return [croisement1,croisement2]

def Mutation(individu):
    ind = Individu(individu.a,individu.b,individu.c)
    value=random.randint(0,2)
    if(value==0):
        ind.a = np.random.standard_normal(1)
    if(value==1):
        ind.b =random.randint(1,20)  
    if(value==2):
        ind.c =random.randint(1,20)  
    return ind

def Evaluation(population):
    population.sort(key=lambda x: x.Fitness())
    return population

def Algo(temps):
    if(temps==None):
      temps=20
    debut = time.time()
    iteration=0
    taillepopulation=500
    population=Population(taillepopulation)
    a=time.time()
    while time.time() - a < temps:
        iteration+=1
        population=Evaluation(population)
        print(population[0])
        newpopulation=Selection(population)
        for i in range(0,len(newpopulation)-1,2):
            newpopulation.extend(Croisement(newpopulation[i],newpopulation[i+1]))
        for i in range(0,random.randint(1,len(newpopulation))):
            newpopulation.append(Mutation(newpopulation[i]))
        population+=newpopulation+Population(26)  
    print("\n")
    print("Meilleur Fonction fitness :",population[0].Fitness(), "(qui correspond à la valeur moyenne de l'écart entre les valeurs réelles et les valeurs du meilleur triplet (a, b et c))","trouvée durant le laps de temps suivant :",temps,"secondes.")
    print("Avec une population de :",taillepopulation,"individus (triplets).")
    print("Il y'a eu :",iteration,"d'itérations pour aboutir à ce résultat.")
    print("Le meilleur triplet abc est :",round(population[0].a,2),",",population[0].b,"et",population[0].c,".")
    GraphiqueComparaison(population[0])
    fin = time.time()
    print("Temps :",fin-debut,"secondes entre l'ouverture de la fonction et la fin.")

def GraphiqueComparaison(individu):  
    sommetheorique=0
    ensembledesvaleurstheoriques=[]
    df=LireCSV()
    for i in range(len(df["#i"])):
        for x in range(individu.c):
            sommetheorique = sommetheorique + (individu.a**x)*(cos((individu.b**x)*pi*df["#i"][i]))
        ensembledesvaleurstheoriques.append(sommetheorique)
    X=list(df["#i"])
    X.sort()
    Y=list(df["t"])
    Y.sort()
    plt.title("Graphique de comparaison entre les valeurs réelles et trouvées")
    plt.plot(X,Y)
    plt.plot(X,ensembledesvaleurstheoriques)
    plt.xlabel('x')
    plt.ylabel('Température(x)') 
    plt.show()