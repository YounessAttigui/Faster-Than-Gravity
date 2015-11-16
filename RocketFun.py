import pygame as pg
from pygame.locals import *
import random as rd
import time, sys
import math as m

pg.mixer.init()
pg.init()

#Fonction générant une surface de display. Les changement aporté à la fenetre (dim, nom, etc...) se font ici
def window():
    screen = pg.display.set_mode((750,600),HWSURFACE|DOUBLEBUF|RESIZABLE)
    pg.display.set_caption("Faster Than Gravity")
    pg.display.set_icon(pg.image.load("rocket_ship.png"))
    return screen

#Permet d'ouvrir une image et de l'enregister en tampon sous la forme d'une image (carte de pixels)
def imageLoader(fichier):
    image = pg.image.load(fichier)
    return(image)

#J'avais juste la flemme de tapper la vraie ligne à chaque fois: change les variables des objets rectangles (x et y)
def setRectCoordinates(rect,x,y):
    rect.x= x
    rect.y= y
    return(rect)

#Tous les préparatif de mix seront fait ici (playlist etc...)
def davidGetta():
    return(pg.mixer.Sound("RocketFun.ogg"))

def calculDesVitesses(vFusee,playerRect,bodies,dT=0.1):
    r,k,bodiesRect=[],[],[]
    for i in range(len(bodies)):
        bodiesRect.append(bodies[i].rect)
        k.append(bodies[i].GM)
    for i in range(len(bodiesRect)):
        r.append((m.sqrt(((bodiesRect[i].centerx-playerRect.centerx)**2)+((bodiesRect[i].centery-playerRect.centery)**2))))
    Fx,Fy=0,0
    for i in range(len(k)):
        Fxint=k[i]*(1/(r[i]**3))*(abs(bodiesRect[i].centery-playerRect.centery))
        if bodiesRect[i].centerx>playerRect.centerx: Fx+=Fxint
        else: Fx-=Fxint
        Fyint=k[i]*(1/(r[i]**3))*(abs(bodiesRect[i].centerx-playerRect.centerx))
        if abs(bodiesRect[i].centery)>playerRect.centery: Fy-=Fyint
        else: Fy+=Fyint
    vFusee=[vFusee[0]+(Fx*dT),vFusee[1]+(Fy*dT)]
    print (vFusee)
    return(vFusee)

def textureToMass(texture):
    mass=1.9*(10**17)
    return(mass)

def randomSpawner(bodies):
    n=rd.randrange(0,5,1)
    if n==0: s=sBody("blackhole.png")
    if n==1: s=sBody("Earth.png")
    if n==2: s=sBody("Aldebaran.png")
    if n==3: s=sBody("ringworld.png")
    if n==4: s=sBody("sun.png")
    for i in range(len(bodies)):
        if s.rect.colliderect(bodies[i].rect):
            s=randomSpawner(bodies)
    return s

def pause(music,screen):
    music.set_volume(0.1)
    pauseScreen=affichage(325,300,35)
    pauseScreen.render("PAUSE")
    screen.blit(pauseScreen.texte, pauseScreen.rect)
    pg.display.flip()
    while 1:
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    return True
            if event.type == pg.QUIT:
                pg.display.quit()
                music.stop()

def control(keyPressed,rocket):
    hypot= m.sqrt((rocket.speed[0]**2)+(rocket.speed[1]**2))
    sgx,sgy,norme=1,1,0
    if rocket.speed[0] * (-1) >=0: sgx=(-1)
    if rocket.speed[1] * (-1) >=0: sgy=(-1)
    if keyPressed[pg.K_UP]:
        norme=0.5
    if keyPressed[pg.K_DOWN]:
        norme=-0.5
    rocket.speed[0]+= sgx*(norme*(abs(rocket.speed[0])/hypot))
    rocket.speed[1]+= sgy*(norme*(abs(rocket.speed[1])/hypot))

def afficheVect(fusee,dt):
    startpos=(fusee.rect.centerx,fusee.rect.top)
    endpos=[startpos[0]+(fusee.speed[0])*(20),startpos[1]+(fusee.speed[1])*(-20)]
    return [startpos,endpos]

def testForDeath(bodies,superNovaPos,playerRect):
    for i in bodies:
        ray = m.sqrt(((i.rect.centerx-playerRect.centerx)**2)+((i.rect.centery-playerRect.centery)**2))
        if ray<= i.ray: return True
    if superNovaPos+50<= playerRect.centery: return True
    return False

def textureToRay(texture):
    if texture == "sun.png": return 30#60
    if texture == "blackhole.png": return 28#56
    if texture == "Earth.png": return 35#69
    if texture == "ringworld.png": return 28#55
    if texture == "Aldebaran.png": return 38#76
    return 1
        
class sBody(object):
    def __init__(self,texture):
        self.text= imageLoader(texture)
        self.rect= self.text.get_rect()
        self.rect = setRectCoordinates(self.rect,rd.randrange(0,650,1),rd.randrange(-500,-200,1))
        self.GM = 6.67*(10**(-11))*textureToMass(texture)
        self.ray = textureToRay(texture)
    def move(self,v):
        self.rect = self.rect.move(0,v)
    def setCoord(self,x,y):
        self.rect.centerx = x
        self.rect.centery = y

