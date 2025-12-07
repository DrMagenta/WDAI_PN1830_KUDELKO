var buttons = document.querySelectorAll("input");

var secBlockObj = document.getElementById("sec-block");
var minBlockObj = document.getElementById("min-block");
var secondsObj = document.getElementById("secs");
var minutesObj = document.getElementById("mins");

var minutes = 0;
var seconds = 0;

var active = false;

for (let i = 0; i < buttons.length; i++)
{
    switch (buttons[i].getAttribute("name"))
    {
        case "start":
            buttons[i].addEventListener("click", function() {
                active = true;
            });
            break;

        case "stop":
            buttons[i].addEventListener("click", function() {
                active = false;
            });
            break; 
        case "reset":
            buttons[i].addEventListener("click", function() {
                resetWatch();
                updateWatch();
            })
            break;
    }
}

function resetWatch()
{
    minBlockObj.style.display = "none"
    seconds = minutes = 0;
}

function updateWatch()
{
    if (active)
    { 

        seconds++;
        if (seconds >= 60)
        {
            seconds = 0;
            minutes++;
        }
        if (minutes > 0)
        {
            minBlockObj.style.display = "inline"
        }
    }
    secondsObj.innerHTML = seconds;
    minutesObj.innerHTML = minutes;
}

setInterval(updateWatch, 1000);