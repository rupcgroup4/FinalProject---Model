import React, { useState } from 'react';
import SettingsIcon from '@mui/icons-material/Settings';
import { Grid, IconButton, Menu, Box } from '@mui/material';

import ModelToggle from '../Gameboard/ModelToggle';
import ChooseStates from './ChooseStates';
import ChooseModel from './ChooseModel';
import '../../CSS/settings.css';

const Settings = ({
  isAgentModel,
  setIsAgentModel,
  isSpyModel,
  setIsSpyModel,
  isTrainedAgent,
  setIsTrainedAgent,
  isTrainedSpy,
  setIsTrainedSpy,
  game_state,
  SetGameState,
  spyModel,
  setSpyModel,
  all_states,
  all_spy_models,
  agentsModelSelection,
  setAgentsModelSelection,
  all_agents_models,
}) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  return (
    <Box sx={{ overflowX: 'auto' }}>
      <Grid className='settingCSS' sx={{ overflowX: 'auto' }}>
        <IconButton
          aria-label='more'
          id='long-button'
          aria-controls={open ? 'long-menu' : undefined}
          aria-expanded={open ? 'true' : undefined}
          aria-haspopup='true'
          onClick={handleClick}
          sx={{ color: 'white' }}
        >
          <SettingsIcon fontSize='large' />
        </IconButton>
        <Menu
          id='long-menu'
          MenuListProps={{
            'aria-labelledby': 'long-button',
          }}
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
        >
          <Grid m={2} sx={{ overflowX: 'auto' }} className='example'>
            <ModelToggle
              role='Spy'
              isModel={isSpyModel}
              setIsModel={setIsSpyModel}
              isTrained={isTrainedSpy}
              setIsTrained={setIsTrainedSpy}
              game_model={spyModel}
              SetGameModel={setSpyModel}
              all_models={all_spy_models}
            />
            <ModelToggle
              role='Agents'
              isModel={isAgentModel}
              setIsModel={setIsAgentModel}
              isTrained={isTrainedAgent}
              setIsTrained={setIsTrainedAgent}
              game_model={agentsModelSelection}
              SetGameModel={setAgentsModelSelection}
              all_models={all_agents_models}
            />
          </Grid>
          <Box display={'flex'} justifyContent={'center'}>
            <ChooseStates
              game_state={game_state}
              SetGameState={SetGameState}
              all_states={all_states}
            />
          </Box>
        </Menu>
      </Grid>
    </Box>
  );
};

export default Settings;
