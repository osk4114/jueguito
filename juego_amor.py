import pygame
import random
import sys
import math
import asyncio

try:
    import platform
    MOBILE = platform.system() == "Emscripten"
except:
    MOBILE = False

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
ANCHO = 800
ALTO = 500
SUELO_Y = 380
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Jueguito ❤️")
RELOJ = pygame.time.Clock()
FPS = 60

# COLORES
ROSA_CLARO = (255, 228, 235)
ROSA_MEDIO = (255, 182, 203)
ROSA_OSCURO = (255, 105, 180)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (220, 20, 60)
DORADO = (255, 215, 0)
NARANJA_GATO = (255, 165, 80)
NARANJA_OSCURO = (220, 140, 60)
VERDE_OSCURO = (34, 120, 34)
VERDE_CLARO = (80, 180, 80)
CIELO_ARRIBA = (255, 200, 220)
CIELO_ABAJO = (255, 235, 240)
TIERRA = (200, 160, 130)
TIERRA_OSCURA = (170, 130, 100)

# --- UTILIDADES ---
def lerp_color(c1, c2, t):
    """Interpola entre dos colores"""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def dibujar_cielo_gradiente():
    """Dibuja un cielo con degradado vertical"""
    for y in range(SUELO_Y):
        t = y / SUELO_Y
        color = lerp_color(CIELO_ARRIBA, CIELO_ABAJO, t)
        pygame.draw.line(PANTALLA, color, (0, y), (ANCHO, y))

def dibujar_suelo(offset=0):
    """Dibuja suelo con pasto animado"""
    # Tierra
    pygame.draw.rect(PANTALLA, TIERRA, (0, SUELO_Y, ANCHO, ALTO - SUELO_Y))
    pygame.draw.rect(PANTALLA, TIERRA_OSCURA, (0, SUELO_Y + 15, ANCHO, ALTO - SUELO_Y - 15))
    # Línea de pasto
    for x in range(-20 + (int(offset) % 20), ANCHO + 20, 12):
        h = 6 + math.sin(x * 0.3 + offset * 0.05) * 3
        pygame.draw.line(PANTALLA, VERDE_CLARO, (x, SUELO_Y), (x - 3, SUELO_Y - h), 2)
        pygame.draw.line(PANTALLA, VERDE_OSCURO, (x + 5, SUELO_Y), (x + 2, SUELO_Y - h + 1), 2)

# --- CLASES DECORATIVAS ---
class Nube:
    def __init__(self, x=None):
        self.x = x if x else random.randint(0, ANCHO)
        self.y = random.randint(20, 150)
        self.velocidad = random.uniform(0.3, 0.8)
        self.escala = random.uniform(0.7, 1.3)
        self.alpha = random.randint(120, 200)

    def update(self):
        self.x -= self.velocidad
        if self.x < -100:
            self.x = ANCHO + random.randint(50, 200)
            self.y = random.randint(20, 150)

    def draw(self):
        s = self.escala
        surf = pygame.Surface((int(90 * s), int(40 * s)), pygame.SRCALPHA)
        color = (255, 255, 255, self.alpha)
        pygame.draw.ellipse(surf, color, (0, int(10*s), int(60*s), int(30*s)))
        pygame.draw.ellipse(surf, color, (int(20*s), 0, int(50*s), int(35*s)))
        pygame.draw.ellipse(surf, color, (int(35*s), int(8*s), int(55*s), int(30*s)))
        PANTALLA.blit(surf, (self.x, self.y))

