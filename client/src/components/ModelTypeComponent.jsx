import React from 'react';
import { Switch, Stack, Typography } from '@mui/material';

export default function ModelTypeComponent(props) {
  const handleChangeOnModelType = (event) => {
    console.log('onChange - ', event.target.checked);
    props.setisTrainedModel(event.target.checked);
  };

  return (
    <Stack
      direction='row'
      spacing={1}
      alignItems='center'
      style={{ zIndex: '1300' }}
    >
      <Typography>Off</Typography>
      <Switch
        onChange={handleChangeOnModelType}
        defaultChecked
        inputProps={{ 'aria-label': 'ant design' }}
      />

      <Typography>Trained</Typography>
    </Stack>
  );
}
