from cmu_graphics import *

# Draw the board
blackRow = False #keeps track of whether the black squares need to be offset

def drawX(row): #draws one row
    if (row):
        x = 0
    else:
        x = 50
    while(x <= 350):
        Rect(x,y,50,50)
        x += 100
y = 0

#draws the board by repeatedly calling drawX()
while(y <= 350):
    drawX(blackRow)
    if (blackRow):
        blackRow = False
    else:
        blackRow = True
    y += 50

##Create the pieces##

#initialize team arrays
blackPieces = []
whitePieces = []

def drawKing(x, y, color):
    king = Group(
        Circle(168,25,10),
        Circle(182,25,10),
        Rect(161,25,29,20),
        Line(175,25, 175,8),
        Line(170,12, 180,12)
        )
    king.fill = color
    king.centerX = x
    king.centerY = y
    king.type = 'king'
    return king

#store kings in separate variables to make them easier to access later (such as when checking checkmate)
blackKing = drawKing(225,25,'darkslategrey')
blackPieces.append(blackKing)

whiteKing = drawKing(225,375,'mocassin')
whitePieces.append(whiteKing)

def drawQueen(x, y, color):
    queen = Group(
        Rect(160,30, 30, 14),
        Polygon(160,30, 155,20, 165,30, 163,15, 171.5,30, 175,10, 178.5,30, 188,15, 185,30, 195,20, 190,30),
        Circle(155,20,2),
        Circle(163,15,2),
        Circle(175,10,2),
        Circle(188,15,2),
        Circle(195,20,2)
        )
    queen.fill = color
    queen.color = color #since queens use a bishop function, they need to have color as well as fill
    queen.centerX = x
    queen.centerY = y
    queen.type = 'queen'
    return queen

blackPieces.append(drawQueen(175, 25, 'darkslategrey'))
whitePieces.append(drawQueen(175, 375, 'mocassin'))

def drawBishop(x, y, color):
    bishop = Group(
        Circle(125,25, 15),
        Rect(125,30, 25,14, align='top'),
        Circle(125,10,5),
        Line(120,23, 130,23),
        Line(125,28, 125,18)
        )
    for shape in bishop.children:
        if (isinstance(shape, Line)):
            if (color == 'darkslategrey'):
                shape.fill = 'white'
            else:
                shape.fill = 'black'
        else:
            shape.fill = color
    bishop.color = color #the cross results in no group.fill so bishops store color separately
    bishop.centerX = x
    bishop.centerY = y
    bishop.type = 'bishop'
    return bishop

blackPieces.append(drawBishop(125, 25, 'darkslategrey'))
blackPieces.append(drawBishop(275, 25, 'darkslategrey'))

whitePieces.append(drawBishop(125, 375, 'mocassin'))
whitePieces.append(drawBishop(275, 375, 'mocassin'))
    
def drawRook(x, y, color):
    rook = Group(
        Rect(15,20,25,25),
        Rect(10,10,5,10),
        Rect(40,10,5,10),
        Rect(20,10,5,10),
        Rect(30,10,5,10),
        Rect(12.5,16,30,6)
        )
    rook.centerX = x
    rook.centerY = y
    rook.fill = color
    rook.type = 'rook'
    return rook

blackPieces.append(drawRook(25, 25, 'darkslategrey'))
blackPieces.append(drawRook(375, 25, 'darkslategrey'))

whitePieces.append(drawRook(25, 375, 'mocassin'))
whitePieces.append(drawRook(375, 375, 'mocassin'))

def drawKnight(x, y, color):
    knight = Group(
        Arc(75, 25, 25, 35, -20, 160),
        Oval(71, 16, 20, 10, rotateAngle=-40),
        Arc(83,36, 25, 25, -90, 70),
        Rect(65,36, 23, 10)
        )
    knight.centerX = x
    knight.centerY = y
    knight.fill = color
    knight.type = 'knight'
    return knight

blackPieces.append(drawKnight(75, 25, 'darkslategrey'))
blackPieces.append(drawKnight(325, 25, 'darkslategrey'))

whitePieces.append(drawKnight(75,375, 'mocassin'))
whitePieces.append(drawKnight(325,375, 'mocassin'))

