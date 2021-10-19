import vtk

def makeAxesActor(tr = vtk.vtkTransform(), scale = 5):
    actor = vtk.vtkAxesActor()
    actor.SetUserTransform(tr)
    actor.AxisLabelsOff()
    actor.SetScale(scale)
    return actor


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
    length = 5
    
    tr1 = vtk.vtkTransform()
    tr2 = vtk.vtkTransform()
    tr3 = vtk.vtkTransform()
 
    tr1.RotateX(30)
    
    tr2.SetInput(tr1)
    tr2.Translate(0,0,length)    
    tr2.RotateX(-30)
 
    tr3.SetInput(tr2)
    tr3.Translate(0,0,length)
    tr3.RotateX(30)
    
    src = vtk.vtkCylinderSource()
    src.SetHeight(length)
 
    srcLong = vtk.vtkCylinderSource()
    srcLong.SetHeight(length*2)
 
    arm1 = makeActor(src)
    arm2 = makeActor(src)
    arm3 = makeActor(srcLong)
 
    tr1act = trCylinder(src)
    tr2act = trCylinder(src)
    tr3act = trCylinder(srcLong)
    tr1act.SetInput(tr1)
    tr2act.SetInput(tr2)
    tr3act.SetInput(tr3)
    
    arm1.SetUserTransform(tr1act)
    arm2.SetUserTransform(tr2act)
    arm3.SetUserTransform(tr3act)
 
    arm1.GetProperty().SetColor(1,1,0)
    arm3.GetProperty().SetColor(0,1,1)
    render.AddActor(arm1)
    render.AddActor(arm2)
    render.AddActor(arm3)

    render.AddActor(makeAxesActor(tr1))
    render.AddActor(makeAxesActor(tr2))
    render.AddActor(makeAxesActor(tr3))

    render.AddActor(makeAxesActor(tr1act))
    render.AddActor(makeAxesActor(tr2act))
    render.AddActor(makeAxesActor(tr3act))
 
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
