// Simple scroll transition for background color
window.addEventListener('scroll', function() {
    var scrollY = window.scrollY;
    var docHeight = document.body.scrollHeight - window.innerHeight;
    var progress = Math.min(scrollY / docHeight, 1);
    // Interpolate color from light to much darker
    var r = Math.round(192 - (192 - 60) * progress);
    var g = Math.round(90 - (90 - 20) * progress);
    var b = Math.round(90 - (90 - 20) * progress);
    document.body.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
});