def drawPawn(x, y, color):
    pawn = Group(
        Rect(10,80,30,10),
        Polygon(15,80, 25,60, 35,80),
        Circle(25,60,7)
        )
    pawn.centerX = x
    pawn.centerY = y
    pawn.fill = color
    pawn.type = 'pawn'
    return pawn

#store the pawns with a loop, because there are a lot of them
x = 25
while (x < 400):
    blackPieces.append(drawPawn(x, 75, 'darkslategrey'))
    whitePieces.append(drawPawn(x, 325, 'mocassin'))
    x += 50

# Piece movement functions #

#initialize move list variable
app.moves = []

def drawMove(x, y):
    if (not getPiece(x, y)):
        move = Rect(x, y, 50, 50, fill='green', opacity=50, align='center')
        move.type = 'move'
        app.moves.append(move)
        return True #return that it's a valid move
    else:
        return False #return that something prevented the move
        #important when drawing moves along a line

def drawCapture(x, y, color):
    if (getPiece(x, y)):
        if (getPiece(x, y).type == 'bishop'): #bishops have no fill, so they use a different check
            targetColor = getPiece(x, y).color
        else: #if it isn't a bishop, we can just use the fill
            targetColor = getPiece(x, y).fill
        
        if (targetColor != color): #it's an enemy piece and can be captured
            cap = Rect(x, y, 50, 50, fill='yellow', opacity=50, align='center')
            cap.type = 'capture'
            
            #get the target
            cap.toBack() #get the capture out of the way, so getPiece() won't detect it instead
            cap.target = getPiece(cap.centerX, cap.centerY)
            cap.toFront() #put the capture back in front, so you can select it later
            app.moves.append(cap)
            return cap

def getPiece(x, y):
    try:
        #if it has a type, it's a piece. Otherwise, it will throw an exception
        if (app.group.hitTest(x, y).type):
            return app.group.hitTest(x, y)
    except AttributeError:
        return None #if it threw the exception that it had no type attribute, it isn't a piece
        # and therefore this should return no piece
    except KeyError: #there seem to be two different types of exceptions for the same thing
        return None

def getPawnMoves(pawn):
    if pawn.fill == 'mocassin': #if it's a white pawn
        if (drawMove(pawn.centerX, pawn.centerY-50) and (pawn.centerY == 325)):
            #if it's currently on the home row, and it was possible to draw the normal move,
            drawMove(pawn.centerX, pawn.centerY-100) #draw the bonus move (to move two spaces)
            #since drawMove draws the move and then returns whether we drew it, we draw the normal move
            #when we call drawMove inside the if loop
            #so basically it's 'draw the move, then if we did successfully, we can draw the other one'
            
        #check for captures
        drawCapture(pawn.centerX-50, pawn.centerY-50, pawn.fill)
        checkPassent(pawn.centerX-50, pawn.centerY-50) #we check en passent inside getPawnMoves because
                                                        #pawns capture differently than other pieces
        drawCapture(pawn.centerX+50, pawn.centerY-50, pawn.fill)
        checkPassent(pawn.centerX+50, pawn.centerY-50)
    else:
        #it's a black pawn
        if (drawMove(pawn.centerX, pawn.centerY+50) and (pawn.centerY == 75)):
            drawMove(pawn.centerX, pawn.centerY+100)
            #we bascially do the same thing except in the other direction
            
        drawCapture(pawn.centerX-50, pawn.centerY+50, pawn.fill)
        checkPassent(pawn.centerX-50, pawn.centerY+50)
        
        drawCapture(pawn.centerX+50, pawn.centerY+50, pawn.fill)
        checkPassent(pawn.centerX+50, pawn.centerY+50)
        
def getRookMoves(rook):
    #starting at the space to the right, project moves along a line until we hit something
    x = rook.centerX+50
    while x < 400:
        if (drawMove(x, rook.centerY)):
            x += 50
        else:
            drawCapture(x, rook.centerY, rook.fill) #if it hit an enemy, it'll draw a capture
            #if it didn't hit an enemy, the capture fails to draw. This is why we pass it the fill.
            break
        
    x = rook.centerX-50
    while x > 0:
        if (drawMove(x, rook.centerY)):
            x -= 50
        else:
            drawCapture(x, rook.centerY, rook.fill)
            break
        
    y = rook.centerY+50
    while y < 400:
        if (drawMove(rook.centerX, y)):
            y += 50
        else:
            drawCapture(rook.centerX, y, rook.fill)
            break
        
    y = rook.centerY-50
    while y > 0:
        if (drawMove(rook.centerX, y)):
            y -= 50
        else:
            drawCapture(rook.centerX, y, rook.fill)
            break
        
