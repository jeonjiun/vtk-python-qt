
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import sys

class DialogVTKFrame(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint )

        self.leftFrame = QFrame()
        self.rightFrame = QFrame()

        self.leftFrame.setMaximumWidth(300)

        self.makeRenderer(self.rightFrame)
        self.makeDialogControl(self.leftFrame)        

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.leftFrame)
        hlayout.addWidget(self.rightFrame)
        self.setLayout(hlayout)

    def makeDialogControl(self, parentFrame):
        
        slider = QSlider(Qt.Horizontal)

        #layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Translation:"))
        layout.addWidget(slider)
        layout.addItem(QSpacerItem(100,100,QSizePolicy.Minimum,QSizePolicy.Expanding))

        parentFrame.setLayout(layout)

    def makeRenderer(self, frame):
        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(frame)
        self.vl.addWidget(self.vtkWidget)

        # Create the graphics structure. The renderer renders into the render
        # window. The render window interactor captures mouse events and will
        # perform appropriate camera or actor manipulation depending on the
        # nature of the events.
        self.ren = vtk.vtkRenderer()

        self.renWin = self.vtkWidget.GetRenderWindow()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        frame.setLayout(self.vl)
   
        # This allows the interactor to initalize itself. It has to be
        # called before an event loop.
        self.iren.Initialize()

        self.ren.ResetCamera()
        self.renWin.Render()

    
    def getRenderer(self):
        return self.ren

class MyDialog(DialogVTKFrame):
    def __init__(self):
        super().__init__()
    
    def makeDialogControl(self, parentFrame):
        slider = QSlider(Qt.Horizontal)
        slider.valueChanged.connect(self.slider_valChanged)

        self.editbox = QLineEdit("Edit box")

        pushbutton = QPushButton("button")
        pushbutton.clicked.connect(self.pushbutton_clicked)

        checkbox = QCheckBox("CheckBox")
        checkbox.stateChanged.connect(self.checkbox_changed)

        #layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Translation:"))
        layout.addWidget(slider)
        layout.addWidget(self.editbox)
        layout.addWidget(pushbutton)
        layout.addWidget(checkbox)
        layout.addItem(QSpacerItem(100,100,QSizePolicy.Minimum,QSizePolicy.Expanding))

        parentFrame.setLayout(layout)

    def slider_valChanged(self, val):
        print(val)

    def pushbutton_clicked(self):
        print(self.editbox.text())

    def checkbox_changed(self,state):
        if state == Qt.Checked:
            print('checked')
        else:
            print('unchecked')


class MyModel:
    actors = []

    def __init__(self):
        src = vtk.vtkConeSource()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(src.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.actors.append(actor)
        
    def setTransform(self, angles):
        self.actors[0].RotateX(angles)

    def makeScene(self, render):
        for actor in self.actors:
            render.AddActor(actor)

def main():
    app = QApplication(sys.argv)

    dlg = MyDialog()
    model = MyModel()
    model.makeScene(dlg.getRenderer())
    
    dlg.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
