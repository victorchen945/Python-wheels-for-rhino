##########################################
######## script by Zhengyang Chen ########
########         +1s              ########
##########################################




#import rhino modules
import rhinoscriptsyntax as rs


#defines
OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2

#compare functions, define if two object overlaps
class _compare():

    def __init__(self):
        pass
    
    #compare 2 points
    def point(self,pt1,pt2):
        if rs.PointCompare(pt1,pt2):
            return TRUE
        return FALSE
        
    #compare 2 lists of points
    def pointcloud(self,pts1,pts2):
        
        #if list length dont fit return false
        if len(pts1)<>len(pts2):
            return FALSE
            
        #compare every units
        if set(pts1).issubset(set(pts2))==True:
            return TRUE
        return FALSE
    
    #compare 2 curves
    def curve(self,crv1,crv2):
        #make sure is curve
        if not rs.IsCurve(crv1)*rs.IsCurve(crv2):
            print "error"
            return ERROR
            
        #compare curve control points
        pts1=rs.CurvePoints(crv1)
        pts2=rs.CurvePoints(crv2)
        
        if self.pointcloud(pts1,pts2)==True:
            return TRUE
        else:
            return FALSE
            
class delobj:
    
    #init operation
    def __init__(self,obj):
        self.pts=obj.points
        self.crvs=obj.curves
        
        print "number of points:", len(self.pts)
        print "number of curves:", len(self.crvs)
        self.delpts()
        self.delcrvs()
        self.delsrfs()
        
    #delete same points
    def delpts(self):
        count=0
        for i in range(len(self.pts)):
            for j in range(i+1,len(self.pts)):
                if rs.IsPoint(self.pts[i]) and rs.IsPoint(self.pts[j])\
                and rs.PointCompare(self.pts[i],self.pts[j])==True:
                    count+=1
                    rs.DeleteObject(self.pts[j])
        print "delete", count, "points"
        
        #renew the point list
        newlist=[]
        for i in range(len(self.pts)):
            if rs.IsPoint(self.pts[i]):
                newlist.append(self.pts[i])
        return newlist
        
    #delete same curves
    def delcrvs(self):
        count=0
        compare=_compare()
        for i in range(len(self.crvs)):
            for j in range(i+1,len(self.crvs)):
                if rs.IsCurve(self.crvs[i]) and rs.IsCurve(self.crvs[j])\
                and compare.curve(self.crvs[i],self.crvs[j])==True:
                    count+=1
                    rs.DeleteObject(self.crvs[j])
        print "delete", count, "curves"
        
        #renew the curve list
        newlist=[]
        for i in range(len(self.crvs)):
            if rs.IsPoint(self.crvs[i]):
                newlist.append(self.crvs[i])
        return newlist
        
    #to be modified
    def delsrfs(self):
        return OK

    
#classify the selected objects
class pool:
    def __init__(self,objs):
        self.points=[]
        self.curves=[]
        self.pickup(objs)
        
        
    def pickup(self,objs):
        for obj in objs:
            if rs.IsPoint(obj):
                self.points.append(obj)
            if rs.IsCurve(obj):
                self.curves.append(obj)
        return objs
        
    
def main():
    objs=rs.GetObjects("select objects")
    bin=pool(objs)
    delete=delobj(bin)
    return OK
main()
