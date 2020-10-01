
const getPageY = () => {
    /// This returns distance scrolled from the top of the page

    let page_y = window.pageYOffset;

    return page_y;

}

const displayPageY = (element_id) => {

    let page_y = getPageY();

    let element = document.getElementById(element_id);

    element.innerHTML = "Page Y = " + "<strong>" + page_y + "<strong>";

}

// ### Y Page Offset Counter
(() => {
    setInterval(() => displayPageY('page_offset_display'), 10);
})();

const getElementY = (element_id, display_to) => {
    
    const element = document.getElementById(element_id);
    let element_rect = element.getBoundingClientRect();
    element_y = parseInt(element_rect.top + window.scrollY);

    display_element = document.getElementById(display_to);
    display_element.innerHTML = "Element Y: " + element_y;

    return element_y;
}

// ### Scroll tests - y offset displays
(() => {
    setInterval(() => getElementY('smooth-vertical', 'smooth-vertical-current-y'), 1);
    setInterval(() => getElementY('instant-vertical', 'instant-vertical-current-y'), 1);
})();


const showElementAtHeight = (element_id, height) => {
    /// Hide given element until the given height is reached (by scrolling to it)
    element = document.getElementById(element_id);
    element.style.visibility = "hidden";

    // Check for correct height every ten seconds
    let timer = setInterval(() => {
        let height_passed = getPageY() >= height;

        if (height_passed){
            element.style.visibility = "visible";
            element.innerHTML = "visible"
            clearInterval(timer);
        }

    }, 10);
}

// Set to show element after certain height is passed
(() => {
    setTimeout(() => showElementAtHeight('hidden-element', 2000), 1);
})();
