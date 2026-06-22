import vtk as vtk

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Isabel_3D.vti")
reader.Update()

ctf = vtk.vtkColorTransferFunction()
ctf.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0) 
ctf.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0) 
ctf.AddRGBPoint(-1873.9,  0.0, 0.0, 0.5) 
ctf.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0) 
ctf.AddRGBPoint(-298.031, 1.0, 0.4, 0.0) 
ctf.AddRGBPoint(2594.97,  1.0, 1.0, 0.0) 

otf = vtk.vtkPiecewiseFunction()
otf.AddPoint(-4931.54, 1.0)
otf.AddPoint(101.815,  0.002)
otf.AddPoint(2594.97,  0.0)

vprop = vtk.vtkVolumeProperty()
vprop.SetColor(ctf)
vprop.SetScalarOpacity(otf)

vprop.SetInterpolationTypeToLinear()

vmpr = vtk.vtkSmartVolumeMapper()
vmpr.SetInputConnection(reader.GetOutputPort())
volume = vtk.vtkVolume()
volume.SetMapper(vmpr)
volume.SetProperty(vprop)

outln = vtk.vtkOutlineFilter()
outln.SetInputConnection(reader.GetOutputPort())

outlnmpr = vtk.vtkPolyDataMapper()
outlnmpr.SetInputConnection(outln.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(outlnmpr)

print("Enable Phong shading? (yes/no) ")
a = input().strip().lower()

if a == 'yes':
    vprop.ShadeOn()
    vprop.SetAmbient(0.5)
    vprop.SetDiffuse(0.5)
    vprop.SetSpecular(0.5)
else:
    vprop.ShadeOff()

rndr = vtk.vtkRenderer()
rndr.AddVolume(volume)
rndr.AddActor(actor)
rndr.SetBackground(1.0, 1.0, 1.0) 

rndrw = vtk.vtkRenderWindow()
rndrw.AddRenderer(rndr)
rndrw.SetSize(1000, 1000)
rndrw.SetWindowName("Assignment 1: 3D Volume Rendering")
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(rndrw)
rndrw.Render()
interactor.Initialize()
interactor.Start()