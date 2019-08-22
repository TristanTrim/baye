search_range = (100,101)

bayesquares = set()

def normalize(tu,a,ba,bna):
    if((tu-a)<a):
        a=tu-a
        ba,bna = bna,ba
    if((tu-ba)<ba):
        ba=tu-ba
        bna=tu-bna
    elif((tu-ba)==ba):
        if((tu-bna)<bna):
            bna=tu-bna
    if((tu-a)==a):
        if(bna<ba):
            ba,bna = bna,ba
    return(tu,a,ba,bna)


def fa(tu,b,ab,anb):
    return( (ab*b + anb*(tu-b))/tu )

def fba(tu,b,ab,anb):
    return( (ab*b)/a )

def fbna(tu,b,ab,anb):
    return( ((tu - ab)*b)/(tu-a) )

def whole_number(x):
    return(abs(x-round(x)) < 0.00001)

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

for tu in range(*search_range):
    ## only count halfway because the other half is symmetrical
    for b in range(1,int(tu/2)+1):
        for ab in range(1,tu):
            for anb in range(1,tu):
                a=fa(tu,b,ab,anb)
                ba=fba(tu,b,ab,anb)
                bna=fbna(tu,b,ab,anb)
                if(
                    all([whole_number(x) for x in [a,ba,bna]])
                   #and not b==ab
                   #and not tu-b==ab
                   #and not all([b==a,ab==ba,anb==bna])
                   #and not anb==tu-ba
                    ):
                        bayesquares.add(normalize(tu,a,ba,bna))
                        #square,pluses = draw_probs(tu,b,ab,anb, a,ba,bna)
                        #if(pluses==2):
                        #    print("tu={},b={},a|b={},a|nb={}".format(tu,b,ab,anb))
                        #    print("a={},b|a={},b|na={}".format(a,ba,bna))
#                       #     print(square)
                        #    print()
             #  else:
             #          print(draw_b_probs(tu,b,ab,anb))

count = 0
for square in bayesquares:

    tu,b,ab,anb = square

    a=fa(tu,b,ab,anb)
    ba=fba(tu,b,ab,anb)
    bna=fbna(tu,b,ab,anb)

    square_drawing,pluses = draw_probs(tu,b,ab,anb,  a,ba,bna)
    if(pluses==2
        and (normalize(tu,a,ba,bna) != normalize(tu,b,ab,anb))
            ):
        count+=1
        print("tu={},b={},a|b={},a|nb={}".format(tu,b,ab,anb))
        print("a={},b|a={},b|na={}".format(a,ba,bna))
        print(square_drawing)
        print()

print("that was {} matches!".format(count))