def getBishopMoves(bishop):
    x = bishop.centerX+50
    y1 = bishop.centerY-50
    y2 = bishop.centerY+50
    y1stop = False
    y2stop = False
    #this projects both diagonals on the same side of the bishop simultaneously
    #as long as at least one diagonal hasn't stopped, and it's not going off the board, it continues
    while x < 400 and (not y1stop or not y2stop):
        if (not y1stop):
            if drawMove(x, y1):
                y1 -= 50
            else:
                drawCapture(x, y1, bishop.color)
                y1stop = True
        if (not y2stop):
            if (drawMove(x, y2)):
                y2 += 50
            else:
                drawCapture(x, y2, bishop.color)
                y2stop = True
        x += 50
    x = bishop.centerX-50
    y1 = bishop.centerY-50
    y2 = bishop.centerY+50
    y1stop = False
    y2stop = False
    while x > 0 and (not y1stop or not y2stop):
        if (not y1stop):
            if (drawMove(x, y1)):
                y1 -= 50
            else:
                drawCapture(x, y1, bishop.color)
                y1stop = True
        if not y2stop:
            if drawMove(x, y2):
                y2 += 50
            else:
                drawCapture(x, y2, bishop.color)
                y2stop = True
        x -= 50

def getKnightMoves(knight):
    x = knight.centerX
    y = knight.centerY
    #knights are pretty simple because they don't care about other pieces unless those pieces are
    #on the space they are trying to go
    if not drawMove(x-100, y-50):
        drawCapture(x-100, y-50, knight.fill)
    if not drawMove(x-100, y+50):
        drawCapture(x-100, y+50, knight.fill)
        
    if not drawMove(x+100, y-50):
        drawCapture(x+100, y-50, knight.fill)
    if not drawMove(x+100, y+50):
        drawCapture(x+100, y+50, knight.fill)
        
    if not drawMove(x+50, y-100):
        drawCapture(x+50, y-100, knight.fill)
    if not drawMove(x+50, y+100):
        drawCapture(x+50, y+100, knight.fill)
        
    if not drawMove(x-50, y-100):
        drawCapture(x-50, y-100, knight.fill)
    if not drawMove(x-50, y+100):
        drawCapture(x-50, y+100, knight.fill)
        
