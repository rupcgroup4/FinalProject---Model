import {
  Dialog,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from '@mui/material';

const GameOverModal = ({ open, setOpen, roleWin }) => {
  const handleClose = () => {
    setOpen(false);
  };
  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby='alert-dialog-title'
        aria-describedby='alert-dialog-description'
      >
        <DialogTitle id='alert-dialog-title'>{'Game over'}</DialogTitle>
        <DialogContent>
          <DialogContentText id='alert-dialog-description'>
            The winner is {roleWin}
          </DialogContentText>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default GameOverModal;
