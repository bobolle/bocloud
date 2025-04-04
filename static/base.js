const source = new EventSource('/stream');
const tableReads = document.getElementById('table-reads');

// fetch data from model
async function fetchData(model, id, amount) {
    const response = await fetch(`/fetch/${model}?${id}`);
    return await response.json();
}

// create new panel for specific device
async function createPanel(model, id, title) {
    function createButton() {
        const newButton = document.createElement('button');
        newButton.innerHTML = 'x';
        newButton.addEventListener('mousedown', function(event) {
            if (event.buttons === 1) {
                newTable.remove();
            }
        });

        return newButton;
    }

    function createTitle() {
        const titleTR = document.createElement('tr');
        const titleTH = document.createElement('th');
        titleTH.innerHTML = title;

        titleTR.className = 'tr-title';
        titleTH.colSpan = data.length;
        titleTR.appendChild(titleTH);

        newButton = createButton();
        titleTH.appendChild(newButton);

        return titleTR;
    }

    function createDescription() {
        const descTR = document.createElement('tr');
        for (const read in data[0]) {
            descTR.className = 'tr-desc';

            const newTableTH = document.createElement('th');
            const THTextNode = document.createTextNode(read);

            newTableTH.appendChild(THTextNode);
            descTR.appendChild(newTableTH);
        }

        return descTR;
    }

    data = await fetchData(model, id);

    const newTable = document.createElement('table');
    newTable.setAttribute('id', 'table-'+model+'-'+id);
    initDragResize(newTable);

    titleTR = createTitle();
    newTable.appendChild(titleTR);

    descTR = createDescription();
    newTable.appendChild(descTR);

    // insert data
    for (const read in data) {
        const newTableTR = document.createElement('tr');
        for (const key in data[read]) {

            const newTableTD = document.createElement('td');
            const TDTextNode = document.createTextNode(data[read][key]);

            newTableTD.appendChild(TDTextNode);
            newTableTR.appendChild(newTableTD);
        }

        newTable.appendChild(newTableTR);
      document.body.appendChild(newTable);
    }

    
}

// create table rows
source.addEventListener('message', function(msg) {
    const json_data = JSON.parse(msg.data);

    const newTableTR = document.createElement('tr');
    for (const key in json_data) {

        const newTableTD = document.createElement('td');
        const TDTextNode = document.createTextNode(json_data[key]);

        newTableTD.appendChild(TDTextNode);
        newTableTR.appendChild(newTableTD);

        if (key == 'device_id') {
            newTableTD.addEventListener('mousedown', function(event) {
                if (event.buttons === 1) {
                    createPanel('device', json_data[key], json_data['device'] + ' ' + json_data['device_id']);
                }
            });
        }

        if (key == 'sensor_id') {
            newTableTD.addEventListener('mousedown', function(event) {
                if (event.buttons === 1) {
                    createPanel('sensor', json_data[key], json_data['sensor_type'] + ' ' + json_data['sensor_id']);
                }
            });
        }
    }

    tableReads.appendChild(newTableTR);

    if (latest) {
        newTableTR.scrollIntoView();
    }
});

source.addEventListener('error', function(msg) {
    source.close();
});

// control
let latest = true;
const buttonLatest = document.getElementById('button-latest');
buttonLatest.addEventListener('mousedown', function(event) {
    if (event.buttons == 1) {
        latest = !latest;
    }

    if (latest) {
        buttonLatest.style.color = '#EEEEEE';
    } else {
        buttonLatest.style.color = '#888888';
        buttonLatest.style.color = '#888888';
    }
});

// drag and resize function
function initDragResize(element) {
    element.style.left = localStorage.getItem(element.getAttribute('id') + 'posX');
    element.style.top = localStorage.getItem(element.getAttribute('id') + 'posY');
    element.style.height = localStorage.getItem(element.getAttribute('id') + 'Height');

    element.addEventListener('mousedown', function(event) {
    if (event.buttons == 1) {
        event.preventDefault();
        let initX = event.clientX;
        let initY = event.clientY;

        function moveElement(event) {
            if (event.shiftKey) {
            const height = event.clientY - element.offsetTop;
            const step = ((height - 2) % 24);

            if ((step < 12) && (height >= 24)) {
                element.style.height = (height - step) + 'px';
            }

            } else {
                let currentX = event.clientX;
                let currentY = event.clientY;
                let deltaX = currentX - initX;
                let deltaY = currentY - initY;

                element.style.left = element.offsetLeft + deltaX + 'px';
                element.style.top = element.offsetTop + deltaY + 'px';

                initX = currentX;
                initY = currentY;
            }
        }

        function stopElement(event) {
            localStorage.setItem((element.getAttribute('id') + 'posX'), element.style.left);
            localStorage.setItem((element.getAttribute('id') + 'posY'), element.style.top);
            localStorage.setItem((element.getAttribute('id') + 'Height'), element.style.height);

            document.removeEventListener('mousemove', moveElement);
            document.removeEventListener('mouseup', stopElement);
        }

        document.addEventListener('mousemove', moveElement);
        document.addEventListener('mouseup', stopElement);
        }
    });
}

const tableElements = document.querySelectorAll('.table-dragable');
tableElements.forEach(function(element) {
    initDragResize(element);
});
