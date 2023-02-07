import rules
import copy
import time
_DEPTH = 2
pointPerPiece={ "bPawn"     :100,    "wPawn"     :-100,
                "bKnight"   :320,    "wKnight"   :-320,
                "bBishop"   :330,    "wBishop"   :-330,
                "bRook"     :500,    "wRook"     :-500,
                "bQueen"    :900,    "wQueen"    :-900,
                "bKing"     :10000,  "wKing"     :-10000}

wPawnPoint=[
    [0,0,0,0,0,0,0,0],
    [-50,-50,-50,-50,-50,-50,-50,-50],
    [-10,-10,-20,-30,-30,-20,-10,-10],
    [-5,-5,-10,-25,-25,-10,-5,-5],
    [0,0,0,-20,-20,0,0,0],
    [-5,5,10,0,0,10,5,-5],
    [-5,-10,-10,20,20,-10,-10,-5],
    [0,0,0,0,0,0,0,0]
]
bPawnPoint=[
    [0,0,0,0,0,0,0,0],
    [5,10,10,-20,-20,10,10,5],
    [5,-5,-10,0,0,-10,-5,5],
    [0,0,0,20,20,0,0,0],
    [5,5,10,25,25,10,5,5],
    [10,10,20,30,30,20,10,10],
    [50,50,50,50,50,50,50,50],
    [0,0,0,0,0,0,0,0]
    ]
wKnightPoint=[
    [50,40,30,30,30,30,40,50],
    [40,20,0,0,0,0,20,40],
    [30,0,-10,-15,-15,-10,0,30],
    [30,-5,-15,-20,-20,-15,-5,30],
    [30,-5,-15,-20,-20,-15,-5,30],
    [30,0,-10,-15,-15,-10,0,30],
    [40,20,0,0,0,0,20,40],
    [50,40,30,30,30,30,40,50]
    ]
bKnightPoint=[
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,0,0,0,0,-20,-40],
    [-30,0,10,15,15,10,0,-30],
    [-30,5,15,20,20,15,5,-30],
    [-30,5,15,20,20,15,5,-30],
    [-30,0,10,15,15,10,0,-30],
    [-40,-20,0,0,0,0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

wBishopPoint=[
    [20,10,10,10,10,10,10,20],
    [10,0,0,0,0,0,0,10],
    [10,0,-5,-10,-10,-5,0,10],
    [10,-5,-5,-10,-10,-5,-5,10],
    [10,0,-10,-10,-10,-10,0,10],
    [10,-10,-10,-10,-10,-10,-10,10],
    [10,-5,0,0,0,0,-5,10],
    [20,10,10,10,10,10,10,20]
    ]
bBishopPoint=[
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,5,0,0,0,0,5,-10],
    [-10,10,10,10,10,10,10,-10],
    [-10,0,10,10,10,10,0,-10],
    [-10,5,5,10,10,5,5,-10],
    [-10,0,5,10,10,5,0,-10],
    [-10,0,0,0,0,0,0,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20],
    ]
wRookPoint=[
    [0,0,0,0,0,0,0,0],
    [-5,-10,-10,-10,-10,-10,-10,-5],
    [5,0,0,0,0,0,0,5],
    [5,0,0,0,0,0,0,5],
    [5,0,0,0,0,0,0,5],
    [5,0,0,0,0,0,0,5],
    [5,0,0,0,0,0,0,5],
    [0,0,0,-5,-5,0,0,0]
    ]
bRookPoint=[
    [0,0,0,5,5,0,0,0],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [5,10,10,10,10,10,10,5],
    [0,0,0,0,0,0,0,0]
    ]
wQueenPoint=[
    [20,10,10,5,5,10,10,20],
    [10,0,0,0,0,0,0,10],
    [10,0,-5,-5,-5,-5,0,10],
    [5,0,-5,-5,-5,-5,0,5],
    [5,0,-5,-5,-5,-5,0,5],
    [10,-5,-5,-5,-5,-5,0,10],
    [10,0,-5,0,0,0,0,10],
    [20,10,10,5,5,10,10,20]
    ]
bQueenPoint=[
    [-20,-10,-10,-5,-5,-10,-10,-20],
    [-10,0,0,0,0,5,0,-10],
    [-10,0,5,5,5,5,5,-10],
    [-5,0,5,5,5,5,0,-5],
    [-5,0,5,5,5,5,0,-5],
    [-10,0,5,5,5,5,0,-10],
    [-10,0,0,0,0,0,0,-10],
    [-20,-10,-10,-5,-5,-10,-10,-20],
    
    
    ]
