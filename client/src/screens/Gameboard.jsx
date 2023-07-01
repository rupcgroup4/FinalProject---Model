import React, { useState, useEffect, useCallback, useRef } from 'react';
import GameMap from '../components/Gameboard/GameMap';
import { graph } from '../classes/utils/flight_graph';
import Map from '../classes/Map';
import axios from 'axios';
import { Box, Grid } from '@mui/material';
import GameAlert from '../components/Gameboard/GameAlert';
import GameOverModal from '../components/Gameboard/GameOverModal';
import { shortest_path } from '../classes/utils/shortestPath';
import NavBar from '../components/NavBar/NavBar';

const url = 'http://localhost:8000';
// const url = 'http://54.210.170.221';

const states = [
  {
    init_spy_position: 0,
    init_agent1_position: 6,
    init_agent2_position: 14,
    init_target_position: 9,
  },
  {
    init_spy_position: 9,
    init_agent1_position: 6,
    init_agent2_position: 14,
    init_target_position: 0,
  },
  {
    init_spy_position: 12,
    init_agent1_position: 6,
    init_agent2_position: 4,
    init_target_position: 2,
  },
  {
    init_spy_position: 2,
    init_agent1_position: 6,
    init_agent2_position: 4,
    init_target_position: 12,
  },
];

const spy_color = '#000000';
const agent1Color = '#0000ff';
const agent2Color = '#006400';

const flightsIds = Object.keys(graph);

//States to print in settings tool
const all_states = states.map((item) => {
  return [
    flightsIds[item.init_spy_position],
    flightsIds[item.init_agent1_position],
    flightsIds[item.init_agent2_position],
    flightsIds[item.init_target_position],
  ].join(' - ');
});

const all_spy_models = [
  'SpyEnv',
  'spy_50k_vs_agents_0k',
  'spy_200k_vs_agents_50k',
];

const all_agents_models = [
  'AgentsEnv',
  'agents_50k_vs_spy_50k',
  'agents_100k_vs_spy_200k',
];