class CorazonFlotante:
    """Corazones decorativos flotando en el fondo"""
    def __init__(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(50, SUELO_Y - 50)
        self.vy = random.uniform(-0.5, -0.2)
        self.vx = random.uniform(-0.3, 0.3)
        self.size = random.randint(6, 12)
        self.alpha = random.randint(40, 100)
        self.vida = random.randint(200, 400)
        self.fase = random.uniform(0, math.pi * 2)

    def update(self):
        self.fase += 0.03
        self.x += self.vx + math.sin(self.fase) * 0.3
        self.y += self.vy
        self.vida -= 1
        if self.vida < 60:
            self.alpha = max(0, self.alpha - 2)

    def draw(self):
        if self.alpha <= 0:
            return
        s = self.size
        surf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
        color = (255, 100, 130, self.alpha)
        pygame.draw.circle(surf, color, (s // 2, s // 2), s // 2)
        pygame.draw.circle(surf, color, (s + s // 2, s // 2), s // 2)
        pygame.draw.polygon(surf, color, [(0, s // 2 + 2), (s * 2, s // 2 + 2), (s, s * 2)])
        PANTALLA.blit(surf, (self.x, self.y))

class Estrella:
    """Estrellitas brillantes decorativas"""
    def __init__(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(10, SUELO_Y - 30)
        self.fase = random.uniform(0, math.pi * 2)
        self.velocidad = random.uniform(0.05, 0.12)
        self.size = random.randint(2, 4)

    def update(self):
        self.fase += self.velocidad

    def draw(self):
        alpha = int(128 + 127 * math.sin(self.fase))
        brillo = max(0, min(255, alpha))
        color = (255, 255, 200, brillo)
        surf = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        cx, cy = self.size * 2, self.size * 2
        # Cruz brillante
        pygame.draw.line(surf, color, (cx - self.size, cy), (cx + self.size, cy), 1)
        pygame.draw.line(surf, color, (cx, cy - self.size), (cx, cy + self.size), 1)
        # Centro
        pygame.draw.circle(surf, (255, 255, 230, brillo), (cx, cy), max(1, self.size // 2))
        PANTALLA.blit(surf, (self.x - self.size * 2, self.y - self.size * 2))

# --- GENERADOR DE GRAFICOS (PIXEL ART MEJORADO) ---
def crear_gatito(frame=0, agachado=False):
    """Crea sprite del cerdito-girasol con animación"""
    # Colores del personaje
    AMARILLO_PETALO = (255, 200, 50)
    AMARILLO_OSCURO = (230, 175, 30)
    CREMA = (255, 240, 235)
    CREMA_SOMBRA = (245, 225, 218)
    ROSA_NARIZ = (255, 180, 190)
    ROSA_MEJILLA = (255, 170, 180)
    ROSA_OREJA = (255, 190, 200)
    ROSA_PATA = (255, 195, 200)

    if agachado:
        w, h = 52, 32
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        cx, cy = 26, 18

        # Cuerpo acostado (elipse horizontal)
        pygame.draw.ellipse(surf, CREMA, (2, 10, 48, 22))
        pygame.draw.ellipse(surf, CREMA_SOMBRA, (4, 14, 44, 16))

        # Pétalos de girasol alrededor (más pequeños, achatados)
        num_petalos = 10
        for i in range(num_petalos):
            ang = (2 * math.pi / num_petalos) * i + math.sin(frame * 0.1) * 0.05
            px = cx + math.cos(ang) * 14
            py = cy - 2 + math.sin(ang) * 9
            pygame.draw.ellipse(surf, AMARILLO_PETALO,
                                (int(px) - 5, int(py) - 3, 10, 7))

        # Cara (círculo achatado)
        pygame.draw.ellipse(surf, CREMA, (10, 4, 32, 24))

        # Ojos cerrados (arcos felices)
        pygame.draw.arc(surf, NEGRO, (17, 11, 6, 5), 0.2, math.pi - 0.2, 2)
        pygame.draw.arc(surf, NEGRO, (29, 11, 6, 5), 0.2, math.pi - 0.2, 2)

        # Hocico
        pygame.draw.ellipse(surf, ROSA_NARIZ, (22, 15, 8, 6))
        pygame.draw.circle(surf, (255, 140, 155), (24, 18), 1)
        pygame.draw.circle(surf, (255, 140, 155), (28, 18), 1)

        # Patitas rosadas asomando
        pygame.draw.ellipse(surf, ROSA_PATA, (6, 24, 8, 6))
        pygame.draw.ellipse(surf, ROSA_PATA, (38, 24, 8, 6))

    else:
        w, h = 48, 52
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        cx, cy = 24, 20

        # --- PÉTALOS DE GIRASOL (alrededor de la cabeza) ---
        num_petalos = 12
        for i in range(num_petalos):
            ang = (2 * math.pi / num_petalos) * i + math.sin(frame * 0.08) * 0.06
            px = cx + math.cos(ang) * 16
            py = cy + math.sin(ang) * 16
            # Pétalos ovalados apuntando hacia afuera
            petalo_surf = pygame.Surface((14, 9), pygame.SRCALPHA)
            pygame.draw.ellipse(petalo_surf, AMARILLO_PETALO, (0, 0, 14, 9))
            pygame.draw.ellipse(petalo_surf, AMARILLO_OSCURO, (1, 1, 12, 7), 1)
            rotado = pygame.transform.rotate(petalo_surf, -math.degrees(ang))
            rect = rotado.get_rect(center=(int(px), int(py)))
            surf.blit(rotado, rect)

        # --- CARA (círculo blanco/crema grande) ---
        pygame.draw.circle(surf, CREMA, (cx, cy), 14)
        pygame.draw.circle(surf, CREMA_SOMBRA, (cx, cy), 14, 1)

        # --- OJOS (arcos cerrados, sonrientes) ---
        parpadeo_abierto = (frame % 150) > 5 and (frame % 150) < 10
        if parpadeo_abierto:
            # Ojos abiertos brevemente (parpadeo inverso)
            pygame.draw.circle(surf, NEGRO, (18, 17), 2)
            pygame.draw.circle(surf, NEGRO, (30, 17), 2)
            pygame.draw.circle(surf, BLANCO, (19, 16), 1)
            pygame.draw.circle(surf, BLANCO, (31, 16), 1)
        else:
            # Ojos cerrados felices (como el peluche)
            pygame.draw.arc(surf, NEGRO, (14, 14, 8, 7), 0.3, math.pi - 0.3, 2)
            pygame.draw.arc(surf, NEGRO, (26, 14, 8, 7), 0.3, math.pi - 0.3, 2)

        # --- MEJILLAS SONROJADAS ---
        mejilla_surf = pygame.Surface((8, 5), pygame.SRCALPHA)
        pygame.draw.ellipse(mejilla_surf, (*ROSA_MEJILLA, 100), (0, 0, 8, 5))
        surf.blit(mejilla_surf, (10, 20))
        surf.blit(mejilla_surf, (30, 20))

        # --- HOCICO (nariz de cerdito) ---
        pygame.draw.ellipse(surf, ROSA_NARIZ, (19, 21, 10, 7))
        # Fosas nasales
        pygame.draw.circle(surf, (255, 130, 150), (22, 24), 1)
        pygame.draw.circle(surf, (255, 130, 150), (26, 24), 1)

        # --- BOCA (sonrisa sutil debajo del hocico) ---
        pygame.draw.arc(surf, (200, 130, 140), (20, 26, 8, 4), math.pi + 0.3, 2 * math.pi - 0.3, 1)

        # --- OREJAS (pequeñas, rosadas, asomando arriba) ---
        pygame.draw.ellipse(surf, ROSA_OREJA, (8, 3, 7, 6))
        pygame.draw.ellipse(surf, ROSA_OREJA, (33, 3, 7, 6))

        # --- CUERPO ---
        pygame.draw.ellipse(surf, CREMA, (10, 32, 28, 18))
        pygame.draw.ellipse(surf, CREMA_SOMBRA, (12, 34, 24, 14))

        # --- PATITAS animadas ---
        desplazamiento = math.sin(frame * 0.4) * 2
        # Patas delanteras
        pygame.draw.ellipse(surf, ROSA_PATA,
                            (10, 42 + int(desplazamiento), 8, 7))
        pygame.draw.ellipse(surf, ROSA_PATA,
                            (30, 42 - int(desplazamiento), 8, 7))

        # --- COLITA (pequeño rizo atrás) ---
        cola_y = 38 + math.sin(frame * 0.2) * 2
        pygame.draw.arc(surf, ROSA_PATA,
                        (36, int(cola_y), 10, 8), -0.5, math.pi, 2)

    return surf

def crear_obstaculo_tipo(tipo):
    """Crea diferentes tipos de obstáculos"""
    if tipo == 0:
        # Cactus mejorado
        surf = pygame.Surface((30, 55), pygame.SRCALPHA)
        pygame.draw.rect(surf, VERDE_OSCURO, (10, 5, 10, 50), border_radius=3)
        pygame.draw.rect(surf, VERDE_OSCURO, (0, 15, 12, 8), border_radius=3)
        pygame.draw.rect(surf, VERDE_OSCURO, (18, 25, 12, 8), border_radius=3)
        # Florcita en la punta
        pygame.draw.circle(surf, ROSA_OSCURO, (15, 5), 4)
        pygame.draw.circle(surf, DORADO, (15, 5), 2)
        return surf
    elif tipo == 1:
        # Roca con corazón roto
        surf = pygame.Surface((35, 35), pygame.SRCALPHA)
        puntos = [(17, 0), (35, 12), (30, 35), (5, 35), (0, 12)]
        pygame.draw.polygon(surf, (140, 130, 130), puntos)
        pygame.draw.polygon(surf, (110, 100, 100), puntos, 2)
        # Corazón roto encima
        pygame.draw.circle(surf, (180, 50, 50), (13, 12), 5)
        pygame.draw.circle(surf, (180, 50, 50), (22, 12), 5)
        pygame.draw.polygon(surf, (180, 50, 50), [(8, 14), (27, 14), (17, 26)])
        # Grieta
        pygame.draw.line(surf, NEGRO, (17, 8), (15, 16), 2)
        pygame.draw.line(surf, NEGRO, (15, 16), (19, 20), 2)
        return surf
    else:
        # Obstáculo aéreo (pajarito triste)
        surf = pygame.Surface((30, 25), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (100, 100, 180), (5, 5, 20, 15))
        pygame.draw.polygon(surf, (100, 100, 180), [(0, 8), (8, 12), (5, 5)])  # Ala
        pygame.draw.polygon(surf, (100, 100, 180), [(22, 5), (25, 12), (30, 8)])  # Ala
        pygame.draw.circle(surf, NEGRO, (12, 10), 2)  # Ojo
        pygame.draw.polygon(surf, DORADO, [(18, 11), (25, 13), (18, 15)])  # Pico
        # Gotita triste
        pygame.draw.ellipse(surf, (100, 180, 255), (10, 16, 3, 5))
        return surf

def crear_corazon_coleccionable():
    """Corazón más bonito para recoger"""
    surf = pygame.Surface((24, 24), pygame.SRCALPHA)
    pygame.draw.circle(surf, ROJO, (7, 7), 7)
    pygame.draw.circle(surf, ROJO, (17, 7), 7)
    pygame.draw.polygon(surf, ROJO, [(0, 9), (24, 9), (12, 23)])
    # Brillo
    pygame.draw.circle(surf, (255, 150, 150), (8, 5), 3)
    return surf

IMG_CORAZON_RECOGER = crear_corazon_coleccionable()

# Corazón para partículas (más pequeño)
def crear_corazon_particula():
    surf = pygame.Surface((14, 14), pygame.SRCALPHA)
    pygame.draw.circle(surf, ROJO, (4, 4), 4)
    pygame.draw.circle(surf, ROJO, (10, 4), 4)
    pygame.draw.polygon(surf, ROJO, [(0, 6), (14, 6), (7, 14)])
    return surf

IMG_CORAZON = crear_corazon_particula()

# --- CLASES DEL JUEGO ---
class Jugador:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 48, 52)
        self.rect.midbottom = (100, SUELO_Y)
        self.gravedad = 0
        self.en_suelo = True
        self.saltos_disponibles = 2  # Doble salto
        self.frame = 0
        self.agachado = False
        self.invencible = 0  # Frames de invencibilidad
        self.trail = []  # Estela visual

    def saltar(self):
        if self.agachado:
            return
        if self.saltos_disponibles > 0:
            self.gravedad = -14 if self.saltos_disponibles == 2 else -11
            self.saltos_disponibles -= 1
            self.en_suelo = False
            # Partículas de salto
            for _ in range(5):
                self.trail.append({
                    'x': self.rect.centerx + random.randint(-5, 5),
                    'y': self.rect.bottom,
                    'vy': random.uniform(-2, 0),
                    'vida': 20,
                    'size': random.randint(2, 4)
                })

    def agachar(self, activo):
        if self.en_suelo:
            self.agachado = activo
            if activo:
                viejo_bottom = self.rect.bottom
                self.rect.height = 32
                self.rect.width = 52
                self.rect.bottom = viejo_bottom
            else:
                viejo_bottom = self.rect.bottom
                self.rect.height = 52
                self.rect.width = 48
                self.rect.bottom = viejo_bottom

    def update(self):
        self.frame += 1
        self.gravedad += 0.8  # Gravedad más suave
        self.rect.y += int(self.gravedad)

        if self.rect.bottom >= SUELO_Y:
            self.rect.bottom = SUELO_Y
            self.en_suelo = True
            self.saltos_disponibles = 2
            self.gravedad = 0
        else:
            self.en_suelo = False

        if self.invencible > 0:
            self.invencible -= 1

        # Actualizar estela
        for p in self.trail[:]:
            p['y'] += p['vy']
            p['vida'] -= 1
            if p['vida'] <= 0:
                self.trail.remove(p)

    def draw(self):
        # Dibujar estela
        for p in self.trail:
            alpha = int((p['vida'] / 20) * 150)
            s = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 200, 150, alpha), (p['size'], p['size']), p['size'])
            PANTALLA.blit(s, (p['x'] - p['size'], p['y'] - p['size']))

        # Dibujar gatito (parpadea si es invencible)
        if self.invencible > 0 and self.frame % 4 < 2:
            return
        img = crear_gatito(self.frame, self.agachado)
        PANTALLA.blit(img, self.rect)

        # Indicador de doble salto disponible
        if not self.en_suelo and self.saltos_disponibles > 0:
            s = pygame.Surface((30, 12), pygame.SRCALPHA)
            txt = pygame.font.Font(None, 16).render("x2", True, (255, 200, 100, 200))
            s.blit(txt, (0, 0))
            PANTALLA.blit(s, (self.rect.centerx - 6, self.rect.top - 14))

class Obstaculo:
    def __init__(self, x, velocidad, tipo=None):
        self.tipo = tipo if tipo is not None else random.choice([0, 0, 1, 1, 2])
        self.image = crear_obstaculo_tipo(self.tipo)
        self.rect = self.image.get_rect()
        if self.tipo == 2:  # Aéreo
            self.rect.midbottom = (x, SUELO_Y - 55)
            self.vy = math.sin(random.random() * math.pi)
            self.fase = random.uniform(0, math.pi * 2)
        else:
            self.rect.midbottom = (x, SUELO_Y)
            self.vy = 0
            self.fase = 0
        self.velocidad = velocidad
        self.frame = 0

    def update(self):
        self.rect.x -= self.velocidad
        self.frame += 1
        if self.tipo == 2:
            self.fase += 0.05
            self.rect.y += int(math.sin(self.fase) * 1.5)

    def draw(self):
        # Sombra
        sombra = pygame.Surface((self.rect.width, 6), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 40), sombra.get_rect())
        PANTALLA.blit(sombra, (self.rect.x, SUELO_Y - 3))
        PANTALLA.blit(self.image, self.rect)

class Coleccionable:
    """Corazones que se pueden recoger para puntos extra"""
    def __init__(self, x):
        self.image = IMG_CORAZON_RECOGER
        self.rect = self.image.get_rect(center=(x, SUELO_Y - random.randint(50, 120)))
        self.fase = random.uniform(0, math.pi * 2)
        self.y_base = self.rect.y
        self.recogido = False
        self.anim = 0

    def update(self):
        self.fase += 0.06
        self.rect.y = self.y_base + int(math.sin(self.fase) * 8)
        self.rect.x -= 5
        if self.recogido:
            self.anim += 1

    def draw(self):
        if self.recogido:
            if self.anim < 15:
                escala = 1 + self.anim * 0.1
                alpha = 255 - self.anim * 17
                s = pygame.transform.scale(self.image,
                    (int(24 * escala), int(24 * escala)))
                s.set_alpha(max(0, alpha))
                PANTALLA.blit(s, (self.rect.x - int(12 * (escala - 1)),
                                   self.rect.y - int(12 * (escala - 1))))
            return
        # Brillo pulsante
        brillo = int(abs(math.sin(self.fase * 2)) * 80)
        glow = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 100, 100, brillo), (18, 18), 18)
        PANTALLA.blit(glow, (self.rect.centerx - 18, self.rect.centery - 18))
        PANTALLA.blit(self.image, self.rect)

class Particula:
    def __init__(self, x, y, color=None, escala=1.0):
        self.x = x
        self.y = y
        self.vx = random.uniform(-6, 6) * escala
        self.vy = random.uniform(-8, 2) * escala
        self.vida = 255
        self.rot = random.uniform(0, 360)
        self.rot_vel = random.uniform(-5, 5)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15  # Gravedad en partículas
        self.vida -= 4
        self.rot += self.rot_vel

    def draw(self):
        if self.vida > 0:
            img = IMG_CORAZON.copy()
            img.set_alpha(max(0, self.vida))
            rotado = pygame.transform.rotate(img, self.rot)
            PANTALLA.blit(rotado, (self.x, self.y))

class ScreenShake:
    """Efecto de temblor de pantalla"""
    def __init__(self):
        self.intensidad = 0
        self.duracion = 0

    def activar(self, intensidad=6, duracion=10):
        self.intensidad = intensidad
        self.duracion = duracion

    def get_offset(self):
        if self.duracion > 0:
            self.duracion -= 1
            return (random.randint(-self.intensidad, self.intensidad),
                    random.randint(-self.intensidad, self.intensidad))
        return (0, 0)

# --- ESTADOS DEL JUEGO ---
async def pantalla_titulo():
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_sub = pygame.font.Font(None, 36)

    nubes = [Nube() for _ in range(5)]
    estrellas = [Estrella() for _ in range(25)]
    corazones_bg = []
    frame = 0
    # Ignorar clics durante los primeros frames (evita que el "Ready to start" de Pygbag salte el título)
    cooldown = 30

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if cooldown <= 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

        frame += 1
        if cooldown > 0:
            cooldown -= 1

        # Fondo
        dibujar_cielo_gradiente()

        # Decoraciones
        for e in estrellas:
            e.update(); e.draw()
        for n in nubes:
            n.update(); n.draw()

        # Corazones flotantes
        if random.random() < 0.04:
            corazones_bg.append(CorazonFlotante())
        for c in corazones_bg[:]:
            c.update(); c.draw()
            if c.vida <= 0:
                corazones_bg.remove(c)

        dibujar_suelo(frame * 0.5)

        # Título con sombra y pulso
        escala = 1.0 + math.sin(frame * 0.04) * 0.03
        titulo_texto = "Jueguito Para mi Lucero"
        # Sombra
        sombra = fuente_titulo.render(titulo_texto, True, (150, 50, 70))
        PANTALLA.blit(sombra, (ANCHO//2 - sombra.get_width()//2 + 2, ALTO//2 - 62))
        # Texto principal
        titulo = fuente_titulo.render(titulo_texto, True, ROJO)
        PANTALLA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 64))

        # Subtítulo parpadeante
        if (frame // 40) % 2 == 0:
            texto = fuente_sub.render("Toca la pantalla para empezar", True, ROSA_OSCURO)
            PANTALLA.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 + 20))

        # Gatito decorativo
        gatito = crear_gatito(frame)
        PANTALLA.blit(gatito, (ANCHO//2 - 20, SUELO_Y - 42))

        pygame.display.update()
        RELOJ.tick(FPS)
        await asyncio.sleep(0)

async def juego_principal():
    jugador = Jugador()
    obstaculos = []
    coleccionables = []
    particulas_fx = []
    nubes = [Nube() for _ in range(4)]
    estrellas = [Estrella() for _ in range(15)]
    corazones_bg = []
    shake = ScreenShake()

    cronometro = 0
    crono_corazon = 0
    puntos = 0
    corazones_recogidos = 0
    meta = 7
    velocidad_base = 5
    frame_global = 0

    fuente = pygame.font.Font(None, 38)
    fuente_peq = pygame.font.Font(None, 24)
    fuente_instrucciones = pygame.font.Font(None, 26)
    fuente_combo = pygame.font.Font(None, 32)

    mensajes_flotantes = []  # Textos tipo "+1" que flotan

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    jugador.saltar()
                if event.key == pygame.K_DOWN:
                    jugador.agachar(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    jugador.agachar(False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                jugador.saltar()

        frame_global += 1
        # Dificultad progresiva
        progreso = min(puntos / meta, 1.0)
        velocidad = velocidad_base + progreso * 3
        spawn_rate = max(55, 90 - int(progreso * 35))

        # --- DIBUJAR FONDO ---
        offset_shake = shake.get_offset()
        dibujar_cielo_gradiente()

        for e in estrellas:
            e.update(); e.draw()
        for n in nubes:
            n.update(); n.draw()

        if random.random() < 0.02:
            corazones_bg.append(CorazonFlotante())
        for c in corazones_bg[:]:
            c.update(); c.draw()
            if c.vida <= 0:
                corazones_bg.remove(c)

        dibujar_suelo(frame_global * velocidad * 0.5)

        # --- LÓGICA JUGADOR ---
        jugador.update()
        jugador.draw()

        # --- LÓGICA OBSTÁCULOS ---
        cronometro += 1
        if cronometro > spawn_rate:
            tipo = random.choices([0, 1, 2], weights=[3, 3, 2])[0]
            obstaculos.append(Obstaculo(ANCHO + random.randint(20, 120), velocidad, tipo))
            cronometro = 0

        # --- COLECCIONABLES ---
        crono_corazon += 1
        if crono_corazon > 130 and random.random() < 0.4:
            coleccionables.append(Coleccionable(ANCHO + random.randint(50, 150)))
            crono_corazon = 0

        for col in coleccionables[:]:
            col.update()
            col.draw()
            if not col.recogido and jugador.rect.colliderect(col.rect):
                col.recogido = True
                corazones_recogidos += 1
                mensajes_flotantes.append({
                    'texto': '+1',
                    'x': col.rect.centerx,
                    'y': col.rect.y,
                    'vida': 40,
                    'color': ROJO
                })
                for _ in range(8):
                    particulas_fx.append(Particula(col.rect.centerx, col.rect.centery, escala=0.5))
            if col.rect.right < -20 or (col.recogido and col.anim > 15):
                coleccionables.remove(col)

        for obs in obstaculos[:]:
            obs.update()
            obs.draw()
            if obs.rect.right < 0:
                obstaculos.remove(obs)
                puntos += 1
                mensajes_flotantes.append({
                    'texto': 'Drama superado!',
                    'x': 100,
                    'y': SUELO_Y - 80,
                    'vida': 50,
                    'color': ROSA_OSCURO
                })
            elif jugador.rect.colliderect(obs.rect) and jugador.invencible <= 0:
                obstaculos.remove(obs)
                jugador.invencible = 60
                shake.activar(8, 15)
                # Partículas de impacto
                for _ in range(15):
                    particulas_fx.append(Particula(
                        jugador.rect.centerx, jugador.rect.centery, escala=0.7))
                mensajes_flotantes.append({
                    'texto': 'Ouch!',
                    'x': jugador.rect.centerx,
                    'y': jugador.rect.top - 20,
                    'vida': 40,
                    'color': (200, 50, 50)
                })

        # --- PARTICULAS FX ---
        for p in particulas_fx[:]:
            p.update(); p.draw()
            if p.vida <= 0:
                particulas_fx.remove(p)

        # --- MENSAJES FLOTANTES ---
        for m in mensajes_flotantes[:]:
            m['y'] -= 1.5
            m['vida'] -= 1
            alpha = max(0, min(255, m['vida'] * 6))
            txt_surf = fuente_combo.render(m['texto'], True, m['color'])
            txt_surf.set_alpha(alpha)
            PANTALLA.blit(txt_surf, (m['x'] - txt_surf.get_width()//2, m['y']))
            if m['vida'] <= 0:
                mensajes_flotantes.remove(m)

        # --- UI ---
        # Barra de progreso
        barra_w = 200
        barra_h = 16
        barra_x = 20
        barra_y = 18
        # Fondo barra
        pygame.draw.rect(PANTALLA, (0, 0, 0, 80), (barra_x - 1, barra_y - 1, barra_w + 2, barra_h + 2), border_radius=8)
        pygame.draw.rect(PANTALLA, (80, 60, 60), (barra_x, barra_y, barra_w, barra_h), border_radius=8)
        # Relleno
        fill_w = int((puntos / meta) * barra_w)
        if fill_w > 0:
            pygame.draw.rect(PANTALLA, ROSA_OSCURO, (barra_x, barra_y, fill_w, barra_h), border_radius=8)
        # Texto en barra
        txt_barra = fuente_peq.render(f"Dramas: {puntos}/{meta}", True, BLANCO)
        PANTALLA.blit(txt_barra, (barra_x + barra_w//2 - txt_barra.get_width()//2, barra_y - 1))

        # Corazones recogidos
        for i in range(corazones_recogidos):
            mini = pygame.transform.scale(IMG_CORAZON_RECOGER, (16, 16))
            PANTALLA.blit(mini, (barra_x + i * 20, barra_y + barra_h + 6))

        # Instrucciones
        txt_inst = fuente_instrucciones.render("Toca/Espacio: saltar  |  Abajo: agacharse", True, (100, 70, 70))
        PANTALLA.blit(txt_inst, (ANCHO - txt_inst.get_width() - 15, 18))

        # Indicador doble salto
        txt_ds = fuente_peq.render("Doble salto!", True, DORADO)
        PANTALLA.blit(txt_ds, (ANCHO - txt_ds.get_width() - 15, 40))

        if puntos >= meta:
            return

        # Aplicar shake
        if offset_shake != (0, 0):
            pantalla_copia = PANTALLA.copy()
            PANTALLA.fill(NEGRO)
            PANTALLA.blit(pantalla_copia, offset_shake)

        pygame.display.update()
        RELOJ.tick(FPS)
        await asyncio.sleep(0)

async def pantalla_propuesta():
    fuente_grande = pygame.font.Font(None, 58)
    fuente_btn = pygame.font.Font(None, 42)

    pregunta = fuente_grande.render("¿Quieres salir conmigo el 14?", True, ROJO)

    btn_si = pygame.Rect(ANCHO//2 - 150, 300, 120, 55)
    btn_no = pygame.Rect(ANCHO//2 + 50, 300, 120, 55)

    particulas = []
    corazones_bg = []
    nubes = [Nube() for _ in range(4)]
    estrellas = [Estrella() for _ in range(20)]
    aceptado = False
    frame = 0
    btn_si_hover = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not aceptado:
                if btn_si.collidepoint(mouse_pos):
                    aceptado = True
                    for _ in range(150):
                        particulas.append(Particula(
                            ANCHO//2 + random.randint(-100, 100),
                            ALTO//2 + random.randint(-50, 50),
                            escala=1.2))

        # Botón NO se escapa
        if not aceptado and btn_no.collidepoint(mouse_pos):
            btn_no.x = random.randint(50, ANCHO - 170)
            btn_no.y = random.randint(50, ALTO - 110)

        btn_si_hover = btn_si.collidepoint(mouse_pos)

        # --- DIBUJAR ---
        dibujar_cielo_gradiente()
        for e in estrellas:
            e.update(); e.draw()
        for n in nubes:
            n.update(); n.draw()

        if random.random() < 0.06:
            corazones_bg.append(CorazonFlotante())
        for c in corazones_bg[:]:
            c.update(); c.draw()
            if c.vida <= 0:
                corazones_bg.remove(c)

        dibujar_suelo(frame * 0.3)

        if not aceptado:
            # Pregunta con sombra
            sombra = fuente_grande.render("Quieres salir conmigo el 14?", True, (150, 50, 70))
            PANTALLA.blit(sombra, (ANCHO//2 - sombra.get_width()//2 + 2, 152))
            PANTALLA.blit(pregunta, (ANCHO//2 - pregunta.get_width()//2, 150))

            # Botón SÍ (con efecto hover)
            si_color = (0, 220, 80) if not btn_si_hover else (0, 255, 100)
            si_rect = btn_si.inflate(6, 6) if btn_si_hover else btn_si
            # Sombra del botón
            pygame.draw.rect(PANTALLA, (0, 0, 0, 60),
                             si_rect.move(3, 3), border_radius=12)
            pygame.draw.rect(PANTALLA, si_color, si_rect, border_radius=12)
            pygame.draw.rect(PANTALLA, BLANCO, si_rect, 2, border_radius=12)
            txt_si = fuente_btn.render("SÍ!", True, BLANCO)
            PANTALLA.blit(txt_si, (si_rect.centerx - txt_si.get_width()//2,
                                    si_rect.centery - txt_si.get_height()//2))

            # Botón NO
            pygame.draw.rect(PANTALLA, (0, 0, 0, 60),
                             btn_no.move(3, 3), border_radius=12)
            pygame.draw.rect(PANTALLA, ROJO, btn_no, border_radius=12)
            pygame.draw.rect(PANTALLA, BLANCO, btn_no, 2, border_radius=12)
            txt_no = fuente_btn.render("NO", True, BLANCO)
            PANTALLA.blit(txt_no, (btn_no.centerx - txt_no.get_width()//2,
                                    btn_no.centery - txt_no.get_height()//2))

            # Gatito esperando
            gatito = crear_gatito(frame)
            PANTALLA.blit(gatito, (ANCHO//2 - 20, SUELO_Y - 42))
        else:
            # Pantalla de éxito
            pulso = 1.0 + math.sin(frame * 0.06) * 0.05
            txt_fin1 = fuente_grande.render("Nos vemos el 14 para ir", True, ROJO)
            txt_fin2 = fuente_grande.render("a tu playa fake xd!", True, ROJO)
            PANTALLA.blit(txt_fin1, (ANCHO//2 - txt_fin1.get_width()//2, ALTO//2 - 40))
            PANTALLA.blit(txt_fin2, (ANCHO//2 - txt_fin2.get_width()//2, ALTO//2 + 15))

            # Lluvia continua de partículas
            if len(particulas) < 80:
                for _ in range(3):
                    particulas.append(Particula(
                        random.randint(100, ANCHO - 100),
                        random.randint(50, ALTO - 100)))

            for p in particulas[:]:
                p.update(); p.draw()
                if p.vida <= 0:
                    particulas.remove(p)

        pygame.display.update()
        RELOJ.tick(FPS)
        await asyncio.sleep(0)

# --- EJECUCIÓN ---
async def main():
    await pantalla_titulo()
    await juego_principal()
    await pantalla_propuesta()

# Ejecución compatible con Pygbag y Python normal
if __name__ == "__main__":
    asyncio.run(main())