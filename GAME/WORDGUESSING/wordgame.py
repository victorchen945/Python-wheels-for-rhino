#word guessing game


#IMPORTS
import rhinoscriptsyntax as rs
import scriptcontext as sc
import random as r


#defines

OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2
WIN=1
FAIL=0

MAXLOOP=99999
MAXPLAY=10

SCALE=1

filename="czy_deudict.txt"

SOL=[]

#surface compare
def srfCompare(srf1,srf2):
    pt1=rs.SurfaceAreaCentroid(srf1)
    pt2=rs.SurfaceAreaCentroid(srf2)
    if rs.PointCompare(pt1[0],pt2[0])==True:
        return True
    return False
    
class display:
    def __init__(self,word,picture):
        rs.HideObjects(picture)
        self.text=[]
        self.startxt=[]
        self.soltxt=[]
        self.blank=self.wordblank(word)  #word blank
        self.surfaces=self.blank[0]
        self.count=len(self.blank[0])       #record word pos
        self.pic=picture
        self.step=0
        self.ranstart(word)
        self.judge=WIN
        self.solution(word)
            
    def solution(self,word):
        for i in range(MAXLOOP):
            if self.count==0:
                self._delete()
                self.judge=WIN
                return WIN
            if self.showword(word)==TRUE:
                self._delete()
                self.judge=FAIL
                return FAIL
            print self.count
        
            
    def _delete(self):
        
        for i in range(len(self.blank[0])):
            rs.DeleteObjects(self.blank[0][i])
        for i in range(len(self.blank[1])):
            rs.DeleteObjects(self.blank[1][i])
        for i in range(len(self.text)):
            rs.DeleteObject(self.text[i])
        for i in range(len(self.startxt)):
            rs.DeleteObject(self.startxt[i])
        
    #draw wordblanks
    def wordblank(self,word):
        srfs=[]
        recs=[]
        for i in range (len(word)-1):
            rec=rs.AddRectangle((10*i*SCALE,0,0),10*SCALE,20*SCALE)
            srf=rs.AddPlanarSrf(rec)
            srfs.append(srf)
            recs.append(rec)
        return srfs,recs
    
    #draw picture
    def showpic(self,step):
        if step>=(len(self.pic)-1):
            return TRUE
        else:
            rs.ShowObject(self.pic[step])
        return FALSE
        
    #randomize a startword
    def ranstart(self,word):
        pos=r.randint(0,len(word)-2)
        rs.DeleteObject(self.blank[0][pos])
        self.startxt.append(rs.AddText(word[pos],(pos*10*SCALE,0,0),10*SCALE))
        self.count-=1
        return OK
    
    #print word
    def showword(self,word):
        #choose blank
        mysrf=rs.GetObject("choose the blank",rs.filter.surface)
        #input word
        while 1:
            str=rs.GetString("which word?")
            if len(str)==1:
                break
            else:
                rs.MessageBox("error,check input")
        #compare and draw
        pos=-1
        for i in range(len(self.surfaces)):
            if rs.IsSurface(self.surfaces[i]):
                if srfCompare(mysrf,self.surfaces[i])==TRUE:
                    pos=i
        if pos==-1:
            print "ERROR"
            return ERROR
        if str==word[pos]:
            rs.DeleteObject(self.blank[0][pos])
            self.text.append(rs.AddText(str,(pos*10*SCALE,0,0),10*SCALE))
            self.count-=1
        else:
            if self.showpic(self.step):
                return TRUE
            self.step+=1
        return FALSE
    def __del__(self):
        pass

#read in dictionary file
class word:
    #init the class
    def __init__(self):
        self.content=self.readfile()
    
    #read in the dictionary txt
    def readfile(self):
        content=[]
        myfile=open(filename,"r")
        for line in myfile.readlines():
            content.append(line)
        return content
    
    #pick a word randomly in the txt file
    def pickword(self):
        pos=r.randint(0,len(self.content)-1)
        return self.content[pos]
        


#input drawings
def inputpic():
    crvs=rs.GetObjects("define the input picture",rs.filter.curve)
    return crvs


def main():
    
    
    pic=inputpic()
    rs.HideObjects(pic)
    #print wD
    count=0
    text=[]
    newtext=[]
    for i in range(MAXPLAY):
        
        myWord=word()
        wD=myWord.pickword()
        myDraw=display(wD,pic)
        count +=1
        if myDraw.judge==WIN:
            for txts in newtext:
                rs.DeleteObjects(newtext)
            newtext.append(rs.AddText("game over! you win",(0,-20*SCALE,0),10*SCALE))
            newtext.append(rs.AddText("Round        word:",(0,-40*SCALE,0),10*SCALE))
            newtext.append(rs.AddText(count,(50*SCALE,-40*SCALE,0),10*SCALE))
            newtext.append(rs.AddText(wD,(150*SCALE,-40*SCALE,0),10*SCALE))
        else:
            for txts in newtext:
                rs.DeleteObjects(newtext)
            newtext.append(rs.AddText("game over! you failed",(0,-20*SCALE,0),10*SCALE))
            newtext.append(rs.AddText("Round        word:",(0,-40*SCALE,0),10*SCALE))
            newtext.append(rs.AddText(count,(50*SCALE,-40*SCALE,0),10*SCALE))
            newtext.append(rs.AddText(wD,(150*SCALE,-40*SCALE,0),10*SCALE))
    return OK
    

main()
