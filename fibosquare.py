

from time import sleep
from typing import Tuple

from termcolor import colored


class FiboSquare() :
    def __init__(self, tl = 1, tr = 1, bl = 3, br = 2) -> None:
        self.tl = tl
        self.tr = tr
        self.bl = bl
        self.br = br
        self.childs = None
        self.parent = None

    def set_br(self):
        self.br = self.tr + self.tl

    def set_bl(self):
        self.bl = self.br + self.tr

    def be_left_child(self):
        self.tl = self.bl
        self.set_br()
        self.set_bl()

    def be_center_child(self):
        self.tl = self.bl
        self.tr = self.br
        self.set_br()
        self.set_bl()
    
    def be_right_child(self):
        self.tr = self.br
        self.set_br()
        self.set_bl()

    def get_childs(self, depth = 0):
        self.childs = [FiboSquare()]
        self.childs.pop()
        for i in [0,1,2] :
            self.childs.append(FiboSquare(self.tl, self.tr, self.bl, self.br))
            self.childs[i].parent = self
            # print(self.childs[i])

        self.childs[0].be_left_child()
        self.childs[1].be_center_child()
        self.childs[2].be_right_child()  

        if depth == 0 : return
        for i in [0,1,2] :
            self.childs[i].get_childs(depth-1)

    def __str__(self) -> str:
        message =  f"[ {self.tl} | {self.tr}  \n"
        message += f"  {self.bl} | {self.br} ]"
        return message

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            if self.tl != __o.tl : return False
            if self.tr != __o.tr : return False
            if self.bl != __o.bl : return False
            if self.br != __o.br : return False
            return True
        else:
            return NotImplementedError


    def show_childs(self, depth = 0, invdepth = 0) -> str:
        if depth == 0:
            return self.__str__()
        else :
            message = ""
            for child in self.childs:
                message += f"{child.show_childs(depth-1, invdepth+1)}\n   \n"
            message = "    " + message.replace("\n", "\n    ")
            message = message.replace("    [", "  |-[")
            message = message.replace("     ", "  |  ")
            return f"{self.__str__()}\n  |  \n{message}"

    def show_path(self, node : "FiboSquare", path = None) -> str:
        if path == None :
            message = self.get_path_to_child(node)
            path = message.split()
            return self.show_path(node, path)
        else :
            depth = len(path)
            if not isinstance(path, list) : return
            if depth == 0:
                if self == node :
                    return colored(self.__str__(), "green")
                else :
                    return self.__str__()
            else :
                cur_path = path[0]
                message = ""
                ways = ["left", "center", "right"]
                for child, way in zip(self.childs, ways):
                    if way == cur_path :
                        message += f"{colored(child.show_path(node, path[1:]), 'green')}\n   \n"
                    else :
                        message += f"{child.show_path(node, [])}\n   \n"
                message = "    " + message.replace("\n", "\n    ")
                message = message.replace("    [", "  |-[")
                message = message.replace("     ", "  |  ")

                if way == cur_path :
                    return f"{colored(self.__str__(), 'green')}\n  |  \n{message}"
                else :
                    return f"{self.__str__()}\n  |  \n{message}"

    def get_pythagorian_triangle(self) -> Tuple[int, int, int]:
        a = self.tl * self.bl
        b = 2 * self.tr * self.br
        c = (self.tl * self.br) + (self.tr * self.bl)
        return a,b,c

    @staticmethod
    def get_fibosquare_from_pyth(a :int , b : int, c : int):
        a_cpl = []
        for tl in range(100) :
            for bl in range(100) :
                if a == (tl*bl) :
                    if ( [tl,bl] not in a_cpl ) : a_cpl.append( [tl,bl] )
        # print(a_cpl)
        b_cpl = []
        for tr in range(100) :
            for br in range(100) :
                if b == 2*(tr*br) :
                    if ( [tr,br] not in b_cpl ) : b_cpl.append( [tr,br] )
        # print(b_cpl)
        c_qdr = []
        for tl,bl in a_cpl :
            for tr,br in b_cpl :
                if c == (tl*br)+(tr*bl):
                    if [tl,tr,bl,br] not in c_qdr :
                        c_qdr.append([tl,tr,bl,br])
        
        # print(c_qdr)
        for tl,tr,bl,br in c_qdr :
            aa = tl*bl
            bb = 2*tr*br
            cc = (tl*br)+(tr*bl)
            # print(aa*aa + bb*bb)
            # print(cc*cc)
            if (aa*aa + bb*bb) == (cc*cc):
                return FiboSquare(tl,tr,bl,br)
        return FiboSquare(0,0,0,0)

    def find_child(self, fs : "FiboSquare", depth = 10) -> str:
        # print(self)
        if self == fs :
            return self
        elif depth > 0 :
            if not self.childs : self.get_childs(0)
            for child in self.childs :
                res = child.find_child(fs, depth-1)
                if res :
                    return res

        else:
            return None

    def get_path_to_child(self, node : "FiboSquare"):
        message = ""
        # node.parent = FiboSquare()
        ways = ["left", "center", "right"]
        if not node.parent : node = self.find_child(node, 14)
        parent = node.parent
        while parent :
            if isinstance(parent, type(self)) :
                for child, way in zip(parent.childs, ways) :
                    if child == node :
                        # print(child)
                        message = f" {way}" + message
                        node = parent
                        parent = node.parent
        return message
            
    def set_fibo_uv(self, u, v):
        if v < u : return
        if (v-u)%2 == 0 : return
        self.tr = u
        self.br = v
        self.tl = v-u
        self.bl = v+u
    
fs = FiboSquare()
fs.set_fibo_uv
fss = FiboSquare()
fss.set_fibo_uv(798, 2251)

print(fs.show_path(fss))