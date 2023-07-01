import FlightTakeoffIcon from '@mui/icons-material/FlightTakeoff';
import { AppBar, Typography, Box, Grid } from '@mui/material';
import GameDescribeButtons from '../Gameboard/GameDescribeButtons';
import Settings from '../Gameboard/Settings';
import FlightIcon from '@mui/icons-material/Flight';
import GameStats from '../Gameboard/GameStats';

function NavBar(props) {
  return (
    <AppBar position='static'>
      <Box display={'flex'} justifyContent={'center'}>
        <Grid
          container
          justifyContent={{ sx: 'center', md: 'center' }}
          spacing={{ xs: 1, md: 8 }}
        >
          <Grid item display={'flex'} alignItems={'center'}>
            <FlightTakeoffIcon
              sx={{ display: { xs: 'flex', md: 'flex' }, mr: 1 }}
            />
            <Typography
              variant='h6'
              noWrap
              component='a'
              href='/'
              sx={{
                mr: 2,
                display: { xs: 'flex', md: 'flex' },
                fontFamily: '"Caveat", "cursive"',
                fontWeight: 700,
                letterSpacing: '.3rem',
                color: 'inherit',
                textDecoration: 'none',
              }}
            >
              Catch Me!
            </Typography>
          </Grid>
          <Grid item display={'flex'} mt={1}>
            <Box display={'flex'} style={{ paddingTop: '11px' }} pr={5}>
              <FlightIcon sx={{ color: '#000000', fontSize: 30 }} />
              <Typography pl={1} sx={{ fontWeight: 700, paddingTop: '3px' }}>
                Spy
              </Typography>
            </Box>
            <Box
              flexDirection={'column'}
              display={'flex'}
              justifyContent={'space-evenly'}
            >
              <Box display={'flex'}>
                <FlightIcon sx={{ color: '#0000ff', fontSize: 30 }} />
                <Typography pl={1} sx={{ fontWeight: 700, paddingTop: '3px' }}>
                  Agent 1
                </Typography>
              </Box>
              <Box display={'flex'}>
                <FlightIcon sx={{ color: '#006400', fontSize: 30 }} />
                <Typography pl={1} sx={{ fontWeight: 700, paddingTop: '3px' }}>
                  Agent 2
                </Typography>
              </Box>
            </Box>
          </Grid>
          <Grid item>
            <GameStats turn={props.turn} steps={props.steps} />
          </Grid>
          <Grid item display={'flex'} alignItems={'center'}>
            <GameDescribeButtons
              step={props.step}
              startGame={props.startGame}
              resetGame={props.resetGame}
            />
          </Grid>
          <Grid item display={'flex'} alignItems={'center'}>
            <Settings
              isAgentModel={props.isAgentModel}
              setIsAgentModel={props.setIsAgentModel}
              isSpyModel={props.isSpyModel}
              setIsSpyModel={props.setIsSpyModel}
              isTrainedAgent={props.isTrainedAgent}
              setIsTrainedAgent={props.setIsTrainedAgent}
              isTrainedSpy={props.isTrainedSpy}
              setIsTrainedSpy={props.setIsTrainedSpy}
              game_state={props.game_state}
              SetGameState={props.SetGameState}
              spyModel={props.spyModel}
              setSpyModel={props.setSpyModel}
              all_states={props.all_states}
              all_spy_models={props.all_spy_models}
              agentsModelSelection={props.agentsModelSelection}
              setAgentsModelSelection={props.setAgentsModelSelection}
              all_agents_models={props.all_agents_models}
            />
          </Grid>
        </Grid>
      </Box>
    </AppBar>
  );
}
export default NavBar;
