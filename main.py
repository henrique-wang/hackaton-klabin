# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 07:37:39 2020

@author: rubel
"""
from tkinter import *
from tkinter import messagebox
import importlib

employee_class = importlib.import_module("classes.employee_class", ".")
comment_class = importlib.import_module("classes.comment_class", ".")
#db_comment = importlib.import_module("db_access_offline.db_comment", ".")
#db_employee = importlib.import_module("db_access_offline.db_employee", ".")
picture_taker = importlib.import_module("Codigo_Guigs.1_TakePictures",".")
trainer = importlib.import_module("Codigo_Guigs.2_TrainModel")
recognizer = importlib.import_module("Codigo_Guigs.3_Recognizer")
sql = importlib.import_module("db_access_online.SQL2object_Interaction")

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

try:
    db = sql.mysql.connect(host='localhost',
                       user='root',
                       password='pythaon',
                       database='hackaluna')

    cursor = db.cursor()
    online=True
except:
    print("Not connected to server")
    online=False



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
        #self.pagina[COMENTARIOS].editar_lista()
        #self.show_frame((COMENTARIOS))
        comentario=sql.fetch_comment_by_id(ID)
        windown_comentario=Toplevel(self)
        windown_comentario.title(comentario.area)
        Label(windown_comentario, text=comentario.getMessage()).grid(row=0, column=0)
        Button(windown_comentario, text="exit", command=windown_comentario.destroy).grid(row=1, column=1)

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

        button6 = Button(self, text="Treinar",
                         command= self.train)
        button6.grid(row=7, column=0, sticky="e")

        button7 = Button(self, text="Testar",#ser adicionado no client.py
                         command=self.reconhecer)
        button7.grid(row=7,column=1, sticky="w")

        button5 = Button(self, text="sair",
                         command=lambda: self.controller.show_frame(LOGIN), width=4)
        button5.grid(row=8, column=2, sticky="w")

    def reconhecer(self):#ser adicionado no client.py
        list_id, list_name = sql.show_only_name_with_id()
        aparecer, sorrir= recognizer.Recognize(list_id, list_name)
        for id in aparecer:
            usuario=sql.fetch_employee_by_id(id)
            usuario.how_many_times+=1
        for id in sorrir:
            comentario=sql.fetch_comment_by_id(id)
            comentario.smile=1

    def train(self):
        trainer.Train()

class Login_page(Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent, bg=BRANCO)
        self.label = Label(self, text="Log in", font=LARGE_FONT, bg=BRANCO)
        self.nomel = Label(self, text="Email do usuário:", font="Verdana 10", bg=BRANCO)
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
        mail = self.nome.get()
        password = self.senha.get()
        usuario = sql.fetch_employee_by_email(mail)

        try:
            if usuario.getPassword() != password and not(usuario.getIsAdmin()):
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
        self.order=[1,0]
        self.textos=["---","A-Z","Z-A","---","Cre", "Dec"]

        self.button1 = Button(self, text="Voltar",
                              command=self.sair)
        self.button1.grid(row=10, column=10)

        self.buscal = Label(self, text="Procurar:", font="Verdana 8", bg=BRANCO)
        self.buscal.grid(row=4, column=0)
        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=3)
        self.busca = Entry(self)
        self.busca.bind("<KeyRelease>",self.editar_lista)
        self.busca.grid(row=4, column=1)

    def sair(self, *args):
        self.busca.delete(0, 'end')
        self.controller.show_frame(HOME)

    def editar_lista(self, *args):
        if self.order[0] == 1:
            lista = sql.show_employee_name_order()
        elif self.order[0] == 2:
            lista = sql.show_employee_name_order_reverse()
        elif self.order[1] == 1:
            lista = sql.show_employee_score_order()
        else:
            lista = sql.show_employee_score_order_reverse()
        if self.busca.get()!="":
            j=0
            for i in range(len(lista)):
                if self.busca.get() not in lista[i-j].getEmployeeName():
                    lista.pop(i-j)
                    j+=1



        self.scrollframe.destroy()
        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=3)
        Label(self.scrollframe.viewPort, text="Nome", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=0)
        Button(self.scrollframe.viewPort, text=self.textos[self.order[0]], command=self.mudar_nome).grid(row=0, column=1)
        Label(self.scrollframe.viewPort, text="Email", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=2)
        Label(self.scrollframe.viewPort, text="Pontuação", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=3)
        Button(self.scrollframe.viewPort, text=self.textos[self.order[1]+3], command=self.mudar_score).grid(row=0,column=4)

        for row in range(len(lista)):
            Label(self.scrollframe.viewPort, text=lista[row].getEmployeeName(), bg=BRANCO).grid(row=row + 1, column=0,columnspan=2)
            Label(self.scrollframe.viewPort, text=lista[row].getEmployeeEmail(), bg=BRANCO).grid(row=row + 1, column=2)
            Label(self.scrollframe.viewPort, text=str(lista[row].getScore()), bg=BRANCO).grid(row=row + 1, column=3,columnspan=2)

    def mudar_nome(self):
        self.order[1]=0
        if self.order[0]==1:
            self.order[0]=2
        else:
            self.order[0]=1
        self.editar_lista()

    def mudar_score(self):
        self.order[0]=0
        if self.order[1]==1:
            self.order[1]=2
        else:
            self.order[1]=1
        self.editar_lista()

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

        self.is_adm=IntVar()
        self.adm = Checkbutton(self, text='Administrador', variable=self.is_adm, bg=BRANCO)
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
        if (sql.fetch_email_if_exist(self.email.get())):
            if (self.email.get() == "" or self.nome.get == "" or self.senha.get() == ""):
                messagebox.showinfo("Erro", "Informações faltando")
                self.senha.delete(0, 'end')
            else:
                new=employee_class.Employee(self.nome.get(),self.email.get(),self.senha.get(),0,self.is_adm.get(),'DEFAULT','path',0)
                id=sql.employee_2_db(new)
                new.id = id
                path=picture_taker.TakePicture(new.getEmployeeID())
                new.photo_path=path
                print(new)
                sql.update_employee_db(new)
                self.nome.delete(0, 'end')
                self.email.delete(0, 'end')
                self.senha.delete(0, 'end')
                self.adm.deselect()
                # Pegar id do novo usuário e colocar como entrada no TakePicture()
                messagebox.showinfo("Ação completada", "Usuário adicionado com sucesso")



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
        self.order=[1]
        self.textos=["Z-A", "A-Z"]

        self.button = Button(self, text="Voltar",
                             command=lambda: self.controller.show_frame(HOME))
        self.button.grid(row=4, column=5)

        self.procural = Label(self, text="Procurar", bg=BRANCO).grid(row=4, column=0)

        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=5)
        self.procura = Entry(self)
        self.procura.bind("<KeyRelease>", self.editar_lista)
        self.procura.grid(row=4, column=1)

    def editar_lista(self, *args):
        if self.order[0]==1:
            lista = sql.show_employee_name_order()
        else:
            lista = sql.show_employee_name_order_reverse()
        if self.procura.get()!="":
            j=0

            for i in range(len(lista)):
                if self.procura.get() not in lista[i-j].getEmployeeName():
                    lista.pop(i-j)
                    j+=1
        self.scrollframe.destroy()
        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=5)
        Label(self.scrollframe.viewPort, text="Nome", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=0)
        Button(self.scrollframe.viewPort, text=self.textos[self.order[0]], command= self.mudar_alfabetico).grid(row=0,column=1)

        Label(self.scrollframe.viewPort, text="Email", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=2)

        for row in range(len(lista)):
            Label(self.scrollframe.viewPort, text=lista[row].getEmployeeName(),bg=BRANCO).grid(row=row + 1, column=0, columnspan=2)
            Label(self.scrollframe.viewPort, text=lista[row].getEmployeeEmail(),bg=BRANCO).grid(row=row + 1, column=2)
            a = row
            Button(self.scrollframe.viewPort, text="editar", command=lambda x=a:
            self.controller.atualizar_usuario(lista[x].getEmployeeID())).grid(row=row + 1, column=3)

    def mudar_alfabetico(self,*args):
        if self.order[0]==1:
            self.order[0]=0
        else:
            self.order[0]=1
        self.editar_lista()


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
        self.label2.configure(text="Nome: " + sql.fetch_employee_by_id(self.ID).getEmployeeName())

    def apagar(self, *args):
        sql.delete_employee_db(sql.fetch_employee_by_id(self.ID))
        messagebox.showinfo("Ação completada", "Usuário apagado com sucesso")
        self.email.delete(0, 'end')
        self.controller.tabela_funcionarios()

    def confirmar(self, *args):
        email = self.email.get()
        if (sql.fetch_email_if_exist(email)):
            new=sql.fetch_employee_by_id(self.ID)
            new.employeeEmail=email
            sql.update_employee_db(new)
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
        self.order=[1,0] #area|data
        self.textos=["---","A-Z","Z-A","---","Cres", "Decres"]

        self.button1 = Button(self, text="Voltar",
                              command=self.voltar)
        self.button1.grid(row=4, column=5)

        self.procural = Label(self, text="Procurar", bg=BRANCO).grid(row=4, column=0)

        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=5)
        self.procura = Entry(self)
        self.procura.bind("<KeyRelease>", self.editar_lista)
        self.procura.grid(row=4, column=1)

        self.editar_lista()

    def editar_lista(self, *args):
        if self.order[0]==1:
            lista = sql.show_comment_area_order()
        elif self.order[0]==2:
            lista=sql.show_comment_area_order_reverse()
        elif self.order[1]==1:
            lista=sql.show_comment_date_order()
        else:
            lista=sql.show_comment_date_order_reverse()

        if self.procura.get()!="":
            j=0
            for i in range(len(lista)):
                if self.procura.get() not in lista[i-j].getArea():
                    lista.pop(i-j)
                    j+=1

        self.scrollframe.destroy()
        self.scrollframe = ScrollFrame(self)
        self.scrollframe.grid(row=1, column=1, columnspan=5)
        Label(self.scrollframe.viewPort, text="Data", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=0)
        Button(self.scrollframe.viewPort, text=self.textos[self.order[1]+3], command=self.mudar_data).grid(row=0,column=1)
        Label(self.scrollframe.viewPort, text="Área", font=STRONG_FONT, bg=BRANCO).grid(row=0, column=2)
        Button(self.scrollframe.viewPort, text=self.textos[self.order[0]], command=self.mudar_area).grid(row=0,column=3)

        for row in range(len(lista)):
            Label(self.scrollframe.viewPort, text=lista[row].getDate(), bg=BRANCO).grid(row=row + 1, column=0, columnspan=2)
            Label(self.scrollframe.viewPort, text=lista[row].getArea(), bg=BRANCO).grid(row=row + 1, column=2, columnspan=2)
            a = row
            Button(self.scrollframe.viewPort, text="vizualizar", command=lambda x=a:
                self.controller.mostrar_comentario(lista[x].getCommentID())).grid(row=row + 1, column=4, sticky="e")

    def mudar_area(self):
        self.order[1]=0
        if self.order[0]==1:
            self.order[0]=2
        else:
            self.order[0]=1
        self.editar_lista()

    def mudar_data(self):
        self.order[0]=0
        if self.order[1]==1:
            self.order[1]=2
        else:
            self.order[1]=1
        self.editar_lista()

    def voltar(self, *args):
        self.procura.delete(0, 'end')
        self.controller.show_frame(HOME)


def main():
    app = Window()
    app.mainloop()


main()