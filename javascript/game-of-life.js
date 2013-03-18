function initGame(iWidth, iHeight) {
    // Create an empty 2D array (i.e., an array of arrays).
    var arrGame = new Array(iHeight);
    var i, j;

    for (i = 0; i < iHeight; ++i) {
        arrGame[i] = new Array(iWidth);
    }

    for (i = 0; i < iHeight; ++i) {
        for (j = 0; j < iWidth; ++j) {
            arrGame[i][j] = Math.round(Math.random());
        }
    }

    return arrGame;
}

function countNeighbors(arrGame, iRow, iCol) {
    var tmp = [-1, 0, 1];
    var iNeighbors = 0;
    var iRows = arrGame.length;
    var iCols = arrGame[0].length;

    tmp.forEach(function (rowOffset) {
        tmp.forEach(function (colOffset) {
            var row = iRow + rowOffset;
            var col = iCol + colOffset;

            if (row !== iRow || col !== iCol)
                if (row >= 0 && row < iRows && col >= 0 && col < iCols)
                    iNeighbors += arrGame[row][col];
        });
    });

    return iNeighbors;
}

function ageGame(arrGame) {
    var iHeight = arrGame.length;
    var iWidth = arrGame[0].length;
    var newGame = copyArray(arrGame);

    arrGame.forEach(function (row, i) {
        row.forEach(function (val, j) {
            var iNeighbors = countNeighbors(arrGame, i, j);
            var bIsAlive = newGame[i][j];

            if (bIsAlive) {
                if (iNeighbors < 2 || iNeighbors > 3)
                    newGame[i][j] = 0;
            } else if (iNeighbors === 3) {
                newGame[i][j] = 1;
            }
        });
    });

    return newGame;
}

function gameIsComplete(currGame, prevGame) {
    var bGameIsComplete = true;
    var iRows = currGame.length;
    var iCols = currGame[0].length;
    var i = 0;
    var j = 0;

    while (bGameIsComplete && i < iRows) {
        j = 0;

        while (bGameIsComplete && j < iCols) {
            bGameIsComplete = (currGame[i][j] === prevGame[i][j]);
            ++j;
        }

        ++i;
    }

    return bGameIsComplete;
}

function buildBoard(arrGame) {
    // The HTML for the board will be stored in a string. That string
    // must start with the opening table tag.
    var htmlTable = '<table>';
    var numRows = arrGame.length;
    var numCols = arrGame[0].length;

    // Loop through the rows to build one row at a time.
    for (var i = 0; i < numRows; ++i) {
        // A row starts with the appropriate opening tag.
        htmlTable += '<tr>';

        // Loop through the columns to build one cell at a time for
        // the current row.
        for (var j = 0; j < numCols; ++j) {
            // For now, each cell will be empty.
            htmlTable += '<td';

            if (arrGame[i][j] === 1)
                htmlTable += ' style="background-color: black;"';

            htmlTable += '></td>';
        }

        // Finish this row.
        htmlTable += '</tr>';
    }

    // Finish the table.
    htmlTable += '</table>';

    // Return the string containing the table.
    return htmlTable;
}

function copyArray(arr) {
    var newArr = new Array(arr.length);

    arr.forEach(function (row, idx) {
        newArr[idx] = [].concat(row);
    });

    return newArr;
}

function iterateGame(currGame, delay) {
    var newGame = copyArray(currGame);

    newGame = ageGame(currGame);

    document.getElementById('divBoard').innerHTML = buildBoard(newGame);

    if (!gameIsComplete(currGame, newGame))
        setTimeout(iterateGame, delay, newGame, delay);
}