def detectThreat(x, y, color):
    #this detects threats using a slightly modified version of the movement algorithms
    #instead of actually projecting moves, it simply checks if the move would hit a piece
    #since basically all moves are reversible; if a rook can capture another rook, that rook could also
        #capture it
    
    #store the original coordinates
    storeX = x
    storeY = y
    
    #detect rook (or queen along horiz/vert)
    y = storeY
    x = storeX + 50
    while x < 400:
        if (not getPiece(x, y)):
            x += 50
        else:
            if (getPiece(x, y).type == 'rook') or (getPiece(x, y).type == 'queen'):
                if (getPiece(x,y).fill != color):
                    return True
            break
    
    y = storeY    
    x = storeX-50
    while x > 0:
        if (not getPiece(x, y)):
            x -= 50
        else:
            if (getPiece(x,y).type == 'rook') or (getPiece(x,y).type == 'queen'):
                if (getPiece(x,y).fill != color):
                    return True
            break
    
    x = storeX    
    y = storeY+50
    while y < 400:
        if (not getPiece(x, y)):
            y += 50
        else:
            if (getPiece(x,y).type == 'queen') or (getPiece(x,y).type == 'rook'):
                if (getPiece(x,y).fill != color):
                    return True
            break
        
    x = storeX
    y = storeY-50
    while y > 0:
        if (not getPiece(x, y)):
            y -= 50
        else:
            if (getPiece(x,y).type == 'queen') or (getPiece(x,y).type == 'rook'):
                if (getPiece(x,y).fill != color):
                    return True
            break
    
    #detect bishop (or queen along diagonal)
    x = storeX
    y = storeY
    
    x += 50
    y1 = y-50
    y2 = y+50
    y1stop = False
    y2stop = False
    while x < 400:
        #y1
        if not y1stop:
            if not getPiece(x, y1):
                y1 -= 50
            else:
                if (getPiece(x,y1).type == 'bishop') or (getPiece(x,y1).type == 'queen'):
                    if (getPiece(x,y1).color != color):
                        return True
                y1stop = True
    
        #y2
        if not y2stop:
            if (not getPiece(x, y2)):
                y2 += 50
            else:
                if (getPiece(x,y2).type == 'bishop') or (getPiece(x,y2).type == 'queen'):
                    if (getPiece(x,y2).color != color):
                        return True
                y2stop = True
            
        x += 50
        
        if y1stop and y2stop:
            break
    
    x = storeX-50
    y1 = storeY-50
    y2 = storeY+50
    y1stop = False
    y2stop = False
    while x > 0:
        #y1
        if not y1stop:
            if (not getPiece(x, y1)):
                y1 -= 50
            else:
                if (getPiece(x,y1).type == 'bishop') or (getPiece(x,y1).type == 'queen'):
                    if (getPiece(x,y1).color != color):
                        return True
                y1stop = True
        #y2
        if not y2stop:
            if not (getPiece(x, y2)):
                y2 += 50
            else:
                if (getPiece(x,y2).type == 'bishop') or (getPiece(x,y2).type == 'queen'):
                    if (getPiece(x,y2).color != color):
                        return True
                y2stop = True
        
        x -= 50
        
        if y1stop and y2stop:
            break
    
    #detect knight
    x = storeX
    y = storeY
    if getPiece(x-100, y-50):
        if (getPiece(x-100, y-50).type == 'knight'):
            if (getPiece(x-100, y-50).fill != color):
                return True
    if getPiece(x-100, y+50):
        if (getPiece(x-100, y+50).type == 'knight'):
            if (getPiece(x-100, y+50).fill != color):
                return True
    if getPiece(x+100, y-50):
        if (getPiece(x+100, y-50).type == 'knight'):
            if (getPiece(x+100, y-50).fill != color):
                return True
    if getPiece(x+100, y+50):
        if (getPiece(x+100, y+50).type == 'knight'):
            if (getPiece(x+100, y+50).fill != color):
                return True
    if getPiece(x+50, y-100):
        if (getPiece(x+50, y-100).type == 'knight'):
            if (getPiece(x+50, y-100).fill != color):
                return True
    if getPiece(x+50, y+100):
        if (getPiece(x+50, y+100).type == 'knight'):
            if (getPiece(x+50, y+100).fill != color):
                return True
    if getPiece(x-50, y-100):
        if (getPiece(x-50, y-100).type == 'knight'):
            if (getPiece(x-50, y-100).fill != color):
                return True
    if getPiece(x-50, y+100):
        if (getPiece(x-50, y+100).type == 'knight'):
            if (getPiece(x-50, y+100).fill != color):
                return True
    
    #detect pawn
    if color == 'mocassin':
        if (getPiece(x-50, y-50)):
            if getPiece(x-50, y-50).type == 'pawn':
                if getPiece(x-50, y-50).fill != color:
                    return True
        if (getPiece(x+50, y-50)):
            if getPiece(x+50, y-50).type == 'pawn':
                if getPiece(x+50, y-50).fill != color:
                    return True
    else:
        if (getPiece(x-50, y+50)):
            if getPiece(x-50, y+50).type == 'pawn':
                if getPiece(x-50, y+50).fill != color:
                    return True
        if (getPiece(x+50, y+50)):
            if getPiece(x+50, y+50).type == 'pawn':
                if getPiece(x+50, y+50).fill != color:
                    return True
    
    #detect opposing king
    if (getPiece(x, y-50)):
        if getPiece(x, y-50).type == 'king':
            if getPiece(x, y-50).fill != color:
                return True
    if (getPiece(x+50, y-50)):
        if getPiece(x+50, y-50).type == 'king':
            if getPiece(x+50, y-50).fill != color:
                return True
    if getPiece(x+50, y):
        if getPiece(x+50, y).type == 'king':
            if getPiece(x+50, y).fill != color:
                return True
    if getPiece(x+50, y+50):
        if getPiece(x+50, y+50).type == 'king':
            if getPiece(x+50, y+50).fill != color:
                return True
    if getPiece(x, y+50):
        if getPiece(x, y+50).type == 'king':
            if getPiece(x, y+50).fill != color:
                return True
    if getPiece(x-50, y+50):
        if getPiece(x-50, y+50).type == 'king':
            if getPiece(x-50, y+50).fill != color:
                return True
    if getPiece(x-50, y):
        if getPiece(x-50, y).type == 'king':
            if getPiece(x-50, y).fill != color:
                return True
    if getPiece(x-50, y-50):
        if getPiece(x-50, y-50).type == 'king':
            if getPiece(x-50, y-50).fill != color:
                return True
    
    #if you've made it here, nothing has returned true, and so the square isn't threatened
    return False

