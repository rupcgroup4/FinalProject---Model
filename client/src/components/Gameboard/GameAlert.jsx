import React from 'react';
import { Alert, AlertTitle } from '@mui/material';

const GameAlert = ({ message }) => {
  if (!message) return;
  return (
    <Alert severity='info'>
      <AlertTitle>Info</AlertTitle>
      <strong>{message}</strong>
    </Alert>
  );
};

export default GameAlert;
