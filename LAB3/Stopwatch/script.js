var buttons = document.querySelectorAll("input");

var min10sObj = document.getElementById("min10s");
var minutesObj = document.getElementById("mins");
var sec10sObj = document.getElementById("sec10s");
var secondsObj = document.getElementById("secs");

var min10s = 0;
var minutes = 0;
var sec10s = 0
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
    }
}

function resetWatch()
{
    seconds = sec10s = minutes = min10s = 0;
}

function updateWatch()
{
    if (active)
    { 
        if (min10s >= 6) return;

        seconds++;
        if (seconds >= 10)
        {
            seconds = 0;
            sec10s++;
        }
        if (sec10s >= 6)
        {
            sec10s = 0;
            minutes++;
        }
        if (minutes >= 10)
        {
            minutes = 0;
            min10s++;
        }
    }
    secondsObj.innerHTML = seconds;
    sec10sObj.innerHTML = sec10s
    minutesObj.innerHTML = minutes
    min10sObj.innerHTML = min10s;
}

setInterval(updateWatch, 1000);