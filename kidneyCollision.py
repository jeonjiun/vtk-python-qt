from pyparsing import null_debug_action
import vtk

camera = vtk.vtkCamera()
trObject = vtk.vtkTransform()
trCamera = vtk.vtkTransform()
trCamera.SetInput(trObject)
trCamera.Translate(0,-2,2)

trFocus = vtk.vtkTransform()
trFocus.SetInput(trObject)
trFocus.Translate(0,0,1)

g_collide = None
g_envActors = []

def makeActor(src):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(src.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

def makeActorFromPort(port):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(port)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

class MyKeyPressInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
#class MyKeyPressInteractorStyle(vtk.vtkInteractorStyleUser):
    def __init__(self, parent=None):
        print('init interactor style')
        self.AddObserver('KeyPressEvent',self.keyPressEvent)
    
    def keyPressEvent(self, obj, event):
        interactor = self.GetInteractor()
        key = interactor.GetKeySym()
        
        oldCollision = g_collide.GetNumberOfContacts() > 0
        oldTr = vtk.vtkTransform()
        oldTr.DeepCopy(trObject)
        
        step = 1
        
        if key == 'z':
            trObject.Translate(0,step,0)
        elif key == 'x':
            trObject.Translate(0,-step,0)
        elif key == 'Left':
            trObject.RotateZ(5)
        elif key == 'Right':
            trObject.RotateZ(-5)
        elif key == 'Up':
            trObject.RotateX(5)
        elif key == 'Down':
            trObject.RotateX(-5)
        elif key == 'space':
            trObject.Translate(0, step,0)
        else:
            print(key)
            
        trObject.Update()
        g_collide.Update()
        
        newCollision = g_collide.GetNumberOfContacts() > 0
        
        if oldCollision and newCollision:
            print('collision')
            trObject.DeepCopy(oldTr)
            
      
        resetCamera(self.GetDefaultRenderer())
        
        self.GetDefaultRenderer().GetRenderWindow().Render()
                
        return
    

def makeFloor(rend):
    append = vtk.vtkAppendPolyData()
    
    maxv = 100
    for i in range(-100,100):
        v = i * 10
        vline = vtk.vtkLineSource()
        vline.SetPoint1(v, -maxv, 0)
        vline.SetPoint2(v,  maxv, 0)
        
        hline = vtk.vtkLineSource()
        hline.SetPoint1(-maxv, v, 0)
        hline.SetPoint2( maxv, v, 0)
        
        append.AddInputConnection(vline.GetOutputPort())
        append.AddInputConnection(hline.GetOutputPort())
    
    
    actor = makeActor(append)
    actor.GetProperty().SetColor(0.2,0.7,0.2)
    actor.GetProperty().SetOpacity(0.5)
    g_envActors.append(actor)
    rend.AddActor(actor)

def makeKidney(rend, collide, portNum):
    reader = vtk.vtkSTLReader()
    reader.SetFileName('d:/kidney.stl')      
    
    tr = vtk.vtkTransform()
    
    collide.SetInputConnection(portNum,reader.GetOutputPort())
    collide.SetTransform(portNum, tr)
    
    actor = makeActorFromPort(collide.GetOutputPort(portNum))
    actor.SetUserTransform(tr)
    
    rend.AddActor(actor)

init = False

def resetCamera(rend):
    global init
    
    for o in g_envActors:
        o.SetVisibility(False)

    if init == False:
        rend.ResetCamera()
        init = True
    else:
        cam = rend.GetActiveCamera()
        cam.SetPosition(trCamera.GetPosition())
        cam.SetFocalPoint(trFocus.GetPosition())
        dx = trObject.GetMatrix().GetElement(0,2)
        dy = trObject.GetMatrix().GetElement(1,2)
        dz = trObject.GetMatrix().GetElement(2,2)
        cam.SetViewUp(dx,dy,dz)
        rend.ResetCameraClippingRange()
    
    for o in g_envActors:
        o.SetVisibility(True)
    
def makeObject(rend, collide, portNum):
    
    src = vtk.vtkCylinderSource()
    src.SetHeight(2)
    
    collide.SetInputConnection(portNum,src.GetOutputPort())
    collide.SetTransform(portNum, trObject)
    
    cylinderActor = makeActorFromPort(collide.GetOutputPort(portNum))
    cylinderActor.SetUserTransform(trObject)
    
    #cylinderActor.GetProperty().SetRepresentationToWireframe()
    
    rend.AddActor(cylinderActor)
    
def makeScene(rend):
    global g_collide
    
    collide = vtk.vtkCollisionDetectionFilter()
    # collide.SetInputConnection(0, reader.GetOutputPort())
    # collide.SetTransform(0, trSTL)
    # collide.SetInputConnection(1, src.GetOutputPort())
    # collide.SetTransform(1, trObject)
    collide.SetBoxTolerance(0.0)
    collide.SetCellTolerance(0.0)
    collide.SetNumberOfCellsPerNode(2)
    collide.SetCollisionModeToAllContacts()
    collide.GenerateScalarsOn()
    
    g_collide = collide
    
    makeFloor(rend)
    makeKidney(rend, collide, 0)
    makeObject(rend, collide, 1)
        
    g_camActor = vtk.vtkCameraActor()
    g_camActor.SetCamera(camera)
    
    rend.AddActor(g_camActor)
    
    g_envActors.append(g_camActor)
    
    axes = vtk.vtkAxesActor()
    axes.AxisLabelsOff()
    axes.SetUserTransform(trObject)
    rend.AddActor(axes)
    
    
    
def main():
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    #iren.SetInteractorStyle(vtk.vtkInteractorStyleFlight())
    istyle = MyKeyPressInteractorStyle()
    istyle.SetDefaultRenderer(ren)
    iren.SetInteractorStyle(istyle)
    iren.SetRenderWindow(renWin)
 
 
 
    makeScene(ren)
 
    renWin.SetSize(300, 300)
    renWin.SetWindowName('CylinderExample')
 
    # This allows the interactor to initalize itself. It has to be
    # called before an event loop.
    iren.Initialize()
 
    # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # method on it.
        
    if 1:
        #ren.ResetCamera()
        #ren.GetActiveCamera().Zoom(1.5)
        
        resetCamera(ren)
        ren.GetActiveCamera().SetViewAngle(50)
        
        camera.DeepCopy(ren.GetActiveCamera())
        
        
    else:
        ren.SetActiveCamera(camera)
    
    renWin.Render()
 
    # Start the event loop.
    iren.Start()
 
 
if __name__ == '__main__':
    main()
