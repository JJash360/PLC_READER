from logic.function import *
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

"""PRUEBA"""
IP_ADDRESS_1="192.168.1.13"

"""PLC REAL"""
#IP_ADDRESS_1="192.168.0.3"

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("app/gui/HMI_demo.ui", self)
        """PRUEBA"""
        """Imágenes de auto y manual"""
        self.pixmap_dict = {
            self.label_13: (QPixmap("gui/img/select_1.png"), QPixmap("gui/img/select_2.png")),
        }
        #Configurar imágenes y botones iniciales
        self.label_13.setPixmap(self.pixmap_dict[self.label_13][0])

        """Imágenes de bomba"""
        self.pixmap_bomb = {
            self.label_12: (QPixmap("gui/img/motor_left.png"), QPixmap("gui/img/motor_fault.png"), QPixmap("gui/img/motor_off.png"), QPixmap("gui/img/motor_right.png"))
        }
        #Configurar imágenes y botones iniciales
        self.label_12.setPixmap(self.pixmap_bomb[self.label_12][3])

        """Mínimos y máximos de sliders y barras"""
        min_man_1=leer_datablock(IP_ADDRESS_1,4,12,"REAL")
        max_man_1=leer_datablock(IP_ADDRESS_1,4,8,"REAL")
        self.slider_manual_1.setMinimum(round(min_man_1))
        self.slider_manual_1.setMaximum(round(max_man_1))
        self.barra_manual_1.setMinimum(round(min_man_1))
        self.barra_manual_1.setMaximum(round(max_man_1))

        min_limt_1=leer_datablock(IP_ADDRESS_1,4,4,"REAL")
        max_limit_1=leer_datablock(IP_ADDRESS_1,4,0,"REAL")
        self.slider_limite_1.setMinimum(round(min_limt_1))
        self.slider_limite_1.setMaximum(round(max_limit_1))
        self.barra_limite_1.setMinimum(round(min_limt_1))
        self.barra_limite_1.setMaximum(round(max_limit_1))

        """PLC REAL"""
        # """Imágenes de auto y manual"""
        # self.pixmap_dict = {
        #     self.label_13: (QPixmap("manual1.jpg"), QPixmap("auto1.jpg")),
        #     self.label_43: (QPixmap("manual2.jpg"), QPixmap("auto2.jpg"))
        # }
        # #Configurar imágenes iniciales
        # self.label_13.setPixmap(self.pixmap_dict[self.label_13][0])
        # self.label_43.setPixmap(self.pixmap_dict[self.label_43][0])

        
        # """Imágenes de bomba"""
        # self.pixmap_bomb = {
        #     self.label_12: (QPixmap("bombblue1.jpg"), QPixmap("bombred1.jpg"), QPixmap("bombwhite1.jpg"), QPixmap("bombyellow1.jpg")),
        #     self.label_24: (QPixmap("bombblue2.jpg"), QPixmap("bombred2.jpg"), QPixmap("bombwhite2.jpg"), QPixmap("bombyellow2.jpg"))
        # }
        # #Configurar imágenes y botones iniciales
        # self.label_12.setPixmap(self.pixmap_bomb[self.label_12][3])
        # self.label_24.setPixmap(self.pixmap_bomb[self.label_24][3])

        # """Mínimos y máximos de sliders y barras"""
        # min_man_1=leer_datablock(IP_ADDRESS_1,4,12,"REAL")
        # max_man_1=leer_datablock(IP_ADDRESS_1,4,8,"REAL")
        # self.slider_manual_1.setMinimum(round(min_man_1))
        # self.slider_manual_1.setMaximum(round(max_man_1))
        # self.barra_manual_1.setMinimum(round(min_man_1))
        # self.barra_manual_1.setMaximum(round(max_man_1))

        # min_limt_1=leer_datablock(IP_ADDRESS_1,4,4,"REAL")
        # max_limit_1=leer_datablock(IP_ADDRESS_1,4,0,"REAL")
        # self.slider_limite_1.setMinimum(round(min_limt_1))
        # self.slider_limite_1.setMaximum(round(max_limit_1))
        # self.barra_limite_1.setMinimum(round(min_limt_1))
        # self.barra_limite_1.setMaximum(round(max_limit_1))
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(2000)  # Se ejecuta cada 500 ms (0.5 segundos)
        self.actualizar_datos()  # Primera actualización inmediata
    
    def actualizar_datos(self):
        try:
            """PRUEBA"""
            """Lectura de memorias enteras o reales"""
            amp=leer_datablock(IP_ADDRESS_1,4,16,"REAL")
            hz=leer_datablock(IP_ADDRESS_1,4,24,"INT") 
            slider_man=leer_datablock(IP_ADDRESS_1,4,20,"REAL")
            slider_limit=leer_datablock(IP_ADDRESS_1,4,16,"REAL")
            self.amp_1.setText(str(f"{amp:.2f}"))
            self.frec_1.setText(str(hz))
            self.slider_manual_1.setValue(round(slider_man))
            self.barra_manual_1.setValue(round(slider_man))
            self.value_manual_1.setText(f"{slider_man:.2f}")
            self.slider_limite_1.setValue(round(slider_limit))
            self.barra_limite_1.setValue(round(slider_limit))
            self.value_limite_1.setText(f"{slider_limit:.2f}")

            """Lectura de memorias booleanas"""
            arranque_1=leer_memory(IP_ADDRESS_1,50,2,"BOOL")
            self.cambiar_color_run(arranque_1,self.run_1)
            parada_1=leer_memory(IP_ADDRESS_1,70,7,"BOOL")
            self.cambiar_color_falla(parada_1,self.falla_1)
            
            """Botones"""
            self.marcha_button_1.clicked.connect(lambda: self.activar_bit(50,0))
            self.paro_button_1.clicked.connect(lambda: self.activar_bit(50,1))

            """Imágenes de auto y manual"""
            #Configurar estado inicial
            self.estado_1={self.label_13: False} #False: manual, True: auto
            #Llamar funciones
            self.label_13.mousePressEvent = lambda event: self.alternar_auto_manual(self.label_13,self.ctrl_auto_1,self.ctrl_manual_1,50,5,self.estado_1)

            """Imágenes de bomba"""
            #Configurar estado inicial
            self.giro_izq_1.setCheckable(True)
            self.giro_der_1.setCheckable(True)
            #Llamar funciones
            self.giro_izq_1.clicked.connect(lambda:                         self.cambiar_bomba(self.label_12,50,2,70,7,self.giro_izq_1,self.giro_der_1,3,4))
            self.giro_der_1.clicked.connect(lambda:     self.cambiar_bomba(self.label_12,50,2,70,7,self.giro_izq_1,self.giro_der_1,3,4))

            """PLC REAL"""
            """Lectura de memorias enteras o reales"""
            # Amperio_1=leer_memory(IP_ADDRESS_1,44,0,"REAL")
            # self.amp_1.setText(str(Amperio_1))
            # Amperio_2=leer_memory(IP_ADDRESS_1,76,0,"REAL")
            # self.amp_2.setText(str(Amperio_2))
            # Hz_1=leer_memory(IP_ADDRESS_1,64,0,"REAL")
            # self.frec_1.setText(str(Hz_1))
            # Hz_2=leer_memory(IP_ADDRESS_1,84,0,"REAL")
            # self.frec_2.setText(str(Hz_2))
            # Presion_1=leer_memory(IP_ADDRESS_1,100,0,"REAL")
            # self.pres_1.setText(str(Presion_1))
            # Presion_2=leer_memory(IP_ADDRESS_1,104,0,"REAL")
            # self.pres_2.setText(str(Presion_2))
            # adj_manual_1=leer_datablock(IP_ADDRESS_1,39,12,"INT")
            # self.slider_manual_1.setValue(int(round(adj_manual_1)))
            # self.barra_manual_1.setValue(int(round(adj_manual_1)))
            # self.value_manual_1.setText(f"{adj_manual_1:.2f}")
            # adj_manual_2=leer_datablock(IP_ADDRESS_1,39,14,"INT")
            # self.slider_manual_2.setValue(int(round(adj_manual_2)))
            # self.barra_manual_2.setValue(int(round(adj_manual_2)))
            # self.value_manual_2.setText(f"{adj_manual_2:.2f}")
            # porcentaje_1=leer_memory(IP_ADDRESS_1,336,0,"REAL")
            # self.barra_porcentaje_1.setValue(int(round(porcentaje_1)))
            # self.value_porcentaje_1.setText(f"{porcentaje_1:.2f}")
            # self.vel_1.setText(f"{porcentaje_1:.2f}")
            # porcentaje_2=leer_memory(IP_ADDRESS_1,360,0,"REAL")
            # self.barra_porcentaje_2.setValue(int(round(porcentaje_2)))
            # self.value_porcentaje_2.setText(f"{porcentaje_2:.2f}")
            # self.vel_2.setText(f"{porcentaje_2:.2f}")
            # limite_1=leer_datablock(IP_ADDRESS_1,39,8,"INT")
            # self.slider_limite_1.setValue(int(round(limite_1)))
            # self.barra_limite_1.setValue(int(round(limite_1)))
            # self.value_limite_1.setText(f"{limite_1:.2f}")
            # limite_2=leer_datablock(IP_ADDRESS_1,39,10,"INT")
            # self.slider_limite_2.setValue(int(round(limite_2)))
            # self.barra_limite_2.setValue(int(round(limite_2)))
            # self.value_limite_2.setText(f"{limite_2:.2f}")
            # premarcha_1=leer_datablock(IP_ADDRESS_1,39,0,"REAL")
            # self.premarcha_1.setText(str(premarcha_1))
            # premarcha_2=leer_datablock(IP_ADDRESS_1,39,4,"REAL")
            # self.premarcha_2.setText(str(premarcha_2))

            # """Lectura de memorias booleanas"""
            # arranque_1=leer_memory(IP_ADDRESS_1,50,2,"BOOL")
            # self.cambiar_color_run(arranque_1,self.run_1)
            # arranque_2=leer_memory(IP_ADDRESS_1,51,2,"BOOL")
            # self.cambiar_color_run(arranque_2,self.run_2)
            # parada_1=leer_memory(IP_ADDRESS_1,70,7,"BOOL")
            # self.cambiar_color_falla(parada_1,self.falla_1)
            # parada_2=leer_memory(IP_ADDRESS_1,71,0,"BOOL")
            # self.cambiar_color_falla(parada_2,self.falla_2)

            # """Botones"""
            # self.marcha_button_1.clicked.connect(lambda: self.activar_bit(50,0))
            # self.marcha_button_2.clicked.connect(lambda: self.activar_bit(51,0))
            # self.paro_button_1.clicked.connect(lambda: self.activar_bit(50,1))
            # self.paro_button_2.clicked.connect(lambda: self.activar_bit(51,1))
            # self.reset_button_1.clicked.connect(lambda: self.activar_bit(70,6))
            # self.reset_button_2.clicked.connect(lambda: self.activar_bit(50,7))

            # """Imágenes de auto y manual"""
            #Configurar estado inicial
            # self.estado_1={self.label_13: False} #False: manual, True: auto
            # self.estado_2={self.label_43: False} #False: manual, True: auto
            # #Llamar funciones
            # self.label_13.mousePressEvent = lambda event: self.alternar_auto_manual(self.label_13,self.ctrl_auto_1,self.ctrl_manual_1,50,5,self.estado_1)
            # self.label_43.mousePressEvent = lambda event: self.alternar_auto_manual(self.label_43,self.ctrl_auto_2,self.ctrl_manual_2,50,6,self.estado_2)

            # """Imágenes de bomba"""
            #Configurar estado inicial
            # self.giro_izq_1.setCheckable(True)
            # self.giro_izq_2.setCheckable(False)
            # self.giro_der_1.setCheckable(True)
            # self.giro_der_2.setCheckable(False)
            # #Llamar funciones
            # self.giro_izq_1.clicked.connect(lambda: self.cambiar_bomba(self.label_12,50,2,70,7,self.giro_izq_1,self.giro_der_1,3,4))
            # self.giro_der_1.clicked.connect(lambda: self.cambiar_bomba(self.label_12,50,2,70,7,self.giro_izq_1,self.giro_der_1,3,4))
            # self.giro_izq_2.clicked.connect(lambda: self.cambiar_bomba(self.label_24,51,2,71,0,self.giro_izq_2,self.giro_der_2,3,4))
            # self.giro_der_2.clicked.connect(lambda: self.cambiar_bomba(self.label_24,51,2,71,0,self.giro_izq_2,self.giro_der_2,3,4))

            print("Actualización correcta")
        except Exception as e:
            print(f"Error al leer los datos: {e}")
    
    def activar_bit(self,number_memory,offset):
        try:
            escribir_memory(IP_ADDRESS_1,number_memory,offset,"BOOL",True)
            escribir_memory(IP_ADDRESS_1,number_memory,offset,"BOOL",False)
            print(f"Memoria M{number_memory}.{offset} funcionando")
        except Exception as e:
            print(f"Error al funcionar la memoria M{number_memory}.{offset}: {e}")

    def cambiar_color_run(self,run,etiqueta):
        if run==True:
            etiqueta.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        else:
            etiqueta.setStyleSheet("background-color: gray; color: black; font-weight: bold;")
    
    def cambiar_color_falla(self,falla,etiqueta):
        if falla==True:
            etiqueta.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        else:
            etiqueta.setStyleSheet("background-color: gray; color: black; font-weight: bold;")

    def alternar_auto_manual(self,etiqueta,auto,manual,number_memory,offset,number_estado):
        try:
            if etiqueta not in self.pixmap_dict:
                print(f"Error: {etiqueta.objectName()} no está en el diccionario de imágenes.")
                return

            img_original, img_alternativa = self.pixmap_dict[etiqueta]

            # Obtener el estado actual
            estado = number_estado[etiqueta]

            # Alternar estado
            if not estado:  # Si está en manual, cambiar a auto
                etiqueta.setPixmap(img_alternativa)
                print(f"Imagen alternativa mostrada en {etiqueta.objectName()} (Auto)")
                auto.setChecked(True)
                manual.setChecked(False)
                escribir_memory(IP_ADDRESS_1,number_memory,offset,"BOOL",True)
                print("Motor en modo automático")
            else:  # Si está en auto, cambiar a manual
                etiqueta.setPixmap(img_original)
                print(f"Imagen original mostrada en {etiqueta.objectName()} (Manual)")
                auto.setChecked(False)
                manual.setChecked(True)
                escribir_memory(IP_ADDRESS_1,number_memory,offset,"BOOL",False)
                print("Motor en modo manual")

            #Guardar nuevo estado
            number_estado[etiqueta] = not estado

            #Forzar la actualización del QLabel para reflejar el cambio
            etiqueta.repaint()

        except Exception as e:
            print(f"Error al cambiar de imagen en {etiqueta.objectName()}: {e}")

    def cambiar_bomba(self, etiqueta, number_memory_run, bit_run, number_memory_falla, bit_falla, izq, der, offset_izq, offset_der):
        try:
            if etiqueta not in self.pixmap_bomb:
                print(f"Error: {etiqueta.objectName()} no está en el diccionario de imágenes.")
                return

            img_blue, img_red, img_white, img_yellow = self.pixmap_bomb[etiqueta]

            # Si no hay imagen inicial, establecer la blanca
            if etiqueta.pixmap() is None:
                etiqueta.setPixmap(img_white)
                print(f"Imagen original mostrada en {etiqueta.objectName()}")
                return

            # Verificar estados actuales
            estado_run = leer_memory(IP_ADDRESS_1, number_memory_run, bit_run, "BOOL")
            estado_stop = leer_memory(IP_ADDRESS_1, number_memory_falla, bit_falla, "BOOL")

            # Lógica para cambiar imágenes
            if estado_run:
                if izq.isChecked():
                    der.setChecked(False)  # Asegurar que solo un botón esté activo
                    etiqueta.setPixmap(img_blue)
                    escribir_memory(IP_ADDRESS_1, number_memory_run, offset_izq, "BOOL", True)
                    escribir_memory(IP_ADDRESS_1, number_memory_run, offset_der, "BOOL", False)
                    print(f"Imagen cambiada a Azul en {etiqueta.objectName()} (Giro Izquierda)")
                elif der.isChecked():
                    izq.setChecked(False)  # Asegurar que solo un botón esté activo
                    etiqueta.setPixmap(img_yellow)
                    escribir_memory(IP_ADDRESS_1, number_memory_run, offset_izq, "BOOL", False)
                    escribir_memory(IP_ADDRESS_1, number_memory_run, offset_der, "BOOL", True)
                    print(f"Imagen cambiada a Amarillo en {etiqueta.objectName()} (Giro Derecha)")
            elif estado_stop:
                etiqueta.setPixmap(img_red)
                print(f"Imagen cambiada a Rojo en {etiqueta.objectName()} (Paro)")
            else:
                etiqueta.setPixmap(img_white)
                print(f"Imagen cambiada a Blanco en {etiqueta.objectName()} (Reposo)")

            # 🔹 Forzar la actualización del QLabel para reflejar el cambio visualmente
            etiqueta.repaint()

        except Exception as e:
            print(f"Error al cambiar de imagen de bomba en {etiqueta.objectName()}: {e}")

