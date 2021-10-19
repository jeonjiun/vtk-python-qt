from types import TracebackType
import vtk

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

class Model:
    transforms = []
    actorTransforms = []
    actors = []
    angles = [0,0,0,0,0,0,0]

    def __init__(self):

        # link 0
        src = makeCylinderSource(0.3,1)
        tr = vtk.vtkTransform()
        tr.RotateZ(self.angles[0])

        trCyl = trCylinder(src,tr)
        act = makeActor(src,trCyl)

        self.transforms.append(tr)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 1
        trOld = tr
        src = makeCylinderSource(1,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,0.5)
        tr.RotateY(90)
        tr.Translate(0,0,-0.5)
        tr.RotateZ(self.angles[1])
        
        trCyl = trCylinder(src,tr)
        act = makeActor(src,trCyl)

        self.transforms.append(tr)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 2
        trOld = tr
        src = makeCylinderSource(1.5,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,0.5)
        tr.RotateZ(120)
        tr.Translate(0.7,0,0)
        tr.RotateY(90)
        tr.RotateZ(self.angles[2])
        
        trCyl = trCylinder(src,tr)
        act = makeActor(src,trCyl)

        self.transforms.append(tr)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 3
        trOld = tr
        src = makeCylinderSource(1,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,1.5)
        tr.RotateY(-90)
        tr.Translate(0,0,-0.5)
        tr.RotateZ(self.angles[3])
        
        trCyl = trCylinder(src,tr)
        act = makeActor(src,trCyl)

        self.transforms.append(tr)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 4
        trOld = tr
        src = makeCylinderSource(1.5,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,0.5)
        tr.RotateX(-90)
        tr.Translate(0,0,1)
        tr.RotateZ(self.angles[4])
        
        trCyl = trCylinder(src,tr)
        act = makeActor(src,trCyl)

        self.transforms.append(tr)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 5
        trOld = tr
        src = makeCylinderSource(1,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,1.5)
        tr.RotateX(-90)
        tr.Translate(0,0,-0.5)
        tr.RotateZ(self.angles[5])
        
        trCyl = trCylinder(src,tr)
        act = makeActor(src,trCyl)

        self.transforms.append(tr)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)

        # link 6
        trOld = tr
        src = makeCylinderSource(0.7,0.3)
        tr = vtk.vtkTransform()
        tr.SetInput(trOld)
        tr.Translate(0,0,0.5)
        tr.RotateY(-90)
        tr.RotateZ(self.angles[6])
        
        trCyl = trCylinder(src,tr)
        act = makeActor(src,trCyl)

        self.transforms.append(tr)
        self.actorTransforms.append(trCyl)
        self.actors.append(act)
    def setTransform(self, angles):

        for i in range(0,len(self.transforms)-1):
            self.angles[i] = angles[i]
            self.transforms[i].Identity()
            self.transforms[i].RotateZ(angles[i])

    def makeScene(self, render):
        
        for actor in self.actors:
            render.AddActor(actor)

        for tr in self.transforms:
            render.AddActor(makeAxesActor(tr))
        
        # for trCyl in self.actorTransforms:
        #     render.AddActor(makeAxesActor(trCyl))

g_myModel = Model()

def makeScene(render):
    g_myModel.makeScene(render)
 
def main():
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
 
    makeScene(ren)
 
    renWin.SetSize(300, 300)
    renWin.SetWindowName('Example')
 
    # This allows the interactor to initalize itself. It has to be
    # called before an event loop.
    iren.Initialize()
 
    # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # method on it.
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()
 
    # Start the event loop.
    iren.Start()
 
 
if __name__ == '__main__':
    main()
