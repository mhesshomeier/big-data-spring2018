

height = 300
width = 250
gap = 10

// overall svg
svg = d3.select("body")
    .append("svg")
    .attr("id", "mainsvg")
    .attr("height", height)
    .attr("width", width*2 + gap)

// first svg
svg1 = d3.select("svg#mainsvg")
    .append("svg")
    .attr("id", "svg1")
    .attr("height", height)
    .attr("width", width)
svg2 = d3.select("svg#mainsvg")
    .append("g") // group to move svg sideways
      .attr("transform", "translate(" + (width+gap) + ")")
      .append("svg")
      .attr("id", "svg2")
      .attr("height", height)
      .attr("width", width)

      // add a box around each SVG
      svg1.append("rect")
          .attr("height", height)
          .attr("width", width)
          .attr("stroke", "black")
          .attr("fill", "#fff")
          .attr("stroke-width", 2)
      svg2.append("rect")
          .attr("height", height)
          .attr("width", width)
          .attr("stroke", "black")
          .attr("fill", "#fff")
          .attr("stroke-width", 2)



// Map svg
var svg = d3.select("#map"),
    margin = {top: 20, right: 20, bottom: 150, left: 40},
    width = +svg1.attr("width") - margin.left - margin.right,
    height = +svg1.attr("height") - margin.top - margin.bottom,
    g = svg1.append("g").attr("class", "stack").attr("transform", "translate(" + margin.left + "," + margin.top + ")");



  // Our D3 code will go here.
  // var width = 720,
  // height = 700;

  var albersProjection = d3.geoAlbers()
    .scale( 190000 )
    .rotate( [71.057,0] )
    .center( [0, 42.313] )
    .translate( [width/2,height/2] );

  var path = d3.geoPath()
      .projection(albersProjection);

  var svg1 = d3.select("#map").append("svg")
      .attr("width", width)
      .attr("height", height);

  var svg2 = d3.select("#chart").append("svg")
      .attr("width", width)
      .attr("height", height);

  var x = d3.scaleLinear()
      .domain([0, 0.1, 0.2, 0.3, 0.4])
      .rangeRound([420, 480]);

  var color = d3.scaleThreshold()
      .domain([0, 0.1, 0.2, 0.3, 0.4])
      .range(d3.schemeBlues[5]);

  var g = svg.append("g")
      .attr("class", "key")
      .attr("transform", "translate(0,40)");

  var tooltip = d3.select("body")
    .append("div")
      .style("position", "absolute")
      .style("font-family", "'Open Sans', sans-serif")
      .style("font-size", "12px")
      .style("z-index", "10")
      .style("background-color", "white")
      .style("padding", "5px")
      .style("opacity", "0.7")
      .style("visibility", "hidden");

  g.selectAll("rect")
    .data(color.range().map(function(d) {
        d = color.invertExtent(d);
        if (d[0] == null) d[0] = x.domain()[0];
        if (d[1] == null) d[1] = x.domain()[1];
        return d;
      }))
    .enter().append("rect")
      .attr("height", 8)
      .attr("x", function(d) { return x(d[0]); })
      .attr("width", function(d) { return x(d[1]) - x(d[0]); })
      .attr("fill", function(d) { return color(d[0]); });

    g.append("text")
        .attr("class", "caption")
        .attr("x", x.range()[0])
        .attr("y", -6)
        .attr("fill", "#000")
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text("% of 311 Requests from Twitter");

    g.call(d3.axisBottom(x)
        .tickSize(13)
        .tickFormat(function(x, i) { return i ? x : x + "%"; })
        .tickValues(color.domain()))
      .select(".domain")
        .remove();

  d3.queue()
    .defer(d3.json, "data/boston_neigh.json") // Load US Counties
    .defer(d3.csv, "data/boston_311_totals.csv") // Load Unemployment csV
    .await(ready); // Run 'ready' when JSONs are loaded

  function ready(error, neigh, calls) {
    if (error) throw error;

    var calls_pct = {}; // Create empty object for holding dataset
    calls.forEach(function(d) {
      // console.log((d.twit_count / d.tot_count) * 100)
      calls_pct[d.id] = +((d.twit_count / d.tot_count) * 100); // Create property for each ID, give it value from rate
    });

    svg.append("g")
        .attr("class", "neighborhoods")
      .selectAll("path")
        .data(topojson.feature(neigh, neigh.objects.boston_neigh).features) // Bind TopoJSON data elements
      .enter().append("path")
        .attr("d", path)
        .style("fill", function(d) {
          return color(calls_pct[d.properties.OBJECTID]); // get rate value for property matching data ID
          // pass rate value to color function, return color based on domain and range
        })
        .style("stroke", "white")
        .on("mouseover", function(d){
          return tooltip.style("visibility", "visible").text(d.properties.Name + ": " + calls_pct[d.properties.OBJECTID].toFixed(2) + "%");
        })
        .on("mousemove", function(d){
          return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px").text(d.properties.Name + ": " + calls_pct[d.properties.OBJECTID].toFixed(2) + "%");
        })
        .on("mouseout", function(d){
          return tooltip.style("visibility", "hidden");
        });

        var x = d3.scaleBand()
          .rangeRound([0, width])
          .paddingInner(0.05)
          .align(0.1);

        // set y scale
        var y = d3.scaleLinear()
          .rangeRound([height, 0]);

          var z = d3.scaleOrdinal()
            .range(["#2166ac","#b2182b","#aaa"]);

          var keys = calls.columns.slice(1);

          calls.sort(function(a, b) { return b.total - a.total; });
          x.domain(calls.map(function(d) { return d.State; }));
          y.domain([0, d3.max(calls, function(d) { return d.total; })]).nice();
          z.domain(keys);

          g.append("g")
            .selectAll("g")
            .data(d3.stack().keys(keys)(calls))
            .enter().append("g")
              .attr("fill", function(d) { return z(d.key); })
            .selectAll("rect")
            .data(function(d) { return d; })
            .enter().append("rect")
              .attr("x", function(d) { return x(d.Name); })
              .attr("y", function(d) { return y(d[1]); })
              .attr("height", function(d) { return y(d[0]) - y(d[1]); })
              .attr("width", x.bandwidth())
              //The next line assigns each rectangle a class that matches the state names above: AK, AR, etc.
              .attr("class", function (d) { return d.Name;})
              //The mouseover functions work just like the ones in the map, they add "hover" class to all matching elements
            .on("mouseover", function(d) {
                //d3.select(this).classed("hover",true);
                d3.selectAll("." + d.Name).classed("hover",true);
                console.log(d.data.Name);
              })
            .on("mouseout", function(d) {
              //d3.select(this).classed("hover",false);
              d3.selectAll("." + d.Name).classed("hover", false);
            });
          }
