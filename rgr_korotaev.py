from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
import math
import sys

xRot = 0
xPos = 0
zPos = 0
golova = 0

golova_svet = True
model_svet = True
plazma_svet = True

model_svetH = 0

global model
global pol_and_potolok
global pol_and_potolok_1
global dveri
global stena_cool
global plazma_t
global stena

posDelta = 1


def chek_golova_svet():
    global golova_svet
    golova_svet = (golova_svet != True)

    if golova_svet:
        glEnable(GL_LIGHT1)
    else:
        glDisable(GL_LIGHT1)


def chek_plazma_svet():
    global plazma_svet
    plazma_svet = (plazma_svet != True)

    if plazma_svet:
        glEnable(GL_LIGHT2)
    else:
        glDisable(GL_LIGHT2)


def chek_model_svet():
    global model_svet
    model_svet = (model_svet != True)

    if model_svet:
        glEnable(GL_LIGHT3)
    else:
        glDisable(GL_LIGHT3)


def Keys_upravlenie(key, x, y):
    global xRot
    global zPos
    global xPos
    global golova

    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:  # Клавиша вверх
        zPos += posDelta * math.cos(math.radians(xRot))
        xPos += posDelta * math.sin(math.radians(xRot))
        golova += 1
    if key == GLUT_KEY_DOWN:  # Клавиша вниз
        zPos -= posDelta * math.cos(math.radians(xRot))
        xPos -= posDelta * math.sin(math.radians(xRot))
        golova -= 1
    if key == GLUT_KEY_LEFT:  # Клавиша влево
        xRot -= 15
    if key == GLUT_KEY_RIGHT:  # Клавиша вправо
        xRot += 15
    if key == GLUT_KEY_HOME:
        chek_golova_svet()
        print("Игрок как источник света вкл/выкл")
    if key == GLUT_KEY_PAGE_UP:
        chek_plazma_svet()
        print("Свет у красивой стены вкл/выкл")
    if key == GLUT_KEY_PAGE_DOWN:
        chek_model_svet()
        print("Свет у модельки вкл/выкл")
    # print("по иксу={}, по зету={}, угол относительно нуля={}".format(xPos, zPos, xRot))
    glutPostRedisplay()  # Вызываем процедуру перерисовки


def load_texture(file_name: str):
    image = Image.open(file_name)
    image.load()
    width, height = image.size
    textureData = np.asarray(image)
    textureData = textureData[::-1]
    image.close()

    t_Id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, t_Id)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)  # сообщаем как хранить данные текстуры
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
                    GL_REPEAT)  # накладвем текстуры с параметрами. (текстура 2д, параметр обтекания, повторяет текстуру)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                    GL_LINEAR)  # параметры фильтрации. сренее значение тикстелей накладываем пиксель
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # миг и ман ужимает и растягивает

    if "png" in file_name:
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    else:
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

    return t_Id


