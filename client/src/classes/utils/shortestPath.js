export const shortest_path = (node1, node2, graph) => {
  const flights = convertGraphToShortestPathAlogorithm(graph);
  const path_list = [[node1]];
  let path_index = 0;
  //To keep track of previously visited nodes
  const previous_nodes = [node1];
  if (node1 === node2) return path_list[0];

  while (path_index < path_list.length) {
    const current_path = path_list[path_index];
    const last_node = current_path.at(-1);
    const next_nodes = flights[last_node]['destinations'];
    //Search goal node
    if (next_nodes.includes(node2)) {
      current_path.push(node2);
      return current_path;
    }

    //Add new paths
    for (const next_node in next_nodes) {
      if (!previous_nodes.includes(next_nodes[next_node])) {
        const new_path = JSON.parse(JSON.stringify(current_path));

        new_path.push(next_nodes[next_node]);
        path_list.push(new_path);
        // To avoid backtracking
        previous_nodes.push(next_nodes[next_node]);
      }
    }
    //Continue to next path in list
    path_index += 1;
  }
  //No path is found
  return [];
};

const convertGraphToShortestPathAlogorithm = (graph) => {
  const ids = Object.keys(graph);
  const obj = [];

  for (let i = 0; i < ids.length; i++) {
    const destinations = graph[ids[i]].destinations.map((dest) =>
      ids.indexOf(dest)
    );

    obj.push({
      id: ids[i],
      destinations: destinations,
    });
  }

  return obj;
};
