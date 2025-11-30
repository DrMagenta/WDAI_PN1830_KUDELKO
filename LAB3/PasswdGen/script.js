const CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%&*~;:-="
const END_UPPERCASE = 27
const BEGIN_SPECIAL = 53

function getMinSize()
{
    let minSize = parseInt(document.getElementById("min-size").value);
    return minSize;
}

function getMaxSize()
{
    let maxSize = parseInt(document.getElementById("max-size").value);
    return maxSize;
}

function checkCapitalLetters()
{
    return document.getElementById("capital-letters").checked;
}

function checkSpecialCharacters()
{
    return document.getElementById("spec-chars").checked;
}

function generatePassword(minSize, maxSize, includeCapital, includeSpecial)
{
    let rangeStart = includeCapital ? 0 : END_UPPERCASE;
    let rangeEnd = includeSpecial ? CHARACTERS.length : BEGIN_SPECIAL;
    let size = Math.floor(Math.random() * (maxSize - minSize) + minSize);

    let passwd = "";

    for (let i = 0; i < size; i++)
    {
        let index = Math.floor(Math.random() * (rangeStart - rangeEnd) + rangeEnd);
        passwd += CHARACTERS[index];

    }

    alert("Your password: " + passwd);
}

document.getElementById("gen-button").addEventListener("click", function() {
    let minSize = getMinSize();
    let maxSize = getMaxSize();
    let includeCapital = checkCapitalLetters();
    let includeSpecial = checkSpecialCharacters();

    if (isNaN(minSize) || isNaN(maxSize))
    {
        alert("Error: invalid arguments")
    } else
    {
        generatePassword(
            minSize,
            maxSize,
            includeCapital,
            includeSpecial
        );}
    }

);