if __name__=='__main__':
    app=QApplication(sys.argv)
    GUI=MainWindow()
    GUI.show()
    sys.exit(app.exec_())

#Etiquetas
falla_1=leer_memory(IP_ADDRESS_1,70,7,"BOOL")
falla_2=leer_memory(IP_ADDRESS_1,71,0,"BOOL")
#premarcha_1=leer_datablock(IP_ADDRESS_1,39,0,"REAL")
#premarcha_2=leer_datablock(IP_ADDRESS_1,39,4,"REAL")
#run_1=leer_memory(IP_ADDRESS_1,50,2,"BOOL")
#run_2=leer_memory(IP_ADDRESS_1,51,2,"BOOL")
giro_izq_1=leer_memory(IP_ADDRESS_1,50,3,"BOOL")
giro_izq_2=leer_memory(IP_ADDRESS_1,51,3,"BOOL")
giro_der_1=leer_memory(IP_ADDRESS_1,50,4,"BOOL")
giro_der_2=leer_memory(IP_ADDRESS_1,51,4,"BOOL")
ctrl_manual_1=leer_memory(IP_ADDRESS_1,50,5,"BOOL")
ctrl_manual_2=not leer_memory(IP_ADDRESS_1,50,6,"BOOL")
ctrl_auto_1=leer_memory(IP_ADDRESS_1,50,5,"BOOL")
ctrl_auto_2=not leer_memory(IP_ADDRESS_1,50,6,"BOOL")
vel_1=leer_memory(IP_ADDRESS_1,336,0,"REAL")
vel_2=leer_memory(IP_ADDRESS_1,360,0,"REAL")
amp_1=leer_memory(IP_ADDRESS_1,44,0,"REAL")
amp_2=leer_memory(IP_ADDRESS_1,76,0,"REAL")
frec_1=leer_memory(IP_ADDRESS_1,64,0,"REAL")
frec_2=leer_memory(IP_ADDRESS_1,84,0,"REAL")
pres_1=leer_memory(IP_ADDRESS_1,100,0,"REAL")
pres_2=leer_memory(IP_ADDRESS_1,104,0,"REAL")
slider_manual_1=leer_datablock(IP_ADDRESS_1,39,12,"INT")
slider_manual_2=leer_datablock(IP_ADDRESS_1,39,14,"INT")
barra_manual_1=leer_datablock(IP_ADDRESS_1,39,12,"INT")
barra_manual_2=leer_datablock(IP_ADDRESS_1,39,14,"INT")
barra_porcentaje_1=leer_memory(IP_ADDRESS_1,336,0,"REAL")
barra_porcentaje_2=leer_memory(IP_ADDRESS_1,360,0,"REAL")
slider_limite_1=leer_datablock(IP_ADDRESS_1,39,8,"INT")
slider_limite_2=leer_datablock(IP_ADDRESS_1,39,10,"INT")
barra_limite_1=leer_datablock(IP_ADDRESS_1,39,8,"INT")
barra_limite_2=leer_datablock(IP_ADDRESS_1,39,10,"INT")
value_manual_1=leer_datablock(IP_ADDRESS_1,39,12,"INT")
value_manual_2=leer_datablock(IP_ADDRESS_1,39,14,"INT")
value_porcentaje_1=leer_memory(IP_ADDRESS_1,336,0,"REAL")
value_porcentaje_2=leer_memory(IP_ADDRESS_1,360,0,"REAL")
value_limite_1=leer_datablock(IP_ADDRESS_1,39,8,"INT")
value_limite_2=leer_datablock(IP_ADDRESS_1,39,10,"INT")
marcha_button_1=leer_memory(IP_ADDRESS_1,50,0,"BOOL")
marcha_button_2=leer_memory(IP_ADDRESS_1,51,0,"BOOL")
paro_button_1=leer_memory(IP_ADDRESS_1,50,1,"BOOL")
paro_button_2=leer_memory(IP_ADDRESS_1,51,1,"BOOL")
reset_button_1=leer_memory(IP_ADDRESS_1,70,6,"BOOL")
reset_button_2=leer_memory(IP_ADDRESS_1,50,7,"BOOL")
