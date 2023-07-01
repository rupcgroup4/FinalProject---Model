export const graph = {
  //Top right
  BKK: {
    name: 'Suvarnabhumi Intl',
    latitude: '13.681108',
    longitude: '100.747283',
    destinations: ['TLV', 'AGP', 'TPE', 'NIM'],
  },
  TPE: {
    name: 'Taoyuan Intl',
    latitude: '25.077731',
    longitude: '121.232822',
    destinations: ['HAM', 'BKK'],
  },
  HAM: {
    name: 'Hamburg',
    latitude: '53.630389',
    longitude: '9.988228',
    destinations: ['AGP', 'TPE', 'VAN'],
  },
  AGP: {
    name: 'Malaga',
    latitude: '36.6749',
    longitude: '-4.499106',
    destinations: ['HAM', 'TLV', 'BKK', 'ELU', 'MEM'],
  },
  TLV: {
    name: 'Ben Gurion',
    latitude: '32.011389',
    longitude: '34.886667',
    destinations: ['BKK', 'AGP', 'JIJ'],
  },
  //Top left
  JFK: {
    name: 'John F Kennedy Intl',
    latitude: '40.639751',
    longitude: '-73.778925',
    destinations: ['VAN', 'MEM'],
  },
  MEM: {
    name: 'Memphis Intl',
    latitude: '35.042417',
    longitude: '-89.976667',
    destinations: ['JFK', 'BJX', 'AGP', 'CAY'],
  },
  BJX: {
    name: 'Guanajuato Intl',
    latitude: '20.993464',
    longitude: '-101.480847',
    destinations: ['MEM', 'SFO', 'VAN', 'CUE'],
  },
  SFO: {
    name: 'San Francisco Intl',
    latitude: '37.618972',
    longitude: '-122.374889',
    destinations: ['BJX', 'VAN', 'CPO'],
  },
  VAN: {
    name: 'Vancouver',
    latitude: '49.252433',
    longitude: '-122.645437',
    destinations: ['SFO', 'BJX', 'JFK', 'HAM'],
  },
  //Botom left
  SDU: {
    name: 'Rio De Janeiro',
    longitude: '-43.163133',
    latitude: '-22.910461',
    destinations: ['CAY', 'EZE', 'ELL'],
  },
  CPO: {
    name: 'Copiapo Chile',
    longitude: '-70',
    latitude: '-27',
    destinations: ['EZE', 'CUE', 'SFO'],
  },
  EZE: {
    name: 'Buenos Aires',
    longitude: '-58.535833',
    latitude: '-34.822222',
    destinations: ['CPO', 'CUE', 'SDU', 'TNR'],
  },
  CUE: {
    name: 'Mariscal Lamar',
    longitude: '-78.984397',
    latitude: '-2.889467',
    destinations: ['CPO', 'EZE', 'CAY', 'BJX'],
  },
  CAY: {
    name: 'French Guiana',
    longitude: '-52.360447',
    latitude: '4.819808',
    destinations: ['CUE', 'SDU', 'MEM', 'ELU'],
  },
  //bottom right
  ELU: {
    name: 'Guemar Algeria',
    longitude: '6.77679',
    latitude: '33.5114',
    destinations: ['JIJ', 'ELL', 'CAY', 'AGP'],
  },
  ELL: {
    name: 'South Africa',
    longitude: '27.75',
    latitude: '-23.666667',
    destinations: ['SDU', 'ELU', 'TNR', 'NIM'],
  },
  TNR: {
    name: 'Madagascar',
    longitude: '47.478806',
    latitude: '-18.79695',
    destinations: ['ELL', 'NIM', 'EZE'],
  },
  JIJ: {
    name: 'Ethiopia',
    longitude: '42.7875',
    latitude: '9.359722',
    destinations: ['TLV', 'NIM', 'ELU'],
  },
  NIM: {
    name: 'Niger',
    longitude: '2.183614',
    latitude: '13.481547',
    destinations: ['JIJ', 'TNR', 'ELL', 'BKK'],
  },
};
