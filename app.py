import pygame
import random
import os

TELA_LARGURA = 1000
TELA_ALTURA = 400
ESCALA = 1.3

IMAGENS_OBSTACULO = [
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'cacto1.png')), ESCALA),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'cacto2.png')), ESCALA),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'cacto3.png')), ESCALA),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'cacto4.png')), ESCALA),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'cacto5.png')), ESCALA),
    [pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'ave1.png')), ESCALA),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'ave2.png')), ESCALA)]
]
IMAGEM_CHAO = [
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'chao1.png')), 2.5),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'chao2.png')), 2.5)
]
IMAGEM_NUVEM = pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'nuvem.png')), ESCALA)
IMAGENS_DINO = [
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'dino1.png')), ESCALA),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'dino2.png')), ESCALA),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'dino3.png')), ESCALA)
]
IMAGENS_DINO_ABAIXADO = [
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'dino1_abaixado.png')), ESCALA),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'dino2_abaixado.png')), ESCALA),
    pygame.transform.scale_by(pygame.image.load(os.path.join('imgs', 'dino3_abaixado.png')), ESCALA)
]

pygame.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 30)
FONTE_REINICIAR = pygame.font.SysFont('arial', 15)

class Dino():
    IMAGEM = IMAGENS_DINO
    IMAGEM_ABAIXADO = IMAGENS_DINO_ABAIXADO
    IMAGEM_ATUAL = IMAGEM
    TEMPO_ANIMACAO = 2.5
    
    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.contagem_imagem = 0
        self.imagem = self.IMAGEM[0]
        self.pos_y = 240
        self.pulando = False
        self.abaixado = False
        self.deslocamento = 0
    
    
    def pular(self):
        self.pulando = True
    
    
    def abaixar(self):
        self.IMAGEM_ATUAL = self.IMAGEM_ABAIXADO
        self.imagem = self.IMAGEM_ATUAL[0]
        self.abaixado = True
    
    
    def mover(self):
        self.deslocamento = 0
        if self.pulando == True:
            self.contagem_imagem = 0
            self.deslocamento = -12
            if self.y < 90:
                self.deslocamento = -8
            if self.y < 75:
                self.deslocamento = -3
            if self.y < 60:
                self.deslocamento = 0
                self.pulando = False 
        else:
            if self.pos_y > self.y:
                if self.abaixado == True:
                    self.deslocamento = 20
                else:
                    self.deslocamento = 11
            else:
                self.y = self.pos_y
                
        self.y += self.deslocamento
    
    
    def levantar(self):
        self.IMAGEM_ATUAL = self.IMAGEM
    
    
    def desenhar(self, tela):
        self.contagem_imagem += 1
        
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMAGEM_ATUAL[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMAGEM_ATUAL[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMAGEM_ATUAL[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMAGEM_ATUAL[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*5:
            self.imagem = self.IMAGEM_ATUAL[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*6:
            self.imagem = self.IMAGEM_ATUAL[2]
            self.contagem_imagem = 0
        
        tela.blit(self.imagem, (self.x, self.y))   
    
    
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Obstaculo():
    VELOCIDADE = 15
    IMG = IMAGENS_OBSTACULO
    TEMPO_ANIMACAO = 5
    
    def __init__(self):
        self.y = 240
        self.y_ave = 180
        self.x = 2000
        self.obstaculo = random.randint(0, 5)
        self.contagem__imagem = 0
        self.sn = 0
    
    
    def mover(self):
        if self.obstaculo == 5:
            if self.x + self.IMG[5][0].get_width() < 0:
                self.sn = random.randint(0, 2)
                self.x = 1000
                self.obstaculo = random.randint(0, 5)
            if self.sn == 0:
                self.y_ave = 90
            elif self.sn >= 1:
                self.y_ave = 180
        else:
            if self.x + self.IMG[self.obstaculo].get_width() < 0:
                self.x = 1000
                self.obstaculo = random.randint(0, 5)
    
    
    def colidir(self, dino):
        dino_mask = dino.get_mask()
        if self.obstaculo == 5:
            obstaculo_mask = pygame.mask.from_surface(self.IMG[5][0])
            distancia = (self.x - dino.x, self.y_ave - dino.y)
        else:
            obstaculo_mask = pygame.mask.from_surface(self.IMG[self.obstaculo])
            distancia = (self.x - dino.x, self.y - dino.y)
        
        tocou = dino_mask.overlap(obstaculo_mask, distancia)
        
        if tocou:
            return True
        else:
            return False
    
    
    def desenhar(self, tela):
        if self.obstaculo == 5:
            self.contagem__imagem += 1
            if self.contagem__imagem < self.TEMPO_ANIMACAO:
                tela.blit(self.IMG[5][0], (self.x, self.y_ave))
            elif self.contagem__imagem < self.TEMPO_ANIMACAO*2:
                tela.blit(self.IMG[5][0], (self.x, self.y_ave))
            elif self.contagem__imagem < self.TEMPO_ANIMACAO*3:
                tela.blit(self.IMG[5][1], (self.x, self.y_ave))
            elif self.contagem__imagem < self.TEMPO_ANIMACAO*4:
                tela.blit(self.IMG[5][1], (self.x, self.y_ave))
                self.contagem__imagem = 0
        else:
            tela.blit(self.IMG[self.obstaculo], (self.x, self.y))


class Chao():
    VELOCIDADE = 15
    LARGURA = IMAGEM_CHAO[0].get_width()
    IMAGEM = IMAGEM_CHAO
    
    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA
    
    
    def mover(self):
        if self.x0 + self.LARGURA < 0:
            self.x0 = self.x1 + self.LARGURA
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x0 + self.LARGURA
    
    
    def desenhar(self, tela):
        tela.blit(self.IMAGEM[0], (self.x0, self.y))
        tela.blit(self.IMAGEM[1], (self.x1, self.y))


class Nuvens():
    IMAGEM = IMAGEM_NUVEM
    VELOCIDADE = 1
    def __init__(self):
        self.altura = [random.randint(10, 150), random.randint(10, 150), random.randint(10, 150)]
        self.X = [random.randint(1000, 1300), random.randint(1300, 1600), random.randint(1600, 2000)]
    
    def mover(self):
        c = 0
        for i, _ in enumerate(self.X):
            self.X[i] -= self.VELOCIDADE
            if self.X[i] + self.IMAGEM.get_width() < 0:
                if c == 0:
                    self.X[i] = random.randint(1000, 1300)
                elif c == 1:
                    self.X[i] = random.randint(1300, 1600)
                elif c == 2:
                    self.X[i] = random.randint(1600, 2000)
                    c = 0
                self.altura[i] = random.randint(10, 150)
                c += 1
    
    
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.X[0], self.altura[0]))
        tela.blit(self.IMAGEM, (self.X[1], self.altura[1]))
        tela.blit(self.IMAGEM, (self.X[2], self.altura[2]))


def game_over_txt(tela):
    texto = FONTE_PONTOS.render('GAME OVER!!', 1, (000, 000, 000))
    reiniciar = FONTE_REINICIAR.render('pule para reiniciar', 0.5, (000, 000, 000))
    tela.blit(texto, (500 - texto.get_width() // 2, 200 - texto.get_height()))
    tela.blit(reiniciar, (500 - reiniciar.get_width() // 2,170 + texto.get_height()))


def desenhar_tela(tela, chao, nuvem, dino, obstaculo, pontos, gameover=''):
    chao.desenhar(tela)

    texto = FONTE_PONTOS.render(f'PONTUAÇÃO: {pontos:.3f}', 1, (000, 0000, 000))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    
    nuvem.desenhar(tela)
    dino.desenhar(tela)
    obstaculo.desenhar(tela)
    if gameover:
        gameover(tela)
    pygame.display.update()


def main():
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    relogio = pygame.time.Clock()
    chao = Chao(300)
    nuvem = Nuvens()
    dino = Dino(40, 240)
    obstaculo = Obstaculo()
    velocidade = 15
    pontos = 0
    rodando = True
    colidiu = False
    
    while rodando:
        relogio.tick(60)
        tela.fill("white")
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_SPACE, pygame.K_UP]:
                    if colidiu:
                        obstaculo.x = 2000
                        obstaculo.obstaculo = random.randint(0, 5)
                        dino.y = 240
                        dino.pulando = False
                        dino.IMAGEM_ATUAL = dino.IMAGEM
                        nuvem.X = [random.randint(1000, 1300), random.randint(1300, 1600), random.randint(1600, 2000)]
                        chao.x0 = 0
                        chao.x1 = chao.LARGURA
                        velocidade = 15
                        pontos = 0
                        colidiu = False
                    elif dino.pos_y == dino.y:
                        dino.levantar()
                        dino.pular()
                if evento.key == pygame.K_DOWN and colidiu == False:
                    dino.abaixar()
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_DOWN and colidiu == False:
                    dino.levantar()
                    dino.abaixado = False
        
        # jogo
        if obstaculo.colidir(dino=dino):
            pass
            '''dino.contagem_imagem = 0
            obstaculo.contagem__imagem = 0
            colidiu = True'''
        if colidiu:
            desenhar_tela(tela, chao, nuvem, dino, obstaculo, pontos, game_over_txt(tela))
        else:
            desenhar_tela(tela, chao, nuvem, dino, obstaculo, pontos)
            dino.mover()
            obstaculo.x -= velocidade
            chao.x0 -= velocidade
            chao.x1 -= velocidade
            obstaculo.mover()
            chao.mover()
            nuvem.mover()
            pontos += 0.0002
            velocidade += 0.001


if __name__ == '__main__':
    main()