def drawWalls(xSize, ySize, zSize):
    glPushMatrix()

    glCullFace(GL_BACK)  # тыльная стороная текстуры
    glFrontFace(GL_CW)  # лицевая сторона текстуры. обход по часовой стрелке

    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (1, 0.5, 1, 1))  # свойства материалов. зеркальное отражение
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 50)  # свечение текстур

    glTranslatef(-xSize / 2, -ySize / 2,
                 -zSize / 2)  # умножает текущую матрицу на  матрицу сдвига и двигает по векторам

    glEnable(GL_TEXTURE_2D)

    # front
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)  # создание квадрата
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.1, zSize * 0.1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 0.1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 0.1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.1, zSize * 0.1)
    glEnd()

    # front-bottom
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)  # создание квадрата
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 0.1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 0.1)
    glEnd()

    # front-front
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)  # создание квадрата
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0, ySize * 0.2, zSize * 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0, ySize * 0, zSize * 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 1, ySize * 0, zSize * 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 1, ySize * 0.2, zSize * 0)
    glEnd()

    # back
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.1, zSize * 0.9)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 0.9)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 0.9)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.1, zSize * 0.9)
    glEnd()

    # back-bottom
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 0.9)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 0.9)
    glEnd()

    # back-front
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 1, ySize * 0.2, zSize * 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 1, ySize * 0.0, zSize * 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0, ySize * 0.0, zSize * 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0, ySize * 0.2, zSize * 1)
    glEnd()

    # right
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.1, zSize * 0.1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 0.1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 0.9)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.1, zSize * 0.9)
    glEnd()

    # right-bottom
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 1, ySize * 0.2, zSize * 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 1, ySize * 0.2, zSize * 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.2, zSize * 1)
    glEnd()

    # right-front
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 1, ySize * 0.2, zSize * 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 1, ySize * 0, zSize * 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 1, ySize * 0, zSize * 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 1, ySize * 0.2, zSize * 1)
    glEnd()

    # left
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.1, zSize * 0.9)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 0.9)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 0.1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.1, zSize * 0.1)
    glEnd()

    # left-bottom
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0, ySize * 0.2, zSize * 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0, ySize * 0.2, zSize * 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.2, zSize * 0)
    glEnd()

    # left-front
    glBindTexture(GL_TEXTURE_2D, stena_cool)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0, ySize * 0.2, zSize * 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0, ySize * 0, zSize * 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0, ySize * 0, zSize * 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0, ySize * 0.2, zSize * 0)
    glEnd()

    # bottom
    glBindTexture(GL_TEXTURE_2D, pol_and_potolok)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.1, zSize * 0.9)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.1, zSize * 0.1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.1, zSize * 0.1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.1, zSize * 0.9)
    glEnd()

    # сзади правая front
    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.925, ySize * 0.2, zSize * 0.975)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.925, ySize * 0.8, zSize * 0.975)
    glTexCoord2f(0.25, 1.0)
    glVertex3f(xSize * 0.975, ySize * 0.8, zSize * 0.975)
    glTexCoord2f(0.25, 0.0)
    glVertex3f(xSize * 0.975, ySize * 0.2, zSize * 0.975)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.25, 0.0)
    glVertex3f(xSize * 0.975, ySize * 0.8, zSize * 0.975)
    glTexCoord2f(0.25, 1.0)
    glVertex3f(xSize * 0.975, ySize * 0.2, zSize * 0.975)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(xSize * 0.975, ySize * 0.2, zSize * 0.925)
    glTexCoord2f(0.5, 0.0)
    glVertex3f(xSize * 0.975, ySize * 0.8, zSize * 0.925)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.5, 0.0)
    glVertex3f(xSize * 0.975, ySize * 0.2, zSize * 0.925)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(xSize * 0.975, ySize * 0.8, zSize * 0.925)
    glTexCoord2f(0.75, 1.0)
    glVertex3f(xSize * 0.925, ySize * 0.8, zSize * 0.925)
    glTexCoord2f(0.75, 0.0)
    glVertex3f(xSize * 0.925, ySize * 0.2, zSize * 0.925)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.75, 0.0)
    glVertex3f(xSize * 0.925, ySize * 0.8, zSize * 0.925)
    glTexCoord2f(0.75, 1.0)
    glVertex3f(xSize * 0.925, ySize * 0.2, zSize * 0.925)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.925, ySize * 0.2, zSize * 0.975)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.925, ySize * 0.8, zSize * 0.975)
    glEnd()

    # сзади слева front
    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.025, ySize * 0.2, zSize * 0.975)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.025, ySize * 0.8, zSize * 0.975)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.075, ySize * 0.8, zSize * 0.975)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.075, ySize * 0.2, zSize * 0.975)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.075, ySize * 0.8, zSize * 0.975)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.075, ySize * 0.2, zSize * 0.975)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.075, ySize * 0.2, zSize * 0.925)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.075, ySize * 0.8, zSize * 0.925)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.075, ySize * 0.2, zSize * 0.925)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.075, ySize * 0.8, zSize * 0.925)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.025, ySize * 0.8, zSize * 0.925)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.025, ySize * 0.2, zSize * 0.925)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.025, ySize * 0.8, zSize * 0.925)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.025, ySize * 0.2, zSize * 0.925)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.025, ySize * 0.2, zSize * 0.975)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.025, ySize * 0.8, zSize * 0.975)
    glEnd()

    # спереди правая front
    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.925, ySize * 0.2, zSize * 0.075)
    glTexCoord2f(0.0, 10.0)
    glVertex3f(xSize * 0.925, ySize * 0.8, zSize * 0.075)
    glTexCoord2f(1.0, 10.0)
    glVertex3f(xSize * 0.975, ySize * 0.8, zSize * 0.075)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.975, ySize * 0.2, zSize * 0.075)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.975, ySize * 0.8, zSize * 0.075)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.975, ySize * 0.2, zSize * 0.075)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.975, ySize * 0.2, zSize * 0.025)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.975, ySize * 0.8, zSize * 0.025)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.975, ySize * 0.2, zSize * 0.025)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.975, ySize * 0.8, zSize * 0.025)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.925, ySize * 0.8, zSize * 0.025)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.925, ySize * 0.2, zSize * 0.025)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.925, ySize * 0.8, zSize * 0.025)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.925, ySize * 0.2, zSize * 0.025)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.925, ySize * 0.2, zSize * 0.075)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.925, ySize * 0.8, zSize * 0.075)
    glEnd()

    # спереди левая front
    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.025, ySize * 0.2, zSize * 0.075)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.025, ySize * 0.8, zSize * 0.075)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.075, ySize * 0.8, zSize * 0.075)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.075, ySize * 0.2, zSize * 0.075)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.075, ySize * 0.8, zSize * 0.075)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.075, ySize * 0.2, zSize * 0.075)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.075, ySize * 0.2, zSize * 0.025)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.075, ySize * 0.8, zSize * 0.025)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.075, ySize * 0.2, zSize * 0.025)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.075, ySize * 0.8, zSize * 0.025)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.025, ySize * 0.8, zSize * 0.025)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.025, ySize * 0.2, zSize * 0.025)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, plazma_t)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.025, ySize * 0.8, zSize * 0.025)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.025, ySize * 0.2, zSize * 0.025)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.025, ySize * 0.2, zSize * 0.075)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.025, ySize * 0.8, zSize * 0.075)
    glEnd()

    # front
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)  # создание квадрата
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 0.1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 1, zSize * 0.1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 1, zSize * 0.1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 0.1)
    glEnd()

    # front-bottom
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)  # создание квадрата
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 0.1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 0.1)
    glEnd()

    # front-front
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)  # создание квадрата
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0, ySize * 1, zSize * 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0, ySize * 0.8, zSize * 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 1, ySize * 0.8, zSize * 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 1, ySize * 1, zSize * 0)
    glEnd()

    # back
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 0.9)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 1, zSize * 0.9)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 1, zSize * 0.9)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 0.9)
    glEnd()

    # back-bottom
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 0.9)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 0.9)
    glEnd()

    # back-front
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 1, ySize * 1, zSize * 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 1, ySize * 0.8, zSize * 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0, ySize * 0.8, zSize * 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0, ySize * 1, zSize * 1)
    glEnd()

    # right
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 0.1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 1, zSize * 0.1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 1, zSize * 0.9)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 0.9)
    glEnd()

    # right-bottom
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 1, ySize * 0.8, zSize * 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 1, ySize * 0.8, zSize * 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 0.8, zSize * 1)
    glEnd()

    # right-front
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 1, ySize * 1, zSize * 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 1, ySize * 0.8, zSize * 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 1, ySize * 0.8, zSize * 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 1, ySize * 1, zSize * 1)
    glEnd()

    # left
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 0.9)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 1, zSize * 0.9)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 1, zSize * 0.1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 0.1)
    glEnd()

    # left-bottom
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0, ySize * 0.8, zSize * 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0, ySize * 0.8, zSize * 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.1, ySize * 0.8, zSize * 0)
    glEnd()

    # left-front
    glBindTexture(GL_TEXTURE_2D, stena)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0, ySize * 1, zSize * 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0, ySize * 0.8, zSize * 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0, ySize * 0.8, zSize * 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0, ySize * 1, zSize * 0)
    glEnd()

    # bottom
    glBindTexture(GL_TEXTURE_2D, pol_and_potolok_1)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 1, zSize * 0.9)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize * 0.1, ySize * 1, zSize * 0.1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 1, zSize * 0.1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.9, ySize * 1, zSize * 0.9)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()


