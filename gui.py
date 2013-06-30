from PySide import QtGui,QtCore

import numpy as np
import engine
from new_game import Ui_NewGameDialog
from about import Ui_AboutDialog

class EngineThread(QtCore.QObject):
    searchFinished = QtCore.Signal(str)
    def __init__(self,state):
        QtCore.QObject.__init__(self)
        self.state = state
    @QtCore.Slot()
    def findMove(self):
        move = engine.find_move(self.state)
        self.searchFinished.emit(move)

class BoardScene(QtGui.QGraphicsScene):
    def __init__(self,board):
        QtGui.QGraphicsScene.__init__(self)        
        self.board = board
    def mouseReleaseEvent(self,mouseEvent):
        pos = mouseEvent.scenePos()
        if(engine.winner(self.board.state) != 0):
            return
        if(np.sum(self.board.state['board'] == 0) == 0):
            return
        if(self.board.state['to_move'] != self.board.state['computer']):
            self.board.humanMove(int(pos.y()),int(pos.x()))

class TTTBoard(QtGui.QMainWindow):
    findMove = QtCore.Signal()
    def __init__(self,depth):
        QtGui.QMainWindow.__init__(self)        
        # Add menu
        self.gameMenu = self.menuBar().addMenu(self.tr("&Game"));
        self.newGame = QtGui.QAction("New",self)
        self.aboutGame = QtGui.QAction("About",self)
        self.gameMenu.addAction(self.newGame)
        self.gameMenu.addAction(self.aboutGame)
        self.newGame.triggered.connect(self.restartGame)
        self.aboutGame.triggered.connect(self.showAbout)
        self.scene = BoardScene(self)
        self.scene.setSceneRect(0,0,9,9);
        self.board = QtGui.QGraphicsView(self.scene,self)
        self.board.setRenderHints(QtGui.QPainter.Antialiasing)
        self.setCentralWidget(self.board)        
        self.resize(800,800)

        settings = QtCore.QSettings()
        if(settings.contains("geometry")):
            self.restoreGeometry(settings.value("geometry"));
        if(settings.contains("windowState")):
            self.restoreState(settings.value("windowState"));
        self.startGame(depth=depth)
    def closeEvent(self,event):
        settings = QtCore.QSettings()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        QtGui.QMainWindow.closeEvent(self,event)
    def drawBoard(self):
        self.scene.clear()
        if(engine.winner(self.state) == 0):
            # draw focus
            if(self.state['to_move'] == 1):
                focusBrush = QtGui.QBrush(QtGui.QColor(255,200,200))
            else:
                focusBrush = QtGui.QBrush(QtGui.QColor(200,200,255))
            if(np.all(self.state['focus'] == 1)):
                self.scene.addRect(0,0,9,9,QtGui.QPen(),focusBrush)
            else:
                focus = np.where(self.state['focus'][::3,::3] == 1)
                self.scene.addRect(focus[1][0]*3,focus[0][0]*3,3,3,
                                   QtGui.QPen(),focusBrush)
            # draw last move
            if(self.state['last_move']):
                if(self.state['to_move'] == 1):                
                    lastMoveBrush = QtGui.QBrush(QtGui.QColor(200,200,255))
                else:
                    lastMoveBrush = QtGui.QBrush(QtGui.QColor(255,200,200))
                r = self.state['last_move'][0]
                c = self.state['last_move'][1]
                self.scene.addRect(c,r,1,1,
                                   QtGui.QPen(),lastMoveBrush)


        # draw lines
        pen = QtGui.QPen()
        pen.setWidthF(0.02)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        thickPen = QtGui.QPen(pen)
        thickPen.setWidthF(0.08)        
        for c in range(0,10):
            if(c % 3):
                self.scene.addLine(c,0,c,9,pen)
            else:
                self.scene.addLine(c,0,c,9,thickPen)
        for r in range(0,10):
            if(r % 3):
                self.scene.addLine(0,r,9,r,pen)
            else:
                self.scene.addLine(0,r,9,r,thickPen)
        # draw symbols
        for r in range(0,9):
            for c in range(0,9):
                if(self.state['finished'][r,c] == 0):
                    self.drawSymbol(r,c,self.state['board'][r,c])
                else:
                    if(r%3 == 0 and c%3 == 0):
                        self.drawSymbol(r,c,self.state['finished'][r,c],size=3)
              
        if(engine.winner(self.state)):
            winner,line = engine.winner(self.state,line=True)
            pen = QtGui.QPen()
            pen.setWidthF(0.15)
            pen.setCapStyle(QtCore.Qt.RoundCap)

            self.scene.addLine(3*line[0][1]+1.5,3*line[0][0]+1.5,
                               3*line[2][1]+1.5,3*line[2][0]+1.5,pen)
            
    def drawSymbol(self,row,col,player,size=1):
        if(player == 0):
            return
        if(player == 1):
            pen = QtGui.QPen(QtGui.QColor(255,0,0))
            pen.setWidthF(0.05*size)
            pen.setCapStyle(QtCore.Qt.RoundCap)
            margin = 0.15*size
            self.scene.addLine(col+margin,row+margin,
                               col+size-margin,row+size-margin,pen)
            self.scene.addLine(col+margin,row+size-margin,
                               col+size-margin,row+margin,pen)
        if(player == 2):
            pen = QtGui.QPen(QtGui.QColor(0,0,255))
            pen.setCapStyle(QtCore.Qt.RoundCap)
            pen.setWidthF(0.05*size)
            margin = 0.12*size
            self.scene.addEllipse(col+margin,row+margin,
                                  size-2*margin,size-2*margin,pen)


    def play(self):
        self.drawBoard()
        QtCore.QCoreApplication.instance().processEvents()
        if(np.sum(self.state['board'] == 0) == 0):
            msg = QtGui.QMessageBox(QtGui.QMessageBox.NoIcon,"Game Drawn",
                              "It's a draw!", QtGui.QMessageBox.Ok)
            self.statusBar().showMessage('Game ends in draw.',5000)
            msg.exec_()
            return
        if(engine.winner(self.state) == self.state['computer']):
            msg = QtGui.QMessageBox(QtGui.QMessageBox.NoIcon,"Computer Wins",
                              "I won the game!", QtGui.QMessageBox.Ok)
            self.statusBar().showMessage('Computer wins the game.',500)
            msg.exec_()
            return
        elif(engine.winner(self.state)):
            msg = QtGui.QMessageBox(QtGui.QMessageBox.NoIcon,"Player Wins",
                              "You won the game!", QtGui.QMessageBox.Ok)
            self.statusBar().showMessage('You win the game.',5000)
            msg.exec_()
            return

        while(engine.winner(self.state) == 0):
            self.drawBoard()
            if(self.state['to_move'] != self.state['computer']):
                self.statusBar().showMessage('Player turn')
                return
            else:
                self.statusBar().showMessage('Computer turn. Thinking...')
                self.findMove.emit()
                return

    def humanMove(self,row,col):
        move = engine.row_col_to_pos(row,col)
        valid,msg = engine.valid_move(self.state,move,verbose=False,
                                      returnMessage=True)
        if(valid):
            engine.make_move(self.state,move)
            self.play()
        else:
            self.statusBar().showMessage(msg,5000)
    def computerMove(self,move):
        engine.make_move(self.state,move)
        self.play()
    def resizeEvent(self,event):
        QtGui.QMainWindow.resizeEvent(self,event)
        margin = 40
        side = min(self.board.height(),self.board.width())
        scale = (side-margin)/9
        transform = QtGui.QTransform (scale, 0, 0, scale, 0, 0 )
        self.board.setTransform(transform)
    def startGame(self,depth,firstMove=0,players=1):
        self.state = engine.init(depth,computer=firstMove,humans=players)
        if(players == 1):
            self.engineThread = EngineThread(self.state)
            self.findMove.connect(self.engineThread.findMove)
            self.engineThread.searchFinished.connect(self.computerMove)
            self.threadHandle = QtCore.QThread()
            self.engineThread.moveToThread(self.threadHandle)
            self.threadHandle.start()
        self.play()
    def restartGame(self,first=False):
        dialog = QtGui.QDialog(self)
        ui = Ui_NewGameDialog()
        ui.setupUi(dialog)
        ret = dialog.exec_()
        if(ret):
            if(not first):
                self.threadHandle.terminate()
            toMove = 0
            if(ui.computerRadio.isChecked()):
                toMove = 1
            if(ui.playerRadio.isChecked()):
                toMove = 2
            nPlayers = 1
            if(ui.vsPlayerRadio.isChecked()):
                nPlayers = 2
            self.startGame(depth=ui.depthSlider.value(),firstMove=toMove,
                           players=nPlayers)
    def showAbout(self):
        dialog = QtGui.QDialog(self)
        ui = Ui_AboutDialog()
        ui.setupUi(dialog)
        ret = dialog.exec_()
        
        
def init_gui(argv,depth):
    QtCore.QCoreApplication.setApplicationName("Ultimate TTT");
    app = QtGui.QApplication(argv)
    aw = TTTBoard(depth)
    aw.show()
    ret = app.exec_()
    while(aw.threadHandle.isRunning()):
        aw.threadHandle.terminate()
    
