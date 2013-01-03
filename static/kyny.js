// Words list downloaded from: http://www.gutenberg.org/ebooks/3201

var canvas,
    context,
    grid_size = 7,
    side = 500,
    squares = new Array(grid_size * grid_size),
    selected = [],
    found = [],
    pisteet = 0,
    checkButton,
    consonants = "BBCCDDFFGGHHHJKLLMMNNNPPQRRRSSSTTTVVWWXZ",
    vowels = "AAAEEEIIIOOOUUYY";
    // TODO: jaa aakkoset vokaaleihin ja konsonantteihin ja pistä joka toiseen
    // ruutuun aina vokaali ja joka toiseen konsonantti

function getLetter(nth) {
    if (nth % 2 == 0) {
        return vowels[Math.floor(Math.random() * vowels.length)];
    } else {
        return consonants[Math.floor(Math.random() * consonants.length)];
    }
}

function emptySquare(square) {
    context.beginPath();
    context.fillStyle = "#333333";
    context.fillRect(square.x, square.y, square.width, square.height);
    context.font = "30px courier";
    context.fillStyle = "#bbbbbb";
    context.fillText(square.letter, square.x 
        + (side / grid_size) / 2 - 5, square.y 
        + (side / grid_size) / 2);
    context.closePath();
    context.stroke();
    context.fill();
}

function hilightSquare(square) {
    context.beginPath();
    context.fillStyle = "#bbbbbb";
    context.fillRect(square.x, square.y, square.width, square.height);
    context.font = "30px courier";
    context.fillStyle = "#333333";
    context.fillText(square.letter, square.x 
        + (side / grid_size) / 2 - 5, square.y 
        + (side / grid_size) / 2, 50);
    context.closePath();
    context.stroke();
    context.fill();
}

function checkValid(square) {
    if (selected.length > 0) {
        var square_x = Math.floor(square.x / (side / grid_size));
        var square_y = Math.floor(square.y / (side / grid_size));
        var last_x = Math.floor(selected[selected.length - 1].x / (side / grid_size));
        var last_y = Math.floor(selected[selected.length - 1].y / (side / grid_size));
        if (Math.abs(square_x - last_x) <= 1 && Math.abs(square_y - last_y) <= 1) {
            return true;
        } else {
            return false;
        }
    } else {
        return true;
    }
}

function updateScore() {
    context.beginPath();
    context.font = "36px courier";
    context.clearRect(500, 0, 300, 500);
    context.fillStyle = "#333333";
    context.fillText("SCORE", 650, 33, 280);
    context.fillText(pisteet, 650, 69, 280);
    context.fillStyle = "#333333";
    context.fillRect(checkButton.x, checkButton.y, checkButton.width, checkButton.height);
    context.fillStyle = "#bbbbbb";
    context.fillText("Check", checkButton.x + checkButton.width / 2, checkButton.y + checkButton.height / 2);
    context.closePath();
}


function handleClick(event) {
    var coord;
    if (event.offsetX !== undefined && event.offsetY !== undefined) { 
        coord = { x: event.offsetX, y: event.offsetY }; 
    } else {
        coord = { x: event.layerX, y: event.layerY };
    }
    if (coord.x <= side) { 
        var grid_x = Math.floor(coord.x / (side / grid_size));
        var grid_y = Math.floor(coord.y / (side / grid_size));
        clicked = squares[grid_y * grid_size + grid_x];
        if (clicked === selected[selected.length - 1]) {
            emptySquare(clicked);
            selected.pop();
        } else {
            // häpeä sen niskaan, joka alla olevan rivin kirjotti
            if (!selected.some(function(square) { return square == clicked;}) && checkValid(clicked) && selected.length < 24) {
                    selected.push(clicked);
                    hilightSquare(clicked);
                }
        }
        var sana = selected.map(function(square) { return square.letter }).join("");
        document.getElementById("word").innerHTML = sana;
    } else {
        if (coord.x >= checkButton.x && coord.x <= checkButton.x + checkButton.width &&
            coord.y >= checkButton.y && coord.y <= checkButton.y + checkButton.height) {
            checkWord();
        }
    }
}

function checkWord() {
    var sana = selected.map(function(square) { return square.letter }).join("");
    if (words.indexOf(sana) >= 0 && found.indexOf(sana) < 0) {
        for (var i = 1; i <= sana.length; i++) {
            pisteet += i;
        }
        selected.forEach(emptySquare);
        selected = [];
        found.push(sana);
        if (found.length == 1 ) {
            document.getElementById("used").innerHTML += sana;
        } else {
            document.getElementById("used").innerHTML += ", " + sana;
        }
        document.getElementById("score").innerHTML = "SCORE:" + pisteet;
    }
}

function init() {
    canvas = document.getElementById("alusta");
    context = canvas.getContext("2d");
    context.textAlign = "center";
    context.textBaseline = "middle";
    checkButton = {} 
    checkButton["x"] = 7 * (side / grid_size) + 5;
    checkButton["width"] = canvas.width - checkButton.x - 10;
    checkButton["height"] = checkButton.width;
    checkButton["y"] = canvas.height / 2 - checkButton.height / 2;
    for (var i = 0; i < (grid_size * grid_size); i++) {
        squares[i] = {
            letter: getLetter(i),
            x: (i % grid_size) * (side / grid_size) + 5,
            y: Math.floor(i / grid_size) * (side / grid_size) + 5,
            width: side / grid_size - 10,
            height: side / grid_size - 10 };
        emptySquare(squares[i]);
    }
    updateScore();
}
