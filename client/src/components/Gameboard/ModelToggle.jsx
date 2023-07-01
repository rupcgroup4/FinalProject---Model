import React from 'react';
import { Box, Switch, Typography, Grid, ListItem } from '@mui/material';
import ChooseModel from '../Gameboard/ChooseModel';

const ModelToggle = ({
  role,
  isTrained,
  setIsTrained,
  game_model,
  SetGameModel,
  all_models,
}) => {
  return (
    <Grid item xs={6}>
      <Box
        display={'flex'}
        // width={"100%"}
        justifyContent={'center'}
        width={400}
      >
        <ListItem>
          <Switch
            onChange={() => setIsTrained((prev) => !prev)}
            checked={isTrained}
          />
          <Typography>Trained {role}</Typography>
        </ListItem>
        <ListItem>
          <ChooseModel
            game_model={game_model}
            SetGameModel={SetGameModel}
            all_models={all_models}
          />
        </ListItem>
      </Box>
    </Grid>
  );
};

export default ModelToggle;
