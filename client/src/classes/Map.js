import * as am5 from '@amcharts/amcharts5';
import * as am5map from '@amcharts/amcharts5/map';
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated';
import am5geodata_worldLow from '@amcharts/amcharts5-geodata/worldLow';
import { shortest_path } from './utils/shortestPath';

const plane_size = 0.13;
const airports_size = 11;

/**
 * This class represent ammap 5 object, link: https://www.amcharts.com/docs/v5/charts/map-chart/
 *
 *
 */

export default class Map {
  constructor(
    spy,
    setSpy,
    agents,
    updateAgentLocationId,
    setSelectedAirport,
    targetPosition,
    delay
  ) {
    this.chart = null;
    this.root = null;
    //Hold fligts graph
    this.graph = null;
    //Hold all the lines objects in the map
    this.allLineSeries = null;
    //Hold the lines objects that are currently visible
    this.lineSeries = null;
    //Hold all the origin (map point series)
    this.airportsSeries = null;
    //Hold the plane
    this.planeSeries = null;
    //Hold the opponent plane
    this.opponentPlaneSeries = [];
    //help build airportsSeries (map point series) in correct format
    this.originCities = [];
    //represent the current selected airport
    this.selectedAirport = null;
    //hold reference to setSelectedAirport in GameConponent
    this.setSelectedAirport = setSelectedAirport;
    //represent the current plane location on the map
    this.spy = spy;
    //hold reference to changePlaneLocationId in GameConponent
    this.updateSpyPlaneLocationId = setSpy;
    //represent the opponent plane location on the map
    this.agents = agents;
    //hold reference to setOpponentPlaneLocationId in GameConponent
    this.updateAgentLocationId = updateAgentLocationId;
    //represent the target position of the map
    this.targetPosition = targetPosition;
    //Hold the target
    this.targetSeries = null;
    //
    this.originTargetCities = [];

    this.spyShortestPathLines = [];
    this.delay = delay;
  }

  createMap = (graph) => {
    this.graph = graph;
    this.root = am5.Root.new('chartdiv');

    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    this.root.setThemes([am5themes_Animated.new(this.root)]);

    // Create the map chart
    // https://www.amcharts.com/docs/v5/charts/map-chart/
    this.chart = this.root.container.children.push(
      am5map.MapChart.new(this.root, {
        panX: 'rotateX',
        panY: 'none',
        // y: 130,
        projection: am5map.geoMercator(),
        zoomLevel: 1.8,
        minZoomLevel: 1.8,
        maxZoomLevel: 1.8,
        centerY: -130,
        centerMapOnZoomOut: true,
        //am5map.geoNaturalEarth1() Option for round map
      })
    );

    this.createSwitchButtonForGlobe(this.chart, this.root);

    // Create main polygon series for countries
    // https://www.amcharts.com/docs/v5/charts/map-chart/map-polygon-series/
    const polygonSeries = this.chart.series.push(
      am5map.MapPolygonSeries.new(this.root, {
        geoJSON: am5geodata_worldLow,
        exclude: ['AQ'],
        // fill: am5.color(0x000000),
      })
    );

    //Add longgitude and latitude lines
    const graticuleSeries = this.chart.series.push(
      am5map.GraticuleSeries.new(this.root, {})
    );
    graticuleSeries.mapLines.template.setAll({
      stroke: this.root.interfaceColors.get('alternativeBackground'),
      strokeOpacity: 0.08,
    });

    //Set the map water color
    const backgroundSeries = this.chart.series.unshift(
      am5map.MapPolygonSeries.new(this.root, {})
    );
    backgroundSeries.mapPolygons.template.setAll({
      fill: am5.color(0xedf7fa),
      stroke: am5.color(0xedf7fa),
    });
    backgroundSeries.data.push({
      geometry: am5map.getGeoRectangle(90, 180, -90, -180),
    });

    //Placed the airports on the map
    this.createAirportsSeries(graph, this.spy.id);
    //Placed the target position on the map
    this.createTargetPositionAirportsSeries(graph);

    //Create lines holder and lines settings
    this.createLineSeries();

    this.initiatePlayers(this.spy, this.agents);
  };

