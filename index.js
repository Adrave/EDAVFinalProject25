import { select } from 'd3';
// Create an SVG container
var svg = d3.select("body").append("svg")
    .attr("width", 800)
    .attr("height", 800);

// Define the data for the chessboard
// create an empty array
var board = [];

// define the names of the columns
let columns = ["a", "b", "c", "d", "e", "f", "g", "h"];

// define the names of the rows
var rows = [8,7,6,5,4,3,2,1];

// loop through the columns and rows to create the names of the squares
for (let i = 0; i < columns.length; i++) {
  for (let j = 0; j < rows.length; j++) {
    board.push(columns[j] + rows[i]);
  }
}


// Create the stacked text boxes
var m1 = svg.append("text")
    .text("d4 d5")
    .attr("x", 500)
    .attr("y", 50)
    .style("font-size", "50px")
    .style("dy", "-5px")
		.on("mouseover", function() {
        d3.select("#d4").style("fill", "red");
        d3.select("#d5").style("fill", "red");
    })
    .on("mouseout", function() {
        d3.select("#d4").style("fill", "black");
        d3.select("#d5").style("fill", "white");
    });

// Create the stacked text boxes
var m2 = svg.append("text")
    .text("d4 Nf6")
    .attr("x", 500)
    .attr("y", 100)
    .style("font-size", "50px")
    .style("dy", "-5px")
		.on("mouseover", function() {
        d3.select("#d4").style("fill", "red");
        d3.select("#f6").style("fill", "red");
    })
    .on("mouseout", function() {
        d3.select("#d4").style("fill", "black");
        d3.select("#f6").style("fill", "black");
    });

// Create the stacked text boxes
var m3 = svg.append("text")
    .text("e4 e5")
    .attr("x", 500)
    .attr("y", 150)
    .style("font-size", "50px")
    .style("dy", "-5px")
		.on("mouseover", function() {
        d3.select("#e4").style("fill", "red");
        d3.select("#e5").style("fill", "red");
    })
    .on("mouseout", function() {
        d3.select("#e4").style("fill", "white");
        d3.select("#e5").style("fill", "black");
    });

// Create the stacked text boxes
var m4 = svg.append("text")
    .text("e4 c5")
    .attr("x", 500)
    .attr("y", 200)
    .style("font-size", "50px")
    .style("dy", "-5px")
		.on("mouseover", function() {
        d3.select("#e4").style("fill", "red");
        d3.select("#c5").style("fill", "red");
    })
    .on("mouseout", function() {
        d3.select("#e4").style("fill", "white");
        d3.select("#c5").style("fill", "black");
    });


// Add the text labels for each square
var labels = svg.selectAll("text")
    .data(board)
    .enter()
    .append("text")
    .text(function(d) {
        return d;
    })
    .attr("x", function(d, i) {
        return (i % 8) * 50 + 25;
    })
    .attr("y", function(d, i) {
        return (Math.floor(i / 8) )* 50 + 25;
    })
    .attr("font-size", "40px")
    .attr("text-anchor", "middle")
    .attr("alignment-baseline", "middle")
    .style("fill", function(d, i) {
        return (d == "d4" || d == "e4" || d == "e5" || d=="c5" || d=="d5") ? "red" : ((i + Math.floor(i / 8)) % 2 == 0) ? "black" : "white";
    })
		.on("mouseover", function() {
    d3.select(this).raise();
  	})
    .on("mouseout", function() {
    d3.select(this).lower();
  	});

// Create the squares on the chessboard
var squares = svg.selectAll("rect")
    .data(board)
    .enter()
    .append("rect")
    .attr("x", function(d, i) {
        return (i % 8) * 50;
    })
    .attr("y", function(d, i) {
        return Math.floor(i / 8) * 50;
    })
    .attr("width", 50)
    .attr("height", 50)

    .style("fill", function(d, i) {
        return ((i + Math.floor(i / 8)) % 2 == 0) ? "white" : "black";
    })
		.on("mouseover", function() {
    d3.select(this).lower();
  	})
    .on("mouseout", function() {
    d3.select(this).raise();
  	})
		.attr("id", function(d) {
        return d;
    });


  