const Gameboard = () => {
  const delay = 500;
  const [theme, setTheme] = useState(false);

  const [autoGame, setAutoGame] = useState(false);
  const [turn, setTurn] = useState(null);
  const [steps, setSteps] = useState(null);
  //
  const [winner, setWinner] = useState(null);
  //
  const [isGameOver, setIsGameOver] = useState(false);
  //
  const [roleWin, setRoleWin] = useState('');

  const [isAgentModel, setIsAgentModel] = useState(true);
  const [isTrainedAgent, setIsTrainedAgent] = useState(true);
  const [isSpyModel, setIsSpyModel] = useState(true);
  const [isTrainedSpy, setIsTrainedSpy] = useState(true);

  const intervalRef = useRef();

  //Hold map class object
  const [map, setMap] = useState(null);
  //current selected airport on the map
  const [selectedAirport, setSelectedAirport] = useState();
  //current tagert position on the map
  const [targetPosition, setTargetPosition] = useState(null);
  //player plane current location on the map
  const [spy, setSpy] = useState(null);
  //opponent player current location on the map
  const [agents, setAgents] = useState([]);
  //messgae for game describe
  const [gameDescribeMessage, setGameDescribeMessage] = useState('');

  const [game_state, SetGameState] = useState(all_states[0]);
  const [spyModel, setSpyModel] = useState(all_spy_models[0]);
  const [agentsModelSelection, setAgentsModelSelection] = useState(
    all_agents_models[0]
  );

  const [init_spy_position, set_spy_position] = useState(
    states[0].init_spy_position
  );
  const [init_agent1_position, set_init_agent1_position] = useState(
    states[0].init_agent1_position
  );
  const [init_agent2_position, set_init_agent2_position] = useState(
    states[0].init_agent2_position
  );
  const [init_target_position, set_init_target_position] = useState(
    states[0].init_target_position
  );

  useEffect(() => {
    const index = all_states.indexOf(game_state);
    set_spy_position(states[index].init_spy_position);
    set_init_agent1_position(states[index].init_agent1_position);
    set_init_agent2_position(states[index].init_agent2_position);
    set_init_target_position(states[index].init_target_position);
    // createNewMap();
  }, [game_state]);

  const sleep = (time) => {
    return new Promise((resolve) => setTimeout(resolve, time));
  };

  const updateSpyLocationId = (newId) => {
    setSpy({ id: newId, color: spy_color });
  };

  const updateAgentLocationId = (agents) => {
    setAgents(agents);
  };

  const createNewMap = useCallback(
    (initial_spy, initial_agents, init_target_position) => {
      const map = new Map(
        structuredClone(initial_spy),
        updateSpyLocationId,
        structuredClone(initial_agents),
        updateAgentLocationId,
        setSelectedAirport,
        flightsIds[init_target_position],
        delay
      );
      setMap(map);
    },
    []
  );

  const agentMove = useCallback(
    (location, agentNum) => {
      setGameDescribeMessage(
        `Agent ${agentNum + 1} moved from ${
          graph[agents[agentNum].id].name
        } to ${graph[location].name}`
      );
      map.placeOpponentPlane(`${agents[agentNum].id} ${location}`, agentNum);
      if (turn === 'agent 1') {
        setSteps((prev) => prev + 1);
        setTurn('agent 2');
      } else {
        setTurn('spy');
      }
    },
    [agents, map, turn]
  );

  const checkWin = useCallback(
    (spyId, agent1Id, agent2Id) => {
      const isSpyWin = spyId === targetPosition;
      const isAgentsWin = agent1Id === spyId || agent2Id === spyId;

      if (isSpyWin || isAgentsWin) {
        setTurn('');
        setAutoGame(false);
        setIsGameOver(true);
      }
      if (isAgentsWin) {
        setRoleWin('Agents');
      } else if (isSpyWin) {
        setRoleWin('Spy');
      }

      setTimeout(() => {
        setGameDescribeMessage('');
      }, 2000);

      return isSpyWin || isAgentsWin;
    },
    [targetPosition]
  );

  const agentsModel = useCallback(async () => {
    const res = await axios.post(`${url}/agents`, {
      spy_position: spy.id,
      agent1_position: agents[0].id,
      agent2_position: agents[1].id,
      target_position: targetPosition,
      isNew: isTrainedAgent,
      model: agentsModelSelection,
    });

    const { result } = res.data;

    return result;
  }, [spy?.id, agents, targetPosition, isTrainedAgent, agentsModelSelection]);

  const agentsShortestPath = useCallback(
    (agentNum) => {
      const flightsIds = Object.keys(graph);
      const spyIndex = flightsIds.indexOf(spy.id);
      const agentIndex = flightsIds.indexOf(agents[agentNum].id);
      const path = shortest_path(agentIndex, spyIndex, graph);

      const pathIds = path.map((i) => flightsIds[i]);
      return pathIds[1];
    },
    [agents, spy?.id]
  );

  const playAgents = useCallback(
    async (spyLocation) => {
      let modelResult;
      if (isAgentModel) {
        modelResult = await agentsModel();
      }

      checkWin(spyLocation, modelResult[0], modelResult[1]);
      await sleep(delay);

      for (let i = 0; i < agents.length; i++) {
        if (isAgentModel) {
          agentMove(modelResult[i], i);
        } else {
          agentMove(agentsShortestPath(i), i);
        }

        await sleep(delay);
      }
    },
    [
      agentMove,
      agents.length,
      agentsModel,
      agentsShortestPath,
      checkWin,
      isAgentModel,
    ]
  );

  const spyMove = useCallback(
    async (location) => {
      setGameDescribeMessage(
        `Spy moved from ${graph[spy.id].name} to ${graph[location].name}`
      );
      await map.setPlane(`${spy.id} ${location}`);
      setTurn('agent 1');
      setSteps((prev) => prev + 1);
      if (!checkWin(location, agents[0].id, agents[1].id)) {
        playAgents(location);
      }
    },
    [spy?.id, map, checkWin, agents, playAgents]
  );

  const PlaySpy = useCallback(async () => {
    const res = await axios.post(`${url}/spy`, {
      spy_position: spy.id,
      agent1_position: agents[0].id,
      agent2_position: agents[1].id,
      target_position: targetPosition,
      isNew: isTrainedSpy,
      model: spyModel,
    });

    const { result } = res.data;
    spyMove(result);
  }, [spy?.id, agents, targetPosition, isTrainedSpy, spyModel, spyMove]);

  const createGame = useCallback(() => {
    setAutoGame(false);
    setWinner(null);
    setSteps(0);
    setTargetPosition(flightsIds[init_target_position]);

    const initial_spy = {
      id: flightsIds[init_spy_position],
      color: spy_color,
    };
    setSpy(initial_spy);

    const initial_agents = [
      { id: flightsIds[init_agent1_position], color: agent1Color },
      { id: flightsIds[init_agent2_position], color: agent2Color },
    ];
    setAgents(initial_agents);

    setTurn('spy');
    createNewMap(initial_spy, initial_agents, init_target_position);
  }, [
    createNewMap,
    init_agent1_position,
    init_agent2_position,
    init_spy_position,
    init_target_position,
  ]);

  const resetGame = () => {
    createGame();
  };

  const playStep = () => {
    if (isSpyModel && isAgentModel) PlaySpy();
  };

  const startGame = () => {
    setAutoGame(true);
  };

  useEffect(() => {
    createGame();
  }, [createGame]);

  useEffect(() => {
    if (autoGame) {
      const interval = setInterval(() => {
        PlaySpy();
      }, delay * 3);
      intervalRef.current = interval;
      return () => clearInterval(intervalRef.current);
    }
  }, [PlaySpy, autoGame]);

  console.log(agentsModelSelection);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <NavBar
        theme={theme}
        setTheme={setTheme}
        steps={steps}
        turn={turn}
        step={playStep}
        startGame={startGame}
        resetGame={resetGame}
        isAgentModel={isAgentModel}
        setIsAgentModel={setIsAgentModel}
        isSpyModel={isSpyModel}
        setIsSpyModel={setIsSpyModel}
        isTrainedAgent={isTrainedAgent}
        setIsTrainedAgent={setIsTrainedAgent}
        isTrainedSpy={isTrainedSpy}
        setIsTrainedSpy={setIsTrainedSpy}
        game_state={game_state}
        SetGameState={SetGameState}
        spyModel={spyModel}
        setSpyModel={setSpyModel}
        all_states={all_states}
        all_spy_models={all_spy_models}
        agentsModelSelection={agentsModelSelection}
        setAgentsModelSelection={setAgentsModelSelection}
        all_agents_models={all_agents_models}
      />
      <Grid container spacing={0.5}>
        <Grid item xs={12} md={12}>
          <Box>
            <GameMap map={map} graph={graph} />
          </Box>
          <GameAlert message={gameDescribeMessage} />
        </Grid>
      </Grid>
      <GameOverModal
        open={isGameOver}
        setOpen={setIsGameOver}
        roleWin={roleWin}
      />
    </Box>
  );
};

export default Gameboard;
