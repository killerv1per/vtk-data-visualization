import vtk as vtk

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Isabel_2D.vti")
reader.Update()

image = reader.GetOutput()

print("Enter Isovalue :")
isoval = float(input())

dims = image.GetDimensions()
val = image.GetPointData().GetScalars()

global_points = vtk.vtkPoints()
global_lines = vtk.vtkCellArray()
for j in range(dims[1] - 1):
    for i in range(dims[0] - 1):
        intersection_points = []
        p0 = j*(dims[0]) + i
        p1 = p0 + 1
        p2 = p1 + dims[0]
        p3 = p2 - 1
        
        s0 = val.GetTuple1(p0)
        s1 = val.GetTuple1(p1)
        s2 = val.GetTuple1(p2)
        s3 = val.GetTuple1(p3)

        pt0 = image.GetPoint(p0)
        pt1 = image.GetPoint(p1)
        pt2 = image.GetPoint(p2)
        pt3 = image.GetPoint(p3)

        if (s0 <= isoval < s1) or (s1 <= isoval < s0):
            t = (isoval - s0) / (s1 - s0)
            x = pt0[0] + t * (pt1[0] - pt0[0])
            y = pt0[1] + t * (pt1[1] - pt0[1])
            z = pt0[2]
            intersection_points.append((x, y, z))

        if (s1 <= isoval < s2) or (s2 <= isoval < s1):
            t = (isoval - s1) / (s2 - s1)
            x = pt1[0] + t * (pt2[0] - pt1[0])
            y = pt1[1] + t * (pt2[1] - pt1[1])
            z = pt1[2]
            intersection_points.append((x, y, z))

        if (s2 <= isoval < s3) or (s3 <= isoval < s2):
            t = (isoval - s2) / (s3 - s2)
            x = pt2[0] + t * (pt3[0] - pt2[0])
            y = pt2[1] + t * (pt3[1] - pt2[1])
            z = pt2[2]
            intersection_points.append((x, y, z))

        if (s3 <= isoval < s0) or (s0 <= isoval < s3):
            t = (isoval - s3) / (s0 - s3)
            x = pt3[0] + t * (pt0[0] - pt3[0])
            y = pt3[1] + t * (pt0[1] - pt3[1])
            z = pt3[2]
            intersection_points.append((x, y, z))

        if len(intersection_points) == 2:
            line = vtk.vtkLine()
            id0 = global_points.InsertNextPoint(intersection_points[0])
            id1 = global_points.InsertNextPoint(intersection_points[1])
            line.GetPointIds().SetId(0, id0)
            line.GetPointIds().SetId(1, id1)
            global_lines.InsertNextCell(line)

        elif len(intersection_points) == 4:
            line1 = vtk.vtkLine()
            id0 = global_points.InsertNextPoint(intersection_points[0])
            id1 = global_points.InsertNextPoint(intersection_points[1])
            line1.GetPointIds().SetId(0, id0)
            line1.GetPointIds().SetId(1, id1)
            global_lines.InsertNextCell(line1)
            
            line2 = vtk.vtkLine()
            id2 = global_points.InsertNextPoint(intersection_points[2])
            id3 = global_points.InsertNextPoint(intersection_points[3])
            line2.GetPointIds().SetId(0, id2)
            line2.GetPointIds().SetId(1, id3)
            global_lines.InsertNextCell(line2)

polyData = vtk.vtkPolyData()
polyData.SetPoints(global_points)
polyData.SetLines(global_lines)

writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("Output.vtp") 
writer.SetInputData(polyData)
writer.Write()

print("Isocontour successfully saved as Output.vtp")