def drawRoom():
    glPushMatrix()
    drawWalls(100, 100, 100)

    glPushMatrix()
    drawModel(100, 100, 100)
    glPopMatrix()

    draw_model_svet()
    drawFireplaceLight()
    glPopMatrix()


def drawModel(xSize, ySize, zSize):
    glPushMatrix()

    glEnable(GL_TEXTURE_2D)

    glTranslatef(xSize * -0.4, ySize * -0.45, zSize * -0.4)
    glRotatef(10, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, dveri)
    glBegin(GL_TRIANGLE_STRIP)
    glVertex3f(xSize * -0.004, ySize * 0, zSize * 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.004, ySize * 0, zSize * 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * -0.003, ySize * 0.1, zSize * 0.02)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0.003, ySize * 0.1, zSize * 0.02)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * -0.002, ySize * 0.2, zSize * 0.05)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize * 0.002, ySize * 0.2, zSize * 0.05)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize * 0, ySize * 0.3, zSize * 0.09)
    glTexCoord2f(1.0, 1.0)
    glEnd()

    glRotatef(30, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, dveri)
    glBegin(GL_TRIANGLE_STRIP)
    glVertex3f(xSize * -0.004, ySize * 0, zSize * 0)
    glVertex3f(xSize * 0.004, ySize * 0, zSize * 0)
    glVertex3f(xSize * -0.003, ySize * 0.1, zSize * 0.02)
    glVertex3f(xSize * 0.003, ySize * 0.1, zSize * 0.02)
    glVertex3f(xSize * -0.002, ySize * 0.2, zSize * 0.05)
    glVertex3f(xSize * 0.002, ySize * 0.2, zSize * 0.05)
    glVertex3f(xSize * 0, ySize * 0.3, zSize * 0.09)
    glEnd()

    glRotatef(20, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, dveri)
    glBegin(GL_TRIANGLE_STRIP)
    glVertex3f(xSize * -0.004, ySize * 0, zSize * 0)
    glVertex3f(xSize * 0.004, ySize * 0, zSize * 0)
    glVertex3f(xSize * -0.003, ySize * 0.1, zSize * 0.02)
    glVertex3f(xSize * 0.003, ySize * 0.1, zSize * 0.02)
    glVertex3f(xSize * -0.002, ySize * 0.2, zSize * 0.05)
    glVertex3f(xSize * 0.002, ySize * 0.2, zSize * 0.05)
    glVertex3f(xSize * 0, ySize * 0.3, zSize * 0.09)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)

    glPopMatrix()


