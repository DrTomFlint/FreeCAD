class ParametricRectangle:

 def __init__(self,obj):
   obj.Proxy = self
   obj.addProperty("App::PropertyFloat","Length")
   obj.addProperty("App::PropertyFloat","Width")

 def execute(self,obj):
   # we need to import the FreeCAD module here too, because we might be running out of the Console
   # (in a macro, for example) where the FreeCAD module has not been imported automatically
   import Part,FreeCAD
   
   # first we need to make sure the values of Length and Width are not 0
   # otherwise the Part.Line will complain that both points are equal
   if (obj.Length == 0) or (obj.Width == 0):
     # if yes, exit this method without doing anything
     return
     
   # we create 4 points for the 4 corners
   v1 = FreeCAD.Vector(0,0,0)
   v2 = FreeCAD.Vector(obj.Length,0,0)
   v3 = FreeCAD.Vector(obj.Length,obj.Width,0)
   v4 = FreeCAD.Vector(0,obj.Width,0)
   
   # we create 4 edges
   e1 = Part.Line(v1,v2).toShape() # Warning. Since FC v0.17, use Part.LineSegment instead of Part.Line
   e2 = Part.Line(v2,v3).toShape()
   e3 = Part.Line(v3,v4).toShape()
   e4 = Part.Line(v4,v1).toShape()
   
   # we create a wire
   w = Part.Wire([e1,e2,e3,e4])
   
   # we create a face
   f = Part.Face(w)
   
   # All shapes have a Placement too. We give our shape the value of the placement
   # set by the user. This will move/rotate the face automatically.
   f.Placement = obj.Placement
   
   # all done, we can attribute our shape to the object!
   obj.Shape = f


# TF added lines
myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Rectangle")
ParamRectangle.ParametricRectangle(myObj)
myObj.ViewObject.Proxy = 0 # this is mandatory unless we code the ViewProvider too
FreeCAD.ActiveDocument.recompute()



