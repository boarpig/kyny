function begins_with(array, word) {
    var newarray = [];
    for (var item = 0, len = array.length; item < len; item++) {
        if (array[item].length >= word.length && array[item].substring(0, word.length) == word) {
            newarray.push(array[item]);
        }
    }
    return newarray;
}

function contains(array, item) {
    var found = false;
    for (var i = 0, len = array.length; i < len; i++) {
        if (array[i][0] == item[0] && array[i][1] == item[1]) {
            found = true;
            break;
        }
    }
    return found;
}

function coordinates(element, index, array) {
    var coords = [null, [-1, -1], [0, -1], [1, -1], [-1, 0], null, [1, 0], 
                 [-1, 1], [0, 1], [1, 1]];
    return coords[element];
}

var foundwords = new Array();

function traverse(lwords, wrd, x, y, prev){
    var previous = prev.slice(0, prev.length);
    var word = wrd.substring(0, wrd.length);
    previous.push([x, y]);
    var left = [1, 4, 7];
    var right = [3, 6, 9];
    var up = [1, 2, 3];
    var bottom = [7, 8, 9];
    word += squares[7 * y + x].letter;
    var temp = begins_with(lwords, word);
    if (temp.indexOf(word) != -1) {
        foundwords.push(word);
    }
    var temp_adjacent = [1, 2, 3, 4, 6, 7, 8, 9];
    if (x == 0) {
        temp_adjacent = _.difference(temp_adjacent, left)
    }
    if (x == 6) {
        temp_adjacent = _.difference(temp_adjacent, right)
    }
    if (y == 0) {
        temp_adjacent = _.difference(temp_adjacent, up)
    }
    if (y == 6) {
        temp_adjacent = _.difference(temp_adjacent, bottom)
    }
    var adjacent = temp_adjacent.map(coordinates);
    if (temp.length > 0) {
        for (var g = 0, len = adjacent.length; g < len; g++) {
            var newx = x + adjacent[g][0];
            var newy = y + adjacent[g][1];
            if (!contains(previous, [newx, newy])) {
                traverse(temp, word, newx, newy, previous);
            }
        }
    }
}

function find_all_words() {
    var dive =  document.getElementById("allwords");
    var start = Date.now();
    for (var x = 0; x < 7; x++) {
        for (var y = 0; y < 7; y++) {
            letter = squares[7 * y + x].letter;
            main = begins_with(words, letter);
            traverse(words, "", x, y, []);
        }
    }
    var since = Date.now() - start;
    if (foundwords.length > 0) {
        foundwords = _.uniq(foundwords);
        dive.innerHTML = "Found " + foundwords.length + " words: ";
        for (var word = 0, len = foundwords.length; word < len; word++) {
            if (found.indexOf(foundwords[word]) != -1) {
                foundwords[word] = "<b>" + foundwords[word] + "</b>";
            }
            if (word == 0) {
                dive.innerHTML += foundwords[word];
            } else {
                dive.innerHTML += ", " + foundwords[word];
            }
        }
        dive.innerHTML += "<br><br>Time used for finding all words:" + since + " ms.";
    } else {
        dive.innerHTML = "No words found";
    }
}
