# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 07:37:39 2020

@author: rubel
"""
from tkinter import *
from tkinter import messagebox
import importlib

employee_class = importlib.import_module("classes.employee_class", ".")
employee_class = importlib.import_module("classes.employee_class", ".")
comment_class = importlib.import_module("classes.comment_class", ".")
db_comment = importlib.import_module("db_access_offline.db_comment", ".")
db_employee = importlib.import_module("db_access_offline.db_employee", ".")

LARGE_FONT = ("Verdana", 12)
STRONG_FONT = ("verdana 12 bold")
BRANCO = "#fff"
HOME = 0
LOGIN = 1
PONTUACAO = 2
ADICIONAR = 3
FUNCIONARIOS = 4
FUNCIONARIO = 5
COMENTARIOS = 6

'''

banco de dados usuario:iduser|name|email|password|admin|score|path
banco de dados de comentarios:idcom|iduser|data|comment|score|area

'''

adm = {"a": ""}
comentarios = [["a", "b"]]


class ScrollFrame(Frame):  # https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01 by mp035
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        self.canvas = Canvas(self, borderwidth=0, background=BRANCO)  # place canvas on self
        self.viewPort = Frame(self.canvas,
                              background=BRANCO)  # place a frame on the canvas, this frame will hold the child widgets
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)  # place a scrollbar on self
        self.vsb2 = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas
        self.canvas.configure(xscrollcommand=self.vsb2.set)

        self.vsb.pack(side="right", fill="y")  # pack scrollbar to right of self
        self.vsb2.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)  # pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",
                                                       # add view port frame to canvas
                                                       tags="self.viewPort")

        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(
            None)  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.


class Window(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self, bg=BRANCO)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        paginas = [Home_page, Login_page, Pontuacao_page, Adicionar_funcionario_page,
                   Editar_funcionario_tabela_page, Editar_funcionario_individual_page, Comentarios_page]

        self.pagina = []
        for F in range(len(paginas)):
            frame = ScrollFrame(container)
            a = paginas[F](frame.viewPort, self)
            a.grid(row=0, column=0)
            self.pagina.append(a)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LOGIN)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def atualizar_usuario(self, ID):
        self.pagina[FUNCIONARIO].atualizar(ID)
        self.show_frame(FUNCIONARIO)

    def mostrar_comentario(self, ID):
        self.pagina[COMENTARIOS].editar_lista()
        self.show_frame((COMENTARIOS))
        print("mostrando comentario " + str(ID))

    def tabela_funcionarios(self):
        self.pagina[FUNCIONARIOS].editar_lista()
        self.show_frame(FUNCIONARIOS)

    def tabela_pontos(self):
        self.pagina[PONTUACAO].editar_lista()
        self.show_frame(PONTUACAO)


class Home_page(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent, bg="#fff")
        label = Label(self, text="Home Page", font=LARGE_FONT, bg=BRANCO)
        label.grid(row=0, column=0, columnspan=3, )
        # self.grid_columnconfigure(0, weight=1)

        button1 = Button(self, text="Ver pontuação",
                         command=lambda: self.controller.tabela_pontos(), width=21)
        button1.grid(row=5, column=0, sticky="e")
        # self.grid_columnconfigure(1, weight=1)

        space = Label(self, bg=BRANCO)
        space.grid(row=2, rowspan=3)

        button2 = Button(self, text="Adicionar funcionário",
                         command=lambda: self.controller.show_frame(ADICIONAR), width=21)
        button2.grid(row=5, column=1, sticky="w")

        button3 = Button(self, text="Editar funcionários",
                         command=lambda: self.controller.tabela_funcionarios(), width=21)
        button3.grid(row=6, column=0, sticky="e")

        button4 = Button(self, text="Comentários",
                         command=lambda: self.controller.show_frame(COMENTARIOS), width=21)
        button4.grid(row=6, column=1, sticky="w")

        button5 = Button(self, text="sair",
                         command=lambda: self.controller.show_frame(LOGIN), width=4)
        button5.grid(row=7, column=2, sticky="w")


class Login_page(Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent, bg=BRANCO)
        self.label = Label(self, text="Log in", font=LARGE_FONT, bg=BRANCO)
        self.nomel = Label(self, text="Nome de usuário:", font="Verdana 10", bg=BRANCO)
        self.senhal = Label(self, text="Senha:", font="Verdana 10", bg=BRANCO)
        self.nome = Entry(self)
        self.senha = Entry(self, show="*")
        self.label.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.nomel.grid(row=1, column=0, sticky="e")
        self.senhal.grid(row=2, column=0, sticky="e")
        self.nome.grid(row=1, column=1, sticky="w")
        self.senha.grid(row=2, column=1, sticky="w")

        self.grid_columnconfigure(3, weight=1)

        self.button = Button(self, text="Log in",
                             command=self.testar)
        self.button.grid(row=3, column=2)

    def testar(self, *args):
        try:
            ID = self.nome.get()
            password = self.senha.get()
            if adm[ID] != password:
                raise ()
            self.nome.delete(0, 'end')
            self.senha.delete(0, 'end')
            self.controller.show_frame(HOME)
        except:
            messagebox.showinfo("erro de login", "usuário ou senha inválida")
            self.controller.show_frame(LOGIN)
            self.nome.delete(0, 'end')
            self.senha.delete(0, 'end')


class Pontuacao_page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BRANCO)
        self.controller = controller
        self.label = Label(self, text="Pontuação", font=LARGE_FONT, bg=BRANCO)
        self.label.grid(row=0, column=0)

        self.button1 = Button(self, text="Voltar",
                              command=self.sair)
        self.button1.grid(row=10, column=10)

        self.buscal = Label(self, text="Procurar:", font="Verdana 8", bg=BRANCO)
        self.buscal.grid(row=4, column=0)
        self.busca = Entry(self)
        self.busca.grid(row=4, column=1)
        self.button2 = Button(self, text="procurar", font="verdana 8",
                              command=self.buscar)
        self.button2.grid(row=4, column=3)

        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=3)

    def sair(self, *args):
        self.busca.delete(0, 'end')
        self.controller.show_frame(HOME)

    def buscar(self, *args):
        print("busca por nome")

    def editar_lista(self, *args):
        lista = db_employee.getAllEmployees()

        self.scrollframe.destroy()
        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=3)
        Label(self.scrollframe.viewPort, text="Nome", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=0)
        Label(self.scrollframe.viewPort, text="Email", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=1)
        Label(self.scrollframe.viewPort, text="Pontuação", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=2)

        for row in range(len(lista)):
            Label(self.scrollframe.viewPort, text=lista[row].getEmployeeName(), bg=BRANCO).grid(row=row + 1, column=0)
            Label(self.scrollframe.viewPort, text=lista[row].getEmployeeEmail(), bg=BRANCO).grid(row=row + 1, column=1)
            Label(self.scrollframe.viewPort, text=str(lista[row].getScore()), bg=BRANCO).grid(row=row + 1, column=2)


class Adicionar_funcionario_page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BRANCO)
        self.controller = controller
        self.label = Label(self, text="Adicionar funcionário", font=LARGE_FONT, bg=BRANCO)
        self.label.grid(row=0, column=0)

        self.nomel = Label(self, text='Nome: ', font=LARGE_FONT, bg=BRANCO)
        self.nome = Entry(self)
        self.nomel.grid(row=1, column=0)
        self.nome.grid(row=1, column=1)

        self.emaill = Label(self, text='Email: ', font=LARGE_FONT, bg=BRANCO)
        self.email = Entry(self)
        self.emaill.grid(row=2, column=0)
        self.email.grid(row=2, column=1)

        self.senhal = Label(self, text='Senha: ', font=LARGE_FONT, bg=BRANCO)
        self.senha = Entry(self, show='*')
        self.senhal.grid(row=3, column=0)
        self.senha.grid(row=3, column=1)

        self.adm = Checkbutton(self, text='Administrador', bg=BRANCO)
        self.adm.grid(row=4, column=0)

        self.button1 = Button(self, text="Voltar",
                              command=self.voltar)
        self.button1.grid(row=5, column=0)

        self.button2 = Button(self, text="Confirmar",
                              command=self.confirmar)
        self.button2.grid(row=5, column=1)

    def voltar(self, *args):
        self.nome.delete(0, 'end')
        self.email.delete(0, 'end')
        self.senha.delete(0, 'end')
        self.adm.deselect()
        self.controller.show_frame(HOME)

    def confirmar(self, *args):
        print("adicionar senha")
        if (db_employee.emailAvailable(self.email.get())):
            if (self.email.get() == "" or self.nome.get == "" or self.senha.get() == ""):
                messagebox.showinfo("Erro", "Informações faltando")
                self.senha.delete(0, 'end')
            else:
                db_employee.addEmployee(self.nome.get(), self.email.get(), "", "", "","")
                messagebox.showinfo("Ação completada", "Usuário adicionado com sucesso")
                self.nome.delete(0, 'end')
                self.email.delete(0, 'end')
                self.senha.delete(0, 'end')
                self.adm.deselect()
        else:
            messagebox.showinfo("Erro", "Email já em uso")
            self.email.delete(0, 'end')
            self.senha.delete(0, 'end')


class Editar_funcionario_tabela_page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BRANCO)
        self.controller = controller
        self.label = Label(self, text="Funcionários", font=LARGE_FONT, bg=BRANCO)
        self.label.grid(row=0, column=0, columnspan=5)
        self.grid_columnconfigure(0, weight=1)

        self.button = Button(self, text="Voltar",
                             command=lambda: self.controller.show_frame(HOME))
        self.button.grid(row=4, column=5)

        self.button2 = Button(self, text='procurar',
                              command=self.procurar)
        self.button2.grid(row=4, column=3)

        self.procural = Label(self, text="Procurar", bg=BRANCO).grid(row=4, column=0)

        self.procura = Entry(self)
        self.procura.grid(row=4, column=1)

        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=5)

    def editar_lista(self, *args):
        lista = db_employee.getAllEmployees()

        self.scrollframe.destroy()
        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=5)
        Label(self.scrollframe.viewPort, text="Nome", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=0)
        Label(self.scrollframe.viewPort, text="Email", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=1)

        for row in range(len(lista)):
            Label(self.scrollframe.viewPort, text=lista[row].getEmployeeName()).grid(row=row + 1, column=0)
            Label(self.scrollframe.viewPort, text=lista[row].getEmployeeEmail()).grid(row=row + 1, column=1)
            a = row
            Button(self.scrollframe.viewPort, text="editar", command=lambda x=a:
            self.controller.atualizar_usuario(lista[x].getEmployeeID())).grid(row=row + 1, column=2)

    def procurar(self, *args):
        print('procurar')


class Editar_funcionario_individual_page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BRANCO)
        self.controller = controller
        self.ID = None
        self.label1 = Label(self, text="Editar usuáro", font=LARGE_FONT, bg=BRANCO)
        self.label1.grid(row=0, column=0)

        self.label2 = Label(self, text="Nome:", font="verdano 10", bg=BRANCO)
        self.label2.grid(row=1, column=0)

        self.email = Entry(self)
        self.email.grid(row=2, column=1)

        self.button1 = Button(self, text="Apagar",
                              command=self.apagar)
        self.button1.grid(row=10, column=1)

        self.button1 = Button(self, text="Confirmar",
                              command=self.confirmar)
        self.button1.grid(row=10, column=2)

        self.button1 = Button(self, text="Voltar",
                              command=self.voltar)
        self.button1.grid(row=10, column=3)

    def atualizar(self, ID):
        self.ID = ID
        self.label2.configure(text="Nome: " + db_employee.getEmployeePerID(ID).getEmployeeName())

    def apagar(self, *args):
        db_employee.deleteEmployee(self.ID)
        messagebox.showinfo("Ação completada", "Usuário apagado com sucesso")
        self.email.delete(0, 'end')
        self.controller.tabela_funcionarios()

    def confirmar(self, *args):
        email = self.email.get()
        if (db_employee.emailAvailable(email)):
            db_employee.setEmployeeEmail(self.ID, email)
            messagebox.showinfo("Ação completada", "Usuário atualizado com sucesso")
            self.controller.tabela_funcionarios()
            self.email.delete(0, 'end')
        else:
            messagebox.showinfo("Erro", "Email já em uso")
            self.email.delete(0, 'end')

    def voltar(self, *args):
        self.email.delete(0, 'end')
        self.controller.tabela_funcionarios()


class Comentarios_page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BRANCO)
        self.controller = controller
        self.label = Label(self, text="Comentários", font=LARGE_FONT, bg=BRANCO)
        self.label.grid(row=0, column=0, columnspan=5)
        self.grid_columnconfigure(0, weight=1)

        self.button1 = Button(self, text="Voltar",
                              command=self.voltar)
        self.button1.grid(row=4, column=5)

        self.button2 = Button(self, text='procurar',
                              command=self.procurar)
        self.button2.grid(row=4, column=3)

        self.procural = Label(self, text="Procurar", bg=BRANCO).grid(row=4, column=0)

        self.procura = Entry(self)
        self.procura.grid(row=4, column=1)

        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=5)
        self.editar_lista()

    def editar_lista(self, *args):
        dbb_comment = importlib.import_module("db_access_offline.db_comment", ".")
        lista = dbb_comment.getAllComments()

        self.scrollframe.destroy()
        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=5)
        Label(self.scrollframe.viewPort, text="Data", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=0)
        Label(self.scrollframe.viewPort, text="Área", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=1)

        for row in range(len(lista)):
            Label(self.scrollframe.viewPort, text=lista[row].getDate(), bg=BRANCO).grid(row=row + 1, column=0)
            Label(self.scrollframe.viewPort, text=lista[row].getArea(), bg=BRANCO).grid(row=row + 1, column=1)
            a = row
            Button(self.scrollframe.viewPort, text="vizualizar", command=lambda x=a:
            self.controller.mostrar_comentario(x)).grid(row=row + 1, column=2, sticky="e")

    def voltar(self, *args):
        self.procura.delete(0, 'end')
        self.controller.show_frame(HOME)

    def procurar(self, *args):
        print('procurar')


def main():
    app = Window()
    app.mainloop()


main()