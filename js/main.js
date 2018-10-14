import React from 'react';
import ReactDOM from 'react-dom';
import ExampleWork from './example-work';

const myWork = [
  {
    'title': "Gather",
    'image': {
      'desc': "Data gathering image",
      'src': "images/gather.png",
      'comment': ""
    }
  },
  {
    'title': "Analyse",
    'image': {
      'desc': "Data analysing image",
      'src': "images/analyse.png",
      'comment': ""
    }
  },
  {
    'title': "Act",
    'image': {
      'desc': "Data adwords mcc image",
      'src': "images/act.png",
      'comment': ""
    }
  }
]
ReactDOM.render(<ExampleWork work={myWork}  />, document.getElementById('example-work'))