#initialize castling trackers
app.bCanCastle = True
app.wCanCastle = True
    
def getKingMoves(king):
    #this just tries to put a move in each spot adjacent to the king, but it can only do that if the
    #square isn't threatened
    
    #also, castling
    for x in range(king.centerX+50, 400, 50):
        if getPiece(x, king.centerY):
            if getPiece(x, king.centerY).type == 'rook':
                if x == 375 and (not app.check):
                    if king.fill == 'mocassin':
                        if (king.centerY == 375) and app.wCanCastle:
                            castle = drawRook(375, 375, 'green')
                            castle.toBack()
                            castle.target = getPiece(375, 375)
                            castle.toFront()
                            castle.opacity = 50
                            castle.type = 'castle'
                            app.moves.append(castle)
                    elif king.fill == 'darkslategrey':
                        if (king.centerY == 25) and app.bCanCastle:
                            castle = drawRook(375, 25, 'green')
                            castle.toBack()
                            castle.target = getPiece(375, 25)
                            castle.toFront()
                            castle.opacity = 50
                            castle.type = 'castle'
                            app.moves.append(castle)
            break
    
    x = king.centerX - 50
    while x > 0:
        if getPiece(x, king.centerY):
            if getPiece(x, king.centerY).type == 'rook':
                if x == 25 and (not app.check):
                    if king.fill == 'mocassin':
                        if (king.centerY == 375) and app.wCanCastle:
                            castle = drawRook(25, 375, 'green')
                            castle.toBack()
                            castle.target = getPiece(25, 375)
                            castle.toFront()
                            castle.opacity = 50
                            castle.type = 'castle'
                            app.moves.append(castle)
                    elif king.fill == 'darkslategrey':
                        if (king.centerY == 25) and app.bCanCastle:
                            castle = drawRook(25, 25, 'green')
                            castle.toBack()
                            castle.target = getPiece(25, 25)
                            castle.toFront()
                            castle.opacity = 50
                            castle.type = 'castle'
                            app.moves.append(castle)
            break
        else:
            x -= 50
    
    x = king.centerX
    y = king.centerY
    king.visible = False #to prevent the king from interposing himself
    if (not detectThreat(x, y-50, king.fill)):
        if not drawMove(x, y-50):
            drawCapture(x, y-50, king.fill)
    for move in app.moves:
        move.toBack()
    if (not detectThreat(x+50, y-50, king.fill)):
        if not drawMove(x+50, y-50):
            drawCapture(x+50, y-50, king.fill)
    for move in app.moves:
        move.toBack()
    if not detectThreat(x+50, y, king.fill):
        if not drawMove(x+50, y):
            drawCapture(x+50, y, king.fill)
    for move in app.moves:
        move.toBack()
    if not detectThreat(x+50, y+50, king.fill):
        if not drawMove(x+50, y+50):
            drawCapture(x+50, y+50, king.fill)
    for move in app.moves:
        move.toBack()
    if not detectThreat(x, y+50, king.fill):
        if not drawMove(x, y+50):
            drawCapture(x, y+50, king.fill)
    for move in app.moves:
        move.toBack()
    if not detectThreat(x-50, y+50, king.fill):
        if not drawMove(x-50, y+50):
            drawCapture(x-50, y+50, king.fill)
    for move in app.moves:
        move.toBack()
    if not detectThreat(x-50, y, king.fill):
        if not drawMove(x-50, y):
            drawCapture(x-50, y, king.fill)
    for move in app.moves:
        move.toBack()
    if not detectThreat(x-50, y-50, king.fill):
        if not drawMove(x-50, y-50):
            drawCapture(x-50, y-50, king.fill)
    for move in app.moves:
        move.toFront()
    king.visible = True
    
def clearMoves():
    for move in app.moves:
        app.group.remove(move)
    app.moves.clear()

