from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
from interprete import interpreteº
from errores_personalizados import ExcessOrFaltaDeParametros, ImposibleProcesar


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()
        self.resulta2 = open("resultados.txt", "w")
        self.contador = 1
        self.ans = []

    def process_consult(self, querry_array):  # Use un for tal como salia en el ejemplo del punto 8.4 del enunciado
        # answer=[self.add_answer(str(interprete(i))+"\n") for i in querry_array]
        for consulta in querry_array:
            try:
                cons = interprete(consulta)
                if str(cons) == str(consulta):
                    raise ImposibleProcesar("Comando no existe")
                # [self.add_answer(str(ans) +"\n") for ans in answer]
                self.add_answer(str(cons) + "\n")
                self.ans.append(str(cons))
            except ZeroDivisionError:
                self.add_answer("Error:" + str(consulta[0:]) + "\n division por cero \n")
                self.ans.append("Error:" + str(consulta[0:]) + "\n division por cero \n")
            except ExcessOrFaltaDeParametros as err:
                self.add_answer("Error:" + str(consulta[0:1]) + "\n {}".format(err) + "\n")
                self.ans.append("Error:" + str(consulta[0:1]) + "\n {}".format(err) + "\n")
            except TypeError as err:
                self.add_answer("Error:" + str(consulta[0:1]) + "\n {}".format(err) + "\n")
                self.ans.append("Error:" + str(consulta[0:1]) + "\n {}".format(err) + "\n")
            except ValueError as err:
                self.add_answer("Error:" + str(consulta[0:1]) + "\n {}".format(err) + "\n")
                self.ans.append("Error:" + str(consulta[0:1]) + "\n {}".format(err))
            except ImposibleProcesar as err:
                self.add_answer("Error:" + str(consulta[0:1]) + "\n {}".format(err) + "\n")
                self.ans.append("Error:" + str(consulta[0:1]) + "\n {}".format(err) + "\n")

    def save_file(self, querry_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        for respuesta in self.ans:
            print("-------- CONSULTA {} ----------".format(self.contador), file=self.resulta2)
            print(respuesta, file=self.resulta2)
            self.contador += 1
        self.ans = []
        self.resulta2.close()
        self.resulta2 = open("resultados.txt", "a")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
