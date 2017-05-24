import rhinoscriptsyntax as rs
import scriptcontext as sc

#defines
OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2

class filter:
    def delduplicatesrf(self,srfs,tolerence):
        for i in range (len(srfs)):
            if srfs[i] is None:continue
            for j in range(i+1,len(srfs)):
                if srfs[j] is None:
                    continue
                if self.srfcompare(srfs[i],srfs[j],tolerence)==True:
                    rs.DeleteObject(srfs[j])
        return OK
    def srfcompare(self,srf1,srf2,tolerence):
        #to be upgraded
        if not rs.IsSurface(srf1) or not rs.IsSurface(srf2):return ERROR
        cen1=rs.SurfaceAreaCentroid(srf1)
        #rs.AddPoint(cen1[0])
        cen2=rs.SurfaceAreaCentroid(srf2)
        #rs.AddPoint(cen2[0])
        if rs.Distance(cen1[0],cen2[0])<tolerence:
            return True
        else :
            return False
    def delextru(self,srfs,tolerence):
        for srf in srfs:
            if srf is None:continue
            if not rs.IsSurface(srf):continue
            edges=rs.DuplicateEdgeCurves(srf)
            edge=rs.JoinCurves(edges,True,None)
            if type(edge)==list:
                max=edge[0]
                for edgeele in edge:
                    if rs.CurveLength(edgeele)>rs.CurveLength(max):
                        max=edgeele
                edge=max
            print edge
            if rs.SurfaceArea(srf)[0]/rs.CurveLength(edge)<tolerence:
                rs.DeleteObject(srf)
            rs.DeleteObject(edge)
                
                    

def flatten(objs):
    objlist=[]
    objrecs=[]
    for obj in objs:
        if rs.IsSurface(obj) and rs.IsSurfacePlanar(obj):
            #step1-transform the current surface to certain plane
            cen=rs.SurfaceAreaCentroid(obj)
            nrm=rs.SurfaceNormal(obj,rs.SurfaceClosestPoint(obj,cen[0]))
            curplane=rs.PlaneFromNormal(cen[0],nrm,None)
            opt=[cen[0][0],cen[0][1],0]
            tarplane=rs.PlaneFromFrame(opt,[1,0,0],[0,1,0])
            xform=rs.XformRotation1(curplane,tarplane)
            newobj=rs.TransformObject(obj,xform)
            #step2-put the surfaces into a rectangle
            objrec=[0,0]
            
            edges=rs.DuplicateEdgeCurves(obj)
            edge=rs.JoinCurves(edges,True,None)
            if type(edge)==list:
                ctrlpts=[]
                for ele in edge:
                    ctrlpts.extend(rs.CurvePoints(ele))
                for ele in edge:
                    rs.DeleteObject(ele)
            else:
                ctrlpts=rs.CurvePoints(edge)
                rs.DeleteObject(edge)
            #rs.AddPoints(ctrlpts)
            
            xmin=ctrlpts[0][0]
            xmax=ctrlpts[0][0]
            ymin=ctrlpts[0][1]
            ymax=ctrlpts[0][1]
            for ctrlpt in ctrlpts:
                if ctrlpt[0]>xmax:
                    xmax=ctrlpt[0]
                elif ctrlpt[0]<xmin:
                    xmin=ctrlpt[0]
                if ctrlpt[1]>ymax:
                    ymax=ctrlpt[1]
                elif ctrlpt[1]<ymin:
                    ymin=ctrlpt[1]
            objrec=rectangle()
            objrec.minpt=[xmin,ymin,0]
            objrec.maxpt=[xmax,ymax,0]
            objrec.xpt=[xmax,ymin,0]
            objrec.ypt=[xmin,ymax,0]
            objrec.xsize=abs(xmax-xmin)
            objrec.ysize=abs(ymax-ymin)
            objrecs.append(objrec)
            
            myele=element()
            myele.object=obj
            myele.rec=objrec
            objlist.append(myele)
    
    #step3- arrange the rectangle
    grouprec=rectangle()
    opointGUID=rs.GetObject("appoint origin point",rs.filter.point)
    opoint=rs.PointCoordinates(opointGUID)
    rs.MessageBox("continue?")
    ###now the force arrangement, should advance into new arrangement 
    for obj in objlist:
        #obj.rec.draw()
        if grouprec.xsize==None and grouprec.ysize==None:
            grouprec=obj.rec
            tmppt=obj.rec.minpt
            obj.rec.rectangletrans(opoint[0]-grouprec.minpt[0],opoint[1]-grouprec.minpt[1])
            grouprec.rectangletrans(opoint[0]-grouprec.minpt[0],opoint[1]-grouprec.minpt[1])
            obj.loc=grouprec.minpt
            rs.MoveObject(obj.object,rs.VectorCreate(obj.loc,tmppt))
            obj.draw()
            continue
        obj.loc=grouprec.xpt
        rs.MoveObject(obj.object,rs.VectorCreate(obj.loc,obj.rec.minpt))
        obj.rec.rectangletrans(grouprec.xpt[0]-obj.rec.minpt[0],grouprec.xpt[1]-obj.rec.minpt[1])
        grouprec.xpt=obj.rec.xpt
        grouprec.xsize+=obj.rec.xsize
        if grouprec.ysize<obj.rec.ysize:
            grouprec.ysize=obj.rec.ysize
        
        obj.draw()
        
            
            
    return OK

class rectangle:
    def __init__(self):
        self.minpt=None         #minimum diagnol point
        self.maxpt=None         #maximum diagnol point
        self.xpt=None           #xdirection point
        self.ypt=None           #ydirection point
        self.xsize=None         #xsize
        self.ysize=None         #ysize
    def rectangletrans(self,x,y):
        self.minpt=(self.minpt[0]+x,self.minpt[1]+y,0)
        self.maxpt=(self.maxpt[0]+x,self.maxpt[1]+y,0)
        self.xpt=(self.xpt[0]+x,self.xpt[1]+y,0)
        self.ypt=(self.ypt[0]+x,self.ypt[1]+y,0)
    def draw(self):
        rec=rs.AddPolyline((self.minpt,self.ypt,self.maxpt,self.xpt,self.minpt))
        return rec
    
    
class element:
    def __init__(self):
        
        self.object=None        #object
        self.boundary=None      #boundary(dwg)
        self.rec=None           #object rectangle
        self.loc=None           #object rectangle origin point
        self.group=None         #object group
        self.groupsize=None     #object group size
        
    def draw(self):
        if self.object==None:return ERROR
        edges=rs.DuplicateEdgeCurves(self.object)
        edge=rs.JoinCurves(edges,True,None)
        rs.DeleteObject(self.object)
    
    
def main():
    objs=rs.GetObjects("",rs.filter.surface)
    flatten(objs)
    #fil=filter()
    #fil.delduplicatesrf(objs,0.5)
    #fil.delextru(objs,0.2)
    return OK
    
main()        