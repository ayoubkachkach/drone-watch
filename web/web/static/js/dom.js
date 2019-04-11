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
    '#f8ff00', //yellow
    '#00ffd9',  //light green/blue
    '#ff0000', //red
    '#A9A9A9', //grey
    '#FF00FF', //fuschia
    '#ffb732', //orange
    '#a41a1a'];
const CASUALTY_TYPE = {INJURY: "INJURY", DEATH: "DEATH"};
const LABELS = ["date", "perpetrator", "country", "region"];
const LABEL_ATTRIBUTE = 'label';
const CONTENT_ID = 'content';
const DEATH_REGEX = /death(\d+)/;
const INJURY_REGEX = /injury(\d+)/;
const VICTIM_REGEX = /victim(\d+)/;

//set IDs for death and injuries
var death_idx = 0, injury_idx = 100, colors_idx = 0;
var labelToColor = {};

//get data from html
var article_url = window.page_data.article_url;
var entities = JSON.parse(window.page_data.loadedEntities);

//create labels from loaded entities
var entityLabels = createLabelsFromEntities(entities);
highlightLabels(entityLabels);

//select type checkbox
selectType(JSON.parse(window.page_data.articleType));

//*************** helper functions ***************************
function getOrNull(object, key){
    return object.hasOwnProperty(key) ? object[key] : null;
}

function mergeDict(a, b){
    var c = {};
    for (var i in a) {
      c[i] = a[i];
    }
    for (var j in b) {
      c[j] = b[j];
    }
    return c;
}

function extractIdx(label){
    var idxStr, idx;
    if(DEATH_REGEX.test(label)){
        idxStr = label.match(DEATH_REGEX)[1];
        return parseInt(idxStr);
    }else if(INJURY_REGEX.test(label)){
        idxStr = label.match(INJURY_REGEX)[1];
        return parseInt(idxStr);
    }

    return null;
}

function shallowCopy(obj){
    return JSON.parse(JSON.stringify(obj));
}

function isValidLabel(label){
    return (label != null && label['start_index'] != null && label['end_index'] != null);
}
//*************** helper functions ***************************

//turn casualty entities into labels for highlighting where key is <casualty_type><idx>
function createCasualtyLabels(casualtyEntities){
    casualties = {};
    for(var i = 0; i < casualtyEntities.length; i++){
        casualty = casualtyEntities[i];
        var color = getColor();
        if(casualty['type'] == CASUALTY_TYPE.INJURY){
            idx = injury_idx;
            injury_idx += 1;
            casualtyStr = 'injury'
        }else{
            idx = death_idx;
            death_idx += 1;
            casualtyStr = 'death';
        }

        casualtyLabel = `${casualtyStr}${idx}`;
        victimLabel =  `victim${idx}`;
        // Assign same color to casualty and victim label
        labelToColor[casualtyLabel] = labelToColor[victimLabel] = color;

        casualties[casualtyLabel] = {start_index: casualty['start_index'], end_index: casualty['end_index'], casualty_type: casualty['type'], color:color, content: casualty['content']};
        victim = getOrNull(casualty, 'victim');
        if(victim != null){
            victim = {start_index:victim['start_index'], end_index:victim['end_index'], color:color, casualty_type: casualty['type'], content: victim['content']};
        }

        casualties[victimLabel] = victim;
    }

    return casualties;
}

function getColor(){
    return COLORS[(colors_idx++) % COLORS.length];
}

//turn entities into labels
function createLabelsFromEntities(entities){
    var entityLabels = {}
    var death_idx = 0, injury_idx = 100;
    for(const key of Object.keys(entities)){
        var entityLabel = {};
        var entity = entities[key];
        if(entity === null || entity == undefined){
            entity = {start_index: null, end_index: null};
        }

        if(key == 'deaths'){
            entityLabel = createCasualtyLabels(entity);
            death_idx += entity.length;
        }else if(key == 'injuries'){
            entityLabel = createCasualtyLabels(entity);
            injury_idx += entity.length;
        }else{
            var start_index = entity['start_index'], end_index = entity['end_index'];
            var color = getColor();

            entityLabel = {[key]:{start_index: entity['start_index'], end_index: entity['end_index'], content:entity['content'], color: color}}
            labelToColor[key] = color;
        }

        entityLabels = mergeDict(entityLabels, entityLabel);
    }

    return entityLabels;
}

function createEntitiesFromLabels(labels){
    entities = {'date':null,'country':null,'region':null, 'perpetrator':null, 'deaths':[], 'injuries':[]}
    deathLabels = Object.keys(labels).filter(function (label) { return DEATH_REGEX.test(label); });
    injuryLabels = Object.keys(labels).filter(function (label) { return INJURY_REGEX.test(label); });
    otherLabels = Object.keys(labels).filter(function (label) { return !(INJURY_REGEX.test(label) || DEATH_REGEX.test(label) || VICTIM_REGEX.test(label)); })

    for(var label of deathLabels){
        var idx = extractIdx(label);
        var deathEntity = shallowCopy(labels[label]);
        deathEntity['victim'] = shallowCopy(getOrNull(labels, `victim${idx}`));
        entities.deaths.push(deathEntity);
    }

    for(var label of injuryLabels){
        var idx = extractIdx(label);
        var injuryEntity = shallowCopy(labels[label]);
        injuryEntity['victim'] = shallowCopy(getOrNull(labels, `victim${idx}`));
        entities.injuries.push(injuryEntity);
    }

    for(var label of otherLabels){
        if(!isValidLabel(labels[label]))
            continue;

        entities[label] = shallowCopy(labels[label]);
    }

    return entities;
}

