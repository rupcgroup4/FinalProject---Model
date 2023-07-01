import React from 'react';
import { Grid, Box } from '@mui/material';
import '../../CSS/buttonsCSS.css';

const GameDescribeButtons = ({ step, startGame, resetGame }) => {
  return (
    <Grid item xs={12}>
      <Box display={'flex'} justifyContent={'center'} alignItems={'center'}>
        <Box mr={2} ml={1}>
          <button onClick={step} className='start-btn'>
            STEP
          </button>
        </Box>
        <Box mr={2} ml={1}>
          <button onClick={startGame} className='start-btn'>
            START
          </button>
        </Box>
        <Box mr={1} ml={1}>
          <button onClick={resetGame} className='start-btn'>
            RESET
          </button>
        </Box>
      </Box>
      <br />
    </Grid>
  );
};

export default GameDescribeButtons;
