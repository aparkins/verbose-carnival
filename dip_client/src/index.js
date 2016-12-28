import React, {Component} from 'react';
import {createStore, combineReducers} from 'redux';
import {render} from 'react-dom';
import {Provider, connect} from 'react-redux';

import StandardMap from './variants/standard';

const store = createStore(combineReducers({
  user(store = {}, action = {}) {
    return store;
  }
}));

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <StandardMap />
      </Provider>
    );
  }
}

render(<App />, document.querySelector('#root'));

