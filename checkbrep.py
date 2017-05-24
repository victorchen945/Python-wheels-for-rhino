import rhinoscriptsyntax as rs
import scriptcontext as sc

def test(objs):
    defclr=rs.LayerColor("bldgbrep")
    for obj in objs:
        rs.ObjectColor(obj,defclr)
        if obj is None: continue
        if (not rs.IsSurface(obj)) and (not rs.IsPolysurface(obj)):
            continue
        if not rs.IsPolysurfaceClosed(obj):
            rs.ObjectColor(obj,[255,0,0])
            print "ERROR"

def main():
    objs=rs.GetObjects("",rs.filter.surface|rs.filter.polysurface)
    test(objs)
    return 0

main()