  initiatePlayers = (spy, agents) => {
    this.planeSeries = null;
    this.opponentPlaneSeries = [];
    this.spy = spy;
    this.agents = agents;

    //select airport based on id starting point
    // this.selectAirport(selectedAirport);
    //intiate the player1 plane based on id starting point
    this.initiatePlane(this.spy.id, this.spy.color);
    //Set spy shortest path to traget lines
    this.setSplyShortestPathLines();

    //intiate the player2 plane based on id starting point
    this.agents.map((agent, idx) =>
      this.initiateOpponentPlane(agent.id, agent.color, idx)
    );
  };

  //Create the switch toggle between regular map and globe
  createSwitchButtonForGlobe = (chart, root) => {
    // Add labels and controls
    const cont = chart.children.push(
      am5.Container.new(root, {
        layout: root.horizontalLayout,
        centerY: 100,
        centerX: -220,
      })
    );
    //add label
    cont.children.push(
      am5.Label.new(root, {
        centerY: am5.p50,
        text: 'Map',
      })
    );
    //add toggle button
    var switchButton = cont.children.push(
      am5.Button.new(root, {
        themeTags: ['switch'],
        centerY: am5.p50,
        icon: am5.Circle.new(root, {
          themeTags: ['icon'],
        }),
      })
    );
    //change between regualr map to globe, based by toggle button (active or not active)
    switchButton.on('active', function () {
      if (!switchButton.get('active')) {
        chart.set('projection', am5map.geoMercator());
        chart.set('panY', 'none');
        chart.set('rotationY', 0);
        chart.set('centerY', -130);
        chart.set('zoomLevel', 1.8);
        chart.set('minZoomLevel', 1.8);
        cont.set('centerY', 100);
      } else {
        chart.set('projection', am5map.geoOrthographic());
        chart.set('panY', 'rotateY');
        chart.set('zoomLevel', 1);
        chart.set('minZoomLevel', 1);
        chart.set('centerY', 0);
        cont.set('centerY', 0);
      }
    });
    //add label
    cont.children.push(
      am5.Label.new(root, {
        centerY: am5.p50,
        text: 'Globe',
      })
    );
  };

  //create series for lines and lines settings
  createLineSeries = () => {
    // Create visible line series for that will show on the plane location
    const lineSeries = this.chart.series.push(
      am5map.MapLineSeries.new(this.root, {})
    );
    lineSeries.mapLines.template.setAll({
      strokeOpacity: 0.6,
      strokeWidth: 2,
      cursorOverStyle: 'pointer',
      tooltipY: 0,
    });

    this.lineSeries = lineSeries;

    //Lines Series for spy shortest path to traget
    const spyPathLineSeries = this.chart.series.push(
      am5map.MapLineSeries.new(this.root, {})
    );
    spyPathLineSeries.mapLines.template.setAll({
      stroke: am5.color(0x5ae65a),
      strokeOpacity: 0.6,
      strokeWidth: 2,
      cursorOverStyle: 'pointer',
      tooltipY: 0,
    });
    this.spyShortestPathLines = spyPathLineSeries;

    //Create transparent line series for plane routes
    const allLineSeries = this.chart.series.push(
      am5map.MapLineSeries.new(this.root, {})
    );
    allLineSeries.mapLines.template.setAll({
      strokeOpacity: 0.6,
      strokeWidth: 0,
      cursorOverStyle: 'pointer',
    });

    const lineSeriesData = [];

    this.airportsSeries.data._values.map((item) => {
      const originLongitude = item.geometry.coordinates[0];
      const originLatitude = item.geometry.coordinates[1];
      item.destinations.map((id) => {
        const destinationDataItem = this.airportsSeries.getDataItemById(id);
        lineSeriesData.push({
          geometry: {
            type: 'LineString',
            coordinates: [
              [originLongitude, originLatitude],
              [
                destinationDataItem.get('longitude'),
                destinationDataItem.get('latitude'),
              ],
            ],
            id: `${item.id} ${id}`,
          },
        });
        return null;
      });
    });

    allLineSeries.data.setAll(lineSeriesData);
    this.allLineSeries = allLineSeries;
  };

