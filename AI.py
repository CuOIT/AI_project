import rules
import copy
import time
_DEPTH = 2
pointPerPiece={ "bPawn"     :-10,    "wPawn"     :10,
                "bKnight"   :-30,    "wKnight"   :30,
                "bBishop"   :-30,    "wBishop"   :30,
                "bRook"     :-50,    "wRook"     :50,
                "bQueen"    :-90,    "wQueen"    :90,
                "bKing"     :-1000, "wKing"     :1000}

wPawnPoint=[
    [20.0,  20.0,  20.0,  20.0,  20.0,  20.0,  20.0,  20.0],
    [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
    [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
    [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
    [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
    [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
    [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ]
bPawnPoint=[
    [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
    [-0.5,-1.0,-1.0,2.0,2.0,-1.0,-1.0,-0.5],
    [-0.5,0.5,1.0,0.0,0.0,1.0,0.5,-0.5],
    [0.0,  0.0,  0.0,  -2.0,  -2.0,0.0,0.0, 0.0],
    [-0.5, -0.5, -1.0, -2.5, -2.5, -1.0, -0.5, -0.5],
    [-1.0, -1.0, -2.0, -3.0, -3.0, -2.0, -1.0, -1.0],
    [-5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0],
    [-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0]
    ]
wKnightPoint=[
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
    [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
    [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
    [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
    [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
    [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
    ]
bKnightPoint=[
    [5.0, 4.0, 3.0, 3.0, 3.0, 3.0, 4.0, 5.0],
    [4.0, 2.0,  0.0,  -0.5,  -0.5,  0.0, 2.0, 4.0],
    [3.0,  -0.5,  -1.0,  -1.5,  -1.5,  -1.0,  -0.5, 3.0],
    [3.0,  -0.5,  -1.5,  -2.0,  -2.0,  -1.5,  0.0, 3.0],
    [3.0,  -0.5,  -1.5,  -2.0,  -2.0,  -1.5,  -0.5, 3.0],
    [3.0,  0.0,  -1.0,  -1.5,  -1.5,  -1.0,  0.0, 3.0],
    [4.0, 2.0,  0.0,  0.0,  0.0,  0.0, 2.0, 4.0],
    [5.0, 4.0, 3.0, 3.0, 3.0, 3.0, 4.0, 5.0]
]

wBishopPoint=[
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
    ]
bBishopPoint=[
    [2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0],
    [1.0, -0.5, 0.0, 0.0, 0.0, 0.0, -0.5, 1.0],
    [1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0],
    [1.0, 0.0, -1.0, -1.0, -1.0, -1.0, 0.0, 1.0],
    [1.0, -0.5, -0.5, -1.0, -1.0, -0.5, -0.5, 1.0], 
    [1.0, 0.0, -0.5, -1.0, -1.0, -0.5, 0.0, 1.0],
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0]
    ]
wRookPoint=[
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
    ]
bRookPoint=[
    [0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0],
    [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5],
    [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5],
    [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5], 
    [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5],
    [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5], 
    [-0.5, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.5], 
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ]
wQueenPoint=[
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
    ]
bQueenPoint=[
    [2.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 2.0],
    [1.0, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0, 1.0], 
    [1.0, -0.5, -0.5, -0.5, -0.5, -0.5, 0.0, 1.0], 
    [0.0, 0.0, -0.5, -0.5, -0.5, -0.5, 0.0, 0.5], 
    [0.5, 0.0, -0.5, -0.5, -0.5, -0.5, 0.0, 0.5], 
    [1.0, 0.0, -0.5, -0.5, -0.5, -0.5, 0.0, 1.0], 
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], 
    [2.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 2.0]
    ]
wKingPoint=[
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
    [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
    ]
bKingPoint=[
    [-2.0, -3.0, -1.0, 0.0, 0.0, -1.0, -3.0, -2.0], 
    [-2.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -2.0], 
    [1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0], 
    [2.0, 3.0, 3.0, 4.0, 4.0, 3.0, 3.0, 2.0], 
    [3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0], 
    [3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0], 
    [3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0], 
    [3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0]
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

                    elif tempState[x][y] == "bKing" and ((newX, newY) == (0,6) or (newX, newY) == (0,1)):
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
    return -totalPoint
def miniMax(chess_state, depth= _DEPTH):
    state_value=maxState_Value(chess_state,depth)
    return state_value[0]
def maxState_Value(chess_state,depth):
    if depth==0 or rules.checkNoMove(chess_state,'b'):
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
    if depth==0 or rules.checkNoMove(chess_state,'w'):
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
# Vũ cắt tỉa :))
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
            
        