//given start and end indexes, highlight appropriate label
function highlightRange(start_index, end_index, label, color){
    var content = document.getElementById("content");
    var str = content.innerHTML;
    if(start_index == null || end_index == null) return;

    highlightContent = str.slice(start_index, end_index + 1);
    str = str.slice(0, start_index) + `<span style="background-color: ${color}; display: inline;" id= ${label}>` + highlightContent + '</span>' + str.slice(end_index + 1);
    content.innerHTML = str;
    return highlightContent;
}


function highlightLabels(entityLabels) {
    labels = Object.getOwnPropertyNames(entityLabels);
    labels.sort(function(a,b) {
        return entityLabels[a]['start_index'] > entityLabels[b]['start_index'] ? -1 : (entityLabels[b]['start_index'] > entityLabels[a]['start_index'] ? 1 : 0);
    });

    for(const label of labels){
        entityLabel = entityLabels[label];
        highlightRange(entityLabel['start_index'], entityLabel['end_index'], label, entityLabel['color']);    
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
        delete entityLabels[label];
        $(style).replaceWith(function() { return this.innerHTML; });
    }
}

// Highlights current selection in html
function highlightSelection(event, color) {
    var label = event.target.getAttribute(LABEL_ATTRIBUTE);
    var range = window.getSelection().getRangeAt(0);
    var highlight = document.createElement("span");

    removeHighlight(label);

    highlight.setAttribute(
        "style",
        `background-color: ${color}; display: inline;`
    );
    highlight.setAttribute(
        "id",
        label
    );
    range.surroundContents(highlight);
}

function clearHighlights(){
    for(const label of Object.keys(entityLabels)){
        removeHighlight(label);
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

function createButton(label, color, div){
    var button = document.createElement("button");
    var divider = document.createElement("div");

    button.setAttribute("style", `background-color: ${color}; color: black; font-weight: bold;`);
    button.setAttribute("class", "btn");
    button.setAttribute(LABEL_ATTRIBUTE, label);
    button.innerHTML = label;
    button.addEventListener("click", function(){
        labelSelection(event, color);
    });

    divider.setAttribute("style", "width:15px;height:auto;display:inline-block; margin-top:20px; margin-bottom:20px;");
    div.appendChild(button);
    div.appendChild(divider);
    labelToColor[label] = color;
}

function createKilledButtons(color, div){
    casualtyLabel = `death${death_idx}`;
    victimLabel = `victim${death_idx}`; 
    createButton(casualtyLabel, color, div);
    createButton(victimLabel, color, div);
    death_idx += 1;

    return [casualtyLabel, victimLabel];
}

function createInjuryButtons(color, div){
    casualtyLabel = `injury${injury_idx}`;
    victimLabel = `victim${injury_idx}`; 
    createButton(casualtyLabel, color, div);
    createButton(victimLabel, color, div);
    injury_idx += 1;

    return [casualtyLabel, victimLabel];
}

function labelSelection(event, color) {
    var label = event.target.getAttribute(LABEL_ATTRIBUTE);
    var casualtyLabel = null, victimLabel = null;

    if(DEATH_REGEX.test(label) && extractIdx(label) == death_idx - 1){
        [casualtyLabel, victimLabel] = createKilledButtons(getColor(), div);
    }else if(INJURY_REGEX.test(label)&& extractIdx(label) == injury_idx - 1){
        [casualtyLabel, victimLabel] = createInjuryButtons(getColor(), div);
    }

    if(casualtyLabel != null && victimLabel != null){
        labelToColor[casualtyLabel] = color;
        labelToColor[victimLabel] = color;
    }

    //TODO: add handling of case where victim button is pressed
    selectedString = getSelectedString();
    if (selectedString === "") {
        removeHighlight(label);
        entityLabels[label] = null;
        return;
    }

    highlightSelection(event, color);

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

    entityLabels[label] = {start_index: startIndex, end_index: endIndex, content: selectedString, color: labelToColor[label]}
}

var navbar = document.getElementById("navbar");
var div = document.getElementById("casualty");

// Create buttons from entityLabels
for(const label of Object.keys(entityLabels)){
    var color = entityLabels[label]['color'];
    // Create button for current label
    if(DEATH_REGEX.test(label) || INJURY_REGEX.test(label) || VICTIM_REGEX.test(label)){
        createButton(label, color, div);
        continue;
    }
    
    createButton(label, color, navbar);
}

createKilledButtons(getColor(), div);
createInjuryButtons(getColor(), div);

// Create save button
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
    entities = createEntitiesFromLabels(entityLabels);
    entities["article_type"] = buttonValue;
    $.ajax({
      url: window.page_data.url,
      type: 'POST',
      data: JSON.stringify(entities),
    });
});

button = document.createElement("button");
button.innerHTML = "Clear highlight";
//button.setAttribute("style", "margin-top: 20px; margin-bottom: 20px;");
//navbar.appendChild(document.createElement("br"));
button.addEventListener("click", clearHighlights);
navbar.appendChild(button);