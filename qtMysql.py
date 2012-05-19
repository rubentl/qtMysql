#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
# vim:ts=3:sw=3:ai:foldmethod=marker:

import sys
from PyQt4 import QtCore, QtGui
from string import find
from commands import getoutput

try:  #{{{
    import psyco
    psyco.full()
except ImportError:
    print "Psyco no importado. La aplicación será más lenta."
  #}}}

Normal = QtCore.Qt.white
Error = QtCore.Qt.red
Titulo = QtCore.Qt.green
Inverso = QtCore.Qt.black

query = 'mysql %s -u %s --password="%s" %s -e "%s"'

class Ui_Principal(object):  #{{{1
    def setupUi(self, Principal):
        Principal.setObjectName("Principal")
        Principal.resize(QtCore.QSize(QtCore.QRect(0,0,780,550).size()).expandedTo(Principal.minimumSizeHint()))
        self.vboxlayout = QtGui.QVBoxLayout(Principal)
        self.vboxlayout.setObjectName("vboxlayout")

        self.Resultados = QtGui.QTextEdit(Principal)

        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(9)
        self.Resultados.setFont(font)
        self.Resultados.setFocusPolicy(QtCore.Qt.TabFocus)
        self.Resultados.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.Resultados.setAutoFormatting(QtGui.QTextEdit.AutoBulletList)
        self.Resultados.setTabChangesFocus(True)
        self.Resultados.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.Resultados.setReadOnly(True)
        self.Resultados.setObjectName("Resultados")
        self.Resultados.setTextBackgroundColor(Normal)
        self.vboxlayout.addWidget(self.Resultados)

        self.Etiqueta = QtGui.QLabel(Principal)
        self.Etiqueta.setObjectName("Etiqueta")
        self.vboxlayout.addWidget(self.Etiqueta)

        self.Historia = QtGui.QComboBox(Principal)
        self.Historia.setEditable(True)
        self.Historia.setMaxVisibleItems(5)
        self.Historia.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.Historia.setAutoCompletion(True)
        self.Historia.setObjectName("Historia")
        self.vboxlayout.addWidget(self.Historia)

        self.Boton_Salir = QtGui.QPushButton(Principal)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Boton_Salir.sizePolicy().hasHeightForWidth())
        self.Boton_Salir.setSizePolicy(sizePolicy)
        self.Boton_Salir.setObjectName("Boton_Salir")
        self.vboxlayout.addWidget(self.Boton_Salir)

        self.retranslateUi(Principal)
        QtCore.QMetaObject.connectSlotsByName(Principal)

    def retranslateUi(self, Principal):
        Principal.setWindowTitle(QtGui.QApplication.translate("Principal", "MySql con ayuda", None, QtGui.QApplication.UnicodeUTF8))
        self.Etiqueta.setText(QtGui.QApplication.translate("Principal", "Usuario:", None, QtGui.QApplication.UnicodeUTF8))
        self.Boton_Salir.setText(QtGui.QApplication.translate("Principal", "&Salir", None, QtGui.QApplication.UnicodeUTF8))
  #}}}1

