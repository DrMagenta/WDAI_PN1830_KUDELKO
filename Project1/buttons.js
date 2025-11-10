var subpages = [
    'index',
    'pros',
    'attractions',
];

var buttons = document.getElementsByClassName('button');

for (let i = 0; i < subpages.length; i++)
{
    let button = buttons[i];
    let href = subpages[i] + '.html';

    button.addEventListener("click", function() {
        window.location.href = href;
    });
}