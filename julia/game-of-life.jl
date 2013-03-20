import Base.*
import Base.size
import Core.Array

type GOLBoard
    board
end

GOLBoard(w::Int, h::Int) = GOLBoard(round(rand(w, h)))
Array(g::GOLBoard) = g.board
size(g::GOLBoard) = size(Array(g))
buildBoard(w, h) = round(rand(h, w))

function updateBoard(g::GOLBoard)
    (h, w) = size(g)
    newBoard = zeros(w, h)

    for i = 1:h
        for j = 1:w
            newBoard[i, j] = updateCell(g, i, j)
        end
    end

    GOLBoard(newBoard)
end

function updateCell(g::GOLBoard, i, j)
    neighbors = countNeighbors(g, i, j)
    board = Array(g)
    newVal = board[i, j]

    if board[i, j] == 1
        if neighbors < 2 || neighbors > 3
            newVal = 0;
        end
    elseif neighbors == 3
        newVal = 1
    end

    newVal
end

withinBounds(A, low, high) = A[low .<= A .<= high]
withinBounds(A, high) = withinBounds(A, 1, high)

function countNeighbors(g, i, j)
    (h, w) = size(g)
    board = Array(g)

    rows = withinBounds([i-1 : i+1], h)
    cols = withinBounds([j-1 : j+1], w)

    sum(board[rows, cols]) - board[i, j]
end