def drawPlayerLight():
    global xPos
    global zPos
    global model_svetH

    colors = list((model_svetH, 0.3, 0.12))
    if golova_svet:
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glTranslate(xPos, 0, -zPos + 20)  # умножает текущую матрицу на  матрицу сдвига и двигает по вектору XZ
        glEnable(GL_LIGHT1)
        glLight(GL_LIGHT1, GL_POSITION, (xPos, 0, -zPos + 20, 1))  # позиция в пространстве
        glLight(GL_LIGHT1, GL_AMBIENT, (0.2, 0.2, 0.2, 1))  # можность фонового освещения
        glLight(GL_LIGHT1, GL_DIFFUSE, (0.2, 0.2, 0.2, 1))  # мощность рассеяного освещения
        glLight(GL_LIGHT1, GL_DIFFUSE, colors)
        glLight(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0)
        glLight(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.00001)
        glPopMatrix()
    else:
        glDisable(GL_LIGHT1)


def drawFireplaceLight():

    if plazma_svet:
        glPushMatrix()
        glLoadIdentity()

        glEnable(GL_LIGHT2)
        glLight(GL_LIGHT2, GL_POSITION, (30, 10, 30, 1))  # позиция в пространстве
        glLight(GL_LIGHT2, GL_DIFFUSE, (200, 0, 0, 0))  # мощность рассеяного освещения
        glLight(GL_LIGHT2, GL_SPOT_DIRECTION, (-1, -1, 0))  # направление
        glLight(GL_LIGHT2, GL_SPOT_CUTOFF, 50)  # угол между осью и стороной конуса света
        glLight(GL_LIGHT2, GL_SPECULAR, (1, 1, 1, 0))  # мощность отсвещения
        glLight(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.00999)  # квадратичное затухание
        glPopMatrix()
    else:
        glDisable(GL_LIGHT2)