  //crate series for aiports their settings and place them on the map
  createAirportsSeries = (graph, selectedAirport) => {
    // Create point series for markers
    // https://www.amcharts.com/docs/v5/charts/map-chart/map-point-series/
    const airportsSeries = this.chart.series.push(
      am5map.MapPointSeries.new(this.root, { idField: 'id' })
    );
    const root = this.root;
    const selectAirport = this.selectAirport;

    airportsSeries.bullets.push(function () {
      var circle = am5.Circle.new(root, {
        radius: airports_size,
        tooltipText: '{title}',
        cursorOverStyle: 'pointer',
        tooltipY: 0,
        fill: am5.color(0xffba00),
        stroke: root.interfaceColors.get('background'),
        strokeWidth: 2,
      });

      circle.events.on('click', function (e) {
        selectAirport(e.target.dataItem.get('id'));
      });
      return am5.Bullet.new(root, {
        sprite: circle,
      });
    });

    for (let i in graph) {
      this.originCities.push({
        id: i,
        title: graph[i].name,
        destinations: graph[i].destinations,
        geometry: {
          type: 'Point',
          coordinates: [graph[i].longitude, graph[i].latitude],
        },
        zoomLevel: 1.5,
        zoomPoint: {
          longitude: 52.4912,
          latitude: -1.9348,
        },
      });
    }
    airportsSeries.data.setAll(this.originCities);
    // airportsSeries.events.on('datavalidated', function () {
    //   selectAirport(selectedAirport);
    // });
    this.airportsSeries = airportsSeries;
  };

  //crate target position aiport on the map
  createTargetPositionAirportsSeries = (graph) => {
    const targetShortName = this.targetPosition;
    const targetPosition = graph[this.targetPosition];
    const flightsIds = Object.keys(graph);
    const targetPositionId = flightsIds.indexOf(this.targetPosition);

    const targetSeries = this.chart.series.push(
      am5map.MapPointSeries.new(this.root, { idField: 'id' })
    );
    const selectAirport = this.selectAirport;
    const root = this.root;
    targetSeries.bullets.push(function () {
      var circle = am5.Circle.new(root, {
        radius: airports_size,
        tooltipText: 'Target - {title}',
        cursorOverStyle: 'pointer',
        tooltipY: 0,
        fill: am5.color(0xff0000),
        stroke: root.interfaceColors.get('background'),
        strokeWidth: 2,
      });

      circle.events.on('click', () => {
        selectAirport(targetShortName);
      });
      return am5.Bullet.new(root, {
        sprite: circle,
      });
    });

    this.originTargetCities.push({
      id: targetPositionId,
      title: targetPosition.name,
      destinations: targetPosition.destinations,
      geometry: {
        type: 'Point',
        coordinates: [targetPosition.longitude, targetPosition.latitude],
      },
      zoomLevel: 1.5,
      zoomPoint: {
        longitude: 52.4912,
        latitude: -1.9348,
      },
    });
    targetSeries.data.setAll(this.originTargetCities);
    this.targetSeries = targetSeries;
  };

  //This function selects an airport and displays all flights departing from that airport
  selectAirport = (airportId) => {
    // this.setState({ currentId: airportId });
    this.selectedAirport = airportId;
    this.setSelectedAirport(airportId);
    const dataItem = this.airportsSeries.getDataItemById(airportId);
    const dataContext = dataItem.dataContext;
    // this.chart.zoomToGeoPoint(
    //   dataContext.zoomPoint,
    //   dataContext.zoomLevel,
    //   false
    // );

    const destinationsIds = dataContext.destinations;
    const lineSeriesData = [];

    const originLongitude = dataItem.get('longitude');
    const originLatitude = dataItem.get('latitude');

    destinationsIds.map((id) => {
      const destinationDataItem = this.airportsSeries.getDataItemById(id);
      lineSeriesData.push({
        geometry: {
          type: 'LineString',
          coordinates: [
            [originLongitude, originLatitude],
            [
              destinationDataItem.get('longitude'),
              destinationDataItem.get('latitude'),
            ],
          ],
          id: `${airportId} ${id}`,
        },
      });
      return null;
    });
    this.lineSeries.data.setAll(lineSeriesData);

    // for (let i = 1; i < this.lineSeries.children._values.length; i++) {
    //   this.lineSeries.children._values[i].events.on('click', (e) => {
    //     this.setPlane(e.target._dataItem.dataContext.geometry.id);
    //   });
    // }
  };