class rocket(object):
    def __init__(self):
        self.text= imageLoader("rocket_ship.png")
        self.rect= self.text.get_rect()
        self.rect = setRectCoordinates(self.rect,350,400)
        self.speed = [0,1]

    def selfControl(self):
        if self.speed[1] > 5: self.speed[1] = 5
        if self.speed[1] < 0: self.speed[1] = 0
        if self.speed[0] > 4: self.speed[0] = 4
        if self.speed[0] < -4: self.speed[0] = -4

    def move(self):
        self.rect=self.rect.move(self.speed[0],0)
        if self.rect.left < 1: self.rect.right = 749
        if self.rect.right > 749: self.rect.left = 1
        #c'est moins cohérent mais c'est plus jouable

class affichage(object):
    def __init__(self,bottom,right,size=20):
        self.__font= pg.font.Font(pg.font.get_default_font(),size)
        self.color=(255,255,255)
        self.texte= self.__font.render("",0,self.color)
        self.rect=self.texte.get_rect()
        self.rect.bottom,self.rect.right=bottom,right
        
    def render(self,texte):
        self.texte=self.__font.render(texte,0,self.color)

    def coord(self,bottom,right):
        self.rect.bottom,self.rect.right=bottom,right

#Cette fonction gère l'affichage. Mais apparement, ce sera la boucle principale.
def display():
    music=davidGetta()
    screen = window()
    warning = imageLoader("warning.png")
    background = imageLoader("Space.jpg")
    supernova=sBody("supernova.png")
    score = affichage(25,600)
    speed = affichage(600,0)
    distance = affichage(600,600)
    backG = background.get_rect()
    backG2 = background.get_rect()
    warningRect = warning.get_rect()
    music.play(-1)
    music.set_volume(0.6)
    isMusicOn = True
    #Toutes les lignes ci-dessus sont des préparatifs. Je stock toutes les images et la musique dont j'ai besoins par la suite.
    while 1:
        supernova.setCoord(375,1200)
        player = rocket()
        bodies=[]
        for i in range(0,4):
            bodies.append(randomSpawner(bodies))
        backG.bottom,backG2.bottom = 600,-424
        scoreCount=0
        vScroling=1
        move_ticker =0
        vSupernova=-1
        gameOver=False
        while gameOver==False:
            t0=time.clock()
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        pause(music,screen)
                        music.set_volume(0.6)
                if event.type == pg.QUIT:
                    pg.display.quit()
                    music.stop()
            key = pg.key.get_pressed() #Je cheque juste les entrée utilisateur ici
            if backG.top==600: backG.bottom = -424
            if backG2.top==600: backG2.bottom = -424
            #les deux if au dessus permentent juste d'utiliser la seamless
            #Controles.... plus tard je renverais juste une valeur à la fonction de calcul des coordonées de la fusée
            if move_ticker == 0:
                control(key,player)
                move_ticker=5
            player.speed = calculDesVitesses(player.speed,player.rect,bodies,time.clock()-t0)
            player.selfControl()
            player.move()
            coordVect=afficheVect(player,time.clock()-t0)
            backG,backG2 = backG.move(0,vScroling),backG2.move(0,vScroling)
            for i in range(len(bodies)):
                bodies[i].move(2)
                if bodies[i].rect.top > 800:
                     bodies[i]=randomSpawner(bodies)
                     scoreCount+=1
            supernova.move(vSupernova+int(player.speed[1])-int(scoreCount/20))
            playerSupernovaDistance=supernova.rect.top-player.rect.bottom
            gameOver = testForDeath(bodies,supernova.rect.top,player.rect)
            distance.render("Distance: "+str(int(playerSupernovaDistance)))
            score.render("Score: "+str(int(scoreCount)))
            speed.render("Speed : "+str(int((player.speed[1]*100))))
            #Les blit me permetent de copier les cartes de pixel sur les rectangles que j'ai deplacé
            screen.blit(background, backG)
            screen.blit(background, backG2)
            screen.blit(player.text, player.rect)
            for i in range(len(bodies)):
                screen.blit(bodies[i].text,bodies[i].rect)
            screen.blit(supernova.text,supernova.rect)
            screen.blit(score.texte, score.rect)
            screen.blit(speed.texte, speed.rect)
            screen.blit(distance.texte, distance.rect)
            pg.draw.aaline(screen,(16,200,246),coordVect[0],coordVect[1])
            if playerSupernovaDistance < 200:
                distance.color=(255,0,0)
                screen.blit(warning, warningRect)
            else:
                distance.color=(255,255,255)
            #Les changements effectués en mémoire tampon sont apliqués à la fenêtre        
            pg.display.flip()
            if move_ticker > 0: move_ticker -= 1
        #Le gameover apparait ici :)

display()