wKingPoint=[
    [ 3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0],
    [ 3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0],
    [ 3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0],
    [ 3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0],
    [ 2.0, 3.0, 3.0, 4.0, 4.0, 3.0, 3.0, 2.0],
    [ 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0],
    [  -2.0,  -2.0,  0.0,  0.0,  0.0,  0.0,  -2.0,  -2.0 ],
    [  -2.0,  -3.0,  -1.0,  0.0,  0.0,  -1.0,  -3.0,  -2.0 ]
    ]
bKingPoint=[
    [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0], 
    [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0], 
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0], 
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0], 
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0], 
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0], 
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0], 
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0]
    ]
def generateChessState(chess_state, turn):
    list = []

    for y in range(0,8):
        for x in range(0, 8):
            if chess_state[x][y] != "xx":
                click = [(x,y)]

                if chess_state[x][y][0] != turn:
                    continue

                for pos in rules.moveList(chess_state, click, turn):
                    tempState = copy.deepcopy(chess_state)
                    newX = pos[0]
                    newY = pos[1]

                    if tempState[x][y] == "bPawn" and newX == 7:
                        tempState[newX][newY] = "bQueen"
                        tempState[x][y] = "xx"

                    elif tempState[x][y] == "bKing" and ((newX, newY) == (0,6) or (newX, newY) == (0,2)):
                        rules.update(tempState, [], [(x,y), (newX, newY)])
                    else:
                        tempState[newX][newY] = tempState[x][y]
                        tempState[x][y] = "xx"
                    list.append(tempState)

    return list

def evaluatePoint(chess_state,pointPerPiece):
    totalPoint=0
    for row in range(8):
        for col in range(8):
            piece=chess_state[row][col]
            if piece=="xx":
                pass
            else:
                func=globals()[piece+"Point"]
                totalPoint=totalPoint+pointPerPiece[piece]+func[row][col]
    return totalPoint
def miniMax(chess_state, depth= _DEPTH):
    state_value=maxState_Value(chess_state,depth)
    return state_value[0]
def maxState_Value(chess_state,depth):
    if depth==0 or rules.checkNoMove(chess_state,'w'):
        state_value=(chess_state,evaluatePoint(chess_state,pointPerPiece))
        return state_value
    else:
        v=-99999
        successors=generateChessState(chess_state,'b')
        #print(successors)
        s=successors[0]
        for gChessState in successors:
            min=minState_Value(gChessState,depth-1)
            if v<min[1]:
                v=min[1]
                s=gChessState
        return (s,v)

def minState_Value(chess_state,depth):
    if depth==0 or rules.checkNoMove(chess_state,'b'):
        state_value=(chess_state,evaluatePoint(chess_state,pointPerPiece))
        print(state_value[1])
        return state_value
    else:
        v=99999
        successors=generateChessState(chess_state,'w')
        s=successors[0]
        for gChessState in successors:
            max=maxState_Value(gChessState,depth-1)
            if v>max[1]:
                v=max[1]
                s=gChessState
        return (s,v)

def alpha_beta_Search(chess_state, depth = _DEPTH):
    stateValue = maxValue(chess_state, -99999, 99999, depth)
    return stateValue[0]

def maxValue(chess_state, a, b, depth):
    if depth == 0 or rules.checkNoMove(chess_state, 'b'):
        state_value = (chess_state, evaluatePoint(chess_state,pointPerPiece))
        print(state_value[1])
        return state_value
    else:
        v= -99999
        successors = generateChessState(chess_state, 'b')
        s = successors[0]
        for gChessState in successors:
            max = minValue(gChessState, a, b, depth-1)
            if v < max[1]:
                v = max[1]
                s = gChessState
            if v >= b: # check v >= beta
                # print("a va b la:",a,b)
                # time.sleep(3)
                return (s,v)
            if v > a: # a = max(a,v)
                a = v
        # print("a va b la:",a,b)
        # time.sleep(3)
        return (s,v)

def minValue(chess_state, a, b, depth):
    if depth == 0 or rules.checkNoMove(chess_state, 'w'):
        state_value = (chess_state, evaluatePoint(chess_state,pointPerPiece))
        print(state_value[1])
        return state_value
    else:
        v= 99999
        successors = generateChessState(chess_state, 'w')
        s = successors[0]
        for gChessState in successors:
            min = maxValue(gChessState, a, b, depth-1)
            if v > min[1]:
                v = min[1]
                s = gChessState
            if v <= a: # check v<= alpha
                # print("a va b la:",a,b)
                # time.sleep(3)
                return (s,v)
            if v < b: # b = min(v,b)
                b = v
        # print("a va b la:",a,b)
        # time.sleep(3)
        return (s,v)
            
        