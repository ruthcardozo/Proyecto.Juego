import pygame
import random

NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (255,0,0)
VERDE = (0,255,0)
class Bloque(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("zombie.png")
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()

    def reset_pos(self):
         self.rect.y = random.randrange(-300, -20)
         self.rect.x = random.randrange(700-20)

    def update(self):
         self.rect.y += 1

         if self.rect.y > 410:
             self.reset_pos()
            
class Protagonista(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("soldado.png")
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()
            
        self.rect.x = 0
        self.rect.y = 0

        self.cambio_x =0
        self.cambio_y =0
            
    def cambio_velocidad(self,x,y):
        self.cambio_x += x
        self.cambio_y += y
    def update(self):
        self.rect.x += self.cambio_x
        if self.rect.x >=650 or self.rect.x <0:
            self.rect.x -= (x*-1)
        self.rect.y += self.cambio_y
        if self.rect.y >= 450 or self.rect.y < 0:
            self.rect.y -= (y*-1)

class Proyectil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4,10])
        self.image.fill(VERDE)

        self.rect = self.image.get_rect()
    def update(self):
        if self.rect.x >0:
            self.rect.x += 3
        else:
            self.rect.x -= 3


pygame.init()

largo= 700
ancho= 500

pantalla = pygame.display.set_mode([largo,ancho])
pygame.display.set_caption("ZombieLand")

imagen = pygame.image.load("bosque.jpg")
fondo = pygame.transform.scale(imagen,(700,500))
mira = pygame.image.load("mira.png")

bloque_lista = pygame.sprite.Group()

lista_todos_sprites = pygame.sprite.Group()

lista_proyectiles = pygame.sprite.Group()

for i in range(5):
       bloque = Bloque()
       bloque.rect.x = random.randrange(largo)
       bloque.rect.y = random.randrange(350)
       bloque_lista.add(bloque)
       lista_todos_sprites.add(bloque)

protagonista = Protagonista()
lista_todos_sprites.add(protagonista)

hecho = False

reloj = pygame.time.Clock()

fuente = pygame.font.Font(None, 36)

# http://freemusicarchive.org/music/Artofescapism/Modern_Experimental__Progressive_Electronic/Leaving_the_Dragons_Behind
pygame.mixer.music.load('Art_Of_Escapism_-_Leaving_the_Dragons_Behind.mp3')
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()

pygame.mouse.set_visible(0)

game_over = False

puntuacion = 0

nivel = 1

while not hecho:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho= True
        elif evento.type == pygame.constants.USEREVENT:
            # Este evento es disparado cuando la canción deja de reproducirse
            # Disponible en: 
            pygame.mixer.music.load('Left 4 Dead Soundtrack.mp3')
            pygame.mixer.music.play()
        elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    protagonista.cambio_velocidad(-3,0)
                elif evento.key == pygame.K_RIGHT:
                    protagonista.cambio_velocidad(3,0)
                elif evento.key == pygame.K_UP:
                    protagonista.cambio_velocidad(0,-3)
                elif evento.key == pygame.K_DOWN:
                    protagonista.cambio_velocidad(0,3)
        elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    protagonista.cambio_velocidad(0,0)
                elif evento.key == pygame.K_RIGHT:
                    protagonista.cambio_velocidad(0,0)
                elif evento.key == pygame.K_UP:
                    protagonista.cambio_velocidad(0,0)
                elif evento.key == pygame.K_DOWN:
                    protagonista.cambio_velocidad(0,0)
            
        elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Disparamos un proyectil si el usuario presiona el botón del ratón
            pygame.mixer.music.load('pistola1.mp3')
            pygame.mixer.music.play()
            proyectil = Proyectil()
                # Configuramos el proyectil de forma que esté donde el protagonista
            proyectil.rect.x = protagonista.rect.x
            proyectil.rect.y = protagonista.rect.y
                # Añadimos el proyectil a la lista
            lista_todos_sprites.add(proyectil)
            lista_proyectiles.add(proyectil)

    lista_todos_sprites.update()

    for proyectil in lista_proyectiles:
        lista_bloques_alcanzados = pygame.sprite.spritecollide(proyectil,bloque_lista,True)
        for bloque in lista_bloques_alcanzados:
            lista_proyectiles.remove(proyectil)
            lista_todos_sprites.remove(proyectil)
            puntuacion += 5
            bloque.reset_pos()
            if lista_bloques_alcanzados == 5:
                print("Ganaste")
                protagonista.cambio_velocidad(0,0)

    if len(bloque_lista) == 0:
            
        nivel += 1
        while nivel<=3:
            for i in range(nivel * 10):
                bloque = Bloque()
                
                bloque.rect.x = random.randrange(largo)
                bloque.rect.y = random.randrange(ancho)
                 
                # Añadimos el bloque a la lista de objetos.
                bloque_lista.add(bloque)
                lista_todos_sprites.add(bloque)
     
    pantalla.blit(fondo,(0,0))
    pos = pygame.mouse.get_pos()
    x= pos[0]
    y= pos[1]
        
    pantalla.blit(mira,(x,y))
        
    lista_todos_sprites.draw(pantalla)

    texto = fuente.render("Puntuación: " + str(puntuacion), True, BLANCO)
    pantalla.blit(texto, [10, 10])

    texto = fuente.render("Nivel: " + str(nivel), True, BLANCO)
    pantalla.blit(texto, [10, 40])
    """
        if 
            game_over = True
            fuente = pygame.font.SysFont("serif", 25)
            texto = fuente.render("Game Over, haz click para volver a jugar", True, BLANCO)
            centrar_x = (largo // 2) - (texto.get_width() // 2)
            centrar_y = (ancho // 2) - (texto.get_height() // 2)
            pantalla.blit(texto, [centrar_x, centrar_y])
    """
    pygame.display.flip()
    reloj.tick(20)

pygame.quit()
