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
    '#10ff00', //green
    '#0080ff', //blue
    '#ff0000', //red
    '#ffb732', //orange
    '#f8ff00', //yellow
    '#00ffd9',  //light green/blue
    '#FF00FF', //fuschia
    '#A9A9A9', //grey    
    '#a41a1a', //brown    
];

const LABELS = ["date", "perpetrator", "killed", "injured", "country", "region"];
const MAX_LABELS = COLORS.length;
const LABEL_ATTRIBUTE = 'label';
const CONTENT_ID = 'content';
var results = {'article_url': window.page_data.article_url};
loadedLabels = JSON.parse(window.page_data.loadedLabels);
selectType(JSON.parse(window.page_data.articleType));

//assign color to each label
var labelToColor = {};
window.labelToColor = labelToColor;
//labelToColor = window.labelToColor
LABELS.forEach((label, i) => {
    labelToColor[label] = COLORS[i];
});

loadLabels(loadedLabels)

function highlightRange(start_index, end_index, label){
    color = labelToColor[label];
    var content = document.getElementById("content");
    var str = content.innerHTML;

    highlightContent = str.slice(start_index, end_index + 1);
    str = str.slice(0, start_index) + `<span style="background-color: ${color}; display: inline;" id= ${label}>` + highlightContent + '</span>' + str.slice(end_index + 1);
    content.innerHTML = str;
    return highlightContent;
}

function loadLabels(labels) {
    var foundLabels = Object.getOwnPropertyNames(loadedLabels)
    foundLabels.sort(function(a,b) {return (loadedLabels[a]['start_index'] > loadedLabels[b]['start_index']) ? -1 : ((loadedLabels[b]['start_index'] > loadedLabels[a]['start_index']) ? 1 : 0);} );
    for (var i = 0; i < foundLabels.length; i++) {
        var label = foundLabels[i];
        var loadedLabel = loadedLabels[label];
        
        if(loadedLabel === null || loadedLabel == undefined)
            continue;

        start_index = loadedLabel['start_index']
        end_index = loadedLabel['end_index']
        if(start_index == null || end_index == null) continue;

        content = highlightRange(loadedLabel['start_index'], loadedLabel['end_index'], label);
        var tagInfo = {
            'content':content,
            'start_ixndex':start_index, 
            'end_index':end_index
        };

        results[label] = tagInfo;
    }
}
function getSelectedString() {
    windowSelection = window.getSelection();
    if (windowSelection) {
        return windowSelection.toString();
    }

    return "";
}


function removeHighlight(label){
    style = document.getElementById(label);
    if(style !== null){
        delete results[label]
        $(style).replaceWith(function() { return this.innerHTML; });
    }

}

function highlightSelection(event) {
    var label = event.target.getAttribute(LABEL_ATTRIBUTE);
    var range = window.getSelection().getRangeAt(0);
    var highlight = document.createElement("span");
    var color = labelToColor[label];

    removeHighlight(label);

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

function clearHighlights(){
    for (var i = 0; i < LABELS.length; i++) {
        var label = LABELS[i];
        removeHighlight(label)
    }
}

function getSelectedButtonValue(){
    checkedButton = document.querySelector('input[name="btn"]:checked');
    if(checkedButton === null){
        return "";
    }

    return checkedButton.value;
}

function selectType(type){
    var checkbox = document.getElementById(type);
    if(checkbox === null){
        checkbox = document.getElementById('NOT_STRIKE');
    }
    checkbox.checked = true;
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
        console.log(textPrecedingSelection);
        var startIndex = textPrecedingSelection.length;
        var endIndex = startIndex + selectedString.length - 1;
    }

    var tagInfo = {
        'content':selectedString,
        'start_index':startIndex, 
        'end_index':endIndex
    };

    results[label] = tagInfo;
}

var navbar = document.getElementById("navbar");

for (var i = 0; i < LABELS.length; i++) {
    var label = LABELS[i];
    var color = labelToColor[label];

    var button = document.createElement("button");
    button.setAttribute("style", `background-color: ${color}; color: black; font-weight: bold;`);
    button.setAttribute("class", "btn");
    button.setAttribute(LABEL_ATTRIBUTE, label);
    button.innerHTML = label;
    navbar.appendChild(button);
    var divider = document.createElement("div");
    divider.setAttribute("style", "width:15px;height:auto;display:inline-block; margin-top:20px; margin-bottom:20px;");
    navbar.appendChild(divider);

    button.addEventListener("click", labelSelection);
}

var button = document.createElement("button");

button.innerHTML = "Save";
button.setAttribute("style", "margin-top: 20px; margin-bottom: 20px;");
navbar.appendChild(document.createElement("br"));
navbar.appendChild(button);
navbar.appendChild(document.createElement("br"));
button.addEventListener("click", function(event) {
    buttonValue = getSelectedButtonValue();
    if(buttonValue === ""){
        buttonValue = "NOT_DRONE";
    }
    results["article_type"] = buttonValue;
    $.ajax({
      url: window.page_data.url,
      type: 'POST',
      data: JSON.stringify(results),
    });
});

button = document.createElement("button");
button.innerHTML = "Clear highlight";
//button.setAttribute("style", "margin-top: 20px; margin-bottom: 20px;");
//navbar.appendChild(document.createElement("br"));
button.addEventListener("click", clearHighlights);
navbar.appendChild(button);