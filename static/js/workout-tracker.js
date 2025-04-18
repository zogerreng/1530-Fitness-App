window.addEventListener("load", setup);

function setup() {
    retrieve_DOM_references();
    set_event_listeners();
}

function retrieve_DOM_references() {
    exercise_reference = document.getElementById("exercise");
    repetitions_reference = document.getElementById("repetitions");
    weight_reference = document.getElementById("weight");
    intensity_reference = document.getElementById("intensity");
}