  //display the current player plane on the screen
  initiatePlane = (selectedAirport, color) => {
    this.spy.id = selectedAirport;
    //create the plane
    const planeSeries = this.chart.series.push(
      am5map.MapPointSeries.new(this.root, {})
    );
    var plane = am5.Graphics.new(this.root, {
      svgPath:
        'm2,106h28l24,30h72l-44,-133h35l80,132h98c21,0 21,34 0,34l-98,0 -80,134h-35l43,-133h-71l-24,30h-28l15,-47',
      scale: plane_size,
      centerY: am5.p50,
      centerX: am5.p50,
      fill: am5.color(color),
    });
    const root = this.root;
    planeSeries.bullets.push(function () {
      var container = am5.Container.new(root, {});
      container.children.push(plane);
      return am5.Bullet.new(root, { sprite: container });
    });

    const lineDataItem = this.allLineSeries.states._entity._dataItems.filter(
      (item) => item.dataContext.geometry.id.substring(0, 3) === selectedAirport
    );

    const planeDataItem = planeSeries.pushDataItem({
      lineDataItem: lineDataItem[0],
      positionOnLine: 0,
      autoRotate: true,
    });
    this.planeSeries = planeSeries;
  };

  //display the opponent player plane on the screen
  initiateOpponentPlane = (id, color, idx) => {
    //create the plane
    const planeSeries = this.chart.series.push(
      am5map.MapPointSeries.new(this.root, {})
    );
    var plane = am5.Graphics.new(this.root, {
      svgPath:
        'm2,106h28l24,30h72l-44,-133h35l80,132h98c21,0 21,34 0,34l-98,0 -80,134h-35l43,-133h-71l-24,30h-28l15,-47',
      scale: plane_size,
      centerY: am5.p50,
      centerX: am5.p50,
      fill: am5.color(color),
      populateText: true,
    });
    const root = this.root;
    planeSeries.bullets.push(function () {
      var container = am5.Container.new(root, {});
      container.children.push(plane);
      return am5.Bullet.new(root, { sprite: container });
    });

    const lineDataItem = this.allLineSeries.states._entity._dataItems.filter(
      (item) => item.dataContext.geometry.id.substring(0, 3) === id
    );

    const planeDataItem = planeSeries.pushDataItem({
      lineDataItem: lineDataItem[0],
      positionOnLine: 0,
      autoRotate: true,
    });

    this.opponentPlaneSeries[idx] = planeSeries;
  };

  //change oponent plane location
  placeOpponentPlane = (ids, agentNum) => {
    const idsArray = ids.split(' ');
    if (idsArray[0] !== this.agents[agentNum].id) return;

    this.chart.series.removeValue(this.opponentPlaneSeries[agentNum]);

    this.opponentPlaneSeries[agentNum] = this.chart.series.push(
      am5map.MapPointSeries.new(this.root, {})
    );

    const plane = am5.Graphics.new(this.root, {
      svgPath:
        'm2,106h28l24,30h72l-44,-133h35l80,132h98c21,0 21,34 0,34l-98,0 -80,134h-35l43,-133h-71l-24,30h-28l15,-47',
      scale: plane_size,
      centerY: am5.p50,
      centerX: am5.p50,
      fill: am5.color(this.agents[agentNum].color),
    });

    const root = this.root;
    this.opponentPlaneSeries[agentNum].bullets.push(function () {
      const container = am5.Container.new(root, {});
      container.children.push(plane);
      return am5.Bullet.new(root, { sprite: container });
    });

    const lineDataItem = this.allLineSeries.states._entity._dataItems.filter(
      (item) => item.dataContext.geometry.id === ids
    );

    const planeDataItem = this.opponentPlaneSeries[agentNum].pushDataItem({
      lineDataItem: lineDataItem[0],
      positionOnLine: 0,
      autoRotate: true,
    });

    planeDataItem.animate({
      key: 'positionOnLine',
      to: 1,
      duration: this.delay,
      loops: false,
      easing: am5.ease.linear,
    });

    this.agents[agentNum].id = idsArray[1];
    this.updateAgentLocationId(this.agents);
  };