def draw_model_svet():
    global model_svetH

    if model_svet:
        glPushMatrix()
        glLoadIdentity()

        colors = list((model_svetH, 0.1, 50))
        colors.append(1)
        glEnable(GL_LIGHT3)
        glLight(GL_LIGHT3, GL_POSITION, (100, 100, 100, 1))  # положение в пространстве
        glLight(GL_LIGHT3, GL_DIFFUSE, colors)  # мощность рассеяного освещения
        glLight(GL_LIGHT3, GL_SPOT_DIRECTION, (0, 0, -1))  # направление свечения
        glLight(GL_LIGHT3, GL_SPOT_CUTOFF, 90)  # угол между осью и стороной конуса света
        glLight(GL_LIGHT3, GL_SPECULAR, (100, 0, 100, 1000))  # мощность отсвещения
        glLight(GL_LIGHT3, GL_QUADRATIC_ATTENUATION, 0.0005)  # квадратичное затухание
        glPopMatrix()
    else:
        glDisable(GL_LIGHT3)


# Процедура перерисовки
def draw():
    global xRot
    global zPos
    global xPos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    drawPlayerLight()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-10.0, 10.0, -10.0, 10.0, 10,
              200.0)  # перспективная проекция. определяет как все будет выглядеть на экране
    glRotate(xRot, 0, 1, 0)

    glTranslate(-xPos, 1, zPos)  # умножает текущую матрицу на  матрицу сдвига и двигае камеру по вектору XZ
    glMatrixMode(GL_MODELVIEW)  # указывает на ту матрицу с которой будут преобразования
    drawRoom()
    glutSwapBuffers()  # смена кадров что бы не было дерганное


# Процедура инициализации
def init():
    global model
    global pol_and_potolok
    global pol_and_potolok_1
    global dveri
    global stena_cool
    global plazma_t
    global stena

    glClearColor(0.1, 0.1, 0.1, 1.0)
    glMatrixMode(GL_PROJECTION)

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)  # Включаем освещение
    glEnable(GL_LIGHT2)
    # glEnable(GL_AUTO_NORMAL)
    glAlphaFunc(GL_GREATER, 0.5)
    glEnable(GL_ALPHA_TEST)

    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)

    pol_and_potolok = load_texture("pol.jpg")
    pol_and_potolok_1 = load_texture("not_pol.jpg")
    dveri = load_texture("dveri.jpg")
    stena_cool = load_texture("stena_cool.jpg")
    plazma_t = load_texture("stena_s_plazmoy.jpg")
    stena = load_texture("stena.jpg")


if __name__ == '__main__':
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 360)
    glutInitWindowPosition(1000, 200)

    glutInit(sys.argv)

    glutCreateWindow(b'Zachtite pozhaluysta')
    glutDisplayFunc(draw)
    glutSpecialFunc(Keys_upravlenie)
    init()
    glutMainLoop()
