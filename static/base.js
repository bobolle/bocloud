const source = new EventSource('/stream');
const tableReads = document.getElementById('table-reads');

// create new panel for specific device
async function createPanel(deviceName) {
    try {
        const response = await fetch(`/fetch?${deviceName}`);
        if (!response.ok) {
            throw new Error('Bad reponse');
        }

        const json_data = await response.json();
        reads = json_data.reads;

        const newTable = document.createElement('table');
        newTable.setAttribute('id', 'table-device-'+deviceName);
        initDragResize(newTable);

        const titleTR = document.createElement('tr');
        const titleTH = document.createElement('th');
        titleTH.innerHTML = deviceName;

        titleTR.className = 'tr-title';
        titleTH.colSpan = reads.length;
        titleTR.appendChild(titleTH);
        newTable.appendChild(titleTR);

        const descTR = document.createElement('tr');
        descTR.className = 'tr-desc';

        for (const read in reads[0]) {
            const newTableTH = document.createElement('th');
            const THTextNode = document.createTextNode(read);

            newTableTH.appendChild(THTextNode);
            descTR.appendChild(newTableTH);
        }

        newTable.appendChild(descTR);

        for (const read in reads) {
            const newTableTR = document.createElement('tr');
            for (const key in reads[read]) {

                const newTableTD = document.createElement('td');
                const TDTextNode = document.createTextNode(reads[read][key]);

                newTableTD.appendChild(TDTextNode);
                newTableTR.appendChild(newTableTD);
            }

            newTable.appendChild(newTableTR);
            document.body.appendChild(newTable);
        }
    } catch (error) {
        console.error('Error: ', error);
    }
}

// create table rows
let openPanels = new Set();
source.addEventListener('message', function(msg) {
    const json_data = JSON.parse(msg.data);

    const newTableTR = document.createElement('tr');
    for (const key in json_data) {

        const newTableTD = document.createElement('td');
        const TDTextNode = document.createTextNode(json_data[key]);

        newTableTD.appendChild(TDTextNode);
        newTableTR.appendChild(newTableTD);

        if (key == 'device') {
            exist = document.getElementById('table-device-' + key);
            newTableTD.addEventListener('mousedown', function(event) {
                if (event.buttons === 1 && !openPanels.has(json_data[key])) {
                    const panel = createPanel(json_data[key]);
                    openPanels.add(json_data[key]);
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

// drag table
const tableElements = document.querySelectorAll('.table-dragable');
tableElements.forEach(function(element) {
    initDragResize(element);
});
