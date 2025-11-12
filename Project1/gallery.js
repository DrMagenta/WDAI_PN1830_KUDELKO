const nextButtons = document.getElementsByClassName("slide-right");
const prevButtons = document.getElementsByClassName("slide-left");
const sliders = document.getElementsByClassName("slider");
const gallery_sizes = [5, 3, 15, 5, 4, 4];
const slider_objs = [];

class Slider
{
    self;
    size;

    constructor(self, size)
    {
        this.self = self;
        this.size = size;
        this.currentSlide = 0;
        this.slideRight = this.slideRight.bind(this);
        this.slideLeft = this.slideLeft.bind(this)
    }
    
    slideRight()
    {
        if (this.currentSlide < this.size - 1)
        {
            let currentX = parseInt(this.self.style.left);
            let gapInPx = 0.5 * document.documentElement.clientWidth;
    
            this.self.style.left = `${currentX - 2*gapInPx}px`;
            this.currentSlide++;
        }
    }
    
    slideLeft()
    {
        if (this.currentSlide > 0)
        {
            let currentX = parseInt(this.self.style.left);
            let gapInPx = 0.5 * document.documentElement.clientWidth;
    
            this.self.style.left = `${currentX + 2*gapInPx}px`;
            this.currentSlide--;
        }
    }
}


for (let i = 0; i < nextButtons.length; i++)
{
    var new_slider = new Slider(sliders[i], gallery_sizes[i])
    new_slider.self.style.left = '0px';

    slider_objs.push();

    nextButtons[i].addEventListener('click', new_slider.slideRight);
    prevButtons[i].addEventListener('click', new_slider.slideLeft);
}