def movePiece(piece, move):
    savedX = piece.centerX
    savedY = piece.centerY
    if move.type == 'capture':
        savedPiece = move.target #save the target of the move, in case we need to roll it back
    else:
        savedPiece = None
    
    if move.type == 'castle':
        if (move.centerX > piece.centerX):
            piece.centerX += 100
            move.target.centerX = piece.centerX-50
        else:
            piece.centerX -= 100
            move.target.centerX = piece.centerX+50
        castled = True

    else:
        piece.centerX = move.centerX
        piece.centerY = move.centerY
        castled = False
        
    clearMoves()
    
    moveReversed = False
    
    #after moving, if the king was in check, make sure you moved out of check
    if app.turn:
        if detectThreat(whiteKing.centerX, whiteKing.centerY, whiteKing.fill):
            #if the king is still in check, you made an invalid move and it needs to be reversed
            piece.centerX = savedX
            piece.centerY = savedY
            if savedPiece:
                savedPiece.visible = True #make the piece reappear
                savedPiece = None
            app.selection = None
            print("Invalid move! The king needs to be out of check!")
            castled = False
            moveReversed = True
            
        else:
            app.check = False
            if castled:
                app.wCanCastle = False
    else:
        if detectThreat(blackKing.centerX, blackKing.centerY, blackKing.fill):
            piece.centerX = savedX
            piece.centerY = savedY
            if savedPiece:
                savedPiece.visible = True
                savedPiece = None
            app.selection = None
            print("Invalid move! The king needs to be out of check!")
            castled = False
            moveReversed = True
        
        else:
            app.check = False
            if castled:
                app.bCanCastle = False
                
    #also, if you moved a pawn two spaces, drop an en passent marker
    if piece.type == 'pawn':
        if abs(piece.centerY - savedY) > 50:
            passent = Circle(piece.centerX, savedY+((savedY-piece.centerY)/-2), 1, fill=None)
            passent.target = piece
            if piece.fill == 'mocassin':
                app.wPassent = passent
            else:
                app.bPassent = passent
    
    #check for pawn promotions
    for x in range (25, 375, 50):
        if app.turn:
            if getPiece(x, 25):
                if getPiece(x, 25).type == 'pawn' and getPiece(x, 25) in whitePieces:
                    promotePawn(getPiece(x, 25))
                    break
        else:
            if getPiece(x, 375):
                if getPiece(x, 375).type == 'pawn' and getPiece(x, 375) in blackPieces:
                    promotePawn(getPiece(x, 375))
                    break
    
    if (not app.check) and (not app.promoting) and (not moveReversed):
        newTurn() #only pass the turn if your move wasn't reversed
        #also, if it's promoting a pawn, the turn needs to remain on the same turn so that the pawn
        #can be promoted
    
def deletePiece(piece):
    if (piece in blackPieces):
        blackPieces.remove(piece)
    elif (piece in whitePieces):
        whitePieces.remove(piece)
    app.group.remove(piece)

#initialize promotion variables
app.promoting = False #marker to change app behavior while promoting the pawn
promoteScreen = Rect(0,0,400,400, fill='white', opacity = 75, visible = False)
promoteScreen.buttons = []

def promotePawn(pawn):
    app.promoting = True
    promoteScreen.visible = True
    promoteScreen.buttons.append(drawQueen(50, 200, pawn.fill))
    promoteScreen.buttons.append(drawBishop(150, 200, pawn.fill))
    promoteScreen.buttons.append(drawKnight(250, 200, pawn.fill))
    promoteScreen.buttons.append(drawRook(350, 200, pawn.fill))
    app.selection = pawn

#initialize selection and turn
app.selection = None
app.turn = True #true is white, false is black
app.check = False

#initialize white and black en passent markers
app.wPassent = None
app.bPassent = None

checkMark = drawKing(0, 0, 'red')
checkMark.type = None
checkMark.visible = False

