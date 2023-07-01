import React from 'react';
import { InputLabel, MenuItem, FormControl, Select } from '@mui/material';

const ChooseModel = (props) => {
  const handleChangeModel = (event) => {
    props.SetGameModel(event.target.value);
  };

  return (
    <FormControl required sx={{ m: 1, minWidth: 220 }}>
      <InputLabel>Model</InputLabel>
      <Select
        value={props.game_model}
        label='Model'
        onChange={handleChangeModel}
      >
        {props.all_models?.map((model, idx) => (
          <MenuItem key={idx} value={model}>
            {model}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default ChooseModel;