class Ui_DialogoInsertar(object):  #{{{1
    def setupUi(self, DialogoInsertar):
        DialogoInsertar.setObjectName("DialogoInsertar")
        DialogoInsertar.setWindowModality(QtCore.Qt.WindowModal)
        DialogoInsertar.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(DialogoInsertar.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogoInsertar.sizePolicy().hasHeightForWidth())
        DialogoInsertar.setSizePolicy(sizePolicy)
        DialogoInsertar.setSizeGripEnabled(True)
        DialogoInsertar.setModal(True)

        self.vboxlayout = QtGui.QVBoxLayout(DialogoInsertar)
        self.vboxlayout.setObjectName("vboxlayout")

        self.botones = QtGui.QDialogButtonBox(DialogoInsertar)
        self.botones.setOrientation(QtCore.Qt.Horizontal)
        self.botones.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.botones.setObjectName("botones")
        self.vboxlayout.addWidget(self.botones)

        self.retranslateUi(DialogoInsertar)
        QtCore.QObject.connect(self.botones,QtCore.SIGNAL("accepted()"),DialogoInsertar.accept)
        QtCore.QObject.connect(self.botones,QtCore.SIGNAL("rejected()"),DialogoInsertar.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogoInsertar)

    def retranslateUi(self, DialogoInsertar):
        DialogoInsertar.setWindowTitle(QtGui.QApplication.translate("DialogoInsertar", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
  #}}}1

class SqlDBase:  #{{{1

    def __init__(self):  #{{{
        temp = self.get_names()
        self.Comandos = []
        [self.Comandos.append(a[3:].lower()) for a in temp if a[:3] == 'do_']
        self.Ayudas = []
        [self.Ayudas.append(a[5:].lower()) for a in temp if a[:5] == 'help_']
        self.Completados = []
        [self.Completados.append(a[9:].lower()) for a in temp if a[:9] == 'complete_']
        self.dbases = []
        self.tablas = []
        self.privilegios = ['all','alter','create','tables','delete','drop','execute','file','index','insert','privileges','temporary','process','references','reload','client','databases','select','shutdown','super','update','usage']
          #}}}
    def ejecutarDB_t(self,comando):  #{{{
        a = getoutput(query % ('-t',App.User,App.Contrasena,App.Base,comando))
        if a.find('ERROR') <> -1: tipo = Error
        else:	tipo = Normal
        App.Salida(a,tipo)
          #}}}
    def ejecutarDB(self,comando):  #{{{
        a = getoutput(query % ('-B',App.User,App.Contrasena,App.Base,comando))
        if a.find('ERROR') <> -1 :
            App.Salida(a,Error)
            return ''
        a = a.split('\n')
        return [i.split('\t') for i in a]
          #}}}
    def ejecutarDB_B(self,query,indice=0):  #{{{
        a=self.ejecutarDB(query)[1:]
        db = []
        for i in range(0,len(a)):
            db.append(a[i][indice])
        return db
          #}}}
    def campos(self,tablas):  #{{{
        camp = []
        for i in range(0,len(tablas)):
            tmp = self.ejecutarDB_B('desc %s' % tablas[i])
            for j in range(0,len(tmp)):
                temp = tablas[i]+'.'+tmp[j]
                if temp not in camp: camp.append(temp)
        return camp
          #}}}
    def valor_de_campo(self,campo):  #{{{
        tabla,camp  = campo.split('.')
        return  self.ejecutarDB_B('select %s from %s order by %s' % (camp,tabla,camp))[1:]
          #}}}
    def tipo_de_campo(self,tabla):  #{{{
        return self.ejecutarDB_B('desc %s' % tabla,1)
          #}}}
    def indices(self,tablas):  #{{{
        camp = []
        for i in range(0,len(tablas)):
            tmp = self.ejecutarDB_B('show index from %s' % tablas[i],4)
        for j in range(0,len(tmp)):
            temp = tablas[i]+'.'+tmp[j]
            if temp not in camp: camp.append(temp)
        return camp
          #}}}
    def get_names(self):  #{{{
        names = []
        classes = [self.__class__]
        while classes:
            aclass = classes.pop(0)
            if aclass.__bases__:
                classes = classes + list(aclass.__bases__)
            names = names + dir(aclass)
        return names
          #}}}
    def help_HELP(self):  #{{{
        """Teclea <help> seguido del comando sobre el que quieres ayuda.
Teclea <F1> cuando necesites ayuda dentro de la edición de un comando.
Teclea <help help> para saber todos los comandos que tienen ayuda.\n"""
    def do_HELP(self):
        linea = str(App.Comando.displayText()).lower().split()
        if len(linea) == 1:
            App.Salida(self.help_HELP.__doc__)
        elif len(linea) == 2:
            if (linea[1] in self.Ayudas):
                App.Salida(getattr(self,'help_'+linea[1].upper()).__doc__)
            if (linea[1] == 'help'):
                App.Salida('____AYUDAS____:',Titulo)
                App.Columnize(self.Ayudas)
        else:pass
          #}}}
#----------------------------------------------------------------------------------[ INSERTAR ]----------------------  #{{{
    def help_INSERTAR(self):
        """Abre un cuadro de diálogo para facilitar la introducción
de nuevos datos."""
    def do_INSERTAR(self):
        linea = str(App.Comando.displayText()).lower().split()
        if len(linea) == 1:
            App.Salida('Debes indicarme la tabla en la que quieres introducir los datos.',Error)
        else:
            loscampos = self.campos([linea[1]])
            self.tipos = self.tipo_de_campo(linea[1])
            elDialogo=QtGui.QDialog()
            ui = Ui_DialogoInsertar()
            ui.setupUi(elDialogo)
            elDialogo.setWindowTitle(elDialogo.tr('insert table '+linea[1]))
            tmp = 70*len(loscampos)
            if tmp < 250: tmp =250 
            elDialogo.setGeometry(0,0,400,tmp)
            self.combo = []
            for x in range(0,len(loscampos)):
                self.groupBox = QtGui.QGroupBox(elDialogo)
                self.groupBox.setTitle(elDialogo.tr(loscampos[x].split('.')[1]+' <'+self.tipos[x]+'>'))
                self.combo.append(QtGui.QComboBox(self.groupBox))
                self.combo[-1].setGeometry(QtCore.QRect(10,20,361,25))
                self.combo[-1].setObjectName(elDialogo.tr(loscampos[x].split('.')[1]))
                if self.tipos[x].find('enum') <> -1: self.combo[-1].setEditable(False)
                else: self.combo[-1].setEditable(True)
                self.combo[-1].setMaxVisibleItems(10)
                self.combo[-1].InsertPolicy(QtGui.QComboBox.InsertAtTop)
                self.combo[-1].setDuplicatesEnabled(False)
                self.combo[-1].setAutoCompletion(True)
                valores = self.valor_de_campo(loscampos[x])
                for i in range(0,len(valores)):
                    if valores[i] <> '' and self.combo[-1].findText(elDialogo.tr(valores[i])) == -1:
                        self.combo[-1].addItem(elDialogo.tr(valores[i]))
                ui.vboxlayout.addWidget(self.groupBox)
            self.combo[0].setFocus()
            if elDialogo.exec_():
                self.txt = "insert "+linea[1]+" values ("
                for x in range(0,len(loscampos)):
                    tmp = str(self.combo[x].currentText())
                    if self.tipos[x].find('char') <> -1 or self.tipos[x].find('text') <> -1 or	((self.tipos[x].find('enum') <> -1 or self.tipos[x].find('set') <> -1) and (self.tipos[x].find("'") <> -1 or self.tipos[x].find('"') <> -1)):
                        tmp = "'"+tmp+"'"
                    self.txt = self.txt+tmp
                    if x < (len(loscampos)-1): self.txt = self.txt + ","
                self.txt = self.txt+')'
                App.Salida(self.txt)
                self.ejecutarDB_t(self.txt)
                self.do_INSERTAR()
            else:
                pass

    def complete_INSERTAR(self):
        if str(App.Comando.displayText()).lower().split() == 'insertar':
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else:
            App.Salida(self.help_INSERTAR.__doc__)
          #}}}
#----------------------------------------------------------------------------------[ ANALIZE ]-----------------------  #{{{
    def help_ANALYZE(self):
        """ANALYZE TABLE <tabla> [, <tabla> ...]"""
    def do_ANALYZE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def complete_ANALYZE(self):
        if str(App.Comando.displayText()).lower().split() == ['analyze','table']:
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else:
            App.Salida(self.help_ANALYZE.__doc__)
          #}}}
#---------------------------------------------------------------------------------[ BACKUP ]-------------------------  #{{{
    def do_BACKUP(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def complete_BACKUP(self):
        if str(App.Comando.displayText()).lower().split() == ['backup','table']:
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else:
            App.Salida(self.help_BACKUP.__doc__)
    def help_BACKUP(self):
        """BACKUP TABLE <tabla> [, <tabla> ...] TO <ruta>"""
          #}}}
#---------------------------------------------------------------------------------[ BEGIN ]--------------------------  #{{{
    def do_BEGIN(self):
        self.ejecutarDB_t('BEGIN')
    def help_BEGIN(self):
        """BEGIN inicia una transacción."""
          #}}}
#---------------------------------------------------------------------------------[ ALTER ]--------------------------  #{{{
    def do_ALTER(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def complete_ALTER(self):
        linea = str(App.Comando.displayText()).lower().split()
        if len(linea) > 1 and linea[-1] in ['table','index','unique','fulltex','key','alter','change','first','after','drop','by']:
            if linea[-1] == 'table': 
                App.Salida('____TABLAS____:',Titulo)
                App.Columnize(self.tablas)
            elif linea[-1] in ['index','unique','fulltext','key']: 
                App.Salida('____INDICES____:',Titulo)
                App.Columnize(self.indices(self.tablas))
            elif linea[-1] in ['alter','change','first','after','drop','by']: 
                App.Salida('____CAMPOS____:',Titulo)
                App.Columnize(self.campos(self.tablas))
        else: 
            App.Salida(self.help_ALTER.__doc__)
    def  help_ALTER(self):
        """ALTER [IGNORE] TABLE <tabla> <especificación alter> [,<especificación alter>...]
        la especificación alter:
        ADD [COLUMN] <definición create> [FIRST | AFTER <campo>]
        ADD [COLUMN] ( <definición create>, <definición create>, ... )
        ADD INDEX [<nombre de índice>] ( <campo>, ...)
        ADD UNIQUE [<nombre de índice>] ( <nombre de índice>, ... )
        ADD FULLTEXT [<nombre de índice>] ( <nombre de índice>, ... )
        ADD [CONSTRAINT <símbolo>] FOREIGN KEY <nombre de índice> (<nombre de índice>, ... ) [<referencia de definición>]
        ALTER [COLUMN] <nombre de campo> {SET DEFAULT <literal> | DROP DEFAULT }
        CHANGE [COLUMN] <nombre de campo> <definición create> [FIRST | AFTER <nombe de campo>]
        MODIFY [COLUMN] <definición create> [FIRST | AFTER <nombe de campo>]
        DROP [COLUMN] <nombre de campo>
        DROP PRIMARY KEY
        DROP INDEX <nombre de índice>
        DISABLE KEYS
        ENABLE KEYS
        RENAME [TO] <nuevo nombre de tabla>
        ORDER BY <nombre de campo> <opciones de tabla>"""
      #}}}
#----------------------------------------------------------------------------------------[ CHECK TABLE ]-------------  #{{{
    def do_CHECK(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_CHECK(self):
        """CHECK TABLE <tabla> [ ,<tabla> ... ] [ CHANGED | EXTENDED | FAST | MEDIUM | QUICK ]"""
    def complete_CHECK(self):
        if str(App.Comando.displayText()).lower().split() == ['check','table']: 
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else:
            App.Salida(self.help_CHECK.__doc__)
              #}}}
#---------------------------------------------------------------------------------[ COMMIT ]-------------------------  #{{{
    def do_COMMIT(self):
        self.ejecutarDB_t('COMMIT')
    def help_COMMIT(self):
        """COMMIT finaliza un conjunto de instrucciones y vuelca los resultados a disco."""
                  #}}}
#---------------------------------------------------------------------------------------[ CREATE ]-------------------  #{{{
    def do_CREATE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
        self.dbases = self.ejecutarDB_B('SHOW DATABASES')
    def help_CREATE(self):
        """CREATE DATABASE [ IF NOT EXISTS ] <dbase>
        CREATE [UNIQUE | FULLTEXT] INDEX <nombre de índice> ON tabla (<campo> [<(longitud)>], ... )
        CREATE [TEMPORARY] TABLE [IF NOT EXISTS] <tabla> [( <crear definición>, ... )] [<opciones de tabla>] [<instrucción select>]
        crear definición:
        <campo> <tipo> [NOT NULL | NULL] [DEFAULT  <valor predeterminado>] [AUTO_INCREMENT] [PRIMARY KEY] [<definición de referencia>]
        PRIMARY KEY (<nombre de campo de índice>, ...)
        KEY [<nombre de índice] (<nombre de campo de índice>, ...)
        UNIQUE [INDEX] [<nombre de índice>] (<nombre de campo de índice>, ...)
        FULLTEXT [INDEX] [<nombre de índice>] (<nombre de campo de índice>, ...)
        [CONSTRAINT <símbolo>] FOREIGN KEY [<nombre de índice>] [<nombre de campo de índice>] [<definición de referencia>]
        CHECK (<expresión>)
        tipo:
        TINYINT[(<longitud>] [UNSIGNED] [ZEROFILL]
        SMALLINT[(<longitud>] [UNSIGNED] [ZEROFILL]
        MEDIUMINT[(<longitud>] [UNSIGNED] [ZEROFILL]
        INT[(<longitud>] [UNSIGNED] [ZEROFILL]
        INTEGER[(<longitud>] [UNSIGNED] [ZEROFILL]
        BIGINT[(<longitud>] [UNSIGNED] [ZEROFILL]
        REAL[(<longitud,decimales>] [UNSIGNED] [ZEROFILL]
        DOUBLE[(<longitud,decimales>] [UNSIGNED] [ZEROFILL]
        FLOAT[(<longitud,decimales>] [UNSIGNED] [ZEROFILL]
        DECIMAL[(<longitud,decimales>] [UNSIGNED] [ZEROFILL]
        NUMERIC[(<longitud,decimales>] [UNSIGNED] [ZEROFILL]
        CHAR(<longitud>) [BINARY]
        VARCHAR(<longitud>)
        DATE
        TIME
        TIMESTAMP
        DATETIME
        TINYBLOB
        BLOB
        MEDIUMBLOB
        LONGBLOB
        TINYTEXT
        TEXT
        MEDIUMTEXT
        LONGTEXT
        ENUM (<valor1>,<valor2>, ...)
        SET (<valor1>,<valor2>, ...)
        nombre de campo de índice:
        <nombre de campo> [(<longitud>)]
        definición de referencia:
        REFERENCES <tabla> [(<nombre de campo de índice>, ...)] [MATCH FULL | MATCH PARTIAL] [ON DELETE <opción de referencia>] [ON UPDATE <opción de referencia>]
        opción de referencia:
        RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT
        opciones de tabla:
        TYPE = { BDB | HEAP | ISAM | INNODB | MERGE | MRG_MYISAM | MYISAM}
        AUTO_INCREMENT = #
        AVG_ROW_LENGTH = #
        CHECKSUM = {0 | 1}
        COMMENT = "cadena"
        MAX_ROWS = #
        MIN_ROWS = #
        PACK_KEYS = {0 | 1 | DEFAULT}
        PASSWORD = "cadena"
        DELAY_KEY_WRITE = {0 | 1}
        ROW_FORMAT = { predeterminado | dinámico | fijo | comprimido }
        RAID_TYPE = {1 | STRIPED | RAID0}
        RAID_CHUNKS = #
        RAID_CHUNKSIZE = #
        UNION = (<tabla>, [<tabla> ... ])
        INSERT_METHOD = {NO | FIRST | LAST }
        DATA DIRECTORY = "ruta absoluta a directorio"
        INDEX DIRECTORY = "ruta absoluta a directorio"
        instrucción select:
        [IGNORE | REPLACE] SELECT ... (instrucción select)"""
    def complete_CREATE(self):
        App.Salida(self.help_CREATE.__doc__)
          #}}}
#----------------------------------------------------------------------------------------[ DELETE ]------------------  #{{{
    def do_DELETE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
        self.dbases = self.ejecutarDB_B('SHOW DATABASES')
        self.tablas = self.ejecutarDB_B('SHOW TABLES')
    def help_DELETE(self):
        """DELETE [LOW_PRIORITY | QUICK] FROM <tabla> [WHERE <cláusula>] [ORDER BY  ...] [LIMIT <filas>]
DELETE [LOW_PRIORITY | QUICK] <tabla [.*]> [,<tabla [.*]> ...] FROM <referencias de tablas> [WHERE <cláusula>]
DELETE [LOW_PRIORITY | QUICK] FROM <tabla [.*]>, [<tabla [.*]> ...] USING <referencias de tablas> [WHERE <cláusula>]"""
    def complete_DELETE(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] in ['from','low_priority','quick','using']:
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else:
            App.Salida(self.help_DELETE.__doc__)
              #}}}
#----------------------------------------------------------------------------------------[ DESCRIBE ]----------------  #{{{
    def do_DESCRIBE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_DESCRIBE(self):
        """DESCRIBE <tabla> [<campo> | <comodin>]"""
    def complete_DESCRIBE(self):
        linea = str(App.Comando.displayText()).lower().split() 
        if linea[-1] == 'describe':
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        elif linea[-1] in self.tablas:
            App.Salida('____CAMPOS____:',Titulo)
            App.Columnize(self.campos(self.tablas))
        else:	
            App.Salida(self.help_DESCRIBE.__doc__)
              #}}}
#----------------------------------------------------------------------------------------[ DO ]----------------------  #{{{
    def do_DO(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_DO(self):
        """DO <expresión>, [ <expresión>, ...]"""
    def complete_DO(self):
        App.Salida(self.help_DO.__doc__)
          #}}}
#----------------------------------------------------------------------------------------[ DROP ]--------------------  #{{{
    def do_DROP(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
        self.dbases = self.ejecutarDB_B('SHOW DATABASES')
        self.tablas = self.ejecutarDB_B('SHOW TABLES')
    def help_DROP(self):
        """DROP DATABASES [IF EXISTS] <dbase> 
DROP TABLE [IF EXISTS] <tabla> [, <tabla>, ...] [RESTRICT | CASCADE]
DROP INDEX <índice> ON <tabla> """
    def complete_DROP(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[1] == 'databases':
            App.Salida('____BASES_DE_DATOS____:',Titulo)
            App.Columnize(self.dbases)
        elif linea[1] == 'table':
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        elif linea[1] == 'index':
            App.Salida('____ÍNDICES____:',Titulo)
            App.Columnize(self.indices(self.tablas))
        else:	
            App.Salida(self.help_DROP.__doc__)
              #}}}
#----------------------------------------------------------------------------------------[ EXPLAIN ]-----------------  #{{{
    def do_EXPLAIN(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_EXPLAIN(self):
        """ EXPLAIN <tabla>
EXPLAIN <consulta select>"""
    def complete_EXPLAIN(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'explain':
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else:	
            App.Salida(self.help_EXPLAIN.__doc__)
              #}}}
#----------------------------------------------------------------------------------------[ FLUSH ]-------------------  #{{{
    def do_FLUSH(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_FLUSH(self):
        """FLUSH <opción de vaciado> [,<opción de vaciado> ... ]
        opción de vaciado:
        DES_KEY_FILE
        HOSTS
        LOGS
        QUERY CACHE
        PRIVILEGES
        STATUS
        TABLES
        [TABLE | TABLES] <tabla> [, <tabla> ...]
        TABLES WITH READ LOCK
        USER_RESOURCES"""
    def complete_FLUSH(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] in ['table','tables']:
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else:	
            App.Salida(self.help_FLUSH.__doc__)
              #}}}
#---------------------------------------------------------------------------------------[ GRANT ]--------------------  #{{{
    def do_GRANT(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_GRANT(self):
        """GRANT <privilegio> [(<lista de campos>)] [, <privilegio> [(<lista de campos>)] .. ]
        ON {<tabla> | * | *.* | <dbase>.*}
        TO <usuario> [IDENTIFIED BY [PASSWORD] 'contraseña'] [, <usuario> [IDENTIFIED BY 'contraseña'] ... ]
        [REQUIRE
        NONE | 
        [ {SSL | X509} ]
        [CIPHER <cifrado> [AND]]
        [ISSUER <emisor> [AND]]
        [SUBJECT <asunto>]]
        [WITH [GRANT OPTION | MAX_QUERIES_PER_HOUR #
                       | MAX_UPDATES_PER_HOUR #
                       | MAX_CONNECTIONS_PER_HOUR #]]"""
    def complete_GRANT(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'on':
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        elif linea[-1] in self.privilegios:
            App.Salida('____CAMPOS____:',Titulo)
            App.Columnize(self.campos(self.tablas))
        else:	
            App.Salida(self.help_GRANT.__doc__)
              #}}}
#---------------------------------------------------------------------------------------[ INSERT ]-------------------  #{{{
    def do_INSERT(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_INSERT(self):
        """INSERT [LOW_PRIORITY | DELAYED] [IGNORE]
        [INTO] <tabla> [(<campo,...)]
        VALUES ((<expresión> | DEFAULT),...),(...),...
        [ON DUPLICATE KEY UPDATE <campo>=<expresión>, ...]
INSERT [LOW_PRIORITY | DELAYED] [IGNORE]
        [INTO] <tabla> [(<campo,...)]'
        SELECT
INSERT [LOW_PRIORITY | DELAYED] [IGNORE]
        [INTO] <tabla> 
        SET <campo>=(<expresión> | DEFAULT), ...
        [ON DUPLICATE KEY UPDATE <campo>=<expresión>, ...]
INSERT [LOW_PRIORITY] [IGNORE] [INTO] <tabla> [(<lista de campos>)] SELECT ..."""
    def complete_INSERT(self):
        linea = str(App.Comando.displayText()).lower().split()
        tmp = ['update','set']
        tmp.append(self.tablas)
        if linea[-1] in ['insert','into']:
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        elif linea[-1] in tmp:
            App.Salida('____CAMPOS____:',Titulo)
            App.Columnize(self.campos(self.tablas))
        else:
            App.Salida(self.help_INSERT.__doc__)
              #}}}
#---------------------------------------------------------------------------------------[ KILL ]---------------------  #{{{
    def do_KILL(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_KILL(self):
        """KILL <id_subproceso>"""
          #}}}
#---------------------------------------------------------------------------------------[ LOAD DATA INFILE ]---------  #{{{
    def do_LOAD(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_LOAD(self):
        """LOAD DATA [LOW_PRIORITY | CONCURRENT] [LOCAL] INFILE <nombre archivo>
        [REPLACE | IGNORE]
        INTO TABLE <tabla>
        [FIELDS
        [TERMINATED BY <\\t>]
        [ [OPTIONALLY] ENCLOSED BY <''>]
        [ESCAPED BY <\\>] ]
        [LINES
        [STARTING BY <''>]
        [TERMINATED BY <\\n>] ]
        [IGNORE <número> LINES]
        [(<campo>, ...)]"""
    def complete_LOAD(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'table':
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else:	
            App.Salida(self.help_LOAD.__doc__)
              #}}}
#-----------------------------------------------------------------------------------------[ LOCK TABLES ]------------  #{{{
    def do_LOCK(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_LOCK(self):
        """LOCK TABLES <tabla> [AS <alias>] {READ [LOCAL] | [LOW_PRIORITY] | WRITE}
        [, <tabla> [AS <alias>] {READ [LOCAL] | [LOW_PRIORITY] | WRITE} ... ]"""
    def complete_LOCK(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'tables': 
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else: 
            App.Salida(self.help_LOCK.__doc__)
          #}}}
#----------------------------------------------------------------------------------------[ OPTIMIZE ]----------------  #{{{
    def do_OPTIMIZE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_OPTIMIZE(self):
        """OPTIMIZE TABLE <tabla> [, <tabla> ...]"""
    def complete_OPTIMIZE(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'table': 
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else: 
            App.Salida(self.help_OPTIMIZE.__doc__)
              #}}}
#----------------------------------------------------------------------------------------[ RENAME ]------------------  #{{{
    def do_RENAME(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
        self.dbases = self.ejecutarDB_B('SHOW DATABASES')
        self.tablas = self.ejecutarDB_B('SHOW TABLES')
    def help_RENAME(self):
        """RENAME TABLE <tabla> TO <tabla> [, <tabla> TO <tabla>, ...]"""
    def complete_RENAME(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'table': 
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else: 
            App.Salida(self.help_RENAME.__doc__)
          #}}}
#----------------------------------------------------------------------------------------[ REPAIR TABLE ]------------  #{{{
    def do_REPAIR(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_REPAIR(self):
        """REPAIR TABLE <tabla> [, <tabla> ...] [EXTENDED] [QUICK] [USE_FRM]"""
    def complete_REPAIR(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] in ['table',',']: 
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else: 
            App.Salida(self.help_REPAIR.__doc__)
              #}}}
#---------------------------------------------------------------------------------------[ REPLACE ]------------------  #{{{
    def do_REPLACE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_REPLACE(self):
        """REPLACE [LOW_PRIORITY | DELAYED] [INTO] <tabla> [(<campo>,...)] VALUES (<expresion>, ...),  (...) ...
REPLACE [LOW_PRIORITY | DELAYED] [INTO] <tabla> [(<campo>,...)] SELECT ...
REPLACE [LOW_PRIORITY | DELAYED] [INTO] <tabla> SET <campo>=<expresión>, ..."""
    def complete_REPLACE(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] in ['replace','into','low_priority','delayed']: 
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        elif linea[-1] in ['set'].append(self.tablas):
            App.Salida('____CAMPOS____:',Titulo)
            App.Columnize(self.campos(self.tablas))
        else: 
            App.Salida(self.help_REPLACE.__doc__)
          #}}}
#---------------------------------------------------------------------------------------[ RESET ]--------------------  #{{{
    def do_RESET(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_RESET(self):
        """RESET <opción reset> [,<opción reset>] ...
        opción reset: MASTER , QUERY CACHE , SLAVE"""
    def complete_RESET(self): 
        App.Salida(self.help_RESET.__doc__)
          #}}}
#---------------------------------------------------------------------------------------[ RESTORE TABLA ]------------  #{{{
    def do_RESTORE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_RESTORE(self):
        """RESTORE TABLE <tabla> [, <tabla> ...] FROM <ruta>"""
    def complete_RESTORE(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] in ['table',',']: 
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else: 
            App.Salida(self.help_RESTORE.__doc__)
              #}}}
#---------------------------------------------------------------------------------------[ REVOKE ]-------------------  #{{{
    def do_REVOKE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_REVOKE(self):
        """REVOKE <privilegio> [(<lista de campos>)] [, <privilegio> [(<lista de campos>)] .. ]
        ON {<tabla> | * | *.* | <dbase>.*}
        FROM <usuario> """
    def complete_REVOKE(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'on': 
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        elif linea[-1] in self.privilegios:
            App.Salida('____CAMPOS____:',Titulo)
            App.Columnize(self.campos(self.tablas))
        else: 
            App.Salida(self.help_REVOKE.__doc__)
              #}}}
#---------------------------------------------------------------------------------------[ ROLLBACK ]-----------------  #{{{
    def do_ROLLBACK(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_ROLLBACK(self):
        """Elimina una transacción o conjunto de instrucciones, y deshace todas las instrucciones de esa transacción."""
                  #}}}
#---------------------------------------------------------------------------------------[ SELECT ]-------------------  #{{{
    def do_SELECT(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_SELECT(self):
        """SELECT [STRAIGHT_JOIN] [SQL_SMALL_RESULT] [SQL_BIG_RESULT] [SQL_BUFFER_RESULT] [SQL_CACHE | SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS] [HIGH_PRIORITY] [DISTINT | DISTINTROW | ALL]
        <select expresión>, ...
        [INTO {OUTFILE | DUMPFILE} <archivo> <opciones de exportación>]
        [FROM <tabla>
        [WHERE <cláusula where>]
        [GROUP BY {<entero sin signo> | <campo> | fórmula} [ASC | DESC] , ... [WITH ROLLUP] ]
        [HAVING <cláusula where>]
        [ORDER BY {<entero sin signo> | <campo> | fórmula} [ASC | DESC] , ...]
        [LIMIT [<desplazamiento>,] <filas> | <filas> OFFSET <desplazamiento>]
        [PROCEDURE <procedimiento(argumentos)>]
        [FOR UPDATE | LOCK IN SHARE MODE]"""
    def complete_SELECT(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'from':
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        elif linea[-1] in	['select','straight_join','sql_small_result','sql_big_result','sql_buffer_result','sql_cache','sql_no_cache','sql_calc_found_rows','high_priority','distint','distintrow','all','by']:
            App.Salida('____CAMPOS____:',Titulo)
            App.Columnize(self.campos(self.tablas))
        else:
            App.Salida(self.help_SELECT.__doc__)
              #}}}
#---------------------------------------------------------------------------------------[ SET ]----------------------  #{{{
    def do_SET(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_SET(self):
        """SET [GLOBAL | SESSION] <variable>=<expresión> [, [GLOBAL | SESSION] <variable>=<expresión> ...]
SET [GLOBAL | SESSION] TRANSACTION LEVEL { READ UNCOMMITTED | READ COMMITTED | REPEATABLE READ | SERIALIZABLE }"""
    def complete_SET(self):
        self.var = self.ejecutarDB_B('SHOW VARIABLES')
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] in ['set','global','session','.']: 
            App.Salida('____VARIABLES____:',Titulo)
            App.Columnize(self.var)
        else: 
            App.Salida(self.help_SET.__doc__)
              #}}}
#----------------------------------------------------------------------------------------[ TRUNCATE ]----------------  #{{{
    def do_TRUNCATE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
        self.dbases = self.ejecutarDB_B('SHOW DATABASES')
        self.tablas = self.ejecutarDB_B('SHOW TABLES')
    def help_TRUNCATE(self):
        """TRUNCATE TABLE <tabla>"""
    def complete_TRUNCATE(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'table':
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else: 
            App.Salida(self.help_TRUNCATE.__doc__)
              #}}}
#---------------------------------------------------------------------------------------[ UNLOCK TABLES ]------------  #{{{
    def do_UNLOCK(self):
        self.ejecutarDB_t('UNLOCK TABLES')
    def help_UNLOCK(self):
        """UNLOCK TABLES  Libera todas las tablas de la conexión actual."""
    def complete_UNLOCK(self):
        App.Salida(self.help_UNLOCK.__doc__)
  #}}}
#----------------------------------------------------------------------------------------[ UPDATE ]------------------  #{{{
    def do_UPDATE(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def help_UPDATE(self):
        """UPDATE [LOW_PRIORITY] [IGNORE] <tabla>
        SET <campo>=<expresión> [, <campo>=<expresión> ...]
        [WHERE <expresión where>]
        [LIMIT <nº filas>]"""
    def complete_UPDATE(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] in ['update','ignore','low_priority']: 
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        elif linea[-1] in ['set',',']:
            App.Salida('____CAMPOS____:',Titulo)
            App.Columnize(self.campos(self.tablas))
        else: 
            App.Salida(self.help_UPDATE.__doc__)
              #}}}
#----------------------------------------------------------------------------------------[ SHOW ]--------------------  #{{{
    def do_SHOW(self):
        self.ejecutarDB_t(str(App.Comando.displayText()))
    def complete_SHOW(self):
        linea = str(App.Comando.displayText()).lower().split()
        if linea[-1] == 'from':
            if linea[-2] in ['tables','status'].append(self.tables):
                App.Salida('____BASES_DE_DATOS____:',Titulo)
                App.Columnize(self.dbases)
            elif linea[-2] in ['columns','index']:
                App.Salida('____TABLAS____:',Titulo)
                App.Columnize(self.tablas)
        elif linea[-1] == 'table':
            App.Salida('____TABLAS____:',Titulo)
            App.Columnize(self.tablas)
        else: 
            App.Salida(self.help_SHOW.__doc__)
    def help_SHOW(self):
        """SHOW DATABASES [LIKE <expresión>]
SHOW [OPEN] TABLES [FROM <dbase>] [LIKE <expresión>]
SHOW [FULL] COLUMNS FROM <tabla> [FROM <dbase>] [LIKE <expresión>]
SHOW INDEX FROM <tabla> [FROM <dbase>]
SHOW TABLE STATUS [FROM <dbase>] [LIKE <expresión>]
SHOW STATUS [LIKE <expresión>]
SHOW VARIABLES [LIKE <expresión>]
SHOW LOGS
SHOW [FULL] PROCESSLIST
SHOW GRANTS FOR <usuario>
SHOW CREATE TABLE <tabla>
SHOW MASTER STATUS
SHOW MASTER LOGS
SHOW SLAVE STATUS"""
  #}}}
#---------------------------------------------------------------------------------------[ USE ]----------------------  #{{{
    def do_USE(self):
        App.Base = str(App.Comando.displayText()).split()[1]
        self.ejecutarDB_t('SHOW TABLES')
        self.tablas = self.ejecutarDB_B('SHOW TABLES')
        [self.ejecutarDB_t('DESCRIBE %s' % a) for a in self.tablas]
    def help_USE(self):
        """USE <dbase>"""
    def complete_USE(self):
        App.Salida('____BASES_DE_DATOS____:',Titulo)
        App.Columnize(self.dbases)
#---------------------------------------------------------------------------------------[ FUNCIONES ]----------------  #{{{
    def help_ADDDATE(self):
        """ADDDATE(fecha,INTERVAL tipo de expresión). Sinónimo de DATE_ADD()."""
    def help_CURDATE(self):
        """Sinónimo de la función CURRENT_DATE()."""
    def help_CURRENT_DATE(self):
        """Devuelve la fecha actual."""
    def help_CURRENT_TIME(self):
        """Devuelve la hora actual."""
    def help_CURRENT_TIMESTAMP(self):
        """Equivale a la función now()."""
    def help_CURTIME(self):
        """Sinónimo de CURRENT_TIME()."""
    def help_DATE_ADD(self):
        """DATE_ADD(fecha,INTERVAL tipo de expresión).
Añade o resta un período de tiempo a la fecha especificada.
Ejemplo: SELECT DATE_ADD("2002-12-25", INTERVAL 1 MONTH)"""
    def help_DATE_FORMAT(self):
        """DATE_FORMAT(fecha,cadena_formato).
Aplica un formato a la fecha especificada en función de la cadena de formato."""
    def help_DATE_SUB(self):
        """DATE_SUB(fecha,INTERVAL tipo de expresión).
Resta un determinado período de tiempo de la fecha especificada.
Ejemplo: SELECT DATE_SUB("2002-12-25 13:00:00",INTERVAL "14:13" MINUTE_SECOND)."""
    def help_DAYNAME(self):
        """DAYNAME(fecha).
Devuelve el nombre del día de la fecha especificada."""
    def help_DAYOFMONTH(self):
        """DAYOFMONTH(fecha).
Devuelve el día del mes de la fecha especificada como número."""
    def help_DAYOFWEEK(self):
        """DAYOFWEEK(fecha).
Devuelve el día de la semana de la fecha especificada como número."""
    def help_DAYOFYEAR(self):
        """DAYOFYEAR(fecha).
Devuelve el día del año de la fecha especificada como número."""
    def help_EXTRACT(self):
        """EXTRACT(tipo_de_fecha FROM fecha).
Utiliza el tipo de fecha para devolver la parte de la fecha.
Ejemplo: SELECT EXTRACT(YEAR FROM "2002-02-03")."""
    def help_FROM_DAYS(self):
        """FROM_DAYS(número).
Convierte el número especificado a una fecha basada en el número de días transcurridos desde el 1 de enero del año 0."""
    def help_FROM_UNIXTIME(self):
        """FROM_UNIXTIME(marca_de_tiempo_unix [, cadena_formato]).
Convierte la marca de tiempo especificada en una fecha y devuelve el resultado."""
    def help_HOUR(self):
        """HOUR(hora). Devuelve la hora de la hora especificada."""
    def help_MINUTE(self):
        """MINUTE(hora). Devuelve los minutos de la hora especificada."""
    def help_MONTH(self):
                """MONTH(fecha). Devuelve el mes de la fecha especificada."""
    def help_MONTHNAME(self):
                """MONTHNAME(fecha). Devuelve el nombre del mes de la fecha especificada."""
    def help_NOW(self):
                """Devuelve la marca de hora actual."""
    def help_PERIOD_ADD(self):
                """PERIOD_ADD(período,meses). Devuelve los meses al período especificado como AAAAMM."""
    def help_PERIOD_DIFF(self):
                """PERIOD_DIFF(período1,período2). Devuelve el número de meses comprendidos entre período1 y período2."""
    def help_QUARTER(self):
                """QUARTER(fecha). Devuelve el trimestre de la fecha especificada."""
    def help_SEC_TO_TIME(self):
                """SEC_TO_TIME(segundos). Convierte los segundos en hora y devuelve una cadena o un número."""
    def help_SECOND(self):
                """SECOND(hora). Devuelve los segundos de la hora especificada."""
    def help_SUBDATE(self):
                """SUBDATE(fecha,INTERVAL tipo de expresión). Sinónimo de DATE_SUB."""
    def help_SYSDATE(self):
                """SYSDATE(). Sinónimo de NOW."""
    def help_TIME_FORMAT(self):
                """TIME_FORMAT(hora,formato). Idéntico a DATE_FORMAT() aunque sólo se pueden usar el subconjunto de formatos de hora."""
    def help_TIME_TO_SEC(self):
                """TIME_TO_SEC(hora). Convierte la hora en segundos."""
    def help_TO_DAYS(self):
                """TO_DAYS(fecha). Devuelve los días transcurridos desde el 1 de enero del año 0 hasta la fecha especificada."""
    def help_UNIX_TIMESTAMP(self):
                """UNIX_TIMESTAMP([fecha]). Devuelve un entero sin signo que representa la marca de tiempo UNIX 
hasta la hora del sistema o la fecha especificada."""
    def help_WEEK(self):
                """WEEK(date [,inicio_semana]). Devuelve la semana de un determinado año de la fecha especificada. 
La semana comienza en domingo a menos que se indique 1 en el parámetro opcinal y sea así el lunes."""
    def help_WEEKDAY(self):
                """WEEKDAY(fecha). Devuelve el día de la semana de la fecha especificada como un número: 0 es lunes."""
    def help_YEAR(self):
                """YEAR(fecha). Devuelve el año de la fecha especificada."""
    def help_YEARWEEK(self):
                """YEARWEEK(fecha [,inicio_semana]). Devuelve una combinación del año y la semana de la fecha especificada."""
    def help_VERSION(self):
                """Muestra la versión del servidor MySQL."""  #}}}
#---------------------------------------------------------------------------------------[ salir ]--------------------  #{{{
    def do_SALIR(self):
        App.quit()
  #}}}	
                      #}}}1

class MyApp(QtGui.QApplication):  #{{{1
    def __init__(self):  #{{{2
        self.User = ''
        self.Base = ''
        self.Contrasena = ''
        QtGui.QApplication.__init__(self,sys.argv)
        self.Principal = QtGui.QWidget()
        self.ui = Ui_Principal()
        self.ui.setupUi(self.Principal)
        self.Comando = self.ui.Historia.lineEdit()
        self.Comando.setFocus()
        self.Principal.connect(self.ui.Boton_Salir,QtCore.SIGNAL('clicked()'),self,QtCore.SLOT('quit()'))
        self.Principal.connect(self.Comando,QtCore.SIGNAL('returnPressed()'),self.Ejecutar)
        #self.Principal.connect(self.Comando,QtCore.SIGNAL('textEdited(QString)'),self.ParaCompletar)
        ParaAyuda = QtGui.QAction(self.Principal.tr('Ayuda'),self.Principal)
        ParaAyuda.setShortcut(QtGui.QKeySequence(self.Principal.tr('F1')))
        self.Principal.connect(ParaAyuda,QtCore.SIGNAL('triggered()'),self.Completar)
        self.Principal.addAction(ParaAyuda)
        ParaSalir = QtGui.QAction(self.Principal.tr('Salir'),self.Principal)
        ParaSalir.setShortcut(QtGui.QKeySequence(self.Principal.tr('Escape')))
        self.Principal.connect(ParaSalir,QtCore.SIGNAL('triggered()'),self.quit)
        self.Principal.addAction(ParaSalir)
        self.Sql = SqlDBase()
        self.Principal.show()  #}}}2

    def Completar(self):  #{{{2
        linea = str(self.Comando.displayText()).lower().split()
        if len(linea) == 0:
            self.Salida('____COMANDOS____:',Titulo)
            self.Columnize(self.Sql.Comandos)
        else:
            if len(linea) > 0:
                if linea[0] in self.Sql.Completados:
                    func=getattr(App.Sql,'complete_'+linea[0].upper())
                    func()
                else:
                    temp=[a for a in self.Sql.Comandos if a.startswith(linea[0])]
                    self.Columnize(temp)  #}}}2

    def Salida(self,texto,modo=Normal):  #{{{2
        if modo == Normal:
            if self.ui.Resultados.textBackgroundColor() == Normal:
                self.ui.Resultados.setTextColor(Inverso)
            else:
                self.ui.Resultados.setTextColor(Normal)
        else:
            self.ui.Resultados.setTextColor(modo)
        self.ui.Resultados.insertPlainText(QtGui.qApp.trUtf8(texto))
        self.ui.Resultados.insertPlainText('\n')
        self.ui.Resultados.moveCursor(QtGui.QTextCursor.End)  #}}}2

    def Ejecutar(self):  #{{{2
        if self.ui.Etiqueta.text() == 'Usuario:':
            self.User = self.Comando.displayText()
            self.ui.Etiqueta.setText('Contraseña:')
            self.ui.Historia.clear()
            self.Comando.setEchoMode(QtGui.QLineEdit.NoEcho)
        elif self.ui.Etiqueta.text() == 'Contraseña:':
            self.Contrasena = self.ui.Historia.currentText()
            self.ui.Etiqueta.setText('Base de Datos:')
            self.ui.Historia.clear()
            self.Comando.setEchoMode(QtGui.QLineEdit.Normal)
            self.Sql.ejecutarDB_t('SHOW DATABASES')
            self.Sql.dbases = self.Sql.ejecutarDB_B('SHOW DATABASES')
        elif self.ui.Etiqueta.text() == 'Base de Datos:':
            self.Base = self.Comando.displayText()
            self.ui.Etiqueta.setText('Comandos MySql:')
            self.Sql.ejecutarDB_t('SHOW TABLES')
            self.Sql.tablas = self.Sql.ejecutarDB_B('SHOW TABLES')
            for a in self.Sql.tablas:
                self.Salida(a,Titulo)
                self.Sql.ejecutarDB_t('DESCRIBE %s' % a) 
            self.ui.Resultados.insertPlainText(self.Sql.help_HELP.__doc__)
            self.ui.Historia.clearEditText()
        elif self.ui.Etiqueta.text() == 'Comandos MySql:':
            self.EjecutarComando()
            self.ui.Historia.clearEditText()
        else:pass
              #}}}2

    def EjecutarComando(self):  #{{{2
        linea=str(self.Comando.displayText()).lower().split()
        if linea[0] in self.Sql.Comandos:
            self.Salida(self.Comando.displayText(),Normal)
            func = getattr(self.Sql,'do_'+linea[0].upper())
            func()
        else:
            self.Salida('Este comando no está implementado.',Error)  #}}}2

    def Columnize(self, list, color=Normal, displaywidth=80):  #{{{2
        """Display a list of strings as a compact set of columns.

    Each column is only as wide as necessary.
    Columns are separated by two spaces (one was not legible enough).
    """
        if not list:
            return
        nonstrings = [i for i in range(len(list))
                      if not isinstance(list[i], str)]
        if nonstrings:
            raise TypeError, ("list[i] not a string for i in %s" %
                              ", ".join(map(str, nonstrings)))
        size = len(list)
        if size == 1:
            self.Salida(str(list[0]),color)
            return
        # Try every row count from 1 upwards
        for nrows in range(1, len(list)):
            ncols = (size+nrows-1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows*col
                    if i >= size:
                        break
                    x = list[i]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break
        else:
            nrows = len(list)
            ncols = 1
            colwidths = [0]
        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows*col
                if i >= size:
                    x = ""
                else:
                    x = list[i]
                texts.append(x)
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            self.Salida(str('  '.join(texts)),color)  #}}}2
          #}}}1

App = MyApp()
sys.exit(App.exec_())
