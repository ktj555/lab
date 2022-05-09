from copy import deepcopy
import pandas as pd

# 방향 설정 바꾸고 싶으면 이 클래스만 수정
class direction:
    n=4
    u=[-1,0]
    d=[1,0]
    r=[0,1]
    l=[0,-1]
    d_list=[u,r,d,l] # up right down left 시계방향 순으로 검색 [u,l,d,r]로 하면 반시계방향 검색

# Path 및 방향 저장을 위한 자료구조
# stack - (LIFO)후입선출 구조, Path
# queue - (FIFO)선입선출 구조, direction
# stack 및 queue 구현은 딱히 필요 x
class stack:
    def __init__(self):
        self.data=[]
        self.top=-1

    def IsEmpty(self):
        if(self.top==-1):
            return True
        else:
            return False
    
    def Top(self):
        if(self.IsEmpty()):
            return None
        else:
            return self.data[self.top]
    
    def Push(self,value):
        i=deepcopy(value)
        try:
            self.data.append(i)
            self.top+=1
            return True
        except:
            return False

    def Pop(self):
        if(self.IsEmpty()):
            return False
        else:
            x=self.data[self.top]
            del self.data[self.top]
            self.top-=1
            return x

    def clear(self):
        if(self.IsEmpty()):
            pass
        else:
            self.data=[]
            self.top=-1

    def search(self,value):
        if(self.IsEmpty()):
            return False
        for i in self.data:
            if (value[0]==i[0] and value[1]==i[1]):
                return True
        return False

    def see(self):
        print(self.data)

class queue:
    def __init__(self):
        self.data=[]
        self.rear=-1

    def IsEmpty(self):
        if(self.rear==-1):
            return True
        else:
            return False
    
    def Front(self):
        if(self.IsEmpty()):
            return None
        else:
            return self.data[0]

    def Rear(self):
        if(self.IsEmpty()):
            return None
        else:
            return self.data[self.rear]
    
    def Push(self,value):
        i=deepcopy(value)
        try:
            self.data.append(i)
            self.rear+=1
            return True
        except:
            return False

    def Pop(self):
        if(self.IsEmpty()):
            return False
        else:
            x=self.data[0]
            del self.data[0]
            self.rear-=1
            return x

    def clear(self):
        if(self.IsEmpty()):
            pass
        else:
            self.data=[]
            self.rear=-1

    def see(self):
        print(self.data)

# 그냥 간단히 하려고 만든거 중요 x
class path:
    def __init__(self):
        self.path=stack()           # 자기 이동 경로 저장
        self.save_direction=stack() # 경로마다 진행 가능 방향 저장
        self.can_direction=queue()  # 방향 탐색을 위해 사용되는 dummy variable
        self.save_path=stack()      # 지나갔었던 모든 칸 저장

# main class // 실제로 문제를 해결하는 함수는 maze class에 있기 때문에 그 부분만 보면 됨
class maze:
    # 미로 class
    # 사용자가 입력한 n by m 미로를 인스턴스변수로 가짐
    def __init__(self,array,start=2,end=-1):
        self.maze=self.makemaze(array)
        self.start=start
        self.end=end


    # 미로 가장자리를 벽으로 둘러치는 함수
    def makemaze(self,array):
        try:
            n=len(array)
            m=len(array[0])
        except:
            return False
        
        for i in range(n):
            array[i]=[1]+array[i]+[1]
        array=[[1 for i in range(m+2)]]+array+[[1 for i in range(m+2)]]
        return array

    def size(self):
        return [len(self.maze)-2,len(self.maze[0])-2]

    # 입력받은 미로의 시작점을 찾는 함수
    def find_start(self):
        for i in range(1,self.size()[0]+1):
            for j in range(1,self.size()[1]+1):
                if(self.maze[i],[j]==self.start):
                    return [i,j]
        return False

    # 실제로 동작하는 함수
    def solve(self,point):
        Solve=True      # 미로 해결을 나타내는 변수
        IsFirst=True    # 처음인지 판단하기 위해 사용하는 변수

        while(point.Where()!=self.end): # 끝지점에 도달하면 종료

            if(point.IsNew()|IsFirst):  # 지금 도달한 칸이 처음 도달했는지 판단 (처음 시작하면 인지 못해서 IsFirst로 강제 실행)

                x=point.search_direction()  # 그 지점에서 갈 수 있는 방향 탐색 (방향은 설정한 순서대로 {본인은 시계방향})
                                            # serach_direction 함수는 진행 가능한 방향이 없을 시 False, 방향을 찾을 시 방향을 return
                if(x): # 방향이 있으면
                    y=point.Path.save_direction.Pop()   # 저장 공간에서 이 칸의 진행 가능 방향 데이터 추출 ex) y=[up, right, left]
                    point.move(y.Pop())                 # 가장 처음 방향으로 진행 및 진행한 방향 제거          up 방향 진행 후 제거
                    point.Path.save_direction.Push(y)   #                                                    [right, left]는 아직 갈 수 있으니
                else:  # 방향이 없으면                                                                        다시 저장 공간에 집어 넣음
                    point.back()    # 뒤로 가기
                IsFirst=False

            else:   # 이미 와봤던 칸이면
                x=point.Path.save_direction.Pop()   # 이 칸에서 진행할 수 있는 방향 저장공간에서 추출
                if(x==False):   # 만약 저장 공간에 아무런 데이터가 존재하지 않는다면
                    Solve=False # 해석 불가
                    break
                elif(x.IsEmpty()):  # 데이터는 있지만 해당 칸에 진행할 방향은 없는 경우
                    point.back()    # 뒤로 가기
                else:           # 그 외 (진행할 방향이 남은 경우, 즉 분기점으로 돌아왔을 때)
                    point.Path.path.Push(point.position)    # 해당 위치 저장 (뒤로 돌아가는 과정에 해당 위치가 삭제되어서 넣어주는 것)
                    point.move(x.Pop())                     # 진행
                    point.Path.save_direction.Push(x)       # 해당 칸에 남은 진행 방향은 다시 저장 공간에 넣어줌

            if(point.Where()==self.start and point.Path.save_direction.IsEmpty()):  # 만약 처음 위치로 돌아왔는데
                Solve=False                                                         # 더 이상 진행할 방향이 없을 경우
                break                                                               # 해석 불가

        if(Solve):  # 해결 했으면 해결 경로를 반환, 아닌 경우 False 반환
            return point.Path.path.data
        else:
            return False

