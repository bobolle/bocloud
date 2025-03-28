var source = new EventSource('/stream');
var tableAll = document.getElementById('table-all');

source.addEventListener('message', function(msg) {
    var json_data = JSON.parse(msg.data);
    for (let i = 0; i < json_data.length; i++) {
        var newTableTR = document.createElement('tr');
        var keys = Object.keys(json_data[i]);

        for (let j = 0; j < keys.length; j++) {
            var newTableTD = document.createElement('td');
            var TDTextNode = document.createTextNode(json_data[i][keys[j]]);

            newTableTD.appendChild(TDTextNode);
            newTableTR.appendChild(newTableTD);
        }

        tableAll.appendChild(newTableTR);
        if (latest) {
            newTableTR.scrollIntoView();
        }
    }
});

source.addEventListener('error', function(msg) {
    source.close();
});

// control
let latest = true;
var buttonLatest = document.getElementById('button-latest');
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

// drag table
var tableElements = document.querySelectorAll('.table-dragable');
tableElements.forEach(function(element) {
    element.style.left = localStorage.getItem(element.getAttribute('id') + 'posX');
    element.style.top = localStorage.getItem(element.getAttribute('id') + 'posY');
    element.style.height = localStorage.getItem(element.getAttribute('id') + 'Height');
});

tableElements.forEach(function(element) {
    element.addEventListener('mousedown', function(event) {
    if (event.buttons == 1) {
        event.preventDefault();
        let initX = event.clientX;
        let initY = event.clientY;

        function moveElement(event) {
            if (event.shiftKey) {
            var height = event.clientY - element.offsetTop;
            var step = ((height - 2) % 24);

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
});
