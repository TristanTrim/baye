search_range = (2,17)

bayesquares = set()

#      ba   bna
#    ###########
#  a # q2 # q1 #
#    ###########
# na # q3 # q4 #
#    ###########
#     bna  nbna

def whole_number(x):
    return(abs(x-round(x)) < 0.00001)

class bayesquare:
    def __init__(self, tu, a, ba, bna):
        self.tu = tu
        self.a = a
        self.ba = ba
        self.bna = bna

        #self.normalize()

    def compute_extras(self):
        self.nba = self.tu-self.ba
        self.q1 = self.a*self.nba
        self.q2 = self.a*self.ba
        self.na = self.tu-self.a
        self.q3 = self.na*self.bna
        self.nbna = self.tu-self.bna
        self.q4 = self.na*self.nbna

        self.b = (self.q2 + self.q3) / self.tu
        self.nb = self.tu - self.b

        self.ab = self.q2 / self.b
        self.anb = self.q1 / self.nb
        self.nab = self.q3 / self.b
        self.nanb = self.q4 / self.nb

    def normalize(self):
        self.compute_extras() ## should this go here?

        maxind=0
        maxval=0
        qs = (self.q1,self.q2,self.q3,self.q4)

        for i in range(0,4):
            if qs[i] > maxval:
                maxind = i
                maxval = qs[i]
        #qs = qs[maxind:]+qs[:maxind]
        if(maxind == 1):
            self.rot_right_90()
        elif(maxind == 2):
            self.rot_180()
        elif(maxind == 3):
            self.rot_left_90()

        if self.q2 < self.q4:
            self.flip()

    def rot_left_90(self):
        self.a = self.nb
        self.ba = self.anb
        self.bna = self.ab
        self.compute_extras() ## which is more expensive, math or memory swapping?
                    ## you're coding in python, it doesn't matter anyway!
                        ## maybe optimize later if you still care!

    def rot_right_90(self):
        self.a = self.b
        self.ba = self.nab
        self.bna = self.nanb
        self.compute_extras()

    def rot_180(self):
        self.a = self.na
        self.ba = self.nbna
        self.bna = self.nba
        self.compute_extras()

    def flip(self):
        self.a = self.nb
        self.ba = self.nanb
        self.bna = self.nab
        self.compute_extras()

    def draw(self):
        pluses=0
        string=""
        string+="tu={}\t".format(self.tu)
        string+="a={},b|a={},b|na={}\t".format(self.a,self.ba,self.bna)
        string+="b={},a|b={},a|nb={}\n".format(self.b,self.ab,self.anb)
        for y in range(0,self.tu+1):

            # B probs
            for x in range(0,self.tu+1):
                if(y<self.a):
                    if(x==self.ba):
                        string+="|"
                    else:
                        string+=" "
                elif(y>self.a):
                    if(x==self.bna):
                        string+="|"
                    else:
                        string+=" "
                elif(x==self.ba or x==self.bna):
                    string+="+"
                    pluses+=1
                else:
                    string+="-"
            string+="    "

            # A probs
            for x in range(0,self.tu+1):
                if(x<self.b):
                    if(y==self.ab):
                        string+="-"
                    else:
                        string+=" "
                elif(x>self.b):
                    if(y==self.anb):
                        string+="-"
                    else:
                        string+=" "
                elif(y==self.ab or y==self.anb):
                    string+="+"
                else:
                    string+="|"

            string+="\n"
        return(string, pluses)

    def check_whole_nums(self):
        return(all((whole_number(x) for x in (self.a,self.b,self.ba,self.bna,self.ab,self.anb))))



## probs mostly garbage down there...

def quadrantize(tu,a,ba,bna):
    nba = tu-ba
    q1 = a*nba
    q2 = a*ba
    na = tu-a
    q3 = na*bna
    nbna = tu-bna
    q4 = na*nbna
    return(q1,q2,q3,q4)


###############
# 1:q2 # 0:q1 #
###############
# 2:q3 # 3:q4 #
###############

def normalize(qs):
    maxind=0
    maxval=0
    for i in range(0,4):
        if qs[maxind] > maxval:
            maxval = qs[maxind]
            maxind = i
    qs = qs[maxind:]+qs[:maxind]
    if qs[1] < qs[3]:
        qs=(qs[0],qs[3],qs[2],qs[1])
    return(qs)


def fa(tu,b,ab,anb):
    return( (ab*b + anb*(tu-b))/tu )

def fba(tu,b,ab,anb):
    return( (ab*b)/a )

def fbna(tu,b,ab,anb):
    return( ((tu - ab)*b)/(tu-a) )


def draw_probs(tu,b,ab,anb, a,ba,bna):
    pluses=0
    string=""
    for y in range(0,tu+1):

        # B probs
        for x in range(0,tu+1):
            if(y<b):
                if(x==ab):
                    string+="|"
                else:
                    string+=" "
            elif(y>b):
                if(x==anb):
                    string+="|"
                else:
                    string+=" "
            elif(x==ab or x==anb):
                string+="+"
                pluses+=1
            else:
                string+="-"
        string+="    "

        # A probs
        for x in range(0,tu+1):
            if(x<a):
                if(y==ba):
                    string+="-"
                else:
                    string+=" "
            elif(x>a):
                if(y==bna):
                    string+="-"
                else:
                    string+=" "
            elif(y==ba or y==bna):
                string+="+"
            else:
                string+="|"

        string+="\n"
    return(string, pluses)

def draw_b_probs(tu,b,ab,anb):
    string=""
    for y in range(0,tu+1):

        for x in range(0,tu+1):
            if(y<b):
                if(x==ab):
                    string+="|"
                else:
                    string+=" "
            elif(y>b):
                if(x==anb):
                    string+="|"
                else:
                    string+=" "
            elif(x==ab or x==anb):
                string+="+"
            else:
                string+="-"
        string+="\n"
    return(string)

#bs = bayesquare(100,50,10,40)
#print(bs.draw()[0])

if __name__ == "__main__":
    for tu in range(*search_range):
        ## only count halfway because the other half is symmetrical
        for a in range(1,int(tu/2)+1):
            for ba in range(1,tu):
                for bna in range(1,tu):
                    square = bayesquare(tu,a,ba,bna)
                    square.normalize()
                    if square.check_whole_nums():
                        bayesquares.add((square.tu,square.a,square.ba,square.bna))
                 #   if(some condition)
                 #           bayesquares.add(normalize(tu,a,ba,bna))


    count = 0
    for squarevals in sorted(bayesquares):
        square = bayesquare(*squarevals)
        square.compute_extras()
        square_drawing,pluses = square.draw()
        if pluses == 2:
            count+=1
            print(square_drawing)
    #    if(pluses==2
    #        and (normalize(tu,a,ba,bna) != normalize(tu,b,ab,anb))
    #            ):
    #        count+=1
    #        print("tu={},b={},a|b={},a|nb={}".format(tu,b,ab,anb))
    #        print("a={},b|a={},b|na={}".format(a,ba,bna))
    #        print(square_drawing)
    #        print()

    print("that was {} matches!".format(count))



