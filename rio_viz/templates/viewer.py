"""rio-viz: Viewer template."""


def viewer_template(
    endpoint: str, mapbox_access_token: str = "", mapbox_style="satellite"
) -> str:
    """Rio-viz viewer."""
    return f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8' />
        <title>Rio Viz</title>
        <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />

        <script src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.js'></script>
        <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.css' rel='stylesheet' />

        <link href='https://api.mapbox.com/mapbox-assembly/v0.23.2/assembly.min.css' rel='stylesheet'>
        <script src='https://api.mapbox.com/mapbox-assembly/v0.23.2/assembly.js'></script>

        <script src='https://npmcdn.com/@turf/turf/turf.min.js'></script>
        <script src="http://d3js.org/d3.v4.js"></script>

        <style>
            body {{ margin:0; padding:0; width:100%; height:100%;}}
            #map {{ position:absolute; top:0; bottom:0; width:100%; }}

            .zoom-info {{
                z-index: 10;
                position: absolute;
                bottom: 17px;
                right: 0;
                padding: 5px;
                width: auto;
                height: auto;
                font-size: 12px;
                color: #000;
            }}
            .loading-map {{
                position: absolute;
                width: 100%;
                height: 100%;
                color: #FFF;
                background-color: #000;
                text-align: center;
                opacity: 0.5;
                font-size: 45px;
            }}
            .loading-map.off{{
                opacity: 0;
                -o-transition: all .5s ease;
                -webkit-transition: all .5s ease;
                -moz-transition: all .5s ease;
                -ms-transition: all .5s ease;
                transition: all ease .5s;
                visibility:hidden;
            }}
            .middle-center {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }}

            .middle-center * {{
                display: block;
                padding: 5px;
            }}

            #menu {{
              left: 0;
              top: 0;
              -o-transition: all .5s ease;
              -webkit-transition: all .5s ease;
              -moz-transition: all .5s ease;
              -ms-transition: all .5s ease;
              transition: all ease .5s;
            }}

            #menu.off {{
              left: -360px;
              -o-transition: all .5s ease;
              -webkit-transition: all .5s ease;
              -moz-transition: all .5s ease;
              -ms-transition: all .5s ease;
              transition: all ease .5s;
            }}
            #toolbar {{
              height: 35px;
            }}

            #toolbar li {{
              display: block;
              color: #fff;
              background-color: #556671;
              font-weight: 700;
              font-size: 12px;
              padding: 5px;
              height: 100%;
              width: 100%;
              text-transform: uppercase;
              text-align: center;
              text-decoration: none;
              outline: 0;
              cursor: pointer;
              -webkit-touch-callout: none;
                -webkit-user-select: none;
                  -moz-user-select: none;
                    -ms-user-select: none;
                        user-select: none;
            }}

            #toolbar li svg {{
              font-size: 25px;
              line-height: 25px;
              padding-bottom: 0;
            }}

            #toolbar li:hover {{
              background-color: #28333b;
            }}

            #toolbar li.active {{
              color: #000;
              background-color: #fff;
            }}

            #menu-content section {{
              display: none;
            }}

            #menu-content section.active {{
              display: inherit;
            }}

            #hide-arrow {{
              -o-transition: all .5s ease;
              -webkit-transition: all .5s ease;
              -moz-transition: all .5s ease;
              -ms-transition: all .5s ease;
              transition: all ease .5s;
            }}

            #hide-arrow.off {{
              transform: rotate(-180deg);
            }}

            #btn-hide {{
              position: absolute;
              top: 0;
              height: 35px;
              font-size: 35px;
              line-height: 35px;
              vertical-align: middle;
              right: -35px;
              color: #28333b;
              background-color: #fff;
            }}

            #btn-hide:hover {{
              color: #fff;
              background-color: #28333b;
              cursor: pointer;
            }}

            .line-red {{
              fill: none;
              stroke: red;
              stroke-width: 1.5px;
            }}
            .line-green {{
              fill: none;
              stroke: green;
              stroke-width: 1.5px;
            }}
            .line-blue {{
              fill: none;
              stroke: blue;
              stroke-width: 1.5px;
            }}

            @media(max-width: 767px) {{

              #menu.off {{
                left: -240px;
                -o-transition: all .5s ease;
                -webkit-transition: all .5s ease;
                -moz-transition: all .5s ease;
                -ms-transition: all .5s ease;
                transition: all ease .5s;
              }}

              .mapboxgl-ctrl-attrib {{
                  font-size: 10px;
              }}
            }}

        </style>
    </head>
    <body>

    <div id='menu' class='flex-child w240 w360-ml absolute bg-white z2 off'>

      <ul id='toolbar' class='grid'>
        <li id='3b' class="col col--4 active" title="rgb" onclick="switchPane(this)">
          <svg class='icon icon--l inline-block'><use xlink:href='#icon-menu'/></svg>
        </li>
        <li id='1b' class="col col--4" title="band" onclick="switchPane(this)">
          <svg class='icon icon--l inline-block'><use xlink:href='#icon-minus'/></svg>
        </li>
        <!--
        <li id='process' disabled class="col col--4" title="process" onclick="switchPane(this)">
          <svg class='icon icon--l inline-block'><use xlink:href='#icon-raster'/></svg>
        </li>
        -->
      </ul>

      <div id='menu-content' class='relative'>

        <!-- RGB Selection -->
        <section id='3b-section' class='px12 pt12 pb6 active'>
          <div class='txt-h5 mb6 color-black'><svg class='icon icon--l inline-block'><use xlink:href='#icon-layers'/></svg> RGB</div>
          <div id='rgb-buttons' class='align-center px6 py6'>
            <div class='select-container'>
              <select id='r-selector' class='select select--s select--stroke wmax-full color-red'></select>
              <div class='select-arrow color-black'></div>
            </div>

            <div class='select-container'>
              <select id='g-selector' class='select select--s select--stroke wmax-full color-green'></select>
              <div class='select-arrow color-black'></div>
            </div>

            <div class='select-container'>
              <select id='b-selector' class='select select--s select--stroke wmax-full color-blue'></select>
              <div class='select-arrow color-black'></div>
            </div>
          </div>

          <!-- Histogram -->
          <div>
            <div class='txt-h5 mt6 mb6 color-black'><svg class='icon icon--l inline-block'><use xlink:href='#icon-graph'/></svg> Histogram</div>
            <div id="histogram3b" class="w-full h120 h240-ml relative"></div>
          </div>

        </section>

        <!-- 1 Band Selection -->
        <section id='1b-section' class='px12 pt12 pb6'>
          <div class='txt-h5 mb6 color-black'>
            <svg class='icon icon--l inline-block'><use xlink:href='#icon-layers'/></svg> Layers
          </div>
          <div class='select-container wmax-full'>
            <select id='layer-selector' class='select select--s select--stroke wmax-full color-black'>
            </select>
            <div class='select-arrow color-black'></div>
          </div>

          <div class='txt-h5 mt6 mb6 color-black'>
            <svg class='icon icon--l inline-block'><use xlink:href='#icon-layers'/></svg> Viz
          </div>
          <div id='viz-selector' class='toggle-group bg-gray-faint mt6 mb6' style="line-height: 0">
            <label class='toggle-container'>
              <input value="raster" checked="checked" name='toggle-viz' type='radio' />
              <div title='Raster Viz' class='toggle color-gray-dark-on-hover'><svg class='icon icon--l inline-block w18 h18'><use xlink:href='#icon-raster'/></svg></div>
            </label>
            <label class='toggle-container'>
              <input value="point" name='toggle-viz' type='radio' />
              <div title='Point Viz' class='toggle color-gray-dark-on-hover'><svg class='icon icon--l inline-block w18 h18'><use xlink:href='#icon-circle'/></svg></div>
            </label>
            <label class='toggle-container'>
              <input value="polygon" name='toggle-viz' type='radio' />
              <div title='3D Viz' class='toggle color-gray-dark-on-hover'><svg class='icon icon--l inline-block w18 h18'><use xlink:href='#icon-extrusion'/></div>
            </label>
          </div>

          <!-- 1b Histogram -->
          <div>
            <div class='txt-h5 mt6 mb6 color-black'><svg class='icon icon--l inline-block'><use xlink:href='#icon-graph'/></svg> Histogram</div>
            <div id="histogram1b" class="w-full h120 h240-ml relative"></div>
          </div>

          <!-- Color Map -->
          <div id='colormap-section'>
            <div class='txt-h5 mb6 color-black'><svg class='icon icon--l inline-block'><use xlink:href='#icon-palette'/></svg> Color Map</div>
            <div class='select-container wmax-full'>
              <select id='colormap-selector' class='select select--s select--stroke wmax-full color-black'>
                <option value='b&w'>Black and White</option>
                <option value='cfastie'>cfastie</option>
                <option value='rplumbo'>rplumbo</option>
                <option value='schwarzwald'>schwarzwald (elevation)</option>
              </select>
              <div class='select-arrow color-black'></div>
            </div>
          </div>

          <!-- V Exag -->
          <div id='extrusion-section' class='none'>
            <div class='txt-h5 mt6 mb6 color-black'>Vercital Exageration</div>
            <div class='px6 py6'>
              <input id="ex-value" class='input input--s wmax60 inline-block align-center color-black' value='1' />
              <button id="updateExag" class='btn bts--xs btn--stroke bg-darken25-on-hover inline-block txt-s color-black ml12'>Apply</button>
            </div>
          </div>
        </section>

        <!-- Histogram Cut -->
        <div class='px12 pt12 pb6'>
          <div class='txt-h5 mt6 mb6 color-black'>Histogram Cut</div>
          <div id='histcut-selector' class='toggle-group bg-gray-faint mt6 mb6' style="line-height: 0">
            <label class='toggle-container'>
              <input value="minmax" checked="checked" name='toggle-histo' type='radio' />
              <div title='MinMax' class='toggle color-gray-dark-on-hover'>MinMax</div>
            </label>
            <label class='toggle-container'>
              <input value="2pc" name='toggle-histo' type='radio' />
              <div title='2%-98%' class='toggle color-gray-dark-on-hover'>2%</div>
            </label>
            <label class='toggle-container'>
              <input value="5pc" name='toggle-histo' type='radio' />
              <div title='5%-95%' class='toggle color-gray-dark-on-hover'>5%</div>
            </label>
          </div>
        </div>

        <!-- Resampling -->
        <div class='px12 pt12 pb6'>
          <div class='txt-h5 mt6 mb6 color-black'>Resampling Method</div>
          <div id='resamp-selector' class='toggle-group bg-gray-faint mt6 mb6' style="line-height: 0">
            <label class='toggle-container'>
              <input value='bilinear' name='toggle-resamp' type='radio' />
              <div title='bilinear' class='toggle color-gray-dark-on-hover'>bilinear</div>
            </label>
            <label class='toggle-container'>
              <input value='nearest' checked='checked' name='toggle-resamp' type='radio' />
              <div title='nearest' class='toggle color-gray-dark-on-hover'>nearest</div>
            </label>
          </div>
        </div>
      </div>

      <button id='btn-hide'><svg id='hide-arrow' class='icon'><use xlink:href='#icon-arrow-right'/></svg></button>

    </div>

    <div id='map'>
      <div id='loader' class="loading-map z3">
        <div class="middle-center">
          <div class="round animation-spin animation--infinite animation--speed-1">
            <svg class='icon icon--l inline-block'><use xlink:href='#icon-satellite'/></svg>
          </div>
        </div>
      </div>
      <div class="zoom-info"><span id="zoom"></span></div>
    </div>

    <script>
    var scope = {{ metadata: {{}}, config: {{}}}}

    mapboxgl.accessToken = '{mapbox_access_token}'
    const api_endpoint = '{endpoint}'

    let style
    if (mapboxgl.accessToken !== '') {{
      style = 'mapbox://styles/mapbox/{mapbox_style}-v9'
    }} else {{
      style = {{ version: 8, sources: {{}}, layers: [] }}
    }}

    var map = new mapboxgl.Map({{
        container: 'map',
        style: style,
        center: [0, 0],
        zoom: 1
    }})

    map.on('zoom', function (e) {{
      const z = (map.getZoom()).toString().slice(0, 6)
      document.getElementById('zoom').textContent = z
    }})

    const set1bViz = () => {{
      const resamp = document.getElementById('resamp-selector').querySelector("input[name='toggle-resamp']:checked").value
      const vizType = document.getElementById('viz-selector').querySelector("input[name='toggle-viz']:checked").value
      switch (vizType) {{
        case 'raster':
          const active_layer = document.getElementById('layer-selector')[document.getElementById('layer-selector').selectedIndex]
          const indexes = active_layer.getAttribute('data-indexes')
          const minV = scope.config[indexes].min
          const maxV = scope.config[indexes].max

          let url = `${{api_endpoint}}/tilejson.json?tile_format=png&indexes=${{indexes}}&rescale=${{minV}},${{maxV}}&resampling_method=${{resamp}}`
          const cmap = document.getElementById('colormap-selector')[document.getElementById('colormap-selector').selectedIndex]
          if (cmap.value !== 'b&w') url += `&color_map=${{cmap.value}}`

          map.addSource('raster', {{ type: 'raster', url: url }})
          addLayer(vizType)
          break

        case 'point':
          map.addSource('mvt', {{
            type: 'vector',
            url: `${{api_endpoint}}/tilejson.json?tile_format=pbf&feature_type=point&resampling_method=${{resamp}}`
          }})
          addLayer(vizType)
          break

        case 'polygon':
          map.addSource('mvt', {{
            type: 'vector',
            url: `${{api_endpoint}}/tilejson.json?tile_format=pbf&feature_type=polygon&resampling_method=${{resamp}}`
          }})
          addLayer(vizType)
          break

        default:
          throw new Error(`Invalid ${{vizType}}`)
      }}
    }}

    const set3bViz = () => {{
      const resamp = document.getElementById('resamp-selector').querySelector("input[name='toggle-resamp']:checked").value

      const r = document.getElementById('r-selector').value
      const g = document.getElementById('g-selector').value
      const b = document.getElementById('b-selector').value

      const min1 = scope.config[r].min
      const max1 = scope.config[r].max
      const min2 = scope.config[g].min
      const max2 = scope.config[g].max
      const min3 = scope.config[r].min
      const max3 = scope.config[r].max
      const rescale = `${{min1}},${{max1}},${{min2}},${{max2}},${{min3}},${{max3}}`
      indexes = `${{r}},${{g}},${{b}}`

      let url = `${{api_endpoint}}/tilejson.json?tile_format=png&indexes=${{indexes}}&rescale=${{rescale}}&resampling_method=${{resamp}}`
      map.addSource('raster', {{ type: 'raster', url: url }})
      map.addLayer({{id: 'raster', type: 'raster', source: 'raster'}})
      addHisto3Bands()
    }}

    const switchViz = () => {{
      if (map.getLayer('raster')) map.removeLayer('raster')
      if (map.getSource('raster')) map.removeSource('raster')

      if (map.getLayer('mvt')) map.removeLayer('mvt')
      if (map.getSource('mvt')) {{ map.removeSource('mvt') }}

      const rasterType = document.getElementById('toolbar').querySelector(".active").id
      switch (rasterType) {{
        case '1b':
          set1bViz()
          break
        case '3b':
          set3bViz()
          break
        default:
          throw new Error(`Invalid ${{rasterType}}`)
      }}
    }}

    const addLayer = (layerType) => {{
      if (map.getLayer('raster')) map.removeLayer('raster')
      if (map.getLayer('mvt')) map.removeLayer('mvt')

      const active_layer = document.getElementById('layer-selector')[document.getElementById('layer-selector').selectedIndex]
      const indexes = active_layer.getAttribute('data-indexes')
      const sMin = scope.config[indexes].min
      const sMax = scope.config[indexes].max
      addHisto1Band()

      const propName = active_layer.value
      const exag = parseFloat(document.getElementById('ex-value').value)

      switch (layerType) {{
        case 'raster':
          map.addLayer({{
            id: 'raster',
            type: 'raster',
            source: 'raster'
          }})
          break

        case 'point':
          map.addLayer({{
            id: 'mvt',
            source: 'mvt',
            'source-layer': 'my_layer',
            type: 'circle',
            paint: {{
              'circle-color': [
                'interpolate',
                ['linear'],
                ['to-number', ['get', propName]],
                sMin, '#3700f0',
                sMax, '#ed0707'
              ],
              'circle-radius': {{
                'base': 1,
                'stops': [
                  [0, 10],
                  [9, 5]
                ]
              }}
            }}
          }})

          break

        case 'polygon':
          map.addLayer({{
            id: 'mvt',
            source: 'mvt',
            'source-layer': 'my_layer',
            type: 'fill-extrusion',
            paint: {{
              'fill-extrusion-opacity': 1,
              'fill-extrusion-height': [
                'interpolate',
                ['linear'],
                ['to-number', ['get', propName]],
                sMin, 0,
                sMax, sMax * exag
              ],
              'fill-extrusion-color': [
                'interpolate',
                ['linear'],
                ['to-number', ['get', propName]],
                sMin, '#3700f0',
                sMax, '#ed0707'
              ]
            }}
          }})

          break

        default:
          throw new Error(`Invalid ${{layerType}}`)
      }}
    }}

    const addHisto3Bands = () => {{
      const r = document.getElementById('r-selector').value
      const g = document.getElementById('g-selector').value
      const b = document.getElementById('b-selector').value

      const rStats = scope.metadata.statistics[r]
      const gStats = scope.metadata.statistics[g]
      const bStats = scope.metadata.statistics[b]

      const minV = Math.min(...[rStats.min, gStats.min, bStats.min])
      const maxV = Math.max(...[rStats.max, gStats.max, bStats.max])

      const rCounts = rStats.histogram[0]
      const gCounts = rStats.histogram[0]
      const bCounts = rStats.histogram[0]

      const h = Math.max(...[].concat.apply([], [rCounts, gCounts, bCounts]))

      const bbox = d3.select('#histogram3b').node().getBoundingClientRect()

      // set the dimensions and margins of the graph
      const margin = {{ top: 10, right: 30, bottom: 30, left: 40 }}
      const width = bbox.width - margin.left - margin.right
      const height = bbox.height - margin.top - margin.bottom

      d3.select('#histogram3b').selectAll('*').remove()
      // append the svg object to the body of the page
      var svg = d3.select('#histogram3b')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

      // X axis: scale and draw:
      var x = d3.scaleLinear()
        .domain([minV, maxV])
        .range([0, width])

      svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x))

      // Y axis: scale and draw:
      var y = d3.scaleLinear().range([height, 0])
      y.domain([0, h])
      svg.append('g').call(d3.axisLeft(y))

      const addLine = (stats, color) => {{
        //Draw Red line
        const data = []
        for (var i = 0; i < stats.histogram[0].length; i++) {{
          data.push({{
            count: stats.histogram[0][i],
            value: stats.histogram[1][i]
          }})
        }}
        var guide = d3.line()
                      .x(function(d){{ return x(d.value) }})
                      .y(function(d){{ return y(d.count) }});
        var line = svg.append('path')
                      .datum(data)
                      .attr('d', guide)
                      .attr('class', `line-${{color}}`);
      }}
      addLine(rStats, "red")
      addLine(gStats, "green")
      addLine(bStats, "blue")

      //Draw axes
      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + h + ")")
          .call(x);

      svg.append("g")
          .attr("class", "y axis")
          .call(y)
          .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
    }}

    const addHisto1Band = () => {{
      const active_layer = document.getElementById('layer-selector')[document.getElementById('layer-selector').selectedIndex]
      const indexes = active_layer.getAttribute('data-indexes')
      const stats = scope.metadata.statistics[indexes]

      const counts = stats.histogram[0]
      const values = stats.histogram[1]
      const bbox = d3.select('#histogram1b').node().getBoundingClientRect()

      // set the dimensions and margins of the graph
      const margin = {{ top: 10, right: 30, bottom: 30, left: 40 }}
      const width = bbox.width - margin.left - margin.right
      const height = bbox.height - margin.top - margin.bottom

      d3.select('#histogram1b').selectAll('*').remove()
      // append the svg object to the body of the page
      var svg = d3.select('#histogram1b')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

      const min = stats.min
      const max = stats.max

      // X axis: scale and draw:
      var x = d3.scaleLinear()
        .domain([min, max])
        .range([0, width])

      svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x))

      // Y axis: scale and draw:
      var y = d3.scaleLinear().range([height, 0])
      y.domain([0, d3.max(counts)])
      svg.append('g').call(d3.axisLeft(y))

      const bins = []
      for (var i = 0; i < counts.length; i++) {{
        bins.push({{
          count: counts[i],
          value: values[i]
        }})
      }}

      // append the bar rectangles to the svg element
      svg.selectAll('rect')
        .data(bins)
        .enter()
        .append('rect')
        .attr('x', 1)
        .attr('transform', d => {{ return 'translate(' + x(d.value) + ',' + y(d.count) + ')' }})
        .attr('width', 10)
        .attr('height', d => {{ return height - y(d.count) }})
        .style('fill', '#69b3a2')
    }}

    document.getElementById('btn-hide').addEventListener('click', () => {{
      document.getElementById('hide-arrow').classList.toggle('off')
      document.getElementById('menu').classList.toggle('off')
    }})

    document.getElementById('viz-selector').addEventListener('change', (e) => {{
      switch (e.target.value) {{
        case 'raster':
          document.getElementById('colormap-section').classList.remove('none')
          document.getElementById('extrusion-section').classList.add('none')
          break

        case 'point':
          document.getElementById('colormap-section').classList.add('none')
          document.getElementById('extrusion-section').classList.add('none')
          break

        case 'polygon':
          document.getElementById('colormap-section').classList.add('none')
          document.getElementById('extrusion-section').classList.remove('none')
          break

        default:
      }}
      switchViz()
    }})

    document.getElementById('resamp-selector').addEventListener('change', (e) => {{
      switchViz()
    }})


    // MVT have already all the layers while for raster we need to fetch new tiles
    const updateViz = () => {{
      const newViz = document.getElementById('viz-selector').querySelector("input[name='toggle-viz']:checked").value
      if (newViz === "raster") {{
        switchViz()
      }} else {{
        addLayer(newViz)
      }}
    }}

    document.getElementById('layer-selector').addEventListener('change', () => {{
      const active_layer = document.getElementById('layer-selector')[document.getElementById('layer-selector').selectedIndex]
      updateViz()
    }})

    document.getElementById('r-selector').addEventListener('change', () => {{switchViz()}})
    document.getElementById('g-selector').addEventListener('change', () => {{switchViz()}})
    document.getElementById('b-selector').addEventListener('change', () => {{switchViz()}})

    document.getElementById('updateExag').addEventListener('click', () => {{
      updateViz()
    }})

    document.getElementById('colormap-selector').addEventListener('change', () => {{
      updateViz()
    }})

    const switchPane = (event) => {{
      const cur = document.getElementById('toolbar').querySelector(".active")
      const activeViz = cur.id
      const nextViz = event.id
      cur.classList.toggle('active')
      event.classList.toggle('active')

      const curSection = document.getElementById(`${{activeViz}}-section`)
      curSection.classList.toggle('active')
      const nextSection = document.getElementById(`${{nextViz}}-section`)
      nextSection.classList.toggle('active')
      switchViz()
    }}

    document.getElementById('histcut-selector').addEventListener('change', (e) => {{
      let pmin = 0
      let pmax = 100

      switch (e.target.value) {{
        case 'minmax':
          break
        case '2pc':
            pmin = 2.0
            pmax = 98.0
          break
        case '5pc':
            pmin = 5.0
            pmax = 95.0
          break
      }}
      fetch(`${{api_endpoint}}/metadata?pmin=${{pmin}}&pmax=${{pmax}}`)
          .then(res => {{
            if (res.ok) return res.json()
            throw new Error('Network response was not ok.')
          }})
          .then(data => {{
            scope.metadata.statistics = data.statistics
            Object.entries(scope.metadata.statistics).forEach(entry => {{
              scope.config[entry[0]] = {{ "min": entry[1].pc[0], "max": entry[1].pc[1] }}
            }})
            const rasterType = document.getElementById('toolbar').querySelector(".active").id
            if (rasterType === "1b") {{
              updateViz()
            }} else {{
              switchViz()
            }}
          }})
          .catch(err => {{
            console.warn(err)
          }})
    }})

    const addAOI = (bounds) => {{
      const geojson = {{
          "type": "FeatureCollection",
          "features": [turf.bboxPolygon(bounds)]
      }}

      map.addSource('aoi', {{
        'type': 'geojson',
        'data': geojson
      }})

      map.addLayer({{
        id: 'aoi-polygon',
        type: 'line',
        source: 'aoi',
        layout: {{
          'line-cap': 'round',
          'line-join': 'round'
        }},
        paint: {{
          'line-color': '#3bb2d0',
          'line-width': 1
        }}
      }})
      return
    }}

    map.on('load', () => {{
      map.on('mousemove', (e) => {{
        if (!map.getLayer('mvt')) return
        const mouseRadius = 1
        const feature = map.queryRenderedFeatures([
          [e.point.x - mouseRadius, e.point.y - mouseRadius],
          [e.point.x + mouseRadius, e.point.y + mouseRadius]
        ], {{ layers: ['mvt'] }})[0]
        if (feature) {{
          map.getCanvas().style.cursor = 'pointer'
        }} else {{
          map.getCanvas().style.cursor = 'inherit'
        }}
      }})

      map.on('click', 'mvt', (e) => {{
        let html = '<table><tr><th class="align-l">property</th><th class="px3 align-r">value</th></tr>'
        Object.entries(e.features[0].properties).forEach(entry => {{
          let key = entry[0]
          let value = entry[1]
          if (key !== 'id') html += `<tr><td>${{key}}</td><td class="px3 align-r">${{value}}</td></tr>`
        }})
        html += `<tr><td class="align-l">lon</td><td class="px3 align-r">${{e.lngLat.lng.toString().slice(0, 7)}}</td></tr>`
        html += `<tr><td class="align-l">lat</td><td class="px3 align-r">${{e.lngLat.lat.toString().slice(0, 7)}}</td></tr>`
        html += '</table>'
        new mapboxgl.Popup()
          .setLngLat(e.lngLat)
          .setHTML(html)
          .addTo(map)
      }})

      // we cannot click on raster layer (mapbox-gl bug)
      map.on('click', (e) => {{
        if (!map.getLayer('raster')) return
        const bounds = map.getSource('raster').bounds
        if (
          (e.lngLat.lng >= bounds[0] && e.lngLat.lng <= bounds[2]) &&
          (e.lngLat.lat >= bounds[1] && e.lngLat.lat <= bounds[3])
        ) {{
          const coord = `${{e.lngLat.lng}},${{e.lngLat.lat}}`
          fetch(`${{api_endpoint}}/point?coordinates=${{coord}}`)
            .then(res => {{
              if (res.ok) return res.json()
              throw new Error('Network response was not ok.');
            }})
            .then(data => {{
              let html = '<table><tr><th class="align-l">property</th><th class="px3 align-r">value</th></tr>'
              Object.entries(data.value).forEach(entry => {{
                let key = entry[0]
                let value = entry[1]
                html += `<tr><td class="align-l">${{key}}</td><td class="px3 align-r">${{value}}</td></tr>`
              }})
              html += `<tr><td class="align-l">lon</td><td class="px3 align-r">${{e.lngLat.lng.toString().slice(0, 7)}}</td></tr>`
              html += `<tr><td class="align-l">lat</td><td class="px3 align-r">${{e.lngLat.lat.toString().slice(0, 7)}}</td></tr>`
              html += '</table>'
              new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML(html)
                .addTo(map)
            }})
            .catch(err => {{
              console.warn(err)
            }})
        }}
      }})

      fetch(`${{api_endpoint}}/metadata`)
        .then(res => {{
          if (res.ok) return res.json()
          throw new Error('Network response was not ok.')
        }})
        .then(data => {{
          scope.metadata = data
          console.log(data)

          scope.config = {{}}
          Object.entries(scope.metadata.statistics).forEach(entry => {{
            scope.config[entry[0]] = {{ "min": entry[1].min, "max": entry[1].max }}
          }})

          //1 band
          const layerList = document.getElementById('layer-selector')
          for (var i = 0; i < scope.metadata.band_descriptions.length; i++) {{
            let l = document.createElement('option')
            l.value = scope.metadata.band_descriptions[i][1]
            l.setAttribute('data-indexes', scope.metadata.band_descriptions[i][0].toString())
            l.text = scope.metadata.band_descriptions[i][1]
            layerList.appendChild(l)
          }}

          //RGB
          const nbands = scope.metadata.band_descriptions.length
          const rList = document.getElementById('r-selector')
          for (var i = 0; i < scope.metadata.band_descriptions.length; i++) {{
            let l = document.createElement('option')
            let val = scope.metadata.band_descriptions[i][0]
            l.value = val
            l.setAttribute('data-indexes', val.toString())
            l.text = scope.metadata.band_descriptions[i][1]
            if (i === 0) l.selected="selected"
            rList.appendChild(l)
          }}

          const gList = document.getElementById('g-selector')
          for (var i = 0; i < scope.metadata.band_descriptions.length; i++) {{
            let l = document.createElement('option')
            let val = scope.metadata.band_descriptions[i][0]
            l.value = val
            l.setAttribute('data-indexes', val.toString())
            l.text = scope.metadata.band_descriptions[i][1]
            if (i === 1) l.selected="selected"
            gList.appendChild(l)
          }}
          const bList = document.getElementById('b-selector')
          for (var i = 0; i < scope.metadata.band_descriptions.length; i++) {{
            let l = document.createElement('option')
            let val = scope.metadata.band_descriptions[i][0]
            l.value = val
            l.setAttribute('data-indexes', val.toString())
            l.text = scope.metadata.band_descriptions[i][1]
            if (nbands > 2 && i === 2) {{
              l.selected="selected"
            }} else {{
              l.selected="selected"
            }}
            bList.appendChild(l)
          }}

          // remove loader
          document.getElementById('loader').classList.toggle('off')
          document.getElementById('hide-arrow').classList.toggle('off')
          document.getElementById('menu').classList.toggle('off')

          const bounds = scope.metadata.bounds.value
          map.fitBounds([[bounds[0], bounds[1]], [bounds[2], bounds[3]]])
          addAOI(bounds)

          switchViz()
        }})
        .catch(err => {{
          console.warn(err)
        }})
    }})

    </script>

    </body>
    </html>"""
