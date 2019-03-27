// text.addEventListener('mouseup', function(event){
//     selectedText = getSelectedString();
//     if(selectedText.length !== 0){
//         console.log(selectedText);
//     }
// })

// const COLORS = [
//   "#00ffff",
//   "#a52a2a",
//   "#ff00ff",
//   "#008000",
//   "#add8e6",
//   "#f0e68c",
//   "#e0ffff",
//   "#90ee90",
//   "#d3d3d3",
//   "#ffb6c1",
//   "#ffffe0",
//   "#00ff00",
//   "#ff00ff",
//   "#800000",
//   "#000080",
//   "#808000",
//   "#ffa500",
//   "#ffc0cb",
//   "#800080",
//   "#ff0000",
//   "#c0c0c0",
//   "#ffff00"
// ];

const COLORS = [
    '#FF00FF', //fuschia
    '#A9A9A9', //grey
    '#ffb732', //orange
    '#0080ff', //blue
    '#ff0000', //red
    '#f8ff00', //yellow
    '#a41a1a', //brown
    '#10ff00', //green
    '#00ffd9'  //light green/blue
];

const LABELS = ["DATE", "LOCATION", "CASUALTY"];
const MAX_LABELS = COLORS.length;
const LABEL_ATTRIBUTE = 'label';
const CONTENT_ID = 'content';
var results = {};

function getSelectedString() {
    windowSelection = window.getSelection();
    if (windowSelection) {
    return windowSelection.toString();
    }

    return "";
}

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}

function highlightSelection(event) {
    var label = event.target.getAttribute(LABEL_ATTRIBUTE);
    var range = window.getSelection().getRangeAt(0);
    var highlight = document.createElement("span");
    var color = labelToColor[label];
    document.getElementById(label);
    highlight.setAttribute(
        "style",
        `background-color: ${color}; display: inline;`
    );
    highlight.setAttribute(
        "id",
        label
    )
    range.surroundContents(highlight);
}

function labelSelection(event) {
    selectedString = getSelectedString();
    if (selectedString === "") {
    return;
    }

    var label = event.target.getAttribute(LABEL_ATTRIBUTE);

    highlightSelection(event);
    if (!results[label]) {
    results[label] = [];
    }

    if (window.getSelection) {
        var selection = window.getSelection();
        var content = document.getElementById("content");
        // Get the selected range
        var selectedRange = selection.getRangeAt(0);
        
        // Create a range that spans the content from the start of the div
        // to the start of the selection
        var precedingRange = document.createRange();
        precedingRange.setStartBefore(content.firstChild);
        precedingRange.setEnd(selectedRange.startContainer, selectedRange.startOffset);

        var textPrecedingSelection = precedingRange.toString();
        var startIndex = textPrecedingSelection.length;
        var endIndex = startIndex + selectedString.length - 1;
    }

    var tagInfo = {
        'CONTENT':selectedString,
        'START_INDEX':startIndex, 
        'END_INDEX':endIndex
    };

    results[label] = tagInfo;
}

//assign color to each label
labelToColor = {};
LABELS.forEach((label, i) => {
    labelToColor[label] = COLORS[i];
});

var navbar = document.getElementById("navbar");
var button = document.createElement("button");

button.innerHTML = "Print results";
navbar.appendChild(button);
button.addEventListener("click", function(event) {
    console.log(results)
    $.ajax({
      url: window.page_data.url,
      type: 'POST',
      data: JSON.stringify(results),
    });
});

for (var i = 0; i < LABELS.length; i++) {
    var label = LABELS[i];
    var color = labelToColor[label];

    var button = document.createElement("button");
    button.setAttribute("style", `background-color: ${color};`);
    button.setAttribute(LABEL_ATTRIBUTE, label);
    button.innerHTML = label;
    navbar.appendChild(button);

    button.addEventListener("click", labelSelection);
}
