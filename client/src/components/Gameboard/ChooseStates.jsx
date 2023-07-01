import React from 'react';
import { InputLabel, MenuItem, FormControl, Select } from '@mui/material';

const ChooseStates = (props) => {
  const handleChangeState = (event) => {
    props.SetGameState(event.target.value);
  };

  return (
    <FormControl required sx={{ m: 1, minWidth: 220 }}>
      <InputLabel>State</InputLabel>
      <Select
        value={props.game_state}
        label='States'
        onChange={handleChangeState}
      >
        {props.all_states?.map((state, idx) => (
          <MenuItem key={idx} value={state}>
            {state}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default ChooseStates;
