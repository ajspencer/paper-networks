function sketchProc(processing) {

    /**
     * Initalizes the empty background and the buttons
     */
    var initBackground = function() {
        processing.size(window.innerWidth, window.innerHeight); 
        processing.background(205,201, 201);
        //Set and load the font
        processing.textFont(processing.loadFont('FFScala-bold.ttf'));
        //Write the combine button
        processing.fill(91, 193, 252);
        processing.rect(window.innerWidth/2 - 150, 10, 105, 30);
        //fill in the text for the combine button
        processing.textAlign(CENTER);
        processing.fill(255,255,255);
        processing.text('Combine', window.innerWidth/2 - 95, 30);
        //Write the save button
        processing.fill(91, 193, 252);
        processing.rect(window.innerWidth/2 + 50, 10, 105, 30);
        //Fill in the text for the save button
        processing.textAlign(CENTER);
        processing.fill(255,255,255);
        processing.text('Remove', window.innerWidth/2 + 105, 30);
        
    };

    //State of the entire canvas: the nodes stores in the canvas
    //Nodes are uniquely defined by the name of the author they represent, so we will keep track of the nodes by mapping from authors to nodes
    var nodes = {};
    //Array to keep track of the selected nodes
    var selected = [];
    /*
     * Constructor for a node, which represents an author in the network of authors
     * @param x | the x location of the node
     * @param y | the y location of the node
     * @param name | the name of the author that this node corresponds to
     * @param connection | a list of the node's connections
     */
    function Node(x, y, name, connections) {
        this.selected = false;
        this.x = x;
        this.y = y;
        this.name = name;
        this.connections = connections;
        //Initalize the standard width of a Node
        this.radius = 35;
    }

    /*
     * Define the logic for drawing a node
     */
    Node.prototype.draw = function() {
        processing.fill(0, 0, 0, 0.5*255);
        processing.ellipse(this.x,this.y, this.radius*2, this.radius*2);
        processing.fill(255,255,255);
        processing.textAlign(CENTER);
        processing.text(this.name, this.x, this.y);
        for(var i = 0; i < this.connections.length; i++) {
            //Get the name of the connection
            if(this.connections[i] != '') { 
                connection = this.connections[i];
                if(nodes[connection]) {
                    processing.line(this.x - this.radius, this.y, nodes[connection].x - this.radius, nodes[connection].y)
                }
            }
        }
    };

    Node.prototype.mouseOver = function() {
        return Math.sqrt((this.x-processing.mouseX)*(this.x-processing.mouseX) + (this.y-processing.mouseY)*(this.y-processing.mouseY)) <= this.radius;
    };

    /*
     * This function gets the name of all the authors currently stored in the database, and draws the nodes based on these names
     */
    function getNodes() {
        $.ajax({
              url: '/network',
              error: function() {
                 alert('ajax call failed');
              },
              dataType: 'json',
              success: function(authors) {
                    console.log(authors);
                    for (var name in authors) {
                        if (!authors.hasOwnProperty(name)) {
                            continue;
                        }
                        var node = new Node(100 + random(window.innerWidth - 200), 100 + random(window.innerHeight - 200), name, []);
                        for(var i = 0; i < authors[name].length; i++) {
                            connection = authors[name][i];
                            node.connections.push(connection);
                            console.log(connection);
                        }
                        nodes[node.name] = node;
                    }
                    //Now that we have all the connections and nodes made, draw all the nodes
                    console.log(nodes);
                    for(name in nodes) {
                        nodes[name].draw();
                    }
                    console.log(nodes);
                    console.log('done');
              },
              type: 'GET'
           });
    }

    var checkClickedNodes = function() {
            for(name in nodes) {
                currentNode = nodes[name];
                if(currentNode.mouseOver()) {
                    console.log(currentNode.selected);
                    //If the node is not selected, select it
                    if(currentNode.selected == false) {
                        processing.fill(255, 247, 188, 0.4*255);
                        processing.ellipse(currentNode.x,currentNode.y, currentNode.radius*2, currentNode.radius*2);
                        selected.push(currentNode);
                        nodes[name].selected = true;
                    }
                    //if the node is selected, unselect it
                    else {
                        processing.fill(205, 201, 201);
                        processing.ellipse(currentNode.x,currentNode.y, currentNode.radius*2, currentNode.radius*2);
                        currentNode.draw();
                        nodes[name].selected = false;
                        //remove the selected item at the correct location
                        if(selected[0].name == name) selected.splice(0, 1);
                        else selected.splice(1,1);
                    }
                    //If the list is too long, unselect the first node
                    if(selected.length > 2) {
                        nodeToDelete = selected[0];    
                        //Draw a node the same color as the background to get rid of the ellipse
                        processing.fill(205, 201, 201);
                        processing.ellipse(nodeToDelete.x,nodeToDelete.y, nodeToDelete.radius*2, nodeToDelete.radius*2);
                        nodeToDelete.draw();
                        nodes[nodeToDelete.name].selected = false;
                        selected.splice(0, 1);
                    }
                }
            }
    };

    /**
     * function that combines the two selected nodes into one nodes, used for nodes that are the same person but have slightly different names
     */
    var combineSelected = function() {
        console.log(nodes);
        if(selected.length != 2) {
            alert("Please select two nodes to combine");
            return;
        }
        var firstNode = nodes[selected[0].name];
        var secondNode = nodes[selected[1].name];
        var node = new Node(100 + random(window.innerWidth - 200), 100 + random(window.innerHeight - 200), firstNode.name + "," + secondNode.name, []);
        //add all the connections from the first and second nodes
        for(var i = 0; i < firstNode.connections.length; i++) {
            node.connections.push(firstNode.connections[i]);
        }
        for(var i = 0; i < secondNode.connections.length; i++) {
            node.connections.push(secondNode.connections[i]);
        }
        //When I have these statements the print to console.log(nodes) is undefined, but when I don't have these statements it prints as expected??
        delete (nodes[firstNode.name]);
        delete (nodes[secondNode.name]);
        nodes[node.name] = node;
        //now, redraw the background and redraw all of the nodes and such!
        initBackground();
        for(name in nodes) {
            for(var i = 0; i < nodes[name].connections.length; i++) {
                if(nodes[name].connections[i] == firstNode.name || nodes[name].connections[i] == secondNode.name) {
                    nodes[name].connections.splice(i, 1, firstNode.name + "," + secondNode.name);
                }
            }
            console.log(nodes);
            nodes[name].draw();
        }
        selected = [];
    };

    /*
     * Removes all of the selected nodes
     */
    var removeSelected = function() {
        //Store the length so we do the correct number of iterations, since we are moving as we go along
        selectedLength = selected.length;
        //For every selected node
        for(int i = 0; i < selectedLength; i++) {
            var removeMe = selected[0];
            delete (nodes[removeMe.name]);
            for(name in nodes) {
                for(var i = 0; i < nodes[name].connections.length; i++) {
                    if(nodes[name].connections[i] == removeMe.name) {
                        nodes[name].connections.splice(i, 1);
                    }
                }
            }
            //remove the entry from selected
            selected.splice(0, 1);
        }
        //Erase all of the nodes
        initBackground();
        for(name in nodes) {
            nodes[name].draw();
        }
    };

     /**
      * Function for handling the logic of clicking button and selecting nodes
      */
     processing.mouseClicked = function() {
            //Iterate through all of the nodes and see if the mouse is clicked on it
            checkClickedNodes();
            //Now, check to see if one of the buttons was pressed
            if(processing.mouseX >= window.innerWidth/2 + 50 && processing.mouseX <= window.innerWidth/2 + 165 && processing.mouseY >= 10 && processing.mouseY <= 40) {
                removeSelected();
            }
            if(processing.mouseX >= window.innerWidth/2 - 150 && processing.mouseX <= window.innerWidth/2 - 45  && processing.mouseY >= 10 && processing.mouseY <= 40) {
                combineSelected();
            }
        };

    //Run the setup function
    processing.setup = function() {
        initBackground();
        getNodes();
    };
}

var canvas = document.getElementById("myCanvas");
// attaching the sketchProc function to the canvas
var processingInstance = new Processing(canvas, sketchProc);

