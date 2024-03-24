"""Converts a 2D topographic map to a 3D model.
    Inputs:
        vertical_offset: A boolean toggle that moves all contour lines in z axis based on its associated value
        contour_input: Geometry pipeline that should be set for only Curves
        mesh_formation: A boolean toggle that creates a delaunay mesh over elevated contours
        smoothness: A number slider that helps control the smoothness of mesh
    Output:
        elevated_contours: The final displaced contours
        final_mesh: The 3D topographic model"""
                
__author__ = "cm_adithya"
                
import Rhino
import ghpythonlib.components as gh
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
                        
# Access the Rhino document
doc = Rhino.RhinoDoc.ActiveDoc
                        
# Getting all objects in the Rhino document
all_objects = doc.Objects.GetObjectList(Rhino.DocObjects.ObjectType.Annotation)
                        
# Initializing a list to store points and points
text_contents = []
points = []
                        
# Iterating through all objects in the Rhino document
for obj in all_objects:
                            
    # Checking if the object is a text entity
    if isinstance(obj.Geometry, Rhino.Geometry.TextEntity):
                                
        # Extracting text content of the object
        text = obj.Geometry.Text
        text_contents.append(text)
                                
        # Getting the bounding box of the text
        bbox = obj.Geometry.GetBoundingBox(True)
                                
                                
        # Calculating the lengths of both sides of the bounding box
        x_length = bbox.Max.X - bbox.Min.X
        y_length = bbox.Max.Y - bbox.Min.Y
                                
                                
        # Determining the longer side of the bounding box
        text_width = max(x_length, y_length)
                                
                                
        # Getting the insertion point of the text entity
        insertion_point = obj.Geometry.Plane.Origin
                                
                                
        # Creating points on either side of the text
        left_point = insertion_point + obj.Geometry.Plane.XAxis * text_width
        right_point = insertion_point - obj.Geometry.Plane.XAxis 
                                
                                
        # Appending the points to the list of points
        points.append(left_point)
        points.append(right_point)
                        
d = text_contents 
                        
# Initializing list to store closest curve IDs
b = []
                        
# Iterating through each point in 'contour_input'
for pt in points:
    # Finding the closest curve to the current point
    closest_curve = rs.PointClosestObject(pt, contour_input)
                            
                            
    # Appending the ID of the closest curve to the list 'b'
    if closest_curve:
        b.append(closest_curve[0])  
                                
                        
e = []
                        
# Assuming 'vertical_offset' is the toggle input
                        
if not vertical_offset:
    for integer in d:
        e.append(float(integer))
                        
max_level = max(e)
min_level = min(e)
                        
# Normalizing levels between zero and 1 
                        
last_levels = []
                        
for figure in e:
                            
                            
    final_value = figure - min_level
    last_levels.append(final_value)
                            
                        
f = []
                        
# Iterating over each element in the list
for value in last_levels:
    # Create a 3D vector with (0, 0, value) and append it to the list
    vector = rg.Vector3d(0, 0, value)
    f.append(vector)
                        
# Moving all curves up
moved_curves = []
                        
processed_curves = set()
                        
# Iterating through pairs of elements from b and f
for i in range(0, len(b), 2):  
    curve_pair = b[i:i+2]
    movement_vector = f[i // 2]
                            
                            
    for curve_id in curve_pair:
        if curve_id not in processed_curves:
                                    
                                    
            moved_curve = rs.MoveObject(curve_id, movement_vector)
            moved_curves.append(moved_curve)
                                    
                                    
            processed_curves.add(curve_id)
                                    
                                    
                        
actual_curves = []
                        
for mov in moved_curves:
    actual_curve = rs.coercecurve(mov)
    actual_curves.append(actual_curve)
                            
                            
elevated_contours = actual_curves
                        
j = []
                        
if not mesh_formation:
    divide = gh.DivideLength(elevated_contours,smoothness)
    j = divide[0]
                        
p = gh.FlattenTree(j,0)
                        
final_mesh = gh.DelaunayMesh(p)

