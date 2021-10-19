import vtk
 
def makeActor(src):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(src.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor
 
def main():
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
 
    ren.AddActor(makeActor(vtk.vtkCylinderSource()))
 
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
