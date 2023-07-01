import React from 'react';
import {
  Grid,
  Box,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
} from '@mui/material';
import SyncIcon from '@mui/icons-material/Sync';
import FlightTakeoffIcon from '@mui/icons-material/FlightTakeoff';

const GameStats = ({ turn, steps }) => {
  return (
    <Grid item>
      <Box display={'flex'} alignItems={'center'} p={3}>
        <Box>
          <ListItem>
            <ListItemAvatar>
              <Avatar>
                <SyncIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText sx={{ width: 100 }} primary={`Turn: ${turn}`} />
          </ListItem>
        </Box>
        <Box>
          <ListItem>
            <ListItemAvatar>
              <Avatar>
                <FlightTakeoffIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText primary={`Steps played: ${steps}`} />
          </ListItem>
        </Box>
      </Box>
    </Grid>
  );
};

export default GameStats;