  setPlane = (ids) => {
    return new Promise((resolve) => {
      const idsArray = ids.split(' ');
      if (idsArray[0] !== this.spy.id) return; //fly to planes current position

      // const origin = airportsSeries.getDataItemById(idsArray[0]);
      // const des = airportsSeries.getDataItemById(idsArray[1]);

      this.chart.series.removeValue(this.planeSeries);

      this.planeSeries = this.chart.series.push(
        am5map.MapPointSeries.new(this.root, {})
      );

      const plane = am5.Graphics.new(this.root, {
        svgPath:
          'm2,106h28l24,30h72l-44,-133h35l80,132h98c21,0 21,34 0,34l-98,0 -80,134h-35l43,-133h-71l-24,30h-28l15,-47',
        scale: plane_size,
        centerY: am5.p50,
        centerX: am5.p50,
        fill: am5.color(this.spy.color),
      });

      const root = this.root;
      this.planeSeries.bullets.push(function () {
        const container = am5.Container.new(root, {});
        container.children.push(plane);
        return am5.Bullet.new(root, { sprite: container });
      });

      const lineDataItem = this.allLineSeries.states._entity._dataItems.filter(
        (item) => item.dataContext.geometry.id === ids
      );

      const planeDataItem = this.planeSeries.pushDataItem({
        lineDataItem: lineDataItem[0],
        positionOnLine: 0,
        autoRotate: true,
      });

      planeDataItem.animate({
        key: 'positionOnLine',
        to: 1,
        duration: this.delay,
        loops: false,
        easing: am5.ease.linear,
      });

      this.spy.id = idsArray[1];
      this.updateSpyPlaneLocationId(idsArray[1]);
      setTimeout(() => {
        // this.selectAirport(idsArray[1]);

        this.setSplyShortestPathLines();

        resolve(true);
      }, 1000);

      //   planeDataItem.on('positionOnLine', function (value) {
      //     if (value >= 0.99) {
      //       plane.set('rotation', 180);
      //     } else if (value <= 0.01) {
      //       plane.set('rotation', 0);
      //     }
      //   });
    });
  };

  // This function selects an airport and displays all flights departing from that airport
  setSplyShortestPathLines = () => {
    const flightsIds = Object.keys(this.graph);
    const spyIndex = flightsIds.indexOf(this.spy.id);
    const targetIndex = flightsIds.indexOf(this.targetPosition);
    const path = shortest_path(spyIndex, targetIndex, this.graph);
    const pathIds = path.map((i) => flightsIds[i]);

    const lineSeriesData = [];
    for (let i = 0; i < pathIds.length - 1; i++) {
      const dataItem = this.airportsSeries.getDataItemById(pathIds[i]);
      const dataContext = dataItem.dataContext;

      const originLongitude = dataItem.get('longitude');
      const originLatitude = dataItem.get('latitude');

      const destinationDataItem = this.airportsSeries.getDataItemById(
        pathIds[i + 1]
      );
      lineSeriesData.push({
        geometry: {
          type: 'LineString',
          coordinates: [
            [originLongitude, originLatitude],
            [
              destinationDataItem.get('longitude'),
              destinationDataItem.get('latitude'),
            ],
          ],
          id: `${pathIds[i]} ${pathIds[i + 1]}`,
        },
      });
    }

    this.spyShortestPathLines.data.setAll(lineSeriesData);
  };
}