def newTurn():
    #pass the turn
    app.turn = not app.turn
    blackKing.opacity = 100
    whiteKing.opacity = 100
    
    if app.turn:
        #check for check
        if detectThreat(whiteKing.centerX, whiteKing.centerY, whiteKing.fill):
            app.check = True
            print("White is in check!")
            detectMate()
            checkMark.centerX = whiteKing.centerX
            checkMark.centerY = whiteKing.centerY
            checkMark.visible = True
            whiteKing.toFront()
            whiteKing.opacity = 60
        else:
            app.check = False
            checkMark.visible = False
        #clear en passent marker
        if app.wPassent:
            app.group.remove(app.wPassent)
            app.wPassent = None
    else:
        #check for check
        if detectThreat(blackKing.centerX, blackKing.centerY, blackKing.fill):
            app.check = True
            print("Black is in check!")
            detectMate()
            checkMark.centerX = blackKing.centerX
            checkMark.centerY = blackKing.centerY
            checkMark.visible = True
            blackKing.toFront()
            blackKing.opacity = 60
        else:
            app.check = False
            checkMark.visible = False
        #clear en passent marker
        if app.bPassent:
            app.group.remove(app.bPassent)
            app.bPassent = None
        #also, clear the black en passent marker, if there is one
    
    app.selection = None
    
    if len(whitePieces) == 1 and len(blackPieces) == 1:
        if (whitePieces[0] == whiteKing) and (blackPieces[0] == blackKing):
            promoteScreen.visible = True
            promoteScreen.opacity = 50
            Label("Stalemate!", 200, 200, fill='red', size=50)
            app.stop()

def checkPassent(x, y):
    if app.turn:
        if (app.bPassent):
            if (x == app.bPassent.centerX) and (y == app.bPassent.centerY):
                passentCap = Rect(x, y, 50, 50, fill='yellow', opacity=50, align='center')
                passentCap.type = 'capture'
                passentCap.target = app.bPassent.target
                app.moves.append(passentCap)
                return True
            
    else:
        if app.wPassent:
            if (x == app.wPassent.centerX) and (y == app.wPassent.centerY):
                passentCap = Rect(x, y, 50, 50, fill='yellow', opacity=50, align='center')
                passentCap.type = 'capture'
                passentCap.target = app.wPassent.target
                app.moves.append(passentCap)
                return True
    
    return False #only runs if it didn't return true, because returning ends the function

#using a small quirk in the code I encountered earlier, I can use the move projection to detect if 
    #a move could allow the king to get out of check, because the check detector allows projected moves
    #to interpose!
def detectMate():
    if app.turn:
        for piece in whitePieces:
            if (piece.type == 'pawn'):
                getPawnMoves(piece)
            elif (piece.type == 'rook'):
                getRookMoves(piece)
            elif (piece.type == 'bishop'):
                getBishopMoves(piece)
            elif (piece.type == 'queen'):
                getRookMoves(piece)
                getBishopMoves(piece)
            elif (piece.type == 'king'):
                getKingMoves(piece)
            elif (piece.type == 'knight'):
                getKnightMoves(piece)
        if detectThreat(whiteKing.centerX, whiteKing.centerY, whiteKing.fill):
            clearMoves()
            getKingMoves(whiteKing)
            for move in app.moves[:]:
                if (move.centerX > 400) or (move.centerX < 0) or (move.centerY > 400) or (move.centerY < 0):
                    app.moves.remove(move)
                    app.group.remove(move)
            if (len(app.moves) == 0):
                endGame()
    else:
        for piece in blackPieces:
            if (piece.type == 'pawn'):
                getPawnMoves(piece)
            elif (piece.type == 'rook'):
                getRookMoves(piece)
            elif (piece.type == 'bishop'):
                getBishopMoves(piece)
            elif (piece.type == 'queen'):
                getRookMoves(piece)
                getBishopMoves(piece)
            elif (piece.type == 'king'):
                getKingMoves(piece)
            elif (piece.type == 'knight'):
                getKnightMoves(piece)
        if detectThreat(blackKing.centerX, blackKing.centerY, blackKing.fill):
            clearMoves()
            getKingMoves(blackKing)
            for move in app.moves[:]:
                if (move.centerX >= 400) or (move.centerX <= 0) or (move.centerY >= 400) or (move.centerY <= 0):
                    app.moves.remove(move)
                    app.group.remove(move)
            
            if (len(app.moves) == 0):
                endGame()

    clearMoves()

def endGame():
    if app.turn:
        promoteScreen.visible = True
        promoteScreen.opacity = 50
        Label("Black wins!", 200, 200, fill='red', size=50)
        app.stop()
    else:
        promoteScreen.visible = True
        promoteScreen.opacity = 50
        Label("White wins!", 200, 200, fill='red', size=50)
        app.stop()