# main class // 미로 내에서 위치에 대한 기능을 담당하는 class
#               구현은 중요하지 않고 기능이 중요
#               가능 기능 - 위치 탐색, 방향 탐색, 이동, 경로 및 방향 등의 데이터 저장
#               point class 는 기능만 가지고 maze class 에서 판단 및 처리하는 구조
class point:
    def __init__(self,array,row=0,column=0):
        self.position=[row,column]
        self.map=array
        self.Path=path()
        self.set()
        self.last_position=[self.position[0],self.position[1]]
        self.Path.path.Push(self.Iswhere())
        self.Path.save_path.Push(self.Iswhere())

    def Iswhere(self):
        return self.position

    def Where(self):
        return self.map.maze[self.position[0]][self.position[1]]
    
    def IsCan(self,row,column):
        if(self.map.maze[row][column]==1):
            return False
        else:
            return True

    def IsNew(self):
        if(self.Path.save_path.search(self.position)):
            return False
        else:
            return True

    def set(self):
        row,column=self.map.find_start()
        self.position=[row,column]

    def last_direction(self):
        row=self.last_position[0]-self.position[0]
        column=self.last_position[1]-self.position[1]
        return [row,column]
    
    def search_direction(self):
        self.Path.can_direction.clear()
        for i in direction.d_list:
            if(self.search_region(i) and (i!=self.last_direction())):
                self.Path.can_direction.Push(i)
        if(self.Path.can_direction.IsEmpty()):
            return False
        else:
            self.Path.save_direction.Push(self.Path.can_direction)
            return True
    
    def search_region(self,direction):
        f_row,f_column=self.position[0]+direction[0],self.position[1]+direction[1]
        if(self.IsCan(f_row,f_column)):
            return True
        else:
            return False

    def move(self,direction):
        if(self.Path.save_path.search(self.position)):
            pass
        else:
            self.Path.save_path.Push(self.position)
        self.last_position[0]=self.position[0]
        self.last_position[1]=self.position[1]
        self.position[0]+=direction[0]
        self.position[1]+=direction[1]
        self.Path.path.Push(self.Iswhere())

    def back(self):
        x=self.Path.path.Pop()
        self.position[0],self.position[1]=x[0],x[1]
        x=self.Path.path.Pop()
        if(x):
            self.last_position[0],self.last_position[1]=x[0],x[1]
        else:
            self.last_position[0],self.last_position[1]=self.position[0],self.position[1]
        self.Path.path.Push(self.last_position)


# 실행 test

# 미로 설정
array=[[2,0,0,0,0,0,0,0,0,0],
       [0,1,1,1,1,1,0,1,1,0],
       [0,1,0,0,0,1,0,1,1,1],
       [0,1,0,1,0,1,0,0,0,0],
       [0,1,0,1,0,1,1,1,1,1],
       [0,0,0,1,0,0,0,0,0,0],
       [0,1,1,1,1,0,1,1,1,0],
       [0,0,0,0,1,0,0,0,1,-1]]

a=deepcopy(array) # 후처리하려고 한 것, 무시

# maze 객체 생성 
map=maze(array,start=2,end=-1)

# point 객체 생성
p=point(map)

# 생성한 maze와 point 객체를 이용하여 solve
way=map.solve(p)



# result Processing

Way=pd.DataFrame(way,columns=['row','column'])

d=Way.diff(axis=0)

d['up']=d['row']==-1
d['down']=d['row']==1
d['right']=d['column']==1
d['left']=d['column']==-1

arrow=[]

for i in range(len(d)):
    if(d['up'][i]):
        arrow.append('^')
    elif(d['right'][i]):
        arrow.append('>')
    elif(d['left'][i]):
        arrow.append('<')
    elif(d['down'][i]):
        arrow.append('v')
    else:
        arrow.append('x')

def printarray(array):
    n,m=len(array),len(array[0])
    for i in range(n):
        for j in range(m):
            print("{:^3}".format(array[i][j]),end='')
        print()

n,m=len(a),len(a[0])
for i in range(n):
    for j in range(m):
        if(a[i][j]==1):
            a[i][j]='|'
for i in range(len(Way)):
    a[Way['row'][i]-1][Way['column'][i]-1]=arrow[i]

if(way==False):
    print("No way")
else:
    printarray(a)