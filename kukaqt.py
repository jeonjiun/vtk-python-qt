
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
    sliders = []
    model = None

    def __init__(self):
        super().__init__()
    
    def setModel(self, model):
        self.model = model

    def makeDialogControl(self, parentFrame):

        layout = QVBoxLayout()

        for i in range(0,6):
            slider = QSlider(Qt.Horizontal)
            slider.setRange(-180,180)
            slider.valueChanged.connect(self.sliderValueChanged)
            self.sliders.append(slider)
            layout.addWidget(QLabel('R{idx}:'.format(idx=i+1)))
            layout.addWidget(slider)
            
        layout.addItem(QSpacerItem(100,100,QSizePolicy.Minimum,QSizePolicy.Expanding))

        parentFrame.setLayout(layout)

    def sliderValueChanged(self, value):
        angles = []
        for slider in self.sliders:
            angles.append(slider.value())
        
        if self.model is not None:
            self.model.setTransform(angles)

        self.renWin.Render()


def makeAxesActor(tr = vtk.vtkTransform(), scale = 5):
    actor = vtk.vtkAxesActor()
    actor.SetUserTransform(tr)
    actor.AxisLabelsOff()
    actor.SetScale(scale)
    return actor


def makeActor(src, tr = vtk.vtkTransform()):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(src.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetUserTransform(tr)
    return actor

def makeCylinderSource(height, radius):
    src = vtk.vtkCylinderSource()
    src.SetHeight(height)
    src.SetRadius(radius)
    src.SetResolution(30)
    return src

def trCylinder(src, trInput = vtk.vtkTransform()):
    tr = vtk.vtkTransform()
    tr.SetInput(trInput)
    tr.Identity()
    tr.Translate(0,0,src.GetHeight()*0.5)
    tr.RotateX(90)
    return tr

class KukaModel:
    transforms = []
    actorTransforms = []
    actors = []
    angles = [0,0,0,0,0,0,0]

    def __init__(self):

        # link 0
        src = makeCylinderSource(0.3,1)
        tr = vtk.vtkTransform()
        trm = vtk.vtkTransform()
        trm.SetInput(tr)
        trm.RotateZ(self.angles[0])

        trCyl = trCylinder(src,trm)
        act = makeActor(src,trCyl)

        self.transforms.append(trm)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 1
        trOld = trm
        src = makeCylinderSource(1,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,0.5)
        tr.RotateY(90)
        tr.Translate(0,0,-0.5)
        
        trm = vtk.vtkTransform()
        trm.SetInput(tr)
        trm.RotateZ(self.angles[1])
        
        trCyl = trCylinder(src,trm)
        act = makeActor(src,trCyl)

        self.transforms.append(trm)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 2
        trOld = trm
        src = makeCylinderSource(1.5,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,0.5)
        tr.RotateZ(120)
        tr.Translate(0.7,0,0)
        tr.RotateY(90)
        
        trm = vtk.vtkTransform()
        trm.SetInput(tr)
        trm.RotateZ(self.angles[2])
        
        trCyl = trCylinder(src,trm)
        act = makeActor(src,trCyl)

        self.transforms.append(trm)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 3
        trOld = trm
        src = makeCylinderSource(1,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,1.5)
        tr.RotateY(-90)
        tr.Translate(0,0,-0.5)

        
        trm = vtk.vtkTransform()
        trm.SetInput(tr)
        trm.RotateZ(self.angles[3])

        trCyl = trCylinder(src,trm)
        act = makeActor(src,trCyl)

        self.transforms.append(trm)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 4
        trOld = trm
        src = makeCylinderSource(1.5,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,0.5)
        tr.RotateX(-90)
        tr.Translate(0,0,1)

        
        trm = vtk.vtkTransform()
        trm.SetInput(tr)
        trm.RotateZ(self.angles[4])
        
        trCyl = trCylinder(src,trm)
        act = makeActor(src,trCyl)

        self.transforms.append(trm)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 5
        trOld = trm
        src = makeCylinderSource(1,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,1.5)
        tr.RotateX(-90)
        tr.Translate(0,0,-0.5)

        trm = vtk.vtkTransform()
        trm.SetInput(tr)
        trm.RotateZ(self.angles[5])
        
        trCyl = trCylinder(src,trm)
        act = makeActor(src,trCyl)

        self.transforms.append(trm)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 6
        trOld = trm
        src = makeCylinderSource(0.7,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,0.5)
        tr.RotateY(-90)
        
        trm = vtk.vtkTransform()
        trm.SetInput(tr)
        trm.RotateZ(self.angles[6])

        trCyl = trCylinder(src,trm)
        act = makeActor(src,trCyl)

        self.transforms.append(trm)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)


    def setTransform(self, angles):

        for i in range(0,len(self.transforms)-1):
            self.angles[i] = angles[i]
            self.transforms[i].Identity()
            self.transforms[i].RotateZ(angles[i])
            self.transforms[i].Update()

    def makeScene(self, render):
        
        for actor in self.actors:
            render.AddActor(actor)

        for tr in self.transforms:
            render.AddActor(makeAxesActor(tr))
        
        render.ResetCamera()
        render.Render()

def main():
    app = QApplication(sys.argv)

    dlg = MyDialog()
    model = KukaModel()
    model.makeScene(dlg.getRenderer())

    dlg.setModel(model)
    
    dlg.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
