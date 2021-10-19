import vtk
 
def makeActor(src):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(src.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor
 
def makeScene(render):
    src = vtk.vtkSTLReader()
    src.SetFileName('d:/ghost.stl')
    render.AddActor(makeActor(src))
    
def main():
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
 
    # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # method on it.
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()
 
    # Start the event loop.
    iren.Start()
 
 
if __name__ == '__main__':
    main()


def makeScene(render):
  src = vtk.vtkSphereSource()
  render.AddActor(makeActor(src))


def makeScene(render):
    src = vtk.vtkConeSource()
    src.SetResolution(120)
    src.SetAngle(60)
    render.AddActor(makeActor(src))


def makeScene(render):
    src = vtk.vtkSTLReader()
    src.SetFileName('d:/ghost.stl')
    actor = makeActor(src)
    actor.GetProperty().SetColor(1.0,1.0,0.0)
    render.AddActor(actor)

