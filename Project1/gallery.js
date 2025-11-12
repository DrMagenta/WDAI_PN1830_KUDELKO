const nextButtons = document.getElementsByClassName("slide-right");
const prevButtons = document.getElementsByClassName("slide-left");
const sliders = document.getElementsByClassName("slider");
const gallery_sizes = [5];
const slider_objs = [];

class Slider
{
    self;
    size;

    constructor(self, size)
    {
        this.self = self;
        this.size = size;

        // console.log(this.self.style.left);
    }

}

function slideRight(slider)
{
    console.log(slider)
    let currentX = parseInt(slider.self.style.left);
    let gapInPx = 0.5 * document.documentElement.clientWidth;

    slider.self.style.left = `${currentX - 2*gapInPx}px`;
}

for (let i = 0; i < nextButtons.length; i++)
{
    var new_slider = new Slider(sliders[i], gallery_sizes[i])
    new_slider.self.style.left = '0px';

    /*
    console.log(new_slider.self); // logs div.slider
    console.log(new_slider.self.style); // logs CSSStyleDeclaration
    console.log(new_slider.self.style.left); // logs 0px
    */
    slider_objs.push();

    // console.log(new_slider.self.style.left);

    nextButtons[i].addEventListener('click', function() {
        slideRight(new_slider);
    });
}