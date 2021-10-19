import vtk
import math
 
length = 5
    
def makeActor(src):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(src.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor
 
def trCylinder(src):
    tr = vtk.vtkTransform()
    tr.Identity()
    tr.Translate(0,0,src.GetHeight()*0.5)
    tr.RotateX(90)
    return tr
 
def makeScene(render):
    global tr1
    global tr2
    global tr3
    
    tr1 = vtk.vtkTransform()
    tr2 = vtk.vtkTransform()
    tr3 = vtk.vtkTransform()
 
    tr1.RotateX(30)
    
    tr2.SetInput(tr1)
    tr2.Translate(0,0,length*2)    
    tr2.RotateX(0)
 
    tr3.SetInput(tr2)
    tr3.Translate(0,0,length*2)
    tr3.RotateX(0)
    
    src = vtk.vtkCylinderSource()
    src.SetHeight(length)
 
    srcLong = vtk.vtkCylinderSource()
    srcLong.SetHeight(length*2)
 
    arm1 = makeActor(src)
    arm2 = makeActor(srcLong)
    arm3 = makeActor(srcLong)
 
    tr1act = trCylinder(src)
    tr2act = trCylinder(srcLong)
    tr3act = trCylinder(srcLong)
    tr1act.SetInput(tr1)
    tr2act.SetInput(tr2)
    tr3act.SetInput(tr3)
    
    arm1.SetUserTransform(tr1act)
    arm2.SetUserTransform(tr2act)
    arm3.SetUserTransform(tr3act)
 
    arm1.GetProperty().SetColor(1,1,0)
    arm2.GetProperty().SetColor(0,1,1)
    render.AddActor(arm1)
    render.AddActor(arm2)
    render.AddActor(arm3)

    render.AddActor(makeActor(vtk.vtkSphereSource()))
 
    centerTr = vtk.vtkTransform()
    centerTr.RotateZ(90)
    centerSrc = vtk.vtkCylinderSource()
    centerSrc.SetRadius(6)
    centerSrc.SetResolution(120)
    centerSrc.SetHeight(0.5)
    center = makeActor(centerSrc)
    center.SetUserTransform(centerTr)
    center.GetProperty().SetColor(0.2,0.2,0.6)
    render.AddActor(center)

class MyTimer(object):
    i = 0
    
    def __init__(self,tr1,tr2,tr3,ren):
        super().__init__()
        self.set(tr1,tr2,tr3)
        self.ren = ren
 
    def set(self,tr1, tr2, tr3):
        self.tr1 = tr1
        self.tr2 = tr2
        self.tr3 = tr3
 
    def a(self,a_deg):
        alpha = math.radians(a_deg)
        sin_a = math.sin(alpha)
        beta = math.acos(sin_a*0.5)
        beta_deg = math.degrees(beta)
        res = -180+(90-a_deg+beta_deg)
        return res
 
    def __call__(self, caller, ev):
        self.i = self.i + 5
        if self.i >= 360:
            self.i -= 360
 
        res = self.a(self.i)
        
        self.tr1.Identity()
        self.tr1.RotateX(self.i)
        self.tr2.Identity()
        self.tr2.Translate(0,0,5)
        self.tr2.RotateX(res)
        self.tr3.Identity()
        self.tr3.Translate(0,0,10)
        self.tr3.RotateX(-(res+self.i))
        
        self.tr1.Update()
        self.tr2.Update()
        self.tr3.Update()
        
        self.ren.Render()
        print(res)

def main():
    global tr1
    global tr2
    global tr3
    
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
 
    makeScene(ren)
 
    renWin.SetSize(300, 300)
    renWin.SetWindowName('CylinderExample')
 
    # This allows the interactor to initalize itself. It has to be
    # called before an event loop.
    iren.Initialize()
 
    # start timer
    iren.AddObserver('TimerEvent',MyTimer(tr1,tr2,tr3,renWin))
    iren.CreateRepeatingTimer(30)
 
    cam = ren.GetActiveCamera()
    cam.SetPosition(30,0,10)
    cam.SetFocalPoint(0,0,10)
    cam.SetViewUp(0,0,1)
    cam.SetClippingRange(100,300)
    ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()
 
    # Start the event loop.
    iren.Start()
 
 
if __name__ == '__main__':
    main()
