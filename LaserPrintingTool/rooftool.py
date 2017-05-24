import rhinoscriptsyntax as rs
import scriptcontext as sc

OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2

NUM=100

def roof():
    srf1=rs.GetObject("select pair srf 1",rs.filter.surface)
    srf2=rs.GetObject("select pair srf 2",rs.filter.surface)
    edge1=rs.JoinCurves(rs.DuplicateEdgeCurves(srf1))
    edge2=rs.JoinCurves(rs.DuplicateEdgeCurves(srf2))
    newsrf=rs.AddLoftSrf([edge1,edge2],None,None,2)
    newsrf=rs.JoinSurfaces([srf1,srf2,newsrf],True)
    if rs.IsPolysurfaceClosed(newsrf):
        print "OK"
        return OK
        rs.DeleteObjects(edge1,edge2)
    else:
        rs.DeleteObjects(newsrf)
        rs.DeleteObjects(edge1,edge2)
        return ERROR

def main():
    count=0
    while 1:
        if roof()==ERROR:break
        count+=1
        if count>NUM:break
        
main()
