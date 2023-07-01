import React, { useLayoutEffect } from 'react';

const GameMap = ({ map, graph }) => {
  //on the first time hte component is loaded it will create new Map to the screen
  //this happens only once
  useLayoutEffect(() => {
    if (map) {
      map.createMap(graph);

      return () => {
        map.root.dispose();
      };
    }
  }, [graph, map]);

  return (
    <div
      id='chartdiv'
      style={{
        width: '100%',
        height: '90vh',
        margin: '0 auto',
      }}
    ></div>
  );
};

export default GameMap;