def onMousePress(mouseX, mouseY):
    if (getPiece(mouseX, mouseY)):
        if (app.selection):
            if app.promoting:
                if getPiece(mouseX, mouseY).type == 'rook':
                    if app.selection in whitePieces:
                        whitePieces.append(drawRook(app.selection.centerX, app.selection.centerY, app.selection.fill))
                    else:
                        blackPieces.append(drawRook(app.selection.centerX, app.selection.centerY, app.selection.fill))
                elif getPiece(mouseX, mouseY).type == 'knight':
                    if app.selection in whitePieces:
                        whitePieces.append(drawKnight(app.selection.centerX, app.selection.centerY, app.selection.fill))
                    else:
                        blackPieces.append(drawKnight(app.selection.centerX, app.selection.centerY, app.selection.fill))
                elif getPiece(mouseX, mouseY).type == 'bishop':
                    if app.selection in whitePieces:
                        whitePieces.append(drawBishop(app.selection.centerX, app.selection.centerY, app.selection.fill))
                    else:
                        blackPieces.append(drawBishop(app.selection.centerX, app.selection.centerY, app.selection.fill))
                elif getPiece(mouseX, mouseY).type == 'queen':
                    if app.selection in whitePieces:
                        whitePieces.append(drawQueen(app.selection.centerX, app.selection.centerY, app.selection.fill))
                    else:
                        blackPieces.append(drawQueen(app.selection.centerX, app.selection.centerY, app.selection.fill))
                deletePiece(app.selection)
                #clear settings, promotion is over
                app.selection = None
                app.promoting = False
                promoteScreen.visible = False
                for item in promoteScreen.buttons:
                    deletePiece(item)
                promoteScreen.buttons.clear
                app.turn = not app.turn
            
            elif (getPiece(mouseX, mouseY) in app.moves):
                move = getPiece(mouseX, mouseY)
                if (move.type == 'capture'):
                    deletePiece(move.target)
                movePiece(app.selection, move)
            
        else:
            #select a piece, only if it's the correct turn
            if app.turn:
                if (getPiece(mouseX, mouseY).type != 'bishop'):
                    if getPiece(mouseX, mouseY).fill == 'mocassin':
                        app.selection = getPiece(mouseX, mouseY)
                else:
                    if getPiece(mouseX, mouseY).color == 'mocassin':
                        app.selection = getPiece(mouseX, mouseY)
            else:
                if (getPiece(mouseX, mouseY).type != 'bishop'):
                    if getPiece(mouseX, mouseY).fill == 'darkslategrey':
                        app.selection = getPiece(mouseX, mouseY)
                else:
                    if getPiece(mouseX, mouseY).color == 'darkslategrey':
                        app.selection = getPiece(mouseX, mouseY)
            if app.selection:
                if (app.selection.type == 'pawn'):
                    getPawnMoves(app.selection)
                elif (app.selection.type == 'rook'):
                    getRookMoves(app.selection)
                elif (app.selection.type == 'bishop'):
                    getBishopMoves(app.selection)
                elif (app.selection.type == 'queen'):
                    getRookMoves(app.selection)
                    getBishopMoves(app.selection)
                elif (app.selection.type == 'king'):
                    getKingMoves(app.selection)
                elif (app.selection.type == 'knight'):
                    getKnightMoves(app.selection)
                #check en passent for non-pawn pieces (pawns use their function)
                if app.selection.type != 'pawn':
                    for move in app.moves:
                        if(checkPassent(move.centerX, move.centerY)):
                            break
                #delete all moves out of bounds
                for move in app.moves[:]:
                    if (move.centerX > 400) or (move.centerX < 0) or (move.centerY > 400) or (move.centerY < 0):
                        #if the move is out of bounds
                        app.moves.remove(move)
                        app.group.remove(move)
                #deselect a piece with no moves
                if len(app.moves) == 0:
                    print("That piece has no valid moves!")
                    app.selection = None

def onKeyPress(key):
    if key == 'space':
        #clear your selection, allowing you to choose another piece
        clearMoves()
        app.selection = None
    elif key == 'g':
        detectThreat(225, 175, 'darkslategrey')

def onKeyHold(keys):
    if ('c' in keys) and ('space' in keys) and ('enter' in keys):
        endGame()
        #c+space+enter concedes the game